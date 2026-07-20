---
name: latexdiff-review-pdf
description: >
  Generate a review PDF showing differences between two LaTeX manuscript versions.
  Yellow highlight = additions, strikethrough = deletions.
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
- **Yellow highlight** = added text, **strikethrough** = removed text
- Qualquer menção a: "gerar diff", "highlighted PDF", "review_clean.pdf", "comparar versões"

## Files in This Repository

| Role | File |
|------|------|
| OLD version (submitted) | `docs/reviewPacote-submetido-jun/_v6.tex` |
| NEW version (revised)   | `_v7.tex` |
| Cleanup script          | `.github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py` |
| Output PDF              | `latex_build/Highlighted_PDF.pdf` |
| Full instructions       | `.github/instructions/InstrucoesLatexdiff.md` |
| Error catalogue         | `.github/skills/latexdiff-review-pdf/references/fix-errors.md` |

## Procedure

### Step 1 — Generate Diff

```powershell
cd "D:\0Code\_phdSeismic\IEEE_Access"
latexdiff --allow-spaces --math-markup=0 `
  "docs/reviewPacote-submetido-jun/_v6.tex" `
  _v7.tex > latex_build/review_raw.tex
```

Required flags:
- `--allow-spaces` — tolerates spaces in environment names (prevents structural errors)
- `--math-markup=0` — disables diff inside equations (prevents errors in `align`, `equation`)

### Step 2 — Clean the Generated File

```powershell
python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex _review_clean.tex
```

The script should report:
```
\DIFadd{} markers preserved: <N>
\DIFdel{} markers preserved: <N>
FL markers left (should be 0): 0
providecommand{} empty left:  0
```

If **`FL markers left`** is non-zero → run cleanup again or manually remove remaining `\DIFaddFL{}`/`\DIFdelFL{}`.

If script prints **`WARNING: multi-paragraph \DIFadd{} block(s) found`** → those blocks must be split manually before compiling (see **Error 13** in `fix-errors.md`).

If other residuals remain, see [fix-errors.md](./references/fix-errors.md).

### Step 3 — Compile to PDF (Two Passes)

```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF _review_clean.tex
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF _review_clean.tex
```

Check for fatal errors:
```powershell
pdflatex -interaction=nonstopmode -output-directory=latex_build -jobname=Highlighted_PDF _review_clean.tex 2>&1 | Select-String "^!"
```

If errors appear, see [fix-errors.md](./references/fix-errors.md).

> **Quick triage guide for `^!` errors:**
> | Error message | Likely cause | See |
> |---|---|---|
> | `soul Error: Reconstruction failed` + `Missing number` | `\mbox{\cite{}}` inside `\DIFadd` | Error 10 |
> | `TeX capacity exceeded` + `}\cite{KEY}\DIFaddend\DIFaddbegin` | Stranded cite between markers | Error 11 |
> | `TeX capacity exceeded` + line ends in `\ref{...}.}` | `\ref{}` inside `\DIFaddbegin` sem `\soulregister\ref{1}` | Error 12 |
> | `Paragraph ended before \DIFadd was complete` | Multi-paragraph `\DIFadd{}` block | Error 13 |
> | `Argument of \DIFadd has an extra }` + `Paragraph ended` | `\textbf{\DIFadd{...}}` nesting | Error 14 |
> | `Undefined color '{red}'` + `soul Error: Reconstruction failed` | `\textcolor{red}{}` inside `\DIFadd{}` | Error 13 |
> | `Argument of \DIFdel has an extra }` (many lines) | `\DIFdel` crossing list/heading | Errors 1, 3, 7 |
> | `Command \DIFadd undefined` | Preamble duplicado (cleanup rodado 2×); apenas `\renewcommand` sem `\providecommand` | Apagar 1º bloco duplicado |
> 
> **Visual issue (sem erro de compilação):**
> | Sintoma no PDF | Causa | Fix |
> |---|---|---|
> | Highlight amarelo interrompido em `~Section X` / `~Table X` | `\protect\ref{}` dentro de `\DIFadd{}` | Mover ref para fora do bloco (Error 12 — visual) |

### Step 4 — Validate Output

```powershell
Get-Item latex_build/Highlighted_PDF.pdf | Select-Object Name, @{N='Size_MB';E={[math]::Round($_.Length/1MB,2)}}, LastWriteTime
```

Expected: file exists, size ≥ 2 MB, no `^!` errors in log.

## Success Criteria

- `latex_build/review_clean.pdf` generated with no LaTeX errors
- **Yellow highlight** visible for added text (IEEE Access requirement: "yellow highlighting indicating changes")
- **Strikethrough** (no color) visible for removed text
- All cross-references resolved (no `??` in PDF)

> ⚠️ The cleanup script injects `soul` + `xcolor` into the preamble to produce yellow highlights.
> It also strips `\textcolor{}{}` wrappers **inside** `\DIFadd{}` blocks (e.g. TODO markers),
> because `soul`'s `\hl` cannot process `\textcolor` in its argument.

## How the Yellow Highlight Works (Technical)

The cleanup script (Step 8) injects into the preamble:

```latex
\PassOptionsToPackage{dvipsnames,table}{xcolor}
\usepackage{xcolor}
\usepackage{soul}
\usepackage[normalem]{ulem}
\sethlcolor{yellow}
\soulregister\textbf{1}  % register commands that appear inside \DIFadd{}
\soulregister\cite{1}
% ...
\renewcommand{\DIFadd}[1]{\ifmmode\textcolor{blue}{#1}\else\hl{#1}\fi}
\renewcommand{\DIFdel}[1]{\ifmmode\textcolor{red}{#1}\else\sout{#1}\fi}
```

Key decisions:
- `\colorbox` was rejected — it does not break lines (text overflows margins)
- `soul` requires `xcolor` loaded **before** it to work with `ieeeaccess.cls` (which uses the older `color` package)
- `\textcolor{}{}` inside `\DIFadd{}` is stripped by the Python script before compile

## Robustness Tips (Advanced)

| Situation | Action |
|-----------|--------|
| Document uses `\input`/`\include` | Add `--flatten` flag (or pre-expand with `latexpand`) |
| Mysterious package-related errors | Add `--packages=none` flag |
| CRLF encoding issues (`^M` chars) | Run `dos2unix` on both `.tex` files before diff |
| Complex custom commands breaking | Use `--config` to tell latexdiff to skip those blocks |
| Full file won't compile | Diff individual sections separately, then merge |

> If `_review_clean.tex` still fails to compile after cleanup, open it in VS Code, find the error line in the log, use **Split Right** to compare with `_v7.tex`, and look up the pattern in `fix-errors.md`.

## References

- [Known Errors and Fixes](./references/fix-errors.md)
- [Full Workflow Guide](../../instructions/InstrucoesLatexdiff.md)
