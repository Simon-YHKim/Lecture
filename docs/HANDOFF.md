# HANDOFF — AutoCAD 기능사 강좌

이 파일이 세션 간 인수인계의 정본이다. 세션을 시작하면 먼저 읽고, 끝낼 때 갱신한다.
최신 블록만 `## Latest` 를 달고, 이전 블록은 `## <날짜>` 로 내린다.

> 지난 블록은 월별로 내렸다 — [`docs/handoff-archive/`](handoff-archive/) · [9월 후속 보관](handoff-archive/2026-09-part2.md).
> 최신 블록과 직전 블록만 이 파일에 둔다. 한 파일 100KB 를 넘기지 않기 위해서다.

> 최종 갱신 **2026-09-15 08:26:34 KST** · Codex · 커밋은 이 파일의 git 이력 참조

---

## Latest — 2026-09-15 / 차시별 자습 슬라이드·영상 국영문 릴리즈 완료

- 사용자 확정 범위인 **국문 HTML 슬라이드 8개·MP4 8개 + 영문 HTML 슬라이드 8개·MP4 8개**, 총 32개를 제작하고 [GitHub 검수 릴리즈](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.15-selfstudy-review.1)로 공개했다. 자습 슬라이드마다 해당 대본을 통합했고 같은 화면에 선생님 복제 음성을 입혔다. 기존 강의 영상과 구분되는 차시별 자습 영상이다.
- [국문 전체 ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.15-selfstudy-review.1/AutoCAD_KO_SELFSTUDY.zip) · [영문 전체 ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.15-selfstudy-review.1/AutoCAD_EN_SELFSTUDY.zip). ZIP 전체 압축을 풀고 `START_REVIEW_KO.html` 또는 `START_REVIEW_EN.html`을 Chrome/Edge에서 열면 대본 클릭 이동, 같은 슬라이드 열기, 시간별 의견 JSON 저장이 된다. 각 ZIP은 차시별 HTML·MP4·MD·VTT·SRT와 검수 페이지·안내·매니페스트·체크섬 등 44개 파일이다. 릴리즈에는 핵심 32개, ZIP 2개, 가이드·매니페스트·체크섬을 합쳐 37개 자산이 있다.
- 국문은 222장·4:12:55, 영문은 263장·4:39:36이다. 1920×1080/30fps H.264/AAC, 음성은 원래 속도 1.00×다. 기존 승인 화면 124장의 음성을 재사용하고 새 자습 361장의 1,328토막을 만들었다. 영문 합성 입력의 숫자는 영어 단어로 명시했으며 표시 수치·좌표·대본은 유지했다.
- 새 음성 1,328토막을 현재 WAV 해시 기준으로 자동 대조했고 빈 인식·길이 의심은 0개다. 두 독립 CPU 인식기로 확인한 KO5 저장 안내, KO6 파일명 반복, EN2 방향, EN3 반복, EN5 높이·60/for 경계, EN6 L 명령, EN7 5×5·나사 개수·95.7, EN8 중심선 축척 등 11토막을 교정했다. 동음 표기 차이는 원문·별도 인식·실제 음성 토막의 경계로 재확인했고 원래 인식 결과를 보존했다. 사람이 청취한 것으로 보고하지 않는다.
- 모든 MP4의 전체 디코딩, 영상·음성 트랙 길이와 프레임 수, 자막 문자·시각, 원본 음성 표본, 모든 출력 화면과 마지막 프레임을 검사했다. 교정 전후 대본·자막 문자·슬라이드 화면 보존과 국영문 8차시 검수 플레이어를 확인했다. 공개 텍스트 91개 및 MP4 메타데이터에서 비공개 경로·자산을 검사했다. 37개 공개 다운로드 모두 비로그인 HTTP 200·크기·GitHub SHA-256 일치를 확인했다.
- 제작 소스는 `c238f0e60045d04eb7e7c976ca5349a7bb81efab`이며 [CI](https://github.com/Simon-YHKim/Lecture/actions/runs/34894484103)와 총 252개 테스트가 통과했다. 마지막 영상 프레임이 일찍 끝나는 문제는 `fps=30` 확장과 정확한 트랙 길이·프레임 수·마지막 화면 검사로 수정했고, 모든 영상은 검증 버전 2다.
- **사람의 전체 청취와 실제 AutoCAD 실행 검수는 남아 있는 prerelease다.** 실습은 도해와 단계별 자습 슬라이드로 구성하며 실제 AutoCAD 조작 녹화는 포함하지 않는다. 명령어·파일명·좌표·기호 발음을 검수자에게 확인받는다. 검수자에게 메시지는 보내지 않았다.
- `local-materials/selfstudy-video-current.json`이 제작 기록 정본이다. `base` 아래 `assets/`, `public-release-validation.json`, `previous-release-preserved.json`, `retake-content-validation.json`, `voice-qa.json`, `completion-report.html`을 확인한다. 기존 릴리즈의 28개 자산 ID·크기·해시와 사용자 미커밋 파일은 보존했다. 참조 음성·개별 WAV·ASR 원문·모델·개인 경로는 공개하지 않았다. 제작·교정·검증·업로드 세션은 종료됐다.

---

## 2026-09-14 / 국문·영문 대본 통합 검수 릴리즈 공개

- 사용자 위임에 따라 [검수 릴리즈](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.14-review.1)를 공개했다. 국문·영문 MP4 8개씩, 전체 ZIP 2개, 영상 제외 자료 ZIP과 개별 덱·워크북 등 28개 자산이다. 모든 다운로드를 비로그인 HTTP 200·크기·원격 SHA-256으로 확인했다.
- 릴리즈 소스는 `cd73dbe868cd2dc12d3aca24eed3e3d6d4d43f4f`다. 원본 승인 대본 16개, 본문 변경 68개, 현재 음성 2,223토막을 반영했으며 국문 총 211:43·영문 총 253:27이다. 배속은 1.00이다.
- 슬라이드 국문 222장·영문 263장에 차시별 전체 대본을 넣고 자습 분권 40개씩과 통합 워크북을 함께 제공했다. ZIP 전체 압축을 해제하고 `START_REVIEW_KO.html` 또는 `START_REVIEW_EN.html`을 열면 대본 클릭 이동과 시간별 의견 JSON 내보내기를 사용할 수 있다.
- MP4 16개 전체 디코딩·자막 문자/시각 왕복·장면별 음성/인코딩 화면 대조, 원본 장면 검사 170개, 자동 테스트 225개, 국영문 브라우저·공개 자료 가드·ZIP CRC를 통과했다. 화면 자동 비교의 글꼴 위치 차이는 실제 두 화면을 본 뒤 원본·MP4 해시에 묶어 기록했다.
- `<>` 측정값 자리표시는 원문을 보존한 VTT 결합으로 해결했다. 모든 2,223개 자막의 문자·시각을 확인했으며 검수 플레이어·MP4 내장 자막·VTT 사용을 안내했다.
- **최종 강의 승인판은 아니다.** 언어별 2~7차시 실제 AutoCAD 실습 녹화 15자리는 PREVIEW이며 실제 실행·전체 사람 청취는 남아 있다. 영문 4차시 14:03~14:36 F8/ortho와 16:47~17:03의 315 뒤 반복 가능 구간을 우선 검수한다. 검수자에게 메시지는 보내지 않았다.
- `local-materials/release-review-current.json`이 제작 기록 정본이다. 여기의 비공개 위치에 원본 MP4·프로젝트·검증 로그를 보존했다. `assets/release-manifest.json`·`release-upload-plan.json`·`public-release-validation.json`이 최종 파일 및 공개 검증 근거다. 참조 음성·개별 WAV·ASR 원문·개인 경로는 공개하지 않았다.
