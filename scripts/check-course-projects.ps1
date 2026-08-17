[CmdletBinding()]
param(
    [switch]$RunHyperFramesChecks
)

$ErrorActionPreference = 'Stop'
$PSDefaultParameterValues['Get-Content:Encoding'] = 'UTF8'
$repoRoot = (& git rev-parse --show-toplevel).Trim()
$courseRoot = Join-Path $repoRoot 'projects\autocad-technician'

$expectedDurations = [ordered]@{
    'lesson-01-drawing-language'     = 600
    'lesson-02-work-environment'     = 720
    'lesson-03-lines-polylines'      = 720
    'lesson-04-curves-offset'        = 720
    'lesson-05-orthographic-reading' = 780
    'lesson-06-placement-repetition' = 780
    'lesson-07-object-editing'       = 855
    'lesson-08-representation-reuse' = 660
    'lesson-09-dimensioning'         = 840
    'lesson-10-final-bracket'        = 1140
}

$expectedDemoCounts = [ordered]@{
    'lesson-01-drawing-language'     = 2
    'lesson-02-work-environment'     = 3
    'lesson-03-lines-polylines'      = 3
    'lesson-04-curves-offset'        = 3
    'lesson-05-orthographic-reading' = 2
    'lesson-06-placement-repetition' = 3
    'lesson-07-object-editing'       = 3
    'lesson-08-representation-reuse' = 3
    'lesson-09-dimensioning'         = 3
    'lesson-10-final-bracket'        = 4
}

$requiredFiles = @('BRIEF.md', 'SCRIPT.md', 'STORYBOARD.md', 'frame.md', 'index.html', 'meta.json', 'hyperframes.json', 'package.json')
$allowedColors = @('#111111', '#666666', '#A4A3A4', '#C7004C', '#F5F5F3', '#FFFFFF')
$forbiddenContent = '(?i)([A-Z]:\\|source-slide-|LG이노텍|\.pptx\b|\.pptm\b|data:image/|<img\b|assets/private/fonts|@font-face\s*\{[^}]*private)'
$failures = [System.Collections.Generic.List[string]]::new()
$results = [System.Collections.Generic.List[object]]::new()

function Get-PointDistance($PointA, $PointB) {
    $dx = [double]$PointA[0] - [double]$PointB[0]
    $dy = [double]$PointA[1] - [double]$PointB[1]
    return [Math]::Sqrt(($dx * $dx) + ($dy * $dy))
}

function Get-PointSegmentDistance($Point, $SegmentStart, $SegmentEnd) {
    $vx = [double]$SegmentEnd[0] - [double]$SegmentStart[0]
    $vy = [double]$SegmentEnd[1] - [double]$SegmentStart[1]
    $wx = [double]$Point[0] - [double]$SegmentStart[0]
    $wy = [double]$Point[1] - [double]$SegmentStart[1]
    $lengthSquared = ($vx * $vx) + ($vy * $vy)
    if ($lengthSquared -le 0) { return Get-PointDistance $Point $SegmentStart }
    $t = [Math]::Max(0, [Math]::Min(1, (($wx * $vx) + ($wy * $vy)) / $lengthSquared))
    $projectionX = ([double]$SegmentStart[0]) + ($t * $vx)
    $projectionY = ([double]$SegmentStart[1]) + ($t * $vy)
    $projection = @($projectionX, $projectionY)
    return Get-PointDistance $Point $projection
}

function Test-PointNear($Actual, $Expected, [double]$Tolerance = 0.002) {
    return (Get-PointDistance $Actual $Expected) -le $Tolerance
}

$canonicalFramePath = Join-Path $courseRoot 'FRAME_STANDARD.md'
$canonicalFrameText = if (Test-Path -LiteralPath $canonicalFramePath -PathType Leaf) {
    Get-Content -LiteralPath $canonicalFramePath -Raw
} else {
    $failures.Add('course: missing FRAME_STANDARD.md')
    $null
}
$masterSpecPath = Join-Path $courseRoot 'MASTER_DRAWING_SPEC.md'
$continuityPath = Join-Path $courseRoot 'course-continuity.json'
$geometryPath = Join-Path $courseRoot 'master-part-geometry.json'
$recordingMapPath = Join-Path $courseRoot 'recording-map.json'
$continuity = $null
$geometry = $null
$recordingMap = $null
if (-not (Test-Path -LiteralPath $masterSpecPath -PathType Leaf)) {
    $failures.Add('course: missing MASTER_DRAWING_SPEC.md')
}
if (-not (Test-Path -LiteralPath $continuityPath -PathType Leaf)) {
    $failures.Add('course: missing course-continuity.json')
} else {
    try {
        $continuity = Get-Content -LiteralPath $continuityPath -Raw | ConvertFrom-Json
    } catch {
        $failures.Add('course: invalid course-continuity.json')
    }
}
if (-not (Test-Path -LiteralPath $geometryPath -PathType Leaf)) {
    $failures.Add('course: missing master-part-geometry.json')
} else {
    try {
        $geometry = Get-Content -LiteralPath $geometryPath -Raw | ConvertFrom-Json
    } catch {
        $failures.Add('course: invalid master-part-geometry.json')
    }
}
if (-not (Test-Path -LiteralPath $recordingMapPath -PathType Leaf)) {
    $failures.Add('course: missing recording-map.json')
} else {
    try {
        $recordingMap = Get-Content -LiteralPath $recordingMapPath -Raw | ConvertFrom-Json
    } catch {
        $failures.Add('course: invalid recording-map.json')
    }
}

if ($null -ne $continuity) {
    if ($continuity.partId -ne 'EDU-SB-01') { $failures.Add('course: unexpected master part id') }
    if ($continuity.paper.format -ne 'A3' -or [int]$continuity.paper.widthMm -ne 420 -or [int]$continuity.paper.heightMm -ne 297 -or $continuity.paper.orientation -ne 'landscape') {
        $failures.Add('course: paper must be ISO A3 landscape 420x297')
    }
    if ($continuity.startup.template -ne 'acadiso.dwt' -or $continuity.startup.units -ne 'millimeters') {
        $failures.Add('course: startup must use acadiso.dwt with millimeters')
    }
    if ($continuity.workspace.courseDefault -ne 'layout-paper-space' -or
        -not ([string]$continuity.workspace.paperGeometryScale).Contains('1:1') -or
        -not ([string]$continuity.workspace.modelGeometryScale).Contains('1:1') -or
        -not ([string]$continuity.workspace.authority).Contains('exam-provided')) {
        $failures.Add('course: workspace contract must separate Model 1:1 from Layout/Paper 1:1 and defer to exam files')
    }
    if ($continuity.projection.method -ne 'third-angle') { $failures.Add('course: projection must be third-angle') }
    if ([int]$continuity.paper.courseFrameInsetMm -ne 10 -or [int]$continuity.paper.titleBlock.widthMm -ne 200 -or [int]$continuity.paper.titleBlock.heightMm -ne 30 -or [int]$continuity.paper.titleBlock.textHeightMm -ne 10) {
        $failures.Add('course: A3 frame/title block does not match the approved 10mm / 200x30 / text 10 training template')
    }
    $titleCells = @($continuity.paper.titleBlock.cells)
    if ($titleCells.Count -ne 2 -or [int]$titleCells[0].widthMm -ne 100 -or [int]$titleCells[1].widthMm -ne 100) {
        $failures.Add('course: title block must contain two 100mm cells')
    }
    $coreLayerNames = @($continuity.requiredCoreLayers)
    foreach ($requiredLayer in @('OUTLINE', 'CENTER', 'HIDDEN', 'DIM')) {
        if ($coreLayerNames -notcontains $requiredLayer) {
            $failures.Add("course: missing required core layer $requiredLayer")
        }
    }
    $expectedLayerNames = @('OUTLINE', 'CENTER', 'HIDDEN', 'DIM', 'BORDER', 'TITLE', 'HATCH', 'CONSTRUCTION')
    $declaredLayerNames = @($continuity.layers | ForEach-Object { [string]$_.name })
    $usedLayerNames = @(
        $continuity.checkpoints |
            ForEach-Object { @($_.layersUsed) } |
            Sort-Object -Unique
    )
    foreach ($expectedLayer in $expectedLayerNames) {
        if ($declaredLayerNames -notcontains $expectedLayer) {
            $failures.Add("course: missing canonical layer definition $expectedLayer")
        }
        if ($usedLayerNames -notcontains $expectedLayer) {
            $failures.Add("course: canonical layer is never practiced $expectedLayer")
        }
    }
    if (-not ([string]$continuity.paper.authority).Contains('exam-instructions-override') -or
        -not ([string]$continuity.projection.authority).Contains('exam-instructions-override') -or
        -not ([string]$continuity.examDisclosure.authority).Contains('official-exam-sheet')) {
        $failures.Add('course: official exam instructions must override course defaults')
    }
    if (@($continuity.checkpoints).Count -ne $expectedDurations.Count) {
        $failures.Add("course: expected $($expectedDurations.Count) continuity checkpoints")
    }
    if ($continuity.geometrySpec -ne 'master-part-geometry.json') {
        $failures.Add('course: continuity must reference master-part-geometry.json')
    }
    if ($continuity.recordingMap -ne 'recording-map.json') {
        $failures.Add('course: continuity must reference recording-map.json')
    }
}

if ($null -ne $recordingMap) {
    if ([int]$recordingMap.totalSlots -ne 29 -or @($recordingMap.slots).Count -ne 29) {
        $failures.Add('course: recording map must contain exactly 29 slots')
    }
    $recordingKeys = @($recordingMap.slots | ForEach-Object { "$($_.lesson)|$($_.demoId)" })
    if (@($recordingKeys | Sort-Object -Unique).Count -ne $recordingKeys.Count) {
        $failures.Add('course: recording map contains duplicate lesson/demo ids')
    }
}

if ($null -ne $geometry) {
    if ($geometry.partId -ne 'EDU-SB-01' -or $geometry.units -ne 'millimeters') {
        $failures.Add('course: geometry identity or units differ from EDU-SB-01 millimeters')
    }
    if ([double]$geometry.envelope.widthX -ne 80 -or [double]$geometry.envelope.heightY -ne 50 -or [double]$geometry.envelope.thicknessZ -ne 8) {
        $failures.Add('course: geometry envelope must remain 80x50x8')
    }

    $centralHole = $geometry.features.centralSensorHole
    $hexPocket = $geometry.features.centralHexPocket
    $mounting = $geometry.features.bottomMountingHoles
    $pattern = $geometry.features.sensorPattern
    $slot = $geometry.features.upperSlot
    $minimumClearance = [double]$geometry.clearanceRules.minimumMaterialClearanceMm

    if (-not (Test-PointNear $centralHole.center @(40, 22)) -or [double]$centralHole.diameter -ne 20) {
        $failures.Add('course: central sensor hole must remain center (40,22), diameter 20')
    }
    if (-not (Test-PointNear $hexPocket.center @(40, 22)) -or [double]$hexPocket.acrossFlats -ne 30 -or @($hexPocket.vertices).Count -ne 6) {
        $failures.Add('course: central hex pocket must remain center (40,22), AF30 with six exact vertices')
    }
    if ([int]$mounting.quantity -ne 2 -or [double]$mounting.diameter -ne 6 -or @($mounting.centers).Count -ne 2 -or
        -not (Test-PointNear $mounting.centers[0] @(15, 8)) -or -not (Test-PointNear $mounting.centers[1] @(65, 8))) {
        $failures.Add('course: bottom mounting holes must remain 2 x diameter 6 at (15,8) and (65,8)')
    }
    $expectedPatternCenters = @(@(55.588, 31), @(24.412, 31), @(40, 4))
    if ([int]$pattern.quantity -ne 3 -or [double]$pattern.diameter -ne 4 -or [double]$pattern.pitchCircleDiameter -ne 36 -or
        [double]$pattern.startAngleDeg -ne 30 -or @($pattern.centers).Count -ne 3) {
        $failures.Add('course: sensor pattern must remain 3 x diameter 4 on PCD 36 from 30 degrees')
    } else {
        for ($i = 0; $i -lt $expectedPatternCenters.Count; $i++) {
            if (-not (Test-PointNear $pattern.centers[$i] $expectedPatternCenters[$i])) {
                $failures.Add("course: sensor pattern center $i differs from canonical geometry")
            }
            $patternRadius = Get-PointDistance $pattern.centers[$i] $pattern.patternCenter
            if ([Math]::Abs($patternRadius - 18) -gt 0.002) {
                $failures.Add("course: sensor pattern center $i is not on PCD 36")
            }
        }
    }
    if (-not (Test-PointNear $slot.center @(40, 42)) -or [double]$slot.width -ne 8 -or
        -not (Test-PointNear $slot.endCenters[0] @(33, 42)) -or -not (Test-PointNear $slot.endCenters[1] @(47, 42)) -or
        [double]$slot.endCenterDistance -ne 14 -or [double]$slot.overallLength -ne 22) {
        $failures.Add('course: upper slot must remain center (40,42), width 8, overall length 22')
    }
    if ($minimumClearance -lt 1) {
        $failures.Add('course: canonical feature clearance must be at least 1mm')
    }

    $section = $geometry.sectionAA
    if ($section.plane -ne 'x=40' -or @($section.voidsYZ).Count -ne 4 -or
        -not (Test-PointNear $section.outerEnvelopeYZ.z @(0, 8)) -or
        -not (Test-PointNear $section.outerEnvelopeYZ.y @(0, 50))) {
        $failures.Add('course: A-A section must define the exact Y50 x Z8 envelope and four canonical voids')
    } else {
        $expectedSectionVoids = [ordered]@{
            sensorPattern     = [pscustomobject]@{ z = @(0, 8); y = @(2, 6) }
            centralHexPocket  = [pscustomobject]@{ z = @(0, 4); y = @(7, 37) }
            centralSensorHole = [pscustomobject]@{ z = @(0, 8); y = @(12, 32) }
            upperSlot         = [pscustomobject]@{ z = @(0, 8); y = @(38, 46) }
        }
        foreach ($voidName in $expectedSectionVoids.Keys) {
            $actualVoid = @($section.voidsYZ | Where-Object { $_.feature -eq $voidName }) | Select-Object -First 1
            if ($null -eq $actualVoid -or
                -not (Test-PointNear $actualVoid.z $expectedSectionVoids[$voidName].z) -or
                -not (Test-PointNear $actualVoid.y $expectedSectionVoids[$voidName].y)) {
                $failures.Add("course: A-A section void differs for $voidName")
            }
        }
    }

    $projected = $geometry.orthographic.projectedFeatures
    $expectedProjection = [ordered]@{
        centralSensorHole = [pscustomobject]@{ topEdges = @(30, 50); topCenter = 40; rightEdges = @(12, 32); rightCenter = 22 }
        centralHexPocket  = [pscustomobject]@{ topEdges = @(22.679, 57.321); topCenter = 40; rightEdges = @(7, 37); rightCenter = 22 }
        upperSlot         = [pscustomobject]@{ topEdges = @(29, 51); topCenter = 40; rightEdges = @(38, 46); rightCenter = 42 }
        localShallowPocket = [pscustomobject]@{ topEdges = @(5, 19); topCenter = 12; rightEdges = @(15, 29); rightCenter = 22 }
    }
    foreach ($featureName in $expectedProjection.Keys) {
        $projectionFeature = $projected.$featureName
        if ($null -eq $projectionFeature -or
            -not (Test-PointNear $projectionFeature.top.hiddenParallelEdgesX $expectedProjection[$featureName].topEdges) -or
            [double]$projectionFeature.top.centerAxisX -ne [double]$expectedProjection[$featureName].topCenter -or
            -not (Test-PointNear $projectionFeature.right.hiddenParallelEdgesY $expectedProjection[$featureName].rightEdges) -or
            [double]$projectionFeature.right.centerAxisY -ne [double]$expectedProjection[$featureName].rightCenter) {
            $failures.Add("course: orthographic projection contract differs for $featureName")
        }
    }
    foreach ($requiredProjectedPattern in @('bottomMountingHoles', 'sensorPattern')) {
        if ($null -eq $projected.$requiredProjectedPattern) {
            $failures.Add("course: orthographic projection contract missing $requiredProjectedPattern")
        }
    }

    $localPocket = $geometry.features.localShallowPocket
    if ($null -eq $localPocket -or [double]$localPocket.depth -ne 2 -or [double]$localPocket.nominalOffset -ne 5 -or
        -not (Test-PointNear $localPocket.seedWindow.lowerLeft @(0, 10)) -or
        -not (Test-PointNear $localPocket.seedWindow.upperRight @(24, 34)) -or
        -not (Test-PointNear $localPocket.finalBoundary.lowerLeft @(5, 15)) -or
        -not (Test-PointNear $localPocket.finalBoundary.upperRight @(19, 29))) {
        $failures.Add('course: local shallow pocket must be the 5mm inward offset of seed window (0,10)-(24,34)')
    }

    $patternRadiusMm = [double]$pattern.diameter / 2
    $slotRadiusMm = [double]$slot.width / 2
    $mountingRadiusMm = [double]$mounting.diameter / 2
    $centralRadiusMm = [double]$centralHole.diameter / 2
    foreach ($patternCenter in @($pattern.centers)) {
        $slotDistance = Get-PointSegmentDistance $patternCenter $slot.endCenters[0] $slot.endCenters[1]
        if ($slotDistance -lt ($patternRadiusMm + $slotRadiusMm + $minimumClearance - 0.002)) {
            $failures.Add('course: sensor pattern overlaps or under-clears the upper slot')
        }
        if ((Get-PointDistance $patternCenter $centralHole.center) -lt ($patternRadiusMm + $centralRadiusMm + $minimumClearance - 0.002)) {
            $failures.Add('course: sensor pattern overlaps or under-clears the central hole')
        }
        foreach ($mountingCenter in @($mounting.centers)) {
            if ((Get-PointDistance $patternCenter $mountingCenter) -lt ($patternRadiusMm + $mountingRadiusMm + $minimumClearance - 0.002)) {
                $failures.Add('course: sensor pattern overlaps or under-clears a mounting hole')
            }
        }
        $hexEdgeDistance = [double]::PositiveInfinity
        $hexVertices = @($hexPocket.vertices)
        for ($edgeIndex = 0; $edgeIndex -lt $hexVertices.Count; $edgeIndex++) {
            $edgeDistance = Get-PointSegmentDistance $patternCenter $hexVertices[$edgeIndex] $hexVertices[($edgeIndex + 1) % $hexVertices.Count]
            if ($edgeDistance -lt $hexEdgeDistance) { $hexEdgeDistance = $edgeDistance }
        }
        if ($hexEdgeDistance -lt ($patternRadiusMm + $minimumClearance - 0.002)) {
            $failures.Add('course: sensor pattern overlaps or under-clears the AF30 pocket')
        }
    }
    $outerArcCenter = @(40, 35)
    foreach ($slotEndCenter in @($slot.endCenters)) {
        $arcMaterial = 15 - (Get-PointDistance $slotEndCenter $outerArcCenter) - $slotRadiusMm
        if ($arcMaterial -lt ($minimumClearance - 0.002)) {
            $failures.Add('course: upper slot overlaps or under-clears the outer R15 lug arc')
        }
    }
    $hexTopY = 37.0
    $slotBottomY = [double]$slot.center[1] - ([double]$slot.width / 2)
    if (($slotBottomY - $hexTopY) -lt ($minimumClearance - 0.002)) {
        $failures.Add('course: upper slot overlaps or under-clears the AF30 pocket')
    }
    if ($null -ne $localPocket) {
        $pocketLeft = [double]$localPocket.finalBoundary.lowerLeft[0]
        $pocketBottom = [double]$localPocket.finalBoundary.lowerLeft[1]
        $pocketRight = [double]$localPocket.finalBoundary.upperRight[0]
        $pocketTop = [double]$localPocket.finalBoundary.upperRight[1]
        foreach ($featureCircle in @(
            @([double]$mounting.centers[0][0], [double]$mounting.centers[0][1], $mountingRadiusMm, 'mounting hole'),
            @([double]$pattern.centers[1][0], [double]$pattern.centers[1][1], $patternRadiusMm, 'sensor pattern')
        )) {
            $closestX = [Math]::Max($pocketLeft, [Math]::Min($pocketRight, [double]$featureCircle[0]))
            $closestY = [Math]::Max($pocketBottom, [Math]::Min($pocketTop, [double]$featureCircle[1]))
            $distance = Get-PointDistance @([double]$featureCircle[0], [double]$featureCircle[1]) @($closestX, $closestY)
            if ($distance -lt ([double]$featureCircle[2] + $minimumClearance - 0.002)) {
                $failures.Add("course: local shallow pocket overlaps or under-clears $($featureCircle[3])")
            }
        }
        $hexEdgeDistanceFromPocket = [double]::PositiveInfinity
        foreach ($pocketCorner in @(@($pocketLeft, $pocketBottom), @($pocketRight, $pocketBottom), @($pocketRight, $pocketTop), @($pocketLeft, $pocketTop))) {
            for ($edgeIndex = 0; $edgeIndex -lt $hexVertices.Count; $edgeIndex++) {
                $edgeDistance = Get-PointSegmentDistance $pocketCorner $hexVertices[$edgeIndex] $hexVertices[($edgeIndex + 1) % $hexVertices.Count]
                if ($edgeDistance -lt $hexEdgeDistanceFromPocket) { $hexEdgeDistanceFromPocket = $edgeDistance }
            }
        }
        if ($hexEdgeDistanceFromPocket -lt ($minimumClearance - 0.002)) {
            $failures.Add('course: local shallow pocket overlaps or under-clears the AF30 pocket')
        }
    }
}

if (Test-Path -LiteralPath $masterSpecPath -PathType Leaf) {
    $masterSpecText = Get-Content -LiteralPath $masterSpecPath -Raw
    foreach ($requiredMasterMarker in @('EDU-SB-01', 'master-part-geometry.json', 'acadiso.dwt', 'A3', '420 × 297', 'Layout/Paper Space', 'Viewport', '제3각법', 'OUTLINE', 'CENTER', 'HIDDEN', 'DIM', '3D 모델', '감점', '문제지와 감독 지시', '시작각 30°')) {
        if (-not $masterSpecText.Contains($requiredMasterMarker)) {
            $failures.Add("course: MASTER_DRAWING_SPEC missing $requiredMasterMarker")
        }
    }
}

foreach ($courseDocument in @('COURSE_PLAN.md', 'RECORDING_GUIDE.md')) {
    $courseDocumentPath = Join-Path $courseRoot $courseDocument
    if (-not (Test-Path -LiteralPath $courseDocumentPath -PathType Leaf)) {
        $failures.Add("course: missing $courseDocument")
        continue
    }
    $courseDocumentText = Get-Content -LiteralPath $courseDocumentPath -Raw
    foreach ($requiredCourseMarker in @('EDU-SB-01', 'A3', '420×297', '제3각법', 'OUTLINE', 'CENTER', 'HIDDEN', 'DIM', '3D 모델', '감점')) {
        if (-not $courseDocumentText.Contains($requiredCourseMarker)) {
            $failures.Add("course: $courseDocument missing $requiredCourseMarker")
        }
    }
}

function Get-HtmlAttribute([string]$Tag, [string]$Name) {
    $pattern = '(?i)\b' + [regex]::Escape($Name) + '="([^"]+)"'
    $match = [regex]::Match($Tag, $pattern)
    if ($match.Success) { return $match.Groups[1].Value }
    return $null
}

function Get-DemoIds([string]$Text) {
    if ([string]::IsNullOrWhiteSpace($Text)) { return @() }
    return @([regex]::Matches($Text, 'DEMO-\d{2}') | ForEach-Object { $_.Value } | Sort-Object -Unique)
}

$previousCheckpointOut = $null

foreach ($entry in $expectedDurations.GetEnumerator()) {
    $name = $entry.Key
    $expectedDuration = [int]$entry.Value
    $projectRoot = Join-Path $courseRoot $name
    $checkpoint = if ($null -ne $continuity) { @($continuity.checkpoints | Where-Object { $_.lesson -eq $name }) | Select-Object -First 1 } else { $null }

    if ($null -eq $checkpoint) {
        $failures.Add("${name}: missing continuity checkpoint")
    } else {
        if ($null -ne $previousCheckpointOut -and $checkpoint.'in' -ne $previousCheckpointOut) {
            $failures.Add("${name}: checkpoint in '$($checkpoint.'in')' does not match previous out '$previousCheckpointOut'")
        }
        $previousCheckpointOut = [string]$checkpoint.out
        if (@($checkpoint.layersUsed).Count -eq 0) {
            $failures.Add("${name}: continuity checkpoint has no layersUsed")
        }
    }

    if (-not (Test-Path -LiteralPath $projectRoot -PathType Container)) {
        $failures.Add("${name}: project directory is missing")
        continue
    }

    foreach ($relativePath in $requiredFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $projectRoot $relativePath) -PathType Leaf)) {
            $failures.Add("${name}: missing $relativePath")
        }
    }

    $projectFramePath = Join-Path $projectRoot 'frame.md'
    if ($null -ne $canonicalFrameText -and (Test-Path -LiteralPath $projectFramePath -PathType Leaf)) {
        $projectFrameText = Get-Content -LiteralPath $projectFramePath -Raw
        if ($projectFrameText -cne $canonicalFrameText) {
            $failures.Add("${name}: frame.md differs from FRAME_STANDARD.md")
        }
    }

    $indexPath = Join-Path $projectRoot 'index.html'
    $actualDuration = $null
    $indexSources = @()
    $indexDurations = @()
    if (Test-Path -LiteralPath $indexPath -PathType Leaf) {
        $indexText = Get-Content -LiteralPath $indexPath -Raw
        $compositionTags = [regex]::Matches($indexText, '(?is)<[^>]*\bdata-composition-src="[^"]+"[^>]*>')
        if ($compositionTags.Count -ne 6) {
            $failures.Add("${name}: expected 6 composition references in index.html, found $($compositionTags.Count)")
        }
        $expectedStart = 0.0
        foreach ($compositionTagMatch in $compositionTags) {
            $tag = $compositionTagMatch.Value
            $source = Get-HtmlAttribute $tag 'data-composition-src'
            $startValue = Get-HtmlAttribute $tag 'data-start'
            $durationValue = Get-HtmlAttribute $tag 'data-duration'
            $indexCompositionId = Get-HtmlAttribute $tag 'data-composition-id'
            if ($null -eq $source -or $null -eq $startValue -or $null -eq $durationValue) {
                $failures.Add("${name}: composition reference is missing src/start/duration")
                continue
            }
            $start = [double]$startValue
            $duration = [double]$durationValue
            $indexSources += $source.Replace('\', '/')
            $indexDurations += $duration
            if ([Math]::Abs($start - $expectedStart) -gt 0.001) {
                $failures.Add("${name}: non-contiguous scene start $start; expected $expectedStart")
            }
            $expectedStart = $start + $duration

            $referencedPath = Join-Path $projectRoot $source
            if (-not (Test-Path -LiteralPath $referencedPath -PathType Leaf)) {
                $failures.Add("${name}: missing referenced composition $source")
                continue
            }

            $frameText = Get-Content -LiteralPath $referencedPath -Raw
            $frameRootTag = [regex]::Match($frameText, '(?is)<[^>]*\bdata-composition-id="[^"]+"[^>]*>').Value
            $frameCompositionId = Get-HtmlAttribute $frameRootTag 'data-composition-id'
            $frameDurationValue = Get-HtmlAttribute $frameRootTag 'data-duration'
            if ($null -eq $frameCompositionId -or $null -eq $frameDurationValue) {
                $failures.Add("${name}: root id/duration missing in $source")
            } else {
                $frameDuration = [double]$frameDurationValue
                if ([Math]::Abs($frameDuration - $duration) -gt 0.001) {
                    $failures.Add("${name}: $source duration $frameDuration differs from index $duration")
                }
                if ($indexCompositionId -and $indexCompositionId -ne $frameCompositionId) {
                    $failures.Add("${name}: $source composition id differs from index")
                }
                $doubleTimelineKey = 'window.__timelines["' + $frameCompositionId + '"]'
                $singleTimelineKey = "window.__timelines['" + $frameCompositionId + "']"
                if (-not $frameText.Contains($doubleTimelineKey) -and -not $frameText.Contains($singleTimelineKey)) {
                    $failures.Add("${name}: timeline key not registered for $frameCompositionId")
                }
            }

            $motionPath = [IO.Path]::ChangeExtension($referencedPath, $null) + '.motion.json'
            if (Test-Path -LiteralPath $motionPath -PathType Leaf) {
                try {
                    $motion = Get-Content -LiteralPath $motionPath -Raw | ConvertFrom-Json
                    if ([Math]::Abs(([double]$motion.duration) - $duration) -gt 0.001) {
                        $failures.Add("${name}: $([IO.Path]::GetFileName($motionPath)) duration differs from index")
                    }
                } catch {
                    $failures.Add("${name}: invalid motion JSON $([IO.Path]::GetFileName($motionPath))")
                }
            }
        }
        if ([Math]::Abs($expectedStart - $expectedDuration) -gt 0.001) {
            $failures.Add("${name}: scene sequence ends at $expectedStart instead of $expectedDuration")
        }
        $durationMatch = [regex]::Match($indexText, 'data-composition-id="[^"]+"[^>]*data-duration="([0-9.]+)"')
        if (-not $durationMatch.Success) {
            $durationMatch = [regex]::Match($indexText, 'data-duration="([0-9.]+)"[^>]*data-composition-id="[^"]+"')
        }
        if ($durationMatch.Success) {
            $actualDuration = [double]$durationMatch.Groups[1].Value
            if ([Math]::Abs($actualDuration - $expectedDuration) -gt 0.001) {
                $failures.Add("${name}: duration $actualDuration does not match $expectedDuration")
            }
        } else {
            $failures.Add("${name}: root data-duration not found")
        }
    }

    $scriptPath = Join-Path $projectRoot 'SCRIPT.md'
    $scriptText = ''
    if (Test-Path -LiteralPath $scriptPath -PathType Leaf) {
        $scriptText = Get-Content -LiteralPath $scriptPath -Raw
        $scriptSections = [regex]::Matches($scriptText, '(?m)^## Line\s+[1-6]\b')
        if ($scriptSections.Count -ne 6) {
            $failures.Add("${name}: expected 6 SCRIPT sections, found $($scriptSections.Count)")
        }
    }

    $briefPath = Join-Path $projectRoot 'BRIEF.md'
    $briefText = if (Test-Path -LiteralPath $briefPath -PathType Leaf) { Get-Content -LiteralPath $briefPath -Raw } else { '' }
    if ($null -ne $checkpoint) {
        $requiredBriefFields = [ordered]@{
            part_id        = 'EDU-SB-01'
            checkpoint_in  = [string]$checkpoint.'in'
            checkpoint_out = [string]$checkpoint.out
            paper          = 'A3-landscape'
            projection     = 'third-angle'
        }
        foreach ($field in $requiredBriefFields.GetEnumerator()) {
            $fieldPattern = '(?m)^' + [regex]::Escape($field.Key) + ':\s*["'']?' + [regex]::Escape($field.Value) + '["'']?\s*$'
            if (-not [regex]::IsMatch($briefText, $fieldPattern)) {
                $failures.Add("${name}: BRIEF missing $($field.Key): $($field.Value)")
            }
        }
    }

    $storyboardPath = Join-Path $projectRoot 'STORYBOARD.md'
    $storyboardText = ''
    if (Test-Path -LiteralPath $storyboardPath -PathType Leaf) {
        $storyboardText = Get-Content -LiteralPath $storyboardPath -Raw
        $storyboardSections = [regex]::Matches($storyboardText, '(?m)^## Frame\s+[1-6]\b')
        if ($storyboardSections.Count -ne 6) {
            $failures.Add("${name}: expected 6 STORYBOARD frames, found $($storyboardSections.Count)")
        }
        $storyboardSources = @([regex]::Matches($storyboardText, '(?m)^- src:\s*(\S+)') | ForEach-Object { $_.Groups[1].Value.Replace('\', '/') })
        $storyboardDurations = @([regex]::Matches($storyboardText, '(?m)^- duration:\s*([0-9.]+)s\s*$') | ForEach-Object { [double]$_.Groups[1].Value })
        if ($storyboardSources.Count -ne 6 -or $storyboardDurations.Count -ne 6) {
            $failures.Add("${name}: storyboard must declare 6 src and 6 duration values")
        } elseif ($indexSources.Count -eq 6 -and $indexDurations.Count -eq 6) {
            for ($i = 0; $i -lt 6; $i++) {
                if ($storyboardSources[$i] -ne $indexSources[$i]) {
                    $failures.Add("${name}: storyboard source $($storyboardSources[$i]) differs from index $($indexSources[$i])")
                }
                if ([Math]::Abs($storyboardDurations[$i] - $indexDurations[$i]) -gt 0.001) {
                    $failures.Add("${name}: storyboard duration $($storyboardDurations[$i]) differs from index $($indexDurations[$i])")
                }
            }
        }
    }

    if ($null -ne $checkpoint) {
        foreach ($artifact in @(
            [pscustomobject]@{ Label = 'SCRIPT'; Text = $scriptText },
            [pscustomobject]@{ Label = 'STORYBOARD'; Text = $storyboardText }
        )) {
            foreach ($requiredMarker in @('EDU-SB-01', [string]$checkpoint.'in', [string]$checkpoint.out)) {
                if (-not $artifact.Text.Contains($requiredMarker)) {
                    $failures.Add("${name}: $($artifact.Label) missing continuity marker $requiredMarker")
                }
            }
            if (-not $artifact.Text.Contains('시험') -or -not $artifact.Text.Contains('감점')) {
                $failures.Add("${name}: $($artifact.Label) must include exam and deduction notice")
            }
            foreach ($layerName in @($checkpoint.layersUsed)) {
                if (-not $artifact.Text.Contains([string]$layerName)) {
                    $failures.Add("${name}: $($artifact.Label) missing required layer $layerName")
                }
            }
        }
    }

    $framesRoot = Join-Path $projectRoot 'compositions\frames'
    $frameFiles = if (Test-Path -LiteralPath $framesRoot) { @(Get-ChildItem -LiteralPath $framesRoot -Filter '*.html' -File) } else { @() }
    $motionFiles = if (Test-Path -LiteralPath $framesRoot) { @(Get-ChildItem -LiteralPath $framesRoot -Filter '*.motion.json' -File) } else { @() }

    if ($frameFiles.Count -ne 6) { $failures.Add("${name}: expected 6 frame HTML files, found $($frameFiles.Count)") }
    if ($motionFiles.Count -ne 6) { $failures.Add("${name}: expected 6 motion sidecars, found $($motionFiles.Count)") }

    foreach ($frame in $frameFiles) {
        $sidecar = Join-Path $frame.DirectoryName ($frame.BaseName + '.motion.json')
        if (-not (Test-Path -LiteralPath $sidecar -PathType Leaf)) {
            $failures.Add("${name}: missing sidecar for $($frame.Name)")
        }
    }

    $expectedDemoCount = [int]$expectedDemoCounts[$name]
    $frameTextCombined = ($frameFiles | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw }) -join "`n"
    if (-not $frameTextCombined.Contains('LG EI Text TTF Regular')) {
        $failures.Add("${name}: frame HTML must prefer the installed LG EI Text TTF Regular family")
    }
    if (-not $frameTextCombined.Contains('src:local("LG EI Text TTF Regular")')) {
        $failures.Add("${name}: frame HTML must declare the installed LG EI Text family with local()")
    }
    if (-not $frameTextCombined.Contains('src:local("LG EI Headline TTF Semibold")')) {
        $failures.Add("${name}: frame HTML must declare the installed LG EI Headline family with local()")
    }
    if (-not $frameTextCombined.Contains('LG EI Headline TTF Semibold')) {
        $failures.Add("${name}: frame HTML must prefer the installed LG EI Headline TTF Semibold family")
    }
    $fontFacePattern = '(?is)@font-face\s*\{.*?\}'
    $fontFaceBlocks = [regex]::Matches($frameTextCombined, $fontFacePattern)
    foreach ($fontFaceBlock in $fontFaceBlocks) {
        if ([regex]::IsMatch($fontFaceBlock.Value, '(?is)font-family\s*:\s*[^;]*,')) {
            $failures.Add("${name}: @font-face font-family must be a single family name, not a fallback stack")
            break
        }
    }
    $fontUsageText = [regex]::Replace($frameTextCombined, $fontFacePattern, '')
    $standaloneHeadlinePattern = 'font-family\s*:\s*"LG EI Headline"\s*;'
    if ([regex]::IsMatch($fontUsageText, $standaloneHeadlinePattern)) {
        $failures.Add("${name}: standalone LG EI Headline declaration may fall back; use the exact installed LG EI Headline TTF family chain")
    }
    $lessonRecordingSlots = if ($null -ne $recordingMap) { @($recordingMap.slots | Where-Object { $_.lesson -eq $name }) } else { @() }
    if ($null -ne $recordingMap -and $lessonRecordingSlots.Count -ne $expectedDemoCount) {
        $failures.Add("${name}: recording map count differs from expected $expectedDemoCount")
    }
    foreach ($slot in $lessonRecordingSlots) {
        if ([int]$slot.frame -lt 1 -or [int]$slot.frame -gt 6) {
            $failures.Add("${name}: $($slot.demoId) has invalid frame number")
            continue
        }
        $expectedSource = [string]$slot.src
        if ($indexSources.Count -eq 6 -and $indexSources[[int]$slot.frame - 1] -ne $expectedSource) {
            $failures.Add("${name}: $($slot.demoId) source differs from index frame $($slot.frame)")
        }
        if ($storyboardSources.Count -eq 6 -and $storyboardSources[[int]$slot.frame - 1] -ne $expectedSource) {
            $failures.Add("${name}: $($slot.demoId) source differs from storyboard frame $($slot.frame)")
        }
        $slotSourcePath = Join-Path $projectRoot $expectedSource
        if (-not (Test-Path -LiteralPath $slotSourcePath -PathType Leaf)) {
            $failures.Add("${name}: recording map source missing for $($slot.demoId)")
            continue
        }
        $slotHtml = Get-Content -LiteralPath $slotSourcePath -Raw
        if (-not $slotHtml.Contains([string]$slot.demoId) -or -not $slotHtml.Contains('USER RECORDING')) {
            $failures.Add("${name}: $($slot.demoId) label missing from canonical frame")
        }
        $frameSectionPattern = '(?ms)^## Frame\s+' + [regex]::Escape([string]$slot.frame) + '\b.*?(?=^## Frame\s+\d+\b|\z)'
        $storyFrameSection = [regex]::Match($storyboardText, $frameSectionPattern).Value
        if (-not $storyFrameSection.Contains([string]$slot.demoId)) {
            $failures.Add("${name}: storyboard frame $($slot.frame) missing $($slot.demoId)")
        }
        $scriptSectionPattern = '(?ms)^## Line\s+' + [regex]::Escape([string]$slot.frame) + '\b.*?(?=^## Line\s+\d+\b|\z)'
        $scriptLineSection = [regex]::Match($scriptText, $scriptSectionPattern).Value
        if (-not $scriptLineSection.Contains([string]$slot.demoId)) {
            $failures.Add("${name}: script line $($slot.frame) missing $($slot.demoId)")
        }
        $coursePlanText = Get-Content -LiteralPath (Join-Path $courseRoot 'COURSE_PLAN.md') -Raw
        if (-not $coursePlanText.Contains("F$($slot.frame) · $($slot.demoId)")) {
            $failures.Add("${name}: COURSE_PLAN missing F$($slot.frame) · $($slot.demoId)")
        }
    }
    $recordingSectionTags = @(
        [regex]::Matches($frameTextCombined, '(?is)<section\b[^>]*>') |
            ForEach-Object {
                $tag = $_.Value
                $classValue = Get-HtmlAttribute $tag 'class'
                $classTokens = if ($classValue) { @($classValue -split '\s+') } else { @() }
                if ($classTokens -contains 'recording' -or $classTokens -contains 'recording-stage' -or $classTokens -contains 'record') { $tag }
            }
    )
    if ($recordingSectionTags.Count -ne $expectedDemoCount) {
        $failures.Add("${name}: expected $expectedDemoCount recording sections, found $($recordingSectionTags.Count)")
    }
    foreach ($recordingTag in $recordingSectionTags) {
        if ($recordingTag -match '(?i)\bdata-layout-allow-occlusion\b') {
            $failures.Add("${name}: USER RECORDING section may not waive header occlusion")
        }
    }
    foreach ($recordingRule in [regex]::Matches($frameTextCombined, '(?is)\.(?:recording|recording-stage|record)\s*\{([^}]*)\}')) {
        foreach ($topValue in [regex]::Matches($recordingRule.Groups[1].Value, '(?i)(?:inset|top)\s*:\s*([0-9]+)px')) {
            if ([int]$topValue.Groups[1].Value -lt 216) {
                $failures.Add("${name}: USER RECORDING overlay starts above the 216px header-safe boundary")
            }
        }
    }
    if ($null -ne $checkpoint) {
        $orderedFrames = @($frameFiles | Sort-Object Name)
        if ($orderedFrames.Count -gt 0) {
            $firstFrameText = Get-Content -LiteralPath $orderedFrames[0].FullName -Raw
            $lastFrameText = Get-Content -LiteralPath $orderedFrames[-1].FullName -Raw
            foreach ($requiredStartMarker in @('EDU-SB-01', [string]$checkpoint.'in')) {
                if (-not $firstFrameText.Contains($requiredStartMarker)) {
                    $failures.Add("${name}: first frame missing start-state marker $requiredStartMarker")
                }
            }
            foreach ($requiredEndMarker in @('EDU-SB-01', [string]$checkpoint.out, 'A3', '시험', '감점')) {
                if (-not $lastFrameText.Contains($requiredEndMarker)) {
                    $failures.Add("${name}: last frame missing release-gate marker $requiredEndMarker")
                }
            }
        }
        foreach ($requiredMarker in @('EDU-SB-01', [string]$checkpoint.'in', [string]$checkpoint.out)) {
            if (-not $frameTextCombined.Contains($requiredMarker)) {
                $failures.Add("${name}: composition HTML missing continuity marker $requiredMarker")
            }
        }
        foreach ($layerName in @($checkpoint.layersUsed)) {
            if (-not $frameTextCombined.Contains([string]$layerName)) {
                $failures.Add("${name}: composition HTML missing required layer $layerName")
            }
        }
        if (-not $frameTextCombined.Contains('시험') -or -not $frameTextCombined.Contains('감점')) {
            $failures.Add("${name}: composition HTML must include exam and deduction notice")
        }
    }
    $demoCounts = [ordered]@{
        SCRIPT     = (Get-DemoIds $scriptText).Count
        STORYBOARD = (Get-DemoIds $storyboardText).Count
        HTML       = (Get-DemoIds $frameTextCombined).Count
    }
    foreach ($demoEntry in $demoCounts.GetEnumerator()) {
        if ($demoEntry.Value -ne $expectedDemoCount) {
            $failures.Add("${name}: expected $expectedDemoCount USER RECORDING cues in $($demoEntry.Key), found $($demoEntry.Value)")
        }
    }

    $compositionFiles = @($frameFiles)
    if (Test-Path -LiteralPath $indexPath -PathType Leaf) { $compositionFiles += Get-Item -LiteralPath $indexPath }
    $usedColors = @(
        foreach ($file in $compositionFiles) {
            [regex]::Matches((Get-Content -LiteralPath $file.FullName -Raw), '#[0-9A-Fa-f]{6}') | ForEach-Object { $_.Value.ToUpperInvariant() }
        }
    ) | Sort-Object -Unique

    foreach ($color in $usedColors) {
        if ($allowedColors -notcontains $color) {
            $failures.Add("${name}: color outside frame.md palette: $color")
        }
    }

    $publicTextFiles = @(
        Get-ChildItem -LiteralPath $projectRoot -Recurse -File -Include '*.html', '*.md', '*.json' |
            Where-Object {
                $_.FullName -notmatch '[\\/](node_modules|snapshots|\.hyperframes|\.thumbnails|private)[\\/]'
            }
    )
    foreach ($file in $publicTextFiles) {
        $match = [regex]::Match((Get-Content -LiteralPath $file.FullName -Raw), $forbiddenContent)
        if ($match.Success) {
            $normalizedRepoRoot = [IO.Path]::GetFullPath($repoRoot).TrimEnd([char[]]@('\', '/'))
            $normalizedFilePath = [IO.Path]::GetFullPath($file.FullName)
            if ($normalizedFilePath.StartsWith($normalizedRepoRoot, [StringComparison]::OrdinalIgnoreCase)) {
                $relative = $normalizedFilePath.Substring($normalizedRepoRoot.Length).TrimStart([char[]]@('\', '/'))
            } else {
                $relative = $normalizedFilePath
            }
            $failures.Add("${name}: forbidden private-source marker '$($match.Value)' in $relative")
        }
    }

    $checkStatus = 'not-run'
    if ($RunHyperFramesChecks) {
        Push-Location $projectRoot
        try {
            & npm run check
            if ($LASTEXITCODE -ne 0) {
                $checkStatus = 'failed'
                $failures.Add("${name}: npm run check failed")
            } else {
                $checkStatus = 'passed'
            }
        } finally {
            Pop-Location
        }
    }

    $results.Add([PSCustomObject]@{
        Lesson   = $name
        Duration = if ($null -eq $actualDuration) { 'missing' } else { $actualDuration }
        Frames   = $frameFiles.Count
        Motion   = $motionFiles.Count
        Check    = $checkStatus
    })
}

$results | Format-Table -AutoSize

if ($failures.Count -gt 0) {
    foreach ($failure in $failures) {
        [Console]::Error.WriteLine("FAILED: $failure")
    }
    exit 1
}

Write-Output "Course project guard passed for $($expectedDurations.Count) lessons."
