---
format: 1920x1080
duration: 12m00s
message: "L03의 EDU-SB-01 외곽에 주요 원·호·포켓·간격 특징을 누적한다."
arc: "L03 체크포인트 → Ø20·러그·장공 Seed → AF30 → 5 mm OFFSET → 통합 검수 → L04 저장"
audience: "L03_BASE_PROFILE까지 완성한 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L03_BASE_PROFILE
checkpoint_out: L04_PRIMARY_FEATURES
paper: A3-landscape
projection: third-angle
layers_used: [OUTLINE, CENTER, CONSTRUCTION]
---

## Frame 1 — L03 외곽에서 주요 특징을 시작한다
- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 30s
- transition_in: cut
- scene: EDU-SB-01과 `L03_BASE_PROFILE → L04_PRIMARY_FEATURES`, OUTLINE·CENTER·CONSTRUCTION, 네 누적 특징을 소개한다.
- voiceover: "새 예제가 아니라 L03에서 만든 같은 부품에 주요 특징을 더합니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

입력 체크포인트는 회색, 이번 차시 추가 형상은 마젠타, 출력 체크포인트는 검정으로 잠근다. 시험은 문제지 우선이고 Layer 불일치는 감점 위험임을 첫 장면에서 고지한다.

## Frame 2 — Ø20 구멍과 러그 원호·장공 Seed를 만든다
- status: animated
- src: compositions/frames/02-circle-arc.html
- duration: 170s
- poster: 85s
- transition_in: magenta-rule-wipe
- scene: Datum 교차점의 Ø20과 러그 ARC·폭 8 장공 Seed를 설명한 뒤 DEMO-01로 전환한다.
- voiceover: "중앙 Ø20은 중심과 지름으로, 러그와 장공 Seed는 접점과 방향으로 정의합니다."
- rules: hyperframes-animation/rules/svg-path-draw.md, hyperframes-animation/rules/control-target-sync.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-01 circle-arc user recording placeholder

정면도 외곽을 계속 유지하고 새 원·호만 마젠타로 그린다. 녹화는 동일 `L03_BASE_PROFILE`에서 수행한다.

## Frame 3 — AF30 중앙 육각 포켓을 배치한다
- status: animated
- src: compositions/frames/03-polygon.html
- duration: 130s
- poster: 65s
- transition_in: technical-cut
- scene: 내접·외접 원리를 비교한 뒤 정본 입력 `POLYGON 6 → 중심 (40,22) → C → 반지름 15`를 고정하고 DEMO-02를 안내한다.
- voiceover: "AF30은 반지름 30이 아닙니다. 외접 옵션 C와 반지름 15로 수평 평면 사이 30을 만듭니다."
- rules: hyperframes-animation/rules/scale-swap-transition.md, hyperframes-animation/rules/svg-path-draw.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-02 polygon user recording placeholder

Ø20과 같은 중심에 수평 면을 가진 육각 포켓을 놓고, AF30·중심·수평 방향을 실제 측정하는 결과를 보여 준다.

## Frame 4 — 좌측 국소 5 mm 얕은 포켓 경계를 만든다
- status: animated
- src: compositions/frames/04-offset.html
- duration: 170s
- poster: 85s
- transition_in: split-wipe
- scene: 좌측 CONSTRUCTION Seed 창 `(0,10)–(24,34)`를 안쪽 5 mm OFFSET하여 최종 `(5,15)–(19,29)` 포켓을 만든 뒤 DEMO-03으로 전환한다.
- voiceover: "본체 전체가 아니라 좌측 국소 Seed 창을 안쪽 5 밀리미터 OFFSET해 닫힌 포켓을 만듭니다."
- rules: hyperframes-animation/rules/control-target-sync.md, hyperframes-animation/rules/svg-path-draw.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-03 offset user recording placeholder

기존 외곽은 검정, CONSTRUCTION Seed 창은 회색 점선, 새 국소 포켓 경계는 마젠타로 유지해 누적 결과와 비중첩을 분명히 한다.

## Frame 5 — 네 특징을 통합해 L04 상태를 검수한다
- status: animated
- src: compositions/frames/05-guided-practice.html
- duration: 145s
- poster: 72.5s
- transition_in: technical-cut
- scene: 동일 EDU-SB-01의 네 특징을 제시하고 20초 뒤 작업 순서와 Layer 검수를 공개한다.
- voiceover: "L03 외곽 위에 추가한 네 특징의 중심, 크기, 접점, 방향을 순서대로 검수하세요."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/stat-bars-and-fills.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only guided practice

정답은 20초 뒤 공개하며 `OUTLINE / CENTER / CONSTRUCTION · ByLayer`를 완료 조건으로 표시한다.

## Frame 6 — L04_PRIMARY_FEATURES로 저장한다
- status: animated
- src: compositions/frames/06-recap.html
- duration: 45s
- poster: 22.5s
- transition_in: magenta-rule-wipe
- scene: 같은 부품의 누적 결과, 시험 감점 위험, 다음 제3각법 투상을 연결한다.
- voiceover: "OUTLINE, CENTER, CONSTRUCTION을 확인하고 L04_PRIMARY_FEATURES로 저장해 다음 투상 단계로 넘깁니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

마지막 화면에 `시험 지시 우선`, `감점 위험 · 중심선/Layer/방향`, `다음 입력 · L04_PRIMARY_FEATURES`를 함께 표시한다.
