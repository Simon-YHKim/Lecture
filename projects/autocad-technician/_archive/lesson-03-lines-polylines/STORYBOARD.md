---
format: 1920x1080
duration: 12m
message: "L02_SETUP에서 OUTLINE과 CONSTRUCTION으로 EDU-SB-01 정면 기준 외곽을 작성한다."
arc: "설정 인계 → 객체 구조 → 원점·Datum → 80×50 외곽 → 러그·폐곡선 검수 → 체크포인트 저장"
audience: "A3 시험 작업 환경을 준비한 Technician 실습과정 입문 수강자"
mode: autonomous
---

## Frame 1 — L02_SETUP에서 정면도를 시작한다

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 18s
- transition_in: cut
- scene: `EDU-SB-01 · L02_SETUP → L03_BASE_PROFILE`, A3 제3각법 정면도 자리와 `OUTLINE · CONSTRUCTION` 역할을 소개한다.
- voiceover: "준비된 파일 위에 오늘의 형상만 누적합니다."
- media: motion-only

시험 지정 Layer와 뷰 위치 불이행이 감점 위험임을 도입부에 표시한다.

## Frame 2 — LINE과 PLINE을 제작 역할로 선택한다

- status: animated
- src: compositions/frames/02-line-vs-pline.html
- duration: 150s
- poster: 28s
- transition_in: magenta-rule-wipe
- scene: CONSTRUCTION 보조선은 LINE, OUTLINE 연속 외곽은 PLINE으로 구분하고 화면 녹화로 이어진다.
- voiceover: "명령이 아니라 다음 작업에서 객체를 어떻게 관리할지 보고 선택합니다."
- media: DEMO-01 LINE and PLINE role comparison user recording

짧은 비교 뒤 반드시 같은 `EDU-SB-01` 누적 작업 파일로 돌아온다.

## Frame 3 — 원점과 Datum을 좌표로 고정한다

- status: animated
- src: compositions/frames/03-coordinate-input.html
- duration: 150s
- poster: 30s
- transition_in: magenta-rule-wipe
- scene: 원점 `0,0`, Datum A 하단, Datum B `X=40`, `@80,0`, `@0,50`을 CONSTRUCTION 평면에 그린다.
- voiceover: "숫자보다 원점 기준과 현재점 기준을 먼저 확인합니다."
- media: motion-only inline SVG

A3 도면틀과 TITLE 객체는 이전 상태로 유지하고 모델 영역만 갱신한다.

## Frame 4 — 80×50 기준 상자와 정면 외곽을 작성한다

- status: animated
- src: compositions/frames/04-rectangle-values.html
- duration: 150s
- poster: 28s
- transition_in: technical-cut
- scene: A3 도면틀·표제란·Layer만 준비되고 Model Space 정면도 영역은 빈 `L02_SETUP`에서 CONSTRUCTION 원점·Datum A·Datum B·80×50 기준 상자를 직접 만든 뒤, OUTLINE PLINE으로 본체와 러그 직선 골격을 입력하고 CLOSE한다.
- voiceover: "기준 상자와 최종 외곽을 다른 Layer로 분리해 다음 특징의 기준을 남깁니다."
- media: DEMO-02 base profile user recording

빈 Model Space에서 `CONSTRUCTION → OUTLINE → PLINE → CLOSE`로 이어지는 실제 누적 제작 순서를 화면 상단에 고정한다.

## Frame 5 — 러그 골격과 폐곡선 상태를 검수한다

- status: animated
- src: compositions/frames/05-closed-contour.html
- duration: 150s
- poster: 30s
- transition_in: magenta-rule-wipe
- scene: 러그 접점, 우측 경사면, 80×50, 하나의 OUTLINE 객체, Closed 상태와 CONSTRUCTION 보존을 확인한다.
- voiceover: "보이는 모양이 아니라 Layer, 기준, 연결, 닫힘을 검수합니다."
- media: DEMO-03 checkpoint and closed-boundary user recording

시험 감점 위험 항목인 Layer 오배치와 지시 불이행을 함께 확인한다.

## Frame 6 — L03_BASE_PROFILE로 저장한다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 60s
- poster: 20s
- transition_in: magenta-rule-wipe
- scene: `OUTLINE · CONSTRUCTION` 결과를 `L03_BASE_PROFILE`로 잠그고 다음 차시 원·호·포켓·장공 작업을 예고한다.
- voiceover: "오늘의 정면 골격이 다음 차시 모든 중심과 곡선 특징의 기준이 됩니다."
- media: motion-only

A3 가로형, 제3각법, 시험·감점 고지와 체크포인트 연속성을 한 화면에서 회상한다.
