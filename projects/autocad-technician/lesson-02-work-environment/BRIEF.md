---
workflow: general-video
flow: automation
storyboard: no
message: "L01_FEATURE_MAP을 받아 acadiso.dwt 기반 A3 시험 도면틀과 전체 Layer를 준비한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "EDU-SB-01 문제 해독을 마친 Technician 실습과정 입문 수강자"
length: 12m
angle: cumulative-exam-setup
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L01_FEATURE_MAP
checkpoint_out: L02_SETUP
paper: A3-landscape
projection: third-angle
---

## Intent

Lesson 01의 `L01_FEATURE_MAP`을 이어받아 `EDU-SB-01`을 그릴 시험형 작업 파일을 만든다. `acadiso.dwt`, millimeter, Model Space 부품 1:1, Layout/Paper Space A3 도면틀 1:1, 잠근 Viewport, A3 가로 420×297 mm, 사방 10 mm 외관선, 우측 하단 200×30 mm 표제란, 사번·이름 100+100 mm, 문자 높이 10 mm, 제3각법과 전체 Layer를 설정한 `L02_SETUP`이 종료 상태다.

## Assets

- AutoCAD 화면은 사용자가 촬영한 비공개 녹화로 교체한다.
- 모션그래픽의 도면틀과 UI는 공개 가능한 인라인 SVG/CSS로 새로 만든다.
- 원본 자료, 시험 캡처, 회사 정보, 폰트·DWG·녹화 바이너리는 공개하지 않는다.

## Customizations

- 6개 장면은 `체크포인트 인계 → acadiso.dwt·단위·저장 → A3 도면틀·표제란 → 전체 Layer → Osnap·좌표·제3각법 → L02_SETUP 저장` 순서다.
- `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`, `BORDER`, `TITLE`, `HATCH`, `CONSTRUCTION`의 이름·역할·교육용 속성을 모두 표시한다.
- 녹화 매핑은 `F2 · DEMO-01` 템플릿·SAVEAS·UNITS·Model 1:1, `F4 · DEMO-02` 빈 Layout/Paper Space부터 A3 도면틀·표제란·잠근 Viewport·8개 Layer 직접 생성, `F5 · DEMO-03` Osnap·Ortho·원점·제3각법 작업 자리다. 모두 `L01_FEATURE_MAP`에서 `L02_SETUP`으로 이어지며 설정·Layer·뷰 지시 누락의 시험 감점 위험을 확인한다.
- 실제 시험 템플릿이나 지시가 있으면 제공 파일의 Model/Layout 공간 구조를 포함해 제공 파일을 우선하고, 설정 누락은 감점 위험임을 고지한다.

## Notes

- 모델 형상은 Model Space 1:1, 교육용 도면틀은 Layout/Paper Space mm 1:1로 작성하며 Viewport의 출력·뷰 축척은 시험 문제지 지시값을 적용하고 잠근다.
- 다음 차시는 새 파일이 아니라 `L02_SETUP`을 열어 `OUTLINE`과 `CONSTRUCTION`으로 정면 외곽을 작성한다.
