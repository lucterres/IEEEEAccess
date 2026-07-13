# IEEE Access Color/Grayscale Figure Guidelines

## Overview
This document provides comprehensive guidelines for preparing color and grayscale figures for IEEE Access publication, based on the requirements and the figures in your manuscript.

## General Requirements

### Color/Grayscale Figures
Figures that are meant to appear in **color** or **shades of black/gray** include:
- Photographs
- Illustrations
- Multicolor graphs
- Flowcharts

### Critical Rules
1. **Avoid gray backgrounds or shading** in multicolor graphs
2. **Do not use screenshots** - instead, export graphs directly from the program used to collect data
3. **Export at high resolution** - minimum 300 DPI for photographs, 600-1200 DPI for line art
4. **Use vector formats when possible** - PDF, EPS, or SVG for graphs and diagrams

## Figure Analysis for Your Manuscript

### Current Figures in Document

| Figure | File | Type | Status | Recommendations |
|--------|------|------|--------|-----------------|
| Fig. 1 | `g50.png` | Pipeline/Flowchart | ✓ Good | Consider converting to vector format |
| Fig. 2 | `vaesGen.png` | Grid of samples | ✓ Good | Ensure no gray background |
| Fig. 3 | `edge detection.png` | Image sample | ⚠ Check | Verify contrast levels |
| Fig. 4 | `7.png` | Annotated image | ⚠ Check | Green lines should be clearly visible |
| Fig. 5 | `edge3.jpg` | Process diagram | ⚠ JPEG | Convert to PNG or high-quality format |
| Fig. 6 | `2.png` | Context zones | ✓ Good | Verify color clarity |
| Fig. 7 | `imagens2.png` | Sample grid | ✓ Good | Ensure consistent quality |
| Fig. 8 | `expert.png` | Analysis demo | ✓ Good | Verify text readability |
| Fig. 9 | `sketches.png` | Sketch samples | ✓ Good | Check contrast |
| Fig. 10 | `boxplots.png` | Box plot graph | ⚠ **Priority** | **Must export from source, no screenshots** |

### Biography Photos
| Image | File | Status | Requirements |
|-------|------|--------|--------------|
| Author 1 | `luciano.jpg` | ✓ OK | Professional headshot, good quality |
| Author 2 | `jacob.jpg` | ✓ OK | Professional headshot, good quality |

## Specific Recommendations by Figure Type

### 1. Multicolor Graphs (Fig. 10: boxplots.png)
**CRITICAL REQUIREMENT**: Must be exported directly from the source program

#### Current Issue
- If this is a screenshot, it must be regenerated
- Gray backgrounds are prohibited

#### Action Items
```python
# Example: Proper export from matplotlib (Python)
import matplotlib.pyplot as plt
import numpy as np

# Your plotting code here
fig, ax = plt.subplots(figsize=(10, 6))
# ... your box plot code ...

# Export settings for IEEE Access
plt.savefig('boxplots.png', 
            dpi=300,                    # High resolution
            bbox_inches='tight',        # No extra whitespace
            facecolor='white',          # White background (not gray)
            edgecolor='none',           # No border
            transparent=False)          # Solid background

# Or better yet, use vector format:
plt.savefig('boxplots.pdf', 
            bbox_inches='tight',
            facecolor='white')
```

```r
# Example: Proper export from R
# Your ggplot code here
p <- ggplot(data, aes(...)) + 
     geom_boxplot() +
     theme_minimal() +
     theme(panel.background = element_rect(fill = "white"),
           plot.background = element_rect(fill = "white"),
           panel.grid.major = element_line(color = "gray90"))

# Export for IEEE Access
ggsave("boxplots.png", p, 
       width = 10, height = 6, 
       dpi = 300, 
       bg = "white")

# Or vector format (preferred):
ggsave("boxplots.pdf", p, 
       width = 10, height = 6, 
       bg = "white")
```

### 2. Pipeline/Flowchart Figures (Fig. 1: g50.png)
- **Current**: PNG raster format
- **Recommendation**: Convert to vector format (PDF/EPS) if possible
- **Color usage**: Clear, distinct colors are acceptable
- **Background**: Must be white or transparent, no gray shading

#### Best Practices
- Use tools like draw.io, PowerPoint, or Adobe Illustrator
- Export as PDF or EPS for LaTeX
- Maintain consistent color scheme throughout

### 3. Seismic Image Samples (Figs. 2, 3, 6, 7)
- **Current**: PNG format - appropriate for photographs
- **Resolution**: Ensure at least 300 DPI
- **Contrast**: Verify that grayscale gradients are clear
- **No compression artifacts**: Avoid over-compressed JPEGs

#### Quality Check
```bash
# Check image resolution
identify -format "%f: %wx%h %x x %y\n" images/*.png
```

### 4. Annotated Images (Fig. 4: 7.png)
- **Green overlay lines**: Ensure sufficient contrast
- **Color choice**: Green is acceptable but verify it's visible in grayscale conversion
- **Alternative**: Consider using distinct line styles (solid, dashed) in addition to color

### 5. JPEG Images (Fig. 5: edge3.jpg)
⚠️ **Action Required**
- JPEGs can introduce compression artifacts
- **Recommendation**: Convert to PNG or use original uncompressed format
- If source is PNG, use PNG directly in LaTeX

```bash
# Convert JPEG to high-quality PNG (if needed)
convert edge3.jpg -quality 100 edge3.png
```

## LaTeX Best Practices

### Current Implementation (Good)
```latex
\includegraphics[width=1\linewidth]{images/filename.png}
```

### Enhanced Options
```latex
% For better quality control
\includegraphics[width=\columnwidth, keepaspectratio]{images/filename.png}

% For vector formats (when available)
\includegraphics[width=\columnwidth]{images/filename.pdf}
```

## File Format Recommendations

| Content Type | Preferred Format | Acceptable | Avoid |
|--------------|------------------|------------|-------|
| Graphs/Plots | PDF, EPS | PNG (300+ DPI) | JPEG, Screenshot |
| Photographs | PNG, TIFF | JPEG (high quality) | Low quality JPEG |
| Diagrams | PDF, EPS, SVG | PNG (600+ DPI) | JPEG |
| Line Art | PDF, EPS | PNG (1200 DPI) | Low-res PNG |

## Quality Checklist

### Before Submission
- [ ] All graphs exported from source program (not screenshots)
- [ ] No gray backgrounds in any figure
- [ ] All PNG images are at least 300 DPI
- [ ] JPEG files converted to PNG where appropriate
- [ ] Vector formats (PDF/EPS) used for diagrams/graphs where possible
- [ ] All colors are distinct and meaningful
- [ ] Figures are readable when printed in grayscale
- [ ] Text in figures is legible (minimum 6pt font size)
- [ ] No compression artifacts visible
- [ ] File names match LaTeX references

## Testing for Grayscale Compatibility

Even though your figures are in color, they should remain interpretable in grayscale:

```python
# Python script to test grayscale conversion
from PIL import Image
import matplotlib.pyplot as plt

def test_grayscale(image_path):
    img = Image.open(image_path)
    gray_img = img.convert('L')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.imshow(img)
    ax1.set_title('Original')
    ax1.axis('off')
    
    ax2.imshow(gray_img, cmap='gray')
    ax2.set_title('Grayscale Preview')
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

# Test your figures
test_grayscale('images/boxplots.png')
```

## Common Issues and Solutions

### Issue 1: Screenshot Instead of Export
**Problem**: Using Print Screen or screenshot tools for graphs  
**Solution**: Always use the native export function of your graphing software

### Issue 2: Gray Background
**Problem**: Default theme has gray panel backgrounds  
**Solution**: Explicitly set white or transparent background in export settings

### Issue 3: Low Resolution
**Problem**: Images appear pixelated when zoomed  
**Solution**: Export at minimum 300 DPI for raster images

### Issue 4: Color Dependence
**Problem**: Information lost in grayscale conversion  
**Solution**: Use different line styles, markers, or patterns in addition to color

## Action Items for Your Manuscript

### High Priority
1. **Verify boxplots.png** (Fig. 10)
   - Confirm it was exported from source program
   - Check for gray background
   - Ensure 300+ DPI resolution
   - Re-export if necessary

### Medium Priority
2. **Convert edge3.jpg** (Fig. 5)
   - Replace with PNG format
   - Verify no compression artifacts

3. **Check annotated image** (Fig. 4)
   - Verify green lines are visible
   - Consider adding labels or legends

### Low Priority (Optimization)
4. **Consider vector formats**
   - Convert g50.png to PDF if source is available
   - Improves scalability and reduces file size

5. **Verify all DPI values**
   - Run resolution check on all PNG files
   - Ensure minimum 300 DPI

## Additional Resources

- IEEE Graphics Requirements: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-article/create-graphics-for-your-article/
- Color vs. Grayscale Guidelines: IEEE Author Center
- Recommended Software:
  - Graphs: MATLAB, Python (matplotlib), R (ggplot2)
  - Diagrams: draw.io, Adobe Illustrator, Inkscape
  - Image Processing: GIMP, Photoshop, ImageMagick

## Summary

Your figures are generally well-prepared. The main areas requiring attention are:

1. **Ensure boxplots.png was exported from source** (not screenshot)
2. **Avoid gray backgrounds** in all figures
3. **Consider converting JPEG to PNG** for better quality
4. **Verify resolution** of all raster images (300+ DPI)

Following these guidelines will ensure your figures meet IEEE Access publication standards.