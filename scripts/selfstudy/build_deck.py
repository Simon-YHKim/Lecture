# -*- coding: utf-8 -*-
"""Build the course as a HyperFrames slideshow — one deck per language.

The self-study edition is read alone; a deck is spoken in front of people. So
this is not the same content reflowed. A slide carries the claim and at most
four supports at a size a room can read; the paragraph it came from goes into
the presenter notes, where it belongs. The rule the slideshow contract sets —
headline is a complete sentence, one idea per slide, nothing under 40px — is
what forces that split, and it is the right split for teaching anyway.

Two decks rather than one with a toggle: a presenter shows one language to one
room, and a deck that can silently be in the wrong language on a projector is a
worse failure than two files.

    python scripts/selfstudy/build_deck.py [출력 디렉터리]

Writes <out>/<lang>/composition/index.html plus a runnable wrapper.
"""
import html as _html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_selfstudy as B          # FIGURES, _find, SCRATCH

W, H = 1920, 1080
SLIDE_SEC = 8.0                       # every slide holds the same length; seek-driven
ACCENT = "#C7004C"                    # the course's crimson, from its own title frames
INK = "#F5F5F3"
DIM = "#A4A3A4"
GROUND = "#0B0A0A"
PANEL = "#151314"

MAX_BULLETS = 4
BULLET_CHARS = 46
HEAD_CHARS = 72

LANGS = (("ko", "국문"), ("en", "English"))
TICK = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")


def esc(s):
    return _html.escape(s or "", quote=False)


def rich(s):
    """Backticks become command chips; ** becomes emphasis. Nothing else."""
    out, i = [], 0
    for m in re.finditer(r"`([^`]+)`|\*\*([^*]+)\*\*", s or ""):
        out.append(esc(s[i:m.start()]))
        if m.group(1) is not None:
            out.append('<span class="cmd">%s</span>' % esc(m.group(1)))
        else:
            out.append("<b>%s</b>" % esc(m.group(2)))
        i = m.end()
    out.append(esc((s or "")[i:]))
    return "".join(out)


def plain(s):
    """The same string with the markup removed — for notes and length checks."""
    s = TICK.sub(r"\1", s or "")
    return BOLD.sub(r"\1", s)


def pick(node, lang):
    if not node:
        return ""
    if isinstance(node, str):
        return node
    return node.get(lang) or node.get("ko") or ""


def shorten(s, limit):
    """Cut on a clause boundary, never mid-word, and only when it must."""
    s = plain(s).strip()
    if len(s) <= limit:
        return s
    for sep in (". ", "다. ", "요. ", " — ", ", "):
        cut = s.rfind(sep, 0, limit)
        if cut > limit * 0.5:
            return s[:cut + len(sep)].strip().rstrip(",—")
    cut = s.rfind(" ", 0, limit)
    return (s[:cut] if cut > limit * 0.5 else s[:limit]).strip()


# ── pulling slide-sized content out of the self-study blocks ────────────────
def block_bullets(block, lang):
    t = block.get("type")
    if t == "list":
        return [pick(i, lang) for i in block.get("items", [])]
    if t == "cards":
        return ["%s — %s" % (pick(i.get("label"), lang), pick(i.get("body"), lang))
                for i in block.get("items", [])]
    if t == "table":
        rows = block.get("rows", [])
        return ["%s · %s" % (pick(r[0], lang), pick(r[1], lang)) if len(r) > 1
                else pick(r[0], lang) for r in rows]
    if t == "note":
        return [pick(block, lang)]
    return []


def section_slide(sec, lang):
    """{head, bullets, notes, figure} — the presentable core of one section."""
    label = pick(sec.get("label"), lang)
    head = pick(sec.get("lede"), lang) or label
    bullets, notes, figure = [], [], None
    for b in sec.get("blocks", []):
        if b.get("type") == "figure" and not figure:
            figure = b.get("ref")
        if b.get("type") == "p":
            txt = pick(b, lang)
            if txt:
                notes.append(plain(txt))
                if not bullets and not sec.get("lede"):
                    head = txt
        else:
            for x in block_bullets(b, lang):
                if x:
                    bullets.append(x)
                    notes.append(plain(x))
    short = [shorten(x, BULLET_CHARS) for x in bullets[:MAX_BULLETS]]
    return {"eyebrow": label, "head": shorten(head, HEAD_CHARS),
            "bullets": [s for s in short if s], "figure": figure,
            "notes": " / ".join(notes[:8])}


# ── slide rendering ─────────────────────────────────────────────────────────
def scene(sid, start, label, body, cls=""):
    return (
        '<div id="%s-scene" data-composition-id="%s" data-start="%s" data-duration="%s" '
        'data-label="%s" data-width="%d" data-height="%d" class="scene %s">'
        '<section id="%s-clip" class="clip" data-start="%s" data-duration="%s" '
        'data-track-index="1">%s</section></div>'
        % (sid, sid, start, SLIDE_SEC, esc(label), W, H, cls, sid, start, SLIDE_SEC, body))


def bullets_html(items, sid):
    if not items:
        return ""
    li = "".join('<li id="%s-b%d">%s</li>' % (sid, i, rich(x)) for i, x in enumerate(items))
    return '<ul class="pts">%s</ul>' % li


def cover_slide(C, lang, start):
    t = pick(C.get("courseTitle"), lang)
    s = pick(C.get("subtitle"), lang)
    body = ('<div class="cover">'
            '<p class="eyebrow">LG이노텍 Green Star · for technician</p>'
            '<h1 id="cover-h">%s</h1><p class="lede">%s</p>'
            '<p class="meta">EDU-IB-02 · A3 · %s</p></div>'
            % (rich(t), rich(s), "제3각법" if lang == "ko" else "third-angle projection"))
    return scene("cover", start, t, body, "dark")


def lesson_title_slide(L, lang, start):
    no = L["no"]
    t = pick(L.get("title"), lang)
    what = pick((L.get("summary") or {}).get("what"), lang)
    body = ('<div class="cover">'
            '<p class="eyebrow">%s %d / 8</p><h1 id="%s-h">%s</h1><p class="lede">%s</p></div>'
            % ("차시" if lang == "ko" else "Lesson", no, "l%02d-title" % no,
               rich(t), rich(shorten(what, 96))))
    return scene("l%02d-title" % no, start, "%d. %s" % (no, t), body, "dark")


def content_slide(sid, eyebrow, head, items, notes, figure, start, label):
    fig = ""
    if figure and figure in B.FIGURES:
        fig = '<div class="fig">%s</div>' % B.FIGURES[figure]
    body = ('<div class="pad %s"><p class="eyebrow">%s</p><h2 id="%s-h">%s</h2>%s%s</div>'
            % ("split" if fig else "", esc(eyebrow), sid, rich(head),
               bullets_html(items, sid), fig))
    return scene(sid, start, label, body)


def build_lang(C, lessons, lang):
    slides, scenes, tl, clock = [], [], [], 0.0

    scenes.append(cover_slide(C, lang, clock))
    slides.append({"sceneId": "cover",
                   "notes": plain(pick(C.get("audience"), lang))})
    tl.append(("cover", 0, clock))
    clock += SLIDE_SEC

    for L in lessons:
        no = L["no"]
        scenes.append(lesson_title_slide(L, lang, clock))
        slides.append({"sceneId": "l%02d-title" % no,
                       "notes": plain(pick((L.get("summary") or {}).get("why"), lang))})
        tl.append(("l%02d-title" % no, 0, clock))
        clock += SLIDE_SEC

        # what this lesson leaves behind — the file chain, which is the spine
        opens, saves = L.get("opens"), L.get("saves")
        objs = [pick(o, lang) for o in (L.get("objectives") or [])][:MAX_BULLETS]
        sid = "l%02d-goal" % no
        head = ("이 차시를 마치면 이렇게 됩니다" if lang == "ko"
                else "By the end of this lesson")
        chain = []
        if opens:
            chain.append(("%s 을 열고" if lang == "ko" else "open %s") % opens)
        if saves:
            chain.append(("%s 로 저장합니다" if lang == "ko" else "save as %s") % saves)
        scenes.append(content_slide(sid, "%s %d" % ("차시" if lang == "ko" else "Lesson", no),
                                    head, [shorten(o, BULLET_CHARS) for o in objs],
                                    "", None, clock, "%d. 목표" % no))
        frag = [round(clock + 1.5 + i * 1.2, 2) for i in range(len(objs))]
        slides.append({"sceneId": sid, "fragments": frag,
                       "notes": " · ".join(chain) or "—"})
        tl.append((sid, len(objs), clock))
        clock += SLIDE_SEC

        for si, sec in enumerate(L.get("sections", [])):
            if sec.get("kind") == "practice":
                continue
            d = section_slide(sec, lang)
            if not d["head"]:
                continue
            sid = "l%02d-s%02d" % (no, si)
            scenes.append(content_slide(sid, d["eyebrow"], d["head"], d["bullets"],
                                        d["notes"], d["figure"], clock,
                                        "%d. %s" % (no, d["eyebrow"])))
            frag = [round(clock + 1.5 + i * 1.2, 2) for i in range(len(d["bullets"]))]
            entry = {"sceneId": sid, "notes": d["notes"] or "—"}
            if frag:
                entry["fragments"] = frag
                tl.append((sid, len(d["bullets"]), clock))
            slides.append(entry)
            clock += SLIDE_SEC

        keys = [("%s — %s" % (k["key"], pick(k.get("when"), lang)))
                for k in (L.get("shortcuts") or [])][:MAX_BULLETS]
        if keys:
            sid = "l%02d-keys" % no
            head = ("오늘 친 것" if lang == "ko" else "What you typed today")
            scenes.append(content_slide(sid, "%s %d" % ("차시" if lang == "ko" else "Lesson", no),
                                        head, [shorten(k, BULLET_CHARS) for k in keys],
                                        "", None, clock, "%d. 명령" % no))
            slides.append({"sceneId": sid,
                           "notes": " · ".join(plain(k["key"]) for k in (L.get("shortcuts") or []))})
            tl.append((sid, len(keys), clock))
            clock += SLIDE_SEC

    return scenes, slides, tl, clock


def page(C, lessons, lang):
    scenes, slides, tl, total = build_lang(C, lessons, lang)
    island = json.dumps({"slides": slides, "slideSequences": []},
                        ensure_ascii=False, indent=1)

    tweens = []
    for sid, n, start in tl:
        var = "tl_" + sid.replace("-", "_")
        lines = ["var %s = gsap.timeline({paused:true});" % var,
                 "window.__timelines[%s] = %s;" % (json.dumps(sid), var),
                 "%s.from('#%s-h',{opacity:0,y:26,duration:0.55},%s);"
                 % (var, sid, round(start + 0.15, 2))]
        for i in range(n):
            lines.append("%s.from('#%s-b%d',{opacity:0,y:22,duration:0.45},%s);"
                         % (var, sid, i, round(start + 1.2 + i * 1.2, 2)))
        tweens.append(chr(10).join(lines))

    # A share build carries its own navigator. The real deck is driven by
    # `hyperframes present`, but a link someone opens has no player behind it,
    # and a deck that needs a server to be read is not a deck you can send.
    nav = ""
    if os.environ.get("DECK_STANDALONE") == "1":
        nav = io.open(os.path.join(HERE, "assets", "deck_nav.html"),
                      encoding="utf-8").read()

    title = pick(C.get("courseTitle"), lang)
    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<style>
@font-face{font-family:"LG EI Text TTF Regular";src:local("LG EI Text TTF Regular");font-weight:400}
@font-face{font-family:"LG EI Headline TTF Semibold";src:local("LG EI Headline TTF Semibold");font-weight:600}
@font-face{font-family:"Malgun Gothic";src:local("Malgun Gothic");font-weight:400}
@font-face{font-family:"Consolas";src:local("Consolas");font-weight:400}
*{box-sizing:border-box}
body{margin:0;background:%(ground)s}
.scene{position:relative;width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:%(ground)s;
  font-family:"LG EI Text TTF Regular","Malgun Gothic",system-ui,sans-serif;color:%(ink)s;
  word-break:keep-all;overflow-wrap:break-word}
.clip{position:absolute;inset:0}
.pad{position:absolute;inset:0;padding:96px 128px;display:flex;flex-direction:column;gap:28px}
.pad.split{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-content:start}
.cover{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;
  padding:0 160px;gap:24px}
.eyebrow{margin:0;font-size:34px;letter-spacing:.14em;text-transform:uppercase;color:%(accent)s;
  font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif}
h1{margin:0;font-size:104px;line-height:1.12;font-weight:600;
  font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;text-wrap:balance}
h2{margin:0;font-size:76px;line-height:1.22;font-weight:600;
  font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;text-wrap:balance}
.lede{margin:0;font-size:48px;line-height:1.5;color:%(dim)s}
.meta{margin:0;font-size:34px;color:%(dim)s;font-family:ui-monospace,Consolas,monospace}
.pts{margin:8px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:22px}
.pts li{font-size:48px;line-height:1.4;padding-left:44px;position:relative}
.pts li::before{content:"";position:absolute;left:0;top:.62em;width:22px;height:4px;background:%(accent)s}
.cmd{font-family:ui-monospace,Consolas,monospace;font-size:.9em;color:%(accent)s;
  background:%(panel)s;padding:.06em .3em;border-radius:4px}
b{color:#fff;font-weight:600}
.fig{display:flex;align-items:center;justify-content:center}
.fig svg{width:100%%;max-height:720px}
.dwg .outline{fill:none;stroke:%(ink)s;stroke-width:.55;stroke-linejoin:round;stroke-linecap:round}
.dwg .hidden{fill:none;stroke:%(dim)s;stroke-width:.3;stroke-dasharray:2.4 1.2;stroke-linecap:butt}
.dwg .center{fill:none;stroke:%(accent)s;stroke-width:.28;stroke-dasharray:6 1.2 1 1.2;stroke-linecap:butt}
.dwg .dim,.dwg .ext,.dwg .tangent{fill:none;stroke:%(dim)s;stroke-width:.26}
.dwg .arrow{fill:%(dim)s;stroke:none}
.dwg text{font-family:ui-monospace,Consolas,monospace;fill:%(dim)s}
.dwg .dimtext{font-size:3.4px}
.dwg .vl{font-size:4.4px;font-weight:600;fill:%(ink)s}
</style>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
</head>
<body>
<script type="application/hyperframes-slideshow+json">
%(island)s
</script>
%(scenes)s
<script>
window.__timelines = window.__timelines || {};
%(tweens)s
</script>
%(nav)s
</body>
</html>
""" % {"lang": lang, "title": esc(title), "ground": GROUND, "ink": INK, "dim": DIM, "nav": nav,
       "accent": ACCENT, "panel": PANEL, "island": island, "w": W, "h": H,
       "scenes": "\n".join(scenes), "tweens": "\n".join(tweens)}


WRAPPER = """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<title>%(title)s</title>
<style>html,body{margin:0;height:100%%;background:#0B0A0A}</style>
<script type="module" src="https://cdn.jsdelivr.net/npm/hyperframes-player/dist/index.js"></script>
</head>
<body>
<hyperframes-slideshow>
  <hyperframes-player src="composition/index.html"></hyperframes-player>
</hyperframes-slideshow>
</body>
</html>
"""


def main(outroot):
    cur = B._find(("design", "curriculum.json"), ("curriculum.json",))
    C = json.load(io.open(cur, encoding="utf-8"))
    lessons = []
    for n in range(1, 9):
        p = B._find(("content", "lesson-%02d.json" % n), ("lesson-%02d.json" % n,))
        if p:
            lessons.append(json.load(io.open(p, encoding="utf-8")))

    for lang, name in LANGS:
        cdir = os.path.join(outroot, lang, "composition")
        os.makedirs(cdir, exist_ok=True)
        doc = page(C, lessons, lang)
        io.open(os.path.join(cdir, "index.html"), "w",
                encoding="utf-8", newline="\n").write(doc)
        io.open(os.path.join(outroot, lang, "index.html"), "w",
                encoding="utf-8", newline="\n").write(
            WRAPPER % {"lang": lang, "title": esc(pick(C.get("courseTitle"), lang))})
        io.open(os.path.join(cdir, "meta.json"), "w",
                encoding="utf-8", newline="\n").write(
            json.dumps({"id": "edu-ib-02-deck-%s" % lang,
                        "name": pick(C.get("courseTitle"), lang)},
                       ensure_ascii=False, indent=1) + "\n")
        io.open(os.path.join(outroot, lang, "package.json"), "w",
                encoding="utf-8", newline="\n").write(json.dumps({
                    "name": "edu-ib-02-deck-%s" % lang, "private": True, "type": "module",
                    "scripts": {
                        "dev": "npx --yes hyperframes@0.7.111 present ./composition",
                        "studio": "npx --yes hyperframes@0.7.111 preview ./composition --background",
                        "check": "npx --yes hyperframes@0.7.111 check ./composition",
                        "lint": "npx --yes hyperframes@0.7.111 lint ./composition",
                    }}, ensure_ascii=False, indent=2) + "\n")
        n_slides = doc.count('data-composition-id=')
        size = len(doc.encode("utf-8"))
        print("%-8s 슬라이드 %3d · %7d B  %s" % (name, n_slides, size,
                                                os.path.join(outroot, lang)))
    return 0


if __name__ == "__main__":
    default = os.path.join(os.path.abspath(os.path.join(HERE, os.pardir, os.pardir)),
                           "docs", "autocad-technician", "deck")
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default))
