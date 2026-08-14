---
format: 1920x1080
duration: 10m
message: "3D 모델·치수·지시사항을 해독해 EDU-SB-01 제작 순서를 계획한다."
arc: "누적 부품 공개 → 3D 형상 → 치수 → 지시사항·Layer → 제3각법 → Feature Map"
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
mode: autonomous
---

## Frame 1 — 열 차시의 하나뿐인 부품

- status: animated
- src: compositions/frames/01-course-orientation.html
- duration: 60s
- poster: 18s
- transition_in: cut
- scene: `EDU-SB-01`의 3D 합성 모델과 전체 10차시 누적 경로, `REFERENCE_READONLY → L01_FEATURE_MAP`을 제시한다.
- voiceover: "시험 문제를 읽고 하나의 부품을 열 차시에 걸쳐 완성합니다."
- media: motion-only inline SVG

3D 모델·치수·지시사항 세 입력과 A3 가로형·제3각법 기본을 화면의 실제 학습 정보로 표시한다.

## Frame 2 — 3D 모델에서 제작 특징을 찾는다

- status: animated
- src: compositions/frames/02-drawing-purpose.html
- duration: 120s
- poster: 24s
- transition_in: magenta-rule-wipe
- scene: 베이스·중앙 센서부·장착부·러그·경사면을 분해하고 첫 화면 녹화로 문제 전체를 탐색한다.
- voiceover: "큰 덩어리에서 기준과 세부 특징으로 내려가며 제작 순서를 만듭니다."
- media: DEMO-01 REFERENCE_READONLY to L01_FEATURE_MAP exam-input user recording

Datum A와 Datum B를 고정하고 실제 자료를 복제하지 않은 인라인 SVG만 사용한다.

## Frame 3 — 숫자를 형상과 기준에 연결한다

- status: animated
- src: compositions/frames/03-line-types.html
- duration: 120s
- poster: 30s
- transition_in: magenta-rule-wipe
- scene: `80×50×8`, `Ø20`, `AF30`, `2×Ø6`, `3×Ø4 PCD Ø36`, `R5`, `C5`, 장공 폭 8을 특징에 연결한다.
- voiceover: "치수는 숫자가 아니라 어느 특징을 어느 기준에서 검수할지 정하는 관계입니다."
- media: motion-only inline SVG

치수는 DIM 정보로 읽되 아직 작도하지 않는다는 상태를 명확히 한다.

## Frame 4 — 지시사항과 Layer를 제작 규칙으로 바꾼다

- status: animated
- src: compositions/frames/04-three-views.html
- duration: 120s
- poster: 28s
- transition_in: magenta-rule-wipe
- scene: `OUTLINE`, `CENTER`, `HIDDEN`, `DIM`의 역할을 같은 부품에 적용하고 두 번째 녹화에서 세 뷰 대응을 확인한다.
- voiceover: "선종류와 Layer는 형상의 상태와 제작 정보를 구분하는 시험 규칙입니다."
- media: DEMO-02 REFERENCE_READONLY to L01_FEATURE_MAP third-angle and layer-mapping user recording

제3각법은 정면도 위 평면도, 정면도 오른쪽 우측면도로 표시한다.

## Frame 5 — 시험 지시와 감점 위험을 확인한다

- status: animated
- src: compositions/frames/05-dimension-note-check.html
- duration: 120s
- poster: 22s
- transition_in: technical-cut
- scene: 문제지 우선 원칙과 용지·축척·외관선·표제란·Layer·뷰 배치의 감점 위험을 체크한다.
- voiceover: "과정 기본값보다 시험 문제지와 감독 지시가 우선입니다."
- media: motion-only guided practice

화면을 멈추고 3D 모델·치수·지시사항을 모두 읽었는지 직접 확인하게 한다.

## Frame 6 — Feature Map을 다음 차시로 넘긴다

- status: animated
- src: compositions/frames/06-recap.html
- duration: 60s
- poster: 20s
- transition_in: magenta-rule-wipe
- scene: `L01_FEATURE_MAP`에 형상·치수·지시·뷰·Layer가 잠기고 `L02_SETUP` 준비로 연결된다.
- voiceover: "오늘 해독한 제작 지도가 다음 차시 작업 환경의 입력이 됩니다."
- media: motion-only

`EDU-SB-01`, A3 가로형, 제3각법, `OUTLINE · CENTER · HIDDEN · DIM`, 시험·감점 고지를 한 화면에서 회상한다.
