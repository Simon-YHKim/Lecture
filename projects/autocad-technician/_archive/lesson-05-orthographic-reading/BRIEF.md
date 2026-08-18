---
workflow: general-video
flow: automation
storyboard: no
message: "L04에서 완성한 EDU-SB-01 정면도를 기준으로 제3각법 평면도와 우측면도를 투영하고 선종류를 구분한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "L04_PRIMARY_FEATURES까지 완성한 Technician 실습과정 초급 수강자"
length: 13m
angle: cumulative-build
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L04_PRIMARY_FEATURES
checkpoint_out: L05_THIRD_ANGLE_VIEWS
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 5차시는 별도 브래킷을 읽는 독립 예제가 아니다. `L04_PRIMARY_FEATURES`의 EDU-SB-01 정면도를 기준 뷰로 고정하고, 제3각법 규칙에 따라 평면도를 위에, 우측면도를 오른쪽에 투영한다. `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`을 실제 객체에 적용해 `L05_THIRD_ANGLE_VIEWS`를 만든다.

## Assets

- 공개 코드에는 인라인 SVG와 추상 훈련 도형만 사용한다.
- AutoCAD 녹화, DWG 체크포인트, 비공개 PPT, LG 폰트 바이너리는 비공개 경계에 둔다.
- 녹화 매핑은 `F3 · DEMO-01` 제3각법 세 뷰 투영·정렬과 Zoom/Pan, `F4 · DEMO-02` Ø20·AF30·장공·OFFSET의 `OUTLINE/CENTER/HIDDEN` 추적이다. 모두 `L04_PRIMARY_FEATURES`에서 `L05_THIRD_ANGLE_VIEWS`를 만들며 뷰 배치·선종류 오류의 시험 감점 위험을 확인한다.

## Customizations

- 누적 경로는 `L04_PRIMARY_FEATURES → L05_THIRD_ANGLE_VIEWS`다.
- 제3각법 배치는 `평면도 = 정면도 위`, `우측면도 = 정면도 오른쪽`으로 고정한다.
- 사용 Layer는 `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`이며 모든 속성은 ByLayer를 원칙으로 한다.
- 정면도의 Ø20, AF30, 장공 Seed, 5 mm 포켓 경계가 다른 뷰에서 외형선·중심선·숨은선으로 어떻게 변하는지 보여 준다.
- 기존 여섯 장면, 780초, 두 DEMO ID와 src를 보존한다.

## Exam disclosure

시험에서는 3D 모델, 치수, 지시사항을 제한시간 안에 해독하고 완성해야 한다. 제3각법 배치 오류, 뷰 정렬 불량, 중심선·숨은선 누락, Layer 또는 선종류 불일치, 축척·지시사항 불이행은 감점 위험이다. 실제 시험의 문제지와 감독 지시가 항상 우선한다.

## Notes

- L05 종료 시 정면도는 다시 그리지 않고, L04 형상을 기준으로 새 뷰만 추가한다.
- 다음 차시의 COPY·MIRROR·ARRAY가 사용할 중심축과 Seed 위치를 보존한다.
