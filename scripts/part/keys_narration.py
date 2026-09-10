"""Regenerate the 「오늘 친 것」 narration from the command table.

That Line carried `<!-- generated: keys -->` but nothing generated it — the
paragraphs were written once by a throwaway script and left as plain text. So
the same three faults sat in all eight lessons: the terse 「~한다」 ending that
belongs on a card and not in speech, a 「은」 glued to every command whatever its
Korean reading ends in, and a usage phrase with no particle at all
(「원과 구멍 씁니다」).

Fixing twenty-nine sentences by hand would have left the rest of the 은/는
errors in place — the auditors hit their finding cap before reaching them — and
the next regeneration would have undone the lot. So the sentence is built here
instead, and the particle problem is removed rather than solved: nothing is
attached to the command at all.

    python scripts/part/keys_narration.py            # all lessons
    python scripts/part/keys_narration.py 3 5        # only these
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats  # noqa: E402
import lesson_kit as kit  # noqa: E402
import verify_course as vc  # noqa: E402

ROOT = "projects/autocad-technician"
MARK = "<!-- generated: keys -->"


def polite(terse):
    """간결체 「~한다」 to 존댓말 「~합니다」.

    Two shapes cover the whole command table. A stem that already ends in a
    consonant takes 는다 and becomes 습니다; otherwise 다 sits on a syllable
    closed by ㄴ, and that ㄴ becomes ㅂ — 그린다 to 그립니다, 잰다 to 잽니다.
    """
    if terse.endswith("는다"):
        return terse[:-2] + "습니다"
    if terse.endswith("다"):
        code = ord(terse[-2]) - 0xAC00
        if 0 <= code < 11172 and code % 28 == 4:        # 종성 ㄴ → ㅂ
            return terse[:-2] + chr(0xAC00 + code + 13) + "니다"
    raise ValueError("존댓말로 바꿀 수 없는 어미: %r" % terse)


def usage(when):
    """The first clause of the usage note, closed with 씁니다.

    Only the first clause is spoken. The rest is an aside that belongs on the
    card, where the reader can take it at their own pace.
    """
    head = when.split(". ")[0]
    if head.endswith("같다"):
        return head[:-2] + "같습니다"
    if head.endswith(("때", "전")):
        return head + " 씁니다"
    return head + "에 씁니다"


def sentence(n, key):
    """One numbered paragraph.

    The command is followed by a full stop, never by 은/는. Korean picks that
    particle from the sound the word ends in, and the sound of an abbreviation
    is its Korean reading — 제트, 엘아이, 세이브애즈 — which no rule can get from
    the letters. Ending the clause sidesteps it, and matches how anyone would
    actually say this out loud.
    """
    full, what, when = kit.COMMANDS[key]
    name = "" if full == key else " %s." % full
    return "(%d) `%s`.%s %s. %s." % (n, key, name, polite(what), usage(when))


def keys_line(script_path, demo_line):
    keys = beats.shortcuts_in(script_path, demo_line)
    lead = ("오늘 친 명령을 한 번에 모아 봅니다. 명령 이름보다 **언제 쓰는지**를 "
            "기억하시면 됩니다.\n    시험이 끝나도 남는 건 그쪽입니다.")
    body = "\n\n".join("    " + sentence(i, k) for i, k in enumerate(keys, 1))
    return "    " + lead + "\n\n" + body + "\n", len(keys)


def rewrite(slug):
    d = os.path.join(ROOT, slug)
    path = os.path.join(d, "SCRIPT.md")
    text = io.open(path, encoding="utf-8").read()
    if MARK not in text:
        return None

    head_re = re.compile(r"^## Line (\d+) .*%s\s*$" % re.escape(MARK), re.M)
    m = head_re.search(text)
    line_no = int(m.group(1))
    start = m.end()
    nxt = text.find("\n## Line ", start)
    end = len(text) if nxt < 0 else nxt

    block = text[start:end]
    tm = re.search(r"\n\*\*Time:\*\*[^\n]*\n", block)
    keep = block[: tm.end()] if tm else "\n\n"

    demo = 5 if beats.parse_steps(path, 5) else 8
    fresh, n = keys_line(path, demo)
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        text[:start] + keep + "\n" + fresh + text[end:])
    return line_no, n


def main(argv):
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(here)
    want = {int(a) for a in argv}
    for i, (slug, _a, _b) in enumerate(vc.LESSONS, 1):
        if want and i not in want:
            continue
        got = rewrite(slug)
        print("  %-32s %s" % (slug, "Line %d · 명령 %d개" % got if got else "keys 블록 없음"))


if __name__ == "__main__":
    main(sys.argv[1:])
