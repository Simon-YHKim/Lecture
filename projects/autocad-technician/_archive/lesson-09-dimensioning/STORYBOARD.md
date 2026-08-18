---
format: 1920x1080
duration: 14m00s
message: "EDU-SB-01에 제작·검사용 치수와 축척 기준을 완성한다."
arc: "누적 상태 확인 → DIMSTYLE → 전체·위치·각도 → R·Ø → 축척 검수 → 시험 고지"
audience: "AutoCAD 기본 조작을 익힌 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L08_REPRESENTED
checkpoint_out: L09_RELEASE_CANDIDATE
paper: A3-landscape
projection: third-angle
---

## Frame 1 — L08 표현 완료 파일에서 계속한다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 12s
- transition_in: cut
- scene: EDU-SB-01 L08_REPRESENTED의 DIM·OUTLINE·CENTER Layer와 목표 상태를 제시한다.
- voiceover: "새 예제가 아니라 같은 브래킷에 치수와 축척을 완성합니다."
- media: motion-only

시험 입력 3D 모델·치수·지시사항과 A3 가로형 제3각법 조건을 함께 표시한다.

## Frame 2 — DIMSTYLE과 DIM Layer를 고정한다

- status: animated
- src: compositions/frames/02-dimstyle.html
- duration: 150s
- poster: 24s
- transition_in: magenta-rule-wipe
- scene: 공통 치수 규칙과 Model 1:1을 확인하고 DEMO-01로 전환한다.
- voiceover: "DIM Layer와 DIMSTYLE을 먼저 고정하고 출력·뷰 축척은 시험 지시를 따릅니다."
- media: DEMO-01 DIMSTYLE USER RECORDING

치수 객체가 OUTLINE이나 CENTER Layer에 섞이지 않도록 점검한다.

## Frame 3 — Datum에서 전체·위치·각도를 전달한다

- status: animated
- src: compositions/frames/03-linear-aligned-angular.html
- duration: 210s
- poster: 28s
- transition_in: technical-cut
- scene: EDU-SB-01의 80×50×8, 중심 (40,22)·(40,42), 하부 구멍 중심과 국부 포켓 경계를 Datum A·B에 연결하고 DEMO-02로 이어진다.
- voiceover: "DIMLINEAR, DIMALIGNED, DIMANGULAR는 측정 관계에 맞춰 같은 브래킷에 적용합니다."
- media: DEMO-02 LINEAR / ALIGNED / ANGULAR USER RECORDING

제3각법 뷰 정렬과 CENTER 기준이 치수의 출발점으로 보인다.

## Frame 4 — 윤곽과 홀·장공·포켓 치수를 전달한다

- status: animated
- src: compositions/frames/04-radius-diameter.html
- duration: 180s
- poster: 24s
- transition_in: split-wipe
- scene: EDU-SB-01의 R15·R5·C5, Ø20·AF30 깊이 4, 22×8 장공, 2×Ø6, 3×Ø4·PCD Ø36·시작각 30°, 14×14 포켓 깊이 2를 제작 의미에 맞춰 치수화하고 DEMO-03으로 전환한다.
- voiceover: "반지름·모따기, 구멍·포켓·장공은 크기와 수량, 깊이, 기준 위치를 함께 전달합니다."
- media: DEMO-03 RADIUS / DIAMETER / REVIEW USER RECORDING

DIM Layer를 유지하며 같은 정보를 여러 뷰에 중복하지 않는다.

## Frame 5 — 누락·중복과 축척을 검수한다

- status: animated
- src: compositions/frames/05-dimension-review.html
- duration: 180s
- poster: 20s
- transition_in: cut
- scene: 같은 EDU-SB-01에 번호형 callout ① 외피·Datum, ② 중앙 특징, ③ 구멍 패턴, ④ 장공·R/C·우측 경사 45°와 nominal `(68,35)→(80,23)`, ⑤ 국부 포켓을 놓고 DIM·OUTLINE·CENTER, Model 1:1, 뷰 축척과 표제란 축척을 검수한다.
- voiceover: "제작에 필요한 정보는 빠짐없이, 같은 정보는 한 번만 표시합니다."
- media: motion-only

80×50×8, Ø20@(40,22), AF30·깊이 4, SLOT 22×8@(40,42), 2×Ø6@(15,8)/(65,8), 3×Ø4·PCD Ø36·30°, R15·R5·C5, 우측 경사 45°·nominal `(68,35)→(80,23)`, 포켓 14×14@(5,15)–(19,29)·깊이 2와 필요한 기준 위치치수를 A3 도면 안에서 확인하고 L09_RELEASE_CANDIDATE로 저장한다. 교육용 값보다 실제 시험 문제지 지정값이 우선한다.

## Frame 6 — 릴리스 후보의 감점 위험을 기록한다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 60s
- poster: 18s
- transition_in: magenta-rule-wipe
- scene: 축척·치수·도면틀·제3각법·Layer 오류를 감점 위험으로 남기고 L10으로 연결한다.
- voiceover: "실제 감점 기준은 공식 문제지를 우선하며 다음 차시는 릴리스 후보만 검사·수정합니다."
- media: motion-only

`L09_RELEASE_CANDIDATE → L10_RELEASE` 상태선을 그린다.
