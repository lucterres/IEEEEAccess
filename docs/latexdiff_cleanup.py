"""
latexdiff_cleanup.py  (rewritten 2026-07-13)
--------------------------------------------
Cleans a latexdiff-generated .tex for pdflatex compilation.

Strategy:
  - Remove WHOLE \DIFdelbegin...\DIFdelend blocks.
    These blocks always start with \DIFdelbegin on its own line.
  - Strip \DIFaddbegin / \DIFaddend markers (keep their content).
  - Unwrap \DIFadd{text} -> text , remove \DIFdel{...}.
  - Fix known preamble issues (\providecommand{}{}, \lstset extendedchars).
  - Remove auxiliary comment lines (%DIFDELCMD, %DIFAUXCMD, %DIF ...).

Usage:
    python docs/latexdiff_cleanup.py latex_build/review_raw.tex latex_build/review_clean.tex
"""

import re
import sys


def remove_delbegin_blocks(text: str) -> str:
    """Remove complete \\DIFdelbegin ... \\DIFdelend blocks.
    These blocks start with a line that IS exactly '\\DIFdelbegin' (possibly
    with trailing spaces) and end with a line that contains '\\DIFdelend'.
    We iterate because blocks can be nested or adjacent.
    """
    # Pattern: from a line starting with \DIFdelbegin up to and including
    # the line ending with \DIFdelend (non-greedy, multiline).
    pattern = re.compile(
        r'^\\DIFdelbegin.*?\\DIFdelend[^\n]*\n?',
        re.DOTALL | re.MULTILINE
    )
    for _ in range(30):
        new = pattern.sub('', text)
        if new == text:
            break
        text = new
    return text

def cleanup(text: str) -> str:
    # 1. Remove entire DEL blocks (start-of-line markers)
    text = remove_delbegin_blocks(text)

    # 1b. Remove inline \DIFdelbegin...\DIFdelend (not at start of line, e.g. mid-paragraph)
    #     These have the form: ...old text \DIFdelend new text...
    #     We need to: remove the \DIFdelbegin...content...\DIFdelend span
    #     and keep the \DIFaddbegin...content...\DIFaddend span
    opts_sl = re.DOTALL
    for _ in range(30):
        prev = text
        text = re.sub(r'\\DIFdelbegin.*?\\DIFdelend', '', text, flags=opts_sl)
        if text == prev:
            break

    # 1c. Strip remaining standalone DIF markers (any \DIFxxx not followed by {)
    #     e.g. \DIFdelend, \DIFaddbegin, \DIFaddend left over inline
    text = re.sub(r'\\DIF(?:delbegin|delend|addbegin|addend|delbeginFL|delendFL|addbeginFL|addendFL|modbegin|modend)\b\s*', '', text)

    # 1d. No generic } removal -- too dangerous (can corrupt \usepackage{} etc.)

    # 2. Remove DIFaddbegin / DIFaddend markers (lines that ARE the marker)
    text = re.sub(r'^\\DIFaddbegin[^\n]*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\\DIFaddend[^\n]*\n?',  '', text, flags=re.MULTILINE)

    # 3. Unwrap \DIFadd{content} -> content  (iterative for nested, with DOTALL for multiline)
    #    First pass: simple [^{}]* (fast, handles flat content)
    for _ in range(20):
        new = re.sub(r'\\DIFadd\{([^{}]*)\}', r'\1', text)
        if new == text:
            break
        text = new
    # Second pass: allow one level of nested {} (e.g. \DIFadd{\textcolor{red}{...}})
    for _ in range(20):
        new = re.sub(r'\\DIFadd\{((?:[^{}]|\{[^{}]*\})*)\}', r'\1', text, flags=re.DOTALL)
        if new == text:
            break
        text = new
    # Third pass: two levels of nesting
    for _ in range(20):
        new = re.sub(r'\\DIFadd\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', r'\1', text, flags=re.DOTALL)
        if new == text:
            break
        text = new

    # 4. Remove remaining \DIFdel{...} (should already be gone with blocks, belt-and-suspenders)
    for _ in range(20):
        new = re.sub(r'\\DIFdel\{[^{}]*\}', '', text)
        if new == text:
            break
        text = new

    # 5. Fix preamble: remove \providecommand{}{} (empty first arg)
    #    Use explicit chr(92) to avoid Python raw-string / regex escape confusion
    BS = chr(92)
    while (BS + 'providecommand{}') in text:
        text = text.replace(BS + 'providecommand{}{}', '')
        text = text.replace(BS + 'providecommand{}', '')

    # 6. Fix \lstset{extendedchars=\true} -> extendedchars=true
    text = text.replace(r'\lstset{extendedchars=\true', r'\lstset{extendedchars=true')

    # 7. Remove auxiliary comment lines
    text = re.sub(r'%DIFDELCMD[^\n]*\n?', '', text)
    text = re.sub(r'%DIFAUXCMD[^\n]*\n?', '', text)
    text = re.sub(r'%DIF [^\n]*\n?', '', text)

    # 8. Remove remaining FL markers (table residues)
    # Remove entire \providecommand lines for FL commands (not just the command name)
    for cmd in ('DIFaddbeginFL','DIFaddendFL','DIFdelbeginFL','DIFdelendFL',
                'DIFmodbegin','DIFmodend','DIFaddFL','DIFdelFL'):
        text = re.sub(r'[^\n]*\\providecommand\{\\' + cmd + r'\}[^\n]*\n?', '', text)
    # Also remove standalone \DIFxxxFL in body (not in \providecommand lines)
    for cmd in ('DIFaddbeginFL','DIFaddendFL','DIFdelbeginFL','DIFdelendFL',
                'DIFmodbegin','DIFmodend'):
        text = text.replace('\\' + cmd, '')
    for _ in range(10):
        prev = text
        text = re.sub(r'\\DIFaddFL\{([^{}]*)\}', r'\1', text)
        text = re.sub(r'\\DIFdelFL\{[^{}]*\}', '', text)
        if text == prev:
            break

    # 8b. Second pass: remove \providecommand{}{} that may have been created
    #     by removing content from \providecommand{\DIFmodbegin}{} etc.
    BS = chr(92)
    while (BS + 'providecommand{}') in text:
        text = text.replace(BS + 'providecommand{}{}', '')
        text = text.replace(BS + 'providecommand{}', '')

    # 8c. Remove orphan \end{comment} blocks left when \begin{comment}
    #     was inside a removed DIFdelbegin block
    begin_count = text.count(r'\begin{comment}')
    end_count   = text.count(r'\end{comment}')
    if end_count > begin_count:
        # Remove excess \end{comment} occurrences from the end
        for _ in range(end_count - begin_count):
            idx = text.rfind(r'\end{comment}')
            if idx >= 0:
                # Remove the line containing \end{comment}
                line_start = text.rfind('\n', 0, idx)
                line_end   = text.find('\n', idx)
                if line_end == -1:
                    line_end = len(text)
                text = text[:line_start+1] + text[line_end+1:]

    # 8d. Surgical fix for the specific stray } left before new content
    #     Pattern: "...painting the salt bodies }images is being redesigned..."
    #     The "...painting the salt bodies" text belongs to the old version inside
    #     a DIFdelbegin block that was improperly truncated.
    #     We detect: a line where text from _v6 (old subsection intro) merges with _v7 text
    #     Strategy: remove from "Our goal is to evaluate..." up to the } before the new text
    old_intro = 'Our goal is to evaluate the synthesized samples quality'
    if old_intro in text:
        # Find the line and remove everything up to and including the stray }
        idx = text.find(old_intro)
        # Find the } that is followed by the new text
        end_stray = text.find('}', idx)
        if end_stray != -1:
            text = text[:idx] + text[end_stray+1:]

    # 8e. Fix \begin{enumerate} that lost its \end{enumerate}
    #     Count and add missing \end{enumerate}
    begin_enum = text.count(r'\begin{enumerate}')
    end_enum   = text.count(r'\end{enumerate}')
    if begin_enum > end_enum:
        # Insert \end{enumerate} before \bigskip that follows the last \item
        bs = chr(92)
        marker = bs + 'bigskip'
        # Find the first \bigskip after the last \begin{enumerate}
        last_enum_idx = text.rfind(bs + 'begin{enumerate}')
        bigskip_idx = text.find(marker, last_enum_idx)
        if bigskip_idx != -1:
            text = text[:bigskip_idx] + bs + 'end{enumerate}\n' + text[bigskip_idx:]

    return text


def main():
    if len(sys.argv) != 3:
        print("Usage: python latexdiff_cleanup.py <input.tex> <output.tex>")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    with open(infile, encoding='utf-8-sig') as f:   # utf-8-sig strips BOM
        text = f.read()

    result = cleanup(text)

    # Count diagnostics
    delbegin = len(re.findall(r'^\\DIFdelbegin', result, re.MULTILINE))
    textbf_empty = len(re.findall(r'\\textbf\{\s*\}', result))
    prov_empty = len(re.findall(r'\\providecommand\{\}', result))

    print(f"DIFdelbegin left (start-of-line): {delbegin}")
    print(f"textbf{{}} empty left:  {textbf_empty}")
    print(f"providecommand{{}} empty: {prov_empty}")
    print(f"Lines: {result.count(chr(10))}")

    with open(outfile, 'w', encoding='utf-8') as f:   # write WITHOUT BOM
        f.write(result)
    print(f"Saved: {outfile}")


if __name__ == '__main__':
    main()
