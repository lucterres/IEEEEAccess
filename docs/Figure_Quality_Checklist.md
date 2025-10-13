# IEEE Access Figure Quality Checklist

Quick reference checklist for preparing figures according to IEEE Access requirements.

## ✅ Pre-Submission Checklist

### General Requirements
- [ ] All figures are in color or grayscale (no mixed format)
- [ ] No gray backgrounds or shading in any figure
- [ ] All text in figures is readable (minimum 6pt font)
- [ ] Figures are appropriately sized for the column width
- [ ] All figure numbers and captions are correct in LaTeX

### Multicolor Graphs (CRITICAL)
- [ ] **Exported directly from source program** (NOT screenshots)
- [ ] No gray panel backgrounds
- [ ] Clear legend with distinct colors
- [ ] Colors remain distinguishable in grayscale
- [ ] White or transparent background only
- [ ] Minimum 300 DPI for raster formats

### File Formats
- [ ] Graphs: PDF/EPS (preferred) or PNG at 300+ DPI
- [ ] Photographs: PNG or high-quality JPEG
- [ ] Diagrams/Flowcharts: PDF/EPS (preferred) or PNG at 600+ DPI
- [ ] No screenshot formats (avoid low-quality images)

### Resolution Check
- [ ] Photographs: ≥ 300 DPI
- [ ] Line art/Diagrams: ≥ 600 DPI (ideally 1200 DPI)
- [ ] Graphs: Vector format (PDF/EPS) or ≥ 300 DPI PNG
- [ ] Author photos: ≥ 300 DPI, professional quality

### Color Usage
- [ ] Colors are meaningful (not decorative only)
- [ ] Sufficient contrast between different elements
- [ ] Figures readable in grayscale conversion
- [ ] Avoid red-green combinations (colorblind-friendly)

## 📊 Your Manuscript Figures

### Priority Actions Required

#### HIGH PRIORITY
1. **Figure 10 (boxplots.png)**
   - [ ] Verify: Exported from source program (not screenshot)?
   - [ ] Check: No gray background present?
   - [ ] Confirm: Resolution ≥ 300 DPI?
   - [ ] If any NO: Re-export from R/Python/MATLAB

#### MEDIUM PRIORITY
2. **Figure 5 (edge3.jpg)**
   - [ ] Convert JPEG to PNG format
   - [ ] Check for compression artifacts
   - [ ] Update LaTeX reference if filename changes

3. **Figure 4 (7.png with green lines)**
   - [ ] Verify green overlay is clearly visible
   - [ ] Test grayscale conversion
   - [ ] Consider adding labels/legend if needed

#### LOW PRIORITY (Optimization)
4. **All PNG figures**
   - [ ] Check DPI of all PNG files
   - [ ] Consider converting diagrams to vector (PDF/EPS)
   - [ ] Optimize file sizes if needed

## 🔍 Quick Tests

### Test 1: Resolution Check
```bash
# Windows (using ImageMagick if installed)
magick identify -format "%f: %wx%h %x x %y DPI\n" images/*.png

# Or check file properties in Windows Explorer
# Right-click → Properties → Details → Look for dimensions and DPI
```

### Test 2: Grayscale Preview
Open each color figure in an image viewer and convert to grayscale to verify:
- Information is not lost
- Contrast is sufficient
- Different elements remain distinguishable

### Test 3: Background Check
- Open figure in image editor
- Check if background is pure white (#FFFFFF) or transparent
- NO gray shades (#F0F0F0, #CCCCCC, etc.)

## 📝 Figure-by-Figure Status

| Figure # | Filename | Type | Status | Action Needed |
|----------|----------|------|--------|---------------|
| 1 | g50.png | Pipeline | ✅ Good | Optional: Convert to vector |
| 2 | vaesGen.png | Grid | ✅ Good | Verify no gray background |
| 3 | edge detection.png | Sample | ⚠️ Check | Verify contrast |
| 4 | 7.png | Annotated | ⚠️ Check | Test green line visibility |
| 5 | edge3.jpg | Diagram | ❌ **Action** | **Convert to PNG** |
| 6 | 2.png | Zones | ✅ Good | Verify clarity |
| 7 | imagens2.png | Grid | ✅ Good | Check consistency |
| 8 | expert.png | Analysis | ✅ Good | Verify text readability |
| 9 | sketches.png | Samples | ✅ Good | Check contrast |
| 10 | boxplots.png | Graph | ⚠️ **Priority** | **Verify export source** |

## 🚀 Action Plan

### Step 1: Critical Issues (Do First)
1. Open the source file used to create `boxplots.png`
2. Re-export with settings:
   - White background (no gray)
   - 300+ DPI for PNG, or use PDF format
   - No screenshots
3. Replace the file in `images/` folder

### Step 2: Format Conversion
1. Convert `edge3.jpg` to PNG:
   ```bash
   # Using ImageMagick
   magick convert edge3.jpg edge3.png
   
   # Or use image editor: GIMP, Photoshop, Paint.NET
   ```
2. Update LaTeX if filename changes

### Step 3: Quality Verification
1. Check resolution of all PNG files
2. Preview all figures in grayscale
3. Verify no gray backgrounds anywhere

### Step 4: Final Review
1. Compile LaTeX document
2. Review all figures in the PDF
3. Zoom in to check quality
4. Verify captions and references

## 📚 Quick Reference: Export Settings

### Python (Matplotlib)
```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
# Or better:
plt.savefig('figure.pdf', bbox_inches='tight', facecolor='white')
```

### R (ggplot2)
```r
ggsave("figure.png", width=10, height=6, dpi=300, bg="white")
# Or better:
ggsave("figure.pdf", width=10, height=6, bg="white")
```

### MATLAB
```matlab
print('figure', '-dpng', '-r300')  % 300 DPI PNG
% Or better:
print('figure', '-dpdf')  % Vector PDF
```

## ⚠️ Common Mistakes to Avoid

1. ❌ Using Print Screen or screenshot tools
2. ❌ Gray panel backgrounds in graphs
3. ❌ Low resolution images (< 300 DPI)
4. ❌ JPEG for non-photographic content
5. ❌ Depending only on color (use patterns/markers too)
6. ❌ Unreadable small text in figures
7. ❌ Inconsistent styling across figures

## ✨ Best Practices

1. ✅ Export directly from source software
2. ✅ Use vector formats (PDF/EPS) for graphs and diagrams
3. ✅ White or transparent backgrounds only
4. ✅ High resolution (300+ DPI) for raster images
5. ✅ Test grayscale conversion
6. ✅ Consistent color scheme across all figures
7. ✅ Clear, readable labels and legends

## 📞 Need Help?

If you're unsure about any figure:
1. Refer to the detailed guide: `IEEE_Access_Figure_Guidelines.md`
2. Check IEEE Author Center: https://journals.ieeeauthorcenter.ieee.org/
3. Contact the journal editor for specific questions

## ✅ Final Sign-Off

Before submitting:
- [ ] All items in Pre-Submission Checklist completed
- [ ] All HIGH PRIORITY actions resolved
- [ ] All figures tested in final PDF compilation
- [ ] No warnings or errors in LaTeX compilation
- [ ] Document ready for submission

---

**Remember**: The most critical rule is to **export graphs from source programs** and **avoid gray backgrounds**. These are the two most common violations of IEEE Access figure requirements.