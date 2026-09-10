# HANDOFF — AutoCAD 기능사 강좌

이 파일이 세션 간 인수인계의 정본이다. 세션을 시작하면 먼저 읽고, 끝낼 때 갱신한다.
최신 블록만 `## Latest` 를 달고, 이전 블록은 `## <날짜>` 로 내린다.

> 지난 블록은 월별로 내렸다 — [`docs/handoff-archive/`](handoff-archive/).
> 최신 블록과 직전 블록만 이 파일에 둔다. 한 파일 100KB 를 넘기지 않기 위해서다.

> 최종 갱신 **2026-09-11 02:00 KST** · Claude Opus 5 (Claude Code) · 커밋은 이 파일의 git 이력 참조

---

## Latest — 2026-09-11 (3차) / 영문 자습판을 끝냈다 — 남은 것은 대본·영상 (PR #25~#30)

### 어디까지 왔나

- main HEAD **`1ad74d8`** · CI 초록 · 열린 PR 0 · 워킹 트리 깨끗.
- 사용자가 이 세션에 정한 것 둘.
  1. **영문판은 영문 도면을 따로 쓴다.** 국문 도면은 검수 중이라 건드리지 않는다.
  2. **영문은 대본·영상 8편까지 끝까지 간다.** (자습만 하고 멈추지 않는다.)
- 머지된 PR 여섯 — #25 영문 1단계 · #26 핸드오프 분할 · #27 영문 도면 · #28 표기 인용 ·
  #29 인수인계 · #30 도해 영문 짝.

### 이 세션이 닫은 것

| 무엇 | 시작 | 지금 |
| --- | --- | --- |
| 학습자용 영문의 한글 잔존·용어 흔들림 | **91건** | **0건** (보류도 0) |
| 도면의 언어 | 국문 하나 | `--lang ko\|en` · 영문 도면 한글 0자 |
| `docs/HANDOFF.md` | 96,917B | 12.6KB + 월별 보관 |
| 자습 검수 파일 | 282장(구판) | **222장** 개정판을 사용자에게 보냄 |
| 도해 23개의 영문 짝 | 없음 (한글 161자리) | **161자리 전부** · 실측 넘침 0 · 겹침 0 |
| 영문 자습 교재 | 없음 | `SELFSTUDY_LANG=en` 으로 빌드해 사용자에게 보냄 |

- 영문 도면은 다섯 글자만 바꾼다 — `4-M5 DEPTH 10` · `2-SLOT R5` · `FRONT/TOP/RIGHT SIDE VIEW`.
  **선은 한 줄도 움직이지 않는다**(두 판에서 `<text>` 를 걷어낸 SVG 가 같다는 검사).
  국문 도면 출력은 바뀌기 전과 SHA-256 이 같다.
- `SELFSTUDY_LANG=en` 이 도면 언어와 `data-lang` 을 자습 빌더까지 나른다.
- `check_english.py` + `test_english.py` 가 CI 에서 돈다. 규칙은 이름을 겨냥하고
  `the base outline` 같은 보통명사는 잡지 않는다 — 그 구분도 검사로 고정했다.

### 다음 작업 큐

| # | 작업 | 크기 | 메모 |
| --- | --- | --- | --- |
| A | ~~도해 23개의 영문 짝~~ **닫음** | — | 161자리 전부. 넘친 2 · 겹친 7 을 문구를 줄여 0 으로. 국문 좌표는 안 건드렸다. 재는 방법은 `figure_sheet.py` 로 남겼다 |
| B | **영문 강의 — 대본 8편 · 슬라이드 78장 · 영상 8편** | large | ⭐ 실측한 규모 — 대본은 한글 **61,872자**, 강의 프레임 78장 안의 한글 조각 **5,756개(문구 2,614종)**. 자습(4,331쌍)보다 크다 |
| B-1 | 영문 낭독 속도 결정 | small | 표본 두 개를 사용자에게 보냈다 — Zira rate 0 은 326자에 **23.88초**, 1.38배는 **17.29초**. 답이 오면 그 속도로 합성한다 |
| B-2 | `narrate_tts` 의 언어 문 열기 | small | 지금은 `voice != Heami` 또는 `tempo != 1.38` 이면 거부한다. 영문 판정을 더하되 국문 정책은 그대로 둔다 |
| C | 2~7차시 실제 AutoCAD 2024 녹화 | large | **사용자 몫.** 이 PC 에도 AutoCAD 가 없다 |
| D | 작도 안내 P2 잔여 5건 | medium | 실제 조작·원본 대조 필요 → C 와 함께 |
| E | 개편 보고서 HTML | small | 저쪽 PC 의 보고서를 못 가져오면 여기서 다시 만든다 |

### 이 PC 환경 (2차 블록과 같다)

Python 3.12.10 · node 24.14.1 · FFmpeg 8.1.1 · Chrome · gh · **Heami + Zira** 음성.
Git Bash 에서 Python 한글 출력은 `PYTHONIOENCODING=utf-8` 를 붙여야 안 깨진다.
⚠ **Bash heredoc 은 `\\` 를 `\` 로 접는다** — 정규식이나 경로가 든 파이썬은 heredoc 대신
파일로 쓴다(Write). 이 세션에서 세 번 걸렸다.

### 사용자 확인 대기

- 저장소 루트의 추적 파일 **`--help`** (31,150B) 삭제 여부. `build_deck_all.py --help` 가
  출력 경로를 `--help` 로 읽어 만든 산출물이다 — 이번 세션에 재현했다. 참조 0.
- 머지 끝난 원격 브랜치 정리 여부.

### 다음 세션 시작하는 법

```bash
git fetch origin main && git pull --ff-only origin main
cat docs/HANDOFF.md
python scripts/selfstudy/check_english.py     # 통과여야 한다
# 큐 A 부터. 도해 하나를 두 벌로 만들고 브라우저로 넘침을 재는 것이 한 단위다.
```

---

## 2026-09-11 (2차) / 개편분을 회수해 main 에 넣었다 (PR #23)

### 어디까지 왔나

- main HEAD **`cfcda5f`** (PR #23 merge) · CI 초록. 열린 PR 0 · 워킹 트리 깨끗.
- 회수 경로 — 다른 PC(`C:\Lecture`)의 미커밋 250+9 파일을 사용자가 `codex/autocad2024-revision`
  브랜치로 push → 이 세션이 검증·수정하고 PR #23 으로 머지했다. **앞 블록의 유실 위험은 닫혔다.**
- 들어간 규모 — 260파일 **+20,924 / −7,026** · 추가 9 · 수정 251 · **삭제 0 · 리네임 0**.
- **작업 PC 가 바뀌었다.** 이 세션은 `E:\Lecture` 다. `C:\Lecture` · `C:\LectureDelivery` ·
  `C:\Users\Soha.Bae` 는 **이 PC 에 없다.** 저장소 밖 산출물(1·8차시 개정 MP4 · WAV ·
  개편 보고서 · 촬영 큐)은 전부 그 PC 에만 있다 — 필요하면 회수하거나 여기서 다시 만든다.

### 이 PC 환경 — 앞 블록의 함정 표는 그 PC 한정이다

| 무엇 | 값 |
| --- | --- |
| Python | **3.12.10 · `python` 이 PATH 에 있다.** `check-course-projects.ps1` 이 그대로 돈다 |
| node · FFmpeg | 24.14.1 · 8.1.1 (`ffmpeg`·`ffprobe` 둘 다 PATH) |
| SAPI 음성 | **Heami(한국어) + Zira(영어)** — 영문판 TTS 를 여기서 만들 수 있다 |
| 그 외 | Chrome · gh 로그인됨 · Playwright MCP(headless) |

⚠ Git Bash 에서 Python 한글 출력이 cp949 로 깨진다. **`PYTHONIOENCODING=utf-8` 를 붙인다.**

### 이 세션이 고친 것 둘

1. **회수 커밋의 CI 실패** — `test_narration_identity` 의 「합성 중 대본이 바뀌면 timing 을 쓰지
   않는다」 검사가 FFmpeg 없는 러너에서 tempo 사전 점검(`Local FFmpeg is required...`)에 먼저
   걸렸다. 그 조사만 stub 해 **낭독 원문 동일성만이 실패 원인**이 되게 했다.
   FFmpeg 를 PATH 에서 감춘 CI 동형 실행으로 확인했다 — 7 / 91(skip 8) / 22, CI 개수와 일치한다.
2. **README 끊긴 링크** — 저장소에 없는 `docs/autocad-technician/revision-20260910-report.html`
   를 가리키던 문단을 걷어냈다. README 의 남은 로컬 링크는 전부 실재한다(스크립트로 확인).

### 검증 (이 PC 실행값)

```
Python 136개 통과       scripts 7 · scripts/part 107 · scripts/selfstudy 22
node 8개 통과           test_review_transfer.cjs
CI 동형(FFmpeg 감춤)     7 / 91(skip 8) / 22 통과
과정 검사 통과           8차시 78프레임 181:49   ← 1.38배 반영 전 247:52
규격 검사 통과(문서 18개) · 판 대조 통과
가드 자체검사 통과 · 비공개 자료 전수 검사 통과 · 커밋마다 staged 검사 통과
```

### 다음 작업 큐

| # | 작업 | 크기 | 권장 |
| --- | --- | --- | --- |
| A | **2~7차시 실제 AutoCAD 2024 녹화** | large | ⭐ 남은 15편의 전제. **사용자 몫** — 이 PC 에도 AutoCAD 가 없다 |
| B | 영문판 자습·슬라이드·대본·영상 | large | 정책상 국문 완성 후. **Zira 음성이 이 PC 에 있어 실행 가능** |
| C | 작도 안내 P2 잔여 5건 | medium | 실제 조작·원본 대조 필요 → A 와 함께 |
| D | 개편 보고서 HTML (사용자 검수용) | small | 그 PC 의 보고서를 못 가져오면 여기서 다시 만든다 |
| E | ~~`docs/HANDOFF.md` 분할~~ **닫음** | — | 96.9KB → **12.6KB**. 옛 블록 여덟 개는 `docs/handoff-archive/2026-09.md` (84.7KB) 로 내렸다 |

### 사용자 확인 대기

- **E(핸드오프 분할)** — 상한을 넘기 직전이라 이번 응답에서 물었다.
- 저장소 루트의 추적 파일 **`--help`** (31,150B · `d47cfe0` 에서 리다이렉트 사고로 유입 ·
  참조 0) 삭제 여부. §7 정지 조건(파일 삭제)이라 묻고 진행한다.
- 머지 끝난 원격 브랜치 정리 여부. `codex/heami-course-sync` 는 다른 세션이 쓸 수 있어 남기길 권한다.

### 다음 세션 시작하는 법

```bash
git fetch origin main && git pull --ff-only origin main
cat docs/HANDOFF.md
# 큐 A 는 사용자 녹화 대기. 에이전트가 지금 진행할 수 있는 것은 B · D 다.
```

---

## 2026-09-11 (1차) / AutoCAD 2024 개편이 **미커밋 상태**로 작업 트리에만 있었다 — 2차 블록에서 회수됨

### 어디까지 왔나
- main HEAD: `534aaddba060ca025200f1cd0f5bbfe7ff3ce67c` — PR #21 (`fix: preserve narration and connect verified practice recordings`) merge 완료.
- 작업 브랜치 `codex/heami-course-sync` 는 `origin/main` 과 **동일하다** (ahead 0 · behind 0). 즉 브랜치에 아직 남은 커밋이 없다.
- **working tree: dirty — 수정 250개 · 추적 안 됨 9개 (+20,012 / −6,935).** 이 세션에서 머지된 PR 은 없다.
- 테스트 상태: **전부 통과 (144개)** — `scripts` 7 · `scripts/part` 107(skip 1) · `scripts/selfstudy` 22 · node `test_review_transfer.cjs` 8.
- 가드: `test-private-materials-guard.ps1` 통과 · `check-private-materials.ps1 -Mode all` 통과.

### ⚠️ 최우선 — 유실 위험
AutoCAD 2024 개편 작업 전체가 **커밋되지 않은 채 이 PC 의 작업 트리에만** 있다. push 도 태그도 없다.
`git checkout`, `git stash`, 컨테이너 재시작, 다른 PC 로 이동 중 어느 하나로도 사라진다. 다음 세션의 첫 판단은 **이걸 커밋할지 폐기할지**다.

미커밋 내용 요약 (git diff 로 확인한 것만 적는다):
- `projects/autocad-technician/course-standards.json` — `policy` 에 확정 정책을 박았다: `autocadVersion: 2024`, `deliveryUnit: lesson`, `lessonCount: 8`, `narrationPlaybackRate: 1.38`, `starterFilesProvided: false`, 채점·시험운영 `"공유 예정"`, 도움 연락처는 **이름만** 공개(김정웅·김양환), 제작 순서 `["ko","en"]`.
- 같은 파일에서 사내 정본 교안 note 를 고쳤다 — **현재 환경에 원본 교안 파일이 없어 이번 개편에서 원문 대조를 완료한 것으로 취급하지 않는다**고 명시.
- `projects/autocad-technician/course-continuity.json` — `totalSec` 14895 → **10909**, `videoCount: 8`, `deliveryMode: "lesson"`, 1차시 450 → 336초. 차시별 episodes 분할 구조를 통합 영상 한 개 구조로 바꿨다.
- 8개 차시의 `compositions/frames` HTML·motion.json 약 156개 + BRIEF/SCRIPT/STORYBOARD/index/narration-timing 갱신.
- 새 스크립트 `scripts/part/refresh_recording_labels.py` (SCRIPT.md 에서 녹화 자막만 갱신, 장면 재빌드 없음).
- 새 테스트 8개: `part/test_edu_ib_02.py`, `part/test_keys_pages.py`, `part/test_recording_labels.py`, `part/test_tempo_delivery.py`, `selfstudy/test_coach.py`, `selfstudy/test_deck_grouping.py`, `selfstudy/test_shortcut_coverage.py`, `test_check_editions.py`.
- `.github/workflows/private-materials-guard.yml` — `python -m unittest discover -s scripts` 한 줄 추가 (루트 테스트가 CI 에서 안 돌던 구멍을 막는다).
- `CHANGELOG.md` · `README.md` 갱신.

### 🐛 미커밋 작업에서 발견한 실제 결함
- `README.md` 의 미커밋 diff 가 `docs/autocad-technician/revision-20260910-report.html` 를 링크하는데 **그 파일은 디스크 어디에도 없다** (`docs/autocad-technician/` 에는 README.md · master-plan · public-artifact-manifest.json · reference · reports · self-study 만 있다). 이대로 커밋하면 끊긴 링크가 그대로 나간다. 파일을 만들거나 링크를 빼야 한다.

### 활성 인프라
- repo: `https://github.com/Simon-YHKim/Lecture` · `gh` 2.93.0 로그인됨 (`Simon-YHKim`).
- 첫 공개판 태그 `autocad-2026.09.10-preview.1` — 첨부 11개 · 256,574,576 bytes. **덮어쓰지 않는다.** 사용자 검수가 이 판 기준으로 진행 중이다.
- CI: `.github/workflows/private-materials-guard.yml` 하나. push · pull_request 에서 돈다.
- 원본 자료 · WAV · 전사 · 폰트 바이너리는 저장소 밖. 공개 대상 아니다.

### 로컬 환경 함정 (이 PC 한정)
- **`python` 이 PATH 에 없다.** `python` / `python3` 는 Microsoft Store 스텁이라 실행하면 exit 9009. **`py` 를 써야 한다** (Python 3.14.5).
- 그래서 `scripts/check-course-projects.ps1` 이 로컬에서 exit 9009 로 실패한다. 스크립트가 `python` 을 호출하기 때문이며 **저장소 결함이 아니다**. CI 는 ubuntu-latest 라 `python` 이 있어 정상이다. 로컬 검증은 아래 `py` 명령으로 대신한다.

### 다음 작업 큐
| # | 작업 | 크기 | 권장 |
|---|---|---|---|
| A | 미커밋 250+9 파일을 커밋·PR 할지 폐기할지 결정하고 처리 | large | ⭐ **먼저 한다.** 유실 위험이 가장 크고 B~D 가 전부 여기 얹힌다 |
| B | README 의 `revision-20260910-report.html` 끊긴 링크 해결 (파일 생성 or 링크 제거) | small | A 커밋 전에 같이 처리 |
| C | 2~7차시 실제 AutoCAD 2024 녹화 + 실제 조작 검증 | large | 실제 AutoCAD 가 있는 환경 필요. 이 환경엔 없다 |
| D | 영문판 자습·슬라이드·대본·영상 | large | 국문 완성 후. 정책상 순서 고정 |
| E | 게시판 P2 잔여 5건 (직교 상태, 장공 보조선/명령 순서, 자습 투상선 삭제, 29mm 측정 기준점, 참고 치수 고정 문자) | medium | C 와 함께. 실제 조작·원본 대조 필요 |

### 적용 중인 정책 (영구)
1. **실제 녹화·실제 AutoCAD 검증 없이 완료로 표시하지 않는다. 결과를 지어내지 않는다.** 환경에 실제 AutoCAD 가 없으면 "미검증"이라고 적는다.
2. 첫 공개판(`preview.1`) 파일을 **덮어쓰지 않는다.** 사용자 검수 기준이 유지돼야 한다. 정정은 릴리즈 안내와 후속 판으로 반영한다.
3. 원본 자료 · 별도 녹음 WAV · 전사 · 폰트 바이너리는 **공개하지 않는다.** 승인된 완성 파일만 Release 첨부로 나간다.
4. 제작 순서는 **국문 완성 → 영문**. 워크북에 이미 있는 영문은 초안이지 완성된 영문 과정이 아니다.
5. 차시마다 **통합 영상 한 개**. 녹화 내부 조각을 별도 에피소드로 공개하지 않는다.
6. 좌표 입력을 가르치지 않는다. 마우스 커서 + 객체 스냅 + 수치 입력. 예외는 용지선 두 구석(0,0 / 420,297).
7. 문체: 합쇼체 70~80% · 해요체 20~30%. 문어체 '~한다' 금지.
8. 보호 설정을 우회하지 않고 branch 를 삭제하지 않는다.
9. 채점·합격 기준·시험 운영은 `"공유 예정"` 으로 둔다. 도움 연락처는 **이름만** 공개한다.

### 핵심 파일 위치
```
docs/HANDOFF.md                                       이 파일 — 인수인계 정본
projects/autocad-technician/course-standards.json     정책·출처 정본 (policy 블록)
projects/autocad-technician/course-continuity.json    차시 연결·길이 (write_course_docs.py 생성물)
projects/autocad-technician/lesson-0N-*/SCRIPT.md     차시 대본 — 녹화 자막의 출처
projects/autocad-technician/lesson-0N-*/compositions/frames/   장면 HTML + motion.json
scripts/part/                                         영상·장면·녹화 파이프라인 + 테스트
scripts/selfstudy/                                    자습 교재 빌드 + 테스트
scripts/check-private-materials.ps1                   비공개 자료 가드 (CI 에서 돈다)
.github/workflows/private-materials-guard.yml         유일한 CI 워크플로
```

### 검증
```bash
py -m unittest discover -s scripts -p 'test_*.py'
py -m unittest discover -s scripts/part -p 'test_*.py'
py -m unittest discover -s scripts/selfstudy -p 'test_*.py'
node --test scripts/selfstudy/test_review_transfer.cjs
pwsh ./scripts/test-private-materials-guard.ps1
pwsh ./scripts/check-private-materials.ps1 -Mode all
```
`check-course-projects.ps1` 은 이 PC 에서 `python` 부재로 실패한다. CI 에서 확인한다.

### 다음 세션 시작하는 법
```bash
git fetch origin main && git pull origin main
cat docs/HANDOFF.md
git status --porcelain | wc -l   # 250+ 이면 미커밋 개편이 아직 살아 있다 → A 작업부터
```

---
