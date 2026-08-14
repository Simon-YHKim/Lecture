---
format: 1920x1080
duration: 13m00s
message: "L04의 EDU-SB-01 정면도를 기준으로 제3각법 세 뷰와 선종류를 완성한다."
arc: "L04 체크포인트 → 제3각법 배치 → 뷰 탐색 → 특징 추적 → Layer 검수 → L05 저장"
audience: "L04_PRIMARY_FEATURES까지 완성한 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L04_PRIMARY_FEATURES
checkpoint_out: L05_THIRD_ANGLE_VIEWS
paper: A3-landscape
projection: third-angle
layers_used: [OUTLINE, CENTER, HIDDEN, CONSTRUCTION]
---

## Frame 1 — L04 정면도를 제3각법 기준 뷰로 고정한다
- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 30s
- transition_in: cut
- scene: EDU-SB-01, 입출력 체크포인트, 제3각법 위치와 네 Layer를 소개한다.
- voiceover: "L04 정면도를 다시 그리지 않고 평면도는 위, 우측면도는 오른쪽에 투영합니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

제3각법 위치와 Layer 불일치가 시험 감점 위험임을 첫 화면에 고지한다.

## Frame 2 — 평면도는 위, 우측면도는 오른쪽에 투영한다
- status: animated
- src: compositions/frames/02-orthographic-principle.html
- duration: 150s
- poster: 75s
- transition_in: magenta-rule-wipe
- scene: 정면도를 기준으로 위의 평면도와 오른쪽 우측면도를 투영선으로 조립한다.
- voiceover: "제3각법에서 평면도는 정면도 위, 우측면도는 정면도 오른쪽입니다."
- rules: hyperframes-animation/rules/svg-path-draw.md, hyperframes-animation/rules/control-target-sync.md
- media: motion-only original SVG

CONSTRUCTION 투영선과 OUTLINE 결과선을 구분하고 Datum B 중심축을 세 뷰에 연결한다.

## Frame 3 — 세 뷰를 잃지 않고 탐색한다
- status: animated
- src: compositions/frames/03-view-navigation.html
- duration: 170s
- poster: 85s
- transition_in: technical-cut
- scene: 전체·세부·전체 탐색을 설명한 뒤 DEMO-01로 전환한다.
- voiceover: "확대해도 평면도 위, 우측면도 오른쪽의 전체 관계로 돌아옵니다."
- rules: hyperframes-animation/rules/coordinate-target-zoom.md, hyperframes-animation/rules/cursor-click-ripple.md
- media: DEMO-01 three-view zoom-pan user recording placeholder

녹화는 동일 `L04_PRIMARY_FEATURES`에서 새 뷰를 추가하는 과정이다.

## Frame 4 — L04의 네 특징을 세 뷰에서 추적한다
- status: animated
- src: compositions/frames/04-feature-tracing.html
- duration: 180s
- poster: 90s
- transition_in: split-wipe
- scene: Ø20, AF30, 장공 Seed, 5 mm 포켓 경계를 같은 번호와 선종류로 추적한 뒤 DEMO-02로 전환한다.
- voiceover: "같은 특징이 뷰에 따라 OUTLINE, CENTER, HIDDEN으로 달라지는 이유를 확인합니다."
- rules: hyperframes-animation/rules/svg-path-draw.md, hyperframes-animation/rules/cursor-click-ripple.md, hyperframes-animation/rules/control-target-sync.md
- media: DEMO-02 hole-step tracing user recording placeholder

마젠타 투영선은 대응을 설명하되 최종 객체 Layer와 혼동하지 않는다.

## Frame 5 — 네 Layer와 뷰 정렬을 검수한다
- status: animated
- src: compositions/frames/05-missing-information.html
- duration: 175s
- poster: 87.5s
- transition_in: technical-cut
- scene: 20초 대응표 뒤 OUTLINE·CENTER·HIDDEN·CONSTRUCTION 정답과 뷰 정렬을 공개한다.
- voiceover: "보이는 선, 중심선, 숨은선, 투영 보조선을 목적에 맞는 Layer로 분리하세요."
- rules: hyperframes-animation/rules/stat-bars-and-fills.md, hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only guided practice

한 뷰에서 부족한 정보는 다른 뷰와 3D 지시에서 확인하고 임의로 추측하지 않는다.

## Frame 6 — L05_THIRD_ANGLE_VIEWS로 저장한다
- status: animated
- src: compositions/frames/06-recap.html
- duration: 45s
- poster: 22.5s
- transition_in: magenta-rule-wipe
- scene: 제3각법 위치와 네 Layer, 시험 감점 위험, 다음 반복 특징 단계를 요약한다.
- voiceover: "세 뷰와 Layer를 검수하고 L05_THIRD_ANGLE_VIEWS로 저장합니다."
- rules: hyperframes-animation/rules/waterfall-entry.md, hyperframes-animation/rules/svg-path-draw.md
- media: motion-only

마지막 화면에서 `시험 지시 우선`, `감점 위험 · 뷰 배치/선종류/Layer`, `다음 입력 · L05_THIRD_ANGLE_VIEWS`를 표시한다.
