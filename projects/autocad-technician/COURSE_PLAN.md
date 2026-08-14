# AutoCAD Technician 누적 제작 과정

## Production baseline

- Audience: CAD 입문 Technician 및 작업형 CAD 시험 준비자
- Format: 1920×1080, 30 fps, 사용자 한국어 나레이션
- Delivery: HyperFrames 모션그래픽 + 사용자 녹화 AutoCAD 실습
- Master part: `EDU-SB-01 교육용 센서 장착 브래킷`
- Master specification: `MASTER_DRAWING_SPEC.md`
- Continuity ledger: `course-continuity.json`
- Drawing startup: `acadiso.dwt` 또는 시험에서 제공하는 동등한 ISO metric 템플릿
- Course paper: ISO A3 landscape, 420×297 mm
- Projection: 과정 기본은 시험 지시사항에 따른 제3각법
- Core layers: `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`
- Public boundary: 대본, 스토리보드, composition HTML, 공개 가능한 추상 SVG와 합성 규격
- Private boundary: PPT, 실제 DWG/DXF/DWT, LG 폰트 바이너리, 녹화, 나레이션, 전사, 스냅샷, 렌더
- Rendering remains blocked until real recordings and narration are synchronized and the final Studio preview is approved.

## 용지명 정정

사용자가 제시한 `297×420 mm`와 캡처의 가로형 비율을 우선한다. 이 크기는 **A3**이며 가로 배치는 `420×297 mm`다. A2는 `594×420 mm`이므로 본 과정에서 A2라고 잘못 표기하지 않는다.

## 과정 공통 시험 고지

시험에서는 3D 모델, 치수, 지시사항이 함께 제공되며 제한시간 안에 도면을 완성해야 한다. 도면 템플릿, 용지 크기, Layer 이름·색상·선종류·선가중치, 축척과 표제란은 시험마다 달라질 수 있다. 강의의 교육용 기본값을 외운 뒤 그대로 적용하는 것이 아니라 **해당 회차 문제지와 감독 지시를 먼저 읽고 값만 교체하는 능력**을 목표로 한다.

본 과정이 대비하는 시험에서는 다음을 감점 위험 항목으로 반복 검수한다.

- 제3각법 뷰 배치 불이행
- 외형선·중심선·숨은선·치수선의 Layer 오적용 또는 누락
- 축척 미설정·오류 또는 축척 표기 누락
- 용지 외관선 누락·크기 오류
- 표제란·주석칸 미설정
- 필수 Layer 항목 누락
- 지정 색상 불일치
- 지정 선종류 불일치
- 문제지의 치수·파일명·저장·출력 지시 불이행

구체적인 배점과 감점 기준은 최신 공식 문제지와 공지를 우선한다.

## 누적 작업 흐름

```text
REFERENCE_READONLY
  → L01_FEATURE_MAP
  → L02_SETUP
  → L03_BASE_PROFILE
  → L04_PRIMARY_FEATURES
  → L05_THIRD_ANGLE_VIEWS
  → L06_PATTERNED_FEATURES
  → L07_GEOMETRY_FINAL
  → L08_REPRESENTED
  → L09_RELEASE_CANDIDATE
  → L10_RELEASE
```

각 강의는 네 질문으로 시작하고 끝난다.

1. 이전 차시에서 무엇이 완성되었는가?
2. 오늘 어떤 형상 또는 정보를 추가하는가?
3. 어떤 Layer와 시험 지시를 검수하는가?
4. 어떤 체크포인트 이름으로 저장하고 다음 차시에 넘기는가?

화면 녹화 ID는 차시 안에서만 `DEMO-01`부터 다시 시작한다. HTML frame의 ID·작업을 정본으로 삼으며 차시별 슬롯 수는 `2, 3, 3, 3, 2, 3, 3, 3, 3, 4`, 전체 29개다. 아래 `Recording cues`의 `F#`는 실제 녹화 플레이스홀더가 있는 frame 번호다. 각 녹화는 해당 차시 `Checkpoint`의 시작 파일에서 출발해 표시된 작업을 수행하고, 종료 체크포인트 생성에 기여한다. 시험 문제지 우선 및 해당 `Deduction gate` 고지를 같은 녹화 문맥으로 유지한다.

## Module 1 — 문제 해독과 도면 환경

### Lesson 01 — 시험 도면을 제작 순서로 읽기

- Project: `lesson-01-drawing-language`
- Duration: 10:00
- Checkpoint: `REFERENCE_READONLY → L01_FEATURE_MAP`
- Production step: 제공된 3D 모델·치수·지시사항에서 기준 뷰, 전체 크기, 구멍, 반복, 모서리, 축척, 용지·표제란 지시를 추출한다.
- Layers preview: `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`
- Practice result: `EDU-SB-01` Feature ID와 실제 제작 순서가 표시된 작업 지도
- Recording cues: `F2 · DEMO-01` 3D 모델·치수·지시사항 탐색, `F4 · DEMO-02` 제3각법 뷰와 `OUTLINE/CENTER/HIDDEN/DIM` 대응 추적
- Deduction gate: 지시사항을 읽기 전에 작도를 시작하지 않는다.

### Lesson 02 — ISO metric 환경과 A3 도면틀 만들기

- Project: `lesson-02-work-environment`
- Duration: 12:00
- Checkpoint: `L01_FEATURE_MAP → L02_SETUP`
- Production step: `acadiso.dwt`, mm, A3 420×297, 사방 10mm 외관선, 우측 하단 200×30 표제란을 준비한다.
- Title block: `사번` 100mm + `이름` 100mm, 교육용 문자 높이 10mm
- Layers: `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`, `BORDER`, `TITLE`, `HATCH`, `CONSTRUCTION`
- Practice result: 모든 Layer와 도면틀이 준비된 누적 작업 파일
- Recording cues: `F2 · DEMO-01` `acadiso.dwt`·SAVEAS·UNITS·Model 1:1, `F4 · DEMO-02` 빈 Layout부터 A3 도면틀·표제란·잠근 Viewport·8개 Layer 직접 작성, `F5 · DEMO-03` Osnap·Ortho·원점·제3각법 작업 자리
- Deduction gate: 시험 제공 템플릿이 있으면 제공 파일을 우선하며 교육용 기본값을 강제로 덮어쓰지 않는다.

## Module 2 — 기준 뷰와 세부 형상

### Lesson 03 — 정면도 기준 외곽 만들기

- Project: `lesson-03-lines-polylines`
- Duration: 12:00
- Checkpoint: `L02_SETUP → L03_BASE_PROFILE`
- Production step: `OUTLINE`과 `CONSTRUCTION`을 구분해 80×50 본체와 러그 직선 골격을 1:1로 작성한다.
- Topics: LINE, PLINE, RECTANGLE, 절대·상대 좌표, Closed 검수
- Recording cues: `F2 · DEMO-01` LINE/PLINE 역할 비교 후 누적 파일 적용, `F4 · DEMO-02` 빈 Model Space에서 CONSTRUCTION 원점·Datum A/B·80×50 기준 상자 후 OUTLINE PLINE·CLOSE, `F5 · DEMO-03` Closed·`OUTLINE/CONSTRUCTION`·Datum 검수
- Deduction gate: 외형 객체가 Layer 0 또는 잘못된 Layer에 남지 않는다.

### Lesson 04 — 원·호·포켓·간격 추가하기

- Project: `lesson-04-curves-offset`
- Duration: 12:00
- Checkpoint: `L03_BASE_PROFILE → L04_PRIMARY_FEATURES`
- Production step: 같은 정면도에 Ø20 구멍, AF30 육각 포켓, 러그 원호, 장공 Seed와 좌측 국소 5mm Offset 포켓을 추가한다.
- Layers: `OUTLINE`, `CENTER`, `CONSTRUCTION`
- Topics: CIRCLE, ARC, POLYGON, OFFSET, 반지름·지름·방향
- Recording cues: `F2 · DEMO-01` Ø20·R15 러그 ARC·22×8 장공 Seed, `F3 · DEMO-02` AF30 육각 포켓, `F4 · DEMO-03` 좌측 국소 Seed 창 내부 5 mm OFFSET·비중첩 검수
- Deduction gate: 원에는 중심선을 준비하고 Offset 방향·간격을 측정한다.

### Lesson 05 — 제3각법으로 평면도·우측면도 투상하기

- Project: `lesson-05-orthographic-reading`
- Duration: 13:00
- Checkpoint: `L04_PRIMARY_FEATURES → L05_THIRD_ANGLE_VIEWS`
- Production step: 정면도를 기준으로 평면도를 위, 우측면도를 오른쪽에 배치한다.
- Layers: `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`
- Topics: 정투상, 뷰 정렬, 숨은선·중심선, 동일 특징 추적
- Recording cues: `F3 · DEMO-01` 제3각법 세 뷰 투영·정렬과 Zoom/Pan, `F4 · DEMO-02` Ø20·AF30·장공·OFFSET의 `OUTLINE/CENTER/HIDDEN` 추적
- Deduction gate: 제3각법 위치와 같은 특징의 수평·수직 정렬을 검수한다.

## Module 3 — 반복·수정·표현

### Lesson 06 — 반복 특징 배치하기

- Project: `lesson-06-placement-repetition`
- Duration: 13:00
- Checkpoint: `L05_THIRD_ANGLE_VIEWS → L06_PATTERNED_FEATURES`
- Production step: 검증된 Seed 구멍을 이동·복사·대칭·배열하고 세 뷰의 숨은선과 중심선을 갱신한다.
- Layers: `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`
- Topics: MOVE, COPY, ROTATE, MIRROR, ARRAY
- Recording cues: `F2 · DEMO-01` Ø6 Seed MOVE·CONSTRUCTION 목표점 `(50,0)` COPY, `F3 · DEMO-02` Ø4 0° Seed 작성·시작각 30° ROTATE·Datum B Ø6 MIRROR·AF30 수평 면 유지, `F4 · DEMO-03` 3×Ø4·PCD Ø36 Polar ARRAY·세 뷰 갱신
- Deduction gate: 복제 전 Seed 크기와 Layer를 검수한다.

### Lesson 07 — 형상 마감하기

- Project: `lesson-07-object-editing`
- Duration: 14:15
- Checkpoint: `L06_PATTERNED_FEATURES → L07_GEOMETRY_FINAL`
- Production step: 닫힌 정본 OUTLINE은 유지하고, 뷰 외피 밖 CONSTRUCTION 투영선·짧은 HIDDEN 대응선을 정리한 뒤 R5·C5를 적용한다.
- Layers: `OUTLINE`, `CENTER`, `HIDDEN`, `CONSTRUCTION`
- Topics: TRIM, EXTEND, FILLET, CHAMFER, SCALE Reference
- SCALE rule: 전체 부품을 확대·축소하지 않고 잘못 삽입된 센서 참조 윤곽만 실제 기준 길이에 맞춘다.
- Recording cues: `F2 · DEMO-01` TRIM/EXTEND·CENTER/HIDDEN 보존, `F3 · DEMO-02` FILLET R5·CHAMFER C5, `F4 · DEMO-03` 센서 참조 윤곽만 SCALE Reference
- Deduction gate: 모델 형상 1:1과 출력 축척을 혼동하지 않는다.

### Lesson 08 — 단면·재사용·표제란 정리하기

- Project: `lesson-08-representation-reuse`
- Duration: 11:00
- Checkpoint: `L07_GEOMETRY_FINAL → L08_REPRESENTED`
- Production step: 같은 도면의 A–A 단면에 Hatch를 적용하고 센서 심볼을 Block으로, 주석 묶음을 Group으로 관리한다.
- Layers: `BORDER`, `TITLE`, `HATCH`, `OUTLINE`, `CENTER`, `HIDDEN`
- Topics: HATCH, BLOCK, INSERT, GROUP, 표제란·주석칸 검수
- Recording cues: `F2 · DEMO-01` A–A 닫힌 경계 HATCH, `F3 · DEMO-02` 센서 심볼 BLOCK/INSERT, `F4 · DEMO-03` TITLE 주석 GROUP 선택 관계
- Deduction gate: 외관선·표제란·주석칸과 필수 Layer 누락을 점검한다.

## Module 4 — 치수·축척·제한시간 검수

### Lesson 09 — 제작·검사용 치수와 축척 확정하기

- Project: `lesson-09-dimensioning`
- Duration: 14:00
- Checkpoint: `L08_REPRESENTED → L09_RELEASE_CANDIDATE`
- Production step: 같은 `EDU-SB-01`에 전체·위치·지름·반지름·각도 치수를 배치하고 축척을 검수한다.
- Layers: `DIM`, `OUTLINE`, `CENTER`
- Topics: DIMSTYLE, DIMLINEAR, DIMALIGNED, DIMANGULAR, DIMRADIUS, DIMDIAMETER
- Recording cues: `F2 · DEMO-01` DIMSTYLE·DIM Layer·Model 1:1, `F3 · DEMO-02` DIMLINEAR·DIMALIGNED·DIMANGULAR, `F4 · DEMO-03` DIMRADIUS·DIMDIAMETER·수량 표기 검수
- Deduction gate: 치수 문자 수동 덮어쓰기와 축척 오표기를 금지한다.

### Lesson 10 — 제한시간 모의시험과 최종 출도

- Project: `lesson-10-final-bracket`
- Duration: 19:00
- Checkpoint: `L09_RELEASE_CANDIDATE → L10_RELEASE`
- Production step: 새로운 파일을 처음부터 다시 그리지 않고 누적 파일을 제한시간 안에 검사·수정·저장한다.
- Exam input: 3D 모델 + 치수 + 지시사항
- Layers: `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`, `BORDER`, `TITLE`, `HATCH`
- Recording cues: `F3 · DEMO-01` 입력·A3·BORDER/TITLE·제3각법·핵심 Layer, `F4 · DEMO-02` 누적 형상·HATCH/BLOCK/GROUP·Model 1:1·뷰 축척, `F5 · DEMO-03` DIM·축척·파일·출력, `F6 · DEMO-04` 재개방·7게이트 최종 감사·`L10_RELEASE` 승인
- Deduction gate: 모든 지시 항목을 체크리스트로 확인하고 남은 시간 안에 재검수한다.

## Per-project completion gate

1. `BRIEF.md`, `SCRIPT.md`, `STORYBOARD.md`, `frame.md`가 존재한다.
2. BRIEF에 `part_id`, `checkpoint_in`, `checkpoint_out`, `paper`, `projection`이 있다.
3. `checkpoint_out(Lesson N) = checkpoint_in(Lesson N+1)`이다.
4. 각 차시는 여섯 장면과 여섯 motion sidecar를 유지한다.
5. 시작 화면은 이전 상태, 마지막 화면은 다음 체크포인트를 보여 준다.
6. 해당 차시의 Layer와 시험·감점 고지가 대본·스토리보드·영상에 반영된다.
7. `npm run check`가 error 0, warning 0으로 통과한다.
8. 장면 중간점 contact sheet를 육안 검수한다.
9. private-material guard와 secret scan이 통과한다.
10. 실제 촬영·나레이션 동기화와 Studio 승인 전에는 렌더·push하지 않는다.
