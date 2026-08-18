---
workflow: general-video
flow: automation
storyboard: no
message: "L02_SETUP을 열어 OUTLINE과 CONSTRUCTION으로 EDU-SB-01 정면도 기준 외곽을 작성한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "A3 시험 작업 환경을 준비한 Technician 실습과정 입문 수강자"
length: 12m
angle: cumulative-front-base-profile
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L02_SETUP
checkpoint_out: L03_BASE_PROFILE
paper: A3-landscape
projection: third-angle
---

## Intent

`L02_SETUP`을 이어받아 `EDU-SB-01`의 제3각법 기준 정면 외곽과 상부 러그 직선 골격을 실제 제작 순서로 작성한다. `CONSTRUCTION`으로 원점·Datum A·Datum B·80×50 기준 상자를 만들고 `OUTLINE`으로 보이는 외곽을 연결해 `L03_BASE_PROFILE`로 저장한다.

## Assets

- 동일 A3 가로형 작업 파일과 교육용 합성 부품만 사용한다.
- 화면 녹화는 사용자가 비공개로 촬영하고 공개 HTML은 인라인 SVG만 사용한다.
- 비공개 원본, 회사 도면, DWG/DXF, 폰트, 녹화, 나레이션은 Git에 포함하지 않는다.

## Customizations

- 6개 장면은 `체크포인트 확인 → LINE/PLINE 선택 → 좌표·Datum → 80×50 기준 상자 → 러그 직선 골격·폐곡선 검수 → 저장`으로 구성한다.
- 현재 차시 Layer는 `OUTLINE`, `CONSTRUCTION`이며 다른 Layer는 준비 상태로 유지한다.
- 녹화 매핑은 `F2 · DEMO-01` LINE/PLINE 역할 비교 후 누적 파일 적용, `F4 · DEMO-02` 빈 Model Space에서 CONSTRUCTION 원점·Datum A/B·80×50 기준 상자를 만든 뒤 OUTLINE PLINE·CLOSE, `F5 · DEMO-03` Closed·`OUTLINE/CONSTRUCTION`·Datum 검수다. 모두 `L02_SETUP`에서 `L03_BASE_PROFILE`을 만들며 Layer·폐곡선·지시 누락의 시험 감점 위험을 확인한다.
- 실제 시험에서는 용지·축척·Layer·제3각법 지시 불이행이 감점 위험임을 고지한다.

## Notes

- 본체 기준 크기는 80×50 mm, 원점은 좌측 하단, Datum A는 하단, Datum B는 X=40 중심선이다.
- 원·호·구멍·포켓·장공은 다음 차시 작업이므로 이번 종료 상태에는 직선 골격만 남긴다.
