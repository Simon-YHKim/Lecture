# RECORDING GUIDE

차시마다 화면 녹화 구간이 하나씩 있다. 슬롯 이름은 언제나 `DEMO-01` 이다.

| 차시 | 주제 | 여는 파일 | 저장하는 상태 | 단계 | 예상 길이 |
| --- | --- | --- | --- | --- | --- |
| 2 | 부품 이해와 도면 환경 | — | L02_TEMPLATE | 16 | 9:50 |
| 3 | 기준선과 외곽 | L02_TEMPLATE | L03_PROFILE | 16 | 16:20 |
| 4 | 원·호·오프셋 | L03_PROFILE | L04_FEATURES | 16 | 16:20 |
| 5 | 제3각법 3뷰와 반복 | L04_FEATURES | L05_VIEWS | 16 | 24:30 |
| 6 | 편집과 표현 | L05_VIEWS | L06_REPRESENTED | 16 | 19:50 |
| 7 | 치수와 출도 | L06_REPRESENTED | L07_RELEASE | 16 | 25:50 |

예상 길이는 그 차시 `SCRIPT.md` Line 5 의 낭독 시간 × 1.3 이다.
타이핑과 대화상자와 기다리는 시간은 말하지 않기 때문이다.

## 녹화하기 전에

1. 그 차시 `SCRIPT.md` 의 Line 5 를 처음부터 끝까지 읽는다. 단계 순서가 곧 녹화 순서다.
2. **여는 파일**을 연다. 새로 만들지 않는다. 앞 차시가 저장한 상태에서 이어 그린다.
3. 화면 배율을 100%로 두고 1920×1080 으로 녹화한다. 프레임 안 삽입 영역이 그 비율이다.
4. 명령행이 보이게 둔다. 학습자가 따라 칠 값이 거기 뜬다.
5. 마지막 단계는 언제나 새 이름으로 저장이다. 저장까지 녹화한다.

## 녹화한 뒤

녹화 파일은 **저장소 밖 비공개 위치**에 둔다. 옮겨 오지 않는다.

    python scripts/part/ingest_recording.py <차시> <녹화파일>

이 명령이 두 파일을 쓴다.

- `recording.json` — 길이·해상도·프레임레이트만. 공개되고 커밋된다.
- `media.local.json` — 파일의 절대경로. gitignore 되며 미리보기만 읽는다.

그다음 그 차시를 다시 만들면 DEMO 프레임이 **예상치가 아니라 실제 길이**가 된다.

    python scripts/part/scaffold_lessons_3_7.py <차시번호>

현재 상태는 언제든 확인할 수 있다.

    python scripts/part/ingest_recording.py --list

## 목소리를 녹음했다면

화면 녹화와 별개로 나레이션을 녹음했다면, 항목이 등장하는 시각을
**추정이 아니라 실제 음성**에 맞출 수 있다.

    pwsh -File scripts/transcribe-narration.ps1 -AudioPath <음성파일>
    pwsh -File scripts/build-narration-timing.ps1 -LessonPath <차시> -TranscriptPath <위 결과>

받아쓴 글은 비공개 위치에 남고, 저장소에는 숫자만 담긴 `narration-timing.json` 만
들어온다. 그 파일이 있으면 스캐폴드가 음절 추정 대신 실측 시각을 쓴다.
지금 타이밍은 초당 5.0음절 가정이라, 실제 낭독이 그보다 빠르거나 느리면
화면이 말보다 앞서거나 뒤처진다.

## 길이가 다르면

손으로 프레임을 맞추지 않는다. 대본을 고치고 다시 만들거나, 위 방법으로
실측값을 넣는다. 길이의 원본은 대본이다 (`LESSON_STYLE.md` 14번).
