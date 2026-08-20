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
    [switch]$RunHyperFramesChecks
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()

$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { $python = 'python' }

$env:PYTHONIOENCODING = 'utf-8'
& $python (Join-Path $repoRoot 'scripts\part\verify_course.py')
$code = $LASTEXITCODE

if ($RunHyperFramesChecks -and $code -eq 0) {
    $courseRoot = Join-Path $repoRoot 'projects\autocad-technician'
    foreach ($dir in Get-ChildItem -LiteralPath $courseRoot -Directory -Filter 'lesson-*') {
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
