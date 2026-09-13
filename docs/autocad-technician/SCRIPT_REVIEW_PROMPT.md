# 강의 대본 검토 프롬프트

다른 AI에게 국문·영문 대본을 **고쳐 달라고** 맡길 때 쓴다. 아래
「복사해 쓰는 프롬프트」를 통째로 붙이면 된다 — **파일을 첨부할 필요가 없다.**
저장소가 공개라 대본을 URL 로 직접 읽는다.

돌려받은 것은 이 저장소에서 다시 산출물로 만든다. 마지막 절
「돌아온 뒤 — 이 세션에 넘기는 법」이 그 방법이다.

## 앞선 판과 무엇이 다른가

이전 프롬프트는 **표로 제안만** 받았다. 이번에는 **고친 파일을 통째로** 받는다.
대신 검토자가 근거를 알고 고치도록 `SCRIPT_DESIGN_RATIONALE.md` 를 함께 읽힌다 —
왜 이렇게 썼는지 모르면 「이상하다」로 끝나고, 알면 「이 제약이라면 이렇게 푸는
게 낫다」로 간다.

---

## 복사해 쓰는 프롬프트

```text
당신은 기업 교육용 영상 강의의 대본을 다듬는 편집자입니다.
읽고 → 고치고 → 고친 파일을 통째로 돌려주는 일입니다.

# 먼저 읽을 것 (순서대로)

1) 이 대본이 왜 이렇게 쓰였는지 — 반드시 먼저 읽으세요
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/docs/autocad-technician/SCRIPT_DESIGN_RATIONALE.md

2) 국문 대본 8개 (문단마다 실측 시각이 붙은 판)
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-01-orientation/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-02-part-and-template/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-03-baseline-profile/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-04-circles-arcs/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-05-three-views/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-06-editing-symbols/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-07-dimensioning-release/SCRIPT.timed.ko.md
   https://raw.githubusercontent.com/Simon-YHKim/Lecture/feat/clone-voice-pipeline/projects/autocad-technician/lesson-08-exam-and-qa/SCRIPT.timed.ko.md

3) 영문 대본 8개 — 위 URL 에서 `SCRIPT.timed.ko.md` 를 `SCRIPT.timed.en.md`
   로 바꾸면 됩니다. 여덟 개 모두 있습니다.

URL 을 못 여는 환경이면 그렇다고 알려 주세요. 파일을 따로 드리겠습니다.

# 이 대본이 무엇인가

사내 기술직 인증 과정의 AutoCAD 2024 실습 강의 8차시 낭독 대본입니다.
듣는 사람은 제도를 처음 배우는 설비 담당자이고, 화면에는 그림·표·도면이
따로 있으며 이 글은 그 위에 얹히는 말입니다. 사람이 읽는 문서가 아니라
**음성 합성기가 소리 내어 읽는 원고**입니다.

**사내 교육물이라는 점을 반드시 지켜 주세요.** 유튜브 강의체(자극적인 후킹,
과장된 감탄, 농담)로 바꾸지 마세요. 현장에서 일하는 성인 동료에게 설명하는
말투입니다. 존중하되 거리를 두지 않는 톤입니다.

# 비판적으로 보셔도 됩니다

근거 문서를 읽고도 납득이 안 되는 결정이 있으면 **그렇게 적어 주세요.**
다만 근거 문서에 이미 이유가 적힌 것을 같은 근거로 되돌리자는 제안은 받지
않습니다. **다른 근거가 있으면 그 근거를 적어 주세요** — 그러면 다시 봅니다.

# 1순위 — 영문에서 엉뚱한 언어로 읽힐 자리

음성은 선생님 본인 목소리를 복제한 것인데, **참조로 쓴 녹음이 한국어**입니다.
그래서 영문을 읽을 때 한국어 발음이 새어 나옵니다. 실제로 잡힌 것:

    영문 대본의 "45 degrees" → 「사십오도 degrees」로 읽힘

영문 대본에 남은 기호 가운데 엔진이 한국어로 읽어 버릴 만한 것을 찾아
**영어 단어로 풀어 써 주세요.**

    Ø  (영문에 41곳)  → "diameter" 로 풀 수 있는가?
    °  ×  →  그리고 숫자에 바로 붙는 단위 (25H7, M5, R10, C5, PCD)

단, 아래 「바꾸면 안 되는 것」의 도면 표기와 충돌하면 **바꾸지 말고 충돌한다고
적어** 주세요. 판단은 제가 합니다.

# 2순위 — 삼켜질 문장

자기회귀 음성 모델은 긴 문장에서 단어를 빠뜨리고, **빠뜨려도 소리는 정상으로
납니다.** 그래서 긴 문장이 위험합니다.
  · 국문: 쉼표로 네 마디 이상 이어지는 문장
  · 영문: 25단어 넘는 복합절
문장을 나눠 주세요. **문단은 나누지 마세요**(아래 참조).

# 3순위 — 호흡과 분량

문단마다 `[m:ss–m:ss]` 로 실측 시각이 붙어 있습니다. 이것으로 봐 주세요.
  · 한 문단이 40초를 넘으면 듣는 사람이 놓칩니다 — 나눌 수 있는지
  · 30초 넘게 한 화면에 머무는데 말이 단조로운 자리
  · 반대로 2초짜리 문단이 연달아 나와 숨이 찬 자리
영문이 국문보다 18% 깁니다(248분 대 211분). **너무 길다고 판단되면 적어 주세요.**

# 4순위 — 소리로 구별이 안 되는 것 · 지시대명사

  · 숫자와 숫자가 붙어 하나로 들리는 자리 ("폭80입니다" → "폭 80입니다")
  · "이것", "그것", "여기"가 화면의 무엇인지 소리만으로 모호한 자리

# 바꾸면 안 되는 것 — 어기면 화면과 음성이 통째로 어긋납니다

1. **문단 수.** 추가·삭제·병합 금지. 빈 줄로 갈린 4칸 들여쓴 덩어리 하나가
   문단 하나이고, 그것이 화면의 한 강조에 묶여 있습니다.
   **문단 안에서 문장을 나누는 것은 괜찮습니다**(빈 줄을 넣지 않는 한).
   지금 문단 수는 차시 순서대로 46 · 103 · 60 · 68 · 56 · 61 · 63 · 31 이고
   **국문과 영문이 같아야 합니다.**
2. **문단 첫머리의 `(1 ...)` 표식.** 화면에서 밝아지는 항목 번호입니다.
3. **백틱 안의 글자** — `REC`, `Ctrl+S` 등. 실제로 치는 키입니다.
4. **제목 줄** — `## Line N`, `### N단계` / `### Step N`, `**Time:**`.
5. **`[m:ss–m:ss]` 시각 표시.** 그대로 두세요. 제가 다시 계산합니다.
6. **도면 표기** — `Ø25 H7`, `PCD Ø44`, `2-C5`, `4-M5`, `2-R10`.
   **국문 대본에서는** 이미 「파이 25 H7」처럼 한글 발음으로 풀어 두었습니다.
   그건 그대로 두세요(근거 문서 참조).
7. **과정 표준 용어** — "외형선", "중심선", "숨은선", "치수보조선".

# 어떻게 돌려주나

차시마다 **고친 파일 전체**를 코드블록으로 주세요. 16개입니다.
한 번에 다 어려우면 차시 하나씩 나눠 주셔도 됩니다.

    ## lesson-04-circles-arcs · ko
    ```markdown
    (고친 파일 전체)
    ```

파일 맨 앞의 `<!-- 생성물이다 ... -->` 주석은 빼고 주세요.

그리고 **맨 끝에 바꾼 것 요약표**를 하나 주세요.

| 차시 | 판 | 분류 | 무엇을 왜 바꿨나 | 문단 수 변화 |

분류는 언어누출 / 삼킴 / 호흡 / 구별 / 지시 / 문체 / 기타 중 하나입니다.
**문단 수 변화는 전부 0 이어야 합니다.** 0 이 아니면 그 차시는 못 씁니다.

# 하지 말아 달라

  · 문단을 나누거나 합치지 마세요.
  · 맞춤법·띄어쓰기만 고치는 변경은 하지 마세요(소리에 영향이 없으면 두세요).
  · 국문의 한글 발음 표기(「컨트롤 에스」, 「파이 25」)를 되돌리지 마세요.
  · 종결어미를 하나로 통일하지 마세요 — 일부러 섞은 것입니다.
  · 확신이 없으면 고치지 말고 요약표에 "검토 필요"로 적어 주세요.
```

---

## 돌아온 뒤 — 이 세션에 넘기는 법

돌려받은 16개 파일을 저장한 뒤, 이 저장소를 아는 세션에 아래를 그대로 붙인다.

```text
대본 검토본을 받아왔다. <경로>에 차시별로 들어 있다.
다음 순서로 반영해라.

1. 문단 수가 국문·영문 모두 46·103·60·68·56·61·63·31 인지 먼저 확인한다.
   하나라도 다르면 그 차시는 반영하지 말고 보고해라.
2. `[m:ss–m:ss]` 표시를 떼어 원본 형식으로 되돌린 뒤
   SCRIPT.md / SCRIPT.en.md 에 덮어쓴다.
3. python -m unittest discover -s scripts/part -p 'test_*.py'
4. python scripts/part/tts_jobs.py local-materials/qwen-narration --lang ko
   python scripts/part/tts_jobs.py local-materials/qwen-narration --lang en
   → 바뀐 토막만 sha 가 달라진다. 전체 재생성이 아니다.
5. python scripts/part/speak_clone.py --work local-materials/qwen-narration --lang ko
   (영문도 같은 방식. 세션 밖 프로세스로 띄울 것 — Start-Process)
6. 바뀐 차시만 ingest_voice → retime_frames → prepare_lecture → 렌더
7. 릴리즈 자산을 다시 만들어 올린다.
```

**되돌리는 비용은 작다.** `done.jsonl` 이 토막마다 글의 sha 를 들고 있어서,
글이 안 바뀐 토막은 다시 만들지 않는다. 열 문단을 고치면 열 문단어치만
다시 만든다.

## 왜 `/vibe` 를 쓰지 않는가

`/vibe` 는 일을 여러 워커에 쪼개 분산하는 스킬이다. 이 일은 **순서가 묶여
있어서**(대본 → 음성 → 시각 → 렌더 → 릴리즈) 쪼개도 이득이 없고, 중간 산출물이
크다(음성 2,220토막 · 영상 1.2GB). 한 세션에서 차례로 하는 것이 맞다.
검토 자체는 이미 바깥 AI 한 대에 맡기는 구조다.
