# SCRIPT — AutoCAD Technician Lesson 07

**Voice:** 사용자 직접 녹음
**Voice settings:** 원음 유지 · 잡음 제거와 음량 정규화만 적용
**Voice direction:** 차분하고 정확한 실습 강사 톤. 이번 차시는 `EDU-SB-01` 누적 도면의 형상 마감 단계임을 반복해 확인한다.

---

## Line 1 — 누적 파일을 이어서 시작한다 (Frame 1)

**Time:** 00:00–01:00
**Delivery:** 시작 체크포인트와 오늘의 종료 상태를 또렷하게 읽는다.
**화면 지시:** `EDU-SB-01 · L06_PATTERNED_FEATURES → L07_GEOMETRY_FINAL` 상태선을 표시한다.

    오늘은 새 예제를 그리지 않습니다. 지난 차시에 반복 구멍까지 배치한 EDU-SB-01의 L06_PATTERNED_FEATURES를 엽니다. A3 가로형 제3각법 도면과 OUTLINE, CENTER, HIDDEN Layer를 유지한 채 경계와 모서리를 마감해 L07_GEOMETRY_FINAL로 저장하겠습니다. 시험에서는 3D 모델, 치수, 지시사항을 먼저 확인하고 제한시간 안에 완성해야 합니다.

## Line 2 — 경계를 남길 쪽부터 판단한다 (Frame 2)

**Time:** 01:00–04:15
**Delivery:** 명령보다 남아야 할 최종 경계를 강조한다.
**화면 지시:** `DEMO-01`에서 우측 경사면과 러그 주변의 실제 누적 형상만 수정한다.

    L06_PATTERNED_FEATURES의 실제 부품 OUTLINE과 러그 R15는 이미 닫혀 있으므로 오류를 새로 만들지 않습니다. 대신 반복 구멍을 세 뷰에 반영하며 남겨 둔 CONSTRUCTION 투영선 중 뷰 외피를 넘은 부분은 TRIM하고, 새 구멍의 짧은 HIDDEN 대응선은 `master-part-geometry.json`의 투상 범위까지 EXTEND합니다. 수정 전에는 OUTLINE과 CENTER를 잠그거나 선택 대상에서 제외합니다. DEMO-01에서는 뷰 외피 경계, 제거할 CONSTRUCTION 끝, 연장할 HIDDEN 끝을 차례로 확인하고 정본 OUTLINE이 변하지 않았는지 확대 검수합니다.

## Line 3 — R5와 C5로 모서리 의도를 완성한다 (Frame 3)

**Time:** 04:15–07:30
**Delivery:** R5와 C5를 구분해 읽고 선택 순서의 의미를 설명한다.
**화면 지시:** `DEMO-02`에서 어깨 R5와 하단 C5를 같은 EDU-SB-01에 적용한다.

    경계가 닫힌 다음에 모서리를 정의합니다. DEMO-02에서 어깨는 FILLET 반지름 5로 연결하고, 하단은 CHAMFER 거리 5로 평평하게 절삭합니다. 두 결과 모두 OUTLINE Layer에 남아야 합니다. 명령 뒤에는 접선 연결, 모따기 방향, 예상하지 않은 선 삭제 여부를 확인하고 CENTER와 HIDDEN 선이 변하지 않았는지 비교합니다.

## Line 4 — 부품이 아니라 센서 참조 윤곽만 교정한다 (Frame 4)

**Time:** 07:30–10:30
**Delivery:** “전체 부품을 SCALE하지 않는다”를 분명히 경고한다.
**화면 지시:** `DEMO-03`에서 센서 참조 윤곽을 별도 선택하고 Reference로 목표 길이에 맞춘다.

    SCALE은 EDU-SB-01 전체 형상의 크기를 바꾸는 명령으로 사용하지 않습니다. 전체 부품을 확대하면 80 곱하기 50 본체와 구멍 지름, R5, C5까지 모두 틀어집니다. DEMO-03에서는 외부에서 가져온 센서 참조 윤곽만 선택하고 조립 기준점을 고정한 뒤 Reference 옵션으로 현재 길이와 목표 길이를 입력합니다. 교정 뒤에는 부품 치수는 그대로이고 참조 윤곽만 목표 크기가 되었는지 측정합니다.

## Line 5 — L07 형상 마감 게이트를 통과한다 (Frame 5)

**Time:** 10:30–13:30
**Delivery:** 학습자가 화면을 멈추고 직접 검수할 시간을 준다.
**화면 지시:** EDU-SB-01의 다섯 점검 위치와 20초 자가 실습을 표시한다.

    이제 EDU-SB-01을 한 화면에서 점검합니다. 투영선 TRIM 경계, HIDDEN EXTEND 도달점, 어깨 R5, 하단 C5, 센서 참조 윤곽 Reference를 순서대로 확인하세요. OUTLINE은 L06 정본에서 이어져 닫혀 있고, CENTER는 원과 대칭축을 설명하며, HIDDEN은 다른 뷰의 가려진 특징을 정확한 범위로 유지해야 합니다. 화면을 멈추고 다섯 항목을 직접 확인한 뒤 L07_GEOMETRY_FINAL로 저장합니다.

## Line 6 — 감점 위험을 지우고 다음 상태로 넘긴다 (Frame 6)

**Time:** 13:30–14:15
**Delivery:** 시험 고지와 다음 체크포인트를 차분하게 연결한다.
**화면 지시:** `L07_GEOMETRY_FINAL → L08_REPRESENTED`를 표시한다.

    오늘은 L06_PATTERNED_FEATURES를 L07_GEOMETRY_FINAL로 발전시켰습니다. 시험에서는 제3각법 불이행, 축척 오류, A3 외관선과 표제란 누락, Layer 이름·색상·선종류·선가중치 오류, 지시사항 불이행이 감점 위험입니다. 실제 기준은 공식 문제지를 우선합니다. 다음 차시에는 이 형상을 다시 그리지 않고 같은 파일에 A–A 단면 표현과 재사용 요소를 더하겠습니다.
