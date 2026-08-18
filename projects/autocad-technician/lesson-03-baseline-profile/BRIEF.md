---
workflow: general-video
flow: automation
storyboard: yes
message: "정확하게 그린다는 것은 점을 정확하게 찍는다는 뜻이고, 기준선은 형상보다 먼저 선다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 29m05s
angle: lesson-03-baseline-profile
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: L02_TEMPLATE
checkpoint_out: L03_PROFILE
paper: A3-landscape
projection: third-angle
recording_slots: 1
---

## Intent

지난 차시에 만든 A3 템플릿 파일을 열어 `EDU-IB-02 아이들러 풀리 브래킷`의 정면 외곽을 처음으로 작도하는 차시다. 학습자는 좌표 원점을 정면도 자리로 옮기고, 중심선을 먼저 세운 뒤, 절대좌표·상대좌표·상대극좌표 세 가지 입력 방식과 LINE·PLINE의 차이를 구분해 가며 베이스 120×16 외곽과 모따기 2-C5, 보스 원 Ø56, 목 접선을 그린다. 접선은 좌표를 계산하지 않고 객체 스냅의 접점으로 잡는다는 것이 이 차시의 핵심 조작이다. 종료 상태는 `L03_PROFILE`.

## Must have

- 타이틀 화면 (`LESSON_STYLE.md` 8번)
- 오늘 그릴 것 카드 4장 — 중심선 / 베이스 120×16 외곽 / 모따기 2-C5 / 보스 원 Ø56과 목 접선
- 좌표 입력 세 방식 — 절대 `x,y` · 상대 `@dx,dy` · 상대극 `@거리<각도` — 각각 언제 쓰는지와 그 이유
- LINE 과 PLINE 의 차이, 그리고 외곽을 폴리선 하나로 그려야 하는 이유
- 도면 위 6단계 판단 — 원점 위치, 베이스 여섯 꼭짓점 좌표, 모따기가 만드는 11과 115, 윗면 y=16, 보스 원 선행, 목 이론 모서리 (20,16)·(100,16)
- 치수표에 없는 값은 전부 표의 값에서 계산하고 계산 과정을 밝힌다 (11 = 16−5, 110 = 120−5−5, 20 = (120−80)÷2, R28 = 56÷2, 62+28 = 90)
- 지난 차시 파일 `L02_TEMPLATE` 을 열어서 시작하고 `SAVEAS` 로 `L03_PROFILE` 저장 (1단계 · 16단계)
- 조작 대본은 명령어·입력값·엔터·옵션 문자·대화상자 항목·기능키까지 (`LESSON_STYLE.md` 7번) — LINE(L), PLINE(PL), CIRCLE(C)+D 옵션, UCS, UCSICON OR, CLAYER, ZOOM(Z) A/W, LIST, OS, TAN, F3/F8/F2, Ctrl+1
- 2차시에서 미룬 선 종류 축척 0.5 를 특성 창에서 실제로 적용
- 확인 카드 4장 — 좌표 오독 / 골뱅이 누락 / 레이어 미변경 / 접점 스냅 꺼짐, 각각 알아차리는 법과 고치는 법까지
- 2분할 마무리 (왼쪽 이번에 한 일 · 오른쪽 다음 차시)
- 인사 화면 — 「고생하셨습니다」 + 4차시 안내 (`LESSON_STYLE.md` 8번)

## Must not

- 확정 치수표에 없는 부품 치수를 지어내는 것 (`LESSON_STYLE.md` 6번). 배치용 UCS 원점 60,70 과 중심선 내밀기 5, 줌 윈도우 범위는 부품 치수가 아니라고 화면과 대본에서 명시한다
- 접점의 좌표를 계산해서 읽어 주는 것 — 접점은 객체 스냅이 잡는다는 것이 이 차시의 요지다
- AutoCAD 명령 동작을 추측해서 쓰는 것 (`LESSON_STYLE.md` 7번). 확실하지 않으면 단순하게 쓰거나 명령을 바꾼다
- 시험 제한시간·배점·합격 기준 언급 (확인된 바 없음)
- 목차나 과정 안내, "오늘은 무엇을 한다" 식 로드맵 (1차시 소관, `LESSON_STYLE.md` 5번)
- 체크포인트 파일명을 로드맵처럼 나열하는 것 — 실제로 타이핑하는 1단계·16단계와 그것을 되짚는 마무리에만 쓴다 (`LESSON_STYLE.md` 22번)
- 이번 차시에서 그리지 않는 것을 그린 것처럼 말하는 것 — 필렛 R10, 축 구멍 Ø25, 탭 PCD Ø44, 장공, 잘라내기는 다음 차시 예고로만 언급한다
- 이모지, 느낌표 남발, "자!" "여러분" 같은 호객

## Frames

| # | 파일 | 길이 | 비트 |
| --- | --- | --- | --- |
| 1 | `01-title` | 12s | — |
| 2 | `02-today` | 133s | 4 |
| 3 | `03-concept` | 148s | 4 |
| 4 | `04-on-the-drawing` | 196s | 6 |
| 5 | `05-demo` | 920s | 16 |
| 6 | `06-check` | 172s | 4 |
| 7 | `07-recap` | 147s | 2 |
| 8 | `08-closing` | 17s | 2 |

프레임 길이와 비트 시각은 `SCRIPT.md` 에서 계산된다 (`LESSON_STYLE.md` 13·14번). 이 표는 손으로 고치지 않는다.
