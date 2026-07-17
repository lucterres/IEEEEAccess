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

## Error 12: `\ref{}` (ou `\protect\ref{}`) dentro de `\DIFadd{}` — soul Quebra a Continuidade

### Symptoms
```
! Missing \endcsname inserted.
! TeX capacity exceeded, sorry [input stack size=10000].
```
O log aponta para linhas como:
```
l.484 ... described in Section~\ref{sec:ablation}}
l.660 }
l.726 }}
```

### Cause
O pacote `soul` (`\hl{}`) — usado por `\DIFadd{}` para o highlight amarelo — **não consegue processar `\ref{label}` dentro de seu argumento**. A chave `}` que fecha `\ref{label}` é interpretada como fechamento prematuro do `\hl{...}` (ou `\DIFadd{...}`), corrompendo o balanço de chaves e causando o loop de capacidade do TeX.

O prefixo `\protect` agrava ainda mais o problema: `~\protect\ref{label}` dentro de `\DIFadd{}` gera `Missing \endcsname` antes mesmo do erro de capacidade.

Exemplo de código problemático gerado pelo latexdiff:
```latex
\DIFadd{, and also for the ablation experiments described in Section~\protect\ref{sec:ablation}}
\DIFadd{diffusion-based seismic image synthesis methods reviewed in Section~\protect\ref{sec:related}.}
\DIFadd{...Table~\protect\ref{tab:metricsSummary}.}
```

### Fix — Passo 1: remover `\protect` (PowerShell)
```powershell
(Get-Content "review_clean.tex" -Raw) -replace '~\\protect\\ref\{', '~\ref{' |
    Set-Content "review_clean.tex" -NoNewline
```

### Fix — Passo 2: quebrar `\DIFadd{}` ao redor de cada `\ref{}` (manual)
Após remover `\protect`, ainda resta o conflito de chaves. Para cada `\ref{}` dentro de um `\DIFadd{}`, quebre o bloco de forma que o `\ref{}` fique **fora** do argumento do `\DIFadd{}`:

```latex
% Antes (quebrado):
\DIFadd{texto antes do ref~\ref{label}. Texto após.}

% Depois (corrigido) — se o \ref for o ÚLTIMO elemento do bloco \DIFadd:
...texto antes~}\DIFaddend \ref{label}. Texto fora do bloco adicionado.

% Depois (corrigido) — se houver texto adicionado APÓS o \ref também:
...texto antes~}\DIFaddend \ref{label}\DIFaddbegin \DIFadd{ texto após.}
```

> ⚠️ **Não introduzir `\DIFaddbegin \DIFadd{}\DIFaddend` vazio** após o `\ref`. Se não há texto adicionado após o `\ref`, basta fechar com `\DIFaddend` e deixar o resto (ponto, vírgula, texto normal) fora do bloco.

Exemplos reais corrigidos em `review_clean.tex`:
```latex
% Caso: \ref é o último elemento — apenas fecha e deixa o ponto fora
...described in Section~}\DIFaddend \ref{sec:ablation}.

% Caso: há texto adicionado após o \ref
...methods reviewed in Section~}\DIFaddend \ref{sec:related}\DIFaddbegin \DIFadd{.
}

% Caso: \ref no meio de um \parbox com vários \ref — cada um quebrado individualmente
...comparison in Table~}\DIFaddend \ref{tab:metricsSummary}\DIFaddbegin \DIFadd{.}
\DIFadd{As noted in Section~}\DIFaddend \ref{sec:results}\DIFaddbegin \DIFadd{, the smaller ...lower than those in Table~}\DIFaddend \ref{tab:metricsSummary}\DIFaddbegin \DIFadd{ (F3, ...}
```

### Prevention
Adicionar `\soulregister\ref{1}` no preâmbulo do `review_clean.tex` **não resolve** este problema, pois o conflito é de chaves (`}` do `\ref{label}` fecha o `\DIFadd{}`), não de comandos não registrados. A única solução robusta é manter `\ref{}` fora do argumento de `\DIFadd{}`.
