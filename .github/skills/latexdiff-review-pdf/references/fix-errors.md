# Known Errors and Workarounds — Latexdiff for LaTeX Manuscripts

## Overview

When `latexdiff` generates markup for rewritten sections (lists → tables, subsections moved, bold text in list items), structural errors often result. This guide catalogs the most common errors and provides surgical fixes.

> **Best approach:** If a fix is too complex, replace the **entire affected block** (table, list, subsection) with a clean version from the new `.tex` file, removing all `\DIFdel`/`\DIFadd`/`\DIFaddFL` markup.

---

## Error 1: DIFdel Wrapping List Items

### Symptoms
```
! Argument of \DIFdel has an extra }.
! Paragraph ended before \DIFdel was complete.
```
Repeated 5–10 times in sequence.

### Cause
When an entire `\begin{itemize}` or `\begin{enumerate}` block is deleted, latexdiff wraps one `\DIFdel{...}` per `\item` in fragmented AUX blocks:

```latex
\begin{itemize}%DIFAUXCMD
%DIFDELCMD <     \item %%%
\item%DIFAUXCMD
\textbf{\DIFdel{Type A}}%DIFAUXCMD
```

LaTeX cannot handle `\DIFdel` crossing list structure boundaries.

### Fix
Replace the entire fragmented block with a comment:

```latex
% (Training process steps deleted in this revision)
```

---

## Error 2: DIFdelFL in Multi-Column Tables

### Symptoms
```
! Argument of \DIFdelFL has an extra }.
! Missing } inserted.
! Extra }, or forgotten \endgroup.
```

### Cause
When tables with many columns (>4) are replaced by simpler tables, latexdiff generates `\DIFdelFL{}` wrappers inside `\begin{tabular*}` cells:

```latex
\DIFdelFL{511.83 }%DIFDELCMD < & %%%
\DIFdelFL{987.74}%DIFDELCMD < & %%%
```

These fragment LaTeX's column parsing.

### Fix
Replace the entire table block with a clean, markup-free version from the new `.tex`:

```powershell
$content = [System.IO.File]::ReadAllText("review.tex", [System.Text.Encoding]::UTF8)
$replacement = @'
\begin{table}[htbp]
    \centering
    \caption{<NEW CAPTION>}
    \label{<NEW LABEL>}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Method} & \textbf{MSE} & \textbf{DSSIM} & \textbf{LBP Distance} \\
        \midrule
        Proposed & 2037.88 & 0.1537 & 0.0283 \\
        \bottomrule
    \end{tabular}
\end{table}
'@
$new = [regex]::Replace($content,
    '\\DIFdelend \\begin\{table\}\[htbp\][\s\S]*?\\DIFaddendFL \\end\{table\}',
    $replacement, 1)
[System.IO.File]::WriteAllText("review.tex", $new, [System.Text.Encoding]::UTF8)
```

---

## Error 3: DIFdel Wrapping Paragraph Headings

### Symptoms
```
! LaTeX Error: Not allowed in LR mode.
! Extra }, or forgotten \endgroup.
```

### Cause
Latexdiff wraps `\paragraph{...}` in `\DIFdel{}`, forbidden in LaTeX's restricted horizontal mode:

```latex
\paragraph{\DIFdel{GAN-Based Image Synthesis:}} %DIFAUXCMD
```

### Fix
Replace the entire deleted section (heading + content + any list) with a comment:

```latex
% GAN-Based Image Synthesis section deleted in this revision
```

---

## Error 4: Unicode Characters from Latexdiff

### Symptoms
```
! LaTeX Error: Unicode character ├ö├Â┬ú (U+251C)
! LaTeX Error: Unicode character ├ö├▓├ª (U+2551)
```

### Cause
On Windows, `latexdiff` may output box-drawing Unicode when terminal encoding is not UTF-8.

### Fix
These are non-fatal in `nonstopmode`. If they block compilation, strip them:

```powershell
$content = Get-Content review.tex -Encoding UTF8
$content | ForEach-Object { $_ -replace '[^\x00-\x7F\u00C0-\u024F]', '' } |
    Set-Content review_clean.tex -Encoding UTF8
Move-Item review_clean.tex review.tex -Force
```

---

## Error 5: `\DIFaddbegin` Disabled by `%` Comment

### Symptoms
```
! Argument of \DIFaddFL has an extra }.
! Paragraph ended before \DIFaddFL was complete.
```

### Cause
If a line starts with `% ... \DIFaddbegin`, LaTeX treats everything after `%` as comment, leaving `\DIFaddend` unmatched:

```latex
% (Deleted heading) \DIFaddbegin ...
```

### Fix
Split into separate lines:

```latex
% (Deleted heading)
\DIFaddbegin ...
\DIFaddend
```

---

## Error 6: Mixed FL Markers in Table Rows

### Symptoms
```
! Argument of \DIFaddFL has an extra }.
! Missing } inserted.
! Extra }, or forgotten \endgroup.
```

### Cause
Latexdiff splits a cell with mixed add/delete markers across row boundaries:

```latex
\DIFaddFL{3}\DIFaddendFL ,\DIFdelbeginFL ... \DIFdelendFL \DIFaddbeginFL \DIFaddFL{820}
```

### Fix
Replace the full table with a clean final version. Cell-by-cell patching is error-prone.

---

## Error 7: `\textbf{\DIFdel{...}}` or `\textbf{\DIFadd{...}}` — Many Occurrences

### Symptoms
```
! Argument of \DIFdel has an extra }.
```
Repeated at many lines (e.g., `l.662`, `l.666`, `l.670`…), each pointing to `\textbf{\DIFdel{Type A}}`, `\textbf{\DIFdel{Type B}}`, etc.

### Cause
When a deleted list has `\textbf{...}` inside each `\item`, latexdiff wraps with `\DIFdel{}` inside `\textbf{}`. LaTeX cannot handle `\DIFdel` (using `\sout`) inside `\textbf{}`:

```latex
\textbf{\DIFdel{Type A}}%DIFAUXCMD
\textbf{\DIFdel{Type B}}%DIFAUXCMD
```

### Fix
Use global PowerShell regex to strip `\DIFdel`/`\DIFadd`/`\DIFaddFL` from all `\textbf{}`, `\subsection`, `\paragraph`:

```powershell
$content = [System.IO.File]::ReadAllText("review.tex", [System.Text.Encoding]::UTF8)
$content = $content -replace '\\textbf\{\\DIFdel\{([^}]+)\}\}(%DIFAUXCMD)', '\textbf{$1}$2'
$content = $content -replace '\\textbf\{\\DIFadd(?:FL)?\{([^}]+)\}\}', '\textbf{$1}'
$content = $content -replace '\\subsection\{\\DIFdel\{([^}]+)\}\}', '\subsection{$1}'
$content = $content -replace '\\paragraph\{\\DIFdel\{([^}]+)\}\}', '\paragraph{$1}'
[System.IO.File]::WriteAllText("review.tex", $content, [System.Text.Encoding]::UTF8)
```

> Run **before compiling** to catch all instances at once.

---

## Error 8: `Misplaced \omit` — DIFaddendFL Inside `\multicolumn`

### Symptoms
```
! Misplaced \omit.
! Argument of \DIFaddFL has an extra }.
```
Log points to a `\multicolumn{N}{c}{\DIFaddendFL ...}` line.

### Cause
`\DIFaddendFL` calls `\omit`, valid only at cell start, not inside `\multicolumn{}{}{...}`. When table column count changes (6 → 3), latexdiff generates:

```latex
\multicolumn{3}{c}{\DIFaddendFL \textbf{MSE}} \\
```

The `\DIFaddendFL` lands inside the argument — forbidden.

### Fix
Replace the **entire table** with the clean version. See Error 2 for the PowerShell pattern.

---

## Error 9: Entirely New Table Wrapped in `\DIFaddbegin...\DIFaddend`

### Symptoms
```
! Argument of \DIFaddFL has an extra }.
! Misplaced \omit.
```
Log points to table cell lines with `\DIFaddFL{...}`.

### Cause
Entirely new tables are wrapped in `\DIFaddbegin...\DIFaddend`, with `\DIFaddFL{}` on every cell:

```latex
\DIFaddbegin \begin{table}[!t]
\caption{\DIFaddFL{Caption text.}}
\textbf{\DIFaddFL{Metric}} & \DIFaddendFL ...
```

### Fix
Remove the `\DIFaddbegin`/`\DIFaddend` wrappers and all `\DIFaddFL`/`\DIFaddendFL` markup:

```latex
\begin{table}[!t]
\caption{Caption text.}
\textbf{Metric} & ...
\end{table}
```

---

## Decision Table: Pattern → Fix

| Pattern | Root Cause | Fix |
|---|---|---|
| `Argument of \DIFdel has an extra }` in `\item` context | DIFdel crosses list structure | Replace list with comment |
| `Argument of \DIFdelFL has an extra }` in tabular | DIFdelFL inside table cell | Replace table (no DIFdelFL) |
| `Paragraph ended before \DIFdel was complete` | DIFdel spans blank lines | One-line or remove |
| `Not allowed in LR mode` | DIFdel in `\paragraph{}` heading | Remove section block |
| `Unicode character U+251C` | Terminal encoding issue | Strip non-ASCII |
| `Argument of \DIFaddFL` after `% ... \DIFaddbegin` | Comment hides `\DIFaddbegin` | Split lines |
| `Missing } inserted` + `Extra }` in table | Mixed FL in one cell | Replace table |
| `Argument of \DIFdel/\DIFadd has an extra }` (many lines) | DIFdel/DIFadd in `\textbf{}` | PowerShell global regex (Error 7) |
| `Misplaced \omit` at `\multicolumn{\DIFaddendFL ...}` | DIFaddendFL inside multicolumn arg | Replace table |
| `Argument of \DIFaddFL` in new table | Whole table in DIFaddbegin | Remove DIFaddbegin/DIFaddend + DIFaddFL |
| No PDF after build | Fatal error unresolved | Find `^!` in log |
| `??` in PDF citations | Single-pass compilation | Run pdflatex 2nd time |
