---
workflow: general-video
flow: automation
storyboard: yes
message: "치수가 없으면 그림이지 도면이 아니다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 42m37s
angle: lesson-07-dimensioning-release
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: L06_REPRESENTED
checkpoint_out: L07_RELEASE
paper: A3-landscape
projection: third-angle
recording_slots: 1
---

## Intent

일곱 차시에 걸쳐 `EDU-IB-02 아이들러 풀리 브래킷` 하나를 완성해 온 과정의 마지막 차시다. 형상이 다 그려진 도면 위에 치수 스타일을 먼저 세우고, 선형·정렬·지름·반지름·각도 다섯 종류의 치수와 지시선으로 부품의 모든 값을 올린다. 참고 치수의 괄호와 수량 표기가 무엇을 지시하는지, 왜 같은 값을 두 번 적으면 안 되는지까지 판단 기준으로 다룬 뒤, 플롯 대화상자에서 A3 1대 1 축척을 확인하고 PDF로 내보낸다. 종료 상태는 `L07_RELEASE` 이고, 여기서 도면 한 장이 완성된다.

## Must have

- 타이틀 화면 (`LESSON_STYLE.md` 8번)
- 치수 스타일 DIMSTYLE 에서 정하는 것 — 문자 높이 · 화살표 크기 · 소수 자릿수, 그리고 각각이 무엇을 바꾸는지
- 다섯 종류 치수 명령의 선택 기준 — 선형 DIMLINEAR / 정렬 DIMALIGNED / 지름 DIMDIAMETER / 반지름 DIMRADIUS / 각도 DIMANGULAR
- 완전한 원은 지름, 원의 일부인 호는 반지름이라는 판단 근거
- 도면 위 **모든** 값의 측정 기준 — 어디서부터 어디까지 잡는가 (120·90 / 60·62 / 29·50·12·8 / Ø25 H7·Ø56·R5·R10 / PCD Ø44·45도 / (95.7)·12·20)
- 필렛이 지운 이론 모서리(목 밑동 80)를 확장 교차점 스냅으로 잡는 방법
- 지시선 MLEADER 로 뽑는 표기 — 2-C5, 4-M5 깊이 10, 그리고 왜 치수선으로는 안 되는가
- 참고 치수 괄호의 뜻 — 검사 대상이 아니라는 지시, DIMEDIT 로 (95.7) 넣기
- 조작 대본은 명령어·입력값·엔터·대화상자 항목과 고를 값까지 (`LESSON_STYLE.md` 7번), 16단계
- 1단계는 지난 차시 파일 열기, 마지막 단계는 SAVEAS 로 새 이름 저장
- PLOT 에서 A3 · 용지에 맞춤 해제 · 1대 1 확인, EXPORTPDF 로 내보내기
- 확인 화면 — 레이어 미변경 / 문자 높이 불일치 / 중복 치수 / 괄호 누락 네 가지와 각각의 확인법
- 2분할 마무리
- 인사 화면 — 「고생하셨습니다」 + 과정을 마치는 문구 (`LESSON_STYLE.md` 8번)

## Must not

- 목차나 학습 순서 안내 (1차시 소관, `LESSON_STYLE.md` 5번)
- 확정 치수표에 없는 부품 치수 값 — 필요하면 표의 값에서 계산하고 계산 과정을 밝힌다 (`LESSON_STYLE.md` 6번)
- 시험 제한시간 · 배점 · 합격 기준 언급 (확인된 바 없음)
- 체크포인트 파일명을 로드맵처럼 나열하는 것 — 실제로 타이핑하는 자리에만 (`LESSON_STYLE.md` 22번)
- 동작이 확실하지 않은 AutoCAD 명령·옵션을 추측해서 쓰는 것
- 측정값을 지우고 손으로 숫자를 쓰는 방식을 참고 치수 외의 일반 치수에 권하는 것
- 기하공차 · 표면 거칠기 기호의 실습 (개념만 언급하고 넘어간다)

## Frames

| # | 파일 | 길이 | 화면 | 비트 |
| --- | --- | --- | --- | --- |
| 1 | `01-title` | 12s | 검정 타이틀 · **치수와 출도** | — |
| 2 | `02-today` | 146s | 왼쪽 카드 4장(마크 포함) / 오른쪽 정면도 | 4 |
| 3 | `03-concept` | 157s | 개념 카드 4장 + 하단 문단 | 4 |
| 4 | `04-on-the-drawing` | 248s | 왼쪽 도면 / 오른쪽 표 6행 — 행마다 도면의 해당 위치가 붉어진다 | 6 |
| 5 | `05-demo` | 1550s | 전체화면 **녹화 삽입 영역** — 하단 띠에 진행 중인 단계와 단축키 | 16 |
| 6 | `06-check` | 151s | 확인 카드 4장 + 하단 문단 | 4 |
| 7 | `07-recap` | 156s | 2분할 마무리 | 2 |
| 8 | `08-keys` | 114s | 오늘 친 단축키 표 + 기능키 | 16 |
| 9 | `09-closing` | 23s | 인사 — 검정 바탕 · 「고생하셨습니다」 · 다음 차시 | 2 |

프레임 길이와 비트 시각은 `SCRIPT.md` 에서 계산된다 (`LESSON_STYLE.md` 13·14번). 이 표는 손으로 고치지 않는다.
