#!/usr/bin/env python3
"""
Unit tests for validate_skill.py
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from validate_skill import SkillValidator, Severity, ValidationIssue


class TestSkillValidator(unittest.TestCase):
    
    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.skill_path = Path(self.test_dir) / "test-skill"
        self.skill_path.mkdir()
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def create_skill_md(self, content: str):
        """Helper to create SKILL.md with content"""
        (self.skill_path / "SKILL.md").write_text(content, encoding='utf-8')
    
    def test_valid_skill_passes(self):
        """A properly formatted skill should pass validation"""
        valid_skill_md = """---
name: test-skill
description: This skill should be used when testing the validation system to ensure all components work correctly.
license: Complete terms in LICENSE.txt
---

# Test Skill

## Overview

Load the configuration file and process the data accordingly.

## When to Use This Skill

Use this skill when validation is needed.

## How to Use This Skill

### Step 1: Initialize

Initialize the system by loading required files.

### Step 2: Process

Process the data using the provided methods.

## Keywords

testing, validation, quality assurance
"""
        self.create_skill_md(valid_skill_md)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should be valid
        self.assertTrue(is_valid)
        
        # Should have no errors
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertEqual(len(errors), 0)
    
    def test_missing_skill_md_fails(self):
        """Skill without SKILL.md should fail"""
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        self.assertFalse(is_valid)
        
        # Should have error about missing SKILL.md
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertGreater(len(errors), 0)
        self.assertIn("SKILL.md", errors[0].message)
    
    def test_invalid_frontmatter_fails(self):
        """Skill with malformed YAML frontmatter should fail"""
        invalid_skill_md = """---
name: test-skill
description: incomplete yaml
---

# Skill
"""
        self.create_skill_md(invalid_skill_md)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warnings about missing sections
        warnings = [i for i in issues if i.severity == Severity.WARNING]
        self.assertGreater(len(warnings), 0)
    
    def test_missing_frontmatter_fails(self):
        """Skill without frontmatter should fail"""
        no_frontmatter = """# My Skill

This is content without frontmatter.
"""
        self.create_skill_md(no_frontmatter)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        self.assertFalse(is_valid)
        
        errors = [i for i in issues if i.severity == Severity.ERROR]
        self.assertGreater(len(errors), 0)
        self.assertIn("frontmatter", errors[0].message.lower())
    
    def test_missing_required_sections_fails(self):
        """Skill missing required sections should fail"""
        minimal_skill_md = """---
name: test-skill
description: Test skill
license: MIT
---

# Test Skill

Just some content.
"""
        self.create_skill_md(minimal_skill_md)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warnings about missing sections
        warnings = [i for i in issues if i.severity == Severity.WARNING]
        self.assertGreater(len(warnings), 0)
    
    def test_second_person_pronoun_detected(self):
        """Should detect 'you' and 'your' in content"""
        skill_with_you = """---
name: test-skill
description: Test skill for validation
license: MIT
---

# Test Skill

## Overview

You should use this skill when you need testing.

## How to Use

Your first step is to load your file.
"""
        self.create_skill_md(skill_with_you)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should fail due to second-person pronouns
        self.assertFalse(is_valid)
        
        errors = [i for i in issues if i.severity == Severity.ERROR and 'you' in i.message.lower()]
        self.assertGreater(len(errors), 0)
    
    def test_placeholder_text_detected(self):
        """Should detect [PLACEHOLDER] text"""
        skill_with_placeholder = """---
name: test-skill
description: Test skill
license: MIT
---

# Test Skill

## Overview

[TODO: Add description here]

## How to Use

Load the [YOUR_FILE_NAME] file.
"""
        self.create_skill_md(skill_with_placeholder)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warnings about placeholders
        warnings_errors = [i for i in issues if 'placeholder' in i.message.lower() or 'TODO' in i.message]
        self.assertGreater(len(warnings_errors), 0)
    
    def test_secrets_detected(self):
        """Should detect hardcoded API keys"""
        skill_with_secret = """---
name: test-skill
description: Test skill
license: MIT
---

# Test Skill

## Overview

Load files and process.

## Configuration

api_key = "sk_live_1234567890abcdefghijklmnopqrstuvwxyz"
"""
        self.create_skill_md(skill_with_secret)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should fail due to API key
        self.assertFalse(is_valid)
        
        errors = [i for i in issues if i.severity == Severity.ERROR and 'key' in i.message.lower()]
        self.assertGreater(len(errors), 0)
    
    def test_python_syntax_error_detected(self):
        """Should detect syntax errors in Python scripts"""
        # Create valid SKILL.md
        valid_skill_md = """---
name: test-skill
description: Test skill with scripts
license: MIT
---

# Test Skill

Process data.
"""
        self.create_skill_md(valid_skill_md)
        
        # Create scripts folder with syntax error
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        
        invalid_script = """#!/usr/bin/env python3
def broken_function(
    # Missing closing parenthesis
    print("This won't work")
"""
        (scripts_dir / "broken.py").write_text(invalid_script)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should fail due to syntax error
        self.assertFalse(is_valid)
        
        errors = [i for i in issues if i.severity == Severity.ERROR and 'syntax' in i.message.lower()]
        self.assertGreater(len(errors), 0)
    
    def test_valid_python_script_passes(self):
        """Valid Python scripts should pass"""
        # Create valid SKILL.md
        valid_skill_md = """---
name: test-skill
description: Test skill with scripts
license: MIT
---

# Test Skill

Process data.
"""
        self.create_skill_md(valid_skill_md)
        
        # Create scripts folder with valid script
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        
        valid_script = """#!/usr/bin/env python3
\"\"\"This is a valid script\"\"\"

def hello():
    try:
        print("Hello, world!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hello()
"""
        (scripts_dir / "valid.py").write_text(valid_script)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Might have warnings but no errors from scripts
        errors = [i for i in issues if i.severity == Severity.ERROR]
        syntax_errors = [e for e in errors if 'syntax' in e.message.lower()]
        self.assertEqual(len(syntax_errors), 0)
    
    def test_folder_naming_validation(self):
        """Should warn about invalid folder naming"""
        # Create skill with uppercase name
        bad_skill_path = Path(self.test_dir) / "BadSkillName"
        bad_skill_path.mkdir()
        
        valid_skill_md = """---
name: badskillname
description: Test skill
license: MIT
---

# Test Skill

Content here.
"""
        (bad_skill_path / "SKILL.md").write_text(valid_skill_md)
        
        validator = SkillValidator(str(bad_skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warning about folder name
        warnings = [i for i in issues if i.severity == Severity.WARNING and 'folder' in i.message.lower()]
        self.assertGreater(len(warnings), 0)
    
    def test_empty_scripts_folder_warning(self):
        """Should warn if scripts/ folder is empty"""
        valid_skill_md = """---
name: test-skill
description: Test skill
license: MIT
---

# Test Skill

Content.
"""
        self.create_skill_md(valid_skill_md)
        
        # Create empty scripts folder
        scripts_dir = self.skill_path / "scripts"
        scripts_dir.mkdir()
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warning about empty scripts folder
        warnings = [i for i in issues if i.severity == Severity.WARNING and 'scripts' in i.message.lower()]
        self.assertGreater(len(warnings), 0)
    
    def test_description_in_frontmatter_validation(self):
        """Should validate description quality"""
        # Very short description
        short_desc_skill = """---
name: test-skill
description: Short.
license: MIT
---

# Test Skill

Content.
"""
        self.create_skill_md(short_desc_skill)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        # Should have warning about short description
        warnings = [i for i in issues if i.severity == Severity.WARNING and 'short' in i.message.lower()]
        self.assertGreater(len(warnings), 0)
    
    def test_generate_report_format(self):
        """Test report generation"""
        valid_skill_md = """---
name: test-skill
description: This is a test skill for validation purposes to ensure the system works correctly.
license: MIT
---

# Test Skill

## Overview

Process data efficiently.

## When to Use

Use for testing.

## How to Use

Load and process.
"""
        self.create_skill_md(valid_skill_md)
        
        validator = SkillValidator(str(self.skill_path))
        is_valid, issues = validator.validate()
        
        report = validator.generate_report(verbose=True)
        
        # Report should be a string
        self.assertIsInstance(report, str)
        
        # Should contain skill name
        self.assertIn("test-skill", report)
        
        # Should have some structure
        self.assertIn("=", report)


class TestValidationIssue(unittest.TestCase):
    """Test ValidationIssue dataclass"""
    
    def test_issue_creation(self):
        """Test creating a ValidationIssue"""
        issue = ValidationIssue(
            severity=Severity.ERROR,
            message="Test error",
            location="test.md",
            line_number=10,
            fix_suggestion="Fix it"
        )
        
        self.assertEqual(issue.severity, Severity.ERROR)
        self.assertEqual(issue.message, "Test error")
        self.assertEqual(issue.location, "test.md")
        self.assertEqual(issue.line_number, 10)
        self.assertEqual(issue.fix_suggestion, "Fix it")
    
    def test_issue_string_representation(self):
        """Test string representation of issue"""
        issue = ValidationIssue(
            severity=Severity.WARNING,
            message="Test warning"
        )
        
        issue_str = str(issue)
        self.assertIn("WARNING", issue_str)
        self.assertIn("Test warning", issue_str)


if __name__ == '__main__':
    unittest.main()

