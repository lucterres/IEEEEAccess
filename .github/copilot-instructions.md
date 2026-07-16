# IEEE Access Research Paper Repository

This repository contains a LaTeX manuscript for IEEE Access publication on "Context-oriented Synthesis of Salt Domes in Labeled Seismic Images" by Luciano D. Terres and Jacob Scharcanski.

## Repository Structure

- **Main manuscript**: `_v7.tex` - Current revision file using `ieeeaccess` document class
- **Submitted version**: `docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex` — original submission (OLD for diff)
- **Bibliography**: Manual `\thebibliography{}` environment, NOT BibTeX. `references.bib` exists but is unused
- **Version tracking**: `diffV2.tex`, `review_clean.tex` (raiz) for tracking manuscript changes
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
  "docs/reviewPacote-submetido-jun/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex

# 2. Clean markup (injects yellow highlight style automatically)
python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex review_clean.tex

# 3. Compile (2 passes) — output: Highlighted_PDF.pdf
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF review_clean.tex
```

Output: `latex_build/Highlighted_PDF.pdf` (≥ 2 MB, no `^!` errors)  
Visual: **yellow highlight** = added text, ~~strikethrough~~ = removed text

> **Nota:** `review_clean.tex` fica na **raiz** do workspace (não em `latex_build/`).  
> Isso é necessário para que o pdflatex encontre `ieeeaccess.cls`, `images/`, etc.  
> Pela extensão LaTeX Workshop, use a recipe **`Highlighted PDF (review_clean)`** com o arquivo aberto na raiz.

### Skill & Full Documentation

| Resource | Location |
|----------|----------|
| VS Code skill (auto-invoked) | `.github/skills/latexdiff-review-pdf/SKILL.md` |
| Full workflow guide | `.github/instructions/InstrucoesLatexdiff.md` |
| Error catalogue (9 known errors) | `.github/skills/latexdiff-review-pdf/references/fix-errors.md` |
| Cleanup script | `.github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py` |

> When the user asks to generate the review PDF, run the diff, or compare manuscript versions,
> use the skill at `.github/skills/latexdiff-review-pdf/SKILL.md` and follow its procedure.

---

## Resubmission Review Workflow

**Goal:** Address all reviewer comments, update the manuscript, maintain the response document, and produce the Highlighted PDF for IEEE Access resubmission.

### Key Files

| Role | File |
|------|------|
| Reviewer comments (source of truth) | `reviewACCESS/_Reviewer.md` |
| Response to reviewers document | `reviewACCESS/response_to_reviewers.md` |
| Resubmission instructions (IEEE) | `docs/reviewInstructions/Instructions_to_resubmmit.md` |
| Current manuscript | `_v7.tex` |
| Original submitted version (diff base) | `docs/reviewPacote-submetido-jun/_v6.tex` |
| Highlighted PDF output | `latex_build/Highlighted_PDF.pdf` |

### Reviewers Summary

**Reviewer 1** (`## 🔵 Reviewer 1` in `_Reviewer.md`) — 4 major points:
- R1.1 Comparison with Henriques et al. — **DONE** (Section II rewritten)
- R1.2 VAE implementation details — **DONE** (Section III, arch + hyperparams added)
- R1.3 Expert evaluation design (blinding) — **PARTIALLY DONE** (blind experiment protocol added; results pending)
- R1.4 Statistical significance for DSSIM (~2.2%) — **DONE** (candid discussion added; Wilcoxon infeasibility explained; MSE −16.7% and LBP −12.4% highlighted)

**Reviewer 2** (`## 🟠 Reviewer 2` in `_Reviewer.md`) — 5 points:
- R2.1 Downstream segmentation experiment — **PENDING**
- R2.2 Blind discrimination experiment — **PARTIALLY DONE** (protocol added; results pending)
- R2.3 Expanded baseline comparison (GAN/diffusion) — **DONE** (contextual comparison added: Related Work expanded; new subsubsection + Table~\ref{tab:comparison_overview} in Sec IV; pix2pix2017 bibitem added)
- R2.4 Clearer experimental setting — **DONE** (added explicit note in Dataset section explaining the two experimental contexts: F3 400×400px N=600 vs TGS 101×101px; added Experimental setting note in Ablation Study section; clarified why MSE ranges differ by ~16×)
- R2.5 Reproducibility — **DONE** (VAE details and texture synthesis details added)

### Workflow for Each Reviewer Comment

When asked to address a reviewer comment:
1. **Read** `reviewACCESS/_Reviewer.md` to confirm the exact concern
2. **Edit** `_v7.tex` — make the change in the appropriate section
3. **Update** `reviewACCESS/response_to_reviewers.md`:
   - Under the correct `### Comment R#.#` heading
   - Fill: reviewer quote → author response → action taken → lines changed
4. **Regenerate** `latex_build/Highlighted_PDF.pdf` using the latexdiff skill
5. **Update** the resubmission package with the 3 required files:
   - new folder in `docs/Responses`
   - `response_to_reviewers.md` (exported as DOCX)
   - `Highlighted_PDF.pdf`
   - `_v7.pdf` (clean manuscript)
6. **Update**  Reviewers Summary Status
7. **Expand** errors and solutions in `fix-errors.md` if any new issues arise during diff generation or compilation


### Updating `response_to_reviewers.md`

Each comment entry must follow this structure:
```markdown
### Comment R#.# — <Short Title>

> *"Exact reviewer quote"*

**Response:**
<Author's explanation and justification>

**Action taken in the revised manuscript:**
<What was changed, where (section + line numbers in _v7.tex)>

**Revised text (lines X–Y in `_v7.tex`):**
> *"New or modified passage"*
```

### IEEE Access Resubmission — 3 Required Files

Per `docs/reviewInstructions/Instructions_to_resubmmit.md`:

| # | File | Upload as |
|---|------|-----------|
| 1 | `reviewACCESS/response_to_reviewers.md` (exported as DOCX using `markbin`) | "Author's Response Files" |
| 2 | `latex_build/Highlighted_PDF.pdf` | "Highlighted PDF" |
| 3 | `latex_build/_v7.pdf` (clean, no highlights) | "Main Manuscript" |

### Generating the Highlighted PDF (after manuscript edits)

```powershell
# 1. Generate diff
use latexdiff-review-pdf skill to run:
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewPacote-submetido-jun/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex

# 2. Clean markup
python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex review_clean.tex

# 3. Compile (2 passes)
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF review_clean.tex
```

> Use the skill at `.github/skills/latexdiff-review-pdf/SKILL.md` for full error handling.