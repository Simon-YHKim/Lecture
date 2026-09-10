"""강의 프레임에서 번역할 글자를 뽑고, 영문으로 갈아 끼운다.

프레임의 GSAP 타임라인은 `.brand` · `h2` 처럼 **구조 선택자**를 쓴다. 단어를
감싼 `<span class="kw">` 는 한국어가 어절 중간에서 줄바꿈되지 않게 하려는 것이지
애니메이션 대상이 아니다. 그래서 문장을 통째로 갈아도 모션이 깨지지 않는다.

번역 단위는 **한 문장을 담은 가장 바깥 요소**다. 문장 안에 `<b>` 같은 강조가
섞여 있어도 한 단위로 본다 — 조각으로 쪼개 옮기면 영어 어순이 무너진다.
갈아 끼울 때는 글자를 찾아 바꾸지 않고 **파싱한 자리(오프셋)를 그대로 덮는다.**
`&nbsp;` 같은 엔티티나 따옴표 때문에 글자 찾기가 빗나가지 않는다.

    python scripts/part/frame_text.py <차시 디렉터리>          번역할 글자를 JSON 으로
    python scripts/part/frame_text.py <차시> --map en.json     빠진 번역만 센다
"""
import argparse
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

HANGUL = re.compile(r'[가-힣]')
KW = re.compile(r'<span class="kw">(.*?)</span>')
TAG = re.compile(r'<[^>]+>')
SCRIPTS = re.compile(r'<(script|style)\b.*?</\1>', re.S)
# 문장 안에 섞여도 문장을 쪼개지 않는 표시들.
INLINE = {'b', 'strong', 'em', 'i', 'span', 'br', 'small', 'sup', 'sub', 'code', 'a', 'u'}
SKIP = {'script', 'style', 'svg'}
# 닫는 태그가 없는 것들. 쌓아 두면 짝 맞추기가 어긋난다.
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'source', 'col',
        'area', 'base', 'embed', 'param', 'track', 'wbr'}


def plain(fragment):
    """마크업과 엔티티를 걷어낸 글자. 지도의 열쇠로 쓴다."""
    return re.sub(r'\s+', ' ', html.unescape(TAG.sub('', KW.sub(r'\1', fragment)))).strip()


class Units(HTMLParser):
    """한 문장을 담은 가장 바깥 요소의 안쪽 범위를 모은다."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        for line in source.splitlines(keepends=True):
            self.lines.append(self.lines[-1] + len(line))
        self.stack = []
        self.spans = []
        self.skip = 0

    def at(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if self.stack and tag not in INLINE:
            self.stack[-1]['block'] = True
        if tag in VOID:
            # 닫는 태그가 없다. 쌓아 두면 그 뒤의 짝 맞추기가 전부 어긋난다.
            return
        end = self.source.index('>', self.at()) + 1
        self.stack.append({'tag': tag, 'inner': end, 'block': False})

    def handle_startendtag(self, tag, attrs):
        if self.stack and tag not in INLINE:
            self.stack[-1]['block'] = True

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        while self.stack and self.stack[-1]['tag'] != tag:
            self.stack.pop()          # 닫히지 않은 태그는 버린다
        if not self.stack:
            return
        node = self.stack.pop()
        inner = self.source[node['inner']:self.at()]
        if self.skip or node['block'] or not HANGUL.search(inner):
            return
        text = plain(inner)
        if text:
            self.spans.append((node['inner'], self.at(), text))


def blank(match):
    """script·style 안쪽을 지우되 길이와 줄 수를 그대로 둔다.

    줄이 하나라도 사라지면 파서가 주는 (줄, 칸) 이 원본의 자리와 어긋나고,
    그때부터 잘라 내는 범위가 전부 엉뚱한 곳을 가리킨다.
    """
    return re.sub(r'[^\n]', ' ', match.group(0))


def units(source):
    """(시작, 끝, 열쇠) — 겹치지 않는 바깥쪽 단위만."""
    parser = Units(source)
    parser.feed(SCRIPTS.sub(blank, source))
    spans = sorted(parser.spans)
    out = []
    for start, end, text in spans:
        if out and start < out[-1][1]:
            continue
        out.append((start, end, text))
    return out


def runs(source):
    """이 프레임이 담은 번역 단위를 읽는 순서대로, 중복 없이."""
    return list(dict.fromkeys(text for _, _, text in units(source)))


def localise(source, english):
    """영문으로 갈아 끼운 HTML 과, 지도에 없던 글자 목록을 돌려준다."""
    out, missing = source, []
    for start, end, text in reversed(units(source)):
        replacement = english.get(text)
        if replacement is None:
            missing.append(text)
            continue
        out = out[:start] + replacement + out[end:]
    return out, list(reversed(missing))


def frames(lesson_dir):
    root = os.path.join(lesson_dir, 'compositions', 'frames')
    return [os.path.join(root, n) for n in sorted(os.listdir(root)) if n.endswith('.html')]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('lesson')
    ap.add_argument('--map', help='이미 번역한 {국문: 영문} JSON')
    a = ap.parse_args(argv)

    english = json.load(open(a.map, encoding='utf-8')) if a.map else {}
    seen, missing = [], []
    for path in frames(a.lesson):
        for text in runs(open(path, encoding='utf-8').read()):
            if text not in seen:
                seen.append(text)
            if text not in english and text not in missing:
                missing.append(text)
    if a.map:
        print('번역 단위 %d · 빠진 것 %d' % (len(seen), len(missing)))
        for text in missing[:60]:
            print('   ', text[:110])
        return 1 if missing else 0
    json.dump({text: '' for text in seen}, sys.stdout, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
