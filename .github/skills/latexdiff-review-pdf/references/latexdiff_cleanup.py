"""
latexdiff_cleanup.py  (rewritten 2026-07-13 v2 — PRESERVE diff markers)
------------------------------------------------------------------------
Cleans a latexdiff-generated .tex for pdflatex compilation,
KEEPING the visual diff markers (\DIFdel, \DIFadd, etc.) so the
output PDF shows red strikethrough (deletions) and blue underline (additions).

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

    return text


def main():
    if len(sys.argv) != 3:
        print("Usage: python latexdiff_cleanup.py <input.tex> <output.tex>")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, encoding='utf-8-sig') as f:   # utf-8-sig strips BOM
        text = f.read()

    result = cleanup(text)

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
