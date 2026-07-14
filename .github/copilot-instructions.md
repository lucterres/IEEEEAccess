# IEEE Access Research Paper Repository

This repository contains a LaTeX manuscript for IEEE Access publication on "Context-oriented Synthesis of Salt Domes in Labeled Seismic Images" by Luciano D. Terres and Jacob Scharcanski.

## Repository Structure

- **Main manuscript**: `_v7.tex` - Current revision file using `ieeeaccess` document class
- **Submitted version**: `docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex` — original submission (OLD for diff)
- **Bibliography**: Manual `\thebibliography{}` environment, NOT BibTeX. `references.bib` exists but is unused
- **Version tracking**: `diffV2.tex`, `latex_build/review_clean.tex` for tracking manuscript changes
- **Images**: `images/` folder contains figures (PNG/JPG format) referenced in manuscript
- **Build artifacts**: `latex_build/` contains compiled PDFs and auxiliary LaTeX files
- **Documentation**: `docs/` contains IEEE Access figure quality guidelines and checklists

## Key LaTeX Conventions

### Document Structure
```latex
\documentclass{ieeeaccess}
\title{Context-oriented Synthesis of Salt Domes in Labeled Seismic Images}
\author{\uppercase{Luciano D. Terres}\authorrefmark{1} and \uppercase{Jacob Scharcanski}\authorrefmark{1}}
```

### Bibliography Management
- Uses **manual bibliography** with `\begin{thebibliography}{00}` ... `\end{thebibliography}`
- Citations use `\cite{AuthorYear}` format (e.g., `\cite{Zeng2019}`, `\cite{He2016}`)
- DO NOT use BibTeX commands like `\bibliography{}` or `\bibliographystyle{}`

### Figure Handling
- Figures stored in `images/` directory, referenced as `\includegraphics{images/filename.png}`
- Follow IEEE Access guidelines from `docs/Figure_Quality_Checklist.md`:
  - Export graphs directly from source programs (NOT screenshots)
  - Use 300+ DPI for photographs, 600+ DPI for line art
  - Avoid gray backgrounds, prefer vector formats (PDF/EPS) when possible

### Special Packages & Configuration
```latex
\usepackage[T1]{fontenc}
\usepackage{lmodern}     % Font handling for better PDF output
\usepackage{mathptmx}    % Times font for math
\usepackage{booktabs}    % Professional table formatting
\usepackage{siunitx}     % Scientific units
```

## Build Process

The manuscript compiles to `latex_build/_v7.pdf`. LaTeX auxiliary files (`.aux`, `.log`, `.out`, `.synctex.gz`) are contained in `latex_build/` directory.

## Research Domain Context

This paper focuses on **seismic image synthesis** using Variational Autoencoders (VAEs) and texture synthesis for salt dome detection. Key concepts:
- Seismic imaging and salt body identification
- Data augmentation for deep learning segmentation models
- VAE-based generative modeling for geophysical data

## Figure Quality Requirements

When adding/modifying figures, consult `docs/IEEE_Access_Figure_Guidelines.md` for specific requirements:
- Figure 10 (`boxplots.png`) marked as priority - must be exported from source, not screenshot
- Biography photos need specific formatting
- All multicolor graphs require direct export, no gray backgrounds

## Common Tasks

1. **Adding citations**: Add to manual bibliography section, use `\cite{AuthorYear}` in text
2. **Adding figures**: Place in `images/`, reference with `\includegraphics{images/filename}`
3. **Version comparison**: Use existing diff files as templates for tracking changes
4. **PDF compilation**: Build artifacts go to `latex_build/` directory

## Generating the Review/Highlighted PDF (latexdiff)

**IEEE Access resubmission requires a "Highlighted PDF"** showing all changes marked in color.
This workflow is fully documented and has a dedicated VS Code skill.

### Quick Reference (3 commands)

```powershell
# 1. Generate diff
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex

# 2. Clean markup
python docs/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex

# 3. Compile (2 passes)
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
```

Output: `latex_build/review_clean.pdf` (≥ 2 MB, no `^!` errors)

### Skill & Full Documentation

| Resource | Location |
|----------|----------|
| VS Code skill (auto-invoked) | `.github/skills/latexdiff-review-pdf/SKILL.md` |
| Full workflow guide | `docs/InstrucoesLatexdiff.md` |
| Error catalogue (9 known errors) | `.github/skills/latexdiff-review-pdf/references/fix-errors.md` |
| Cleanup script | `docs/latexdiff_cleanup.py` |

> When the user asks to generate the review PDF, run the diff, or compare manuscript versions,
> use the skill at `.github/skills/latexdiff-review-pdf/SKILL.md` and follow its procedure.