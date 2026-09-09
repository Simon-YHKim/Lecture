# 두 판 — 강의용과 자습용

이 과정은 같은 내용을 두 판으로 낸다. 어느 쪽이 원본이고 어느 쪽이 복사본이
아니다. **매체가 달라서 두 판인 것**이고, 그래서 서로 다를 수 있는 것과 반드시
같아야 하는 것이 나뉜다.

이 문서가 그 경계를 정한다. 경계가 문서로만 있으면 다시 갈라지므로
`scripts/check-editions.py` 가 같은 규칙을 기계로 확인한다.

---

## 1. 무엇이 어느 판인가

| | 강의용 | 자습용 |
| --- | --- | --- |
| 무엇 | 화면 녹화가 들어가는 **영상 강의** | 혼자 읽고 따라 하는 **교재** |
| 원본 | `projects/autocad-technician/lesson-0N/SCRIPT.md` | `scripts/selfstudy/source/lesson-0N.json` |
| 화면 | `compositions/frames/*.html` (HyperFrames) | 인라인 SVG 도해 + 코치 마크 |
| 시간 | `narration-timing.json` — 실제로 읽혀 잰 값 | 없다. 읽는 속도는 학습자가 정한다 |
| 묶음 | `compositions/episodes/ep*.html` — 한 편 20분 | 쪽 — 한 쪽 100KB |
| 산출물 | 영상 19편 · 248분 | `docs/autocad-technician/self-study/*.html` |
| 검수 | 프레임 미리보기 | 오프라인 단일 HTML 데크 (메모·노트 달림) |

**강사가 있느냐가 갈라지는 지점이다.** 영상에는 목소리가 있어 어디를 봐야 할지
말로 끌 수 있다. 교재에는 목소리가 없으므로 그 몫을 코치 마크와 「이렇게 되면
맞습니다 / 왜 이 순서인가 / 안 되면 여기」 세 칸이 대신한다.

---

## 2. 반드시 같아야 하는 것 — 기계가 본다

### 2-1. 학습자가 치는 명령의 집합

한쪽 판에만 있는 명령이 있으면 안 된다. 영상을 보고 온 사람이 교재에서 못 찾거나,
교재로 예습한 사람이 영상에서 처음 보는 것이 생긴다.

**차시별로 같을 필요는 없다.** 어느 차시에서 가르치든 과정 안에 있으면 된다 —
두 판은 배치가 다르다. `check-editions.py` 가 과정 전체로 대조한다.

### 2-2. 차시를 잇는 체크포인트 파일 이름

`EDU-IB-02_L03_PROFILE` 같은 이름은 학습자가 실제로 찾고 저장하는 값이다.
두 판이 다른 이름을 부르면 사슬이 끊긴다.

### 2-3. 규격

레이어·용지·기능키·특수문자는 `course-standards.json` 이 정본이고
`check-standards.py` 가 두 판을 함께 본다. 근거는 사내 정본 교안이다
(`LESSON_STYLE.md` 6번 — 규격은 지어내지 않는다).

### 2-4. 방법

좌표를 치지 않고 마우스 커서 + 객체 스냅 + 수치 입력으로 그린다. 예외는 용지선
두 구석뿐이다. **이것이 실제로 갈라졌던 자리다** — 자습본은 골뱅이 상대좌표를
84곳 걷어냈는데 녹화 대본은 그대로였고, 3차시 한 차시 안에서 개념 화면과 실습
대본이 서로를 부정하고 있었다.

---

## 3. 달라도 되는 것

| 항목 | 강의용 | 자습용 | 왜 달라도 되나 |
| --- | --- | --- | --- |
| 단계를 쪼개는 방식 | 녹화 한 덩어리로 16단계 | 14~17단계 | 화면에서 한 호흡인 것과 글에서 한 덩어리인 것이 다르다 |
| 분량 | 낭독 시간이 곧 길이 | 읽는 사람이 속도를 정한다 | — |
| 등장 순서 | 말이 끌고 간다 | 눈이 끌고 간다. 표는 처음부터 다 보인다 | — |
| 되묻기·격려 | 내레이터의 억양이 대신한다 | 글로 써야 한다 | 목소리가 없다 |
| 검산 | 화면에서 함께 확인 | 「이렇게 되면 맞습니다」로 판정 기준을 글로 | 봐 줄 사람이 없다 |
| 코치 마크 | 있으면 좋다 | **없으면 못 따라 한다** | 「베이스 윗면 왼쪽쯤」은 탐색 지시다 |
| 영문 | 없다 | 전 문장 병기 | 자습본만 이중언어다 |

---

## 4. 어느 쪽이 먼저인가

**내용은 강의용이 먼저, 표현은 자습용이 먼저다.**

- 무엇을 어떤 순서로 가르칠지는 `SCRIPT.md` 와 `COURSE_PLAN.md` 가 정한다.
- 그 내용을 혼자 읽어도 되게 만드는 방법 — 문체·도해·코치 마크·검산 — 은
  자습본이 먼저 풀고 강의용이 따라간다. 실제로 좌표 제거도 코치 마크도
  자습본이 먼저 했다.

그래서 **자습본에서 방법이 바뀌면 강의용 대본과 프레임을 같이 고쳐야 한다.**
안 고치면 이번에 겪은 일이 반복된다.

---

## 5. 한쪽을 고쳤을 때 따라오는 일

```
자습본 JSON 을 고쳤다
  → python scripts/check-editions.py        두 판이 갈라졌는지
  → python scripts/check-standards.py       규격이 갈라졌는지
  → python scripts/selfstudy/tone_check.py <file>
  → SELFSTUDY_SRC=… python scripts/selfstudy/build_selfstudy.py

강의 대본(SCRIPT.md)을 고쳤다
  → python scripts/part/narrate_tts.py --all --out <저장소 밖>
  → python scripts/part/retime_frames.py <차시>       (여덟 번)
  → python scripts/part/rebuild_episodes.py
  → python scripts/part/write_course_docs.py
  → pwsh -File scripts/check-course-projects.ps1
```

낭독 시간이 길이를 정하므로(`LESSON_STYLE.md` 13·14번) 대본을 고치면 TTS 재합성이
반드시 뒤따른다. 건너뛰면 모션이 옛 녹음을 가리킨 채 남는다.

---

## 6. 검사

```bash
python scripts/check-standards.py     # 규격이 한 값인가
python scripts/check-editions.py      # 두 판이 같은 것을 가르치는가
pwsh -File scripts/check-course-projects.ps1
```

셋 다 종료 코드로 판정한다. `check-course-projects.ps1` 이 앞의 둘을 함께 부른다.
