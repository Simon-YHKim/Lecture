---
workflow: general-video
flow: automation
storyboard: no
message: "시험 문제의 3D 모델·치수·지시사항을 먼저 해독해야 EDU-SB-01을 정확한 순서로 제작할 수 있다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 10m
angle: exam-brief-decoding
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: REFERENCE_READONLY
checkpoint_out: L01_FEATURE_MAP
paper: A3-landscape
projection: third-angle
---

## Intent

열 차시에 걸쳐 하나의 `EDU-SB-01 교육용 센서 장착 브래킷`을 완성하는 첫 수업이다. 학습자는 읽기 전용 문제 자료의 3D 모델, 치수, 지시사항을 해독하고 실제 제작 순서를 계획한다. 차시 시작 상태는 `REFERENCE_READONLY`, 종료 상태는 `L01_FEATURE_MAP`이다.

## Assets

- 비공개 원본 자료는 교육 범위와 시각 방향 참고용이며 공개 Git에 올리지 않는다.
- 3D 모델과 도면은 실제 사내 자료를 복사하지 않은 인라인 SVG 합성 형상만 사용한다.
- LG EI 폰트 바이너리, 녹화, 나레이션, DWG/DXF, 렌더는 로컬 비공개 영역에 둔다.

## Customizations

- 6개 장면을 `누적 부품 공개 → 3D 형상 해독 → 치수 해독 → 지시사항·Layer → 제3각법 뷰 → Feature Map 저장`으로 구성한다.
- 화면에는 부품 ID, 체크포인트, `OUTLINE`, `CENTER`, `HIDDEN`, `DIM` 역할을 실제 학습 내용으로 표시한다.
- 녹화 매핑은 `F2 · DEMO-01` 문제의 3D 모델·치수·지시사항 탐색, `F4 · DEMO-02` 제3각법 뷰와 `OUTLINE/CENTER/HIDDEN/DIM` 대응 추적이다. 둘 다 `REFERENCE_READONLY`를 근거로 `L01_FEATURE_MAP`을 만들며 작도 전 지시 누락의 시험 감점 위험을 확인한다.
- 시험에서는 문제지와 감독 지시가 과정 기본값보다 우선하며, 지시 불이행은 감점 위험이라는 고지를 포함한다.

## Notes

- 과정 기본은 ISO A3 가로형과 제3각법이지만 실제 시험 용지·축척·Layer 규칙은 달라질 수 있다.
- 이 차시에는 형상을 작도하지 않는다. 제작 근거와 순서를 확정해 `L01_FEATURE_MAP`만 만든다.
