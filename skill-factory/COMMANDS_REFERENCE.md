# Quick Command Reference - Claude Skills Generator

## 🎯 Most Common Commands

```bash
# Generate skills prompt
python generate_skills.py

# Validate a skill
python validate_skill.py ./my-skill

# Package a skill
python package_skill.py ./my-skill

# Run all tests
python -m unittest discover
```

---

## 📋 Generate Skills

### Basic Usage
```bash
# Use default config (skills_config.yaml)
python generate_skills.py

# Use custom config
python generate_skills.py path/to/config.yaml

# Custom output location
python generate_skills.py config.yaml ./output/prompt.md
```

### Output
- Creates: `generated_skills/SKILLS_GENERATION_PROMPT.md`
- Creates: `generated_skills/generation_log.json`

---

## ✅ Validate Skills

### Basic Validation
```bash
# Validate a skill
python validate_skill.py ./my-skill

# See all issues (verbose)
python validate_skill.py ./my-skill --verbose
python validate_skill.py ./my-skill -v
```

### Advanced Validation
```bash
# Treat warnings as errors
python validate_skill.py ./my-skill --strict

# JSON output (for CI/CD)
python validate_skill.py ./my-skill --json

# JSON with verbose
python validate_skill.py ./my-skill --json --verbose
```

### Exit Codes
- `0` = Valid
- `1` = Invalid
- `130` = Cancelled by user

---

## 📦 Package Skills

### Single Skill
```bash
# Package with default settings
python package_skill.py ./my-skill

# Custom output path
python package_skill.py ./my-skill --output ~/Downloads/skill.zip
python package_skill.py ./my-skill -o ./dist/skill.zip
```

### Skip Validation
```bash
# Skip validation (not recommended)
python package_skill.py ./my-skill --no-validate

# Force package despite warnings
python package_skill.py ./my-skill --force
```

### Batch Packaging
```bash
# Package all skills in directory
python package_skill.py --batch ./generated_skills

# Package all skills matching pattern
python package_skill.py --batch ./generated_skills
```

### Output
- Creates: `./my-skill/my-skill.zip`
- Includes: manifest.json with checksums

---

## 🧪 Run Tests

### All Tests
```bash
# Run all test files
python -m unittest discover

# Run with verbose output
python -m unittest discover -v

# Run from specific directory
python -m unittest discover -s . -p "test_*.py"
```

### Specific Test Files
```bash
# Run validation tests only
python -m unittest test_validate_skill

# Run packaging tests only
python -m unittest test_package_skill

# Run generator tests only
python -m unittest test_generate_skills
```

### Specific Test Cases
```bash
# Run a specific test class
python -m unittest test_validate_skill.TestSkillValidator

# Run a specific test method
python -m unittest test_validate_skill.TestSkillValidator.test_valid_skill_passes
```

---

## 🔍 Debug and Inspect

### Check Configuration
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('skills_config.yaml'))"

# Pretty print config
python -c "import yaml, json; print(json.dumps(yaml.safe_load(open('skills_config.yaml')), indent=2))"
```

### View Generation History
```bash
# View log (Linux/Mac)
cat generated_skills/generation_log.json

# View log (Windows)
type generated_skills\generation_log.json

# Pretty print
python -m json.tool generated_skills/generation_log.json
```

### Inspect Package
```bash
# List files in package
unzip -l my-skill.zip

# Extract package
unzip my-skill.zip -d /tmp/inspect

# View manifest
unzip -p my-skill.zip manifest.json | python -m json.tool
```

### Test Imports
```bash
# Test validate_skill import
python -c "from validate_skill import SkillValidator; print('✓ OK')"

# Test package_skill import
python -c "from package_skill import SkillPackager; print('✓ OK')"

# Test generate_skills import
python -c "from generate_skills import SkillsGenerator; print('✓ OK')"
```

---

## 🔄 Complete Workflows

### First-Time Setup
```bash
# 1. Install dependencies
pip install pyyaml

# 2. Copy example config
cp skills_config.example.yaml skills_config.yaml

# 3. Edit config
vim skills_config.yaml  # or nano, code, etc.

# 4. Generate prompt
python generate_skills.py

# 5. Use prompt with Claude
# (Copy generated_skills/SKILLS_GENERATION_PROMPT.md)
```

### Validate → Package Workflow
```bash
# 1. Validate
python validate_skill.py ./my-skill

# 2. Fix issues
vim ./my-skill/SKILL.md

# 3. Re-validate
python validate_skill.py ./my-skill

# 4. Package
python package_skill.py ./my-skill

# 5. Import to Claude
# Settings → Features → Skills → Import
```

### Batch Processing
```bash
# Validate all skills
for skill in generated_skills/*/; do
    python validate_skill.py "$skill"
done

# Package all valid skills
python package_skill.py --batch ./generated_skills

# Count skills
ls -d generated_skills/*/ | wc -l
```

### CI/CD Pipeline
```bash
# Validate in strict mode with JSON output
python validate_skill.py ./my-skill --strict --json > validation_report.json

# Check exit code
if [ $? -eq 0 ]; then
    echo "✓ Validation passed"
    python package_skill.py ./my-skill --no-validate
else
    echo "✗ Validation failed"
    exit 1
fi
```

---

## 🛠️ Troubleshooting Commands

### Fix Common Issues
```bash
# Check Python version (need 3.7+)
python --version

# Install/upgrade PyYAML
pip install --upgrade pyyaml

# Check dependencies
pip list | grep -i yaml

# Verify files exist
ls -la *.py

# Check file permissions
ls -l validate_skill.py package_skill.py generate_skills.py
```

### Reset and Clean
```bash
# Remove generated files
rm -rf generated_skills/

# Remove test artifacts
rm -rf __pycache__/
rm -f *.pyc

# Remove backup files
rm -f *.backup *.bak

# Start fresh
git clean -fdx  # if using git
```

### Get Help
```bash
# Validation help
python validate_skill.py --help

# Packaging help
python package_skill.py --help

# Generator help
python generate_skills.py --help
```

---

## 📊 Monitoring and Logging

### View Logs
```bash
# Generation log
cat generated_skills/generation_log.json

# Last generation
tail -n 20 generated_skills/generation_log.json

# Count generations
python -c "import json; print(len(json.load(open('generated_skills/generation_log.json'))))"
```

### Check Status
```bash
# Count skills
ls -d generated_skills/*/ 2>/dev/null | grep -v 'SKILLS_GENERATION' | wc -l

# List all skills
ls -d generated_skills/*/ 2>/dev/null | grep -v 'SKILLS_GENERATION'

# Find packaged skills
find generated_skills -name "*.zip"

# Disk usage
du -sh generated_skills/
```

---

## 🚀 Advanced Usage

### Custom Validation
```bash
# Validate only Python syntax
python -c "
from validate_skill import SkillValidator
v = SkillValidator('./my-skill')
v._validate_python_scripts()
print(v.issues)
"
```

### Programmatic Usage
```python
# In Python script
from validate_skill import SkillValidator

validator = SkillValidator('./my-skill')
is_valid, issues = validator.validate()

if is_valid:
    print("✓ Skill is valid")
else:
    for issue in issues:
        print(issue)
```

### Batch Validation with Report
```bash
# Create validation report
echo "# Validation Report" > report.md
echo "" >> report.md

for skill in generated_skills/*/; do
    if [ -f "$skill/SKILL.md" ]; then
        echo "## $(basename $skill)" >> report.md
        python validate_skill.py "$skill" >> report.md 2>&1
        echo "" >> report.md
    fi
done
```

---

## 🔐 Security Checks

### Scan for Secrets
```bash
# Validate with focus on secrets
python validate_skill.py ./my-skill --verbose 2>&1 | grep -i "secret\|key\|password"

# Check specific file
python -c "
from validate_skill import SkillValidator
v = SkillValidator('./my-skill')
v._check_for_secrets()
for issue in v.issues:
    print(issue)
"
```

### Verify Package Contents
```bash
# List all files being packaged
python -c "
from package_skill import SkillPackager
p = SkillPackager('./my-skill', validate=False)
# Would need to modify to expose file list
"

# Check for excluded files manually
unzip -l my-skill.zip | grep -E "test_|__pycache__|\.pyc"
```

---

## 📖 Documentation Commands

### View Documentation
```bash
# View README in terminal
less README.md

# View troubleshooting guide
less TROUBLESHOOTING.md

# View quick start
less QUICKSTART.md

# View all markdown files
ls *.md
```

### Search Documentation
```bash
# Search for specific term
grep -r "validation" *.md

# Find all examples
grep -B2 -A2 "```bash" *.md

# List all sections
grep "^##" *.md
```

---

## 💡 Pro Tips

### Aliases (Add to .bashrc or .zshrc)
```bash
# Validation alias
alias vskill='python validate_skill.py'

# Package alias
alias pskill='python package_skill.py'

# Generate alias
alias gskill='python generate_skills.py'

# Test alias
alias tskill='python -m unittest discover'
```

### Quick Functions
```bash
# Function to validate and package
validate_and_package() {
    python validate_skill.py "$1" && python package_skill.py "$1"
}

# Usage
validate_and_package ./my-skill
```

### Watch for Changes
```bash
# Re-validate on file change (requires entr)
ls ./my-skill/SKILL.md | entr python validate_skill.py ./my-skill
```

---

## 🎯 Quick Reference Card

| Task | Command |
|------|---------|
| Generate | `python generate_skills.py` |
| Validate | `python validate_skill.py ./skill` |
| Validate (verbose) | `python validate_skill.py ./skill -v` |
| Validate (strict) | `python validate_skill.py ./skill --strict` |
| Package | `python package_skill.py ./skill` |
| Package (force) | `python package_skill.py ./skill --force` |
| Batch package | `python package_skill.py --batch ./dir` |
| Run tests | `python -m unittest discover` |
| Check config | `python -c "import yaml; yaml.safe_load(open('skills_config.yaml'))"` |
| View log | `cat generated_skills/generation_log.json` |

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-25  

For detailed explanations, see:
- README.md - Full documentation
- TROUBLESHOOTING.md - Problem solving
- QUICKSTART.md - Getting started guide

