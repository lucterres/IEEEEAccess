---
name: latexdiff-review-pdf
description: 'Generate a color-coded review PDF showing differences between two LaTeX manuscript versions. Red strikethrough = deletions, blue underline = additions. Use when: generating review.pdf, creating latexdiff output, comparing .tex versions, showing manuscript changes, producing color diff of LaTeX files, updating review.tex from git commits.'
argument-hint: '<commit-base> (optional git commit hash to compare against; defaults to HEAD~1)'
---

# Generate Review PDF from Latexdiff

## When to Use
- User asks to generate or update `review.pdf`
- Comparing two versions of `_v6.tex` (or any `.tex` manuscript)
- Showing what changed between git commits in a color-coded PDF
- Red = removed text, Blue = added text

## Procedure

### Step 1 — Identify Comparison Base

```powershell
cd "d:\0Code\_phdSeismic\IEEE_Access"
git log --oneline --decorate -10
```

Use the commit hash provided by the user, or select the most meaningful ancestor commit (e.g., the last commit on `main` before current branch diverged).

### Step 2 — Export Baseline Version

```powershell
git show <COMMIT_HASH>:_v6.tex > _v6_base.tex
```

### Step 3 — Generate Diff with Latexdiff

```powershell
latexdiff --math-markup=0 --append-textcmd="PARstart" _v6_base.tex _v6.tex > review.tex
```

Required flags for this repository:
- `--math-markup=0` — prevents invalid DIFdel inside math environments
- `--append-textcmd="PARstart"` — marks `\PARstart` as safe text command

### Step 4 — Check for Structural Errors

```powershell
pdflatex -interaction=nonstopmode review.tex > review_build_check.log 2>&1
Select-String "^!" review_build_check.log | Select-Object -First 20
```

If errors appear, proceed to [Step 5 — Fix Errors](./references/fix-errors.md). Otherwise skip to Step 6.

### Step 5 — Fix Structural Errors (if any)

See [fix-errors.md](./references/fix-errors.md) for the full catalogue of known errors and workarounds.

**Quick fixes**:

1. **DIFdel wrapping a `\begin{itemize}` or `\begin{enumerate}` block**:
   Replace the fragmented `\item%DIFAUXCMD` structure with a plain comment:
   ```latex
   % (List deleted in this revision)
   ```

2. **DIFdelFL inside table with many columns**:
   Replace the entire malformed `\DIFdelend \begin{table}...\DIFaddendFL \end{table}` block with a clean table containing only the new version's data (no DIFdel/DIFadd markup).

3. **Paragraph-level DIFdel spanning blank lines**:
   Consolidate into a single `\DIFdel{full paragraph text}` on one line, or remove if too complex.

### Step 6 — Compile (Two Passes)

```powershell
pdflatex -interaction=nonstopmode review.tex > review_build1.log 2>&1
pdflatex -interaction=nonstopmode review.tex > review_build2.log 2>&1
```

### Step 7 — Validate Output

```powershell
if (Test-Path review.pdf) {
    Write-Host "✓ review.pdf generated"
    Get-Item review.pdf | Select-Object Name, Length, LastWriteTime
} else {
    Write-Host "✗ Build failed"
    Select-String "^!" review_build2.log | Select-Object -First 10
}
```

Expected output:
- File exists
- Size ≥ 2 MB (for a ~15-page manuscript)
- No `^!` errors in logs

### Step 8 — Clean Up

```powershell
Remove-Item _v6_base.tex -ErrorAction SilentlyContinue
```

## Success Criteria

- `review.pdf` generated with no LaTeX errors
- Red strikethrough visible for removed text
- Blue underline visible for added text  
- All cross-references resolved (no `??` in PDF)

## References

- [Known Errors and Fixes](./references/fix-errors.md)
- [Full Workflow Guide](../../docs/skillsIA/InstruçõesLatexdiff.md)
