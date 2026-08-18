---
format: 1920x1080
duration: 13m00s
message: "L05의 EDU-SB-01 세 뷰에서 검수된 Seed를 복제해 반복 특징을 완성한다."
arc: "L05 체크포인트 → Ø6 Seed·목표점 COPY → Ø4 0° Seed·30° ROTATE·Ø6 MIRROR → Ø4 Polar ARRAY → 세 뷰 검수 → L06 저장"
audience: "L05_THIRD_ANGLE_VIEWS까지 완성한 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L05_THIRD_ANGLE_VIEWS
checkpoint_out: L06_PATTERNED_FEATURES
paper: A3-landscape
projection: third-angle
layers_used: [OUTLINE, CENTER, HIDDEN, CONSTRUCTION]
---

## Frame 1 — L05 세 뷰에서 반복 특징을 시작한다
- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 30s
- transition_in: cut
- scene: EDU-SB-01, 체크포인트, `2×Ø6`, `3×Ø4 PCD Ø36`, 세 Layer를 소개한다.
- voiceover: "새 도형이 아니라 L05의 세 뷰와 중심축에서 반복 특징을 계속 만듭니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

시험은 문제지 우선이며 Seed·축·배열·Layer 오류가 감점 위험임을 고지한다.

## Frame 2 — 검수된 Ø6 Seed를 배치하고 COPY한다
- status: animated
- src: compositions/frames/02-move-copy.html
- duration: 180s
- poster: 90s
- transition_in: magenta-rule-wipe
- scene: 하부 Ø6 Seed를 `(15,8)`에 놓고 중심의 CONSTRUCTION 목표표시만 `(50,0)` COPY해 `(65,8)`을 준비한 뒤 DEMO-01로 전환한다.
- voiceover: "Ø6 원은 하나만 두고, COPY는 오른쪽 MIRROR 결과를 검수할 목표점에 사용합니다."
- rules: hyperframes-animation/rules/control-target-sync.md, hyperframes-animation/rules/cursor-click-ripple.md, hyperframes-animation/rules/svg-path-draw.md
- media: DEMO-01 move-copy user recording placeholder

기존 L05 세 뷰는 검정, 이번 Seed와 복사한 CONSTRUCTION 목표표시만 마젠타로 표시한다. 오른쪽 Ø6 원은 아직 만들지 않는다.

## Frame 3 — Datum B로 방향과 대칭을 확정한다
- status: animated
- src: compositions/frames/03-rotate-mirror.html
- duration: 190s
- poster: 95s
- transition_in: technical-cut
- scene: Ø4 Seed를 PCD 0° 중심 `(58,22)`에 만든 뒤 시작각 30°로 ROTATE하고, 하부 왼쪽 Ø6을 Datum B로 MIRROR해 오른쪽 목표 `(65,8)`과 일치시킨다. AF30 수평 면은 수정하지 않고 검수한 뒤 DEMO-02로 전환한다.
- voiceover: "회전 중심은 위치를 지키고, MIRROR 축은 Datum B의 두 점으로 고정합니다."
- rules: hyperframes-animation/rules/control-target-sync.md, hyperframes-animation/rules/scale-swap-transition.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-02 rotate-mirror user recording placeholder

원본 유지와 양쪽 거리를 확인하고 다른 뷰의 HIDDEN 대응을 갱신한다.

## Frame 4 — 3×Ø4를 PCD Ø36에 Polar ARRAY한다
- status: animated
- src: compositions/frames/04-array.html
- duration: 160s
- poster: 80s
- transition_in: split-wipe
- scene: PCD 중심과 Ø4 Seed에서 3개 Polar ARRAY를 만든 뒤 DEMO-03으로 전환한다.
- voiceover: "중앙을 ARRAY 중심으로, 항목 수 3과 전체 각도 360도로 반복 규칙을 고정합니다."
- rules: hyperframes-animation/rules/control-target-sync.md, hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-03 array user recording placeholder

하나씩 COPY한 근사 패턴이 아니라 `3 × Ø4 · PCD Ø36` 관계를 시각화한다.

## Frame 5 — 세 뷰의 반복 결과를 검수한다
- status: animated
- src: compositions/frames/05-guided-practice.html
- duration: 145s
- poster: 72.5s
- transition_in: technical-cut
- scene: 20초 계획 뒤 Ø6 대칭, Ø4 배열, OUTLINE·CENTER·HIDDEN 검수 순서를 공개한다.
- voiceover: "기준 객체와 전체 패턴을 검수하고 다른 뷰의 선종류까지 갱신하세요."
- rules: hyperframes-animation/rules/stat-bars-and-fills.md, hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only guided practice

같은 EDU-SB-01 세 뷰를 유지하며 추가 특징만 마젠타로 강조한다.

## Frame 6 — L06_PATTERNED_FEATURES로 저장한다
- status: animated
- src: compositions/frames/06-recap.html
- duration: 45s
- poster: 22.5s
- transition_in: magenta-rule-wipe
- scene: 반복 결과, 세 Layer, 시험 감점 위험, 다음 형상 마감을 요약한다.
- voiceover: "OUTLINE, CENTER, HIDDEN을 확인하고 L06_PATTERNED_FEATURES로 저장합니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

마지막 화면에 `시험 지시 우선`, `감점 위험 · Seed/축/배열/Layer`, `다음 입력 · L06_PATTERNED_FEATURES`를 표시한다.
