# HANDOFF — AutoCAD 기능사 강좌

이 파일이 세션 간 인수인계의 정본이다. 세션을 시작하면 먼저 읽고, 끝낼 때 갱신한다.
최신 블록만 `## Latest` 를 달고, 이전 블록은 `## <날짜>` 로 내린다.

> 지난 블록은 월별로 내렸다 — [`docs/handoff-archive/`](handoff-archive/).
> 최신 블록과 직전 블록만 이 파일에 둔다. 한 파일 100KB 를 넘기지 않기 위해서다.

> 최종 갱신 **2026-09-11 06:30 KST** · Claude Opus 5 (Claude Code) · 커밋은 이 파일의 git 이력 참조

---

## Latest — 2026-09-11 (5차) / 영문 대본 여덟 차시 완성 · 프레임 넘침 11장을 0으로 (PR #39)

### 어디까지 왔나

- main HEAD **`4b7867b`** (PR #39 squash merge) · CI 초록 · 열린 PR 0 · 워킹 트리 깨끗.
- **영문 대본이 여덟 차시 다 갖춰졌다.** 2~7차시 627문단을 이 세션에서 썼다.
- 영문 음성도 2~7차시를 합성했다(Zira 1.15배). 프레임 시각까지 맞췄다.
- **영문 프레임이 캔버스 밖으로 넘치던 것을 찾아 고쳤다.** 78장을 전수로 재
  보니 영문 11장이 잘리고 있었다. 지금은 0장이다.

| 무엇 | 상태 |
| --- | --- |
| 영문 자습 교재 | 완료 |
| 영문 도면 | 완료 |
| 영문 프레임 지도 | 여덟 차시 973줄 |
| 영문 대본 | **여덟 차시 706문단 완료** |
| 영문 음성 | **여덟 차시 완료** (2~7차시는 이 세션) |
| 영문 영상 | 1·8차시만 (2~7차시는 녹화 대기) |

### 영문 대본은 국문과 **같은 뼈대**여야 한다

문단이 하나만 달라도 그 차시의 강조 시점이 통째로 밀린다. 그래서 번역이기
이전에 구조가 같아야 한다 — 같은 Line, 같은 문단 수, 같은 비트 번호.

- `test_script_editions.py` 가 Line·문단·비트를 검사한다. 영문 대본이 있는
  차시만 본다.
- 비트는 문단 첫 글자가 `(1` 처럼 **괄호와 숫자**로 시작할 때만 잡힌다.
  「(card 1 · …)」로 쓰면 비트가 통째로 사라진다. 「(1 card — …)」로 쓴다.
- 녹화 Line 의 단계 제목은 국문 `### 3단계`, 영문 `### Step 3` 둘 다 읽는다
  (`beats._STEP_HEAD`).
- **단계별 명령 표기(`step_keys`)와 첫 사용 순서(`shortcuts_in`)가 국문과
  완전히 같은지도 맞춰 두었다.** 옵션으로 치는 글자가 명령으로 세어지지 않게
  영문에도 「chamfer option」「fillet option」「the layer option」「the close
  option」「current layer」를 적었다. 안 적으면 그 차시의 명령표가 어긋난다.

| 차시 | 문단 | 단계 | 명령 |
| --- | --- | --- | --- |
| 2 | 130 | 16 | — |
| 3 | 85 | 16 | 15 |
| 4 | 100 | 16 | 24 |
| 5 | 105 | 16 | 11 |
| 6 | 104 | 16 | 17 |
| 7 | 103 | 17 | 17 |

### 프레임 넘침 — 원인은 번역 길이가 아니었다

`.clip` 은 `overflow:hidden` 이라 넘친 부분이 **조용히 잘린다**. 잘린 화면은
"원래 그런 그림" 처럼 보이므로 눈으로는 못 찾는다. 한계선은 **1016px** —
1080 캔버스에서 `.clip` 아래 여백 64 를 뺀 값.

원인은 표 설명 칸의 인라인 `white-space:nowrap` 이었다. 국문은 「선을 긋는다」
처럼 짧아 문제가 없지만, 영문은 같은 자리가 한 문장이라 그 칸이 624px 를 먹고
옆 칸이 114px 로 찌그러진다. 그러면 옆 칸이 네댓 줄로 접히며 표가 통째로
내려간다. 3차시 명령표가 724px 자리에서 **1470px** 이 됐고 4차시에서는 겹침
오류까지 났다.

- `build_english_lesson.py` 가 사본에서 **먹색 설명 칸의 줄바꿈 금지만** 푼다.
  명령 이름·치수 값이 들어가는 강조색 칸은 그대로 둔다.
- 그래도 남은 것은 문장을 줄였다 — 카드 6개, 명령 설명 38개.
  **명령 설명은 여덟 차시가 같은 문장을 쓰므로 지도 전체에 한 번에 건다.**
  한 차시만 고치면 같은 명령이 차시마다 다르게 설명된다.
- **문장을 깎는 것으로 닫히지 않는 자리가 있다.** 표가 자동 배치라 한 칸을
  줄이면 열 너비가 다시 나뉘면서 다른 행이 대신 두 줄이 된다 — 6차시 명령표는
  세 줄짜리 두 행을 없앴는데 전체 높이가 585px 그대로였다. 그래서 영문 사본에서만
  `table.spec.tight` 의 셀 여백을 6px→3px 로 좁힌다. 글자 크기는 안 건드린다.

```
국문 78장 넘침 0 · 영문 78장 넘침 11 → 0
```

### 재는 방법 (`scripts/part/frame_sheet.py`)

프레임 본문은 `<template>` 안에 있어 파일을 그냥 열면 아무것도 안 보인다.
측정 쪽이 `fetch` 로 읽어 복제해 붙인다.

```bash
python scripts/part/frame_sheet.py <잴 폴더> --en <영문 사본들이 모인 폴더>
cd <잴 폴더> && python -m http.server 8731 --bind 127.0.0.1
# 브라우저(Playwright MCP headless)로 measure.html 을 열고 await measureAll()
```

⚠ **이 측정값은 상대 비교용이다.** hyperframes check 는 JetBrains Mono 를
받아 `@font-face` 를 주입하므로 같은 프레임이 30~60px 더 높게 잡힌다.
넘침의 최종 판정은 언제나 `hyperframes check` 다.

### 영문 강의를 만드는 길 (4차 블록과 같다, 한 줄 추가)

```bash
python scripts/part/build_english_lesson.py <국문 차시> <비공개 사본>
python scripts/part/narrate_tts.py <사본> --voice "Microsoft Zira Desktop" --out <새 폴더>
python scripts/part/retime_frames.py <사본>
python scripts/part/prepare_lecture.py <사본> --out <렌더 폴더> --gsap <gsap.min.js> --preview
python scripts/part/prepare_scene_checks.py <렌더 폴더> --out <장면 폴더>   # ← 긴 차시는 이것부터
npx hyperframes@0.8.33 check <렌더 폴더> --json --at-transitions
```

**긴 차시는 통짜 check 의 모션 판정을 믿으면 안 된다.** 0.8.33 은 모션을 300점
까지만 훑으므로 30분 차시는 6초에 한 번 본다. 그러면 2초짜리 등장이 통째로
"늦게 나타남" 오류가 된다. `prepare_scene_checks.py` 가 장면별로 쪼개 준다.
**레이아웃·대비 판정은 통짜 check 도 정확하다.**

### 이 세션의 영문 음성 길이 (Zira 1.15배, 실측)

| 차시 | 길이 | | 차시 | 길이 |
| --- | --- | --- | --- | --- |
| 2 | 30:06 | | 5 | 33:55 |
| 3 | 30:48 | | 6 | 31:54 |
| 4 | 31:08 | | 7 | 36:27 |

국문보다 3~5분 길다. 1.15배가 1.38배보다 느린 것이 그대로 반영된 값이다.

### 사용자 확인 대기 (4차 블록에서 그대로)

- **국문 낭독도 1.15 로 내릴까.** 지금은 영문만 1.15 다. 국문까지 내리면 8차시
  음성을 다시 합성하고 프레임 시각을 다시 맞춰야 하며, 공개된 첫 판과 달라진다.
- 저장소 루트의 추적 파일 **`--help`** (31,150B · 참조 0) 삭제 여부.
- 머지 끝난 원격 브랜치 정리 여부.

### 남은 것

| # | 작업 | 크기 | 메모 |
| --- | --- | --- | --- |
| A | 2~7차시 실제 AutoCAD 2024 녹화 | large | **사용자 몫.** 국문·영문 영상이 같이 막혀 있다 |
| B | 작도 안내 P2 잔여 5건 | medium | 실제 조작·원본 대조 필요 → A 와 함께 |
| C | 2~7차시 영문 **장면별** 모션 check 완주 | small | lint·runtime·layout·contrast 는 여섯 차시 전부 오류 0 · 경고 0 으로 확인했다. 모션만 남았다 |

### 다음 세션 시작하는 법

```bash
git fetch origin main && git pull --ff-only origin main
cat docs/HANDOFF.md
python -m unittest discover -s scripts/part -p 'test_*.py'   # 126개 통과여야 한다
python scripts/selfstudy/check_english.py                    # 통과여야 한다
```

---

## 2026-09-11 (4차) / 영문 강의가 굴러간다 — 1·8차시 영상 완성 · 프레임 지도 여덟 차시 (PR #34~#37)

### 어디까지 왔나

- main HEAD **`866f426`** · CI 초록 · 열린 PR 0 · 워킹 트리 깨끗.
- **영문 1·8차시가 영상까지 나왔다.** 녹화가 필요 없는 두 차시다.
  국문도 이 둘만 영상이 있으므로, 두 판의 진도가 같아졌다.
- 사용자가 영문 낭독 속도를 **1.15배**로 정했다(1.38배 표본을 듣고 빠르다고 판단).
  국문 1.38 은 그대로다. **국문도 내릴지는 사용자 확인 대기.**

| 무엇 | 상태 |
| --- | --- |
| 영문 자습 교재 | **완료** (도해 영문 짝 161자리 · 넘침 0) |
| 영문 도면 | **완료** (`--lang en` · 다섯 글자만 영문) |
| 영문 프레임 지도 | **여덟 차시 973개 전부** |
| 영문 대본 | **1·8차시 완료** · 2~7차시 남음 |
| 영문 영상 | **1·8차시 완료** (6:04 · 6:50) |

### 영문 강의를 만드는 길

```bash
python scripts/part/build_english_lesson.py <국문 차시> <비공개 사본>
python scripts/part/narrate_tts.py <사본> --voice "Microsoft Zira Desktop" --out <새 폴더>
python scripts/part/retime_frames.py <사본>
python scripts/part/prepare_lecture.py <사본> --out <렌더 폴더> --gsap <gsap.min.js>
npx hyperframes@0.8.33 check <렌더 폴더> --json --at-transitions
npx hyperframes@0.8.33 render <렌더 폴더> --quality high --fps 30 --low-memory-mode --output <mp4>
```

**국문 프레임은 건드리지 않는다.** 사본에서만 갈아 끼운다. 필요한 것 둘 —
`SCRIPT.en.md`(문단·비트가 국문과 같아야 한다)와 `scripts/part/frames_en/<차시>.json`.

- 배속은 목소리를 따른다 — `TEMPOS = {Heami: 1.38, Zira: 1.15}`. 시각 파일에 적힌
  목소리로 판정하므로 국문 시각은 그대로 통과한다.
- 번역 단위는 **한 문장을 담은 가장 바깥 요소**다. `<b>` 강조가 섞여도 한 단위다.
  자리는 글자 찾기가 아니라 **파싱한 오프셋**으로 덮는다.

### 남은 것 — 영문 대본 2~7차시

문단 수가 국문과 한 개라도 다르면 그 차시의 강조 시점이 통째로 밀린다.
`test_script_editions.py` 가 Line·문단·비트 번호를 검사한다.

| 차시 | 문단 | 비고 |
| --- | --- | --- |
| 2 | 130 | Line 8 이 16단계 42문단 |
| 3 | 85 | Line 5 가 40문단 |
| 4 | 100 | Line 5 가 47문단 |
| 5 | 105 | Line 5 가 64문단 |
| 6 | 104 | Line 5 가 58문단 |
| 7 | 103 | Line 5 가 56문단 |

합계 **627문단**. 국문 대본 한글 61,872자에 대응한다.

### 사용자 확인 대기

- **국문 낭독도 1.15 로 내릴까.** 지금은 영문만 1.15 다. 국문까지 내리면 8차시
  음성을 다시 합성하고 프레임 시각을 다시 맞춰야 하며, 공개된 첫 판과 달라진다.
- 저장소 루트의 추적 파일 **`--help`** (31,150B · 참조 0) 삭제 여부.
- 머지 끝난 원격 브랜치 정리 여부.

### 다음 세션 시작하는 법

```bash
git fetch origin main && git pull --ff-only origin main
cat docs/HANDOFF.md
python scripts/selfstudy/check_english.py            # 통과여야 한다
python scripts/part/frame_text.py projects/autocad-technician/lesson-02-part-and-template --map scripts/part/frames_en/lesson-02-part-and-template.json
# 2차시 SCRIPT.en.md 부터. 1·8차시를 본보기로 삼는다.
```

---

