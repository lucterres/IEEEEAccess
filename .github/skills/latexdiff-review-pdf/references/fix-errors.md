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
    Set-Content _review_clean.tex -Encoding UTF8
Move-Item _review_clean.tex review.tex -Force
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

### Fix (manual — surgical edit of `_review_clean.tex`)
Move the `\cite{}` outside the `\DIFadd{}` argument:
```latex
% Before (broken):
\DIFadd{...following the pix2pix~\mbox{\cite{pix2pix2017} }\hskip0pt image-to-image...}

% After (fixed):
\DIFadd{...following the pix2pix}~\cite{pix2pix2017}\DIFadd{ image-to-image...}
```

### Fix (PowerShell — global, after cleanup script)
```powershell
$c = Get-Content -Raw "_review_clean.tex"
# Remove \mbox{} wrappers around \cite (with optional space inside)
$c = $c -replace '\\mbox\{(\\cite\{[^}]+\})\s*\}', '$1'
# Remove any remaining \hskip0pt artefacts
$c = $c -replace '\\hskip0pt\b', ''
$c | Set-Content "_review_clean.tex" -Encoding UTF8
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
$c = Get-Content -Raw "_review_clean.tex"
# Collapse: }\cite{KEY}\DIFaddend\DIFaddbegin\DIFadd{ → \cite{KEY}
$c = $c -replace '\\}\s*\\cite\{([^}]+)\}\\DIFaddend\s*\\DIFaddbegin\s*\\DIFadd\{', '\cite{$1} '
$c | Set-Content "_review_clean.tex" -Encoding UTF8
```

---

## Error 12: `\ref{}` dentro de `\DIFadd{}` — soul e conflito de chaves

> **Status (2026-07-18):** Este erro **não ocorre** com o setup atual do preamble, que inclui `\soulregister\ref{1}`. O latexdiff também tende a dividir naturalmente `\DIFadd{}` nos pontos de `\ref{}`. A seção abaixo é mantida como referência para setups sem `\soulregister\ref{1}`.

### Symptoms (sem `\soulregister\ref{1}` no preamble)
```
! Missing \endcsname inserted.
! TeX capacity exceeded, sorry [input stack size=10000].
```

### Cause
Sem `\soulregister\ref{1}`, o pacote `soul` não sabe que `\ref` recebe 1 argumento. Ao encontrar `\ref{label}` dentro de `\hl{}` (expansão de `\DIFadd{}`), o `}` de fechamento de `\ref{label}` é interpretado como fechamento prematuro do próprio `\hl{...}`, corrompendo o balanço de chaves.

Com `\protect\ref{label}` o problema é ainda pior: gera `Missing \endcsname` antes do erro de capacidade.

### Por que não ocorre no setup atual

O preamble injetado pelo `latexdiff_cleanup.py` inclui:
```latex
\soulregister\ref{1}
```
Isso registra `\ref` no soul como comando de 1 argumento. O soul então processa `\ref{label}` corretamente dentro de `\hl{...}`, sem confundir o `}` do argumento com o fechamento do highlight.

Adicionalmente, o latexdiff tende a dividir `\DIFadd{}` naturalmente nos pontos onde há `\ref{}`, resultando em padrões como:
```latex
\DIFadd{...in Table} ~\protect\ref{tab:label}\DIFadd{. As noted in Section} ~\protect\ref{sec:label}\DIFadd{, ...}
```
onde os `\ref{}` ficam **entre** blocos `\DIFadd{}`, não dentro deles.

### Fix (fallback — se o erro ocorrer mesmo assim)

**Passo 1:** Verificar se `\soulregister\ref{1}` está no preamble de `_review_clean.tex`. Se não estiver, adicioná-lo manualmente antes de `\begin{document}`.

**Passo 2:** Se o erro persistir, quebrar o `\DIFadd{}` ao redor de cada `\ref{}` problemático:

```latex
% Antes (quebrado — \ref dentro de \DIFadd):
\DIFadd{texto antes~\ref{label}. Texto após.}

% Depois (corrigido — \ref fora do \DIFadd):
\DIFadd{texto antes~}\DIFaddend \ref{label}\DIFaddbegin \DIFadd{ texto após.}
```

> ⚠️ Se não há texto adicionado após o `\ref`, basta fechar o bloco sem reabrir:
> ```latex
> \DIFadd{texto antes~}\DIFaddend \ref{label}.
> ```

### Problema visual (não causa erro de compilação)

Mesmo com `\soulregister\ref{1}`, o token `\protect` antes de `\ref` pode interromper visualmente o highlight amarelo no PDF — o número da seção/tabela aparece sem fundo amarelo no meio de texto destacado.

**Fix**: mover `\protect\ref{label}` para **fora** do argumento `\DIFadd{}`:

```latex
% Antes (highlight interrompido):
\DIFadd{...described in Section~\protect\ref{sec:results}). A stratified...}

% Depois (highlight contínuo):
\DIFadd{...described in Section~}\protect\ref{sec:results}\DIFadd{). A stratified...}
```

> Aplicar em todos os `\protect\ref{}` dentro de `\DIFadd{}`. O número da referência ficará sem amarelo, mas o texto ao redor permanece destacado continuamente.

---

## Error 13: `\textcolor{color}{}` dentro de `\DIFadd{}` — xcolor Quebra com soul

### Symptoms
```
! Package xcolor Error: Undefined color `{red}'.
! Argument of \textcolor has an extra }.
! Paragraph ended before \textcolor was complete.
! Package soul Error: Reconstruction failed.
```

### Cause
`\textcolor{red}{content}` dentro de `\DIFadd{}` expande para `\textcolor{red}{content}` dentro de `\hl{}` (soul). O soul tenta tokenizar `\textcolor` mas confunde a chave `{red}` como argumento inválido — a cor entre chaves simples é interpretada como `{red}` (com chaves), não como `red`.

Ocorre tipicamente em marcadores TODO coloridos que foram adicionados no texto novo:
```latex
\DIFadd{\textcolor{red}{\textbf{[TODO: text]}}}
```

### Fix
Remover o wrapper `\textcolor{}{}`, mantendo apenas o conteúdo interno:

```latex
% Antes (quebrado):
\DIFadd{\textcolor{red}{\textbf{[TODO: text]}}}

% Depois (corrigido):
\DIFadd{\textbf{[TODO: text]}}
```

> Se o `\textcolor` for essencial para o output final, mova-o para fora do `\DIFadd{}`:
> ```latex
> \textcolor{red}{\DIFadd{\textbf{[TODO: text]}}}
> ```
> Atenção: `\textcolor{}{}` não é soulregistered por padrão — se houver outros itens dentro do `\hl{}`, pode falhar. Prefira remover o `\textcolor` em blocos `\DIFadd{}`.

---

## Error 14: `\textbf{\DIFadd{...}}` — soul não suporta `\hl{}` dentro de argumento

### Symptoms
```
! Argument of \DIFadd has an extra }.
! Paragraph ended before \DIFadd was complete.
```
O log aponta para linhas com `}}` no final, como:
```
l.729 \noindent\textbf{\DIFadd{Dataset.}}
l.735 ...textbf{\DIFadd{800 real training images}}
```

### Cause
`\textbf{\DIFadd{text}}` faz com que `\DIFadd` (que expande para `\hl{}`) seja chamado **dentro** do argumento de `\textbf{}`. O soul não pode operar dentro de um grupo aberto por outro comando — ele precisa estar no nível de texto horizontal.

Diferente do Error 7 (que remove o marker), aqui o marker deve ser **preservado** para manter o highlight.

### Fix
Inverter a ordem — mover `\textbf{}` para dentro de `\DIFadd{}`:

```latex
% Antes (quebrado):
\textbf{\DIFadd{Dataset.}}
\noindent\textbf{\DIFadd{Segmentation model.}}

% Depois (corrigido — highlight preservado):
\DIFadd{\textbf{Dataset.}}
\noindent\DIFadd{\textbf{Segmentation model.}}
```

### Fix (PowerShell — casos simples, sem braces aninhadas)
```powershell
$c = Get-Content -Raw "_review_clean.tex"
# \textbf{\DIFadd{TEXT}} → \DIFadd{\textbf{TEXT}}
$c = $c -replace '\\textbf\{\\DIFadd\{([^{}]+)\}\}', '\DIFadd{\textbf{$1}}'
# \noindent\textbf{\DIFadd{TEXT}} → \noindent\DIFadd{\textbf{TEXT}}
$c = $c -replace '\\noindent\\textbf\{\\DIFadd\{([^{}]+)\}\}', '\noindent\DIFadd{\textbf{$1}}'
$c | Set-Content "_review_clean.tex" -Encoding UTF8
```

> Para casos com múltiplos `\DIFadd{}` dentro do `\textbf{}` (ex: `\textbf{\DIFadd{A }\emph{\DIFadd{et al.}}\DIFadd{...}}`), substituir manualmente: remover os `\DIFadd{}` internos e deixar apenas o conteúdo sem highlight, ou reestruturar o bloco inteiro.
