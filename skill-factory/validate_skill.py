#!/usr/bin/env python3
"""
Claude Skills Validator
Validates generated skills against Anthropic's schema requirements

Usage:
    python validate_skill.py <skill_folder_path>
    python validate_skill.py <skill_folder_path> --strict
    python validate_skill.py <skill_folder_path> --verbose
"""

import re
import ast
import yaml
import json
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    severity: Severity
    message: str
    location: str = ""
    line_number: Optional[int] = None
    fix_suggestion: str = ""
    
    def __str__(self):
        result = f"[{self.severity.value}] {self.message}"
        if self.location:
            result += f"\n  Location: {self.location}"
            if self.line_number:
                result += f" (line {self.line_number})"
        if self.fix_suggestion:
            result += f"\n  Fix: {self.fix_suggestion}"
        return result


class SkillValidator:
    """Validates Claude Skills structure and content"""
    
    # REQUIRED: Define these constants
    REQUIRED_FRONTMATTER_KEYS = ['name', 'description', 'license']
    
    REQUIRED_SECTION_PATTERNS = [
        (r'^#\s+.+$', "Main skill title (H1 header)"),
        (r'^##\s+(?:Overview|About)', "Overview or About section"),
        (r'^##\s+(?:When to Use|Usage)', "When to Use or Usage section"),
        (r'^##\s+(?:How to Use|Instructions)', "How to Use or Instructions section"),
    ]
    
    FORBIDDEN_PATTERNS = [
        (r'\byou\b', "Second-person pronoun 'you'", "Use imperative form instead (e.g., 'Load the file' not 'You should load')"),
        (r'\byour\b', "Second-person possessive 'your'", "Use imperative form instead (e.g., 'the file' not 'your file')"),
        (r'\[(?!SKILL_NAME|skill-name).*?\]', "Placeholder text in brackets", "Replace [PLACEHOLDER] with actual content"),
        (r'Lorem ipsum', "Lorem ipsum placeholder", "Replace with real content"),
        (r'TODO:', "TODO comment", "Complete TODO before finalizing"),
        (r'FIXME:', "FIXME comment", "Fix issue before finalizing"),
        (r'XXX:', "XXX marker", "Resolve marked issue"),
    ]
    
    SECRETS_PATTERNS = [
        (r'api[_-]?key[\s]*[:=][\s]*["\']?[a-zA-Z0-9]{20,}', "Possible API key"),
        (r'password[\s]*[:=][\s]*["\'][^"\']+["\']', "Hardcoded password"),
        (r'secret[\s]*[:=][\s]*["\'][^"\']+["\']', "Hardcoded secret"),
        (r'(sk|pk)_live_[a-zA-Z0-9]{32,}', "API key pattern (Stripe-like)"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub personal access token"),
        (r'xox[baprs]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}', "Slack token"),
        (r'AKIA[0-9A-Z]{16}', "AWS Access Key ID"),
        (r'["\']?access_token["\']?\s*[:=]\s*["\'][^"\']+["\']', "Access token"),
    ]
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_md_path = self.skill_path / "SKILL.md"
        self.issues: List[ValidationIssue] = []
    
    def validate(self) -> Tuple[bool, List[ValidationIssue]]:
        """
        Run all validations on the skill
        Returns: (is_valid, list_of_issues)
        """
        try:
            # Check skill_path exists and is directory
            if not self.skill_path.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Skill path does not exist: {self.skill_path}",
                    fix_suggestion="Ensure the path is correct and the directory exists"
                ))
                return False, self.issues
            
            if not self.skill_path.is_dir():
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Skill path is not a directory: {self.skill_path}",
                    fix_suggestion="Provide a path to a skill directory, not a file"
                ))
                return False, self.issues
            
            # Check SKILL.md exists
            if not self.skill_md_path.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message="SKILL.md file not found",
                    location=str(self.skill_path),
                    fix_suggestion="Every skill must have a SKILL.md file in the root directory"
                ))
                return False, self.issues
            
            # Call all validation methods
            self._validate_skill_md()
            self._validate_file_structure()
            self._validate_python_scripts()
            self._validate_content_quality()
            self._check_for_secrets()
            
            # Check if there are any errors
            has_errors = any(issue.severity == Severity.ERROR for issue in self.issues)
            
            return not has_errors, self.issues
            
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Unexpected error during validation: {str(e)}",
                fix_suggestion="Please report this error"
            ))
            return False, self.issues
    
    def _validate_skill_md(self):
        """Validate SKILL.md structure and formatting"""
        try:
            # Read SKILL.md content
            content = self.skill_md_path.read_text(encoding='utf-8')
            
            # Check starts with "---\n" (YAML frontmatter)
            if not content.startswith('---\n'):
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message="SKILL.md must start with YAML frontmatter (---)",
                    location="SKILL.md",
                    line_number=1,
                    fix_suggestion="Add YAML frontmatter at the top:\n---\nname: skill-name\ndescription: ...\nlicense: ...\n---"
                ))
                return
            
            # Extract and parse YAML frontmatter
            try:
                # Find the end of frontmatter
                parts = content.split('---\n', 2)
                if len(parts) < 3:
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message="YAML frontmatter not properly closed with '---'",
                        location="SKILL.md",
                        fix_suggestion="Ensure frontmatter ends with '---' on its own line"
                    ))
                    return
                
                frontmatter_text = parts[1]
                body = parts[2]
                
                # Parse YAML
                frontmatter = yaml.safe_load(frontmatter_text)
                
                if frontmatter is None:
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message="YAML frontmatter is empty",
                        location="SKILL.md",
                        fix_suggestion="Add required fields: name, description, license"
                    ))
                    return
                
                # Validate required frontmatter keys
                for key in self.REQUIRED_FRONTMATTER_KEYS:
                    if key not in frontmatter:
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            message=f"Missing required frontmatter key: '{key}'",
                            location="SKILL.md (frontmatter)",
                            fix_suggestion=f"Add '{key}: <value>' to the YAML frontmatter"
                        ))
                
                # Validate frontmatter values
                if 'name' in frontmatter:
                    name = frontmatter['name']
                    if not isinstance(name, str) or not name:
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            message="'name' must be a non-empty string",
                            location="SKILL.md (frontmatter)",
                            fix_suggestion="Set name to a lowercase string with hyphens (e.g., 'my-skill')"
                        ))
                    elif not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', name):
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Skill name '{name}' should use lowercase and hyphens only",
                            location="SKILL.md (frontmatter)",
                            fix_suggestion="Use format: lowercase-with-hyphens (e.g., 'my-skill-name')"
                        ))
                
                if 'description' in frontmatter:
                    desc = frontmatter['description']
                    if not isinstance(desc, str) or not desc:
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            message="'description' must be a non-empty string",
                            location="SKILL.md (frontmatter)",
                            fix_suggestion="Add a clear description of when this skill should be used"
                        ))
                    else:
                        # Check description length
                        word_count = len(desc.split())
                        if word_count < 10:
                            self.issues.append(ValidationIssue(
                                severity=Severity.WARNING,
                                message=f"Description is very short ({word_count} words)",
                                location="SKILL.md (frontmatter)",
                                fix_suggestion="Add more detail (aim for 20-50 words) about when and how to use this skill"
                            ))
                        elif word_count > 100:
                            self.issues.append(ValidationIssue(
                                severity=Severity.WARNING,
                                message=f"Description is very long ({word_count} words)",
                                location="SKILL.md (frontmatter)",
                                fix_suggestion="Keep description concise (20-50 words) - details go in the body"
                            ))
                        
                        # Check for second-person in description
                        if re.search(r'\byou\b|\byour\b', desc, re.IGNORECASE):
                            self.issues.append(ValidationIssue(
                                severity=Severity.ERROR,
                                message="Description contains second-person pronouns (you/your)",
                                location="SKILL.md (frontmatter - description)",
                                fix_suggestion="Use third-person: 'This skill should be used when...' not 'Use this when you...'"
                            ))
                
                # Check for required markdown sections in body
                for pattern, description in self.REQUIRED_SECTION_PATTERNS:
                    if not re.search(pattern, body, re.MULTILINE):
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Missing recommended section: {description}",
                            location="SKILL.md (body)",
                            fix_suggestion=f"Add a section for {description}"
                        ))
                
                # Check for forbidden patterns
                lines = body.split('\n')
                for line_num, line in enumerate(lines, 1):
                    for pattern, name, fix in self.FORBIDDEN_PATTERNS:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.issues.append(ValidationIssue(
                                severity=Severity.ERROR if 'you' in name.lower() else Severity.WARNING,
                                message=f"Found {name}: '{line.strip()[:50]}...'",
                                location="SKILL.md",
                                line_number=line_num + frontmatter_text.count('\n') + 2,
                                fix_suggestion=fix
                            ))
                
                # Validate word count
                word_count = len(body.split())
                if word_count < 50:
                    self.issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"SKILL.md body is very short ({word_count} words)",
                        location="SKILL.md",
                        fix_suggestion="Add more detail about how to use the skill (aim for 200-5000 words)"
                    ))
                elif word_count > 5000:
                    self.issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"SKILL.md body is very long ({word_count} words)",
                        location="SKILL.md",
                        fix_suggestion="Consider moving detailed content to references/ folder (keep SKILL.md under 5000 words)"
                    ))
                
            except yaml.YAMLError as e:
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"YAML frontmatter parsing error: {str(e)}",
                    location="SKILL.md (frontmatter)",
                    fix_suggestion="Check YAML syntax - ensure proper indentation and format"
                ))
                
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Error reading SKILL.md: {str(e)}",
                location="SKILL.md",
                fix_suggestion="Ensure file is readable and properly encoded (UTF-8)"
            ))
    
    def _validate_file_structure(self):
        """Validate directory structure and file naming conventions"""
        try:
            # Check folder name uses lowercase and hyphens
            folder_name = self.skill_path.name
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', folder_name):
                self.issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Skill folder name '{folder_name}' should use lowercase and hyphens only",
                    location=str(self.skill_path),
                    fix_suggestion="Rename folder to use format: lowercase-with-hyphens"
                ))
            
            # Check for unexpected files in root
            expected_root_items = {'SKILL.md', 'scripts', 'references', 'assets', 'TESTING_GUIDE', 
                                   'LICENSE.txt', 'LICENSE', 'README.md', 'manifest.json', 
                                   '.gitignore', folder_name + '.zip'}
            
            for item in self.skill_path.iterdir():
                if item.name.startswith('.'):
                    continue  # Hidden files are okay
                if item.name not in expected_root_items:
                    self.issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        message=f"Unexpected item in skill root: {item.name}",
                        location=str(item),
                        fix_suggestion="Only include: SKILL.md, scripts/, references/, assets/, TESTING_GUIDE/, LICENSE.txt"
                    ))
            
            # Validate scripts/ folder
            scripts_dir = self.skill_path / "scripts"
            if scripts_dir.exists():
                if not scripts_dir.is_dir():
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message="'scripts' exists but is not a directory",
                        location=str(scripts_dir),
                        fix_suggestion="Remove the file and create a directory if scripts are needed"
                    ))
                else:
                    py_files = list(scripts_dir.glob("*.py"))
                    if not py_files:
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message="scripts/ folder exists but contains no .py files",
                            location=str(scripts_dir),
                            fix_suggestion="Remove empty scripts/ folder or add Python scripts"
                        ))
            
            # Validate references/ folder
            references_dir = self.skill_path / "references"
            if references_dir.exists():
                if not references_dir.is_dir():
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message="'references' exists but is not a directory",
                        location=str(references_dir),
                        fix_suggestion="Remove the file and create a directory if references are needed"
                    ))
                else:
                    doc_files = list(references_dir.glob("*.md")) + list(references_dir.glob("*.txt"))
                    if not doc_files:
                        self.issues.append(ValidationIssue(
                            severity=Severity.INFO,
                            message="references/ folder exists but contains no documentation files",
                            location=str(references_dir),
                            fix_suggestion="Add .md or .txt reference files or remove empty folder"
                        ))
            
            # Validate assets/ folder
            assets_dir = self.skill_path / "assets"
            if assets_dir.exists() and not assets_dir.is_dir():
                self.issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    message="'assets' exists but is not a directory",
                    location=str(assets_dir),
                    fix_suggestion="Remove the file and create a directory if assets are needed"
                ))
            
            # Check TESTING_GUIDE exists (info only)
            testing_guide_dir = self.skill_path / "TESTING_GUIDE"
            if not testing_guide_dir.exists():
                self.issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    message="No TESTING_GUIDE/ folder found",
                    location=str(self.skill_path),
                    fix_suggestion="Consider adding TESTING_GUIDE/ with sample data and test scenarios"
                ))
                
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Error validating file structure: {str(e)}",
                fix_suggestion="Ensure directory permissions allow reading"
            ))
    
    def _validate_python_scripts(self):
        """Validate Python scripts if present"""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return
        
        try:
            py_files = list(scripts_dir.glob("*.py"))
            
            for py_file in py_files:
                try:
                    content = py_file.read_text(encoding='utf-8')
                    
                    # Check Python syntax
                    try:
                        ast.parse(content)
                    except SyntaxError as e:
                        self.issues.append(ValidationIssue(
                            severity=Severity.ERROR,
                            message=f"Python syntax error in {py_file.name}",
                            location=str(py_file),
                            line_number=e.lineno,
                            fix_suggestion=f"Fix syntax error: {str(e)}"
                        ))
                        continue
                    
                    # Check for module docstring
                    tree = ast.parse(content)
                    has_docstring = (
                        isinstance(tree.body[0], ast.Expr) and
                        isinstance(tree.body[0].value, (ast.Str, ast.Constant))
                    ) if tree.body else False
                    
                    if not has_docstring:
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Missing module docstring in {py_file.name}",
                            location=str(py_file),
                            fix_suggestion="Add a docstring at the top explaining what the script does"
                        ))
                    
                    # Check for error handling
                    has_try_except = any(
                        isinstance(node, ast.Try) or isinstance(node, ast.ExceptHandler)
                        for node in ast.walk(tree)
                    )
                    
                    if not has_try_except:
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"No error handling (try/except) found in {py_file.name}",
                            location=str(py_file),
                            fix_suggestion="Add try/except blocks for robust error handling"
                        ))
                    
                    # Check for __main__ guard
                    has_main_guard = '__name__' in content and '__main__' in content
                    
                    if not has_main_guard:
                        self.issues.append(ValidationIssue(
                            severity=Severity.INFO,
                            message=f"No __main__ guard in {py_file.name}",
                            location=str(py_file),
                            fix_suggestion="Add: if __name__ == '__main__': main()"
                        ))
                        
                except Exception as e:
                    self.issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        message=f"Error reading {py_file.name}: {str(e)}",
                        location=str(py_file),
                        fix_suggestion="Ensure file is readable and properly encoded"
                    ))
                    
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.ERROR,
                message=f"Error validating Python scripts: {str(e)}",
                fix_suggestion="Check scripts/ directory permissions"
            ))
    
    def _validate_content_quality(self):
        """Check content quality across all text files"""
        try:
            # Scan all .md, .txt, .py files (excluding TESTING_GUIDE)
            text_files = []
            for pattern in ['*.md', '*.txt', '*.py']:
                for f in self.skill_path.rglob(pattern):
                    # Skip TESTING_GUIDE directory
                    if 'TESTING_GUIDE' in f.parts:
                        continue
                    text_files.append(f)
            
            placeholder_pattern = r'\[(?:YOUR|FILL|INSERT|DESCRIBE|REPLACE|TODO|FIXME)[_\s][^\]]*\]'
            
            for text_file in text_files:
                try:
                    content = text_file.read_text(encoding='utf-8')
                    
                    # Check for placeholder text patterns
                    matches = re.finditer(placeholder_pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Get line number
                        line_num = content[:match.start()].count('\n') + 1
                        self.issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Placeholder text found: {match.group()[:50]}",
                            location=str(text_file.relative_to(self.skill_path)),
                            line_number=line_num,
                            fix_suggestion="Replace placeholder with actual content"
                        ))
                        
                except Exception:
                    # Skip files that can't be read as text
                    pass
                    
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Error checking content quality: {str(e)}",
                fix_suggestion="Manual review recommended"
            ))
    
    def _check_for_secrets(self):
        """Scan for hardcoded secrets or sensitive information"""
        try:
            # Scan all text files (exclude TESTING_GUIDE/)
            text_files = []
            for pattern in ['*.md', '*.txt', '*.py', '*.yaml', '*.yml', '*.json']:
                for f in self.skill_path.rglob(pattern):
                    # Skip TESTING_GUIDE directory
                    if 'TESTING_GUIDE' in f.parts:
                        continue
                    text_files.append(f)
            
            for text_file in text_files:
                try:
                    content = text_file.read_text(encoding='utf-8')
                    
                    # Check against SECRETS_PATTERNS
                    for pattern, description in self.SECRETS_PATTERNS:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            self.issues.append(ValidationIssue(
                                severity=Severity.ERROR,
                                message=f"{description} detected in {text_file.name}",
                                location=str(text_file.relative_to(self.skill_path)),
                                line_number=line_num,
                                fix_suggestion="Remove hardcoded secrets - use environment variables or configuration instead"
                            ))
                            
                except Exception:
                    # Skip binary files or files that can't be read
                    pass
                    
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity=Severity.WARNING,
                message=f"Error checking for secrets: {str(e)}",
                fix_suggestion="Manual security review recommended"
            ))
    
    def generate_report(self, verbose: bool = False) -> str:
        """Generate human-readable validation report"""
        if not self.issues:
            return f"""
{'='*70}
✓ VALIDATION PASSED
{'='*70}

Skill: {self.skill_path.name}
Path: {self.skill_path}

No issues found! This skill meets all validation requirements.
"""
        
        # Count errors, warnings, info
        errors = [i for i in self.issues if i.severity == Severity.ERROR]
        warnings = [i for i in self.issues if i.severity == Severity.WARNING]
        infos = [i for i in self.issues if i.severity == Severity.INFO]
        
        # Build report
        lines = []
        lines.append('='*70)
        
        if errors:
            lines.append('✗ VALIDATION FAILED')
        else:
            lines.append('⚠ VALIDATION PASSED WITH WARNINGS')
        
        lines.append('='*70)
        lines.append(f"\nSkill: {self.skill_path.name}")
        lines.append(f"Path: {self.skill_path}\n")
        
        # Status summary
        lines.append("Summary:")
        lines.append(f"  Errors:   {len(errors)}")
        lines.append(f"  Warnings: {len(warnings)}")
        lines.append(f"  Info:     {len(infos)}")
        lines.append("")
        
        # Errors section (always show)
        if errors:
            lines.append('-'*70)
            lines.append('ERRORS (must be fixed):')
            lines.append('-'*70)
            for i, issue in enumerate(errors, 1):
                lines.append(f"\n{i}. {issue}\n")
        
        # Warnings section (show if verbose or no errors)
        if warnings and (verbose or not errors):
            lines.append('-'*70)
            lines.append('WARNINGS (should be addressed):')
            lines.append('-'*70)
            for i, issue in enumerate(warnings, 1):
                lines.append(f"\n{i}. {issue}\n")
        
        # Info section (show if verbose)
        if infos and verbose:
            lines.append('-'*70)
            lines.append('INFORMATION:')
            lines.append('-'*70)
            for i, issue in enumerate(infos, 1):
                lines.append(f"\n{i}. {issue}\n")
        
        lines.append('='*70)
        
        if not verbose and (warnings or infos):
            lines.append("\nUse --verbose to see all issues")
        
        return '\n'.join(lines)


def validate_skill_cli():
    """Command-line interface for skill validation"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate Claude Skills against Anthropic standards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_skill.py ./my-skill
  python validate_skill.py ./my-skill --verbose
  python validate_skill.py ./my-skill --strict
  python validate_skill.py ./my-skill --json
        """
    )
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--strict', action='store_true',
                       help='Treat warnings as errors')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show all issues including info messages')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    try:
        # Create validator
        validator = SkillValidator(args.skill_path)
        
        # Run validation
        is_valid, issues = validator.validate()
        
        # Handle --strict mode
        if args.strict:
            warnings = [i for i in issues if i.severity == Severity.WARNING]
            if warnings:
                is_valid = False
        
        # Handle --json output
        if args.json:
            result = {
                "valid": is_valid,
                "skill_path": str(validator.skill_path),
                "skill_name": validator.skill_path.name,
                "issues": [
                    {
                        "severity": issue.severity.value,
                        "message": issue.message,
                        "location": issue.location,
                        "line_number": issue.line_number,
                        "fix_suggestion": issue.fix_suggestion
                    }
                    for issue in issues
                ]
            }
            print(json.dumps(result, indent=2))
        else:
            # Print report
            report = validator.generate_report(verbose=args.verbose)
            print(report)
        
        # Exit with appropriate code
        sys.exit(0 if is_valid else 1)
        
    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    validate_skill_cli()

