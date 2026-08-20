"""How long a paragraph of this course's Korean takes to say.

    T  =  H·s  +  Σ cost(token)  +  P·(문장 수 − 1)  +  K·쉼표 수  +  E

Every term on the right was measured rather than assumed — see
`measure_speech.py` for how, and `speech_costs.json` for the numbers. Across the
477 paragraphs the course actually contains, the median error is under 2%.

The two things worth knowing before touching this:

**Tokens are measured, not spelled out.** There is no table mapping `120` to
「백이십」. Asking a Korean voice to say `@120,0` inside a carrier phrase and
subtracting the carrier gives 1.9 seconds, and 1.9 seconds is the answer
regardless of how the syllables would be written down. That sidesteps every
edge case a transliteration table would have to get right — `Ø56`, `2-C5`,
`@7.07<135`, `L02_TEMPLATE` — and it is why the recording steps, which are
almost entirely such tokens, are now estimated as well as the prose is.

**`PACE` is the only dial.** 1.0 is the reference voice: 5.4 syllables a second
of articulation with the pauses above. Someone reading briskly is nearer 0.85,
someone taking their time nearer 1.15. It scales articulation and pauses alike,
because a faster reader shortens both. Set it from a real reading — say a
paragraph aloud, time it, divide.

None of this survives contact with a recording. Once `narration-timing.json`
exists for a lesson, `beats.load_measured` uses the observed times and this
module is not consulted for that lesson at all.
"""

import io
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_DOC = json.load(io.open(os.path.join(_HERE, "speech_costs.json"),
                         encoding="utf-8"))

_M = _DOC["model"]
SEC_PER_SYL = _M["secPerSyllable"]
SENTENCE_PAUSE = _M["sentencePause"]
COMMA_PAUSE = _M["commaPause"]
EDGE = _M["paragraphEdge"]

_U = _DOC["unknownToken"]
COST = _DOC["tokenCost"]

#: Scales the reference voice to whoever is recording. See the module docstring.
PACE = 1.0

_HAN = re.compile(r"[가-힣]")
_TOK = re.compile(r"[^가-힣\s]+")
_SENT = re.compile(r"[.?!]")
_COMMA = re.compile(r"[,·]")
_MD_CODE = re.compile(r"`([^`]*)`")
_MD_BOLD = re.compile(r"\*\*([^*]*)\*\*")
_LABEL = re.compile(r"^\(\d+[^)]*\)\s*")
_TRIM = ".,·—「」()"

_unknown = set()


def spoken(text):
    """The words as said. Markdown is punctuation for the reader, not speech."""
    t = _MD_CODE.sub(r"\1", text)
    t = _MD_BOLD.sub(r"\1", t)
    t = _LABEL.sub("", t)
    return re.sub(r"\s+", " ", t).strip()


def token_cost(tok):
    """Seconds for one non-Hangul token.

    A token nobody has measured is predicted from its shape and remembered, so
    `unmeasured()` can report it and the next measurement run can pick it up.
    """
    if tok in COST:
        return COST[tok]
    _unknown.add(tok)
    return max(_U["base"]
               + _U["perDigit"] * len(re.findall(r"[0-9]", tok))
               + _U["perLatin"] * len(re.findall(r"[A-Za-z]", tok))
               + _U["perSymbol"] * len(re.findall(r"[^0-9A-Za-z가-힣\s]", tok)),
               0.0)


def read_seconds(text, pace=None):
    """How long this paragraph takes to say, edges and internal pauses included."""
    t = spoken(text)
    if not t:
        return 0.0
    total = len(_HAN.findall(t)) * SEC_PER_SYL + EDGE
    total += max(len(_SENT.findall(t)) - 1, 0) * SENTENCE_PAUSE
    total += len(_COMMA.findall(t)) * COMMA_PAUSE
    for m in _TOK.findall(t):
        m = m.strip(_TRIM)
        if m:
            total += token_cost(m)
    return total * (PACE if pace is None else pace)


def unmeasured():
    """Tokens seen since import that had to be predicted rather than measured."""
    return sorted(_unknown)


def summary():
    f = _DOC["fit"]
    return ("%s · 조음 %.2f 음절/초 · 중앙 오차 %.1f%% · 문단 %d개로 맞춤"
            % (_DOC["voice"], 1 / SEC_PER_SYL, f["medianError"] * 100,
               _DOC["method"]["paragraphs"]))


if __name__ == "__main__":
    print("  " + summary())
    for s in ("선을 긋습니다.",
              "다음 점 `@120,0` 엔터. 오른쪽으로 120. 베이스 폭입니다.",
              "`DTEXT` 입력하고 엔터."):
        print("  %5.2fs  %s" % (read_seconds(s), s))
