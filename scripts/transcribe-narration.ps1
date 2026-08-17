[CmdletBinding()]
param(
    # Path to the narration recording. Keep recordings in the approved private
    # storage location; do not copy one into this repository to run the script.
    [Parameter(Mandatory)][string]$AudioPath,

    # Where to write the word-level transcript. Defaults to a sibling of the
    # recording, which keeps the transcript outside the public working tree.
    [string]$TranscriptPath,

    [string]$Model = 'large-v3',
    [string]$Device = 'cuda',
    [string]$ComputeType = 'float16',
    [string]$Language = 'ko',
    [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()

if (-not (Test-Path -LiteralPath $AudioPath -PathType Leaf)) {
    throw "Narration recording not found: $AudioPath"
}

if ([string]::IsNullOrWhiteSpace($TranscriptPath)) {
    $TranscriptPath = [IO.Path]::ChangeExtension((Resolve-Path -LiteralPath $AudioPath).Path, '.transcript.json')
}

# The transcript carries the spoken text of a private recording. Refuse to write
# it inside the repository even though .gitignore and the guard would also catch
# it, so the mistake is reported before any bytes are produced.
$transcriptFull = [IO.Path]::GetFullPath($TranscriptPath)
$repoFull = [IO.Path]::GetFullPath($repoRoot)
if ($transcriptFull.StartsWith($repoFull, [StringComparison]::OrdinalIgnoreCase)) {
    throw @"
Refusing to write a transcript inside the repository.

  requested: $TranscriptPath

Transcripts are derived from private narration recordings and must stay in the
approved private storage location. Publish only the numbers-only derivative that
build-narration-timing.ps1 produces.
"@
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

$transcriber = Join-Path $repoRoot 'scripts/narration/transcribe.py'
& $PythonPath $transcriber $AudioPath $TranscriptPath `
    --model $Model --device $Device --compute-type $ComputeType --language $Language
if ($LASTEXITCODE -ne 0) {
    throw "Transcription failed with exit code $LASTEXITCODE."
}
