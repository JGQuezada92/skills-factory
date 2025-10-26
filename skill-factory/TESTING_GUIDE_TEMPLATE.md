# Testing Guide Template for Claude Skills

This template should be included with each generated skill to ensure comprehensive testing coverage.

---

# Test Guide for [SKILL_NAME]

## Quick Start

**Skill Invocation:**
```
Hey Claude—I just added the "[skill-name]" skill. Can you make something amazing with it?
```

## Overview

This testing guide provides comprehensive scenarios for validating the `[skill-name]` skill. Use the sample data provided in the `sample_data/` folder to test each scenario.

---

## Sample Data Files

The following sample data files are included for testing:

### `sample_data/[filename]`
**Description:** [What this file contains]
**Use Case:** [Which scenarios use this file]
**Format:** [CSV/JSON/Excel/PDF/etc.]

### `sample_data/[filename2]`
**Description:** [What this file contains]
**Use Case:** [Which scenarios use this file]
**Format:** [CSV/JSON/Excel/PDF/etc.]

---

## Invocation Prompts

### Basic Invocation
```
Hey Claude—I just added the "[skill-name]" skill. Can you make something amazing with it?

I've uploaded [sample_data_file]. Please [specific action].
```

### Specific Task Example 1
```
Hey Claude—I just added the "[skill-name]" skill. Can you [specific task description]?

Use the attached [file_name] and focus on [specific aspect].
```

### Specific Task Example 2
```
Hey Claude—I just added the "[skill-name]" skill. I need help with [specific problem].

Context: [Additional details about the task]
Expected outcome: [What you want to achieve]
```

### Advanced Usage Example
```
Hey Claude—I just added the "[skill-name]" skill. Can you [complex multi-step task]?

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Use the data from [file_name].
```

### Edge Case Example
```
Hey Claude—I just added the "[skill-name]" skill. I have [edge case situation].

Can you handle [specific edge case]?
```

---

## Test Scenarios

### Basic Scenarios

#### Scenario 1: [Simple Use Case Name]

**Objective:** Validate that the skill can perform its core function with standard input.

**Setup:**
- Use `sample_data/[filename]`
- No special configuration needed

**Invocation:**
```
Hey Claude—I just added the "[skill-name]" skill. Can you [basic task] using the attached file?
```

**Expected Output:**
- [Expected result 1]
- [Expected result 2]
- [Expected format/structure]

**Success Criteria:**
- ✓ Output is generated without errors
- ✓ [Specific validation point 1]
- ✓ [Specific validation point 2]
- ✓ Results are accurate and complete

**Estimated Time:** [X minutes]

---

#### Scenario 2: [Another Basic Task]

**Objective:** [What this scenario tests]

**Setup:**
- [Setup instructions]

**Invocation:**
```
[Specific prompt]
```

**Expected Output:**
- [Expected results]

**Success Criteria:**
- ✓ [Criterion 1]
- ✓ [Criterion 2]
- ✓ [Criterion 3]

**Estimated Time:** [X minutes]

---

### Intermediate Scenarios

#### Scenario 3: [More Complex Use Case]

**Objective:** Test the skill's ability to handle [specific complexity].

**Setup:**
- Use `sample_data/[filename]`
- [Additional setup if needed]

**Invocation:**
```
Hey Claude—I just added the "[skill-name]" skill. Can you [more complex task]?

[Additional context or requirements]
```

**Expected Output:**
- [Expected result with more detail]
- [Specific features or capabilities demonstrated]

**Success Criteria:**
- ✓ [More detailed criterion 1]
- ✓ [More detailed criterion 2]
- ✓ Output demonstrates [specific capability]
- ✓ [Additional validation]

**Estimated Time:** [X minutes]

---

#### Scenario 4: [Multi-Step Workflow]

**Objective:** Validate the skill's ability to handle multi-step workflows.

**Setup:**
- [Setup details]

**Invocation:**
```
[Multi-step prompt]
```

**Expected Output:**
- [Step 1 output]
- [Step 2 output]
- [Final integrated result]

**Success Criteria:**
- ✓ Each step completes successfully
- ✓ Steps are properly sequenced
- ✓ Final output integrates all steps
- ✓ [Additional criteria]

**Estimated Time:** [X minutes]

---

### Advanced Scenarios

#### Scenario 5: [Complex Edge Case or Advanced Feature]

**Objective:** Test the skill's robustness with [complex situation].

**Setup:**
- [Complex setup details]
- [Special considerations]

**Invocation:**
```
[Advanced prompt with detailed requirements]
```

**Expected Output:**
- [Sophisticated output description]
- [Expected handling of complexity]

**Success Criteria:**
- ✓ [Advanced criterion 1]
- ✓ Handles [complex situation] gracefully
- ✓ [Performance or quality metric]
- ✓ [Edge case handling]

**Estimated Time:** [X minutes]

---

#### Scenario 6: [Integration or Scale Test]

**Objective:** Test [integration with other tools/large scale data].

**Setup:**
- [Integration setup]

**Invocation:**
```
[Integration test prompt]
```

**Expected Output:**
- [Output demonstrating integration]

**Success Criteria:**
- ✓ [Integration works smoothly]
- ✓ [Scale is handled appropriately]
- ✓ [Performance is acceptable]

**Estimated Time:** [X minutes]

---

## Edge Cases to Verify

### Edge Case 1: [Missing or Incomplete Data]
**Test:** [How to test this edge case]
**Expected Behavior:** Skill should [handle gracefully/provide helpful error/request clarification]

### Edge Case 2: [Unusual Input Format]
**Test:** [How to test]
**Expected Behavior:** [Expected handling]

### Edge Case 3: [Large Scale Input]
**Test:** [How to test with large data]
**Expected Behavior:** [Performance expectations]

### Edge Case 4: [Conflicting Requirements]
**Test:** [How to create conflicting requirements]
**Expected Behavior:** [How skill should resolve or clarify]

### Edge Case 5: [Invalid or Corrupted Data]
**Test:** [How to test with bad data]
**Expected Behavior:** [Error handling expectations]

---

## Common Issues and Solutions

### Issue 1: [Common Problem]
**Symptoms:** [What you might see]
**Cause:** [Why this happens]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

### Issue 2: [Another Common Problem]
**Symptoms:** [Observable issues]
**Cause:** [Root cause]
**Solution:** [Resolution steps]
**Prevention:** [Best practices]

### Issue 3: [Skill Not Triggering]
**Symptoms:** Claude doesn't invoke the skill when expected
**Cause:** Invocation prompt may not match skill description triggers
**Solution:** 
- Review the skill description in SKILL.md
- Use keywords from the skill's trigger conditions
- Be more explicit: "Use the [skill-name] skill to..."
**Prevention:** Include clear trigger keywords in your initial prompt

---

## Performance Benchmarks

### Expected Performance Metrics

| Scenario | Expected Duration | Acceptable Range |
|----------|------------------|------------------|
| Basic Scenario 1 | [X minutes] | [Y-Z minutes] |
| Intermediate Scenario 3 | [X minutes] | [Y-Z minutes] |
| Advanced Scenario 5 | [X minutes] | [Y-Z minutes] |

### Quality Metrics

- **Accuracy:** [Expected accuracy level or validation criteria]
- **Completeness:** [What constitutes complete output]
- **Formatting:** [Expected output quality standards]
- **Usability:** [User experience expectations]

---

## Testing Checklist

Use this checklist to ensure comprehensive testing:

- [ ] All basic scenarios tested and passed
- [ ] All intermediate scenarios tested and passed
- [ ] All advanced scenarios tested and passed
- [ ] All edge cases verified
- [ ] Sample data files are appropriate and realistic
- [ ] Invocation prompts work as documented
- [ ] Error handling works correctly
- [ ] Performance meets expectations
- [ ] Output quality meets standards
- [ ] Integration points (if any) work correctly
- [ ] Documentation is accurate and helpful
- [ ] Python scripts (if any) execute correctly
- [ ] Reference files (if any) are loaded properly
- [ ] Assets (if any) are used correctly

---

## Feedback and Iteration

### What to Note During Testing

- Scenarios where the skill excels
- Scenarios where the skill struggles
- Unexpected behaviors or outputs
- Suggestions for improvement
- Additional use cases discovered
- Performance issues or bottlenecks

### How to Improve This Skill

Based on testing results:
1. Identify patterns in issues or limitations
2. Review SKILL.md for clarity and completeness
3. Consider adding reference files for complex topics
4. Evaluate if Python scripts would improve reliability
5. Update sample data to be more representative
6. Refine skill description for better triggering

---

## Additional Resources

- **SKILL.md:** Core skill documentation
- **scripts/:** Python scripts included with skill (if any)
- **references/:** Additional documentation (if any)
- **assets/:** Templates and resources (if any)

---

## Contact and Support

For issues with this skill or suggestions for improvement:
- Review the skill's SKILL.md for detailed instructions
- Check if Claude Code or API version affects behavior
- Verify sample data matches expected formats
- Consult Claude's official Skills documentation

---

**Last Updated:** [Date]
**Skill Version:** 1.0
**Tested With:** Claude [version/product]

