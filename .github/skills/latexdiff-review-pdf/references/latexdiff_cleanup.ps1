param(
    [string]$InputFile  = "latex_build\review_raw.tex",
    [string]$OutputFile = "_review_clean.tex"
)

$root = "D:\0Code\_phdSeismic\IEEE_Access"
$inPath  = Join-Path $root $InputFile
$outPath = Join-Path $root $OutputFile

if (-not (Test-Path $inPath)) { Write-Error "Not found: $inPath"; exit 1 }

$raw = [System.IO.File]::ReadAllText($inPath, [System.Text.Encoding]::UTF8)
Write-Host "Read: $inPath ($($raw.Length) chars)"
Write-Host "DIFdelbegin: $(([regex]::Matches($raw, '\\DIFdelbegin')).Count)"
Write-Host "DIFaddbegin: $(([regex]::Matches($raw, '\\DIFaddbegin')).Count)"

# STEP 1: Remove entire \DIFdelbegin ... \DIFdelend blocks (deleted content)
# IMPORTANT: Use (?m) to match \DIFdelbegin only at start-of-line (not inside \providecommand args)
$opts = [System.Text.RegularExpressions.RegexOptions]::Singleline -bor [System.Text.RegularExpressions.RegexOptions]::Multiline
for ($i = 0; $i -lt 30; $i++) {
    $prev = $raw
    $raw = [regex]::Replace($raw, '(?m)^\\DIFdelbegin[\s\S]*?\\DIFdelend[ \t]*$', '', $opts)
    if ($raw -eq $prev) { break }
}
Write-Host "After DEL blocks removed - DIFdelbegin left: $(([regex]::Matches($raw, '(?m)^\\DIFdelbegin', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count)"

# STEP 2: Unwrap \DIFaddbegin ... \DIFaddend (keep content, remove markers only)
# Only when at start of line
$raw = [regex]::Replace($raw, '(?m)^\\DIFaddbegin[ \t]*$[\r\n]*', '', [System.Text.RegularExpressions.RegexOptions]::Multiline)
$raw = [regex]::Replace($raw, '(?m)^\\DIFaddend[ \t]*$[\r\n]*',  '', [System.Text.RegularExpressions.RegexOptions]::Multiline)

# STEP 3: Unwrap \DIFadd{content} -> content
for ($i = 0; $i -lt 20; $i++) {
    $prev = $raw
    $raw = [regex]::Replace($raw, '\\DIFadd\{([^{}]*)\}', '$1')
    if ($raw -eq $prev) { break }
}

# STEP 4: Clean latexdiff preamble residues
# Use literal string replacement for the empty \providecommand{}{}
# (these appear as multiple on same line separated by spaces in the latexdiff preamble)
while ($raw.Contains('\providecommand{}')) {
    $raw = $raw.Replace('\providecommand{}{}', '')
    $raw = $raw.Replace('\providecommand{}', '')
}
$raw = $raw.Replace('\lstset{extendedchars=\true', '\lstset{extendedchars=true')
$raw = [regex]::Replace($raw, '%DIFDELCMD[^\r\n]*', '')
$raw = [regex]::Replace($raw, '%DIFAUXCMD[^\r\n]*', '')
$raw = [regex]::Replace($raw, '%DIF [^\r\n]*', '')

# STEP 5: Clean remaining FL markers (table cells)
foreach ($cmd in @('DIFaddbeginFL','DIFaddendFL','DIFdelbeginFL','DIFdelendFL','DIFmodbegin','DIFmodend')) {
    $raw = $raw.Replace("\$cmd", '')
}
for ($i = 0; $i -lt 10; $i++) {
    $prev = $raw
    $raw = [regex]::Replace($raw, '\\DIFaddFL\{([^{}]*)\}', '$1')
    $raw = [regex]::Replace($raw, '\\DIFdelFL\{[^{}]*\}', '')
    if ($raw -eq $prev) { break }
}

# STEP 6: Remove empty commands (residues from deleted content)
foreach ($cmd in @('textbf','emph','textit','textrm','texttt','text','paragraph','subsubsection','subsection','caption')) {
    for ($i = 0; $i -lt 5; $i++) {
        $prev = $raw
        $raw = [regex]::Replace($raw, "\\\\$cmd\{\s*\}", '')
        if ($raw -eq $prev) { break }
    }
}

# REPORT
Write-Host "textbf empty left:   $(([regex]::Matches($raw, '\\textbf\{\s*\}')).Count)"
Write-Host "DIFdelbegin left:    $(([regex]::Matches($raw, '\\DIFdelbegin')).Count)"
Write-Host "Lines: $(($raw -split '\n').Count)"

[System.IO.File]::WriteAllText($outPath, $raw, [System.Text.Encoding]::UTF8)
Write-Host "Done: $outPath"
