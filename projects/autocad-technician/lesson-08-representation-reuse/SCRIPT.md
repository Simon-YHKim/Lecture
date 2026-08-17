# SCRIPT — AutoCAD Technician Lesson 08

**Voice:** 사용자 직접 녹음
**Voice settings:** 원음 유지 · 잡음 제거와 음량 정규화만 적용
**Voice direction:** 명령 기능보다 같은 `EDU-SB-01` 도면의 표현·관리 목적을 먼저 설명한다.

---

## Line 1 — 완성 형상에 표현 정보를 더한다 (Frame 1)

**Time:** 00:00–01:00
**Delivery:** 누적 상태와 여섯 Layer를 천천히 읽는다.
**화면 지시:** `EDU-SB-01 · L07_GEOMETRY_FINAL → L08_REPRESENTED` 상태선을 표시한다.

    EDU-SB-01의 L07_GEOMETRY_FINAL에서 계속합니다. 이번 차시는 A3 가로형 제3각법 도면의 형상을 다시 그리지 않습니다. BORDER, TITLE, HATCH, OUTLINE, CENTER, HIDDEN Layer를 점검하면서 A–A 단면, 센서 심볼, 주석 묶음을 더해 L08_REPRESENTED를 만들겠습니다. 시험 입력은 3D 모델, 치수, 지시사항이며 제한시간이 있습니다.

## Line 2 — A–A 단면은 HATCH Layer로 표현한다 (Frame 2)

**Time:** 01:00–03:30
**Delivery:** 단면 경계와 해칭 의미를 분리한다.
**화면 지시:** `DEMO-01`에서 A–A 닫힌 경계와 HATCH Layer 적용을 보여 준다.

    DEMO-01에서는 같은 EDU-SB-01의 A–A 단면을 확대합니다. X=40 절단면이 통과하는 PCD Ø36 하단 Ø4 관통 구멍 Y 2–6, AF30 깊이 4 포켓 Y 7–37, 중앙 Ø20 관통 구멍 Y 12–32, 22×8 상부 장공 Y 38–46의 네 빈 영역을 확인합니다. 먼저 OUTLINE 경계가 닫혀 있는지 확인하고 HATCH Layer를 현재 Layer로 전환합니다. 절단된 재료 영역에만 해칭을 적용하며 네 빈 영역은 채우지 않습니다. 해칭이 새어 나가면 패턴을 바꾸기 전에 경계 틈을 찾고, CENTER와 HIDDEN의 의미가 단면 표현과 충돌하지 않는지 확인합니다.

## Line 3 — 센서 심볼은 하나의 BLOCK 정의로 관리한다 (Frame 3)

**Time:** 03:30–06:30
**Delivery:** 정의와 인스턴스의 관계를 명확히 읽는다.
**화면 지시:** `DEMO-02`에서 센서 참조 심볼을 BLOCK으로 만들고 INSERT한다.

    DEMO-02에서는 L07 DEMO-03에서 SCALE Reference로 목표 크기까지 교정한 바로 그 센서 참조 윤곽을 선택해 BLOCK으로 정의합니다. 기준점은 조립 기준과 맞는 CENTER 교차점으로 선택하고 이름은 교육용 규칙에 맞춥니다. INSERT한 인스턴스는 OUTLINE과 CENTER 관계를 유지합니다. 나중에 심볼을 수정해야 할 때 개별 복사본을 고치는 것이 아니라 하나의 정의를 갱신한다는 점을 확인합니다.

## Line 4 — 주석 객체는 GROUP으로 선택 관계만 묶는다 (Frame 4)

**Time:** 06:30–08:30
**Delivery:** BLOCK과 GROUP의 차이를 짧고 분명하게 말한다.
**화면 지시:** `DEMO-03`에서 TITLE Layer의 주석 묶음을 GROUP으로 선택한다.

    DEMO-03에서는 HATCH와 센서 BLOCK이 적용된 작업 중 파일에서 A–A 라벨과 리더 같은 주석 객체를 TITLE Layer의 GROUP으로 묶어 L08_REPRESENTED에 누적합니다. GROUP은 선택 편의를 위한 관계이며 BLOCK처럼 하나의 재사용 정의를 공유하지 않습니다. 선택 묶음을 해제해도 원래 객체가 남는지, 표제란 안의 정보와 주석이 서로 침범하지 않는지 확인합니다. BLOCK·GROUP 역할 혼동과 TITLE 주석 누락은 시험 감점 위험입니다.

## Line 5 — BORDER와 TITLE까지 같은 도면에서 점검한다 (Frame 5)

**Time:** 08:30–10:15
**Delivery:** 도면틀 검수가 형상 검수와 같은 중요도임을 강조한다.
**화면 지시:** 420×297 A3 외관선과 우측 하단 표제란, 여섯 Layer 체크를 표시한다.

    표현이 끝났다면 도면 전체로 돌아옵니다. BORDER Layer의 A3 가로형 420 곱하기 297 외관선과 TITLE Layer의 우측 하단 표제란을 확인합니다. HATCH는 A–A 단면에만, OUTLINE은 보이는 형상에, CENTER는 중심에, HIDDEN은 가려진 특징에 있어야 합니다. 이 여섯 Layer를 통과하면 L08_REPRESENTED로 저장합니다.

## Line 6 — 표현 누락은 시험 감점으로 이어진다 (Frame 6)

**Time:** 10:15–11:00
**Delivery:** 공식 지시 우선 원칙을 분명히 한다.
**화면 지시:** `L08_REPRESENTED → L09_RELEASE_CANDIDATE`를 표시한다.

    A3 외관선, 표제란과 주석칸, 지정 Layer, 색상과 선종류, 제3각법 배치, 축척을 누락하면 시험에서 감점 위험이 있습니다. 실제 항목과 배점은 공식 문제지와 최신 공지를 우선합니다. 다음 차시에는 L08_REPRESENTED를 그대로 열어 DIM Layer에 제작·검사용 치수를 배치하고 축척을 검수하겠습니다.
