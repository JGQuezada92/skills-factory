# Quick Start Guide - Claude Skills Generator

Get your custom Claude Skills up and running in 5 minutes.

## ⚡ 5-Minute Setup

### 1. Install Python Dependencies (30 seconds)

```bash
pip install pyyaml
```

### 2. Configure Your Requirements (2 minutes)

Copy the example configuration:

```bash
cp skills_config.example.yaml skills_config.yaml
```

Edit `skills_config.yaml` and fill in:
- Your business description
- Your industry
- 2-3 specific use cases you want skills for

**Tip:** Keep it simple for your first run. You can always generate more skills later.

### 3. Generate Your Prompt (10 seconds)

```bash
python generate_skills.py
```

This creates: `generated_skills/SKILLS_GENERATION_PROMPT.md`

### 4. Use with Claude (2 minutes)

1. Open `generated_skills/SKILLS_GENERATION_PROMPT.md`
2. Copy the entire file contents (Ctrl+A, Ctrl+C)
3. Open Claude (claude.ai or Claude Code)
4. Paste the prompt into a new conversation
5. Press Enter

### 5. Review & Test (2 minutes)

Claude will generate your skills with:
- ✅ SKILL.md files (ready to use)
- ✅ Python scripts (if needed)
- ✅ Testing guides with sample data
- ✅ Invocation prompt examples
- ✅ .zip files (for easy import)

## 🎯 First-Time Example

Here's what to put in your first `skills_config.yaml`:

```yaml
business:
  description: |
    I run a marketing agency. We create content, analyze campaign 
    performance, and generate client reports weekly.
  industry: "Marketing & Advertising"
  team_size: "5-10"
  primary_workflows:
    - "Content Creation"
    - "Campaign Analysis"

skills:
  count: 2
  overlap_strategy: "overlapping"
  use_cases:
    - name: "Campaign Performance Reporter"
      description: |
        Analyze marketing campaign data (CTR, conversions, ROI) and 
        create formatted Excel reports with visualizations and insights.
      requires_python: true
      sample_data_type: "csv"
      
    - name: "Social Media Content Planner"
      description: |
        Create social media content calendars with post suggestions,
        optimal timing, and engagement strategies.
      requires_python: false
      sample_data_type: "json"

output:
  output_directory: "./generated_skills"
  include_testing_guides: true
  sample_data_style: "realistic"
  test_scenario_depth: "comprehensive"
```

## 🔄 What Happens Next?

1. **Claude generates your skills** (~10-15 minutes)
   - Creates complete folder structure
   - Writes SKILL.md with proper formatting
   - Generates Python scripts if specified
   - Creates testing materials and sample data

2. **You receive structured output:**
   ```
   generated_skills/
   ├── campaign-performance-reporter/
   │   ├── SKILL.md
   │   ├── scripts/analyze_campaign.py
   │   ├── campaign-performance-reporter.zip
   │   └── TESTING_GUIDE/
   │       ├── sample_data/campaign_data.csv
   │       ├── invocation_prompts.txt
   │       └── test_scenarios.md
   │
   └── social-media-content-planner/
       ├── SKILL.md
       ├── social-media-content-planner.zip
       └── TESTING_GUIDE/
           └── ...
   ```

3. **Test your first skill:**
   ```
   Hey Claude—I just added the "campaign-performance-reporter" skill. 
   Can you make something amazing with it?
   
   I've uploaded the sample campaign data. Create a performance report.
   ```

4. **Import into Claude:**
   - Go to Settings → Features → Skills
   - Click "Import Skill"
   - Upload the `.zip` file
   - Start using it!

## 💡 Pro Tips

### Start Small
- Generate 2-3 skills initially
- Test them thoroughly
- Iterate and improve before creating more

### Be Specific
- Vague: "Help with data"
- Specific: "Analyze sales data and create Excel dashboards with pivot tables and charts"

### Use Realistic Examples
- Include actual workflow steps
- Mention specific tools you use
- Describe typical inputs and desired outputs

### Iterate Quickly
- Generate skills → Test → Get feedback → Refine config → Regenerate
- Skills get better with each iteration

## 🚨 Common First-Time Issues

### "Configuration validation failed"
**Fix:** Make sure you replaced ALL placeholder text in `[square brackets]`

### "Template file not found"
**Fix:** Make sure you're running the script from the same directory as the template files

### "Skill doesn't trigger in Claude"
**Fix:** Explicitly invoke it: `Hey Claude—I just added the "skill-name" skill. Can you use it?`

### "Python script errors"
**Fix:** Skills with complex Python requirements might need additional libraries. Check the script's imports.

## 📚 Next Steps

Once you're comfortable:

1. **Read the full README.md** for advanced features
2. **Explore the examples** in `claude_skills_example/`
3. **Create more skills** for different use cases
4. **Share with your team** via the .zip files
5. **Iterate and improve** based on real usage

## 🎓 Learning Resources

- [Full README](README.md) - Comprehensive documentation
- [Configuration Guide](README.md#-configuration-guide) - Detailed config options
- [Anthropic Skills Docs](https://www.anthropic.com/news/skills) - Official documentation
- [Example Skills](https://github.com/anthropics/skills) - Anthropic's skill examples

## ❓ Quick Questions

**Q: How long does generation take?**
A: 10-15 minutes per skill depending on complexity.

**Q: Can I edit generated skills?**
A: Yes! Edit SKILL.md and other files directly. Skills are meant to evolve.

**Q: Do I need to regenerate to make changes?**
A: No. You can manually edit existing skills. Regenerate for major overhauls.

**Q: Can skills work together?**
A: Yes! Use `overlap_strategy: "overlapping"` to create complementary skills.

**Q: What if I don't need Python scripts?**
A: Set `requires_python: false` - Claude will create instruction-only skills.

---

**Ready?** Let's create your first skill in 5 minutes! 🚀

```bash
python generate_skills.py
```

