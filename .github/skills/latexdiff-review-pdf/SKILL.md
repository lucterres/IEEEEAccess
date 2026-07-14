---
name: latexdiff-review-pdf
description: >
  Generate a color-coded review PDF showing differences between two LaTeX manuscript versions.
  Red strikethrough = deletions, blue underline = additions.
  Use when: generating review_clean.pdf, creating latexdiff output, comparing .tex versions,
  showing manuscript changes, producing color diff of LaTeX files, gerar PDF de revisão,
  gerar highlighted PDF para IEEE Access, comparar versões do manuscrito, diff entre _v6 e _v7,
  atualizar review_clean.pdf, resubmissão IEEE Access highlighted PDF.
argument-hint: '<old-file> <new-file> (default: _v6.tex vs _v7.tex for this repository)'
mode: agent
---

# Generate Review PDF from Latexdiff

## When to Use
- User asks to generate or update the "Highlighted PDF" (required by IEEE Access for resubmission)
- Comparing two versions of a `.tex` manuscript
- Showing what changed between the submitted version and the revised version
- Red = removed text, Blue = added text
- Qualquer menção a: "gerar diff", "highlighted PDF", "review_clean.pdf", "comparar versões"

## Files in This Repository

| Role | File |
|------|------|
| OLD version (submitted) | `docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex` |
| NEW version (revised)   | `_v7.tex` |
| Cleanup script          | `docs/latexdiff_cleanup.py` |
| Output PDF              | `latex_build/review_clean.pdf` |
| Full instructions       | `docs/InstrucoesLatexdiff.md` |
| Error catalogue         | `.github/skills/latexdiff-review-pdf/references/fix-errors.md` |

## Procedure

### Step 1 — Generate Diff

```powershell
cd "D:\0Code\_phdSeismic\IEEE_Access"
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewACCESS/submetido ao IEEE Access junho 2026/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex
```

Required flags:
- `--allow-spaces` — tolerates spaces in environment names (prevents structural errors)
- `--math-markup=0` — disables diff inside equations (prevents errors in `align`, `equation`)

### Step 2 — Clean the Generated File

```powershell
python docs/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex
```

The script should report:
```
DIFdelbegin left (start-of-line): 0
textbf{} empty left:  0
providecommand{} empty: 0
```

If residuals remain, see [fix-errors.md](./references/fix-errors.md).

### Step 3 — Compile to PDF (Two Passes)

```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex
```

Check for fatal errors:
```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build latex_build/review_clean.tex 2>&1 | Select-String "^!"
```

If errors appear, see [fix-errors.md](./references/fix-errors.md).

### Step 4 — Validate Output

```powershell
Get-Item latex_build/review_clean.pdf | Select-Object Name, Length, LastWriteTime
```

Expected: file exists, size ≥ 2 MB, no `^!` errors in log.

## Success Criteria

- `latex_build/review_clean.pdf` generated with no LaTeX errors
- Red strikethrough visible for removed text
- Blue underline visible for added text
- All cross-references resolved (no `??` in PDF)

> ⚠️ The `ieeeaccess` class redefines colors internally — if colors don't appear, the diff structure is still correct. Use the PDF as "Highlighted PDF" for submission.

## Robustness Tips (Advanced)

| Situation | Action |
|-----------|--------|
| Document uses `\input`/`\include` | Add `--flatten` flag (or pre-expand with `latexpand`) |
| Mysterious package-related errors | Add `--packages=none` flag |
| CRLF encoding issues (`^M` chars) | Run `dos2unix` on both `.tex` files before diff |
| Complex custom commands breaking | Use `--config` to tell latexdiff to skip those blocks |
| Full file won't compile | Diff individual sections separately, then merge |
| Many packages / custom commands | Consider `git-latexdiff` (more stable for complex projects) |

> If `review_clean.tex` still fails to compile after cleanup, open it in VS Code, find the error line in the log, use **Split Right** to compare with `_v7.tex`, and look up the pattern in `fix-errors.md`.

## References

- [Known Errors and Fixes](./references/fix-errors.md)
- [Full Workflow Guide](../../docs/InstrucoesLatexdiff.md)
