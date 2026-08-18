# SCRIPT — AutoCAD Technician Lesson 02

**Part:** `EDU-SB-01 교육용 센서 장착 브래킷`<br>
**Checkpoint:** `L01_FEATURE_MAP → L02_SETUP`<br>
**Voice:** 사용자 직접 녹음<br>
**Voice direction:** 시험 시작 전 설정 체크처럼 차분하고 명확하게 읽는다. 수치와 Layer 이름은 또렷하게 끊는다.

> 목표 길이는 12분입니다. 실제 나레이션과 화면 조작이 들어오면 단어 타임코드를 최종 기준으로 사용합니다.

## Line 1 — Feature Map을 작업 파일로 바꾼다 (Frame 1)

**Time:** 00:00–01:00

    두 번째 수업은 L01_FEATURE_MAP에서 시작합니다. 지난 시간에 해독한 EDU-SB-01의 형상, 치수, 지시사항을 실제로 그릴 수 있도록 ISO metric 작업 환경과 A3 도면틀을 만듭니다. 오늘 종료 체크포인트는 L02_SETUP입니다.

    시험에서는 제공 템플릿, 용지, 축척, Layer 속성이 달라질 수 있으므로 문제지와 감독 지시를 먼저 확인합니다. 과정 기본은 acadiso.dwt, millimeter, A3 가로 420 곱하기 297, 제3각법입니다. 설정 누락은 나중에 고치기 어렵고 감점 위험이 있으므로 첫 선보다 준비를 먼저 완료합니다.

## Line 2 — acadiso.dwt에서 안전하게 시작한다 (Frame 2)

**Time:** 01:00–03:00

    새 파일은 acadiso.dwt 또는 시험에서 제공된 동등한 ISO metric 템플릿으로 시작합니다. 시험 제공 파일이 있으면 임의로 새 템플릿을 열지 않습니다. 단위는 millimeter, 모델 형상은 Model Space에서 1대1로 작성합니다.

    파일을 열면 EDU-SB-01_L02_SETUP_V01처럼 교육용 이름으로 저장하고 현재 파일과 저장 위치를 다시 확인합니다. DEMO-01 · USER RECORDING에서는 템플릿 확인, SAVEAS, UNITS, 현재 파일 재확인을 순서대로 보여 줍니다.

    화면 확대와 이동은 보기를 바꿀 뿐 객체 좌표를 바꾸지 않습니다. Zoom과 Pan을 사용한 뒤 원점과 전체 도면 위치를 다시 확인합니다.

## Line 3 — A3 도면틀과 표제란을 정확한 값으로 만든다 (Frame 3)

**Time:** 03:00–05:30

    과정 기본 용지는 A3 가로형 420 곱하기 297밀리미터입니다. 과정 촬영에서는 Layout 또는 Paper Space에서 용지와 도면틀을 밀리미터 1대1로 만듭니다. BORDER Layer에서 용지 외곽을 확인하고 네 변에서 10밀리미터 안쪽에 도면 외관선을 만듭니다. 유효 외관선은 400 곱하기 277입니다. Model Space에서는 정면도, 평면도, 우측면도를 모두 1대1로 수동 작도하고 정렬하며, Layout의 잠근 Viewport 하나가 이 배열을 참조합니다.

    TITLE Layer에서는 외관선 내부 우측 하단에 폭 200, 높이 30 표제란을 만듭니다. 표제란은 사번 100, 이름 100으로 나누고 기본 문자 높이는 10밀리미터입니다. 축척, 제3각법, 도면명, 버전은 시험 지시가 허용하는 위치에 기록합니다.

    A3 420×297, 사방 10밀리미터 외관선, 표제란 200×30, 사번·이름 100+100, 문자 높이 10을 Layout 1대1 입력값으로 만들고 측정합니다. Viewport는 시험 지시 축척을 적용한 뒤 잠급니다. 시험 제공 DWT나 DWG가 Model Space 도면틀 또는 다른 Layout 구조를 지정하면 제공 구조를 그대로 따릅니다. Frame 3 모션은 입력값과 공간 구성을 먼저 설명합니다. 실제 작성은 다음 Frame의 DEMO-02에서 빈 Layout 또는 Paper Space부터 시작해 BORDER 외관선, TITLE 표제란, 잠근 Viewport와 여덟 Layer를 직접 만든 뒤 한 화면에서 검수합니다.

## Line 4 — 여덟 Layer를 한 번에 준비한다 (Frame 4)

**Time:** 05:30–08:00

    이제 전체 Layer를 만듭니다. OUTLINE은 보이는 외형, CENTER는 중심과 대칭, HIDDEN은 가려진 형상, DIM은 치수입니다. BORDER는 도면틀, TITLE은 표제란과 주석, HATCH는 단면 해칭, CONSTRUCTION은 투영과 보조선입니다.

    교육용 기본값을 정확히 입력합니다. OUTLINE은 ACI 7·Continuous·0.50밀리미터, CENTER는 ACI 1·CENTER2·0.25, HIDDEN은 ACI 3·HIDDEN2·0.25, DIM은 ACI 2·Continuous·0.25입니다. BORDER는 ACI 7·Continuous·0.50, TITLE은 ACI 7·Continuous·0.25, HATCH는 ACI 8·Continuous·0.18, CONSTRUCTION은 ACI 9·Continuous·0.18밀리미터입니다. 모든 객체 속성은 원칙적으로 ByLayer입니다. 이 값은 교육용 기본값이며 시험 문제지나 제공 DWT/DWG가 다른 값을 지정하면 그 지시가 우선합니다.

    DEMO-02 · USER RECORDING은 DEMO-01을 저장한 빈 Layout 또는 Paper Space에서 시작합니다. A3 가로 420×297을 설정하고 BORDER에서 사방 10밀리미터 외관선, TITLE에서 우측 하단 200×30 표제란과 100+100 분할·문자 높이 10을 실제로 작성합니다. 이어 Model Space의 제3각법 작업 영역을 참조하는 Viewport 하나를 만들고 잠근 뒤, OUTLINE·CENTER·HIDDEN·DIM·BORDER·TITLE·HATCH·CONSTRUCTION 여덟 Layer의 이름·색상·선종류·선가중치와 ByLayer 상태를 생성·검수합니다. 시험 제공 DWT나 DWG 또는 문제지 지정값이 있으면 그 구조와 값이 우선합니다. 필수 Layer 누락, 지정 색상 또는 선종류 불일치는 감점 위험입니다.

## Line 5 — 정확한 점과 제3각법 작업 자리를 확인한다 (Frame 5)

**Time:** 08:00–11:00

    EDU-SB-01의 원점은 본체 좌측 하단입니다. Endpoint, Midpoint, Center, Intersection Osnap을 준비하고 수평·수직 외곽에는 Ortho를 사용합니다. 클릭 전 필요한 점의 이름과 화면 표식이 일치하는지 확인합니다.

    제3각법 배치 자리를 미리 확보합니다. 정면도를 기준으로 평면도는 위, 우측면도는 오른쪽입니다. CONSTRUCTION Layer의 투영선을 사용할 공간과 DIM Layer의 치수 공간을 남깁니다.

    DEMO-03 · USER RECORDING에서는 Osnap과 Ortho 상태, 원점, 정면·평면·우측면 배치 자리, 현재 Layer를 확인합니다. 뷰 배치나 축척을 문제지와 다르게 적용하면 시험 감점 위험이 있습니다.

## Line 6 — L02_SETUP을 저장하고 외곽 작성으로 넘긴다 (Frame 6)

**Time:** 11:00–12:00

    최종 체크를 하겠습니다. acadiso.dwt와 millimeter, Model Space 부품 1대1, Layout/Paper Space 도면틀 1대1, Viewport 축척 잠금, A3 가로 420×297, 사방 10밀리미터 외관선, 우측 하단 200×30 표제란, 사번과 이름 100+100, 문자 높이 10을 확인합니다.

    OUTLINE, CENTER, HIDDEN, DIM, BORDER, TITLE, HATCH, CONSTRUCTION 여덟 Layer와 제3각법 배치 공간을 확인하고 L02_SETUP으로 저장합니다. 다음 차시에서는 이 파일을 그대로 열어 OUTLINE과 CONSTRUCTION Layer로 EDU-SB-01 정면도 기준 외곽과 러그 직선 골격을 작성합니다.
