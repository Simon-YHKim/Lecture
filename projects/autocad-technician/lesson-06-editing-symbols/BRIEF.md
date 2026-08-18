---
workflow: general-video
flow: automation
storyboard: yes
message: "그려 놓은 것과 제대로 보이는 것은 다르다. 정리와 표기가 도면을 도면으로 만든다."
destination: desktop-course
aspect: 1920x1080
language: ko
audience: "CAD를 처음 접하는 Technician 실습과정 입문 수강자"
length: 31m57s
angle: lesson-06-editing-symbols
narration: user-recorded
style_preset: lg-training
part_id: EDU-IB-02
checkpoint_in: L05_VIEWS
checkpoint_out: L06_REPRESENTED
paper: A3-landscape
projection: third-angle
recording_slots: 1
---

## Intent

일곱 차시에 걸쳐 `EDU-IB-02 아이들러 풀리 브래킷` 하나를 완성하는 과정의 여섯 번째 차시다. 지난 차시에서 제3각법으로 정면도·평면도·우측면도가 다 나온 파일을 열어, 새 형상을 더하지 않고 이미 있는 것을 정리하고 제대로 보이게 만든다. 학습자는 TRIM과 EXTEND로 투상선과 보조선을 걷어 내고, MIRROR로 장공의 좌우 대칭을 좌표 입력으로 다시 맞추고, MATCHPROP·LAYER·QSELECT로 모든 선이 제 레이어에 ByLayer로 들어가 있는지 점검하고, 개체 선 종류 축척과 LTSCALE로 중심선과 숨은선의 파선 간격을 맞춘다. 아울러 표면 거칠기 기호·기하 공차·재질 표기·열처리 지시가 무엇을 지시하는 표기인지를 그리지 않고 읽기만 한다. 종료 상태는 `L06_REPRESENTED`.

## Must have

- 타이틀 화면 (`LESSON_STYLE.md` 8번)
- 오늘 그릴 것 카드 4장 — 투상선과 보조선 정리 / 선 종류 축척 맞추기 / 레이어 점검 / 도면 기호 알아두기
- 개념 카드 4장 — TRIM과 EXTEND / MIRROR로 대칭 만들기 / MATCHPROP으로 특성 옮기기 / LTSCALE이 무엇을 바꾸는가. 각각 왜 그렇고 어떤 효과가 있는지까지
- 도면 위에서 표 6행 — 표면 거칠기 기호, 기하 공차, 재질 표기, 열처리 지시, 선 종류 축척, 레이어 점검. 앞 네 항목은 이 과정 실습에서 그리지 않는다는 것을 명시
- DEMO 15단계 — 1단계는 지난 파일 `EDU-IB-02_L05_VIEWS` 열기, 마지막 15단계는 `SAVEAS`로 `EDU-IB-02_L06_REPRESENTED` 저장
- DEMO에서 TRIM(TR), EXTEND(EX), MIRROR(MI), MATCHPROP(MA), LTSCALE, LAYER(LA), 특성 창 Ctrl+1, QSELECT를 모두 실제로 사용
- MIRROR 대칭축을 좌표 `60,0`–`60,90`으로 입력하고, 60이 전체 가로 120의 절반이며 보스 중심 가로 위치와 같다는 근거를 밝힘
- 장공 좌우 대칭의 근거를 확정 치수로 계산해 보임 — 29와 12와 50에서 끝원 중심 29·41(중심 35)과 79·91(중심 85), 120에서 91을 뺀 29
- 중심선·숨은선의 선 종류 축척 0.5는 2차시 레이어 표에서 정한 값임을 밝히고, 개체 값과 LTSCALE 전역 값이 곱해진다는 것을 설명
- 색상·선종류·선가중치를 ByLayer로 통일하는 단계와, 특성 창에서 도면층 칸은 건드리지 않는다는 경고
- 조작 대본은 명령어·입력값·엔터·클릭 위치·대화상자 항목·기능키까지 (`LESSON_STYLE.md` 7번)
- 확인 카드 4장 — 보조선을 남긴 채 넘어감 / 레이어만 끄고 지운 줄 앎 / LTSCALE을 개체 하나에만 적용 / 레이어는 맞는데 색을 개체에 직접 줌
- 2분할 마무리 — 왼쪽 이번에 한 일, 오른쪽 다음 차시 (각각 항목 4~5개를 문장으로)
- 인사 화면 — 「고생하셨습니다」 + 7차시 안내 (`LESSON_STYLE.md` 8번)

## Must not

- 확정 치수표에 없는 숫자를 지어내는 것. 계산해 쓸 때는 계산 과정을 밝힌다 (`LESSON_STYLE.md` 6번)
- 이 부품의 재질·표면 거칠기 등급·기하 공차 허용값·열처리 조건을 구체적인 값으로 지정하는 것
- 네 개(외형선·중심선·숨은선·치수선) 말고 다섯 번째 레이어를 새로 만들어 내는 것
- AutoCAD 명령의 동작을 추측해서 쓰는 것. 확실하지 않으면 단계를 단순하게 쓰거나 명령을 바꾼다
- 표면 거칠기·기하 공차·재질·열처리의 실습 (읽는 법만 다루고 그리지 않는다)
- 시험 제한시간·배점·합격 기준 언급
- 목차나 과정 안내 (1차시 오리엔테이션 소관, `LESSON_STYLE.md` 5번)
- 체크포인트 파일명을 로드맵처럼 나열하는 것. 실제로 타이핑하는 자리에만 쓴다 (`LESSON_STYLE.md` 22번)
- 7차시의 체크포인트 이름을 지어내는 것
- 이모지, 느낌표 남발, "자!" "여러분" 같은 호객

## Frames

| # | 파일 | 길이 | 비트 |
| --- | --- | --- | --- |
| 1 | `01-title` | 12s | — |
| 2 | `02-today` | 134s | 4 |
| 3 | `03-concept` | 145s | 4 |
| 4 | `04-on-the-drawing` | 265s | 6 |
| 5 | `05-demo` | 1030s | 15 |
| 6 | `06-check` | 160s | 4 |
| 7 | `07-recap` | 148s | 2 |
| 8 | `08-closing` | 23s | 2 |

프레임 길이와 비트 시각은 `SCRIPT.md` 에서 계산된다 (`LESSON_STYLE.md` 13·14번). 이 표는 손으로 고치지 않는다.
