"""Measure how long the course's Korean actually takes to say, and fit a model.

The old estimate counted characters: a Hangul block was one unit, a digit was
one, and a run of Latin was `max(2, len // 2)`. That is wrong in a way that
matters here, because the recording steps are mostly coordinates and command
names. `@120,0` counted as four units and takes 1.9 seconds to say; `DTEXT`
counted as two and takes 0.7. So the frames that carry the most typing were the
ones estimated worst, and they came out shorter than the words that go in them.

Nothing here is guessed. Windows ships a Korean voice, so every paragraph in
every script is spoken to a wave file and the wave length read back, and every
non-Hangul token is measured the same way inside a carrier phrase. What is left
over — articulation rate, the pause at a full stop, the pause at a comma, the
silence at a paragraph's edges — is solved by least squares against those
measurements.

The voice is not a person. It is a real Korean reading of these exact words at a
steady pace, which makes it a reference rather than a prediction: `speech.PACE`
scales it to whoever is actually recording. Once a recording exists,
`beats.load_measured` takes over and none of this is consulted.

    python scripts/part/measure_speech.py            # remeasure and refit
    python scripts/part/measure_speech.py --check    # report drift, write nothing

Needs Windows with the ko-KR voice installed. On any other machine the committed
`speech_costs.json` is used as-is.
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import verify_course as vc  # noqa: E402

ROOT = "projects/autocad-technician"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "speech_costs.json")
VOICE = "Microsoft Heami Desktop"
CARRIER = "그리고"
REPEATS = 3

HAN = re.compile(r"[가-힣]")
TOK = re.compile(r"[^가-힣\s]+")
SENT = re.compile(r"[.?!]")
COMMA = re.compile(r"[,·]")
_TRIM = ".,·—「」()"

_PS = r"""
param([string]$InFile, [string]$OutFile)
Add-Type -AssemblyName System.Speech
$syn = New-Object System.Speech.Synthesis.SpeechSynthesizer
$syn.SelectVoice("%s")
$syn.Rate = 0
$rows = [System.Collections.Generic.List[string]]::new()
$tmp = Join-Path $env:TEMP ("hf-speech-{0}.wav" -f $PID)
foreach ($ln in [IO.File]::ReadAllLines($InFile, [Text.Encoding]::UTF8)) {
  if ([string]::IsNullOrWhiteSpace($ln)) { continue }
  $p = $ln.Split("`t", 2)
  if ($p.Length -lt 2) { continue }
  $syn.SetOutputToWaveFile($tmp)
  $syn.Speak($p[1])
  $syn.SetOutputToNull()
  $fs = [IO.File]::OpenRead($tmp)
  $h = New-Object byte[] 44
  [void]$fs.Read($h, 0, 44)
  $rate = [BitConverter]::ToInt32($h, 28)
  $sec = [math]::Round(($fs.Length - 44) / $rate, 3)
  $fs.Close()
  $rows.Add(("{0}`t{1}" -f $p[0], $sec))
}
Remove-Item $tmp -Force -ErrorAction SilentlyContinue
[IO.File]::WriteAllLines($OutFile, $rows, [Text.Encoding]::UTF8)
""" % VOICE


def say(pairs):
    """{key: seconds} for [(key, text), ...], spoken by the reference voice."""
    d = tempfile.mkdtemp(prefix="hf-speech-")
    src, dst, ps = (os.path.join(d, n) for n in ("in.tsv", "out.tsv", "say.ps1"))
    io.open(src, "w", encoding="utf-8", newline="\n").write(
        "".join("%s\t%s\n" % kv for kv in pairs))
    io.open(ps, "w", encoding="utf-8", newline="\n").write(_PS)
    subprocess.run(["pwsh", "-NoProfile", "-File", ps, "-InFile", src,
                    "-OutFile", dst], check=True, capture_output=True)
    out = {}
    for ln in io.open(dst, encoding="utf-8-sig"):
        if ln.strip():
            k, v = ln.rstrip("\n").split("\t")
            out[k] = float(v)
    for p in (src, dst, ps):
        os.remove(p)
    os.rmdir(d)
    return out


def clean(t):
    """What the narrator says. The markdown is punctuation for the reader."""
    t = re.sub(r"`([^`]*)`", r"\1", t)
    t = re.sub(r"\*\*([^*]*)\*\*", r"\1", t)
    t = re.sub(r"^\(\d+[^)]*\)\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()


def paragraphs():
    """Every spoken paragraph in the course, keyed by lesson, line and index."""
    out = []
    for i, (slug, _a, _b) in enumerate(vc.LESSONS, 1):
        p = os.path.join(ROOT, slug, "SCRIPT.md")
        sc = beats.parse_script(p)
        steps = beats.parse_steps(p, 5) or beats.parse_steps(p, 8)
        if steps:
            sc[5 if beats.parse_steps(p, 5) else 8] = list(steps)
        for ln in sorted(sc):
            for k, item in enumerate(sc[ln]):
                t = clean(item[1] if isinstance(item, (list, tuple)) else item)
                if t:
                    out.append(("L%d.%d.%d" % (i, ln, k), t))
    return out


def tokens(paras):
    seen = set()
    for _k, t in paras:
        for m in TOK.findall(t):
            m = m.strip(_TRIM)
            if m:
                seen.add(m)
    return sorted(seen)


def solve(X, y):
    m = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) for j in range(m)]
         + [sum(r[i] * v for r, v in zip(X, y))] for i in range(m)]
    for i in range(m):
        p = max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        d = A[i][i]
        A[i] = [v / d for v in A[i]]
        for r in range(m):
            if r != i and A[r][i]:
                f = A[r][i]
                A[r] = [a - f * b for a, b in zip(A[r], A[i])]
    return [A[i][m] for i in range(m)]


def measure():
    paras = paragraphs()
    toks = tokens(paras)

    # A token is measured in the middle of a carrier so that the lengthening a
    # word gets at the end of an utterance does not land in its cost.
    probe = [("CARRIER", " ".join([CARRIER] * (REPEATS + 1)))]
    probe += [(t, (" %s " % t).join([CARRIER] * (REPEATS + 1))) for t in toks]
    raw = say(probe)
    base = raw.pop("CARRIER")
    cost = {t: round(max((raw[t] - base) / REPEATS, 0.0), 4) for t in toks}

    obs = say(paras)

    # T = H·s + Σcost + P·(문장−1) + K·쉼표 + E
    X, y, feat = [], [], {}
    for k, t in paras:
        h = len(HAN.findall(t))
        c = sum(cost.get(m.strip(_TRIM), 0.0) for m in TOK.findall(t)
                if m.strip(_TRIM))
        s = max(len(SENT.findall(t)) - 1, 0)
        m = len(COMMA.findall(t))
        feat[k] = (h, c, s, m)
        X.append([h, s, m, 1.0])
        y.append(obs[k] - c)
    per_syl, sent, comma, edge = solve(X, y)

    res = []
    for k, _t in paras:
        h, c, s, m = feat[k]
        res.append(abs(h * per_syl + c + s * sent + m * comma + edge - obs[k])
                   / max(obs[k], 0.01))
    res.sort()

    # Unmeasured tokens still have to cost something, predicted from shape.
    XT = [[len(re.findall(r"[0-9]", t)), len(re.findall(r"[A-Za-z]", t)),
           len(re.findall(r"[^0-9A-Za-z가-힣\s]", t)), 1.0] for t in toks]
    digit, latin, symbol, tok_base = solve(XT, [cost[t] for t in toks])

    return {
        "note": ("Windows ko-KR 음성으로 실측한 값이다. 손으로 고치지 말고 "
                 "measure_speech.py 를 다시 돌려라."),
        "voice": VOICE,
        "rate": 0,
        "method": {
            "carrier": CARRIER,
            "repeats": REPEATS,
            "paragraphs": len(paras),
            "tokens": len(toks),
        },
        "model": {
            "secPerSyllable": round(per_syl, 5),
            "sentencePause": round(sent, 4),
            "commaPause": round(comma, 4),
            "paragraphEdge": round(edge, 4),
        },
        "unknownToken": {
            "perDigit": round(digit, 4),
            "perLatin": round(latin, 4),
            "perSymbol": round(symbol, 4),
            "base": round(tok_base, 4),
        },
        "fit": {
            "medianError": round(res[len(res) // 2], 4),
            "p90Error": round(res[int(len(res) * 0.9)], 4),
            "totalSeconds": round(sum(obs.values()), 1),
        },
        "tokenCost": cost,
    }


def main(argv):
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    fresh = measure()
    m, f = fresh["model"], fresh["fit"]
    print("  문단 %d · 토큰 %d" % (fresh["method"]["paragraphs"],
                                   fresh["method"]["tokens"]))
    print("  조음 %.2f 음절/초 · 마침표 %.2fs · 쉼표 %.2fs · 가장자리 %.2fs"
          % (1 / m["secPerSyllable"], m["sentencePause"], m["commaPause"],
             m["paragraphEdge"]))
    print("  중앙 오차 %.1f%% · 90퍼센타일 %.1f%% · 낭독 합계 %.1f분"
          % (f["medianError"] * 100, f["p90Error"] * 100, f["totalSeconds"] / 60))

    if "--check" in argv:
        old = json.load(io.open(OUT, encoding="utf-8"))
        drift = abs(fresh["fit"]["totalSeconds"] - old["fit"]["totalSeconds"])
        print("  기존 %.1f분 대비 %+.1f초" % (old["fit"]["totalSeconds"] / 60,
                                              fresh["fit"]["totalSeconds"]
                                              - old["fit"]["totalSeconds"]))
        return 1 if drift > 30 else 0

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(fresh, ensure_ascii=False, indent=2, sort_keys=False) + "\n")
    print("  %s 갱신" % os.path.basename(OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
