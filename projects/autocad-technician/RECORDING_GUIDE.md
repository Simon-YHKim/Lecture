# AutoCAD Technician 누적 실습 촬영 가이드

## 촬영 원칙

모든 화면 녹화는 동일한 `EDU-SB-01` 작업 파일의 다음 체크포인트를 만든다. 기능 비교를 위한 짧은 미니 예제 뒤에는 반드시 마스터 도면에 같은 명령을 적용하고 저장한다.

- 해상도: 1920×1080
- 프레임률: 30 fps
- 녹화: 무음, 커서 표시 100–125%, 조작 전후 2초 정지
- 명령줄: 명령과 입력값을 읽을 수 있게 유지
- 개인정보: 회사 로고, 실제 도면번호, 설비명, 사용자명, 서버 경로, 라이선스 정보 비노출
- 시작 파일: 직전 차시 종료 체크포인트 또는 강사용 비공개 복구 파일
- 종료 파일: 원본을 덮어쓰지 않고 해당 차시의 `checkpoint_out`으로 SAVEAS
- 실제 DWG/DWT/DXF와 녹화 파일은 공개 저장소 밖의 승인된 비공개 저장 위치에 둔다. 공개 문서에는 그 절대 경로를 기록하지 않는다.

## DEMO 슬롯 정본

- 녹화 ID는 차시마다 `DEMO-01`부터 다시 시작하며 차시별 슬롯 수는 `2, 3, 3, 3, 2, 3, 3, 3, 3, 4`, 전체 29개다.
- 각 제목의 `F#`는 녹화를 삽입하는 실제 HTML frame 번호다. 같은 ID를 다른 frame이나 다른 작업에 재사용하지 않는다.
- 모든 슬롯은 해당 Lesson 제목에 표시된 시작 체크포인트를 열고, 목록의 작업을 수행해 종료 체크포인트 생성에 기여한다.
- 각 녹화에는 시작 체크포인트, 핵심 작업, 종료 체크포인트, 시험 문제지 우선·감점 위험을 확인할 수 있는 전후 화면을 포함한다.

## 시험 고지 오버레이

각 차시 첫 녹화에는 다음 의미를 3–5초간 표시한다.

> 교육용 템플릿·Layer 값은 기본 연습값입니다. 실제 시험의 용지, 도면틀, Layer 이름·색상·선종류·선가중치, 축척과 표제란은 문제지와 감독 지시를 우선하십시오.

각 차시 마지막 녹화에는 해당 Layer와 감점 위험 체크를 표시한다.

## 비공개 전달 구조

```text
[approved-private-storage]/autocad-technician/
├─ checkpoints\
│  ├─ L02_SETUP.dwg
│  ├─ L03_BASE_PROFILE.dwg
│  └─ ...
├─ recordings\lesson-01\ ... lesson-10\
└─ audio\lesson-01_narration.wav ... lesson-10_narration.wav
```

## Lesson 01 — `REFERENCE_READONLY → L01_FEATURE_MAP`

### `F2 · DEMO-01_exam-input-overview.mp4`

- 시작 상태: `REFERENCE_READONLY`.
- 3D 모델, 치수, 지시사항이 함께 제공된 교육용 시험 화면을 연다.
- 용지, 축척, 제3각법, 파일명과 제한시간 지시를 차례로 가리킨다.
- 완료 조건: 작도 전에 확인할 정보를 한 화면 체크리스트로 정리해 `L01_FEATURE_MAP` 작성에 넘긴다.
- 시험 맥락: 지시사항을 읽기 전에 작도를 시작하면 감점 위험이 있음을 표시한다.

### `F4 · DEMO-02_feature-layer-trace.mp4`

- 시작 상태: `REFERENCE_READONLY`와 DEMO-01에서 정리한 시험 입력.
- `EDU-SB-01`의 외형, 중심, 가려진 특징, 치수를 추적한다.
- 각각을 `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`과 연결한다.
- 종료 상태: `L01_FEATURE_MAP`.
- 시험 맥락: 제3각법 뷰와 Layer 대응 누락은 감점 위험이며 공식 지시가 우선임을 표시한다.

## Lesson 02 — `L01_FEATURE_MAP → L02_SETUP`

### `F2 · DEMO-01_template-saveas-units.mp4`

- 시작 상태: `L01_FEATURE_MAP`.
- 시험 제공 파일이 없는 연습 상황에서 `acadiso.dwt`를 선택한다.
- 교육용 파일명으로 SAVEAS하고 UNITS를 mm, Model Space를 1:1로 확인한다.
- 과정 기본은 Model Space의 정면·평면·우측면을 mm 1:1로 수동 작도·정렬하고, Layout/Paper Space에서 A3 도면틀을 mm 1:1로 구성한다. 잠근 Viewport 하나가 세 뷰 배열을 참조한다. 시험 제공 DWT/DWG의 공간 구조가 다르면 제공 구조를 우선한다.
- 종료 기여: ISO metric 파일·단위·저장 상태를 `L02_SETUP`에 누적한다.
- 시험 맥락: 제공 템플릿이 있으면 그것을 우선하며 임의 템플릿·단위 사용은 감점 위험임을 표시한다.

### `F4 · DEMO-02_a3-frame-title-layers.mp4`

- 시작 상태: DEMO-01을 저장했지만 도면틀·Viewport·사용자 Layer는 아직 없는 빈 Layout/Paper Space의 `L02_SETUP` 작업 중 파일.
- A3 가로 420×297을 설정하고 `BORDER`에서 사방 10mm 외관선을 mm 1:1로 직접 작성한다.
- `TITLE`에서 우측 하단 200×30 표제란, 사번·이름 100+100 분할과 문자 높이 10을 직접 작성한다.
- Model Space의 1:1 제3각법 작업 영역을 참조하는 단일 Viewport를 만들고 시험 지시 축척을 적용한 뒤 잠근다.
- 여덟 Layer를 직접 만든다: `OUTLINE` ACI 7·Continuous·0.50mm, `CENTER` ACI 1·CENTER2·0.25mm, `HIDDEN` ACI 3·HIDDEN2·0.25mm, `DIM` ACI 2·Continuous·0.25mm, `BORDER` ACI 7·Continuous·0.50mm, `TITLE` ACI 7·Continuous·0.25mm, `HATCH` ACI 8·Continuous·0.18mm, `CONSTRUCTION` ACI 9·Continuous·0.18mm.
- 위 값은 교육용 기본값이다. 시험 문제지나 제공 DWT/DWG가 이름·색상·선종류·선가중치 또는 공간 구조를 지정하면 그 값을 우선하고, 객체 속성은 `ByLayer`로 둔다.
- 종료 기여: A3 도면틀·표제란·8개 Layer를 `L02_SETUP`에 누적한다.
- 시험 맥락: 도면틀·표제란·필수 Layer·색상·선종류 누락은 감점 위험임을 표시한다.

### `F5 · DEMO-03_osnap-ortho-third-angle-workspace.mp4`

- 시작 상태: A3 도면틀·표제란·8개 Layer가 준비된 작업 중 파일.
- Endpoint·Midpoint·Center·Intersection Osnap과 Ortho, 원점을 확인한다.
- 정면도·평면도·우측면도의 제3각법 작업 자리와 `CONSTRUCTION` 현재 Layer를 확인한다.
- 종료 상태: `L02_SETUP`.
- 시험 맥락: 뷰 배치·축척·정확한 점 설정 불이행은 감점 위험임을 표시한다.

## Lesson 03 — `L02_SETUP → L03_BASE_PROFILE`

### `F2 · DEMO-01_line-pline-role.mp4`

- 시작 상태: `L02_SETUP`.
- 짧은 골격을 LINE과 PLINE으로 비교한 뒤 같은 EDU-SB-01 파일로 돌아온다.
- `CONSTRUCTION` 보조선과 `OUTLINE` 연속 외곽의 역할·현재 Layer·연결 상태를 확인한다.
- 종료 기여: 객체 구조 선택을 확정해 `L03_BASE_PROFILE` 작도에 넘긴다.
- 시험 맥락: 외형을 잘못된 Layer나 열린 객체로 남기면 감점 위험임을 표시한다.

### `F4 · DEMO-02_front-base-profile.mp4`

- 시작 상태: A3 도면틀·표제란·여덟 Layer는 준비됐지만 Model Space 정면도 작업 영역은 빈 `L02_SETUP` 파일.
- `CONSTRUCTION`을 현재 Layer로 두고 원점 `(0,0)`, Datum A, Datum B `X=40`, 80×50 기준 상자를 직접 작성한다.
- `OUTLINE`을 현재 Layer로 바꾸고 `(0,0) → (0,35) → (25,35) → (40,50) → (55,35) → (68,35) → (80,23) → (80,0)` 순서로 본체와 러그 직선 골격을 수치 입력한다.
- PLINE의 CLOSE를 사용해 정면 기본 외곽을 연결한다.
- 다음 차시의 R15 원호, 이후 R5·C5로 바뀔 Seed 꼭짓점임을 표시하고 좌표를 검수한다.
- 종료 기여: `L03_BASE_PROFILE`의 OUTLINE을 만든다.
- 시험 맥락: A3 제3각법 정면도 자리와 Layer·입력값 불일치가 감점 위험임을 표시한다.

### `F5 · DEMO-03_closed-layer-review.mp4`

- 시작 상태: DEMO-02의 정면 기본 외곽.
- 본체 외곽의 80×50, Closed 상태, 원점 일치와 Layer를 확인한다.
- `OUTLINE`과 `CONSTRUCTION`, Datum A·B 보존을 함께 확인한다.
- 종료 상태: `L03_BASE_PROFILE`.
- 시험 맥락: 열린 외곽·Layer 혼용·기준 치수 오류는 감점 위험임을 표시한다.

## Lesson 04 — `L03_BASE_PROFILE → L04_PRIMARY_FEATURES`

### `F2 · DEMO-01_circle-arc-slot-seed.mp4`

- 시작 상태: `L03_BASE_PROFILE`.
- 중앙 `(40,22)`에 Ø20 구멍을 만들고, 끝점 `(25,35)`·`(55,35)`, 중심 `(40,35)`, R15의 러그 원호를 같은 정면도에 만든다.
- 중심 `(40,42)`, 끝 중심 `(33,42)`·`(47,42)`, 폭 8, 전체 길이 22의 수평 장공 Seed를 만들고 필요한 `CENTER` 기준을 추가한다.
- 종료 기여: Ø20·러그 ARC·장공 Seed를 `L04_PRIMARY_FEATURES`에 누적한다.
- 시험 맥락: 중심·지름·접점·폭과 `OUTLINE/CENTER` 불일치는 감점 위험임을 표시한다.

### `F3 · DEMO-02_polygon-af30.mp4`

- 시작 상태: DEMO-01 특징이 누적된 작업 중 파일.
- `POLYGON` → 변의 개수 `6` → 중심 `(40,22)` → `Circumscribed about circle (C)` → 반지름 `15`를 입력해 중앙 Ø20과 같은 중심에 AF30 육각 포켓을 만든다.
- 마주 보는 수평 평면 간 거리 `30`, 중심 일치, 수평 면 방향, 닫힌 객체와 OUTLINE Layer를 측정·검수한다. 실제 누적 파일에는 비교용 내접 객체를 남기지 않는다.
- 종료 기여: AF30 OUTLINE을 `L04_PRIMARY_FEATURES`에 누적한다.
- 시험 맥락: 중심·AF 방식·Layer 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-03_offset-center-review.mp4`

- 시작 상태: DEMO-01·02 특징이 누적된 작업 중 파일.
- CONSTRUCTION Seed 창 `(0,10)–(24,34)`를 안쪽 5 mm OFFSET하여 최종 OUTLINE 포켓 `(5,15)–(19,29)`, 깊이 2를 만든다.
- 본체 전체 외곽은 OFFSET하지 않는다. 안쪽 방향, 14×14 닫힌 경계, Seed 창 보존, 주변 특징과의 비중첩을 확인한다.
- 종료 상태: `L04_PRIMARY_FEATURES`.
- 시험 맥락: OFFSET 방향·간격·Layer 오류와 원본 삭제는 감점 위험임을 표시한다.

## Lesson 05 — `L04_PRIMARY_FEATURES → L05_THIRD_ANGLE_VIEWS`

### `F3 · DEMO-01_third-angle-projection.mp4`

- 시작 상태: `L04_PRIMARY_FEATURES`.
- `CONSTRUCTION` 투영선으로 평면도를 정면도 위에 만든다.
- 우측면도를 정면도 오른쪽에 배치한다.
- Zoom/Pan 뒤 제3각법 배치와 뷰 정렬을 한 화면에서 확인한다.
- 종료 기여: 세 뷰 외형을 `L05_THIRD_ANGLE_VIEWS`에 누적한다.
- 시험 맥락: 뷰 위치·정렬·제3각법 불이행은 감점 위험임을 표시한다.

### `F4 · DEMO-02_outline-hidden-center.mp4`

- 시작 상태: DEMO-01의 제3각법 세 뷰.
- 각 뷰의 보이는 선은 `OUTLINE`, 가려진 구멍과 포켓은 `HIDDEN`, 축은 `CENTER`에 둔다.
- Ø20·AF30·장공 Seed·5mm OFFSET 특징을 같은 번호로 추적한다.
- 선종류 축척이 화면과 출력에서 읽히는지 확인한다.
- 종료 상태: `L05_THIRD_ANGLE_VIEWS`.
- 시험 맥락: 중심선·숨은선 누락과 Layer·선종류 불일치는 감점 위험임을 표시한다.

## Lesson 06 — `L05_THIRD_ANGLE_VIEWS → L06_PATTERNED_FEATURES`

### `F2 · DEMO-01_move-copy-seed.mp4`

- 시작 상태: `L05_THIRD_ANGLE_VIEWS`.
- Ø6 Seed를 중심 `(15,8)`에 MOVE하고, Ø6 원이 아니라 그 중심의 CONSTRUCTION 목표표시만 변위 `(50,0)`으로 COPY해 오른쪽 목표 `(65,8)`을 만든다.
- Ø6 크기, 왼쪽 OUTLINE 원 하나, CENTER 중심표시와 오른쪽 CONSTRUCTION 목표점만 있는지 확인한다. 오른쪽 Ø6 원은 아직 만들지 않는다.
- 종료 기여: 하부 장착 구멍 Seed를 `L06_PATTERNED_FEATURES`에 누적한다.
- 시험 맥락: Seed 검수 없이 복제하거나 기준점·Layer를 틀리면 감점 위험임을 표시한다.

### `F3 · DEMO-02_rotate-mirror-mount.mp4`

- 시작 상태: DEMO-01의 왼쪽 Ø6 Seed와 오른쪽 CONSTRUCTION 목표 `(65,8)`.
- OUTLINE Layer에 Ø4 Seed를 PCD 0° 중심 `(58,22)`, 지름 `4`로 만든 뒤 PCD 중심 `(40,22)` 기준 반시계 30° ROTATE해 `(55.588,31)`에 놓는다. Datum B를 기준으로 왼쪽 Ø6과 중심표시를 MIRROR해 오른쪽 목표 `(65,8)`과 일치시키고 임시 목표표시는 정리한다. AF30은 L04의 수평 면을 유지하며 수정하지 않는다.
- 원본 삭제 질문과 중심선 대칭을 확인한다.
- 종료 기여: 2×Ø6 대칭 결과를 `L06_PATTERNED_FEATURES`에 누적한다.
- 시험 맥락: 회전 중심·대칭축·원본 유지·양쪽 거리 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-03_array-three-views.mp4`

- 시작 상태: Ø6 대칭 결과와 시작각 30°·중심 `(55.588, 31)`로 검수된 Ø4 Seed.
- 중심 `(40, 22)`의 PCD Ø36에서 반시계 방향 3×Ø4 구멍을 ARRAY하고, 최종 중심 `(55.588, 31)`, `(24.412, 31)`, `(40, 4)`를 확인한다.
- 중심 `(40, 42)`·22×8의 상부 장공과 구멍이 겹치지 않는지 확인한다.
- 세 뷰의 `OUTLINE/CENTER/HIDDEN`을 함께 갱신한다.
- 종료 상태: `L06_PATTERNED_FEATURES`.
- 시험 맥락: 배열 중심·개수·360도·PCD 또는 Layer 오류는 감점 위험임을 표시한다.

## Lesson 07 — `L06_PATTERNED_FEATURES → L07_GEOMETRY_FINAL`

### `F2 · DEMO-01_trim-extend-master.mp4`

- 시작 상태: `L06_PATTERNED_FEATURES`.
- 실제 부품 OUTLINE은 L06의 닫힌 정본 그대로 보존한다. 반복 특징을 TOP/RIGHT에 반영하며 뷰 외피를 넘은 CONSTRUCTION 투영선은 TRIM하고, 짧은 HIDDEN 대응선은 정본 투상 범위까지 EXTEND한다.
- `OUTLINE/CENTER/HIDDEN`의 경계가 정확히 만나는지 확인한다.
- 종료 기여: 닫힌 경계를 `L07_GEOMETRY_FINAL`에 누적한다.
- 시험 맥락: 불필요한 선·끊긴 경계·Layer 관계 훼손은 감점 위험임을 표시한다.

### `F3 · DEMO-02_fillet-chamfer-master.mp4`

- 시작 상태: DEMO-01에서 정리한 경계.
- 어깨 R5와 하단 C5를 같은 브래킷에 적용한다.
- 입력값과 최종 외형선을 함께 확인한다.
- 종료 기여: R5·C5 OUTLINE을 `L07_GEOMETRY_FINAL`에 누적한다.
- 시험 맥락: 반지름·거리·선택 순서 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-03_scale-reference-symbol.mp4`

- 시작 상태: R5·C5가 적용된 누적 브래킷과 센서 참조 윤곽.
- 잘못된 크기의 센서 참조 윤곽만 선택해 SCALE Reference로 교정한다.
- 브래킷 본체와 1:1 모델 형상은 확대·축소하지 않는다.
- 종료 상태: `L07_GEOMETRY_FINAL`.
- 시험 맥락: 모델 1:1과 출력 축척을 혼동하거나 부품 전체를 SCALE하면 감점 위험임을 표시한다.

## Lesson 08 — `L07_GEOMETRY_FINAL → L08_REPRESENTED`

### `F2 · DEMO-01_section-hatch.mp4`

- 시작 상태: `L07_GEOMETRY_FINAL`.
- X=40 A–A 단면에서 하단 Ø4 sensorPattern `(Y 2–6, Z 0–8)`, AF30 포켓 `(Y 7–37, Z 0–4)`, 중앙 Ø20 구멍 `(Y 12–32, Z 0–8)`, 22×8 상부 장공 `(Y 38–46, Z 0–8)`의 네 빈 영역을 확인하고, 닫힌 재료 영역만 `HATCH`에 해칭한다.
- 네 빈 영역과 외부 영역이 잘못 채워지지 않았는지 검수한다.
- 종료 기여: 단면 표현을 `L08_REPRESENTED`에 누적한다.
- 시험 맥락: 열린 경계·잘못 채운 영역·HATCH Layer 누락은 감점 위험임을 표시한다.

### `F3 · DEMO-02_sensor-block-insert.mp4`

- 시작 상태: A–A HATCH와 L07에서 SCALE Reference로 목표 크기까지 교정한 센서 참조 윤곽이 있는 작업 중 파일.
- L07에서 교정한 바로 그 센서 참조 윤곽을 선택해 BLOCK으로 정의하고 설치 중심을 기준점으로 지정한다.
- INSERT 배율 1:1과 위치를 확인한다.
- 종료 기여: 센서 BLOCK 인스턴스를 `L08_REPRESENTED`에 누적한다.
- 시험 맥락: 정의 이름·기준점·포함 Layer·배율 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-03_group-title-annotation.mp4`

- 시작 상태: HATCH와 센서 BLOCK이 적용된 작업 중 파일.
- `TITLE` Layer의 A–A 라벨·리더 주석을 GROUP으로 묶고 선택 관계를 확인한다.
- 종료 기여: 주석 선택 관계를 `L08_REPRESENTED`에 누적한다.
- 시험 맥락: BLOCK과 GROUP의 역할 혼동, TITLE 주석 누락은 감점 위험임을 표시한다. `BORDER/TITLE/HATCH/OUTLINE/CENTER/HIDDEN` 전체 점검은 이어지는 Frame 5 모션 게이트에서 수행한다.
- 종료 상태: `L08_REPRESENTED`.

## Lesson 09 — `L08_REPRESENTED → L09_RELEASE_CANDIDATE`

### `F2 · DEMO-01_dimstyle-exam-values.mp4`

- 시작 상태: `L08_REPRESENTED`.
- 시험 지시의 문자 높이, 화살표, 단위, 정밀도를 DIMSTYLE에 적용한다.
- 모든 치수 객체를 `DIM`에 둔다.
- Model 1:1과 출력·뷰 축척이 서로 다른 기준임을 확인한다.
- 종료 기여: 치수 환경을 `L09_RELEASE_CANDIDATE` 제작에 넘긴다.
- 시험 맥락: DIM Layer 오용·수동 문자 덮어쓰기·지정 스타일 불일치는 감점 위험임을 표시한다.

### `F3 · DEMO-02_linear-aligned-angular-master.mp4`

- 시작 상태: DEMO-01의 DIMSTYLE과 DIM Layer.
- 80×50×8 전체 크기와 Datum A·B를 먼저 배치한다. 중앙·장공 중심 (40,22)·(40,42), 하부 구멍 중심 (15,8)·(65,8), 국부 포켓 경계 (5,15)–(19,29)를 기준 위치치수로 연결한다.
- 우측 경사의 nominal 시작 `(68,35)`·끝 `(80,23)`과 Datum A 기준 `45°`를 배치하고, R5 접선 구간 `(69.464,33.536)–(80,23)`의 실제 길이는 DIMALIGNED로 검토한다. R15 러그와 R5·C5 우측 윤곽에는 제작에 필요한 위치·크기만 남긴다.
- 기준면과 중복 치수를 확인한다.
- 종료 기여: DIMLINEAR·DIMALIGNED·DIMANGULAR 결과를 `L09_RELEASE_CANDIDATE`에 누적한다.
- 시험 맥락: Datum·측정 방향·중복·Layer 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-03_radius-diameter-review.mp4`

- 시작 상태: 선형·정렬·각도 치수가 적용된 작업 중 파일.
- R15·R5·C5, Ø20@(40,22), 같은 중심의 AF30·깊이 4, 22×8 장공@(40,42), 2×Ø6@(15,8)/(65,8), 3×Ø4·PCD Ø36·시작각 30° 반시계 방향, 14×14 포켓@(5,15)–(19,29)·깊이 2를 배치한다.
- 반지름·모따기·지름·수량·깊이 표기와 필요한 중심 위치를 검수한다. 같은 정보를 여러 뷰에 반복하지 않는다.
- 종료 상태: `L09_RELEASE_CANDIDATE`.
- 시험 맥락: 반지름·지름 혼동, 치수 누락·중복은 감점 위험임을 표시한다. 전체 축척·중복 감사는 이어지는 Frame 5 모션 게이트에서 수행한다.

## Lesson 10 — `L09_RELEASE_CANDIDATE → L10_RELEASE`

### `F3 · DEMO-01_input-a3-third-angle-layers.mp4`

- 시작 상태: `L09_RELEASE_CANDIDATE`와 시험 입력.
- 제한시간 타이머를 시작하고 3D 모델·치수·지시사항을 다시 확인한다.
- A3 도면틀·표제란, 제3각법 뷰 정렬과 `OUTLINE/CENTER/HIDDEN/DIM` 속성을 점검한다.
- 종료 기여: 입력·도면틀·투상·핵심 Layer 게이트를 닫아 `L10_RELEASE` 감사에 넘긴다.
- 시험 맥락: 제공 템플릿과 공식 지시를 우선하며 A3·제3각법·Layer 오류는 감점 위험임을 표시한다.

### `F4 · DEMO-02_geometry-hatch-block-scale.mp4`

- 시작 상태: DEMO-01 네 게이트를 통과한 릴리스 후보.
- 누적 형상, 반복 특징, A–A HATCH, 센서 BLOCK, TITLE 주석 GROUP을 점검한다.
- Model 1:1과 A3 뷰 축척·표기 일치를 확인하고 틀린 항목만 수정한다.
- 종료 기여: 형상·표현 게이트를 닫아 `L10_RELEASE` 감사에 넘긴다.
- 시험 맥락: 재작도하지 않고 형상·표현·축척 오류만 수정하며 누락은 감점 위험임을 표시한다.

### `F5 · DEMO-03_dimension-scale-file-output.mp4`

- 시작 상태: 입력·도면틀·투상·형상·표현 게이트를 통과한 릴리스 후보.
- DIM을 `① 80×50×8·Datum`, `② Ø20·AF30 깊이 4@(40,22)`, `③ 2×Ø6 위치·3×Ø4 PCD Ø36 시작각 30°`, `④ 22×8 장공@(40,42)·R15/R5/C5·우측 경사 45°·nominal (68,35)→(80,23)`, `⑤ 14×14 포켓@(5,15)–(19,29) 깊이 2`로 나눠 누락·중복·수동 덮어쓰기를 확인한다.
- 필요한 기준 위치치수와 Model 1:1·뷰 축척·축척 표기를 확인한다.
- 파일명·저장 위치와 최종 출력 미리보기를 문제지와 대조한다.
- 종료 기여: DIM·축척·파일·출력 감점 위험을 수정해 최종 감사 준비 상태로 저장한다.
- 시험 맥락: 치수·축척·파일·출력 지시 불이행은 감점 위험임을 표시한다.

### `F6 · DEMO-04_final-audit-release.mp4`

- 시작 상태: DEMO-03까지 수정된 최종 감사 준비 파일.
- 남은 시간 안에 파일을 다시 열어 입력·A3, 제3각법·Layer, 형상·표현, 치수·축척, 파일·출력의 일곱 게이트를 확인한다.
- 화면의 번호형 callout 1~5를 따라 80×50×8, Ø20·AF30 깊이 4와 중심, 22×8 장공 중심, 2×Ø6 위치, 3×Ø4·PCD Ø36·시작각 30°, R15·R5·C5, 우측 경사 45°·nominal `(68,35)→(80,23)`, 14×14 국부 포켓 위치·깊이 2가 형상과 일치하는지 최종 대조한다.
- 재작도 없이 오류만 수정했다는 전후 상태와 공식 문제지 우선 원칙을 확인한다.
- 종료 상태: `L10_RELEASE`.
- 시험 맥락: 교육용 정본과 다른 문제지 지정값은 즉시 문제지 값으로 교체한다. 남은 오류가 감점 위험인지 확인하고 실제 배점·감점은 최신 공식 기준을 우선한다.

## 전달 전 사용자 점검

- 3D 모델·치수·지시사항이 모두 교육용 합성 자료인가?
- 회사 로고·실제 도면번호·설비명·사용자명·서버 경로가 없는가?
- 시작/종료 체크포인트가 가이드와 정확히 일치하는가?
- 명령줄 입력값과 현재 Layer가 읽히는가?
- 제3각법, 외형선·중심선·숨은선·치수선 구분이 보이는가?
- A3 도면틀·표제란·축척과 감점 위험 고지가 포함되었는가?
- 실제 시험 지시가 교육용 기본값보다 우선한다는 문구가 있는가?
- 모든 녹화와 DWG를 공개 저장소 밖의 승인된 비공개 저장 위치에 두었는가?
