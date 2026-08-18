---
workflow: general-video
flow: automation
storyboard: no
message: "L05의 EDU-SB-01 세 뷰와 중심축을 기준으로 목표점 COPY·Seed MIRROR·ARRAY를 중복 없이 적용해 반복 특징을 완성한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "L05_THIRD_ANGLE_VIEWS까지 완성한 Technician 실습과정 초급 수강자"
length: 13m
angle: cumulative-build
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L05_THIRD_ANGLE_VIEWS
checkpoint_out: L06_PATTERNED_FEATURES
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 6차시는 새 합성 브래킷을 그리지 않는다. `L05_THIRD_ANGLE_VIEWS`의 EDU-SB-01 정면도·평면도·우측면도와 중심축을 그대로 사용한다. 왼쪽 Ø6 Seed를 배치하고 COPY한 CONSTRUCTION 목표점으로 오른쪽 위치를 검수한 뒤, 실제 Ø6은 Datum B MIRROR로 한 번만 생성한다. PCD 0° 위치 `(58,22)`의 Ø4 Seed는 중심 `(40,22)` 기준 30° ROTATE한 후 Polar ARRAY해 3개 센서 구멍을 만든다. 다른 뷰의 숨은선 대응까지 갱신해 `L06_PATTERNED_FEATURES`를 만든다.

## Assets

- 화면 도형은 인라인 SVG만 사용하며 회사 도면이나 첨부 PNG를 복사하지 않는다.
- 녹화 매핑은 `F2 · DEMO-01` Ø6 Seed MOVE와 CONSTRUCTION 목표점 COPY, `F3 · DEMO-02` Ø4 Seed 작성·30° ROTATE와 Datum B Ø6 MIRROR·원본 유지, `F4 · DEMO-03` 3×Ø4·PCD Ø36 Polar ARRAY·세 뷰 갱신이다. 모두 `L05_THIRD_ANGLE_VIEWS`에서 `L06_PATTERNED_FEATURES`를 만들며 중복 객체·기준점·개수·Layer 오류의 시험 감점 위험을 확인한다.
- DWG 체크포인트, 실제 녹화, 나레이션, 비공개 PPT와 폰트 바이너리는 비공개 경계에 둔다.

## Customizations

- 누적 경로는 `L05_THIRD_ANGLE_VIEWS → L06_PATTERNED_FEATURES`다.
- 사용 Layer는 `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`이며 반복 뒤 세 뷰의 선종류와 임시 목표·투영 보조선도 함께 검수한다.
- 하부 장착 구멍은 `2 × Ø6`, 센서 구멍은 `3 × Ø4 · PCD Ø36`으로 고정한다.
- 기존 여섯 장면, 780초, 세 DEMO ID와 src를 보존한다.
- 마젠타는 이번 차시에서 추가되는 Seed와 복제 결과에만 사용한다.

## Exam disclosure

시험에서는 제공된 3D 모델·치수·지시사항을 제한시간 안에 완성해야 한다. 검수하지 않은 Seed 복제, 잘못된 기준점·대칭축·배열 중심, 개수·각도 오류, OUTLINE·CENTER·HIDDEN Layer 또는 선종류 불일치, 지시사항 불이행은 감점 위험이다. 실제 문제지와 감독 지시가 우선한다.

## Notes

- 기준 객체 한 개를 먼저 측정한 뒤 복제한다. 잘못된 객체를 반복하지 않는다.
- 배열 결과는 정면도뿐 아니라 평면도·우측면도의 HIDDEN과 CENTER 대응까지 검수한다.
