[CmdletBinding()]
param(
    # Lesson project directory, for example
    # projects/autocad-technician/lesson-01-drawing-language
    [Parameter(Mandatory)][string]$LessonPath,

    # Word-level transcript produced by transcribe-narration.ps1. It lives in the
    # approved private storage location and is read, never copied.
    [Parameter(Mandatory)][string]$TranscriptPath,

    # Where to write the publishable timing file. Defaults to the lesson project.
    [string]$OutputPath,

    # Fail when the aligned character ratio falls below this value, which means
    # the recording and SCRIPT.md have diverged rather than merely drifted.
    [double]$MinimumRatio = 0.7,

    [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()

if (-not (Test-Path -LiteralPath $LessonPath -PathType Container)) {
    throw "Lesson project not found: $LessonPath"
}
if (-not (Test-Path -LiteralPath (Join-Path $LessonPath 'SCRIPT.md') -PathType Leaf)) {
    throw "Lesson project has no SCRIPT.md: $LessonPath"
}
if (-not (Test-Path -LiteralPath $TranscriptPath -PathType Leaf)) {
    throw "Transcript not found: $TranscriptPath"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $LessonPath 'narration-timing.json'
}

if ([string]::IsNullOrWhiteSpace($PythonPath)) {
    $PythonPath = Join-Path $repoRoot '.venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
        $PythonPath = Join-Path $repoRoot '.venv/bin/python'
    }
}
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw @"
Python environment not found: $PythonPath

Create it once from the repository root:

  py -3.12 -m venv .venv
  ./.venv/Scripts/python.exe -m pip install faster-whisper
"@
}

$aligner = Join-Path $repoRoot 'scripts/narration/align.py'
& $PythonPath $aligner $LessonPath $TranscriptPath $OutputPath --min-ratio $MinimumRatio
if ($LASTEXITCODE -ne 0) {
    throw "Narration alignment failed with exit code $LASTEXITCODE."
}

# The published file must never carry spoken text. Verify rather than trust.
$timing = Get-Content -LiteralPath $OutputPath -Raw -Encoding UTF8 | ConvertFrom-Json
$allowedFrameKeys = @(
    'frame', 'id', 'start', 'end', 'duration', 'plannedDuration',
    'driftSeconds', 'matchedChars', 'scriptChars', 'matchedRatio'
)
foreach ($frame in @($timing.frames)) {
    $unexpected = @($frame.PSObject.Properties.Name | Where-Object { $allowedFrameKeys -notcontains $_ })
    if ($unexpected.Count -gt 0) {
        throw "Timing output carries unexpected frame fields: $($unexpected -join ', ')"
    }
}
if ((Get-Content -LiteralPath $OutputPath -Raw -Encoding UTF8) -match '[가-힣]') {
    throw 'Timing output contains Hangul text. It must carry numbers and identifiers only.'
}

Write-Output "Narration timing written for $($timing.frames.Count) frames."
