# STATE — AutoCAD 기능사 강좌

덮어쓰기 파일. 네 절만. 갱신 2026-09-12 03:13 KST · Claude Code (Opus 5)

## 완료

- 자습 교재·도면·프레임 지도·대본: **국문·영문 여덟 차시 전부**.
- 공개판 `autocad-2026.09.11-preview.2` 게시 (자습/강의 × 국문/영문 12개 파일).
- 대본 검토(73건) 반영 — 발음 165자리 + 문장 33곳. 감정 태그본 16개.
- 복제 음성 경로 구축: `tts_jobs.py`(작업 목록) · `speak_clone.py`(생성) ·
  `ingest_voice.py`(받아쓰기·시각) · 시험 2개. 부품 시험 141개 통과.
- 환경 확인(실행값): RTX 4070 SUPER · 12GB · compute 8.9 · torch 2.11.0+cu128 ·
  qwen-tts 0.1.1 · RAM 31.6GB. flash-attn 없음(Windows 빌드 필요) → sdpa.

## 진행중

- **국문 음성 1,184토막 생성.** 배치 크기를 재는 중 — 낱개 27초/토막(실시간
  0.28배), 배치 8 은 호스트 RAM 초과로 죽었고 배치 2 는 RSS 2.1GB 로 안전.
- 브랜치 `feat/clone-voice-pipeline` · 커밋 2개 · **push 안 함**.

## 다음 1개

**배치 크기를 확정하고 국문 전량(1,184토막) 생성을 시작한다.**
그 뒤 영문 1,036토막 → `ingest_voice.py` → `retime_frames.py` →
`prepare_lecture.py`(1·8차시는 배포본, 2~7차시는 `--preview`).

## 막힌 것

- **PR #50 빨강.** 국문 7차시 `narration-timing.json` 이 검토 반영 전 대본에
  묶여 `check-course-projects.ps1` 이 막는다. 복제 음성으로 다시 만들면 풀린다.
- **2~7차시 배포본 영상** — AutoCAD 화면 녹화 15개(`DEMO-01`,
  `DEMO-01A/B/C` ×5)가 없다. 사용자만 만들 수 있다. preview 렌더는 가능.
- 작도 안내 P2 잔여 5건.
