[CmdletBinding()]
param(
    [string]$RepoRoot,
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $RepoRoot 'docs\autocad-technician\public-artifact-manifest.json'
}

$courseRoot = Join-Path $RepoRoot 'projects\autocad-technician'
$snapshotFiles = @(
    Get-ChildItem -LiteralPath $courseRoot -Recurse -File |
        Where-Object {
            $_.FullName -match '[\\/]lesson-\d{2}-[^\\/]+[\\/]snapshots[\\/]' -and
            $_.Extension.ToLowerInvariant() -in @('.png', '.jpg', '.jpeg')
        }
)
$explicitFiles = @(
    (Join-Path $RepoRoot 'docs\autocad-technician\reference\a3-landscape-template-reference.png'),
    (Join-Path $RepoRoot 'docs\autocad-technician\master-plan\AutoCAD_Technician_Video_Course_MasterPlan_260811.html')
)

# The bracket model under model/ is the course author's own work, cleared for
# publication. CAD sources and images are blocked by extension for everyone
# else, so these files ride the same reviewed path-and-hash allowlist as the
# other public artifacts: rename or edit one and the guard blocks it until this
# script is run again and the change is reviewed.
$modelRoot = Join-Path $RepoRoot 'model'
$modelFiles = @()
if (Test-Path -LiteralPath $modelRoot -PathType Container) {
    $modelFiles = @(
        Get-ChildItem -LiteralPath $modelRoot -Recurse -File |
            Where-Object {
                $_.Extension.ToLowerInvariant() -in @('.ipt', '.iam', '.idw', '.ipn', '.ipj', '.png', '.jpg', '.jpeg')
            }
    )
}
$files = @($snapshotFiles.FullName) + $explicitFiles + @($modelFiles.FullName)

$assets = foreach ($file in ($files | Sort-Object -Unique)) {
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
        throw "Public artifact is missing: $file"
    }
    $fullPath = [IO.Path]::GetFullPath($file)
    $relativePath = $fullPath.Substring([IO.Path]::GetFullPath($RepoRoot).TrimEnd('\').Length).TrimStart('\').Replace('\', '/')
    $gitBlob = (& git -C $RepoRoot hash-object -- $fullPath).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitBlob)) {
        throw "Unable to calculate Git blob hash: $relativePath"
    }
    [ordered]@{
        path    = $relativePath
        bytes   = (Get-Item -LiteralPath $fullPath).Length
        sha256  = (Get-FileHash -LiteralPath $fullPath -Algorithm SHA256).Hash.ToLowerInvariant()
        gitBlob = $gitBlob.ToLowerInvariant()
    }
}

$manifest = [ordered]@{
    schemaVersion = 1
    policy = 'Only exact reviewed paths and hashes may bypass the default private-media block.'
    assetCount = @($assets).Count
    assets = @($assets)
}

$outputDirectory = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
$json = $manifest | ConvertTo-Json -Depth 5
[IO.File]::WriteAllText($OutputPath, $json + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "Public artifact manifest written: $OutputPath ($(@($assets).Count) assets)"
