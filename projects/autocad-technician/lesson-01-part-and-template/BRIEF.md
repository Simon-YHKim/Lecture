---
workflow: general-video
flow: automation
storyboard: yes
message: "부품이 왜 그 모양인지 읽을 수 있어야 도면을 정확한 순서로 그릴 수 있고, 그리기 전에 종이와 레이어 규칙을 먼저 세운다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 10m30s
angle: part-reading-and-drawing-environment
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: REFERENCE_READONLY
checkpoint_out: L01_TEMPLATE
paper: A3-landscape
projection: third-angle
recording_slots: 1
---

## Intent

여섯 차시에 걸쳐 하나의 `EDU-IB-02 아이들러 풀리 브래킷`을 완성하는 첫 수업이다. 학습자는 부품의 기능에서 형상의 이유를 읽고, 도면이 담고 있는 정보 가운데 이 과정에서 다루는 것과 개념만 알고 넘어갈 것을 구분한 뒤, A3 도면틀과 여덟 개 레이어가 준비된 템플릿 파일을 직접 만든다. 시작 상태는 `REFERENCE_READONLY`, 종료 상태는 `L01_TEMPLATE`이다.

## Assets

- 부품 형상은 `scripts/part/edu_ib_02.py`가 생성하는 인라인 SVG만 사용한다. 손으로 그린 도형을 프레임에 직접 써 넣지 않는다.
- 정본 좌표는 `master-part-geometry.json`이며, 그 파일도 같은 스크립트가 생성한다.
- LG EI 폰트 바이너리, 녹화, 나레이션, DWG, 렌더는 승인된 비공개 위치에 둔다.

## Customizations

- 여섯 장면을 `부품 소개 → 형상의 이유 → 도면 읽기 → 종이와 레이어 → 템플릿 작성 녹화 → 정리`로 구성한다.
- 형상을 소개하는 장면은 `data-feature` 속성으로 특징을 하나씩 강조한다. 좌표를 프레임에 중복 기입하지 않는다.
- 녹화는 한 개다. `F5 · DEMO-01` 템플릿 작성이며, `acadiso.dwt` 선택부터 저장까지 한 번에 이어 간다.
- 표면거칠기·기하공차·재질·열처리는 뜻과 이유만 설명하고 작도 대상에서 제외한다.

## Notes

- 이 차시에는 형상을 작도하지 않는다. 다만 문서 하나가 아니라 **열 수 있는 파일**을 남긴다.
- 과정 기본은 ISO A3 가로형과 제3각법이지만 실제 시험의 용지·축척·레이어 규칙은 달라질 수 있으며 문제지와 감독 지시가 우선한다.
- 다음 차시가 쓰는 접점(TAN) 스냅을 이 차시 마지막에 켜 두고 끝낸다.
