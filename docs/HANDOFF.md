# HANDOFF — AutoCAD 기능사 강좌

이 파일이 세션 간 인수인계의 정본이다. 세션을 시작하면 먼저 읽고, 끝낼 때 갱신한다.
최신 블록만 `## Latest` 를 달고, 이전 블록은 `## <날짜>` 로 내린다.

> 지난 블록은 월별로 내렸다 — [`docs/handoff-archive/`](handoff-archive/) · [9월 후속 보관](handoff-archive/2026-09-part2.md).
> 최신 블록과 직전 블록만 이 파일에 둔다. 한 파일 100KB 를 넘기지 않기 위해서다.

> 최종 갱신 **2026-09-16 00:58:39 KST** · Codex · 커밋은 이 파일의 git 이력 참조

---

## Latest — 2026-09-16 / 미병합 PR 통합 · main 기준 세션 인수인계

- **PR·병합 정리 완료:** 사용자 위임에 따라 [통합 PR #51](https://github.com/Simon-YHKim/Lecture/pull/51)을 main에 병합했다. 통합 커밋은 `e74050e8266af5e28dd583065266d78f59b47a44`이며 제작 브랜치의 29개 커밋이 모두 포함된다. [PR #50](https://github.com/Simon-YHKim/Lecture/pull/50)도 조상 커밋 포함으로 GitHub에서 **MERGED**가 됐다. 과거의 낭독 시각 불일치 보류 사유는 최신 음성·시각 재생성과 현재 검사 통과로 해소됐다. 인수 문서 자체의 최종 main 커밋은 이 파일의 Git 이력에서 확인한다.
- **검증:** 로컬 자동 테스트 252개(Python 7+167+68, Node 10), `check-private-materials.ps1 -Mode all`, `check-course-projects.ps1`를 다시 통과했다. [통합 PR CI](https://github.com/Simon-YHKim/Lecture/actions/runs/34991020137)도 성공했다. 기존 작업 폴더의 `feat/clone-voice-pipeline` 체크아웃과 미추적 `AutoCAD_Scripts_Review_Report.html`·`.md`는 보존했다. 인수 문서는 별도 `.worktrees/handoff-20260916-005434` 작업 폴더, `handoff/20260916-005434` 브랜치에서 갱신했다. 브랜치 삭제나 기존 릴리즈 교체는 하지 않았다.
- **현재 다운로드:** [9월 15일 차시별 자습 검수 릴리즈](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.15-selfstudy-review.1). 국문·영문 각각 **대본 통합 HTML 슬라이드 8개 + 같은 화면의 복제 음성 MP4 8개**, 핵심 32개이며 ZIP·안내 등을 합쳐 37개 자산이다. 국문 222장·4:12:55, 영문 263장·4:39:36, 음성 1.00×다. 각 언어 ZIP 전체를 풀고 `START_REVIEW_KO.html` 또는 `START_REVIEW_EN.html`을 Chrome/Edge에서 연다. 직전 블록에 ZIP 링크와 제작 검증 근거가 있다.
- **승인 상태 구분:** 자습 영상은 도해·단계별 슬라이드 화면이며 실제 AutoCAD 조작 녹화는 포함하지 않는다. 사람의 전체 청취와 실제 AutoCAD 실행 검수는 아직 남아 있는 prerelease다. [9월 14일 기존 강의 검수 릴리즈](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.14-review.1)의 28개 자산도 유지했다. 그 강의 영상의 언어별 실습 녹화 15자리 PREVIEW 보완은 별도 남은 범위다.
- **다음 세션의 첫 일:** 사용자가 모은 검수 JSON·의견이 있는지 확인하고 언어·차시·시각별로 정리한다. 전체 사람 청취, 명령어·파일명·좌표 발음, 실제 AutoCAD 절차를 검수한다. 검수자가 아직 정해지지 않았거나 의견이 없으면 자료 위치와 검수 우선순위만 정리하며 대량 재합성을 시작하지 않는다. 외부 사람에게 메시지를 보내는 권한은 주어지지 않았다.
- **수정이 승인되면:** 구조·기술 절차는 원자료와 공식 근거부터 확인한다. 승인된 변경만 대본에 적용하고, 해시로 바뀐 음성 토막만 다시 만든 뒤 확인·시각 재생성·자막/화면/전체 디코딩 검사를 수행한다. 제작 진입점은 `README.md`의 Per-lesson self-study video production 및 `scripts/selfstudy/`, `scripts/part/`다. 기존 게시 자산을 덮어쓰지 않고 검증된 새 버전으로 배포한다. 유료 API 대량 호출은 별도 명시적 확인이 필요하다.
- **로컬 제작 기록:** `local-materials/selfstudy-video-current.json`의 `base` 아래에 `assets/`, `voice-qa.json`, `retake-content-validation.json`, `public-release-validation.json`, `previous-release-preserved.json`, `completion-report.html`이 있다. 기존 강의는 `local-materials/release-review-current.json`, 이번 병합 근거는 `local-materials/handoff-current.json`에서 찾는다. 실제 비공개 작업 위치는 locator에서만 확인한다. 이 파일들은 Git에 없으므로 다른 컴퓨터에서는 공개 릴리즈·소스로 검수를 시작하고, 재제작 전에 비공개 원본의 별도 인계를 확인한다. 참조 녹음·개별 WAV·ASR 원문·모델·글꼴을 Git/공개 자료에 추가하지 않는다. 이전 제작·업로드 세션은 종료됐으므로 과거 PID나 생성 스크립트를 무조건 재시작하지 않는다.
- **안전한 재개:** 기존 체크아웃에서 `git fetch origin main` 후 `git show origin/main:docs/HANDOFF.md`를 먼저 읽고 `git status --short --branch`를 확인한다. 이 작업 폴더의 feature 브랜치가 그대로인 것은 의도한 보존 상태다. 새 수정은 최신 main에서 별도 worktree로 시작하며, 미커밋 변경이 있는 폴더에서 임의 checkout/pull/reset을 하지 않는다. `STATE.md`는 현재 상태, `DECISIONS.md`는 누적 결정이다. 아래 검사는 합성이나 게시를 실행하지 않는다.

```powershell
./scripts/check-private-materials.ps1 -Mode all
./scripts/check-course-projects.ps1
python -m unittest discover -s scripts -p 'test_*.py'
python -m unittest discover -s scripts/part -p 'test_*.py'
python -m unittest discover -s scripts/selfstudy -p 'test_*.py'
node --test scripts/selfstudy/test_review_transfer.cjs
```

---

## 2026-09-15 / 차시별 자습 슬라이드·영상 국영문 릴리즈 완료

- 사용자 확정 범위인 **국문 HTML 슬라이드 8개·MP4 8개 + 영문 HTML 슬라이드 8개·MP4 8개**, 총 32개를 제작하고 [GitHub 검수 릴리즈](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.15-selfstudy-review.1)로 공개했다. 자습 슬라이드마다 해당 대본을 통합했고 같은 화면에 선생님 복제 음성을 입혔다. 기존 강의 영상과 구분되는 차시별 자습 영상이다.
- [국문 전체 ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.15-selfstudy-review.1/AutoCAD_KO_SELFSTUDY.zip) · [영문 전체 ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.15-selfstudy-review.1/AutoCAD_EN_SELFSTUDY.zip). ZIP 전체 압축을 풀고 `START_REVIEW_KO.html` 또는 `START_REVIEW_EN.html`을 Chrome/Edge에서 열면 대본 클릭 이동, 같은 슬라이드 열기, 시간별 의견 JSON 저장이 된다. 각 ZIP은 차시별 HTML·MP4·MD·VTT·SRT와 검수 페이지·안내·매니페스트·체크섬 등 44개 파일이다. 릴리즈에는 핵심 32개, ZIP 2개, 가이드·매니페스트·체크섬을 합쳐 37개 자산이 있다.
- 국문은 222장·4:12:55, 영문은 263장·4:39:36이다. 1920×1080/30fps H.264/AAC, 음성은 원래 속도 1.00×다. 기존 승인 화면 124장의 음성을 재사용하고 새 자습 361장의 1,328토막을 만들었다. 영문 합성 입력의 숫자는 영어 단어로 명시했으며 표시 수치·좌표·대본은 유지했다.
- 새 음성 1,328토막을 현재 WAV 해시 기준으로 자동 대조했고 빈 인식·길이 의심은 0개다. 두 독립 CPU 인식기로 확인한 KO5 저장 안내, KO6 파일명 반복, EN2 방향, EN3 반복, EN5 높이·60/for 경계, EN6 L 명령, EN7 5×5·나사 개수·95.7, EN8 중심선 축척 등 11토막을 교정했다. 동음 표기 차이는 원문·별도 인식·실제 음성 토막의 경계로 재확인했고 원래 인식 결과를 보존했다. 사람이 청취한 것으로 보고하지 않는다.
- 모든 MP4의 전체 디코딩, 영상·음성 트랙 길이와 프레임 수, 자막 문자·시각, 원본 음성 표본, 모든 출력 화면과 마지막 프레임을 검사했다. 교정 전후 대본·자막 문자·슬라이드 화면 보존과 국영문 8차시 검수 플레이어를 확인했다. 공개 텍스트 91개 및 MP4 메타데이터에서 비공개 경로·자산을 검사했다. 37개 공개 다운로드 모두 비로그인 HTTP 200·크기·GitHub SHA-256 일치를 확인했다.
- 제작 소스는 `c238f0e60045d04eb7e7c976ca5349a7bb81efab`이며 [CI](https://github.com/Simon-YHKim/Lecture/actions/runs/34894484103)와 총 252개 테스트가 통과했다. 마지막 영상 프레임이 일찍 끝나는 문제는 `fps=30` 확장과 정확한 트랙 길이·프레임 수·마지막 화면 검사로 수정했고, 모든 영상은 검증 버전 2다.
- **사람의 전체 청취와 실제 AutoCAD 실행 검수는 남아 있는 prerelease다.** 실습은 도해와 단계별 자습 슬라이드로 구성하며 실제 AutoCAD 조작 녹화는 포함하지 않는다. 명령어·파일명·좌표·기호 발음을 검수자에게 확인받는다. 검수자에게 메시지는 보내지 않았다.
- `local-materials/selfstudy-video-current.json`이 제작 기록 정본이다. `base` 아래 `assets/`, `public-release-validation.json`, `previous-release-preserved.json`, `retake-content-validation.json`, `voice-qa.json`, `completion-report.html`을 확인한다. 기존 릴리즈의 28개 자산 ID·크기·해시와 사용자 미커밋 파일은 보존했다. 참조 음성·개별 WAV·ASR 원문·모델·개인 경로는 공개하지 않았다. 제작·교정·검증·업로드 세션은 종료됐다.
