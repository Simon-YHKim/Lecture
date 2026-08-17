[CmdletBinding()]
param(
    [string]$RepoRoot,
    [string]$OutputPath,
    [switch]$HyperFramesChecksPassed
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $RepoRoot 'docs\autocad-technician\reports\AutoCAD_Technician_All_Lessons_Completion_260812.html'
}

$courseRoot = Join-Path $RepoRoot 'projects\autocad-technician'
$continuityPath = Join-Path $courseRoot 'course-continuity.json'
$continuity = Get-Content -LiteralPath $continuityPath -Raw -Encoding UTF8 | ConvertFrom-Json
$outputDirectory = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

$kstNow = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId((Get-Date), 'Korea Standard Time')
$timestamp = $kstNow.ToString('yy.MM.dd HH:mm:ss')

$lessons = @(
    [pscustomobject]@{ Number = 1;  Module = 1; Slug = 'lesson-01-drawing-language';     TitleKo = '시험 도면을 제작 순서로 읽기';       TitleEn = 'Reading the exam input as a production plan'; Duration = 600;  FocusKo = '3D 모델·치수·지시사항에서 형상 ID와 제작 순서를 추출합니다.'; FocusEn = 'Extract feature IDs and the production sequence from the 3D model, dimensions, and instructions.' },
    [pscustomobject]@{ Number = 2;  Module = 1; Slug = 'lesson-02-work-environment';     TitleKo = 'ISO metric 환경과 A3 도면틀 만들기';     TitleEn = 'Build the ISO metric A3 drawing frame'; Duration = 720;  FocusKo = 'acadiso.dwt, mm, A3 420×297, 10 mm 외관선과 200×30 표제란을 준비합니다.'; FocusEn = 'Set up acadiso.dwt, millimeters, A3 420×297, the 10 mm border, and 200×30 title block.' },
    [pscustomobject]@{ Number = 3;  Module = 2; Slug = 'lesson-03-lines-polylines';      TitleKo = '정면도 기준 외곽 만들기';             TitleEn = 'Build the front-view base profile'; Duration = 720;  FocusKo = '누적 파일에 80×50 본체와 러그 직선 골격을 1:1로 작성합니다.'; FocusEn = 'Draw the 80×50 body and lug skeleton at 1:1 in the cumulative file.' },
    [pscustomobject]@{ Number = 4;  Module = 2; Slug = 'lesson-04-curves-offset';        TitleKo = '원·호·포켓·간격 추가하기';         TitleEn = 'Adding circles, arcs, pockets, and offsets'; Duration = 720;  FocusKo = '같은 정면도에 Ø20, AF30, 22×8 장공과 좌측 국소 5 mm Offset 포켓을 추가합니다.'; FocusEn = 'Add Ø20, AF30, the 22×8 slot, and the local left-side 5 mm offset pocket to the same front view.' },
    [pscustomobject]@{ Number = 5;  Module = 2; Slug = 'lesson-05-orthographic-reading'; TitleKo = '제3각법으로 평면도·우측면도 투상하기'; TitleEn = 'Projecting top and right views in third angle'; Duration = 780;  FocusKo = '정면도 위에 평면도, 오른쪽에 우측면도를 배치하고 숨은선과 중심선을 갱신합니다.'; FocusEn = 'Place the top view above and the right view to the right, then update hidden and center lines.' },
    [pscustomobject]@{ Number = 6;  Module = 3; Slug = 'lesson-06-placement-repetition'; TitleKo = '반복 특징 배치하기';                 TitleEn = 'Placing repeated features'; Duration = 780;  FocusKo = '검증된 Seed를 복사·대칭·배열하고 세 뷰의 선 표현을 동시에 갱신합니다.'; FocusEn = 'Copy, mirror, and array the verified seed while updating all three views.' },
    [pscustomobject]@{ Number = 7;  Module = 3; Slug = 'lesson-07-object-editing';       TitleKo = '형상 마감하기';                       TitleEn = 'Finishing the geometry'; Duration = 855;  FocusKo = 'CONSTRUCTION·HIDDEN 투영 범위를 정리하고 R5·C5를 적용하며 SCALE은 참조 형상에만 사용합니다.'; FocusEn = 'Clean projected CONSTRUCTION and HIDDEN extents, apply R5 and C5, and reserve SCALE for reference geometry only.' },
    [pscustomobject]@{ Number = 8;  Module = 3; Slug = 'lesson-08-representation-reuse'; TitleKo = '단면·재사용·표제란 정리하기';           TitleEn = 'Organizing sections, reuse, and title data'; Duration = 660;  FocusKo = 'A–A 단면, Hatch, Block, Group과 표제란을 같은 도면에 축적합니다.'; FocusEn = 'Add the A–A section, Hatch, Block, Group, and title information to the same drawing.' },
    [pscustomobject]@{ Number = 9;  Module = 4; Slug = 'lesson-09-dimensioning';         TitleKo = '제작·검사용 치수와 축척 확정하기';       TitleEn = 'Finalizing production dimensions and scale'; Duration = 840; FocusKo = 'DIM Layer로 전체·위치·지름·반지름·각도 치수를 배치하고 축척을 검수합니다.'; FocusEn = 'Place overall, location, diameter, radius, and angle dimensions on DIM and verify scale.' },
    [pscustomobject]@{ Number = 10; Module = 4; Slug = 'lesson-10-final-bracket';        TitleKo = '제한시간 모의시험과 최종 출도';             TitleEn = 'Timed mock exam and final release'; Duration = 1140; FocusKo = '새로 그리지 않고 L09 누적 파일을 일곱 개 게이트로 검사·수정·저장합니다.'; FocusEn = 'Audit, correct, and save the L09 cumulative file through seven timed release gates.' }
)

function Get-DurationLabel([int]$Seconds) {
    return ('{0}:{1:00}' -f [Math]::Floor($Seconds / 60), ($Seconds % 60))
}

function Convert-ImageToDataUri([string]$Path) {
    if (-not $Path -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }

    $extension = [IO.Path]::GetExtension($Path).ToLowerInvariant()
    $mime = switch ($extension) {
        '.png'  { 'image/png' }
        '.webp' { 'image/webp' }
        default { 'image/jpeg' }
    }
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($Path))
    return "data:$mime;base64,$base64"
}

function Find-ContactSheet([string]$ProjectRoot) {
    $preferred = @(
        (Join-Path $ProjectRoot 'snapshots\final-approval\contact-sheet.jpg'),
        (Join-Path $ProjectRoot 'snapshots\final-look\contact-sheet.jpg'),
        (Join-Path $ProjectRoot 'snapshots\course-review\contact-sheet.jpg')
    )
    foreach ($candidate in $preferred) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return $candidate
        }
    }

    $fallback = Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'snapshots') -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '^contact-sheet\.(jpg|jpeg|png|webp)$' } |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($fallback) { return $fallback.FullName }
    return $null
}

$lessonCards = [System.Text.StringBuilder]::new()
$chartBars = [System.Text.StringBuilder]::new()
$verifiedCount = 0
$sceneCount = 0
$totalDuration = 0

foreach ($lesson in $lessons) {
    $projectRoot = Join-Path $courseRoot $lesson.Slug
    $checkpoint = @($continuity.checkpoints | Where-Object { $_.lesson -eq $lesson.Slug }) | Select-Object -First 1
    $checkpointLabel = "$($checkpoint.'in') → $($checkpoint.out)"
    $layerLabel = @($checkpoint.layersUsed) -join ' · '
    $framesRoot = Join-Path $projectRoot 'compositions\frames'
    $frameCount = @(Get-ChildItem -LiteralPath $framesRoot -Filter '*.html' -File -ErrorAction SilentlyContinue).Count
    $motionCount = @(Get-ChildItem -LiteralPath $framesRoot -Filter '*.motion.json' -File -ErrorAction SilentlyContinue).Count
    $docsReady = @('BRIEF.md', 'SCRIPT.md', 'STORYBOARD.md', 'frame.md', 'index.html') |
        ForEach-Object { Test-Path -LiteralPath (Join-Path $projectRoot $_) -PathType Leaf }
    $structureReady = ($frameCount -eq 6 -and $motionCount -eq 6 -and ($docsReady -notcontains $false))
    $isVerified = ($structureReady -and $HyperFramesChecksPassed)
    if ($isVerified) { $verifiedCount++ }
    $sceneCount += $frameCount
    $totalDuration += $lesson.Duration

    $sheetPath = Find-ContactSheet $projectRoot
    $sheetUri = Convert-ImageToDataUri $sheetPath
    $imageMarkup = if ($sheetUri) {
        '<img class="contact-sheet" src="' + $sheetUri + '" alt="Lesson ' + $lesson.Number + ' storyboard contact sheet">'
    } else {
        '<div class="contact-sheet missing" role="img" aria-label="Contact sheet unavailable"><span>CONTACT SHEET<br>NOT AVAILABLE</span></div>'
    }

    $statusClass = if ($isVerified) { 'pass' } else { 'pending' }
    $statusKo = if ($isVerified) { '검증 통과' } elseif ($structureReady) { '구조 완료' } else { '확인 필요' }
    $statusEn = if ($isVerified) { 'Verified' } elseif ($structureReady) { 'Structure ready' } else { 'Needs review' }
    $durationLabel = Get-DurationLabel $lesson.Duration

    [void]$lessonCards.AppendLine(@"
      <article class="lesson-card" id="lesson-$($lesson.Number)">
        <header class="lesson-head">
          <div class="lesson-no">L$('{0:00}' -f $lesson.Number)</div>
          <div>
            <p class="eyebrow">MODULE $($lesson.Module) · $durationLabel</p>
            <h3 data-lang="ko">$($lesson.TitleKo)</h3>
            <h3 data-lang="en">$($lesson.TitleEn)</h3>
          </div>
          <span class="status $statusClass"><span data-lang="ko">$statusKo</span><span data-lang="en">$statusEn</span></span>
        </header>
        $imageMarkup
        <div class="lesson-summary">
          <p data-lang="ko" data-mode="easy">$($lesson.FocusKo)</p>
          <p data-lang="en" data-mode="easy">$($lesson.FocusEn)</p>
          <p data-lang="ko" data-mode="expert"><code>$checkpointLabel</code><br>Layer: $layerLabel<br>6개 composition과 6개 motion sidecar를 $($lesson.Duration)초 root timeline에 조립했습니다.</p>
          <p data-lang="en" data-mode="expert"><code>$checkpointLabel</code><br>Layers: $layerLabel<br>Six compositions and six motion sidecars are assembled on a $($lesson.Duration)-second root timeline.</p>
        </div>
        <details>
          <summary><span data-lang="ko">[자세히] 산출물과 다음 단계</span><span data-lang="en">[Details] Deliverables and next step</span></summary>
          <div class="detail-grid">
            <div><strong data-lang="ko">구현</strong><strong data-lang="en">Build</strong><p><code>$($lesson.Slug)</code><br>BRIEF · SCRIPT · STORYBOARD · HTML × $frameCount · MOTION × $motionCount</p></div>
            <div data-mode="easy"><strong data-lang="ko">다음</strong><strong data-lang="en">Next</strong><p data-lang="ko">화면 구성을 확인한 뒤, 촬영 안내서에 맞춰 AutoCAD 화면과 목소리를 녹음합니다.</p><p data-lang="en">Approve the visuals, then record the AutoCAD screen and narration using the recording guide.</p></div>
            <div data-mode="expert"><strong data-lang="ko">통합 게이트</strong><strong data-lang="en">Integration gate</strong><p data-lang="ko">실제 미디어는 비공개 경로에서만 연결하고, Whisper 타임코드 검증 후 최종 렌더를 허용합니다.</p><p data-lang="en">Real media remains private; final rendering is allowed only after Whisper timing validation.</p></div>
          </div>
        </details>
      </article>
"@)

    $barWidth = [Math]::Round(($lesson.Duration / 1140) * 520, 0)
    $barY = 20 + (($lesson.Number - 1) * 32)
    [void]$chartBars.AppendLine("<text x='0' y='$($barY + 13)' class='chart-label'>L$('{0:00}' -f $lesson.Number)</text><rect x='46' y='$barY' width='$barWidth' height='18' class='bar'/><text x='$($barWidth + 56)' y='$($barY + 13)' class='chart-value'>$durationLabel</text>")
}

$durationTotalLabel = ('{0}:{1:00}:{2:00}' -f [Math]::Floor($totalDuration / 3600), [Math]::Floor(($totalDuration % 3600) / 60), ($totalDuration % 60))
$completionPercent = [Math]::Round(($verifiedCount / $lessons.Count) * 100)
$circumference = 301.6
$dashOffset = [Math]::Round($circumference * (1 - ($verifiedCount / $lessons.Count)), 1)

$html = @"
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AutoCAD Technician · All Lessons Completion Review</title>
  <style>
    :root{--accent:#c7004c;--text:#111;--muted:#666;--paper:#f5f5f3;--line:#a4a3a4;--white:#fff;color-scheme:light dark}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--text);font-family:"Segoe UI","Malgun Gothic",Arial,sans-serif;line-height:1.55}
    body.lang-ko [data-lang="en"],body.lang-en [data-lang="ko"],body.mode-easy [data-mode="expert"],body.mode-expert [data-mode="easy"]{display:none!important}
    .page{max-width:1460px;margin:auto;padding:36px}.topbar{display:flex;justify-content:space-between;gap:24px;align-items:center;border-top:8px solid var(--accent);padding:18px 0 30px}
    .brand{font-weight:800;letter-spacing:.08em}.controls{display:flex;gap:8px;flex-wrap:wrap}button{border:1px solid var(--text);background:transparent;color:inherit;padding:9px 14px;font:inherit;font-weight:700;cursor:pointer}button[aria-pressed="true"]{background:var(--text);color:var(--paper)}button:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
    .hero{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(300px,.7fr);gap:28px;align-items:end;padding:42px 0 28px;border-bottom:2px solid var(--text)}.kicker,.eyebrow{font-size:.78rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}h1{font-size:clamp(2.5rem,6vw,6rem);line-height:.94;letter-spacing:-.055em;margin:.15em 0}.lede{max-width:760px;font-size:1.2rem;color:var(--muted)}
    .hero-status{display:flex;gap:24px;align-items:center;justify-content:flex-end}.donut{width:150px;height:150px}.donut-bg{fill:none;stroke:var(--line);stroke-width:10}.donut-value{fill:none;stroke:var(--accent);stroke-width:10;stroke-linecap:square;transform:rotate(-90deg);transform-origin:60px 60px}.donut-text{font-weight:800;font-size:24px;fill:var(--text)}
    .summary-grid{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:2px solid var(--text)}.metric{padding:24px 18px;border-right:1px solid var(--line)}.metric:last-child{border-right:0}.metric b{display:block;font-size:2.2rem;line-height:1}.metric span{color:var(--muted);font-size:.9rem}
    .section{padding:48px 0}.section-title{display:flex;justify-content:space-between;gap:30px;align-items:end;margin-bottom:22px}.section-title h2{font-size:clamp(1.8rem,4vw,3.4rem);line-height:1;margin:0}.section-title p{max-width:620px;margin:0;color:var(--muted)}
    .chart-wrap{background:var(--white);border-top:4px solid var(--accent);padding:24px;overflow:auto}.duration-chart{display:block;width:100%;min-width:720px;height:350px}.bar{fill:var(--accent)}.chart-label,.chart-value{fill:var(--text);font-family:inherit;font-size:13px;font-weight:700}
    .spec-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(300px,.85fr);gap:18px}.paper-card,.spec-card{background:var(--white);border-top:4px solid var(--accent);padding:24px}.paper-svg{display:block;width:100%;height:auto;max-height:390px}.paper-line{fill:none;stroke:var(--text);stroke-width:2}.paper-accent{fill:none;stroke:var(--accent);stroke-width:3}.paper-label{fill:var(--text);font:700 15px inherit}.spec-list{display:grid;gap:0}.spec-row{display:grid;grid-template-columns:120px 1fr;gap:16px;padding:13px 0;border-bottom:1px solid var(--line)}.spec-row b{color:var(--accent)}.checkpoint-flow{display:flex;gap:6px;align-items:center;overflow:auto;padding:18px 0}.checkpoint-flow span{white-space:nowrap;border:1px solid var(--line);padding:8px 10px;font:700 .78rem Consolas,monospace}.checkpoint-flow i{color:var(--accent);font-style:normal;font-weight:900}
    .lessons{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.lesson-card{background:var(--white);border-top:5px solid var(--text);padding:22px}.lesson-head{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start}.lesson-no{font-size:1.7rem;font-weight:900;color:var(--accent)}h3{font-size:1.55rem;line-height:1.15;margin:.15em 0}.status{font-size:.78rem;font-weight:800;padding:6px 8px;border:1px solid currentColor}.status.pass{color:var(--accent)}.status.pending{color:var(--muted)}
    .contact-sheet{display:block;width:100%;aspect-ratio:16/5.2;object-fit:cover;margin:20px 0;border:1px solid var(--line);background:var(--paper)}.contact-sheet.missing{display:grid;place-items:center;text-align:center;color:var(--muted);font-weight:800;letter-spacing:.12em}.lesson-summary{min-height:72px;color:var(--muted)}details{border-top:1px solid var(--line);padding-top:14px}summary{cursor:pointer;font-weight:800;color:var(--accent)}.detail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:14px}.detail-grid p{font-size:.92rem;color:var(--muted)}code{font-family:Consolas,monospace;font-size:.84em;overflow-wrap:anywhere}
    .gate-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.gate{background:var(--white);border-left:5px solid var(--accent);padding:22px}.gate h3{font-size:1.18rem}.gate ul{padding-left:1.2em}.gate li{margin:.45em 0}.risk{border-left-color:var(--text)}
    .privacy{background:var(--text);color:var(--paper);padding:30px}.privacy strong{color:#fff}.privacy .accent{color:#ff4f91}.footer{display:flex;justify-content:space-between;gap:30px;padding:28px 0;color:var(--muted);font-size:.86rem}
    @media(max-width:900px){.hero,.gate-grid,.spec-grid{grid-template-columns:1fr}.hero-status{justify-content:flex-start}.summary-grid{grid-template-columns:repeat(2,1fr)}.metric:nth-child(2){border-right:0}.lessons{grid-template-columns:1fr}.page{padding:24px}}
    @media(max-width:560px){.topbar,.section-title,.footer{align-items:flex-start;flex-direction:column}.summary-grid{grid-template-columns:1fr}.metric{border-right:0;border-bottom:1px solid var(--line)}.lesson-head{grid-template-columns:auto 1fr}.status{grid-column:2}.detail-grid{grid-template-columns:1fr}.page{padding:18px}}
    @media(prefers-color-scheme:dark){:root{--text:#f5f5f3;--paper:#111;--white:#1b1b1b;--muted:#a4a3a4;--line:#666}.privacy{background:#f5f5f3;color:#111}.privacy strong{color:#111}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  </style>
</head>
<body class="lang-ko mode-easy">
  <main class="page">
    <nav class="topbar" aria-label="Report controls">
      <div class="brand">AUTOCAD TECHNICIAN · COURSE REVIEW</div>
      <div class="controls">
        <button type="button" data-control="lang" data-value="ko" aria-pressed="true" aria-label="한국어로 보기">한국어</button>
        <button type="button" data-control="lang" data-value="en" aria-pressed="false" aria-label="View in English">EN</button>
        <button type="button" data-control="mode" data-value="easy" aria-pressed="true" aria-label="쉬운 설명 보기">쉬운 설명</button>
        <button type="button" data-control="mode" data-value="expert" aria-pressed="false" aria-label="전문가 설명 보기">전문가</button>
      </div>
    </nav>

    <section class="hero">
      <div>
        <p class="kicker">IMPLEMENTATION COMPLETION · 2026-08-12</p>
        <h1 data-lang="ko">10개 강의,<br>하나의 도면.</h1>
        <h1 data-lang="en">Ten lessons.<br>One drawing.</h1>
        <p class="lede" data-lang="ko" data-mode="easy"><strong>EDU-SB-01 센서 장착 브래킷</strong> 하나를 문제 해독부터 제3각법, 치수, 제한시간 최종 검수까지 실제 제작 순서로 완성합니다.</p>
        <p class="lede" data-lang="en" data-mode="easy">One <strong>EDU-SB-01 sensor mounting bracket</strong> now progresses from exam-input analysis through third-angle projection, dimensions, and timed final release.</p>
        <p class="lede" data-lang="ko" data-mode="expert">10개 단계는 <code>checkpoint_out(N) = checkpoint_in(N+1)</code>로 연결됩니다. 각 단계는 6개 HyperFrames composition, motion sidecar, 정확한 root duration, 비공개 실습 슬롯을 유지합니다.</p>
        <p class="lede" data-lang="en" data-mode="expert">Ten stages satisfy <code>checkpoint_out(N) = checkpoint_in(N+1)</code>. Every stage keeps six HyperFrames compositions, motion sidecars, exact timing, and private practice slots.</p>
      </div>
      <div class="hero-status" aria-label="Completion $completionPercent percent">
        <svg class="donut" viewBox="0 0 120 120" role="img" aria-label="$verifiedCount of 10 lessons structurally ready">
          <circle class="donut-bg" cx="60" cy="60" r="48"/>
          <circle class="donut-value" cx="60" cy="60" r="48" stroke-dasharray="$circumference" stroke-dashoffset="$dashOffset"/>
          <text class="donut-text" x="60" y="67" text-anchor="middle">$verifiedCount/10</text>
        </svg>
        <div><p class="eyebrow">STRUCTURE</p><strong data-lang="ko">구현 게이트</strong><strong data-lang="en">Build gate</strong><p>$timestamp KST</p></div>
      </div>
    </section>

    <section class="summary-grid" aria-label="Course summary">
      <div class="metric"><b>$($lessons.Count)</b><span data-lang="ko">전체 강의</span><span data-lang="en">lessons</span></div>
      <div class="metric"><b>$sceneCount</b><span data-lang="ko">구현 장면</span><span data-lang="en">implemented scenes</span></div>
      <div class="metric"><b>$durationTotalLabel</b><span data-lang="ko">목표 러닝타임</span><span data-lang="en">target runtime</span></div>
      <div class="metric"><b>8</b><span data-lang="ko">실제 활용 Layer</span><span data-lang="en">layers used in practice</span></div>
    </section>

    <section class="section">
      <div class="section-title"><h2 data-lang="ko">정본 형상 계약</h2><h2 data-lang="en">Canonical geometry contract</h2><p data-lang="ko">모든 장면은 <code>master-part-geometry.json</code>의 동일 좌표를 사용하며 이미 완성한 특징을 차시마다 바꾸지 않습니다.</p><p data-lang="en">Every scene uses the same coordinates from <code>master-part-geometry.json</code>; completed features cannot change between lessons.</p></div>
      <div class="gate-grid">
        <article class="gate"><h3>EDU-SB-01</h3><ul><li>80×50×8 · 중앙 Ø20 · AF30</li><li>2×Ø6: (15,8), (65,8)</li><li>3×Ø4 · PCD Ø36 · 시작각 30°</li><li>중심: (55.588,31), (24.412,31), (40,4)</li><li>장공 중심 (40,42) · 22×8 · 양단 중심 (33,42)/(47,42)</li><li>우측 경사 45° · nominal (68,35)→(80,23)</li><li>좌측 국소 포켓 (5,15)–(19,29) · 깊이 2</li><li>A–A X=40 · Ø4/AF30/Ø20/장공 네 빈 영역</li></ul></article>
        <article class="gate"><h3 data-lang="ko">자동 보호</h3><h3 data-lang="en">Automated protection</h3><ul data-lang="ko"><li>특징 최소 간격 1 mm 검사</li><li>FRONT 80×50 · TOP 80×8 · RIGHT 8×50 검사</li><li>A–A 네 빈 영역과 29개 녹화 슬롯 계약</li><li>녹화 대체 화면 top 216 px 이상 안전 경계</li></ul><ul data-lang="en"><li>One-millimeter minimum feature clearance</li><li>FRONT 80×50, TOP 80×8, RIGHT 8×50 contract</li><li>Four A–A voids and contracts for 29 recording slots</li><li>Recording overlays begin at or below the 216-pixel top-safe boundary</li></ul></article>
      </div>
    </section>

    <section class="section">
      <div class="section-title"><h2 data-lang="ko">제작 기준선</h2><h2 data-lang="en">Production baseline</h2><p data-lang="ko">사용자 캡처의 수치는 보존하되, 297×420 mm는 ISO A3이므로 가로 420×297 mm로 정정했습니다.</p><p data-lang="en">The dimensions from the supplied capture are preserved, while 297×420 mm is correctly identified as ISO A3 and used as 420×297 mm landscape.</p></div>
      <div class="spec-grid">
        <article class="paper-card">
          <svg class="paper-svg" viewBox="0 0 720 510" role="img" aria-labelledby="paperTitle paperDesc"><title id="paperTitle">ISO A3 landscape training frame</title><desc id="paperDesc">A3 420 by 297 millimeter sheet with a ten millimeter inset border and a two hundred by thirty millimeter title block.</desc><rect x="42" y="36" width="636" height="450" class="paper-line"/><rect x="58" y="52" width="604" height="418" class="paper-accent"/><rect x="360" y="425" width="302" height="45" class="paper-line"/><line x1="511" y1="425" x2="511" y2="470" class="paper-line"/><text x="360" y="24" text-anchor="middle" class="paper-label">420 mm · ISO A3 LANDSCAPE</text><text x="25" y="270" text-anchor="middle" transform="rotate(-90 25 270)" class="paper-label">297 mm</text><text x="284" y="76" class="paper-label">10 mm INSET BORDER</text><text x="435" y="452" text-anchor="middle" class="paper-label">사번 100</text><text x="586" y="452" text-anchor="middle" class="paper-label">이름 100</text></svg>
        </article>
        <article class="spec-card">
          <div class="spec-list">
            <div class="spec-row"><b>START</b><span><code>acadiso.dwt</code> 또는 시험 제공 ISO metric 파일</span></div>
            <div class="spec-row"><b>MODEL</b><span>millimeter · Model Space 1:1</span></div>
            <div class="spec-row"><b>PROJECTION</b><span>과정 지시: 제3각법 · 실제 시험 문제지 우선</span></div>
            <div class="spec-row"><b>CORE</b><span>OUTLINE · CENTER · HIDDEN · DIM</span></div>
            <div class="spec-row"><b>SUPPORT</b><span>BORDER · TITLE · HATCH · CONSTRUCTION</span></div>
            <div class="spec-row"><b>EXAM</b><span>3D 모델 + 치수 + 지시사항 · 제한시간 · 감점 게이트</span></div>
          </div>
        </article>
      </div>
      <div class="checkpoint-flow" aria-label="Cumulative checkpoint flow"><span>REFERENCE</span><i>→</i><span>L01 MAP</span><i>→</i><span>L02 SETUP</span><i>→</i><span>L03 PROFILE</span><i>→</i><span>L04 FEATURES</span><i>→</i><span>L05 VIEWS</span><i>→</i><span>L06 PATTERN</span><i>→</i><span>L07 FINAL</span><i>→</i><span>L08 REPRESENTED</span><i>→</i><span>L09 CANDIDATE</span><i>→</i><span>L10 RELEASE</span></div>
    </section>

    <section class="section">
      <div class="section-title"><h2 data-lang="ko">러닝타임 설계</h2><h2 data-lang="en">Runtime design</h2><p data-lang="ko">짧은 개념 강의부터 19분 최종 실습까지, 난이도와 실습량에 맞춰 배분했습니다.</p><p data-lang="en">Durations scale from compact concepts to the 19-minute final practice.</p></div>
      <div class="chart-wrap"><svg class="duration-chart" viewBox="0 0 700 350" role="img" aria-label="Lesson runtime bar chart">$($chartBars.ToString())</svg></div>
    </section>

    <section class="section">
      <div class="section-title"><h2 data-lang="ko">강의별 화면 리뷰</h2><h2 data-lang="en">Lesson-by-lesson review</h2><p data-lang="ko">각 이미지는 장면 중간 프레임을 묶은 연락판입니다. 움직임은 Studio에서 직접 확인합니다.</p><p data-lang="en">Each image is a contact sheet of scene midpoints. Review motion directly in Studio.</p></div>
      <div class="lessons">$($lessonCards.ToString())</div>
    </section>

    <section class="section">
      <div class="section-title"><h2 data-lang="ko">완료와 남은 게이트</h2><h2 data-lang="en">Completed and remaining gates</h2></div>
      <div class="gate-grid">
        <article class="gate"><h3 data-lang="ko">완료된 범위</h3><h3 data-lang="en">Completed scope</h3><ul data-lang="ko"><li><code>EDU-SB-01</code> 하나로 연결된 10개 제작 단계</li><li>10개 BRIEF·SCRIPT·STORYBOARD와 60개 HyperFrames 장면</li><li>A3 420×297, 10 mm 외관선, 200×30 표제란 장면</li><li>OUTLINE·CENTER·HIDDEN·DIM을 포함한 8개 Layer 실습</li><li>제3각법·축척·표제란·Layer·선종류 감점 게이트</li><li>실제 AutoCAD 영상용 USER RECORDING 슬롯 29개</li><li>HyperFrames·연속성·비공개 자료 가드 자동 검사</li></ul><ul data-lang="en"><li>Ten production stages connected by one <code>EDU-SB-01</code> drawing</li><li>Ten BRIEF, SCRIPT, and STORYBOARD sets plus sixty HyperFrames scenes</li><li>A3 420×297, 10 mm border, and 200×30 title-block scenes</li><li>Eight practiced layers including OUTLINE, CENTER, HIDDEN, and DIM</li><li>Third-angle, scale, title, layer, and linetype deduction gates</li><li>Twenty-nine USER RECORDING slots for real AutoCAD footage</li><li>Automated HyperFrames, continuity, and privacy guards</li></ul></article>
        <article class="gate risk"><h3 data-lang="ko">렌더 전 남은 일</h3><h3 data-lang="en">Remaining before render</h3><ul data-lang="ko"><li>사용자의 Studio 화면 승인</li><li>교육용 AutoCAD 화면 녹화</li><li>최종 대본 나레이션 녹음</li><li>Whisper 타임코드 생성·문맥 보정</li><li>영상·음성 동기화 후 최종 렌더 검증</li></ul><ul data-lang="en"><li>User approval in Studio</li><li>Sanitized AutoCAD screen recordings</li><li>Final narration recording</li><li>Whisper timestamps and contextual correction</li><li>Final sync and render verification</li></ul></article>
      </div>
    </section>

    <section class="privacy">
      <p class="eyebrow accent">CONFIDENTIALITY BOUNDARY</p>
      <h2 data-lang="ko">PPT와 실제 촬영본은 공개 Git에 들어가지 않습니다.</h2><h2 data-lang="en">PPT sources and real recordings never enter public Git.</h2>
      <p data-lang="ko" data-mode="easy">이 공개 리뷰에는 <strong>검토된 합성 강의 화면</strong>만 포함합니다. PPT/PPTX, 슬라이드 직접 파생물, 실제 촬영본과 폰트 바이너리는 포함하지 않습니다.</p>
      <p data-lang="en" data-mode="easy">This public review contains only <strong>reviewed synthetic course frames</strong>. PPT/PPTX files, direct slide derivatives, real recordings, and font binaries are excluded.</p>
      <p data-lang="ko" data-mode="expert">정확한 파일명 허용목록과 내용 검사를 통과한 QA 스냅샷만 공개합니다. 프레젠테이션 원본·직접 파생물·녹화·폰트·도구 캐시는 계속 차단합니다.</p>
      <p data-lang="en" data-mode="expert">Only QA snapshots that pass exact-path allowlisting and content review are public. Presentation sources and derivatives, recordings, fonts, and tool caches remain blocked.</p>
    </section>

    <footer class="footer"><span>AutoCAD Technician Video Course · Public completion review</span><span>Generated $timestamp KST · Reviewed public artifact</span></footer>
  </main>
  <script>
    const body=document.body,buttons=[...document.querySelectorAll('button[data-control]')];
    function setValue(kind,value){body.className=body.className.replace(new RegExp(kind+'-(ko|en|easy|expert)','g'),'').trim()+' '+kind+'-'+value;buttons.filter(b=>b.dataset.control===kind).forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.value===value)));if(kind==='lang')document.documentElement.lang=value;}
    buttons.forEach(button=>button.addEventListener('click',()=>setValue(button.dataset.control,button.dataset.value)));
  </script>
</body>
</html>
"@

[IO.File]::WriteAllText($OutputPath, $html, [Text.UTF8Encoding]::new($false))
Write-Output "Completion report written: $OutputPath"
