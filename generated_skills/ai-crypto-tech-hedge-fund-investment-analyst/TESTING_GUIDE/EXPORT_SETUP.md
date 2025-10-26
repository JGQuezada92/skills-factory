# Export Setup Guide

## Installing Required Libraries for PDF and Word Export

To enable automatic PDF and Word document generation, install these Python libraries:

### **Option 1: Install All at Once (Recommended)**

```bash
pip install python-docx markdown2 weasyprint
```

### **Option 2: Install Individually**

**For Word (.docx) Export:**
```bash
pip install python-docx
```

**For PDF Export:**
```bash
pip install markdown2 weasyprint
```

**Note:** WeasyPrint may require additional dependencies on Windows. If you encounter issues, see troubleshooting below.

---

## Testing the Export Functionality

### **Test 1: Manual Script Test**

Run the export script directly to test:

```bash
cd "C:\Users\Jonathan Quezada\OneDrive - Phenom People, Inc\Desktop\Claude Skills\generated_skills\ai-crypto-tech-hedge-fund-investment-analyst\scripts"

python memo_exporter.py
```

**Expected Output:**
```
Testing memo export functionality...
✓ Saved Markdown: C:\Users\Jonathan Quezada\...\skills artifacts\Example_Company_Investment_Memo_[timestamp].md
✓ Saved PDF: C:\Users\Jonathan Quezada\...\skills artifacts\Example_Company_Investment_Memo_[timestamp].pdf
✓ Saved Word Document: C:\Users\Jonathan Quezada\...\skills artifacts\Example_Company_Investment_Memo_[timestamp].docx

Export Complete! Files saved to:
C:\Users\Jonathan Quezada\OneDrive - Phenom People, Inc\Desktop\Claude Skills\skills artifacts
```

---

### **Test 2: Using the Skill in Claude**

After re-importing the updated skill:

```
Hey Claude—I just updated the "ai-crypto-tech-hedge-fund-investment-analyst" skill.

Please analyze Anthropic as an investment opportunity, then export the memo to PDF and Word format.
```

**Claude will:**
1. Generate the investment memo
2. Automatically run the export script
3. Save files to the skills artifacts folder
4. Confirm file locations

---

## Output Location

All exported files are saved to:
```
C:\Users\Jonathan Quezada\OneDrive - Phenom People, Inc\Desktop\Claude Skills\skills artifacts\
```

**File Naming Convention:**
```
[Company_Name]_Investment_Memo_[Timestamp].[extension]

Examples:
- Anthropic_Investment_Memo_20251025_151530.md
- Anthropic_Investment_Memo_20251025_151530.pdf
- Anthropic_Investment_Memo_20251025_151530.docx
```

---

## Troubleshooting

### **Issue: WeasyPrint installation fails on Windows**

**Solution 1: Use GTK3 Runtime**
1. Download GTK3 runtime from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install the runtime
3. Retry: `pip install weasyprint`

**Solution 2: Skip PDF export**
- Only install `python-docx` for Word export
- Use browser Print-to-PDF for PDF generation

---

### **Issue: "Module not found" error**

**Solution:**
Ensure you're using the same Python environment where you installed the libraries:

```bash
# Check which Python you're using
python --version
which python  # or "where python" on Windows

# Install libraries to the correct Python
python -m pip install python-docx markdown2 weasyprint
```

---

### **Issue: Files not appearing in skills artifacts folder**

**Solution:**
Check that the folder path is correct:

```python
# The script uses this path:
C:/Users/Jonathan Quezada/OneDrive - Phenom People, Inc/Desktop/Claude Skills/skills artifacts
```

If your folder is named differently or in a different location, edit `memo_exporter.py`:

```python
# Line ~25 in memo_exporter.py
self.output_dir = Path("YOUR_CUSTOM_PATH_HERE")
```

---

## Manual Export (Without Libraries)

If you don't want to install the Python libraries, you can still export memos:

### **Method 1: Browser Print-to-PDF**
1. Generate the memo in Claude
2. Press `Ctrl+P` (or Cmd+P on Mac)
3. Select "Save as PDF"
4. Save to skills artifacts folder

### **Method 2: Online Converters**
1. Save the memo as Markdown (.md)
2. Use online converter:
   - **Markdown to PDF:** https://www.markdowntopdf.com/
   - **Markdown to Word:** https://www.markdowntoword.com/
3. Download and save to skills artifacts folder

### **Method 3: Copy-Paste to Word**
1. Generate the memo in Claude
2. Copy the entire memo
3. Paste into Microsoft Word
4. Apply formatting as needed
5. Save to skills artifacts folder

---

## Features of Exported Documents

### **PDF Features:**
- ✅ Professional formatting (1-inch margins)
- ✅ Clean typography (Calibri 11pt)
- ✅ Styled headers (H1, H2, H3)
- ✅ Formatted tables
- ✅ Print-ready quality
- ✅ Portable (works on any device)

### **Word (.docx) Features:**
- ✅ Fully editable
- ✅ Professional formatting
- ✅ Easy to share with team
- ✅ Version control friendly
- ✅ Comments and track changes enabled
- ✅ Compatible with all Microsoft Office versions

### **Markdown (.md) Features:**
- ✅ Source file for regeneration
- ✅ Version control friendly (Git)
- ✅ Human-readable
- ✅ Easy to edit and iterate
- ✅ Can be converted to any format

---

## Next Steps

1. ✅ Install the required libraries (if desired)
2. ✅ Test the export script
3. ✅ Re-import the skill to Claude.ai
4. ✅ Generate a memo and request export
5. ✅ Check the skills artifacts folder for files

---

**Last Updated:** 2025-10-25  
**Skill Version:** 1.1 (with export functionality)


