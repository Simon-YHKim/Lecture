---
format: 1920x1080
duration: 19m00s
message: "L09_RELEASE_CANDIDATE를 제한시간 내 일곱 감점 게이트로 검사·수정해 L10_RELEASE한다."
arc: "모의시험 시작 → 7게이트 계획 → 입력·도면틀·투상 → 형상·표현·축척 → 치수·파일 → 승인"
audience: "AutoCAD 기본과정을 마무리하는 Technician 실습과정 초급 수강자"
mode: autonomous
part_id: EDU-SB-01
checkpoint_in: L09_RELEASE_CANDIDATE
checkpoint_out: L10_RELEASE
paper: A3-landscape
projection: third-angle
---

## Frame 1 — 재작도 없이 릴리스 후보에서 시작한다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 75s
- poster: 14s
- transition_in: cut
- scene: EDU-SB-01 L09_RELEASE_CANDIDATE와 3D 모델·치수·지시사항, 제한시간을 제시한다.
- voiceover: "처음부터 다시 그리지 않고 누적 릴리스 후보의 오류만 수정합니다."
- media: motion-only

OUTLINE·CENTER·HIDDEN·DIM·BORDER·TITLE·HATCH와 A3 가로형·제3각법을 최종 범위로 고정한다.

## Frame 2 — 일곱 감점 게이트를 계획한다

- status: animated
- src: compositions/frames/02-work-plan.html
- duration: 135s
- poster: 24s
- transition_in: magenta-rule-wipe
- scene: 입력, 도면틀, 제3각법, Layer, 형상·표현, 치수·축척, 파일·출력의 7게이트를 연결한다.
- voiceover: "일곱 게이트를 순서대로 통과하며 발견한 오류만 수정합니다."
- media: motion-only

각 게이트에 감점 위험과 남은 시간 표시를 연결한다.

## Frame 3 — 입력·A3·제3각법·Layer를 검사한다

- status: animated
- src: compositions/frames/03-environment-outline.html
- duration: 255s
- poster: 30s
- transition_in: technical-cut
- scene: DEMO-01에서 입력·도면틀·제3각법·핵심 Layer의 네 게이트를 연결한다.
- voiceover: "3D 모델·치수·지시사항, A3 외관선·표제란, 제3각법과 Layer 속성을 먼저 닫습니다."
- media: DEMO-01 INPUT / A3 / THIRD-ANGLE / LAYERS USER RECORDING

BORDER·TITLE과 OUTLINE·CENTER·HIDDEN·DIM의 이름·색상·선종류·선가중치를 공식 지시와 비교한다.

## Frame 4 — 형상·표현·축척을 검사한다

- status: animated
- src: compositions/frames/04-holes-repetition.html
- duration: 240s
- poster: 28s
- transition_in: split-wipe
- scene: EDU-SB-01 누적 특징과 A–A HATCH, 센서 BLOCK, 주석 GROUP, Model 1:1·뷰 축척을 DEMO-02로 검수한다.
- voiceover: "틀린 항목만 수정하고 이미 검수된 형상은 다시 그리지 않습니다."
- media: DEMO-02 GEOMETRY / HATCH / SCALE USER RECORDING

HATCH와 OUTLINE·CENTER·HIDDEN의 표현 관계를 포함해 게이트 5와 6을 닫는다.

## Frame 5 — 치수·파일·출력을 검사한다

- status: animated
- src: compositions/frames/05-edit-represent.html
- duration: 225s
- poster: 28s
- transition_in: technical-cut
- scene: ① 80×50×8·Datum, ② Ø20·AF30 깊이 4@(40,22), ③ 2×Ø6 위치·3×Ø4 PCD Ø36 시작각 30°, ④ 22×8 장공@(40,42)·R15/R5/C5·우측 경사 45°와 nominal `(68,35)→(80,23)`, ⑤ 14×14 포켓@(5,15)–(19,29) 깊이 2의 DIM 누락·중복과 Model 1:1·뷰 축척, 파일명·저장 위치·출력 상태를 DEMO-03으로 검사한다.
- voiceover: "제출 직전에는 치수와 파일·출력 지시를 대조해 마지막 감점 위험을 지웁니다."
- media: DEMO-03 DIMENSION / SCALE / FILE / OUTPUT USER RECORDING

감점 위험만 수정하고 재작도하지 않은 채 최종 감사와 L10_RELEASE 저장을 준비한다.

## Frame 6 — L10_RELEASE를 승인한다

- status: animated
- src: compositions/frames/06-dimension-final-check.html
- duration: 210s
- poster: 30s
- transition_in: magenta-rule-wipe
- scene: DEMO-04에서 최종 파일을 다시 열어 번호형 제작 치수 callout 1~5와 입력·A3, 제3각법·Layer, 형상·표현, 치수·축척, 파일·출력의 일곱 감점 게이트를 확인하고 릴리스를 승인한다.
- voiceover: "실제 감점 기준과 배점은 공식 문제지를 우선하며 EDU-SB-01을 L10_RELEASE로 저장합니다."
- media: DEMO-04 FINAL AUDIT / RELEASE USER RECORDING

번호형 callout과 검수 패널은 제작 치수의 크기·수량·깊이·필요한 기준 위치치수가 모두 존재함을 보여 준다. 교육용 정본보다 실제 시험 문제지 지정값이 우선한다. 처음부터 재작도하지 않았음을 before/after 상태선으로 확인하고 과정 전체를 마친다.
