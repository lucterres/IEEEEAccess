r"""
latexdiff_cleanup.py  (rewritten 2026-07-16 v3 — add step 8g: stray } after \cite)
------------------------------------------------------------------------
Cleans a latexdiff-generated .tex for pdflatex compilation,
KEEPING the visual diff markers (\DIFdel, \DIFadd, etc.) so the
output PDF shows:
  - YELLOW HIGHLIGHT for insertions (\DIFadd)
  - STRIKETHROUGH (no color) for deletions (\DIFdel)

This matches the IEEE Access "Highlighted PDF" requirement:
  "updated manuscript with yellow highlighting indicating changes"

What this script PRESERVES (necessary for colored PDF):
  \DIFdelbegin ... \DIFdelend   — wraps deleted content
  \DIFaddbegin ... \DIFaddend   — wraps added content
  \DIFdel{...}                  — deleted text (rendered with red strikethrough)
  \DIFadd{...}                  — added text (rendered with blue underline)

What this script REMOVES (causes LaTeX compilation errors):
  %DIFDELCMD < ...              — commented-out old commands (not needed)
  %DIFAUXCMD ...                — auxiliary diff comments
  %DIF > / %DIF < ...           — diff margin annotations
  \DIFaddFL{} / \DIFdelFL{}     — table floating-line markers (break tabular)
  \DIFaddbeginFL / \DIFaddendFL — table environment markers
  \DIFdelbeginFL / \DIFdelendFL — table environment markers
  \providecommand{}{}           — empty providecommands left after FL removal
  \begin{enumerate} without \end{enumerate} mismatch (fix only)

Usage:
    python .github/skills/latexdiff-review-pdf/references/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex
"""

import re
import sys


def cleanup(text: str) -> str:

    # 0. Remove \DIFdelbegin...\DIFdelend blocks that contain %DIFDELCMD lines.
    #    These are deleted tables/lists/structures — they cannot be rendered and
    #    leave broken \textbf{} shells after comment removal.
    #    Simple text-diff blocks (no %DIFDELCMD inside) are preserved so that
    #    \DIFdel{old text} still appears in the PDF with red strikethrough.
    def remove_structural_del_blocks(t: str) -> str:
        pattern = re.compile(
            r'\\DIFdelbegin\b(.*?)\\DIFdelend\b[^\n]*',
            re.DOTALL
        )
        def replace_if_structural(m):
            inner = m.group(1)
            if '%DIFDELCMD' in inner or '%DIFAUXCMD' in inner:
                return ''   # structural block — remove entirely
            return m.group(0)   # simple text block — keep as-is
        for _ in range(20):
            new = pattern.sub(replace_if_structural, t)
            if new == t:
                break
            t = new
        return t

    text = remove_structural_del_blocks(text)

    # 1. Remove auxiliary comment lines (these are safe to remove — they are
    #    just commented-out old LaTeX commands, not needed for rendering)
    text = re.sub(r'%DIFDELCMD[^\n]*\n?', '', text)
    text = re.sub(r'%DIFAUXCMD[^\n]*\n?', '', text)
    # %DIF > and %DIF < margin markers (but NOT lines with %DIF PREAMBLE — keep those)
    text = re.sub(r'%DIF [<>][^\n]*\n?', '', text)

    # 2. Remove FL table markers (these break tabular/array environments).
    #    \DIFaddFL{content} -> content  (keep the text, remove the wrapper)
    #    \DIFdelFL{content} -> ''       (remove deleted table cell content)
    for _ in range(20):
        prev = text
        text = re.sub(r'\\DIFaddFL\{([^{}]*)\}', r'\1', text)
        text = re.sub(r'\\DIFdelFL\{[^{}]*\}', '', text)
        if text == prev:
            break
    # Also handle one level of nested braces in FL markers
    for _ in range(20):
        prev = text
        text = re.sub(r'\\DIFaddFL\{((?:[^{}]|\{[^{}]*\})*)\}', r'\1', text)
        text = re.sub(r'\\DIFdelFL\{(?:[^{}]|\{[^{}]*\})*\}', '', text)
        if text == prev:
            break

    # 3. Remove standalone FL environment markers ONLY in document body
    #    (NOT in preamble lines tagged with %DIF PREAMBLE)
    #    These appear in table bodies and break compilation.
    #    We process line-by-line to avoid touching preamble.
    body_lines = []
    fl_cmds = ('DIFaddbeginFL', 'DIFaddendFL', 'DIFdelbeginFL', 'DIFdelendFL',
               'DIFmodbegin', 'DIFmodend')
    for line in text.split('\n'):
        if '%DIF PREAMBLE' not in line:
            for cmd in fl_cmds:
                line = line.replace('\\' + cmd, '')
        body_lines.append(line)
    text = '\n'.join(body_lines)

    # 4. Fix \providecommand{}{} left after FL marker removal
    BS = chr(92)
    for _ in range(10):
        prev = text
        text = text.replace(BS + 'providecommand{}{}', '')
        text = text.replace(BS + 'providecommand{}', '')
        if text == prev:
            break

    # 5. Fix \lstset{extendedchars=\true} -> extendedchars=true
    text = text.replace(r'\lstset{extendedchars=\true', r'\lstset{extendedchars=true')

    # 6. Fix unbalanced \begin{enumerate} / \end{enumerate}
    begin_enum = text.count(r'\begin{enumerate}')
    end_enum   = text.count(r'\end{enumerate}')
    if begin_enum > end_enum:
        bs = chr(92)
        marker = bs + 'bigskip'
        last_enum_idx = text.rfind(bs + 'begin{enumerate}')
        bigskip_idx = text.find(marker, last_enum_idx)
        if bigskip_idx != -1:
            text = text[:bigskip_idx] + bs + 'end{enumerate}\n' + text[bigskip_idx:]

    # 7. Fix orphan \end{comment} (when \begin{comment} was inside a deleted block)
    begin_count = text.count(r'\begin{comment}')
    end_count   = text.count(r'\end{comment}')
    if end_count > begin_count:
        for _ in range(end_count - begin_count):
            idx = text.rfind(r'\end{comment}')
            if idx >= 0:
                line_start = text.rfind('\n', 0, idx)
                line_end   = text.find('\n', idx)
                if line_end == -1:
                    line_end = len(text)
                text = text[:line_start+1] + text[line_end+1:]

    # 8b. Remove \hskip0pt and \hskip\z@skip injected by latexdiff after \mbox{\cite{}}
    #     These cause "Missing number, treated as zero" when inside soul's \hl{} argument.
    #     They are pure latexdiff artefacts — safe to remove entirely.
    text = re.sub(r'\\hskip0pt\b', '', text)
    text = re.sub(r'\\hskip\\z@skip\b', '', text)

    # 8c. Unwrap \mbox{\cite{KEY}} and \mbox{\cite{KEY} } (with optional space).
    #     Latexdiff wraps citations in \mbox{} to protect them inside diff arguments,
    #     but soul's \hl{} cannot process \mbox{\cite{}} — causes "Reconstruction failed".
    #     Safe to remove the \mbox{} wrapper; \cite{KEY} remains intact.
    #     (Error 10 in fix-errors.md)
    for _ in range(10):
        prev = text
        text = re.sub(r'\\mbox\{(\\cite\{[^}]+\})\s*\}', r'\1', text)
        if text == prev:
            break

    # 8d. Collapse stranded \cite{KEY} between \DIFaddend and \DIFaddbegin.
    #     After \mbox{} removal, patterns like \DIFadd{~}\cite{KEY}\DIFaddend\DIFaddbegin\DIFadd{
    #     may appear. Collapse them back into a continuous \DIFadd span.
    #     (Error 11 in fix-errors.md)
    for _ in range(10):
        prev = text
        text = re.sub(
            r'\\}\s*\\cite\{([^}]+)\}\\DIFaddend\s*\\DIFaddbegin\s*\\DIFadd\{',
            r'\\cite{\1} ',
            text
        )
        if text == prev:
            break

    # 8e. Add \protect before bare \ref{} inside \DIFadd{} blocks.
    #     soul's \hl{} tokeniser requires \ref to be \protect-ed.
    #     (Error 12 in fix-errors.md)
    # Process only inside \DIFadd{...} content
    def protect_ref_in_difadd(t: str) -> str:
        def fix_inner(m: re.Match) -> str:
            inner = m.group(1)
            # Replace \ref{ but not already-protected \protect\ref{
            inner = re.sub(r'(?<!\\protect)\\ref\{', r'\\protect\\ref{', inner)
            return r'\DIFadd{' + inner + '}'
        for _ in range(5):
            prev = t
            t = re.sub(
                r'\\DIFadd\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}',
                fix_inner, t
            )
            if t == prev:
                break
        return t

    text = protect_ref_in_difadd(text)

    # 8f. Report multi-paragraph \DIFadd{} blocks (cannot auto-fix — manual split needed).
    #     Warn if any \DIFadd{...} block spans a blank line (paragraph break).
    #     (Error 13 in fix-errors.md — must be fixed manually)
    multi_para = re.findall(r'\\DIFadd\{[^}]*\n\s*\n[^}]*\}', text)
    if multi_para:
        print(f"WARNING: {len(multi_para)} multi-paragraph \\DIFadd{{}} block(s) found — "
              "must be split manually (see Error 13 in fix-errors.md).")

    # 8g. Remove stray } immediately after \cite{KEY} that latexdiff injects when
    #     splitting a \DIFadd{} block at a citation boundary.
    #     Pattern: \cite{KEY} }<whitespace><lowercase-letter>  → \cite{KEY} <letter>
    #     (Error 15 in fix-errors.md)
    #     Also handles the variant: \cite{KEY} }\hskip0pt<text>
    #     (the \hskip0pt itself was already removed in step 8b, so the residual
    #     looks like  \cite{KEY} }<text>  where text starts with a lowercase letter
    #     or a space followed by lowercase — i.e. continuation of the sentence.)
    for _ in range(10):
        prev = text
        # Case A: } immediately after \cite{KEY} followed by continuation word
        text = re.sub(
            r'(\\cite\{[^}]+\})\s*\}(\s+[a-z])',
            r'\1\2',
            text
        )
        # Case B: } immediately after \cite{KEY} at end of line (no space before word)
        text = re.sub(
            r'(\\cite\{[^}]+\})\s*\}\n(\s*[a-z])',
            r'\1\n\2',
            text
        )
        if text == prev:
            break

    # 8. Inject yellow-highlight style for \DIFadd and strikethrough for \DIFdel.
    #    - \hl (soul) supports line-breaking, unlike \colorbox which overflows margins.
    #    - \soulregister registers commands that appear inside \DIFadd{} so soul
    #      can process them without crashing (textbf, textit, textcolor, cite, ref...).
    #    - Math mode fallback: soul/ulem don't work in math → use \textcolor instead.
    yellow_highlight_block = r"""
% ---- IEEE Access Highlighted PDF: yellow=added, strikethrough=deleted ----
% soul+xcolor: load xcolor BEFORE soul so \hl can use xcolor's color model.
% PassOptionsToPackage ensures xcolor replaces the 'color' pkg already loaded by ieeeaccess.cls.
\PassOptionsToPackage{dvipsnames,table}{xcolor}
\usepackage{xcolor}
\usepackage{soul}
\usepackage[normalem]{ulem}
\sethlcolor{yellow}
% Register commands that may appear inside \DIFadd{} blocks:
\soulregister\textbf{1}
\soulregister\textit{1}
\soulregister\emph{1}
\soulregister\texttt{1}
\soulregister\cite{1}
\soulregister\ref{1}
\soulregister\label{1}
% \DIFadd: yellow highlight in text mode, blue in math (soul fails in math)
\providecommand{\DIFadd}[1]{\ifmmode\textcolor{blue}{#1}\else\hl{#1}\fi}
\providecommand{\DIFdel}[1]{\ifmmode\textcolor{red}{#1}\else\sout{#1}\fi}
\renewcommand{\DIFadd}[1]{\ifmmode\textcolor{blue}{#1}\else\hl{#1}\fi}
\renewcommand{\DIFdel}[1]{\ifmmode\textcolor{red}{#1}\else\sout{#1}\fi}
% -------------------------------------------------------------------------
"""
    # Remove latexdiff's own \DIFadd / \DIFdel definitions so ours take precedence.
    for pat in [
        r'\\providecommand\{\\DIFadd\}\[1\]\{[^\n]+\}\n?',
        r'\\providecommand\{\\DIFdel\}\[1\]\{[^\n]+\}\n?',
        r'\\DeclareRobustCommand\{\\DIFadd\}\[1\]\{[^\n]+\}\n?',
        r'\\DeclareRobustCommand\{\\DIFdel\}\[1\]\{[^\n]+\}\n?',
    ]:
        text = re.sub(pat, '', text)

    # Insert our block just before \begin{document}
    begin_doc = r'\begin{document}'
    if begin_doc in text and yellow_highlight_block.strip() not in text:
        text = text.replace(begin_doc, yellow_highlight_block + begin_doc, 1)

    return text


def strip_textcolor_in_difadd(text: str) -> str:
    """Remove \\textcolor{color}{content} -> content inside \\DIFadd{} blocks.
    soul's \\hl cannot process \\textcolor inside its argument."""
    def fix_block(m: re.Match) -> str:
        inner = m.group(1)
        inner = re.sub(
            r'\\textcolor\{[^}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}',
            r'\1', inner
        )
        return r'\DIFadd{' + inner + '}'
    for _ in range(5):
        prev = text
        text = re.sub(
            r'\\DIFadd\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}',
            fix_block, text
        )
        if text == prev:
            break
    return text


def main():
    if len(sys.argv) != 3:
        print("Usage: python latexdiff_cleanup.py <input.tex> <output.tex>")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, encoding='utf-8-sig') as f:   # utf-8-sig strips BOM
        text = f.read()

    result = strip_textcolor_in_difadd(cleanup(text))

    # Diagnostics
    difadd  = len(re.findall(r'\\DIFadd\{', result))
    difdel  = len(re.findall(r'\\DIFdel\{', result))
    prov_empty = len(re.findall(r'\\providecommand\{\}', result))
    fl_left = len(re.findall(r'\\DIFaddFL\{|\\DIFdelFL\{', result))

    print(f"\\DIFadd{{}} markers preserved: {difadd}")
    print(f"\\DIFdel{{}} markers preserved: {difdel}")
    print(f"FL markers left (should be 0): {fl_left}")
    print(f"providecommand{{}} empty left:  {prov_empty}")
    print(f"Lines: {result.count(chr(10))}")

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Saved: {outfile}")


if __name__ == '__main__':
    main()
