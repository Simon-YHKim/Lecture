[CmdletBinding()]
param(
    [ValidateSet('staged', 'all')]
    [string]$Mode = 'staged'
)

$ErrorActionPreference = 'Stop'

$paths = if ($Mode -eq 'staged') {
    @(& git -c core.quotepath=false diff --cached --name-only --diff-filter=ACMR)
} else {
    @(& git -c core.quotepath=false ls-files)
}

if ($LASTEXITCODE -ne 0) {
    throw 'Unable to read Git paths.'
}

$blockedExtensions = @(
    '.ppt', '.pptx', '.pptm', '.pps', '.ppsx', '.ppsm',
    '.pot', '.potx', '.potm', '.odp',
    '.dwg', '.dxf', '.dwt', '.dws', '.sv$', '.ac$', '.dwl', '.dwl2',
    '.pdf', '.mp4', '.mov', '.mkv', '.avi',
    '.wav', '.m4a', '.mp3', '.srt', '.vtt',
    '.zip', '.7z', '.rar'
)

$privateDirectoryPattern = '(^|/)(private|_private|private-materials|source-materials|raw-materials|local-materials|course-source|private-work)(/|$)'
$violations = @()

foreach ($path in $paths) {
    if ([string]::IsNullOrWhiteSpace($path)) {
        continue
    }

    $normalized = $path.Replace('\', '/').ToLowerInvariant()
    $extension = [IO.Path]::GetExtension($normalized)
    $reason = $null

    if ($normalized -match $privateDirectoryPattern) {
        $reason = 'private-only directory'
    } elseif ($blockedExtensions -contains $extension) {
        $reason = 'blocked private-source or derived-media type'
    } elseif ($normalized -like '*autocad_technician_video_course_masterplan_*.html') {
        $reason = 'private planning source'
    }

    if ($reason) {
        $violations += [PSCustomObject]@{ Path = $path; Reason = $reason }
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
