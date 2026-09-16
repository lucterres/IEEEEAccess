"""
Comprehensive post-processing script for _review_clean.tex
Applies all known fixes for latexdiff issues.
"""
import re

with open('_review_clean.tex', 'r', encoding='utf-8') as f:
    c = f.read()

print(f'Original lines: {c.count(chr(10))}')

# === FIX 1: Convert DIFaddFL -> DIFadd in document body ===
doc_start = c.find(r'\begin{document}')
preamble = c[:doc_start]
body = c[doc_start:]
body = re.sub(r'\\DIFaddFL\{', r'\\DIFadd{', body)
c = preamble + body
print('Fix 1 (DIFaddFL->DIFadd in body): done')

# === FIX 2: Unwrap \mbox{%DIFAUXCMD\n\cite{KEY} }\hskip0pt%DIFAUXCMD -> \cite{KEY} ===
mbox_pattern = r'\\mbox\{%DIFAUXCMD\s*\n(\\cite\{[^}]+\})\s*\}\\hskip0pt%DIFAUXCMD\n?'
count2 = len(re.findall(mbox_pattern, c))
c = re.sub(mbox_pattern, r'\1', c)
print(f'Fix 2a (unwrap mbox cite with space): {count2} instances')

mbox_pattern2 = r'\\mbox\{%DIFAUXCMD\s*\n(\\cite\{[^}]+\})\}\\hskip0pt%DIFAUXCMD\n?'
count2b = len(re.findall(mbox_pattern2, c))
c = re.sub(mbox_pattern2, r'\1', c)
print(f'Fix 2b (unwrap mbox cite without space): {count2b} instances')

# === FIX 3: Remove remaining \hskip0pt ===
count3 = c.count(r'\hskip0pt')
c = c.replace(r'\hskip0pt', '')
print(f'Fix 3 (remove hskip0pt): {count3} instances')

# === FIX 4: Fix textbf{DIFadd{TEXT}} -> DIFadd{\textbf{TEXT}} (simple) ===
count4 = len(re.findall(r'\\textbf\{\\DIFadd\{([^{}]+)\}\}', c))
c = re.sub(r'\\textbf\{\\DIFadd\{([^{}]+)\}\}', r'\\DIFadd{\\textbf{\1}}', c)
print(f'Fix 4 (textbf DIFadd flip, simple): {count4} instances')

# === FIX 5: Fix noindent\textbf{DIFadd{}} -> noindent\DIFadd{\textbf{}} ===
count5 = len(re.findall(r'\\noindent\\textbf\{\\DIFadd\{([^{}]+)\}\}', c))
c = re.sub(r'\\noindent\\textbf\{\\DIFadd\{([^{}]+)\}\}', r'\\noindent\\DIFadd{\\textbf{\1}}', c)
print(f'Fix 5 (noindent textbf DIFadd flip): {count5} instances')

# === FIX 6: Remove trailing newline before closing brace of DIFadd ===
count6 = len(re.findall(r'(\\DIFadd\{(?:[^{}]|\{[^{}]*\})*?)\n\}', c, re.DOTALL))
c = re.sub(r'(\\DIFadd\{(?:[^{}]|\{[^{}]*\})*?)\n\}', r'\1}', c, flags=re.DOTALL)
print(f'Fix 6 (remove trailing newline in DIFadd): {count6} instances')

# === FIX 7: Remove empty \DIFadd{} ===
count7 = c.count(r'\DIFadd{}')
c = c.replace(r'\DIFadd{}', '')
print(f'Fix 7 (remove empty DIFadd): {count7} instances')

print(f'Final lines: {c.count(chr(10))}')

with open('_review_clean.tex', 'w', encoding='utf-8') as f:
    f.write(c)
print('All fixes applied and saved.')
