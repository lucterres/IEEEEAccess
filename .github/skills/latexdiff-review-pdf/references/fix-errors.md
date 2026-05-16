# Known Errors and Workarounds — Latexdiff for LaTeX Manuscripts

## Error 1: DIFdel Wrapping List Items

### Symptoms
```
! Argument of \DIFdel has an extra }.
! Paragraph ended before \DIFdel was complete.
```

Repeated multiple times in the log, typically 5–10 occurrences in sequence.

### Cause
When an entire `\begin{itemize}` or `\begin{enumerate}` block is deleted, latexdiff generates one `\DIFdel{...}` per `\item`, wrapping them in fragmented AUX blocks:

```latex
\begin{itemize}%DIFAUXCMD
%DIFDELCMD <     \item %%%
\item%DIFAUXCMD
\textbf{\DIFdel{Type A}}%DIFAUXCMD
\DIFdel{: description text...
    }%DIFDELCMD < \item %%%
```

LaTeX cannot process `\DIFdel` that spans list structure boundaries.

### Fix
Replace the entire fragmented block (from `%DIFDELCMD < \begin{itemize}` through `%DIFDELCMD < \end{itemize}`) with a comment:

```latex
% (Sketch types A-E deleted in this revision)
```

Same approach for `\begin{enumerate}`:
```latex
% (Training process steps deleted in this revision)
```

---

## Error 2: DIFdelFL in Multi-Column Tables

### Symptoms
```
! Argument of \DIFdelFL has an extra }.
! Paragraph ended before \DIFdelFL was complete.
! Missing } inserted.
! Extra }, or forgotten \endgroup.
```

### Cause
When a table with many columns (> 4) is replaced by a simpler table, latexdiff generates `\DIFdelFL{}` wrappers inside `\begin{tabular*}` cells, with dangling `%DIFDELCMD < & %%%` tokens:

```latex
\DIFdelFL{511.83 }%DIFDELCMD < & %%%
\DIFdelFL{987.74  }%DIFDELCMD < & %%%
```

These fragment LaTeX's column parsing.

### Fix
Use a PowerShell regex replacement to rewrite the entire table block with a clean, markup-free version:

```powershell
$p = 'review.tex'
$raw = Get-Content $p -Raw
$replacement = @'
\begin{table}[htbp]
    \centering
    \caption{<CAPTION>}
    \label{<LABEL>}
    \begin{tabular}{lccc}
        \toprule
        \textbf{Method} & \textbf{MSE} & \textbf{DSSIM} & \textbf{LBP Distance} \\
        \midrule
        Ferreira \emph{et al.}~\cite{Ferreira2020} & 4712.1 & 0.39 & 0.17 \\
        Proposed method & 2037.88 & 0.1537 & 0.0283 \\
        \bottomrule
    \end{tabular}
\end{table}
'@
$new = [regex]::Replace($raw,
    '\\DIFdelend \\begin\{table\}\[htbp\][\s\S]*?\\DIFaddendFL \\end\{table\}',
    $replacement, 1)
Set-Content $p $new
```

---

## Error 3: DIFdel Wrapping Nested Paragraph Subsection

### Symptoms
```
! LaTeX Error: Not allowed in LR mode.
! Extra }, or forgotten \endgroup.
```

### Cause
Latexdiff wraps `\paragraph{...}` heading lines in `\DIFdel{}`, which is not allowed inside LaTeX's restricted horizontal mode for headings.

```latex
\paragraph{\DIFdel{GAN-Based Image Synthesis:}} %DIFAUXCMD
```

### Fix
Replace the entire deleted `\paragraph{...}` block (heading + associated content + following list if any) with a comment:

```latex
% GAN-Based Image Synthesis section deleted in this revision
```

---

## Error 4: Unicode Characters from Latexdiff

### Symptoms
```
! LaTeX Error: Unicode character Ôö£ (U+251C)
! LaTeX Error: Unicode character Ôòæ (U+2551)
```

### Cause
Latexdiff occasionally inserts box-drawing Unicode characters (U+251C, U+2551, etc.) in its output on Windows when the terminal encoding is not UTF-8.

### Fix
These are non-fatal and can be ignored in `nonstopmode`. If they prevent compilation, strip them:

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

Often appears after manually commenting out a deleted heading and keeping `\DIFaddbegin` on the same line.

### Cause
If a line starts with `% ... \DIFaddbegin`, LaTeX treats everything after `%` as comment, so `\DIFaddbegin` is not executed. A later `\DIFaddend` then becomes unmatched.

### Fix
Split into two lines:

```latex
% (Deleted subsection heading)
\DIFaddbegin ...
```

---

## Error 6: Mixed FL Markers Corrupting a Table Row

### Symptoms
```
! Argument of \DIFaddFL has an extra }.
! Missing } inserted.
! Extra }, or forgotten \endgroup.
```

### Cause
Latexdiff may split a single numeric/table cell with mixed add/delete markers across row boundaries, e.g.:

```latex
\DIFaddFL{3}\DIFaddendFL ,\DIFdelbeginFL ... \DIFdelendFL \DIFaddbeginFL \DIFaddFL{820}
```

This breaks both `\DIF...` grouping and tabular parsing.

### Fix
Replace the full table environment with a clean final table (no `\DIFaddFL`/`\DIFdelFL` inside cells). This is usually faster and safer than trying to patch cell-by-cell.

---

## Error 7: `\textbf{\DIFdel{...}}` or `\textbf{\DIFadd{...}}` — Multiple Occurrences

### Symptoms
```
! Argument of \DIFdel has an extra }.
! Paragraph ended before \DIFdel was complete.
```
Repeated many times (same line number), e.g. `l.662`, `l.666`, `l.670`… each pointing to a `\textbf{\DIFdel{Type A}}`, `\textbf{\DIFdel{Type B}}`, etc.

### Cause
When a deleted list had `\textbf{...}` inside each `\item`, latexdiff wraps the bold text with `\DIFdel{}` inside `\textbf{}`. LaTeX cannot handle `\DIFdel` (which uses `\sout`) inside `\textbf{}`:

```latex
\textbf{\DIFdel{Type A}}%DIFAUXCMD
\textbf{\DIFdel{Type B}}%DIFAUXCMD
```

Similarly, added content can produce `\textbf{\DIFadd{Results and Analysis}}`, `\textbf{\DIFaddFL{Metric}}`, etc.

### Fix
Use a global PowerShell regex to strip the `\DIFdel`/`\DIFadd`/`\DIFaddFL` wrappers from all `\textbf{}` arguments at once. Also covers `\subsection` and `\paragraph` sectioning commands:

```powershell
$content = [System.IO.File]::ReadAllText("$PWD\review.tex", [System.Text.Encoding]::UTF8)
# Remove \DIFdel inside \textbf (DIFAUXCMD context)
$content = $content -replace '\\textbf\{\\DIFdel\{([^}]+)\}\}(%DIFAUXCMD)', '\textbf{$1}$2'
# Remove \DIFadd / \DIFaddFL inside \textbf (any context)
$content = $content -replace '\\textbf\{\\DIFadd(?:FL)?\{([^}]+)\}\}', '\textbf{$1}'
# Remove \DIFdel inside \subsection and \paragraph headings
$content = $content -replace '\\subsection\{\\DIFdel\{([^}]+)\}\}', '\subsection{$1}'
$content = $content -replace '\\paragraph\{\\DIFdel\{([^}]+)\}\}', '\paragraph{$1}'
[System.IO.File]::WriteAllText("$PWD\review.tex", $content, [System.Text.Encoding]::UTF8)
```

> **Note:** Run this BEFORE compiling, as the first pass will reveal if there are still remaining instances.

---

## Error 8: `Misplaced \omit` — DIFaddendFL / DIFdelendFL Inside `\multicolumn`

### Symptoms
```
! Misplaced \omit.
! Argument of \DIFaddFL has an extra }.
```

Typically at a `\multicolumn{N}{c}{...}` line that contains a `\DIFaddendFL` or `\DIFdelendFL` inside the third argument:

```
l.798 ...ticolumn{3}{c}{\DIFaddendFL \textbf{MSE}}
```

### Cause
`\DIFaddendFL` and `\DIFdelendFL` internally call `\omit`, which is only valid at the start of a table cell — not inside `\multicolumn{}{}{...}` arguments. When a table's column count changed (e.g., 6 → 3 columns), latexdiff generates:

```latex
\DIFdelbeginFL %DIFDELCMD < \multicolumn{6}{c}{%%%
\DIFdelendFL \DIFaddbeginFL \multicolumn{3}{c}{\DIFaddendFL \textbf{MSE}} \\
```

The `\DIFaddendFL` lands inside the `{...}` argument of `\multicolumn`, which is forbidden.

### Fix
Replace the **entire table** (from `\begin{table}` to `\end{table}`) with the clean final version from `_v6.tex`. This is always safer than trying to patch individual `\multicolumn` rows. See [Error 2](#error-2-difdelfl-in-multi-column-tables) for the PowerShell replacement pattern.

---

## Error 9: Entirely New Table Wrapped in `\DIFaddbegin...\DIFaddend`

### Symptoms
```
! Argument of \DIFaddFL has an extra }.
! Paragraph ended before \DIFaddFL was complete.
! Misplaced \omit.
```

The log points to table cell lines like:
```
l.869 \textbf{\DIFaddFL{Metric}}
```

### Cause
When a table exists only in the new version (entirely added), latexdiff wraps the whole `\begin{table}...\end{table}` inside `\DIFaddbegin...\DIFaddend` and marks every cell with `\DIFaddFL{...}`:

```latex
\DIFaddbegin \begin{table}[!t]
\caption{\DIFaddFL{Caption text.}}
...
\textbf{\DIFaddFL{Metric}} & \textbf{\DIFaddFL{VAE}} & \DIFaddendFL ...
```

The `\DIFaddFL`/`\DIFaddendFL` inside tabular cells again trigger the `\omit` restriction.

### Fix
Replace the entire `\DIFaddbegin \begin{table}...\end{table}\n\DIFaddend` block with the clean table from `_v6.tex`, removing the `\DIFaddbegin`/`\DIFaddend` wrappers entirely:

```powershell
# Manual edit: locate the block and paste the clean table directly.
# The result should be:
\begin{table}[!t]
\caption{Clean caption.}
\label{tab:example}
...clean tabular content...
\end{table}
```

Use `replace_string_in_file` with a unique anchor (e.g., `\label{tab:ablation_masks}`) to identify and replace the block.

---

## Decision Table: Error → Fix

| Error Pattern | Root Cause | Fix |
|---|---|---|
| `Argument of \DIFdel has an extra }` | DIFdel inside list `\item` | Replace whole list with comment |
| `Argument of \DIFdelFL has an extra }` | DIFdelFL inside tabular cell | Rewrite table without DIFdelFL |
| `Paragraph ended before \DIFdel was complete` | DIFdel spans blank lines | Consolidate on one line or remove |
| `Not allowed in LR mode` | DIFdel around `\paragraph{}` | Remove entire paragraph block |
| `Unicode character U+251C` | latexdiff inserted box chars | Strip non-ASCII or ignore in nonstopmode |
| `Argument of \DIFaddFL has an extra }` after `% ... \DIFaddbegin` | `\DIFaddbegin` commented out | Move `\DIFaddbegin` to next line |
| `Missing } inserted` + `Extra }, or forgotten \endgroup` in table | Mixed FL markers in one row/cell | Replace full table with clean version |
| `Argument of \DIFdel has an extra }` at `\textbf{\DIFdel{...}}` (many lines) | DIFdel/DIFadd inside `\textbf{}` | Global PowerShell regex (Error 7) |
| `Misplaced \omit` at `\multicolumn{N}{c}{\DIFaddendFL ...}` | DIFaddendFL inside multicolumn arg | Replace whole table with clean version (Error 8) |
| `Argument of \DIFaddFL has an extra }` in entirely new table | Whole table wrapped in DIFaddbegin | Remove DIFaddbegin/DIFaddend + DIFaddFL from table (Error 9) |
| Missing `review.pdf` after build | Fatal error in nonstopmode | Find `^!` in log and fix |
| `??` citations in PDF | Single-pass compilation | Run pdflatex a second time |
