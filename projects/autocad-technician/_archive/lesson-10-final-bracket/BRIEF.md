---
workflow: general-video
flow: automation
storyboard: no
message: "도면 읽기부터 작도·수정·표현·치수·자체 검수까지 같은 기준으로 연결하면 완성 도면을 스스로 검증할 수 있다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "AutoCAD 기본과정을 마무리하는 Technician 실습과정 초급 수강자"
length: 19m
angle: capstone-practice
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L09_RELEASE_CANDIDATE
checkpoint_out: L10_RELEASE
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 10차시는 처음부터 다시 작도하지 않는다. 시험 입력인 `3D 모델 + 치수 + 지시사항`과 `EDU-SB-01`의 `L09_RELEASE_CANDIDATE`를 제한시간 안에 대조한다. 80×50×8 외피, 중앙 Ø20·AF30 깊이 4와 중심 위치, 22×8 장공, 2×Ø6, 3×Ø4·PCD Ø36·시작각 30°, R15·R5·C5, 14×14 국부 포켓·깊이 2와 필요한 기준 위치치수를 포함한 제작 치수 세트를 최종 감사한다. `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`, `BORDER`, `TITLE`, `HATCH`를 포함한 일곱 감점 게이트를 검사·수정해 `L10_RELEASE`로 승인한다.

## Assets

- `frame.md` — 공개 가능한 디자인 규칙.
- 공개 장면은 `LG EI` family 이름과 `Malgun Gothic` fallback만 사용한다. 폰트 바이너리와 로컬 위치는 저장소 밖에서 비공개로 관리한다.
- `assets/private/recordings/` — 사용자 무음 화면 녹화 경로.
- `assets/private/audio/` — 사용자 한국어 나레이션 경로.

## Customizations

- 6개 장면, 1,140초 고정 타임라인이다.
- 녹화 매핑은 `F3 · DEMO-01` 입력·A3·BORDER/TITLE·제3각법·핵심 Layer, `F4 · DEMO-02` 누적 형상·HATCH/BLOCK/GROUP·Model 1:1·뷰 축척, `F5 · DEMO-03` DIM·축척·파일·출력, `F6 · DEMO-04` 재개방·7게이트 최종 감사·`L10_RELEASE` 승인이다. 모두 `L09_RELEASE_CANDIDATE`에서 출발해 시험 감점 위험을 제거하고 `L10_RELEASE`를 만든다.
- 합성 브래킷은 공개 가능한 단순 교육 도형이며 DWG, DXF, PPT 이미지 또는 실제 회사 형상을 사용하지 않는다.
- 일곱 감점 게이트는 `입력 지시`, `A3 도면틀·표제란`, `제3각법`, `핵심 Layer`, `형상·표현`, `치수·축척`, `파일·최종 출력`이다.
- Frame 6에서는 번호형 callout 1~5와 제작 치수 패널을 함께 사용해 외피·Datum, 중앙 특징, 구멍 패턴, 장공·윤곽, 국부 포켓의 크기·수량·깊이·위치를 마지막으로 대조한다.
- 마지막 장면에서 도면 파일명, 전체 검수, 자가 채점과 `L10_RELEASE` 저장까지 완료한다.
- 실제 녹화와 나레이션을 받은 뒤 Whisper 타임코드로 동기화하고 Studio 승인 뒤 렌더한다.

## Notes

- 녹화 기준은 1920×1080, 30fps, 커서 표시, 무음, 앞뒤 2초 핸들이다.
- 특정 버전 UI보다 목적·기준점·작업 순서·검수 근거를 우선한다.
- 실제 감점 기준과 배점은 해당 회차 공식 문제지와 최신 공지를 우선한다.
