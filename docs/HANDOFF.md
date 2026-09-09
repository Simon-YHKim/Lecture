# HANDOFF — AutoCAD 기능사 강좌

이 파일이 세션 간 인수인계의 정본이다. 세션을 시작하면 먼저 읽고, 끝낼 때 갱신한다.
최신 블록만 `## Latest` 를 달고, 이전 블록은 `## <날짜>` 로 내린다.

---

## Latest — 2026-09-09 / 자습본 검수 반영 — 강조 정합·상대좌표 제거·전 슬라이드 여백 검사

### 어디까지 왔나
- main HEAD: `24e7496` (이번 세션에 머지한 코드 PR 없음 — 이 핸드오프가 첫 머지)
- 이번 세션 머지된 PR: 없음. **작업물 130개가 커밋되지 않은 채 워킹 트리에만 있다.**
- CI: `private-materials-guard` — main 최근 3회 전부 green.
- working tree: **dirty (수정 110 · 신규 20)** — 커밋은 사용자 판단으로 남겨 둠

### ⛔ 막힌 것 — 작업물을 지금 커밋하면 CI 가 빨개진다

`scripts/check-course-projects.ps1` 이 **워킹 트리에서 183건 실패**한다.
`origin/main` 을 따로 떼어 같은 검사를 돌리면 **0건 통과**다. 즉 커밋 안 된
작업물 쪽 문제이고, 이 핸드오프 커밋(문서 + 검사 도구)에는 영향이 없다.

원인은 결함이 아니라 **검사기와 프로젝트가 갈라선 것**이다.

- `index.html` 의 프레임 길이가 char-count 추정값(12, 141, 95…)에서
  **실측값**(16.053, 141.899, 80.472…)으로 바뀌어 있다. `feat/measured-timing`
  에서 정한 방식이다 — "Measure how long the Korean takes instead of counting
  characters".
- 그런데 `check-course-projects.ps1` 은 여전히 SCRIPT.md 글자 수로 기준을 만든다.
  그래서 "대본을 고치고 스캐폴드를 다시 돌리지 않았다" 로 183건이 뜬다.

**따라서 작업물 커밋 전에 검사기를 먼저 고쳐야 한다.** `narration-timing.json`
이 있으면 그것을 기준으로 삼고, 없을 때만 글자 수로 떨어지게 하는 것이 맞다
(`narration-timing.json` 8개는 아직 untracked 이므로 함께 커밋해야 한다).
이걸 안 하고 커밋하면 자동 머지가 막히고, 억지로 넘기면 검사기가 무의미해진다.

### 이번 세션에 한 일

검수 메모 18건을 받아 반영했다. 자습본 데크는 191장 → **207장**(개념 절이 넘치면
스스로 나뉘게 바꿔서 늘었다).

**1. 수치 강조가 엉뚱한 것을 가리키던 문제 (메모 1~6)** — 원인이 둘이었다.

- 재생기가 한 박자 늦게 섰다. 조각 시각은 전환이 *시작되는* 순간인데 데크가 정확히
  거기 멈춰서, 앞 행이 아직 켜져 있고 새 행은 아직 안 켜진 화면이 보였다.
  `deck_nav.html` 의 `paint()` 에서 전환이 끝난 뒤에 서도록 고쳤다.
- 강조 겹선이 너무 굵었다. `profile` 하나가 베이스·목·윤곽을 한꺼번에 켰다.
  `edu_ib_02.py` 에 형상별 겹선 6종(`basehl` `neck` `bossc` `filletc` `slotc` `thick`)을
  추가하고, 프레임 트윈이 자기 치수가 재는 곳만 켜도록 재조준했다.

**2. 애니메이션·노트 전수 검사 (207장)**

| 항목 | 전 | 후 |
|---|---|---|
| 다음을 눌러도 안 변하는 구간 | 15장 | 0장 |
| 노트 빈 장 | 23장 | 0장 |
| 콘솔 오류 | 1건 | 0건 |
| 글이 상자를 넘는 곳 | — | 0장 |
| 아래 여백 12% 초과 | — | 0장 |

- 슬라이드 12는 타임라인 한 줄(`ease:"power2.out"78.35);`)이 깨져 그 화면 전체가
  정지해 있었다. 앞선 재조정 때 낸 흠이고, 전 프레임을 훑어 같은 유형 0건.
- 노트가 3~7차시에서 두 칸씩 밀려 있었다. 대본은 프레임 **파일 번호**로, 시각표는
  **슬롯 차례**로 번호를 매기는데 시연이 `05-demo-a/b/c` 로 셋인 차시에서 어긋난다.
  `build_deck_selfstudy.py` 에서 `fnum = int(base[:2])` 으로 고정.
- 아래 빈 띠는 43·44·47만이 아니라 **자습 슬라이드 전부**였다. 프레임 조판의
  `.body` 높이가 724px 로 못 박혀 있던 탓. `.ss>.body{height:auto}` 한 줄로 전부 해결.

**3. `@` 상대좌표 제거 (메모 16)** — **84개 → 0개.**
베이스는 `REC` 로 120×16 사각형을 먼저 그리고 `CHAMFER` 로 위 두 구석만 5×5.
11·115·110 같은 계산값이 아예 필요 없어진다. 잡을 것이 없던 자리(`@29,8`,
`@-33,62`)는 OFFSET 교차점 / 「길이 먼저 만들고 중간점으로 이동」으로 바꿨다.
2차시에는 **왜 골뱅이를 안 쓰는지** 설명을 남겼다.

**4. 코치 마크** — 7차시 치수 단계 9개, 6차시 4개에 도면+코치마크+형상 강조 (메모 18).

**5. 검수 UI** — 공통 메모 단추를 `.tools` 한 줄로 옮겨 항상 보이게, 노트 높이 고정
(216px) + 안쪽 스크롤, 메모·노트가 슬라이드를 가리지 않고 무대를 줄이도록.

### 활성 인프라
- 외부 서비스 없음. 전부 국지 빌드다.
- 산출물: 오프라인 단일 HTML 1개 (2.4MB, GSAP 인라인). 네트워크 참조 0.
- TTS: Windows SAPI `Microsoft Heami Desktop` (ko-KR). 측정값 **배속 = 1.115^Rate**,
  Rate 0 에서 **6.01 자/초**. Web Speech API 로 같은 목소리가 나며 1.00× 에서
  오프라인 렌더와 +0.1% 안쪽으로 일치. 엔진은 교체 가능하게 열어 둠.

### 다음 작업 큐

| # | 작업 | 크기 | 권장 |
|---|---|---|---|
| A | **`check-course-projects.ps1` 을 실측 시간 기준으로 고치고, 130개 작업물 + `narration-timing.json` 8개를 커밋** | small | ⭐ 위 「막힌 것」. 이걸 안 하면 이번 세션 결과물이 저장소에 못 들어간다. 다른 무엇보다 먼저 |
| B | A3 용지 도해 + 3뷰 도해를 만들고 나머지 74개 실습 단계에 코치 마크 | large | 사용자 정책 2번이고 검수 메모 8~11·13이 전부 이것이다. 실습 단계 103개 중 아직 29개만 붙어 있다. 2차시(도면틀)는 A3 용지 도해가, 5차시(3뷰)는 3뷰 도해가 없어서 막혀 있다 |
| C | 3~5차시 대본 낭독 시간 재측정 → 프레임 재조정 | medium | 녹화 대본을 다시 썼다. 영상 제작 전에 필요. **자습본 데크에는 영향 없다**(바뀐 곳이 전부 녹화 프레임 안이라) |
| D | `scripts/selfstudy/source/curriculum.json` 의 옛 방법 정리 | small | 기획 문서라 사용자에게 안 보이지만, 다시 빌드하는 사람이 옛 방법을 되살릴 수 있다 |

### 적용 중인 정책 (영구 — 사용자가 명시한 것)

1. **좌표 입력 금지.** "좌표를 이용한 작업은 권장하지 않음. 너무 어렵고 불편한 방법임.
   마우스와 키보드를 이용해서 작업하는게 훨씬 직관적. 모든 강좌에서 이런방식으로
   설명해야 함." → 마우스 커서 + 스냅 + 수치입력. 예외는 용지선 두 구석(`0,0`,`420,297`).
2. **작도 실습 슬라이드에는 도면 + 코치 마크 + 지금 그리는 요소 강조.** 점검 카드는
   최하단 한 행으로 내리고 그 자리에 도면을 띄운다. 코치 마크는 슬라이드마다 지시하는
   작업이 다르면 함께 바뀌어야 한다.
3. **윈도우(좌→우) / 크로싱(우→좌) 선택의 차이를 설명한다.**
4. **박스 중심 텍스트** — 박스에 X 사선을 긋고, DTEXT 정렬을 중간-센터로 해서 교차점에
   스냅한 뒤, X 를 지운다.
5. **슬라이드 아래 빈 공간 금지.** "전 슬라이드에 걸쳐서 이런 현상이 발생하지 않도록
   명심해. 다른 슬라이드에 대해서는 별도 언급하지 않을테니 전수 검사해서 개선해."
6. **문체** — 합쇼체 70~80% / 해요체 20~30%.
7. **디테일한 키 입력 규제보다 방법을 알려주는 데 초점.**
8. **검수 HTML 은 다운로드 가능한 단일 파일.** 사용자는 아티팩트를 못 보는 환경이다.

### 이 저장소의 함정 (겪은 것만)

- **셸 히어독이 이스케이프를 먹는다.** `\n`, `\\`, `\s` 가 한 번 더 풀려 파이썬·JS
  소스가 깨진다. 이스케이프가 있는 것은 **반드시 Write/Edit 도구로** 쓴다.
  이번 세션에도 두 번 당했다.
- **KST 시각은 PowerShell 로.** Git Bash 의 `TZ=Asia/Seoul date` 는 이 머신에서
  9시간 이르다. `powershell.exe -NoProfile -Command "Get-Date"`.
- **`private-materials-guard` 는 사용자 폴더를 가리키는 로컬 절대 경로를 막는다.**
  `file:` 스킴으로 시작하는 윈도우 사용자 폴더 경로가 대표적이다. 공개 저장소에
  개인 경로가 남는 것을 막는 규칙이라 맞는 동작이고, **이 문서에 그 형태를 예시로
  적어도 걸린다**(직접 겪었다). 도구 스크립트는 경로를 런타임에 찾아야 한다 —
  `scripts/selfstudy/audit/pw.mjs` 가 그 방법이다.
- **SCRIPT.md 는 문장마다 줄을 나누고 네 칸을 들여 쓴다.** 여러 문장을 한 덩어리로
  바꾸려 하면 안 맞는다. **문단이 교체 단위**이고 앞에 `'    '` 를 붙인다.
- **데크 화면을 눈으로 확인할 때는 장면을 이름으로 집는다.** 데크는 장면을 겹쳐 두고
  투명도로만 가리므로 "폭이 0 아닌 첫 장면"은 엉뚱한 장을 집는다. 이것 때문에
  한 시간을 헤맸다.

### 핵심 파일 위치

```
scripts/selfstudy/build_deck_selfstudy.py   차시 하나를 데크로. 단계·개념·분할 장 생성
scripts/selfstudy/build_deck_all.py         8차시를 한 파일로 (--standalone 로 오프라인판)
scripts/selfstudy/assets/deck_nav.html      무대·이동·발표자 노트. paint() 가 조각 시각을 잡는다
scripts/selfstudy/assets/deck_memo.html     검수 메모 (드래그·화면·요소·공통) + 프롬프트 복사
scripts/selfstudy/source/lesson-0N.json     자습본 원본. steps[].actions / spots / feature
scripts/selfstudy/figures.py                정본 도면을 슬라이드용으로 줄여 준다
scripts/selfstudy/audit/audit_deck.mjs      전 슬라이드 애니메이션·노트 누락 검사
scripts/selfstudy/audit/audit_fit.mjs       넘침·아래 빈 띠 검사
scripts/selfstudy/audit/shot.mjs            슬라이드 화면 캡쳐 (n 또는 n:조각)
scripts/part/edu_ib_02.py                   정본 도면 생성기. 형상별 강조 겹선이 여기 있다
scripts/part/retime_frames.py               프레임 트윈을 다시 잰 박자에 맞춘다
projects/autocad-technician/lesson-0N-*/    대본(SCRIPT.md) · 프레임 · narration-timing.json
```

### 검증

```bash
# 1) 저장소 가드 (CI 와 같은 것)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/check-private-materials.ps1 -Mode all
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/check-course-projects.ps1

# 2) 데크를 짓고
python scripts/selfstudy/build_deck_all.py <출력.html> --standalone <gsap.min.js>

# 3) 전수 검사 — 넷 다 0 이어야 한다
node scripts/selfstudy/audit/audit_deck.mjs <출력.html>   # 정지 구간 · 빈 노트 · 콘솔 오류
node scripts/selfstudy/audit/audit_fit.mjs  <출력.html>   # 넘침 · 아래 빈 띠
```

`audit_*.mjs` 는 playwright 가 필요하다. 없으면 `npm i -g playwright`,
또는 `PLAYWRIGHT_PKG=<경로>` 로 알려 준다.

### 다음 세션 시작하는 법

```bash
git fetch origin main && git pull origin main
cat docs/HANDOFF.md
# A 작업(도해 두 개 만들고 코치 마크 확장)부터 시작
```

---
