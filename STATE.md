# STATE — AutoCAD 기능사 강좌

덮어쓰기 파일. 네 절만. 갱신 2026-09-12 09:24 KST · Claude Code (Opus 5)

## 완료

- 자습 교재·도면·프레임 지도·대본: **국문·영문 여덟 차시 전부**.
- 공개판 `autocad-2026.09.11-preview.2` 게시 (자습/강의 × 국문/영문 12개 파일).
- 대본 검토(73건) 반영 — 발음 165자리 + 문장 33곳. 감정 태그본 16개.
- **1차시 국문 영상 완성** — 복제 음성 · 20.6MB · 6분 21초 ·
  `hyperframes check` 오류 0. 무음 제거까지 반영한 판이다(v1 6:49 → v2 6:21).
- 복제 음성 파이프라인: `tts_jobs.py` → `speak_clone.py` → `retrim_clone.py`
  → `ingest_voice.py` → `retime_frames.py` → `prepare_lecture.py`. 시험 159개.
- 영문 사본 8개 (`C:/Users/202502/AppData/Local/Temp/en-lessons`) — 작업 목록과
  문단·토막·본문 **완전 일치**. 재부팅을 넘겼다.
- 환경(실행값): RTX 4070 SUPER · 12GB · compute 8.9 · torch 2.11.0+cu128 ·
  qwen-tts 0.1.1 · RAM 31.6GB. flash-attn 없음 → sdpa.

## 진행중

- **국문 음성 511 / 1,184 토막** · 1.69배속 · VRAM 4.3GB · 의심 0 · 남은 ~70분.
  세션 밖 프로세스(`Start-Process`)라 이 대화가 끊겨도 계속 돈다.
- 브랜치 `feat/clone-voice-pipeline` · 커밋 10개 · **push 안 함**.

## 다음 1개

**국문이 끝나면 전량 재다듬기 → `scratchpad/finish.py ko 02 … 08`**
(받아쓰기 · 재동기 · 묶기 · 검사) → 영상 8편 렌더(2~7은 `--preview`) →
영문 1,036토막 → 같은 체인.

## 막힌 것

- **PR #50 빨강.** 국문 7차시 `narration-timing.json` 이 검토 반영 전 대본에
  묶여 있다. 이번 복제 음성이 그 일곱 차시를 다 갈아 치우면 함께 풀린다.
- **2~7차시 배포본 영상** — AutoCAD 화면 녹화 15개(`DEMO-01`,
  `DEMO-01A/B/C` ×5)가 없다. 사용자만 만들 수 있다. preview 렌더는 가능하고
  사용자가 그렇게 하라고 정했다.
- 작도 안내 P2 잔여 5건 — 실제 조작·원본 대조가 필요해 위 녹화와 함께 묶인다.
