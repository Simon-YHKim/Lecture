[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()
$checker = Join-Path $repoRoot 'scripts/check-private-materials.ps1'
$temporaryIndex = [IO.Path]::GetTempFileName()
$shell = if (Get-Command pwsh -ErrorAction SilentlyContinue) { 'pwsh' } else { 'powershell.exe' }

Remove-Item -LiteralPath $temporaryIndex
$previousIndex = $env:GIT_INDEX_FILE
$env:GIT_INDEX_FILE = $temporaryIndex

try {
    & git read-tree HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Unable to initialize the temporary Git index.' }

    $fixtureBlob = ('fixture' | & git hash-object -w --stdin).Trim()

    function Set-TestPath([string]$Path) {
        & git read-tree HEAD
        & git update-index --add --cacheinfo "100644,$fixtureBlob,$Path"
        if ($LASTEXITCODE -ne 0) { throw "Unable to stage test path: $Path" }
    }

    function Assert-Blocked([string]$Path) {
        Set-TestPath $Path
        & $shell -NoProfile -File $checker -Mode staged *> $null
        if ($LASTEXITCODE -eq 0) { throw "Expected guard to block: $Path" }
    }

    function Assert-Allowed([string]$Path) {
        Set-TestPath $Path
        & $shell -NoProfile -File $checker -Mode staged *> $null
        if ($LASTEXITCODE -ne 0) { throw "Expected guard to allow: $Path" }
    }

    Assert-Blocked 'materials/source.PPTX'
    Assert-Blocked '자료/강사용 원본.PPTX'
    Assert-Blocked 'private/notes.txt'
    Assert-Blocked 'exports/course.pdf'
    Assert-Blocked 'assets/drawing.dwg'
    Assert-Blocked 'archives/materials.zip'
    Assert-Allowed 'docs/public-course-outline.md'

    Write-Output 'Private materials guard tests passed.'
} finally {
    $env:GIT_INDEX_FILE = $previousIndex
    Remove-Item -LiteralPath $temporaryIndex -ErrorAction SilentlyContinue
}
