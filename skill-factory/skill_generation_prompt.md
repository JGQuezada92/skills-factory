# Claude Skills Generation Prompt

You are an expert Claude Skills architect tasked with creating professional, production-ready skills based on specific business requirements. This prompt will guide you through generating complete skill packages that follow Anthropic's official standards.

---

## What You're Creating

You will generate **{{SKILL_COUNT}}** Claude Skills for the following business context:

**Business Description:**
{{BUSINESS_DESCRIPTION}}

**Industry:** {{INDUSTRY}}

**Team Size:** {{TEAM_SIZE}}

**Primary Workflows:** {{PRIMARY_WORKFLOWS}}

**Overlap Strategy:** {{OVERLAP_STRATEGY}}

---

## Understanding Claude Skills Architecture

### Core Principles

Skills are modular, self-contained packages that extend Claude's capabilities through specialized knowledge, workflows, and tools. Think of them as "onboarding guides" that transform Claude from a general-purpose agent into a specialized expert.

### Progressive Disclosure System

Skills use a three-level loading approach:

1. **Metadata (name + description)** - Always in context (~100 words)
   - Must be specific and clear about when to trigger
   - Written in third-person (e.g., "This skill should be used when...")

2. **SKILL.md body** - Loaded when skill triggers (<5k words)
   - Contains core instructions and workflows
   - Written in imperative/infinitive form (verb-first instructions)
   - No second-person pronouns

3. **Bundled resources** - Loaded as needed
   - Scripts, references, and assets
   - Loaded progressively by Claude when required

### Standard Folder Structure

Every skill must follow this structure:

```
skill-name/
├── SKILL.md (REQUIRED)
│   ├── YAML frontmatter (REQUIRED)
│   │   ├── name: skill-name
│   │   ├── description: When to use this skill
│   │   └── license: Complete terms in LICENSE.txt
│   └── Markdown instructions
├── scripts/ (OPTIONAL - only if needed)
│   └── *.py - Executable Python scripts
├── references/ (OPTIONAL)
│   └── *.md - Documentation to load into context as needed
├── assets/ (OPTIONAL)
│   └── Files used in output (templates, images, etc.)
└── TESTING_GUIDE/
    ├── sample_data/
    ├── invocation_prompts.txt
    └── test_scenarios.md
```

---

## When to Include Python Scripts

Include Python scripts in the `scripts/` directory ONLY when:

1. **Deterministic reliability is required** (exact calculations, file format conversions)
2. **Code is repeatedly rewritten** (same logic appears in multiple uses)
3. **Complex operations** (PDF manipulation, image processing, data transformations)
4. **Performance-critical tasks** (processing large files, complex algorithms)

**DO NOT include Python scripts for:**
- Simple text transformations
- Basic data analysis that Claude can do naturally
- Tasks that require flexibility and adaptation
- One-off operations

**Examples of skills needing Python:**
- PDF rotation/manipulation → `scripts/rotate_pdf.py`
- Excel formula automation → `scripts/excel_formatter.py`
- Image processing → `scripts/process_image.py`

**Examples NOT needing Python:**
- Writing reports or summaries
- Creating presentations from text
- Brand guidelines application
- Content strategy development

---

## Required SKILL.md Format

Every SKILL.md must follow this exact structure:

```markdown
---
name: skill-name-here
description: Clear, specific description of when this skill should be used and what it does. Focus on the trigger conditions and use cases. This should be 1-3 sentences written in third person.
license: Complete terms in LICENSE.txt
---

# Skill Name

## Overview

[1-2 paragraph explanation of what this skill provides and its purpose]

## When to Use This Skill

[Specific trigger conditions, use cases, and scenarios where Claude should invoke this skill]

## How to Use This Skill

### Step 1: [First Major Step]

[Detailed instructions using imperative form]

### Step 2: [Second Major Step]

[Continue with procedural instructions]

### Step 3: [Additional Steps as Needed]

[More instructions]

## Important Considerations

[Any critical details, edge cases, constraints, or best practices]

## Resources

[Reference any scripts, reference files, or assets included with the skill]
- `scripts/example_script.py` - [What it does]
- `references/schema.md` - [What information it contains]
- `assets/template.xlsx` - [What it's used for]

## Keywords

[Comma-separated list of keywords that might trigger this skill: keyword1, keyword2, keyword3]
```

---

## Writing Style Requirements

**CRITICAL:** All skill content must be written in **imperative/infinitive form**, NOT second person.

### ✅ CORRECT Examples:
- "To accomplish X, do Y"
- "Load the configuration file"
- "Execute the script with these parameters"
- "Consider using this approach when..."
- "Analyze the data by following these steps"

### ❌ INCORRECT Examples:
- "You should do X"
- "If you need to accomplish X"
- "You will find that..."
- "Your next step is to..."

### Metadata Quality Examples

**✅ GOOD description:**
```yaml
description: This skill should be used when analyzing SEC financial filings (10-K, 10-Q) to create comprehensive financial models with automated ratio calculations, trend analysis, and formatted Excel outputs with formulas and charts.
```

**❌ BAD description (too vague):**
```yaml
description: Financial analysis skill for working with data.
```

**❌ BAD description (first person):**
```yaml
description: Use this skill when you want to analyze financial data.
```

---

## Your Task: Generate Skills for These Use Cases

{{USE_CASES_SECTION}}

---

## For Each Skill, You Must Create:

### 1. Complete Folder Structure
- Create the skill folder with proper naming (lowercase, hyphens)
- Include SKILL.md with proper YAML frontmatter
- Add scripts/ folder ONLY if Python execution is needed
- Add references/ folder if detailed documentation should be separate
- Add assets/ folder if templates or resources are needed for output

### 2. SKILL.md Content
Following the exact format specified above with:
- Proper YAML frontmatter (name, description, license)
- Clear overview and purpose
- Specific trigger conditions
- Step-by-step procedural instructions
- Resource references
- Keywords for discoverability

### 3. Python Scripts (if applicable)
- Well-documented, production-ready code
- Clear docstrings explaining purpose and usage
- Error handling and validation
- Example usage in comments

### 4. Reference Files (if applicable)
- Detailed documentation that would clutter SKILL.md
- Database schemas, API specs, or domain knowledge
- Examples and use case walkthroughs

### 5. Asset Files (if applicable)
- Templates (Excel, PowerPoint, etc.)
- Images, icons, or design resources
- Boilerplate code or configuration files

### 6. Testing Materials
Create a `TESTING_GUIDE/` folder with:

**a) `sample_data/` folder containing:**
- Realistic sample data files appropriate to the skill type
- For data analysis: CSV or Excel files with realistic business data
- For API skills: JSON response examples
- For document skills: Sample PDFs or documents
- For image skills: Sample images
- Multiple examples covering different scenarios

**b) `invocation_prompts.txt` with:**
Multiple example prompts following this format:
```
Hey Claude—I just added the "[skill-name]" skill. Can you make something amazing with it?

[Additional context or specific request]
---

Hey Claude—I just added the "[skill-name]" skill. Can you [specific task]?

[Sample data reference or additional details]
---

[3-5 different invocation examples covering various use cases]
```

**c) `test_scenarios.md` with:**
```markdown
# Test Scenarios for [Skill Name]

## Basic Scenarios

### Scenario 1: [Name]
**Input:** [What data/prompt to use]
**Expected Output:** [What should be generated]
**Success Criteria:** [How to verify success]

### Scenario 2: [Name]
[Continue...]

## Intermediate Scenarios

### Scenario 3: [Name]
[More complex test case]

## Advanced Scenarios

### Scenario 4: [Name]
[Edge cases and complex situations]

## Edge Cases to Verify

- [Edge case 1]
- [Edge case 2]
- [Edge case 3]

## Common Issues and Solutions

- **Issue:** [Potential problem]
  **Solution:** [How to fix it]
```

---

## Integration and Overlap Guidance

**Strategy:** {{OVERLAP_STRATEGY}}

{{OVERLAP_GUIDANCE}}

---

## Domain-Specific Considerations

{{DOMAIN_KNOWLEDGE_SECTION}}

{{INTEGRATIONS_SECTION}}

{{CONSTRAINTS_SECTION}}

---

## Quality Standards

Each skill must meet these standards:

1. **Professional Quality**
   - Production-ready code with error handling
   - Clear, comprehensive documentation
   - Follows all formatting requirements exactly

2. **Practical Utility**
   - Solves real business problems
   - Includes concrete examples
   - Provides clear value over general Claude usage

3. **Maintainability**
   - Well-organized file structure
   - Clear separation of concerns
   - Easy to update and extend

4. **Testability**
   - Comprehensive testing materials included
   - Multiple realistic scenarios covered
   - Clear success criteria defined

---

## Output Format

For each skill, provide:

1. A clear summary of what the skill does
2. The complete file structure
3. Full contents of SKILL.md
4. Any Python scripts with complete code
5. Reference files if applicable
6. Asset files descriptions
7. Complete testing guide with sample data

Present each skill in a clear, organized manner that can be directly implemented.

---

## Additional Notes

- Keep SKILL.md under 5,000 words
- Use references/ for detailed docs to keep SKILL.md lean
- Scripts should be token-efficient alternatives to repeated generation
- Assets are files used IN outputs, not loaded into context
- Testing materials should be comprehensive enough to validate all functionality

---

Begin generating the {{SKILL_COUNT}} skills now, following all specifications above.

