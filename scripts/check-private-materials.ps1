[CmdletBinding()]
param(
    [ValidateSet('staged', 'all')]
    [string]$Mode = 'staged'
)

$ErrorActionPreference = 'Stop'
$repoRoot = (& git rev-parse --show-toplevel).Trim()
$manifestRelativePath = 'docs/autocad-technician/public-artifact-manifest.json'

function Get-GitOutputBytes([string]$Arguments) {
    # `& git ...` decodes stdout with the console code page, which mangles every
    # non-ASCII byte, so staged reads come back as raw bytes and are decoded as
    # UTF-8 here. ArgumentList is .NET Core only; Windows PowerShell 5.1 needs
    # the single quoted Arguments string, the same way Get-GitNulPaths does it.
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'git'
    $startInfo.Arguments = $Arguments
    $startInfo.WorkingDirectory = $repoRoot
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    $stream = [IO.MemoryStream]::new()
    try {
        if (-not $process.Start()) { return $null }
        $process.StandardOutput.BaseStream.CopyTo($stream)
        [void]$process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) { return $null }
        return $stream.ToArray()
    } finally {
        $stream.Dispose()
        $process.Dispose()
    }
}

function Get-RepositoryText([string]$Path) {
    if ($Mode -eq 'staged') {
        $bytes = Get-GitOutputBytes ('show "' + (":$Path" -replace '"', '\"') + '"')
        if ($null -eq $bytes) { return $null }
        return [Text.UTF8Encoding]::new($false).GetString($bytes)
    }

    $fullPath = Join-Path $repoRoot $Path
    if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
        return Get-Content -LiteralPath $fullPath -Raw -Encoding UTF8
    }
    return $null
}

function Get-Sha256Hex([byte[]]$Bytes) {
    $sha256 = [Security.Cryptography.SHA256]::Create()
    try {
        return (($sha256.ComputeHash($Bytes) | ForEach-Object { $_.ToString('x2') }) -join '')
    } finally {
        $sha256.Dispose()
    }
}

function Get-GitNulPaths([string]$Arguments) {
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'git'
    $startInfo.Arguments = $Arguments
    $startInfo.WorkingDirectory = $repoRoot
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    $stream = [IO.MemoryStream]::new()
    try {
        if (-not $process.Start()) {
            throw "Unable to start git $Arguments"
        }
        $process.StandardOutput.BaseStream.CopyTo($stream)
        $errorText = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) {
            throw "Unable to read Git paths: $errorText"
        }
        $decoded = [Text.UTF8Encoding]::new($false, $true).GetString($stream.ToArray())
        return @($decoded.Split([char]0, [StringSplitOptions]::RemoveEmptyEntries))
    } finally {
        $stream.Dispose()
        $process.Dispose()
    }
}

function Get-GitBlobBytes([string]$GitBlob) {
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'git'
    $startInfo.Arguments = "cat-file blob $GitBlob"
    $startInfo.WorkingDirectory = $repoRoot
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    $stream = [IO.MemoryStream]::new()
    try {
        if (-not $process.Start()) {
            throw "Unable to start git cat-file for blob $GitBlob"
        }
        $process.StandardOutput.BaseStream.CopyTo($stream)
        $errorText = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) {
            throw "Unable to read Git blob $GitBlob`: $errorText"
        }
        return ,$stream.ToArray()
    } finally {
        $stream.Dispose()
        $process.Dispose()
    }
}

function Get-RepositoryAsset([string]$Path) {
    if ($Mode -eq 'staged') {
        $gitBlob = @(& git rev-parse ":$Path" 2>$null) | Select-Object -First 1
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitBlob)) {
            return $null
        }
        $gitBlob = $gitBlob.Trim().ToLowerInvariant()
        $bytes = Get-GitBlobBytes $gitBlob
    } else {
        $fullPath = Join-Path $repoRoot $Path
        if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
            return $null
        }
        $bytes = [IO.File]::ReadAllBytes($fullPath)
        $gitBlob = @(& git hash-object -- $fullPath 2>$null) | Select-Object -First 1
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitBlob)) {
            return $null
        }
        $gitBlob = $gitBlob.Trim().ToLowerInvariant()
    }

    return [PSCustomObject]@{
        Bytes   = $bytes
        GitBlob = $gitBlob
        Sha256  = Get-Sha256Hex $bytes
    }
}

$paths = if ($Mode -eq 'staged') {
    @(Get-GitNulPaths 'diff --cached --name-only --diff-filter=ACMR -z')
} else {
    @(Get-GitNulPaths 'ls-files --cached --others --exclude-standard -z' | Sort-Object -Unique)
}

$blockedExtensions = @(
    '.ppt', '.pptx', '.pptm', '.pps', '.ppsx', '.ppsm',
    '.pot', '.potx', '.potm', '.odp',
    '.dwg', '.dxf', '.dwt', '.dws', '.sv$', '.ac$', '.dwl', '.dwl2',
    '.ipt', '.iam', '.idw', '.ipn', '.ipj',
    '.sldprt', '.sldasm', '.slddrw',
    '.step', '.stp', '.igs', '.iges', '.sat', '.x_t', '.x_b', '.stl',
    '.pdf', '.mp4', '.mov', '.mkv', '.avi',
    '.wav', '.m4a', '.mp3', '.srt', '.vtt',
    '.ttf', '.ttc', '.otf', '.woff', '.woff2',
    '.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tif', '.tiff', '.avif', '.svg',
    '.zip', '.7z', '.rar', '.tar', '.tgz', '.gz', '.bz2', '.xz'
)

$privateDirectoryPattern = '(^|/)(private|_private|private-materials|source-materials|raw-materials|local-materials|course-source|private-work)(/|$)'
# Whisper transcripts and caption data are derived from the private narration
# recordings, so they are blocked unconditionally and cannot be bypassed by the
# approved artifact manifest. Only a numbers-only timing derivative such as
# narration-timing.json may be published.
$privateTranscriptDirectoryPattern = '(^|/)(transcript|transcripts|caption|captions)/'
$privateTranscriptFilePattern = '(^|/)(?:[^/]+\.)?(?:transcript|caption|captions)\.(?:json|txt|tsv|csv|md)$'
$reviewedPublicMasterPlan = 'docs/autocad-technician/master-plan/autocad_technician_video_course_masterplan_260811.html'
$reviewedPublicReference = 'docs/autocad-technician/reference/a3-landscape-template-reference.png'
$reviewedSnapshotPattern = '^projects/autocad-technician/(?:lesson-01-drawing-language|lesson-02-work-environment|lesson-03-lines-polylines|lesson-04-curves-offset|lesson-05-orthographic-reading|lesson-06-placement-repetition|lesson-07-object-editing|lesson-08-representation-reuse|lesson-09-dimensioning|lesson-10-final-bracket)/snapshots/.+\.(?:png|jpe?g)$'
# The EDU-IB-02 bracket model. The course author built it and cleared it for
# publication, so these paths may appear in the manifest; the hash check below
# still applies, and no other CAD file anywhere gets this treatment.
$reviewedModelPattern = '^model/(?:[^/]+/)*[^/]+\.(?:ipt|iam|idw|ipn|ipj|png|jpe?g)$'
$violations = @()
$approvedAssets = @{}
$approvedSha256 = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

$manifestText = Get-RepositoryText $manifestRelativePath
if ([string]::IsNullOrWhiteSpace($manifestText)) {
    $violations += [PSCustomObject]@{ Path = $manifestRelativePath; Reason = 'approved public artifact manifest is missing' }
} else {
    try {
        $manifest = $manifestText | ConvertFrom-Json
        $manifestAssets = @($manifest.assets)
        if ([int]$manifest.schemaVersion -ne 1 -or [int]$manifest.assetCount -ne $manifestAssets.Count) {
            throw 'manifest schema or asset count mismatch'
        }
        foreach ($asset in $manifestAssets) {
            $assetRepositoryPath = ([string]$asset.path).Replace('\', '/')
            $assetPath = $assetRepositoryPath.ToLowerInvariant()
            $assetSha256 = ([string]$asset.sha256).ToLowerInvariant()
            $assetGitBlob = ([string]$asset.gitBlob).ToLowerInvariant()
            $assetBytes = 0L
            $hasValidByteCount = [long]::TryParse(([string]$asset.bytes), [ref]$assetBytes) -and $assetBytes -ge 0
            $isAllowedManifestPath = $assetPath -eq $reviewedPublicMasterPlan -or
                $assetPath -eq $reviewedPublicReference -or
                $assetPath -match $reviewedSnapshotPattern -or
                $assetPath -match $reviewedModelPattern
            if ([string]::IsNullOrWhiteSpace($assetPath) -or
                -not $isAllowedManifestPath -or
                -not $hasValidByteCount -or
                $assetSha256 -notmatch '^[a-f0-9]{64}$' -or
                $assetGitBlob -notmatch '^[a-f0-9]{40}$' -or
                $approvedAssets.ContainsKey($assetPath)) {
                throw "invalid or duplicate manifest entry: $assetPath"
            }

            $repositoryAsset = Get-RepositoryAsset $assetRepositoryPath
            if ($null -eq $repositoryAsset) {
                throw "manifest entry does not exist in the selected repository state: $assetPath"
            }
            if ($repositoryAsset.GitBlob -ne $assetGitBlob -or
                $repositoryAsset.Bytes.LongLength -ne $assetBytes -or
                $repositoryAsset.Sha256 -ne $assetSha256) {
                throw "manifest entry does not match its repository bytes: $assetPath"
            }

            $approvedAssets[$assetPath] = $asset
            [void]$approvedSha256.Add($repositoryAsset.Sha256)
        }
    } catch {
        $violations += [PSCustomObject]@{ Path = $manifestRelativePath; Reason = "invalid approved artifact manifest: $($_.Exception.Message)" }
    }
}

foreach ($path in $paths) {
    if ([string]::IsNullOrWhiteSpace($path)) {
        continue
    }

    $normalized = $path.Replace('\', '/').ToLowerInvariant()
    $extension = [IO.Path]::GetExtension($normalized)
    $reason = $null
    $isReviewedPublicAsset = $approvedAssets.ContainsKey($normalized)

    if ($normalized -match $privateDirectoryPattern) {
        $reason = 'private-only directory'
    } elseif ($normalized -match $privateTranscriptDirectoryPattern -or $normalized -match $privateTranscriptFilePattern) {
        $reason = 'recording-derived transcript or caption data'
    } elseif ($normalized -match '^projects/autocad-technician/lesson-\d{2}-[^/]+/snapshots/' -and -not $isReviewedPublicAsset) {
        $reason = 'snapshot artifact is not in the approved path-and-hash manifest'
    } elseif (($blockedExtensions -contains $extension) -and -not $isReviewedPublicAsset) {
        $reason = 'blocked private-source or derived-media type'
    } elseif (($normalized -like '*autocad_technician_video_course_masterplan_*.html') -and
              ($normalized -ne $reviewedPublicMasterPlan -or -not $isReviewedPublicAsset)) {
        $reason = 'private planning source'
    }

    if (-not $reason -and $isReviewedPublicAsset) {
        $actualGitBlob = $null
        if ($Mode -eq 'staged') {
            $actualGitBlob = @(& git rev-parse ":$path" 2>$null) | Select-Object -First 1
        } else {
            $fullPath = Join-Path $repoRoot $path
            if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
                $actualGitBlob = @(& git hash-object -- $fullPath 2>$null) | Select-Object -First 1
            }
        }
        if ([string]::IsNullOrWhiteSpace($actualGitBlob) -or
            $actualGitBlob.Trim().ToLowerInvariant() -ne ([string]$approvedAssets[$normalized].gitBlob).ToLowerInvariant()) {
            $reason = 'approved public artifact content differs from its manifest hash'
        }
    }

    if ($reason) {
        $violations += [PSCustomObject]@{ Path = $path; Reason = $reason }
    }
}

$contentRules = [ordered]@{
    'absolute Windows path'       = '(?i)(?:^|[\s"''(])(?:[A-Z]:[\\/]|\\\\[A-Za-z0-9_.-]+[\\/])'
    'file URI'                    = '(?i)\bfile:///'
    'private workspace marker'    = '(?i)Lecture_Private'
    'PPT-derived slide artifact'  = '(?i)(source-slide-|assets[/\\]ppt|qa[/\\](source-inspection|review-boards))'
    'private key'                 = '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
    'known credential token'      = '(?i)\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b'
    'bearer credential'           = '(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}'
    'credential assignment'       = '(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|client[_-]?secret)\b\s*[:=]\s*["'']?[A-Za-z0-9_./+=-]{8,}'
}
$scannableExtensions = @('.html', '.htm', '.md', '.json', '.txt', '.ps1', '.psm1', '.psd1', '.yml', '.yaml', '.js', '.mjs', '.cjs', '.ts', '.css', '.xml', '.csv', '.py', '.pyi')
$contentScanExclusions = @(
    'scripts/check-private-materials.ps1',
    'scripts/test-private-materials-guard.ps1',
    'scripts/check-course-projects.ps1'
)

foreach ($path in $paths) {
    if ([string]::IsNullOrWhiteSpace($path)) { continue }
    $normalized = $path.Replace('\', '/').ToLowerInvariant()
    $extension = [IO.Path]::GetExtension($normalized)
    $fileName = [IO.Path]::GetFileName($normalized)
    if (($extension -notin $scannableExtensions -and $fileName -ne '.env') -or $contentScanExclusions -contains $normalized) {
        continue
    }

    $content = Get-RepositoryText $path
    if ($null -eq $content) { continue }

    $embeddedImagePattern = '(?is)data:image/(?:png|jpeg|webp);base64,(?<payload>[A-Za-z0-9+/=\r\n]+)'
    foreach ($embeddedImage in [regex]::Matches($content, $embeddedImagePattern)) {
        try {
            $imageBytes = [Convert]::FromBase64String($embeddedImage.Groups['payload'].Value)
            $imageSha256 = Get-Sha256Hex $imageBytes
            if (-not $approvedSha256.Contains($imageSha256)) {
                $violations += [PSCustomObject]@{ Path = $path; Reason = 'embedded image hash is not in the approved artifact manifest' }
            }
        } catch {
            $violations += [PSCustomObject]@{ Path = $path; Reason = 'embedded image data URI is invalid' }
        }
    }
    $contentForScan = [regex]::Replace($content, $embeddedImagePattern, '[approved-embedded-image]')
    if ($contentForScan -match '(?i)data:image/') {
        $violations += [PSCustomObject]@{ Path = $path; Reason = 'unrecognized embedded image data URI' }
    }
    foreach ($rule in $contentRules.GetEnumerator()) {
        if ([regex]::IsMatch($contentForScan, $rule.Value)) {
            $violations += [PSCustomObject]@{ Path = $path; Reason = $rule.Key }
        }
    }
}

if ($violations.Count -gt 0) {
    foreach ($violation in $violations) {
        [Console]::Error.WriteLine("BLOCKED: {0} ({1})", $violation.Path, $violation.Reason)
    }
    [Console]::Error.WriteLine('Private course material detected. Keep originals outside this public repository.')
    exit 1
}

Write-Output "Private materials guard passed ($Mode)."
