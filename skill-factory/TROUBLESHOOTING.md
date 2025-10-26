# Troubleshooting Guide - Claude Skills Generator

This guide helps you resolve common issues when working with the Claude Skills Generator system.

## Table of Contents

- [Validation Errors](#validation-errors)
- [Packaging Errors](#packaging-errors)
- [Configuration Errors](#configuration-errors)
- [Generation Errors](#generation-errors)
- [Runtime Errors](#runtime-errors)
- [Getting Help](#getting-help)

---

## Validation Errors

### "SKILL.md must start with YAML frontmatter"

**Cause:** SKILL.md doesn't begin with `---`

**Fix:**
```markdown
---
name: skill-name
description: Your description
license: Complete terms in LICENSE.txt
---

# Your Skill Title
...
```

### "Missing required frontmatter key: 'description'"

**Cause:** YAML frontmatter is incomplete

**Fix:**
Ensure all three required keys are present:
```yaml
---
name: my-skill-name
description: This skill should be used when... (detailed description)
license: Complete terms in LICENSE.txt
---
```

### "Python syntax error in scripts/file.py"

**Cause:** Python script has syntax errors

**Fix:**
1. Open the .py file mentioned in the error
2. Check the line number in the error message
3. Fix the syntax error (missing parenthesis, colon, indentation, etc.)
4. Re-run validation: `python validate_skill.py <skill_folder>`

**Example:**
```python
# ❌ Wrong - missing colon
def my_function()
    print("Hello")

# ✅ Correct
def my_function():
    print("Hello")
```

### "Second-person pronoun 'you' found"

**Cause:** SKILL.md uses "you" or "your" instead of imperative form

**Fix:**
Convert to imperative/infinitive form:

```markdown
❌ Wrong:
"You should load the file and process your data."

✅ Correct:
"Load the file and process the data."
```

### "Placeholder text found: [YOUR_TEXT]"

**Cause:** Template placeholder text wasn't replaced

**Fix:**
Search for text in square brackets and replace with actual content:
- `[YOUR_DESCRIPTION]` → actual description
- `[TODO: ...]` → completed content
- `[FIXME: ...]` → fixed content

### "Possible API key detected"

**Cause:** Hardcoded secret or API key found in skill files

**Fix:**
1. Remove the hardcoded secret
2. Use environment variables instead:
   ```python
   # ❌ Wrong
   API_KEY = "sk_live_1234567890abcdefg..."
   
   # ✅ Correct
   import os
   API_KEY = os.getenv('API_KEY')
   ```
3. Document in SKILL.md that users need to set environment variables

### "Missing required section: Overview"

**Cause:** SKILL.md is missing recommended markdown sections

**Fix:**
Add the missing section to SKILL.md:
```markdown
## Overview

[Explanation of what this skill provides]

## When to Use This Skill

[Specific trigger conditions and use cases]

## How to Use This Skill

[Step-by-step instructions]
```

---

## Packaging Errors

### "Cannot package skill with validation errors"

**Cause:** Skill has validation errors that must be fixed first

**Fix:**
1. Run: `python validate_skill.py <skill_folder>`
2. Fix all ERROR items listed
3. Try packaging again: `python package_skill.py <skill_folder>`

**Quick bypass (not recommended):**
```bash
python package_skill.py <skill_folder> --force
```

### "Permission denied writing to..."

**Cause:** No write permissions to output directory

**Fix:**
1. Check directory permissions
2. Try different output location:
   ```bash
   python package_skill.py <skill_folder> --output ~/Downloads/skill.zip
   ```
3. On Windows, try running PowerShell as Administrator
4. On Linux/Mac, check with: `ls -la`

### "SKILL.md not found in skill folder"

**Cause:** The skill folder doesn't contain SKILL.md

**Fix:**
1. Verify you're pointing to the correct folder
2. Check folder structure:
   ```
   my-skill/
   ├── SKILL.md  ← Must exist in root
   ├── scripts/
   └── ...
   ```
3. Ensure the file is named exactly `SKILL.md` (case-sensitive)

---

## Configuration Errors

### "Missing required section: 'business'"

**Cause:** Configuration file is missing required sections

**Fix:**
Add the missing section to `skills_config.yaml`:
```yaml
business:
  description: "Your business description"
  industry: "Your industry"
  team_size: "10-50"
  primary_workflows:
    - "Workflow 1"
```

### "Invalid overlap_strategy: 'invalid_value'"

**Cause:** `overlap_strategy` has invalid value

**Fix:**
Must be one of two valid options:
```yaml
skills:
  overlap_strategy: "overlapping"  # Skills can work together
  # OR
  overlap_strategy: "mutually_exclusive"  # Distinct skills
```

### "'skills.count' must be an integer"

**Cause:** Count value is not a number or is in quotes

**Fix:**
```yaml
❌ Wrong:
skills:
  count: "3"  # String

✅ Correct:
skills:
  count: 3  # Integer (no quotes)
```

### "'skills.count' must be between 1 and 20"

**Cause:** Count is outside valid range

**Fix:**
```yaml
skills:
  count: 5  # Must be 1-20
```

**Recommendation:** Start with 2-3 skills for first run.

### "Duplicate use case names found"

**Cause:** Multiple use cases have the same name

**Fix:**
Ensure each use case has a unique name:
```yaml
use_cases:
  - name: "Financial Analysis"  # Unique
    description: "..."
  - name: "Portfolio Reporting"  # Different
    description: "..."
```

### "Configuration file not found"

**Cause:** `skills_config.yaml` doesn't exist in current directory

**Fix:**
1. Create config from example:
   ```bash
   cp skills_config.example.yaml skills_config.yaml
   ```
2. Or specify custom path:
   ```bash
   python generate_skills.py path/to/my_config.yaml
   ```

### "YAML Syntax Error"

**Cause:** Invalid YAML syntax (indentation, special characters, etc.)

**Fix:**
1. Check indentation (use spaces, not tabs)
2. Validate YAML online: https://www.yamllint.com/
3. Common issues:
   ```yaml
   ❌ Wrong:
   description: This has a: colon problem
   
   ✅ Correct:
   description: "This has a: colon but is quoted"
   # OR
   description: |
     This is multi-line text
     that handles special characters fine
   ```

---

## Generation Errors

### "Template file not found"

**Cause:** `skill_generation_prompt.md` is missing

**Fix:**
1. Ensure you're running from the correct directory
2. Check file exists: `ls skill_generation_prompt.md`
3. Re-download if missing from repository

### "Output path must be within current directory"

**Cause:** Security check preventing writing outside project directory

**Fix:**
Use relative paths within project:
```yaml
output:
  output_directory: "./generated_skills"  # ✅ Within project
  # Not: "/tmp/skills"  # ❌ Outside project
```

### "File already exists: SKILLS_GENERATION_PROMPT.md"

**Cause:** Output file already exists

**Options:**
1. Type `y` to overwrite (creates backup automatically)
2. Type `n` to cancel
3. Or specify different output path:
   ```bash
   python generate_skills.py config.yaml ./output/prompt_v2.md
   ```

---

## Runtime Errors

### "ModuleNotFoundError: No module named 'yaml'"

**Cause:** Required Python package not installed

**Fix:**
```bash
pip install pyyaml
```

**For all dependencies:**
```bash
pip install pyyaml
```

### "ImportError: cannot import name 'SkillValidator'"

**Cause:** Module import path issue

**Fix:**
1. Ensure all .py files are in the same directory
2. Run from the project root directory:
   ```bash
   cd /path/to/project
   python validate_skill.py ./my-skill
   ```

### Tests fail with "No module named 'validate_skill'"

**Cause:** Tests can't find project modules

**Fix:**
Run tests from project root:
```bash
cd /path/to/project
python -m unittest test_validate_skill.py
```

Or run all tests:
```bash
python -m unittest discover -s . -p "test_*.py"
```

---

## Common Workflow Issues

### Skill doesn't trigger in Claude

**Problem:** Claude doesn't invoke the skill when expected

**Solutions:**
1. **Check skill description** - Make it more specific about trigger conditions
2. **Add relevant keywords** - Include them at the end of SKILL.md
3. **Explicit invocation** - Mention the skill by name:
   ```
   Hey Claude—I just added the "financial-analysis" skill. 
   Can you analyze this data?
   ```
4. **Review validation** - Ensure skill passed validation without errors

### Skills conflict with each other

**Problem:** Multiple skills trigger for the same task

**Solutions:**
1. **Review overlap_strategy** - Consider using `mutually_exclusive`
2. **Refine descriptions** - Make trigger conditions more distinct
3. **Test individually** - Verify each skill works alone first

### Generated prompt is too long

**Problem:** Prompt exceeds Claude's context limits

**Solutions:**
1. **Reduce skill count** - Generate 2-3 skills at a time
2. **Simplify use cases** - Make descriptions more concise
3. **Remove optional sections** - Remove advanced/ section if not needed
4. **Batch generation** - Generate skills in separate runs

---

## Performance Issues

### Validation is slow

**Cause:** Large skills with many files

**Solutions:**
1. Normal for skills with 50+ files
2. Skip validation during development:
   ```bash
   python package_skill.py <skill> --no-validate
   ```
3. Use `--json` for faster output:
   ```bash
   python validate_skill.py <skill> --json
   ```

### Packaging takes long time

**Cause:** Large asset files being checksummed

**Normal Behavior:** Files >10MB skip checksum (by design)

---

## Debugging Tips

### Enable Verbose Output

```bash
# Validation
python validate_skill.py <skill> --verbose

# See all issues including INFO level
python validate_skill.py <skill> -v
```

### Check Generation Log

```bash
# View generation history
cat generated_skills/generation_log.json

# Pretty print
python -m json.tool generated_skills/generation_log.json
```

### Inspect Package Contents

```bash
# List files in packaged skill
unzip -l my-skill.zip

# Extract and inspect
unzip my-skill.zip -d /tmp/inspect
```

### Validate YAML

```bash
# Python one-liner to check YAML
python -c "import yaml; yaml.safe_load(open('skills_config.yaml'))"
```

---

## Getting Help

If you encounter an issue not listed here:

### 1. Check Documentation
- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide
- **SYSTEM_OVERVIEW.md** - Architecture details

### 2. Review Error Messages
- Error messages include fix suggestions
- Read the full message, not just the first line
- Check line numbers mentioned in errors

### 3. Verify Your Setup
```bash
# Check Python version (need 3.7+)
python --version

# Check dependencies
pip list | grep -i yaml

# Verify file structure
ls -la
```

### 4. Enable Debug Mode
```python
# Add to scripts for debugging
import traceback
try:
    # your code
except Exception as e:
    traceback.print_exc()
```

### 5. Common Debug Commands
```bash
# Validate configuration
python -c "import yaml; print(yaml.safe_load(open('skills_config.yaml')))"

# Test imports
python -c "from validate_skill import SkillValidator; print('OK')"

# Run specific test
python -m unittest test_validate_skill.TestSkillValidator.test_valid_skill_passes
```

---

## Error Message Reference

### Exit Codes

- `0` - Success
- `1` - General error
- `130` - Interrupted by user (Ctrl+C)

### Common Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `✗` | Error | Must be fixed |
| `⚠` | Warning | Should be addressed |
| `✓` | Success | All good |
| `❌` | Critical failure | Blocks progress |

---

## Prevention Best Practices

### Before Validation
1. Use a text editor with YAML support
2. Run a YAML linter first
3. Check for TODO/FIXME comments
4. Review for hardcoded secrets

### Before Packaging
1. Always validate first
2. Test Python scripts independently
3. Remove test files from skill folder
4. Check file sizes (large assets?)

### Before Generation
1. Fill out all required config fields
2. Replace all placeholder text
3. Test with 1-2 skills first
4. Review example config for reference

---

## Quick Reference Card

```bash
# Validate a skill
python validate_skill.py ./my-skill

# Package a skill
python package_skill.py ./my-skill

# Generate prompt
python generate_skills.py

# Run all tests
python -m unittest discover

# Check validation in JSON
python validate_skill.py ./my-skill --json

# Force package (skip warnings)
python package_skill.py ./my-skill --force

# Package all skills in directory
python package_skill.py --batch ./generated_skills
```

---

**Last Updated:** 2025-10-25
**Version:** 1.0

For additional support, review the generated_skills/generation_log.json for your specific generation details.

