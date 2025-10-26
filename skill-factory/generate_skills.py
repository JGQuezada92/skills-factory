#!/usr/bin/env python3
"""
Claude Skills Generator - Orchestrator Script

This script reads a configuration file and generates a complete, ready-to-use prompt
for creating Claude Skills based on your business requirements.

Usage:
    python generate_skills.py [config_file]
    
    If no config file is specified, defaults to 'skills_config.yaml'
"""

import yaml
import sys
import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime


# Custom Exception Classes
class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


class TemplateError(Exception):
    """Raised when template processing fails"""
    pass


class OutputError(Exception):
    """Raised when output operations fail"""
    pass


class ConfigValidator:
    """Validates skills_config.yaml comprehensively"""
    
    REQUIRED_SECTIONS = {
        'business': ['description', 'industry'],
        'skills': ['count', 'overlap_strategy', 'use_cases']
    }
    
    VALID_OVERLAP_STRATEGIES = ['overlapping', 'mutually_exclusive']
    VALID_SAMPLE_DATA_TYPES = ['csv', 'json', 'excel', 'pdf', 'image', 'text', 'api', 'none']
    
    PLACEHOLDER_PATTERNS = [
        r'\[YOUR[_\s].*?\]',
        r'\[FILL[_\s].*?\]',
        r'\[INSERT[_\s].*?\]',
        r'\[DESCRIBE[_\s].*?\]',
        r'\[e\.g\.,.*?\]',
        r'\[Example:.*?\]',
    ]
    
    def __init__(self, config: dict):
        self.config = config
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate configuration
        Returns: (is_valid, errors, warnings)
        """
        self._validate_structure()
        self._validate_types()
        self._validate_values()
        self._validate_content()
        self._check_placeholders()
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_structure(self):
        """Check all required sections and keys exist"""
        for section, keys in self.REQUIRED_SECTIONS.items():
            if section not in self.config:
                self.errors.append(
                    f"Missing required section: '{section}'\n"
                    f"  Fix: Add '{section}:' section to your config file\n"
                    f"  See skills_config.example.yaml for reference"
                )
                continue
            
            for key in keys:
                if key not in self.config[section]:
                    self.errors.append(
                        f"Missing required key: '{key}' in section '{section}'\n"
                        f"  Fix: Add '{key}: <value>' under '{section}:' section"
                    )
    
    def _validate_types(self):
        """Check all values have correct types"""
        # Check 'count' is integer
        if 'skills' in self.config:
            count = self.config['skills'].get('count')
            if count is not None and not isinstance(count, int):
                self.errors.append(
                    f"'skills.count' must be an integer, got {type(count).__name__}\n"
                    f"  Current value: {count}\n"
                    f"  Fix: Use 'count: 3' (no quotes)"
                )
            
            # Check 'use_cases' is list
            use_cases = self.config['skills'].get('use_cases')
            if use_cases is not None:
                if not isinstance(use_cases, list):
                    self.errors.append(
                        f"'skills.use_cases' must be a list\n"
                        f"  Fix: Format as:\n"
                        f"  use_cases:\n"
                        f"    - name: 'First Skill'\n"
                        f"      description: '...'"
                    )
                else:
                    # Check each use_case has required keys
                    for i, uc in enumerate(use_cases, 1):
                        if not isinstance(uc, dict):
                            self.errors.append(
                                f"Use case {i} must be a dictionary with keys: name, description"
                            )
                            continue
                        
                        if 'name' not in uc:
                            self.errors.append(
                                f"Use case {i} missing required 'name' field\n"
                                f"  Fix: Add 'name: Skill Name' to use case {i}"
                            )
                        
                        if 'description' not in uc:
                            self.errors.append(
                                f"Use case {i} missing required 'description' field\n"
                                f"  Fix: Add 'description: ...' to use case {i}"
                            )
    
    def _validate_values(self):
        """Check values are within acceptable ranges/enums"""
        if 'skills' in self.config:
            # Check count is 1-20
            count = self.config['skills'].get('count')
            if count is not None and isinstance(count, int):
                if count < 1 or count > 20:
                    self.errors.append(
                        f"'skills.count' must be between 1 and 20, got {count}\n"
                        f"  Fix: Set count to a reasonable number (3-5 recommended for first run)"
                    )
            
            # Check overlap_strategy is valid
            strategy = self.config['skills'].get('overlap_strategy')
            if strategy and strategy not in self.VALID_OVERLAP_STRATEGIES:
                self.errors.append(
                    f"Invalid 'overlap_strategy': '{strategy}'\n"
                    f"  Valid options: {', '.join(self.VALID_OVERLAP_STRATEGIES)}\n"
                    f"  Fix: Use 'overlapping' or 'mutually_exclusive'"
                )
            
            # Check sample_data_type values are valid
            use_cases = self.config['skills'].get('use_cases', [])
            if isinstance(use_cases, list):
                for i, uc in enumerate(use_cases, 1):
                    if isinstance(uc, dict):
                        data_type = uc.get('sample_data_type')
                        if data_type and data_type not in self.VALID_SAMPLE_DATA_TYPES:
                            self.errors.append(
                                f"Invalid 'sample_data_type' in use case {i}: '{data_type}'\n"
                                f"  Valid options: {', '.join(self.VALID_SAMPLE_DATA_TYPES)}\n"
                                f"  Fix: Use one of the valid data types"
                            )
    
    def _validate_content(self):
        """Check content quality"""
        if 'business' in self.config:
            # Check description length
            desc = self.config['business'].get('description', '')
            if isinstance(desc, str):
                word_count = len(desc.split())
                if word_count < 20:
                    self.warnings.append(
                        f"Business description is very short ({word_count} words)\n"
                        f"  Recommendation: Add more detail (50-200 words) for better skill generation"
                    )
        
        if 'skills' in self.config:
            use_cases = self.config['skills'].get('use_cases', [])
            if isinstance(use_cases, list):
                # Check for duplicate use case names
                names = [uc.get('name') for uc in use_cases if isinstance(uc, dict) and 'name' in uc]
                if len(names) != len(set(names)):
                    duplicates = [name for name in names if names.count(name) > 1]
                    self.errors.append(
                        f"Duplicate use case names found: {', '.join(set(duplicates))}\n"
                        f"  Fix: Each use case must have a unique name"
                    )
                
                # Check use case description quality
                for i, uc in enumerate(use_cases, 1):
                    if isinstance(uc, dict):
                        desc = uc.get('description', '')
                        if isinstance(desc, str):
                            word_count = len(desc.split())
                            if word_count < 10:
                                self.warnings.append(
                                    f"Use case {i} ('{uc.get('name', 'unnamed')}') has very short description ({word_count} words)\n"
                                    f"  Recommendation: Add more detail (30-100 words) about what this skill should do"
                                )
    
    def _check_placeholders(self):
        """Detect placeholder text that wasn't replaced"""
        config_str = json.dumps(self.config, indent=2)
        
        for pattern in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, config_str, re.IGNORECASE)
            if matches:
                self.warnings.append(
                    f"Placeholder text detected: {matches[0][:50]}...\n"
                    f"  Recommendation: Replace placeholder text with actual content\n"
                    f"  Found {len(matches)} placeholder(s) in total"
                )
                break  # Only warn once about placeholders


class SkillsGenerator:
    """Orchestrates the generation of Claude Skills prompt from configuration."""
    
    def __init__(self, config_path: str = "skills_config.yaml"):
        """Initialize the generator with a config file path."""
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.template_path = "skill_generation_prompt.md"
        
    def load_config(self) -> None:
        """Load and validate the configuration file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"✓ Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            print(f"✗ Error: Configuration file '{self.config_path}' not found.")
            print(f"  Please create a configuration file or specify a valid path.")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"✗ Error parsing YAML configuration: {e}")
            sys.exit(1)
    
    def validate_config(self) -> bool:
        """Validate configuration comprehensively"""
        validator = ConfigValidator(self.config)
        is_valid, errors, warnings = validator.validate()
        
        if errors:
            print(f"\n❌ Configuration Validation Failed\n")
            print(f"Found {len(errors)} error(s):\n")
            for i, error in enumerate(errors, 1):
                print(f"{i}. {error}")
            print(f"\nPlease fix these errors in {self.config_path} and try again.")
            print(f"For help, see README.md section 'Configuration Guide'\n")
            return False
        
        if warnings:
            print(f"\n⚠️  Configuration Warnings\n")
            print(f"Found {len(warnings)} warning(s):\n")
            for i, warning in enumerate(warnings, 1):
                print(f"{i}. {warning}")
            
            response = input("\nContinue with generation? (y/n): ")
            if response.lower() != 'y':
                print("Generation cancelled.")
                return False
        
        print("✓ Configuration validated successfully")
        return True
    
    def load_template(self) -> str:
        """Load the prompt template."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            print(f"✓ Template loaded from {self.template_path}")
            return template
        except FileNotFoundError:
            print(f"✗ Error: Template file '{self.template_path}' not found.")
            sys.exit(1)
    
    def format_list(self, items: List[str]) -> str:
        """Format a list of items as a bulleted markdown list."""
        if not items:
            return "- None specified"
        return '\n'.join(f"- {item}" for item in items)
    
    def generate_use_cases_section(self) -> str:
        """Generate the detailed use cases section."""
        use_cases = self.config['skills'].get('use_cases', [])
        
        if not use_cases:
            return "No specific use cases provided."
        
        sections = []
        for i, uc in enumerate(use_cases, 1):
            name = uc.get('name', f'Use Case {i}')
            desc = uc.get('description', 'No description provided')
            requires_python = uc.get('requires_python', False)
            sample_data_type = uc.get('sample_data_type', 'none')
            
            section = f"""### Use Case {i}: {name}

**Description:**
{desc}

**Requirements:**
- Python scripts needed: {'Yes' if requires_python else 'No'}
- Sample data type for testing: {sample_data_type}

**What to create:**
- Skill name: `{self._slugify(name)}`
- Include `scripts/` folder: {'Yes' if requires_python else 'Only if truly necessary'}
- Testing materials: Provide realistic {sample_data_type} sample data
"""
            sections.append(section)
        
        return '\n\n'.join(sections)
    
    def generate_overlap_guidance(self) -> str:
        """Generate guidance based on overlap strategy."""
        strategy = self.config['skills'].get('overlap_strategy', 'overlapping')
        
        if strategy == 'overlapping':
            return """
**Since you're creating overlapping skills:**
- Skills may share some functionality and complement each other
- Design skills to work together (e.g., one skill generates data, another visualizes it)
- It's okay for skills to reference or build upon each other
- Consider creating a skill ecosystem where skills can be composed
- Document in each SKILL.md how it works with other skills
"""
        else:
            return """
**Since you're creating mutually exclusive skills:**
- Each skill must have a distinct, non-overlapping purpose
- Clearly define boundaries between skills
- Avoid functionality duplication
- Each skill should be independently useful
- Ensure trigger conditions don't overlap
"""
    
    def generate_domain_knowledge_section(self) -> str:
        """Generate domain knowledge section if applicable."""
        domain_knowledge = self.config.get('advanced', {}).get('domain_knowledge', [])
        
        if not domain_knowledge or domain_knowledge == ['[e.g., Industry-specific terms, internal process names, compliance requirements]']:
            return ""
        
        return f"""
### Domain Knowledge to Incorporate

The following domain-specific terminology and knowledge should be incorporated into skills:

{self.format_list(domain_knowledge)}

Ensure these concepts are properly explained in SKILL.md or reference files.
"""
    
    def generate_integrations_section(self) -> str:
        """Generate integrations section if applicable."""
        integrations = self.config.get('advanced', {}).get('integrations', [])
        
        if not integrations or integrations == ['[e.g., Excel, PowerPoint, Salesforce, internal APIs, etc.]']:
            return ""
        
        return f"""
### Required Integrations

Skills should integrate with or support these tools/platforms:

{self.format_list(integrations)}

Include appropriate instructions for working with these tools in your skills.
"""
    
    def generate_constraints_section(self) -> str:
        """Generate constraints section if applicable."""
        constraints = self.config.get('advanced', {}).get('constraints', [])
        
        if not constraints or constraints == ['[e.g., Must comply with HIPAA, Must work offline, Must handle files >100MB, etc.]']:
            return ""
        
        return f"""
### Constraints and Requirements

All skills must adhere to these constraints:

{self.format_list(constraints)}

Consider these constraints when designing workflows and selecting approaches.
"""
    
    def populate_template(self, template: str) -> str:
        """Replace all template variables with actual values from config."""
        business = self.config['business']
        skills = self.config['skills']
        
        # Basic replacements
        replacements = {
            '{{SKILL_COUNT}}': str(skills.get('count', 3)),
            '{{BUSINESS_DESCRIPTION}}': business.get('description', 'Not provided').strip(),
            '{{INDUSTRY}}': business.get('industry', 'Not specified'),
            '{{TEAM_SIZE}}': business.get('team_size', 'Not specified'),
            '{{PRIMARY_WORKFLOWS}}': self.format_list(business.get('primary_workflows', [])),
            '{{OVERLAP_STRATEGY}}': skills.get('overlap_strategy', 'overlapping'),
            '{{USE_CASES_SECTION}}': self.generate_use_cases_section(),
            '{{OVERLAP_GUIDANCE}}': self.generate_overlap_guidance(),
            '{{DOMAIN_KNOWLEDGE_SECTION}}': self.generate_domain_knowledge_section(),
            '{{INTEGRATIONS_SECTION}}': self.generate_integrations_section(),
            '{{CONSTRAINTS_SECTION}}': self.generate_constraints_section(),
        }
        
        populated = template
        for key, value in replacements.items():
            populated = populated.replace(key, value)
        
        print("✓ Template populated with configuration values")
        return populated
    
    def save_output(self, content: str, output_path: str = None) -> None:
        """Save the generated prompt to a file with comprehensive error handling"""
        try:
            if output_path is None:
                output_path = self.config.get('output', {}).get('output_directory', './generated_skills')
                output_path = os.path.join(output_path, 'SKILLS_GENERATION_PROMPT.md')
            
            output_path = Path(output_path).resolve()
            
            # Validate output path is within current directory (security)
            try:
                output_path.relative_to(Path.cwd().resolve())
            except ValueError:
                raise OutputError(
                    f"Output path must be within current directory\n"
                    f"  Attempted: {output_path}\n"
                    f"  Current directory: {Path.cwd()}"
                )
            
            # Check if file exists
            if output_path.exists():
                print(f"\n⚠️  File already exists: {output_path}")
                response = input("Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print("Generation cancelled.")
                    return
                
                # Backup existing file
                backup_path = output_path.with_suffix('.md.backup')
                shutil.copy2(output_path, backup_path)
                print(f"  Created backup: {backup_path}")
            
            # Create output directory
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Generated prompt saved to: {output_path}")
            self._print_success_message(output_path)
            
        except PermissionError:
            raise OutputError(
                f"Permission denied writing to: {output_path}\n"
                f"  Ensure you have write permissions to this directory"
            )
        except OSError as e:
            raise OutputError(
                f"Failed to write output file: {e}\n"
                f"  Check disk space and file path validity"
            )
    
    def _print_success_message(self, output_path: Path):
        """Print formatted success message with next steps"""
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS! Your skills generation prompt is ready.")
        print(f"{'='*70}")
        print(f"\nNext steps:")
        print(f"1. Review: {output_path}")
        print(f"2. Copy the entire file content")
        print(f"3. Open Claude (claude.ai or Claude Code)")
        print(f"4. Paste the prompt into a new conversation")
        print(f"5. Claude will generate {self.config['skills']['count']} custom skills")
        print(f"6. Validate: python validate_skill.py <skill_folder>")
        print(f"7. Package: python package_skill.py <skill_folder>")
        print(f"\n{'='*70}\n")
    
    def generate(self, output_path: str = None) -> None:
        """Main generation workflow (legacy method for compatibility)."""
        self.load_config()
        
        if not self.validate_config():
            sys.exit(1)
        
        template = self.load_template()
        populated_prompt = self.populate_template(template)
        
        # Add metadata injection
        populated_prompt = self.inject_metadata(populated_prompt)
        
        self.save_output(populated_prompt, output_path)
        
        # Create generation log
        if output_path:
            log_path = output_path
        else:
            log_path = self.config.get('output', {}).get('output_directory', './generated_skills')
            log_path = os.path.join(log_path, 'SKILLS_GENERATION_PROMPT.md')
        
        self.create_generation_log(log_path)
    
    def inject_metadata(self, prompt_content: str) -> str:
        """Inject metadata into generated prompt as HTML comments"""
        metadata_block = f"""<!-- GENERATION METADATA
Config Version: {self.config.get('metadata', {}).get('config_version', 'unknown')}
Generated: {datetime.utcnow().isoformat()}Z
Claude Model: {self.config.get('generation_settings', {}).get('claude_model', 'claude-sonnet-4-20250514')}
Template Version: {self.config.get('generation_settings', {}).get('prompt_template_version', '1.0')}
Skill Count: {self.config.get('skills', {}).get('count', 0)}
Overlap Strategy: {self.config.get('skills', {}).get('overlap_strategy', 'unknown')}
-->

"""
        return metadata_block + prompt_content
    
    def create_generation_log(self, output_path: str):
        """Create or update generation_log.json"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "config_version": self.config.get('metadata', {}).get('config_version'),
            "skills_requested": self.config.get('skills', {}).get('count'),
            "use_cases": [uc.get('name', 'unnamed') for uc in self.config.get('skills', {}).get('use_cases', [])],
            "output_path": str(output_path),
            "status": "generated",
            "business_industry": self.config.get('business', {}).get('industry'),
            "overlap_strategy": self.config.get('skills', {}).get('overlap_strategy')
        }
        
        log_file = Path("generated_skills/generation_log.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing or create new
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, IOError):
                logs = []
        else:
            logs = []
        
        logs.append(log_entry)
        
        # Write updated log
        try:
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            print(f"✓ Generation logged to: {log_file}")
        except Exception as e:
            print(f"⚠ Warning: Could not write generation log: {e}")
    
    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to a slug format (lowercase, hyphens)."""
        return text.lower().replace(' ', '-').replace('_', '-')


def main():
    """Main entry point with comprehensive error handling"""
    config_file = sys.argv[1] if len(sys.argv) > 1 else "skills_config.yaml"
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"\n{'='*70}")
    print(f"Claude Skills Generator")
    print(f"{'='*70}\n")
    
    try:
        generator = SkillsGenerator(config_file)
        generator.load_config()
        
        if not generator.validate_config():
            sys.exit(1)
        
        template = generator.load_template()
        populated_prompt = generator.populate_template(template)
        generator.save_output(populated_prompt, output_file)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user.")
        sys.exit(130)
        
    except FileNotFoundError as e:
        print(f"\n❌ File Not Found Error")
        print(f"\n{e}")
        print(f"\nTroubleshooting:")
        print(f"  • Ensure configuration file exists: {config_file}")
        print(f"  • Check file path is correct")
        print(f"  • Try running from project root directory")
        sys.exit(1)
        
    except yaml.YAMLError as e:
        print(f"\n❌ YAML Syntax Error")
        print(f"\n{e}")
        print(f"\nTroubleshooting:")
        print(f"  • Check {config_file} for syntax errors")
        print(f"  • Ensure proper indentation (use spaces, not tabs)")
        print(f"  • Validate YAML at: https://www.yamllint.com/")
        sys.exit(1)
        
    except ConfigValidationError as e:
        print(f"\n❌ Configuration Validation Error")
        print(f"\n{e}")
        sys.exit(1)
        
    except TemplateError as e:
        print(f"\n❌ Template Error")
        print(f"\n{e}")
        print(f"\nEnsure skill_generation_prompt.md exists and is valid")
        sys.exit(1)
        
    except OutputError as e:
        print(f"\n❌ Output Error")
        print(f"\n{e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error")
        print(f"\n{e}")
        print(f"\nPlease report this error with:")
        print(f"  • The command you ran")
        print(f"  • Your configuration file")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

