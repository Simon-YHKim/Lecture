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

function Add-TestIndexEntry([string]$Blob, [string]$Path) {
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'git'
    $startInfo.Arguments = 'update-index --add -z --index-info'
    $startInfo.WorkingDirectory = $repoRoot
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardInput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    try {
        if (-not $process.Start()) { throw "Unable to start git update-index for: $Path" }
        $payload = [Text.UTF8Encoding]::new($false).GetBytes("100644 $Blob`t$Path" + [char]0)
        $process.StandardInput.BaseStream.Write($payload, 0, $payload.Length)
        $process.StandardInput.BaseStream.Flush()
        $process.StandardInput.Close()
        $errorText = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) { throw "Unable to stage test path: $Path`n$errorText" }
    } finally {
        $process.Dispose()
    }
}

try {
    & git read-tree HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Unable to initialize the temporary Git index.' }

    $fixtureBlob = ('fixture' | & git hash-object -w --stdin).Trim()
    $manifestPath = 'docs/autocad-technician/public-artifact-manifest.json'
    $manifestFile = Join-Path $repoRoot $manifestPath
    $productionManifest = Get-Content -LiteralPath $manifestFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $fixtureAssetPaths = @(
        'docs/autocad-technician/master-plan/AutoCAD_Technician_Video_Course_MasterPlan_260811.html',
        'docs/autocad-technician/reference/a3-landscape-template-reference.png',
        'projects/autocad-technician/lesson-01-drawing-language/snapshots/final-approval/frame-00-at-30s.png',
        'projects/autocad-technician/lesson-10-final-bracket/snapshots/final-approval/contact-sheet.jpg',
        'projects/autocad-technician/lesson-07-object-editing/snapshots/finding-01-text_occluded.png'
    )
    $fixtureAssets = @($productionManifest.assets | Where-Object { $fixtureAssetPaths -contains [string]$_.path })
    if ($fixtureAssets.Count -ne $fixtureAssetPaths.Count) {
        throw 'Unable to build the minimal approved artifact fixture manifest.'
    }
    $manifestObject = [PSCustomObject]@{
        schemaVersion = 1
        policy = [string]$productionManifest.policy
        assetCount = $fixtureAssets.Count
        assets = $fixtureAssets
    }
    $manifestJson = $manifestObject | ConvertTo-Json -Depth 8
    $manifestBlob = ($manifestJson | & git hash-object -w --stdin).Trim()

    Add-TestIndexEntry $manifestBlob $manifestPath
    foreach ($asset in @($manifestObject.assets)) {
        $assetPath = ([string]$asset.path).Replace('\', '/')
        $assetFile = Join-Path $repoRoot $assetPath
        $assetBlob = (& git hash-object -w -- $assetFile).Trim()
        Add-TestIndexEntry $assetBlob $assetPath
    }
    $approvedFixtureTree = (& git write-tree).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($approvedFixtureTree)) {
        throw 'Unable to create the approved artifact fixture tree.'
    }

    function Reset-TestIndex {
        & git read-tree $approvedFixtureTree
        if ($LASTEXITCODE -ne 0) { throw 'Unable to restore the approved artifact fixture tree.' }
    }

    function Set-TestContentPath([string]$Path, [string]$Content) {
        Reset-TestIndex
        $blob = ($Content | & git hash-object -w --stdin).Trim()
        Add-TestIndexEntry $blob $Path
    }

    function Set-TestPath([string]$Path) {
        Reset-TestIndex
        Add-TestIndexEntry $fixtureBlob $Path
    }

    function Set-TestRepositoryPath([string]$Path) {
        Reset-TestIndex
        $fullPath = Join-Path $repoRoot $Path
        $blob = (& git hash-object -w -- $fullPath).Trim()
        Add-TestIndexEntry $blob $Path
    }

    function Set-TestManifestContent([string]$Content) {
        Reset-TestIndex
        $blob = ($Content | & git hash-object -w --stdin).Trim()
        Add-TestIndexEntry $blob $manifestPath
    }

    function Set-TestContentWithManifest([string]$Path, [string]$Content, [string]$ManifestContent) {
        Reset-TestIndex
        $manifestTestBlob = ($ManifestContent | & git hash-object -w --stdin).Trim()
        Add-TestIndexEntry $manifestTestBlob $manifestPath
        $contentBlob = ($Content | & git hash-object -w --stdin).Trim()
        Add-TestIndexEntry $contentBlob $Path
    }

    function Invoke-GuardChecker {
        $previousErrorAction = $ErrorActionPreference
        try {
            # Windows PowerShell 5 can promote a child pwsh stderr stream to a
            # terminating NativeCommandError even when it is redirected. A
            # Blocked fixtures are expected, so retain output only for an
            # unexpected allow/fail assertion instead of printing every case.
            $ErrorActionPreference = 'Continue'
            $script:lastGuardOutput = @(& $shell -NoProfile -File $checker -Mode staged 2>&1)
            return $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $previousErrorAction
        }
    }

    function Assert-Blocked([string]$Path) {
        Set-TestPath $Path
        $exitCode = Invoke-GuardChecker
        if ($exitCode -eq 0) { throw "Expected guard to block: $Path" }
    }

    function Assert-Allowed([string]$Path) {
        Set-TestPath $Path
        $exitCode = Invoke-GuardChecker
        if ($exitCode -ne 0) { throw "Expected guard to allow: $Path`n$($script:lastGuardOutput -join "`n")" }
    }

    function Assert-BlockedContent([string]$Path, [string]$Content) {
        Set-TestContentPath $Path $Content
        $exitCode = Invoke-GuardChecker
        if ($exitCode -eq 0) { throw "Expected guard to block content in: $Path" }
    }

    function Assert-AllowedContent([string]$Path, [string]$Content) {
        Set-TestContentPath $Path $Content
        $exitCode = Invoke-GuardChecker
        if ($exitCode -ne 0) { throw "Expected guard to allow content in: $Path`n$($script:lastGuardOutput -join "`n")" }
    }

    function Assert-AllowedRepositoryPath([string]$Path) {
        Set-TestRepositoryPath $Path
        $exitCode = Invoke-GuardChecker
        if ($exitCode -ne 0) { throw "Expected guard to allow approved repository artifact: $Path`n$($script:lastGuardOutput -join "`n")" }
    }

    function Assert-BlockedManifest([string]$Content) {
        Set-TestManifestContent $Content
        $exitCode = Invoke-GuardChecker
        if ($exitCode -eq 0) { throw 'Expected guard to block modified artifact manifest.' }
    }

    function Assert-BlockedMissingStagedManifest {
        Reset-TestIndex
        & git update-index --force-remove -- $manifestPath
        if ($LASTEXITCODE -ne 0) { throw 'Unable to remove the staged manifest fixture.' }
        $exitCode = Invoke-GuardChecker
        if ($exitCode -eq 0) { throw 'Expected guard to fail closed when the manifest is absent from the index.' }
        if (($script:lastGuardOutput -join "`n") -notmatch 'approved public artifact manifest is missing') {
            throw "Expected the missing-index-manifest failure reason.`n$($script:lastGuardOutput -join "`n")"
        }
    }

    function Assert-BlockedContentWithManifest([string]$Path, [string]$Content, [string]$ManifestContent) {
        Set-TestContentWithManifest $Path $Content $ManifestContent
        $exitCode = Invoke-GuardChecker
        if ($exitCode -eq 0) { throw "Expected guard to block forged manifest content in: $Path" }
    }

    Assert-Blocked 'materials/source.PPTX'
    Assert-Blocked '자료/강사용 원본.PPTX'
    Assert-Blocked 'private/notes.txt'
    Assert-Blocked 'exports/course.pdf'
    Assert-Blocked 'assets/drawing.dwg'
    Assert-Blocked 'assets/fonts/LGEIText.ttf'
    Assert-Blocked 'assets/fonts/LGEIHeadline.woff2'
    Assert-Blocked 'exports/source-slide-01.png'
    Assert-Blocked 'exports/deck-page.jpg'
    Assert-Blocked 'exports/deck-page.webp'
    Assert-Blocked 'exports/source-slide.svg'
    Assert-Blocked 'archives/materials.zip'
    Assert-Blocked 'archives/materials.tar'
    Assert-Blocked 'archives/materials.tar.gz'
    Assert-Blocked 'archives/materials.tgz'
    Assert-Blocked 'archives/materials.bz2'
    Assert-Blocked 'archives/materials.xz'
    # Windows Git refuses these pathnames before they reach the index. Exercise
    # the NUL-delimited parser on Unix CI, where quote/tab filenames are valid.
    $runningOnWindows = [Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([Runtime.InteropServices.OSPlatform]::Windows)
    if (-not $runningOnWindows) {
        Assert-Blocked 'exports/lecture".pptx'
        Assert-Blocked "exports/lecture`tcopy.pptx"
    }
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/snapshots/final-approval/source-slide-01.png'
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/snapshots/arbitrary.json'
    Assert-Blocked 'docs/autocad-technician/reference/unreviewed.png'
    Assert-Blocked 'planning/AutoCAD_Technician_Video_Course_MasterPlan_260811.html'
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/transcript.json'
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/lesson-01.transcript.json'
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/transcript.tsv'
    Assert-Blocked 'assets/transcripts/lesson-01.json'
    Assert-Blocked 'docs/captions/lesson-01.json'
    Assert-Blocked 'notes/transcript.md'
    Assert-Allowed 'docs/public-course-outline.md'
    Assert-Allowed 'projects/autocad-technician/lesson-01-drawing-language/narration-timing.json'
    Assert-AllowedRepositoryPath 'projects/autocad-technician/lesson-01-drawing-language/snapshots/final-approval/frame-00-at-30s.png'
    Assert-AllowedRepositoryPath 'projects/autocad-technician/lesson-10-final-bracket/snapshots/final-approval/contact-sheet.jpg'
    Assert-AllowedRepositoryPath 'projects/autocad-technician/lesson-07-object-editing/snapshots/finding-01-text_occluded.png'
    Assert-AllowedRepositoryPath 'docs/autocad-technician/reference/a3-landscape-template-reference.png'
    Assert-AllowedRepositoryPath 'docs/autocad-technician/master-plan/AutoCAD_Technician_Video_Course_MasterPlan_260811.html'
    Assert-Blocked 'projects/autocad-technician/lesson-01-drawing-language/snapshots/final-approval/frame-00-at-30s.png'
    Assert-BlockedMissingStagedManifest

    $forgedShaManifest = $manifestJson | ConvertFrom-Json
    $forgedShaManifest.assets[0].sha256 = ('0' * 64)
    Assert-BlockedManifest ($forgedShaManifest | ConvertTo-Json -Depth 8)

    $forgedPayloadBytes = [Text.Encoding]::UTF8.GetBytes('unapproved-slide-payload')
    $sha256 = [Security.Cryptography.SHA256]::Create()
    try {
        $forgedPayloadSha = (($sha256.ComputeHash($forgedPayloadBytes) | ForEach-Object { $_.ToString('x2') }) -join '')
    } finally {
        $sha256.Dispose()
    }
    $forgedDataUriManifest = $manifestJson | ConvertFrom-Json
    $forgedDataUriManifest.assets[0].sha256 = $forgedPayloadSha
    $forgedDataUri = [Convert]::ToBase64String($forgedPayloadBytes)
    Assert-BlockedContentWithManifest `
        'docs/autocad-technician/reports/forged-data-uri.html' `
        "<img src=`"data:image/png;base64,$forgedDataUri`">" `
        ($forgedDataUriManifest | ConvertTo-Json -Depth 8)

    $ghostManifest = $manifestJson | ConvertFrom-Json
    $ghostManifest.assets += [PSCustomObject]@{
        path = 'projects/autocad-technician/lesson-01-drawing-language/snapshots/ghost.png'
        bytes = 4
        sha256 = ('0' * 64)
        gitBlob = ('0' * 40)
    }
    $ghostManifest.assetCount = @($ghostManifest.assets).Count
    Assert-BlockedManifest ($ghostManifest | ConvertTo-Json -Depth 8)

    $outOfScopeManifest = $manifestJson | ConvertFrom-Json
    $outOfScopeManifest.assets += [PSCustomObject]@{
        path = 'exports/ppt-copy.png'
        bytes = 4
        sha256 = ('0' * 64)
        gitBlob = ('0' * 40)
    }
    $outOfScopeManifest.assetCount = @($outOfScopeManifest.assets).Count
    Assert-BlockedManifest ($outOfScopeManifest | ConvertTo-Json -Depth 8)

    $approvedImagePath = Join-Path $repoRoot 'docs/autocad-technician/reference/a3-landscape-template-reference.png'
    $approvedImageData = [Convert]::ToBase64String([IO.File]::ReadAllBytes($approvedImagePath))
    Assert-AllowedContent 'docs/autocad-technician/reports/public.html' "<p>PPT and PPTX sources remain private.</p><img src=`"data:image/png;base64,$approvedImageData`">"
    Assert-BlockedContent 'docs/autocad-technician/reports/unapproved-image.html' '<img src="data:image/png;base64,QUJDRA==">'
    Assert-BlockedContent 'docs/autocad-technician/reports/absolute-path.html' '<p>Do not publish C:\restricted\source.pptx</p>'
    Assert-BlockedContent 'docs/autocad-technician/reports/absolute-path-slash.html' '<p>Do not publish C:/restricted/source.pptx</p>'
    Assert-BlockedContent 'notes/network-path.txt' '<p>Do not publish \\server\share\source.pptx</p>'
    Assert-BlockedContent 'docs/autocad-technician/reports/slide-copy.html' '<p>source-slide-01.png</p>'
    Assert-BlockedContent 'scripts/narration/leaky.py' 'AUDIO = "C:\restricted\lesson-01_narration.wav"'
    Assert-BlockedContent 'scripts/narration/leaky.pyi' 'AUDIO: str = "C:/restricted/lesson-01_narration.wav"'
    Assert-AllowedContent 'scripts/narration/clean.py' 'AUDIO = "recordings/lesson-01_narration.wav"'
    Assert-BlockedContent 'config/.env' 'API_KEY=abcdefghijklmnop'
    Assert-BlockedContent 'config/secret.yml' 'authorization: Bearer abcdefghijklmnopqrstuvwxyz'
    Assert-BlockedContent 'notes/key.txt' '-----BEGIN PRIVATE KEY-----'

    Write-Output 'Private materials guard tests passed.'
    exit 0
} finally {
    $env:GIT_INDEX_FILE = $previousIndex
    Remove-Item -LiteralPath $temporaryIndex -ErrorAction SilentlyContinue
}
