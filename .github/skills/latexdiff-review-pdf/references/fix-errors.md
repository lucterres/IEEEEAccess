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

## Error 10: `\cite{}` inside `\DIFadd{}` — soul Reconstruction Failure

### Symptoms
```
! Missing number, treated as zero.
! Illegal unit of measure (pt inserted).
! Package soul Error: Reconstruction failed.
```
Log points to a line like `l.207 ... and alignment of the generated images. }`.

### Cause
When new text containing `~\cite{KEY}` is added, latexdiff wraps the citation in `\mbox{\cite{KEY} }\hskip0pt` inside the `\DIFadd{}` block:

```latex
\DIFadd{...following the pix2pix~\mbox{\cite{pix2pix2017} }\hskip0pt image-to-image...}
```

The `soul` package (`\hl{}`) cannot process `\mbox{\cite{...}}` or `\hskip0pt` inside its argument — it requires fragile commands to be registered via `\soulregister`.

### Fix (manual — surgical edit of `review_clean.tex`)
Move the `\cite{}` outside the `\DIFadd{}` argument:
```latex
% Before (broken):
\DIFadd{...following the pix2pix~\mbox{\cite{pix2pix2017} }\hskip0pt image-to-image...}

% After (fixed):
\DIFadd{...following the pix2pix}~\cite{pix2pix2017}\DIFadd{ image-to-image...}
```

### Fix (PowerShell — global, after cleanup script)
```powershell
$c = Get-Content -Raw "latex_build/review_clean.tex"
# Remove \mbox{} wrappers around \cite (with optional space inside)
$c = $c -replace '\\mbox\{(\\cite\{[^}]+\})\s*\}', '$1'
# Remove any remaining \hskip0pt artefacts
$c = $c -replace '\\hskip0pt\b', ''
$c | Set-Content "latex_build/review_clean.tex" -Encoding UTF8
```

> **Prevention (preferred):** The cleanup script already removes `\hskip0pt`. Add `\mbox{\cite{}}` unwrapping there too — see `latexdiff_cleanup.py` update below.

---

## Error 11: `\cite{}` Between `\DIFaddend` and `\DIFaddbegin` — Broken by `\mbox` Removal

### Symptoms
```
! Missing \endcsname inserted.
! TeX capacity exceeded, sorry [input stack size=10000].
```
Log points to a line with `}\cite{KEY}\DIFaddend\DIFaddbegin\DIFadd{`.

### Cause
After removing `\mbox{\cite{KEY} }`, the pattern `\DIFadd{~}\cite{KEY}\DIFaddend\DIFaddbegin\DIFadd{...}` is left — a `\cite{}` stranded between `\DIFaddend` and `\DIFaddbegin`. The empty `\DIFadd{~}` before it also leaves unbalanced markers.

### Fix (PowerShell)
```powershell
$c = Get-Content -Raw "latex_build/review_clean.tex"
# Collapse: }\cite{KEY}\DIFaddend\DIFaddbegin\DIFadd{ → \cite{KEY}
$c = $c -replace '\\}\s*\\cite\{([^}]+)\}\\DIFaddend\s*\\DIFaddbegin\s*\\DIFadd\{', '\cite{$1} '
$c | Set-Content "latex_build/review_clean.tex" -Encoding UTF8
```

---

## Error 12: `\subsubsection{}` or `\subsection{}` Inside `\DIFaddbegin...\DIFaddend`

### Symptoms
```
! Missing \endcsname inserted.
! TeX capacity exceeded, sorry [input stack size=10000].
```
Log points to a line ending like `...reviewed in Section~\ref{sec:related}.}`.

### Cause
When an entirely new subsubsection is added, latexdiff wraps the heading inside `\DIFaddbegin...\DIFaddend`:

```latex
\DIFaddbegin \subsubsection{\DIFadd{New Section Title}}
\DIFadd{First paragraph...}\DIFaddend
```

LaTeX section commands cannot appear inside `\DIFaddbegin...\DIFaddend` (soul cannot tokenize `\subsubsection`).

Also, a `\ref{}` inside a `\DIFadd{}` block causes the same error unless protected:

```latex
\DIFadd{...methods reviewed in Section~\ref{sec:related}.}
% → must be:
\DIFadd{...methods reviewed in Section~\protect\ref{sec:related}.}
```

### Fix
1. Move the `\subsubsection{}` command **outside** `\DIFaddbegin...\DIFaddend`:
```latex
% Before (broken):
\DIFdelbegin \DIFdel{Old paragraph.}\DIFdelend \DIFaddbegin \subsubsection{\DIFadd{New Title}}
\DIFadd{New content.}\DIFaddend

% After (fixed):
\DIFdelbegin \DIFdel{Old paragraph.}\DIFdelend

\subsubsection{New Title}

\DIFaddbegin \DIFadd{New content.}\DIFaddend
```

2. Replace `\ref{}` with `\protect\ref{}` inside `\DIFadd{}`:
```latex
\DIFadd{...see Section~\protect\ref{sec:related}.}
```

---

## Error 13: Paragraph Breaks Inside a Single `\DIFadd{}` Block

### Symptoms
```
! Missing \endcsname inserted.
! TeX capacity exceeded, sorry [input stack size=10000].
```
or
```
! Argument of \DIFadd has an extra }.
! Paragraph ended before \DIFadd was complete.
```
Log points to the **last line** of a long `\DIFadd{}` that spans multiple paragraphs.

### Cause
When an entire section is rewritten, latexdiff may wrap multiple paragraphs in a single `\DIFaddbegin \DIFadd{...}\DIFaddend` block. The `soul` package (`\hl{}`) cannot span paragraph boundaries — a blank line inside `\DIFadd{}` terminates the argument prematurely.

```latex
\DIFaddbegin \DIFadd{Paragraph one text.

Paragraph two text.

Paragraph three text.}\DIFaddend
```

### Fix
Split the single `\DIFadd{}` block into **one `\DIFaddbegin...\DIFaddend` per paragraph**:

```latex
\DIFaddbegin \DIFadd{Paragraph one text.}\DIFaddend

\DIFaddbegin \DIFadd{Paragraph two text.}\DIFaddend

\DIFaddbegin \DIFadd{Paragraph three text.}\DIFaddend
```

---

## Error 14: `\textbf{\DIFadd{...}}` or Nested Commands Inside `\DIFadd{}`

### Symptoms
```
! Paragraph ended before \textbf was complete.
! Missing } inserted.
! Extra \else.
```
Log points to a line like `l.672 ... (MSE, DSSIM, LBP Distance) is possible}}`.

### Cause
When new text uses `\textbf{...}` containing `\DIFadd{...}` sub-blocks, the nesting creates unbalanced braces and causes `soul` to fail:

```latex
\DIFadd{In summary, }\textbf{\DIFadd{Ferreira }\emph{\DIFadd{et al.}}\DIFadd{~\cite{X} is the only baseline...}}
```

The outer `\textbf{}` closes before the inner `\DIFadd{}` chains resolve.

### Fix
Remove the `\textbf{}` wrapper (and any `}}` residuals) and keep plain text inside `\DIFadd{}`:

```latex
% Before (broken):
\DIFadd{In summary, }\textbf{\DIFadd{Ferreira }\emph{\DIFadd{et al.}}\DIFadd{~\cite{X} is possible}}

% After (fixed):
\DIFadd{In summary, Ferreira }\emph{\DIFadd{et al.}}\DIFadd{~\cite{X} is possible.}
```

Also clean up any double-close braces `}}` that become `}` residuals:
```powershell
# Remove leftover }} that was the textbf closer + DIFadd closer
$c = Get-Content -Raw "latex_build/review_clean.tex"
$c = $c.Replace('is possible}}\DIFadd{.', 'is possible.')
$c | Set-Content "latex_build/review_clean.tex" -Encoding UTF8
```

---

## Error 15: `Too many }'s` — `\DIFadd{}` Block Split at a `\cite{}` or `\emph{}`

### Symptoms
```
! Too many }'s.
l.649 \cite{Ferreira2020} }
                           \hskip0ptwere not publicly released...
You've closed more groups than you opened.
! Too many }'s.
l.649 ... the DSSIM result does indicate is that }
                                                  \emph{\DIFadd{both methods...
```

### Cause
When a **long rewritten paragraph** containing `\cite{}` or `\emph{}` commands is added to `_v7.tex`, latexdiff sometimes splits the `\DIFadd{}` block incorrectly at the citation boundary. The resulting markup has unbalanced closing braces:

```latex
% Generated by latexdiff (broken — extra } before \hskip0pt):
\DIFadd{...Wilcoxon test; however, the sample-level DSSIM values of Ferreira et al.~}
\cite{Ferreira2020} }\hskip0ptwere not publicly released...
```

The stray `}` before `\hskip0pt` closes the `\DIFadd{}` group prematurely, leaving the continuation text and the next `}` without a matching opening group.

This typically happens when the added text contains **`\cite{}` without a preceding `~`** inside a `\DIFadd{}` span, causing latexdiff to break the span at the citation.

### Fix (manual — surgical edit of `review_clean.tex`)
Reconstruct the `\DIFadd{}` block manually, removing the spurious `}` and `\hskip0pt`:

```latex
% Before (broken):
\DIFadd{...values of Ferreira et al.~}\cite{Ferreira2020} }\hskip0ptwere not...indicates that }\emph{\DIFadd{both methods operate...}}

% After (fixed):
\DIFadd{...values of Ferreira et al.~}\cite{Ferreira2020}\DIFadd{ were not...indicates that }\emph{\DIFadd{both methods operate...}}
```

**Pattern:** locate `} }` or `} }\hskip0pt` immediately after a `\cite{...}` inside a `\DIFadd{}` region. Each extra `}` that is not the intended closing brace of a `\DIFadd{}` must be removed.

### Fix (PowerShell — targeted)
```powershell
$c = Get-Content -Raw "latex_build/review_clean.tex"
# Remove \hskip0pt artefacts that latexdiff injects after broken \cite splits
$c = $c -replace '\\hskip0pt\b', ''
# Remove the stray } that lands right after \cite{KEY} and before the continuation
$c = $c -replace '(\\cite\{[^}]+\})\s*\}(\s*[a-z])', '$1 $2'
$c | Set-Content "latex_build/review_clean.tex" -Encoding UTF8
```

> **Note:** `\hskip0pt` removal is already handled by the cleanup script. The stray `}` pattern is harder to fix automatically because it depends on context. Manual inspection is recommended when the log shows `Too many }'s` at a `\cite{}` line.

### Prevention
When writing new paragraphs in `_v7.tex` that contain `\cite{}` inside long sentences, prefer keeping the citation **at the end of a sentence** (before the period), which reduces latexdiff's tendency to break the `\DIFadd{}` span there. Alternatively, split the paragraph into shorter sentences before each `\cite{}`.

---

## Updated Decision Table

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
| `soul Error: Reconstruction failed` + `Missing number` | `\mbox{\cite{}}` inside `\DIFadd{}` | Remove `\mbox{}` + `\hskip0pt` (Error 10) |
| `TeX capacity exceeded` + `}\cite{KEY}\DIFaddend\DIFaddbegin` | Stranded cite between markers | Collapse markers (Error 11) |
| `TeX capacity exceeded` + `\ref{...}` in `\DIFadd{}` | `\ref` or `\subsubsection` inside DIFadd/DIFaddbegin | `\protect\ref` + move heading out (Error 12) |
| `Paragraph ended before \DIFadd was complete` | Multi-paragraph `\DIFadd{}` block | Split into per-paragraph blocks (Error 13) |
| `Paragraph ended before \textbf was complete` + `Extra \else` | `\textbf{\DIFadd{...}}` nesting | Remove `\textbf{}` wrapper (Error 14) |
| **`Too many }'s` at a `\cite{}` line** | **`\DIFadd{}` split incorrectly at `\cite{}`** | **Remove stray `}` + `\hskip0pt` after citation (Error 15)** |
| No PDF after build | Fatal error unresolved | Find `^!` in log |
| `??` in PDF citations | Single-pass compilation | Run pdflatex 2nd time |
