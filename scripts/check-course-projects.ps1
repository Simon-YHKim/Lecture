<#
.SYNOPSIS
    AutoCAD Technician 과정 8차시를 검사한다.

.DESCRIPTION
    이전 버전은 차시별 길이를 상수로 적어 두고 대조했다. 그 방식은 컴포지션이
    저지르던 실수와 같다 — 같은 숫자를 두 곳에 적으면 어긋나고, 원본이 아닌
    쪽이 조용히 이긴다.

    지금은 SCRIPT.md 가 길이의 원본이고, 검사는 빌드 결과가 그 원본과 맞는지를
    본다. 판정 로직은 타이밍 계산기(beats.py)와 같은 자리에 둔다.

    -RunHyperFramesChecks 를 주면 차시마다 `npm run check` 도 함께 돌린다.
#>
[CmdletBinding()]
param(
    [switch]$RunHyperFramesChecks,
    [string]$PythonPath = $env:LECTURE_PYTHON
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()

$python = $PythonPath
if (-not $python) {
    $python = Join-Path $repoRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) { $python = 'python' }
}
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    throw "Python 실행 파일을 찾을 수 없습니다: $python"
}

$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
& $python (Join-Path $repoRoot 'scripts\part\verify_course.py')
$code = $LASTEXITCODE

# 규격이 한 값인가, 두 판이 같은 것을 가르치는가. 둘 다 사람이 세어서 찾았던
# 결함이라 세는 일을 검사기로 옮겼다 — TWO_EDITIONS.md 6절.
foreach ($extra in @('scripts\check-standards.py', 'scripts\check-editions.py')) {
    Write-Host ''
    & $python (Join-Path $repoRoot $extra)
    if ($LASTEXITCODE -ne 0) { $code = $LASTEXITCODE }
}

if ($RunHyperFramesChecks -and $code -eq 0) {
    $courseRoot = Join-Path $repoRoot 'projects\autocad-technician'
    foreach ($dir in Get-ChildItem -LiteralPath $courseRoot -Directory -Filter 'lesson-*') {
        if (-not (Test-Path -LiteralPath (Join-Path $dir.FullName 'package.json'))) { continue }
        Write-Host ''
        Write-Host "== $($dir.Name) =="
        Push-Location $dir.FullName
        try {
            & npm run check
            if ($LASTEXITCODE -ne 0) { $code = $LASTEXITCODE }
        } finally {
            Pop-Location
        }
    }
}

exit $code
