# STATE — AutoCAD 기능사 강좌

덮어쓰기 파일. 네 절만. 갱신 2026-09-13 15:00 KST · Claude Code (Opus 5)

## 완료

- **여덟 차시 국문·영문 전편이 복제 음성으로 다시 만들어졌다.**
  국문 211분 · 영문 248분. 배속 1.0(사람 말투라 올릴 이유가 없다).
- **영상 16편.** 국문 545MB · 영문 681MB. 2~7차시는 `_PREVIEW`
  (AutoCAD 화면 녹화 자리가 비어 있다). 1·8차시는 그대로 완성본이다.
- **공개판 `autocad-2026.09.13-clone.1`** — 자산 26개 1.2GB, 전부 `uploaded`.
  자습 KO/EN(38·37장 + 워크북) · 강의 KO/EN(대본 8차시 + 덱 + 영상 8편) ·
  `SHA256SUMS.txt` · `release-manifest.json`.
- 복제 음성 파이프라인과 시험 150개. `tts_jobs.py` → `speak_clone.py` →
  `retrim_clone.py` → `ingest_voice.py` → `retime_frames.py` →
  `prepare_lecture.py`. Colab 노트북은 예비로 남겼다.
- **검증** — 대역 밖 토막 0개(국문 1,184 · 영문 1,036). 문단 경계는 합친 PCM 을
  다시 재서 얻은 실측값. `hyperframes check` 는 1·8차시 통짜, 2~7차시 장면별
  (국문 71 · 영문 73장면 전부 통과). `check-course-projects.ps1` 여덟 차시 통과.

## 진행중

- 없음. 브랜치 `feat/clone-voice-pipeline` 에 커밋 15개가 **push 되지 않은 채**
  남아 있다 — 머지 여부는 사용자가 정한다.

## 다음 1개

**브랜치를 올릴지 정한다.** `git push -u origin feat/clone-voice-pipeline` 뒤
PR 을 열면 PR #50 은 닫아도 된다 — 그것이 막혀 있던 이유(국문 7차시의
`narration-timing.json` 이 검토 반영 전 대본에 묶임)가 이 브랜치에서 풀렸다.

## 막힌 것

- **2~7차시 배포본 영상** — AutoCAD 화면 녹화 15개(`DEMO-01`,
  `DEMO-01A/B/C` ×5)가 없다. 사용자만 만들 수 있다. 녹화가 들어오면
  `--preview` 를 떼고 다시 렌더하면 된다(대본·음성·시각은 이미 서 있다).
- 작도 안내 P2 잔여 5건 — 위 녹화와 함께 묶인다.
- 참조 음성이 `base.wav` 하나라 여덟 차시가 한 말투로 나온다. `refs/` 에
  careful·firm·light 를 10~15초씩 넣으면 그 mood 토막만 다시 만들면 된다
  (국문 422개 · 36%). `done.jsonl` 이 sha 로 가려 전체 재생성이 아니다.
