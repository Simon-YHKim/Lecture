---
format: 1920x1080
duration: 12m
message: "L01_FEATURE_MAP을 시험형 A3 작업 파일 L02_SETUP으로 변환한다."
arc: "체크포인트 인계 → 템플릿·단위 → A3 도면틀 → 전체 Layer → 스냅·뷰 자리 → 설정 저장"
audience: "EDU-SB-01 문제 해독을 마친 Technician 실습과정 입문 수강자"
mode: autonomous
---

## Frame 1 — Feature Map을 작업 파일로 바꾼다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 18s
- transition_in: cut
- scene: `EDU-SB-01 · L01_FEATURE_MAP → L02_SETUP`과 A3 가로형·제3각법 설정 목표를 소개한다.
- voiceover: "첫 선을 그리기 전에 시험 지시에 맞는 작업 파일을 완성합니다."
- media: motion-only

시험 문제지 우선과 설정 누락의 감점 위험을 도입부에서 분명하게 고지한다.

## Frame 2 — acadiso.dwt와 millimeter를 확인한다

- status: animated
- src: compositions/frames/02-saveas-units.html
- duration: 120s
- poster: 24s
- transition_in: magenta-rule-wipe
- scene: ISO metric 템플릿, SAVEAS, millimeter, Model Space 1:1을 조립한 뒤 화면 녹화로 전환한다.
- voiceover: "시험 제공 파일이 없다면 acadiso.dwt에서 시작하고 모델은 1대1로 작성합니다."
- media: DEMO-01 template, saveas and units user recording

현재 파일이 `EDU-SB-01_L02_SETUP`인지 확인한다.

## Frame 3 — A3 도면틀과 표제란을 만든다

- status: animated
- src: compositions/frames/03-view-coordinate.html
- duration: 150s
- poster: 28s
- transition_in: magenta-rule-wipe
- scene: Layout/Paper Space에서 A3 `420×297`, 사방 `10 mm`, 표제란 `200×30`, 사번·이름 `100+100`, 문자 높이 `10`을 mm 1:1 값과 형상으로 동기화하고 Model Space 1:1 Viewport를 구분한다.
- voiceover: "부품은 Model Space 1대1, 도면틀은 Layout 1대1로 분리하고 Viewport 축척을 잠급니다."
- media: motion-only inline SVG

`BORDER`와 `TITLE` Layer가 Layout 도면틀 객체에 적용되는 모습을 보여 주며, 시험 제공 DWT/DWG의 공간 구조가 다르면 제공 구조를 우선한다고 고지한다.

## Frame 4 — 여덟 Layer를 준비한다

- status: animated
- src: compositions/frames/04-layer.html
- duration: 150s
- poster: 26s
- transition_in: technical-cut
- scene: 여덟 Layer의 역할과 교육용 속성을 한 표로 조립한 뒤, 빈 Layout/Paper Space에서 A3 `420×297`, 사방 `10 mm` BORDER, 우측 하단 `200×30` TITLE과 `100+100` 분할·문자 높이 `10`, 잠근 Viewport, `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`, `BORDER`, `TITLE`, `HATCH`, `CONSTRUCTION`을 실제로 생성·검수한다.
- voiceover: "모든 객체를 ByLayer로 만들고 시험 지정 속성이 있으면 그 값을 우선합니다."
- media: DEMO-02 A3 border, title block and eight-layer user recording

DEMO-01을 저장한 빈 Layout/Paper Space에서 출발해 A3 도면틀·표제란·Viewport·8개 Layer를 직접 만든다. 시험 제공 DWT/DWG나 문제지 지정 구조·값이 있으면 그것을 우선하고, Layer 누락·색상·선종류 불일치가 시험 감점 위험임을 표시한다.

## Frame 5 — 정확한 점과 제3각법 작업 자리를 확인한다

- status: animated
- src: compositions/frames/05-osnap-ortho.html
- duration: 180s
- poster: 30s
- transition_in: magenta-rule-wipe
- scene: Osnap·Ortho와 정면도 위 평면도, 오른쪽 우측면도 작업 영역을 확인하고 화면 녹화로 전환한다.
- voiceover: "원점과 정확한 점을 고정하고 제3각법 뷰와 치수 공간을 먼저 확보합니다."
- media: DEMO-03 osnap, ortho and third-angle workspace user recording

다음 차시에서 사용할 현재 Layer를 `CONSTRUCTION`으로 준비한다.

## Frame 6 — L02_SETUP을 저장한다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 60s
- poster: 20s
- transition_in: magenta-rule-wipe
- scene: 템플릿·단위·A3 도면틀·표제란·전체 Layer·제3각법을 잠그고 `L02_SETUP`으로 저장한다.
- voiceover: "준비 파일은 다음 차시 정면 외곽 작성의 유일한 시작점입니다."
- media: motion-only

시험·감점 고지와 여덟 Layer를 회상하며 `L03_BASE_PROFILE`로 연결한다.
