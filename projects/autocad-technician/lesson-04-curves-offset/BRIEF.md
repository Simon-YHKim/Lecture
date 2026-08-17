---
workflow: general-video
flow: automation
storyboard: no
message: "L03에서 만든 EDU-SB-01 기준 외곽에 중심·크기·접점·간격으로 주요 특징을 정확히 추가한다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "L03_BASE_PROFILE까지 완성한 Technician 실습과정 초급 수강자"
length: 12m
angle: cumulative-build
narration: user-recorded
style_preset: ppt-derived-lg-training
part_id: EDU-SB-01
checkpoint_in: L03_BASE_PROFILE
checkpoint_out: L04_PRIMARY_FEATURES
paper: A3-landscape
projection: third-angle
---

## Intent

AutoCAD 기본과정 4차시는 별도 플레이트를 새로 그리지 않는다. L03에서 저장한 `EDU-SB-01`의 정면도 기준 외곽 `L03_BASE_PROFILE`을 열어 중앙 센서 구멍 Ø20, 상부 러그 R15 원호와 22×8 mm 장공 Seed, 중앙 육각 포켓 AF30, 좌측 국소 Seed 창에서 안쪽으로 5 mm 떨어진 14×14 얕은 포켓 경계를 누적한다. 결과는 다음 차시의 제3각법 투상 기준인 `L04_PRIMARY_FEATURES`가 된다.

## Assets

- `frame.md`는 공개 가능한 색·서체·레이아웃 규칙의 정본이다.
- `assets/private/recordings/`에는 `DEMO-01`부터 `DEMO-03`까지의 무음 AutoCAD 녹화가 들어간다.
- `assets/private/audio/`에는 사용자가 녹음한 최종 한국어 나레이션이 들어간다.
- 강사용 DWG 체크포인트와 비공개 PPT·LG 폰트 바이너리는 공개 저장소에 포함하지 않는다.

## Customizations

- 누적 경로는 `L03_BASE_PROFILE → L04_PRIMARY_FEATURES`이며 부품 ID는 항상 `EDU-SB-01`로 표시한다.
- 이번 차시 실제 사용 Layer는 `OUTLINE`, `CENTER`, `CONSTRUCTION`이다. 보이는 특징은 `OUTLINE`, 중심과 대칭축은 `CENTER`, 국소 포켓 Seed 창과 예정 위치 기준은 `CONSTRUCTION`에 두고 모든 객체 속성은 원칙적으로 ByLayer로 유지한다.
- 녹화 매핑은 `F2 · DEMO-01` 중심 (40,22) Ø20·중심 (40,35) R15 러그 ARC·중심 (40,42) 22×8 장공 Seed, `F3 · DEMO-02` AF30 육각 포켓, `F4 · DEMO-03` 국소 Seed 창 (0,10)–(24,34)의 내부 5 mm OFFSET과 비중첩 검수다. 모두 `L03_BASE_PROFILE`에서 `L04_PRIMARY_FEATURES`를 만들며 중심·Layer·방향 오류의 시험 감점 위험을 확인한다.
- 여섯 장면, 기존 720초 타임라인과 녹화 슬롯 ID를 보존한다.
- 형상은 인라인 SVG로만 추상화하며 PNG, 회사 도면, PPT 캡처를 복사하지 않는다.

## Exam disclosure

시험에서는 3D 모델, 치수, 지시사항이 함께 제공되며 제한시간 안에 도면을 완성해야 한다. 템플릿, 용지, Layer 이름·색상·선종류·선가중치, 축척은 해당 회차 문제지와 감독 지시를 우선한다. 중심선 누락, 반지름·지름 혼동, 지정 Layer 불일치, OFFSET 방향 오류, 지시사항 불이행은 감점 위험이다.

## Notes

- 화면 녹화 기본값은 1920×1080, 30 fps, 커서 표시, 무음, 앞뒤 2초 여유다.
- L04 종료 전에 `OUTLINE`, `CENTER`, `CONSTRUCTION`을 분리하고 체크포인트 이름으로 SAVEAS한다.
- 실제 녹음 후 Whisper 단어 타임코드로 화면 전환과 강조를 재동기화한다.
