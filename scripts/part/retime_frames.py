# -*- coding: utf-8 -*-
"""대본이 바뀐 프레임의 모션을 다시 잰 나레이션에 맞춘다.

프레임의 강조 시각은 대본의 박자에서 나온 값이다. 대본을 고치면 그 값이 옛
녹음을 가리킨 채 남는다. 1차시 3번 프레임이 그랬다 — 카드 2가 2.8초 만에
꺼지고 카드 3이 17초 뒤에야 켜져, 그 사이 아무것도 강조되지 않았다. 검수자가
「카드 애니메이션이 일관성 있게 적용되지 않았음」이라고 적은 자리다.

원인은 표식 없는 문단 하나였다. 그 문단이 어느 카드에도 속하지 않아 박자
사이에 구멍이 생겼다. 대본에서 그 대목을 정리하고 다시 합성하면 구멍이
사라지므로, 남은 일은 프레임의 시각을 새 박자에 다시 붙이는 것뿐이다.

붙이는 규칙은 하나다.

    i 번째 강조가 켜지는 시각 = i 번째 박자가 시작하는 시각
    꺼지는 시각              = 다음 박자가 시작하는 시각 (마지막은 그 박자의 끝)

그래서 강조는 말하는 동안 켜져 있고, 말이 넘어가면 같이 넘어간다. 사이가 비지
않는다. 등장 연출은 첫 박자 직전으로, 퇴장은 프레임 끝으로 옮긴다.

    python scripts/part/retime_frames.py <lesson-dir> [--dry]
"""
import argparse
import io
import json
import math
import os
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from narrate_tts import verify_script_hash, verify_tempo_timing, frame_hold
from lesson_edit import staged_edit

# tl.to("#l1f3 .tk1",{ … },9.34);  ―  마지막 인자가 시각이다
CALL = re.compile(
    r'(?P<head>tl\.(?P<kind>fromTo|to|from|set)\(")(?P<sel>[^"]+)"(?P<mid>[^;]*?),\s*'
    r'(?P<time>-?(?:\d+(?:\.\d*)?|\.\d+))\s*\);', re.S)
FAMILY = re.compile(r'#\w+\s+\.([a-zA-Z][\w-]*?)(\d+)\b')
ROOT_DUR = re.compile(r'(data-composition-id="(?P<cid>[^"]+)"[^>]*?data-duration=")(?P<d>[\d.]+)(")')
SECT_DUR = re.compile(r'(<section id="(?P<cid>[^"]+)"[^>]*?data-duration=")(?P<d>[\d.]+)(")')
SLOT = re.compile(
    r'(data-composition-src="compositions/frames/(?P<id>[^"]+)\.html"\s+data-start=")'
    r'(?P<s>[\d.]+)("\s+data-duration=")(?P<d>[\d.]+)(")')
MAIN_DUR = re.compile(r'(id="root"[^>]*?data-duration=")(?P<d>[\d.]+)(")')

TAIL = 1.6          # 말이 끝난 뒤 프레임이 더 서 있는 시간
LEAD = 0.9          # 첫 박자 전에 등장 연출을 끝내 둘 여유

_ROW_SELECTOR = re.compile(r'#(?P<scope>[\w-]+)\s+(?P<tag>[A-Za-z][\w-]*)?(?P<classes>(?:\.[\w-]+)*)\Z')
_ROW_OPACITY = re.compile(r'(\bopacity\s*:\s*)(0?\.34|0?\.64)(?![\d.])')
_ROW_CLEAR = re.compile(r'''(\bbackgroundColor\s*:\s*)(['"])rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*\)\2''')
_ROW_TINT = re.compile(r'''\bbackgroundColor\s*:\s*(['"])(?:#F5F5F3|#FFF|rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*\))\1''', re.I)
_ROW_SEED = re.compile(r'gsap\.set\(gsap\.utils\.toArray\([^\n]+; // row-readability-background\r?\n')
# 두 쪽짜리 명령표의 행. `#l4f8 .ky13` 처럼 생겼다.
_KEY_ROW = re.compile(r'#[\w-]+\s+\.ky\d+\Z')


class _RowTargets(HTMLParser):
    """Resolve only the scoped tag/class selectors emitted by our generators."""
    _VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
             'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__()
        self.stack, self.nodes = [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, set(attrs.get('class', '').split()),
                           {identity for _, identity in self.stack if identity}))
        if tag not in self._VOID:
            self.stack.append((tag, attrs.get('id')))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self._VOID:
            self.handle_endtag(tag)

    def matches(self, selector):
        match = _ROW_SELECTOR.fullmatch(selector.strip())
        if not match or not (match['tag'] or match['classes']):
            return None
        classes = set(re.findall(r'\.([\w-]+)', match['classes']))
        return [tag for tag, found, ancestors in self.nodes
                if match['scope'] in ancestors and classes <= found
                and (not match['tag'] or match['tag'].lower() == tag)]


def fix_row_readability(source):
    """Keep generated rows opaque on a white base without changing timing.

    A mixed selector retains its original tween and stagger. Its deterministic
    GSAP value function returns 1 only for TR targets, leaving every other
    target's old opacity intact. Unsupported selectors are left unchanged.
    """
    if '<tr' not in source.lower():
        return source
    source = _ROW_SEED.sub('', source)
    targets = _RowTargets(source)

    def row_tags(call):
        matched = [targets.matches(selector) for selector in call['sel'].split(',')]
        if any(tags is None or not tags for tags in matched):
            return []
        tags = [tag for group in matched for tag in group]
        return tags if 'tr' in tags else []

    tinted = [call for call in CALL.finditer(source)
              if (_ROW_TINT.search(call['mid']) or
                  "backgroundColor:(i,target)=>target.tagName==='TR'?'#FFF':" in call['mid'])
              and row_tags(call)]
    selectors = list(dict.fromkeys(selector.strip() for call in tinted
                                  for selector in call['sel'].split(',')))
    seed_at = tinted[0].start() if tinted else None
    # Transparent black is a poor interpolation endpoint on white tables.
    # Filter at runtime too: a shared class may also identify a card or a note.
    seed = ('gsap.set(gsap.utils.toArray(%s).filter(target=>target.tagName===\'TR\'),'
            '{backgroundColor:\'#FFF\'}); // row-readability-background\n'
            % json.dumps(','.join(selectors)))

    def fix(call):
        tags = row_tags(call)
        if not tags:
            return call.group(0)
        only_rows = all(tag == 'tr' for tag in tags)
        def opacity(match):
            value = '1' if only_rows else "(i,target)=>target.tagName==='TR'?1:" + match[2]
            return match[1] + value
        def background(match):
            value = "'#FFF'" if only_rows else "(i,target)=>target.tagName==='TR'?'#FFF':" + match[0][len(match[1]):]
            return match[1] + value
        mid = _ROW_OPACITY.sub(opacity, call['mid'])
        mid = _ROW_CLEAR.sub(background, mid)
        start, end = call.start('mid') - call.start(), call.end('mid') - call.start()
        prefix = seed if call.start() == seed_at else ''
        return prefix + call.group(0)[:start] + mid + call.group(0)[end:]

    return CALL.sub(fix, source)


def beats_of(timing, frame):
    f = [x for x in timing['frames'] if x['frame'] == frame][0]
    raw = [b for b in timing['beats'] if b['frame'] == frame]
    if len({b['beat'] for b in raw}) != len(raw):
        raise ValueError('Duplicate beat in frame: ' + f['id'])
    bs = [(float(b['observedStart']) - float(f['start']),
           float(b['observedEnd']) - float(f['start'])) for b in raw]
    bs.sort()
    validate_beats(bs, float(f['duration']))
    return f, bs


def validate_beats(spans, duration):
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Frame duration must be finite and positive')
    previous_end = 0
    for start, end in spans:
        if not all(math.isfinite(v) for v in (start, end)):
            raise ValueError('Beat times must be finite')
        if start < previous_end - .003 or end <= start or end > duration + .003:
            raise ValueError('Beats must be ordered, disjoint, and inside their frame')
        previous_end = end


def retime_frame(path, beats, dur, dry=False):
    """이 프레임의 tl.* 호출 시각을 새 박자에 맞춘다."""
    validate_beats(beats, dur)
    s = Path(path).read_text(encoding='utf-8')
    head = s[:s.index('const tl')] if 'const tl' in s else s
    if 'const tl' not in s:
        return 0, '타임라인 없음'
    tl = s[s.index('const tl'):]

    calls = list(CALL.finditer(tl))
    if not calls:
        return 0, '호출 없음'

    # 강조는 여러 갈래로 나란히 흐른다. 표의 행이 하나 밝아질 때 도면의 치수선도
    # 같이 밝아지는 식이다. 갈래마다 순서가 있으므로 갈래를 먼저 나누고, 갈래
    # 안에서 i 번째가 i 번째 박자를 받게 한다. 한 갈래만 다시 맞추면 나머지가
    # 옛 시각에 남아 표와 도면이 서로 다른 것을 가리킨다.
    def stream_of(sel):
        parts = [x.strip() for x in sel.split(',') if x.strip()]
        if not parts:
            return None
        fam = FAMILY.findall(parts[0])
        if len(parts) == 1 and len(fam) == 1:
            return 'fam:' + fam[0][0], int(fam[0][1])
        # 한 박자마다 치수선·치수값·강조겹선이 나란히 켜진다. 셋은 각각 제
        # 갈래로 세어야 한다. 하나로 묶으면 켜짐·꺼짐 짝이 어긋난다.
        if all('data-dim=' in x for x in parts):
            return ('dimtext' if all('text[' in x for x in parts) else 'dimline'), None
        if all('data-feature=' in x for x in parts):
            return 'feat', None
        return None

    streams = {}
    for m in calls:
        got = stream_of(m.group('sel'))
        if got:
            streams.setdefault(got[0], []).append((got[1], m))

    newtime, newmid = {}, {}
    for key, items in streams.items():
        if key.startswith('fam:'):
            seen = {}
            for idx, m in items:
                seen.setdefault(idx, []).append(m)
            keys = sorted(seen)
            groups = [seen[k] for k in keys]
        else:
            # 갈래 안에서는 켜짐·꺼짐이 번갈아 온다. 둘씩 묶는다.
            ms = [m for _i, m in items]
            groups = [ms[i:i + 2] for i in range(0, len(ms), 2)]
        if len(groups) not in (len(beats), len(beats) - 1):
            continue
        for k, ms in enumerate(groups):
            if k >= len(beats):
                break
            on, off = beats[k]
            nxt = beats[k + 1][0] if k + 1 < len(beats) else off
            for j, m in enumerate(ms):
                newtime[m.start()] = round(on if j == 0 else nxt, 2)
                if key in ('fam:sp', 'fam:wy'):
                    # Step captions share one physical slot: finish fading the
                    # old label before revealing the next, not on top of it.
                    if j:
                        newtime[m.start()] = round(max(on, nxt - .2), 2)
                    newmid[m.start()] = re.sub(r'duration:[\d.]+',
                        'duration:0.25' if j == 0 else 'duration:0.18', m.group('mid'))

    order = streams          # 아래 홑 요소 처리가 쓰는 이름을 맞춰 둔다

    explicit = re.search(r'// narration-beats: (\[[^\n]+\])', tl)
    if explicit:
        groups = json.loads(explicit.group(1))
        if len(groups) != len(beats):
            raise ValueError('Explicit scene beat mapping differs from measured narration')
        for index, selectors in enumerate(groups):
            on, off = beats[index]
            next_on = beats[index + 1][0] if index + 1 < len(beats) else off
            for selector in selectors:
                matched = [m for m in calls if m.group('sel') == selector]
                if not matched:
                    raise ValueError('A mapped beat has no animation: ' + selector)
                for j, m in enumerate(matched):
                    newtime[m.start()] = round(on if j == 0 else next_on, 2)

    for call in calls:
        tagged = re.match(r'[^\S\n]*// narration-beat: (\d+) (on|off)\b', tl[call.end():])
        if not tagged:
            continue
        index, phase = int(tagged[1]) - 1, tagged[2]
        if not 0 <= index < len(beats):
            raise ValueError('A drawing highlight names an absent narration beat')
        on, off = beats[index]
        if phase == 'off' and index + 1 < len(beats):
            off = beats[index + 1][0]
        newtime[call.start()] = round(on if phase == 'on' else off, 2)

    if 'USER RECORDING' in head:
        for m in calls:
            sel, mid = m.group('sel'), m.group('mid')
            if sel.endswith(' .strip'):
                newtime[m.start()] = float(m.group('time')) if m.group('kind') == 'fromTo' else round(dur - 1.05, 2)
                newmid[m.start()] = re.sub(r'y:-?[\d.]+', 'y:0', mid)
                if m.group('kind') == 'fromTo':
                    # Older retiming could merge two calls and turn the strip's
                    # target opacity into zero. Restore the visible entry state.
                    newmid[m.start()] = re.sub(r'(\},\{opacity:)\d+(?:\.\d+)?',
                                               r'\g<1>1', newmid[m.start()])
            elif sel.endswith(' .tag') and m.group('kind') == 'to':
                newtime[m.start()] = round(dur - 1.4, 2)
            elif sel.endswith(' .prog'):
                newtime[m.start()] = float(m.group('time'))
                newmid[m.start()] = re.sub(r'duration:[\d.]+',
                    'duration:%g' % max(.1, dur - float(m.group('time')) - 1.05), mid)

    # 계열이 박자보다 하나 적으면 마지막 박자를 받을 홑 요소를 찾는다.
    covered = max((len(set(i for i, _ in v)) for k, v in order.items()
                   if k.startswith('fam:')), default=0)
    if beats and 0 < covered == len(beats) - 1:
        solo = {}
        for m in calls:
            sel = m.group('sel')
            if m.start() in newtime or ',' in sel or '.topline' in sel:
                continue
            if FAMILY.search(sel):
                continue
            solo.setdefault(sel, []).append(m)
        if solo:
            sel = list(solo)[-1]
            on, off = beats[-1]
            for j, m in enumerate(sorted(solo[sel], key=lambda x: float(x.group('time')))):
                newtime[m.start()] = round(on if j == 0 else off, 2)

    # 계열 이름이 번호로 끝나지 않는 프레임이 있다. 2분할 마무리의 `.p-done` ·
    # `.p-next`, 도면틀 조립의 `.sh-paper` · `.sh-frame` … 이 그렇다. 계열로는
    # 하나도 안 잡혀서 박자가 통째로 비었다 — 검수에서 「다음을 눌러도 안 변한다」
    # 로 올라온 자리다.
    #
    # 마지막 수단으로 **등장 순서**를 쓴다. 항목은 대본이 말하는 차례대로 뜨므로,
    # 셀렉터를 지금 시각 순으로 줄 세워 박자에 하나씩 붙이면 그 뜻이 그대로 산다.
    if beats and len(_covered_beats(newtime, beats)) < len(beats):
        first_by_sel = {}
        for m in calls:
            sel = m.group('sel')
            if '.topline' in sel or m.start() in newtime:
                continue
            first_by_sel.setdefault(sel, []).append(m)
        order_sel = sorted(first_by_sel,
                           key=lambda s: min(float(x.group('time')) for x in first_by_sel[s]))
        # 계열 전체를 한 번에 잡는 등장 연출(쉼표가 있고 번호 계열)은 항목이 아니다.
        order_sel = [s for s in order_sel
                     if not (s.count(',') >= 1 and FAMILY.search(s))]
        # 한 항목이 두 셀렉터로 나뉘어 있는 경우가 있다 — 2분할 마무리의 `.p-done`
        # (칸)과 `.p-done-li`(그 안의 줄)가 그렇다. 클래스 이름이 앞뒤로 걸리면
        # 같은 항목으로 묶는다. 안 묶으면 항목 수가 박자 수의 두 배가 된다.
        groups, taken = [], set()
        for s in order_sel:
            if s in taken:
                continue
            cls = _cls(s)
            mates = [t for t in order_sel
                     if t not in taken and (_cls(t) == cls or _cls(t).startswith(cls + '-'))]
            for t in mates:
                taken.add(t)
            groups.append(mates)
        # 한 박자에서 도형과 그 옆 라벨이 함께 뜨는 자리가 있다 — 용지선과
        # 「A3 420 × 297」, 도면선과 「사방 10」이 그렇다. 이름은 남남이지만
        # 지금 시각이 붙어 있으면 같은 박자의 식구다. 안 묶으면 항목이 박자보다
        # 많아져 순서 맞추기가 통째로 포기된다.
        def _t0(mates):
            return min(float(x.group('time')) for s in mates for x in first_by_sel[s])

        groups.sort(key=_t0)
        merged = []
        for g in groups:
            if merged and _t0(g) - _t0(merged[-1]) < 1.5:
                merged[-1] = merged[-1] + g
            else:
                merged.append(list(g))
        if len(merged) == len(beats):
            groups = merged

        if len(groups) == len(beats):
            for k, mates in enumerate(groups):
                on, off = beats[k]
                nxt = beats[k + 1][0] if k + 1 < len(beats) else off
                ms = sorted((m for s in mates for m in first_by_sel[s]),
                            key=lambda x: float(x.group('time')))
                base = float(ms[0].group('time'))
                for m in ms:
                    # 같은 항목 안에서 처음 뜨는 것들은 함께 켜고, 뒤늦은 것은 물러난다.
                    same = abs(float(m.group('time')) - base) < 1.5
                    newtime[m.start()] = round(on if same else nxt, 2)

    # Recap bullets share one measured paragraph per panel. A stale, evenly
    # spaced stagger can reveal the last bullet after the next paragraph has
    # started. Show the whole list with its panel until item timings exist.
    recap_lists = ('p-done-li', 'p-next-li')
    if len(beats) == 2 and all(any(
            m.group('kind') == 'fromTo' and m.group('sel').endswith(' .' + name)
            for m in calls) for name in recap_lists):
        for name, (on, _off) in zip(recap_lists, beats):
            panel = name.removesuffix('-li')
            for m in calls:
                if m.group('kind') != 'fromTo':
                    continue
                if m.group('sel').endswith((' .' + panel, ' .' + name)):
                    newtime[m.start()] = round(on, 2)
                    newmid[m.start()] = re.sub(r'stagger:[\d.]+', 'stagger:0',
                                              newmid.get(m.start(), m.group('mid')))

    title_exit = next((m for m in calls if m.group('kind') == 'to'
        and all(name in m.group('sel') for name in (' .brand', ' .cert', ' .sub'))), None)
    if title_exit:
        fade_at = round(max(0.0, dur - 1.05), 2)
        newtime[title_exit.start()] = fade_at
        for m in calls:
            if m.group('kind') != 'fromTo' or not m.group('sel').endswith(
                    (' .brand', ' .cert', ' h2', ' .rule', ' .sub')):
                continue
            duration = re.search(r'duration:([\d.]+)', m.group('mid'))
            if duration:
                # Short titles need the subtitle before the outro, with time
                # to read it. Keep the established rhythm when it already fits.
                latest = max(0.0, fade_at - float(duration[1]) - 2.0)
                newtime[m.start()] = round(min(float(m.group('time')), latest), 2)

    # 등장 연출(계열 전체를 한 번에 잡는 호출)과 퇴장을 양 끝으로 옮긴다.
    first_on = beats[0][0] if beats else 0.0
    for m in calls:
        sel = m.group('sel')
        if m.start() in newtime:
            continue
        if sel.count(',') >= 1 and FAMILY.search(sel):
            # An overview can intentionally be visible during the spoken
            # introduction. Do not postpone it until the first item is named.
            newtime[m.start()] = round(min(float(m.group('time')),
                                          max(0.0, first_on - LEAD)), 2)
        elif '.topline' in sel and '.body' in sel:
            newtime[m.start()] = round(max(0.0, dur - 1.05), 2)

    if not newtime:
        # 맞출 트윈이 없어도 길이는 바뀐다. 인사 화면과 녹화 프레임이 그렇다.
        s = ROOT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), head + tl, count=1)
        s = SECT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
        s = fix_row_readability(s)
        if not dry and s != head + tl:
            Path(path).write_text(s, encoding='utf-8', newline='\n')
        if not dry:
            sync_motion(path, dur)
        return 0, '맞출 것 없음'

    out, last, n = [], 0, 0
    for m in calls:
        if m.start() not in newtime:
            continue
        out.append(tl[last:m.start()])
        out.append('%s%s"%s,%s);' % (m.group('head'), m.group('sel'),
                                     newmid.get(m.start(), m.group('mid')), newtime[m.start()]))
        last = m.end()
        n += 1
    out.append(tl[last:])
    s = head + ''.join(out)

    s = ROOT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
    s = SECT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
    s = fix_row_readability(s)
    if not dry:
        Path(path).write_text(s, encoding='utf-8', newline='\n')
        sync_motion(path, dur, beats)
    return n, ''


def _cls(sel):
    """`#l3f7 .p-done-li` → `p-done-li`. 없으면 셀렉터 자체를 이름으로 쓴다."""
    m = re.search(r'\.([A-Za-z][\w-]*)\s*$', sel.strip())
    return m.group(1) if m else sel.strip()


def _covered_beats(newtime, beats):
    """새로 잡은 시각이 실제로 덮은 박자 번호."""
    got = set()
    for t in newtime.values():
        for k, (on, _off) in enumerate(beats):
            if abs(t - on) < 0.05:
                got.add(k)
    return got


def sync_motion(frame_path, dur, beats=None):
    """`.motion.json` 의 duration 을 프레임과 같게 둔다.

    프레임 HTML 만 고치고 이 파일을 두면 검사기가 「motion.json 길이가 슬롯과
    다르다」로 잡는다. 같은 값을 두 곳에 적어 두는 구조라 한쪽만 고치면 반드시
    어긋난다 — 고치는 자리를 한 곳으로 모은다.
    """
    p = frame_path[:-5] + '.motion.json'
    if not os.path.exists(p):
        return
    doc = json.loads(Path(p).read_text(encoding='utf-8'))
    original = json.dumps(doc, sort_keys=True)
    doc['duration'] = round(dur, 3)
    source = Path(frame_path).read_text(encoding='utf-8')
    first_calls = {}
    for call in CALL.finditer(source):
        first_calls.setdefault(call.group('sel'), call)
    title = any(call['kind'] == 'to' and all(name in call['sel'] for name in
                (' .brand', ' .cert', ' .sub')) for call in CALL.finditer(source))
    if title:
        for assertion in doc['assertions']:
            call = first_calls.get(assertion.get('selector'))
            if assertion['kind'] != 'appearsBy' or not call or call['kind'] != 'fromTo':
                continue
            if not call['sel'].endswith((' .brand', ' .cert', ' h2', ' .rule', ' .sub')):
                continue
            fade = re.search(r'duration:([\d.]+)', call['mid'])
            if fade:
                assertion['bySec'] = round(float(call['time']) + float(fade[1]) + .15, 3)
    if beats:
        for a in doc['assertions']:
            if a['kind'] != 'appearsBy':
                continue
            call = first_calls.get(a['selector'])
            if call and call.group('kind') == 'fromTo' and call.group('mid').lstrip().startswith(',{opacity:0'):
                at = float(call.group('time'))
                if any(abs(at - start) < .05 for start, _ in beats):
                    # An entrance tied to measured speech can move later when
                    # the script grows. Keep the deadline tied to that beat.
                    a['bySec'] = round(at + 2.4, 3)
    if beats:
        # 두 쪽짜리 명령표(24개)의 행 조건은 만든 쪽에서 「그 행이 켜지는 박자
        # + 3초」로 적힌다. 그런데 행의 등장 트윈은 스물넉 줄을 한 선택자에 묶어
        # 부르므로 바로 위의 규칙이 `#l4f8 .ky13` 을 못 찾는다. 그래서 시각을 다시
        # 맞춰도 조건만 옛 값으로 남았고, 4차시 영문판에서 13·14행이 「나타나야 할
        # 때보다 6초 늦게 나타남」으로 잡혔다. 대신 그 행을 켜는 tl.to 를 본다.
        # 뒤쪽 쪽으로 넘어가는 시점도 13번 박자라 두 쪽 모두 이 값이 맞다.
        for a in doc['assertions']:
            if a['kind'] != 'appearsBy' or not _KEY_ROW.match(a.get('selector', '')):
                continue
            call = first_calls.get(a['selector'])
            if call and call.group('kind') == 'to' and 'opacity:1' in call.group('mid'):
                a['bySec'] = round(float(call.group('time')) + 3, 2)
    explicit = re.search(r'// narration-beats: (\[[^\n]+\])', source)
    if explicit and beats:
        groups = json.loads(explicit.group(1))
        for a in doc['assertions']:
            if a['kind'] != 'appearsBy':
                continue
            for i, selectors in enumerate(groups):
                # A motion condition may name one SVG member of a group that
                # animates together (e.g. the title-block rectangle and text).
                if any(a['selector'] == sel or a['selector'] == sel.replace(' .', ' g.') for sel in selectors):
                    a['bySec'] = round(beats[i][0] + 2.4, 3)
    if beats and len(beats) == 2:
        recap = [next((sel for sel in first_calls if sel.endswith(' .' + name)), None)
                 for name in ('p-done-li', 'p-next-li')]
        if all(recap):
            for selector, (on, _off) in zip(recap, beats):
                # Checking only the panel misses bullets delayed past the clip.
                last = selector + ':last-child'
                assertion = next((a for a in doc['assertions']
                    if a['kind'] == 'appearsBy' and a['selector'] == last), None)
                if assertion is None:
                    assertion = {'kind': 'appearsBy', 'selector': last}
                    doc['assertions'].append(assertion)
                assertion['bySec'] = round(on + 2.4, 3)
    if json.dumps(doc, sort_keys=True) == original:
        return
    with io.open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')


def planned_spans(lesson_dir, slug):
    """대본에서 계산한 박자 — 잰 박자가 없는 프레임(녹화)이 쓰는 답.

    `narrate_tts` 는 `(N …)` 표식이 붙은 문단만 비트로 적는다. 녹화 프레임은
    단계를 `### N단계` 로 쓰므로 잰 비트가 하나도 없고, 그러면 이 스크립트가
    그 프레임을 건너뛰어 단계 띠가 옛 시각에 남는다. 실제로 2차시 녹화 프레임의
    9~16단계가 그렇게 어긋나 있었다.

    검사기(`verify_course`)가 그 프레임을 판정할 때 쓰는 것과 **같은 계산**을
    여기서도 한다. 다른 계산을 쓰면 고쳐도 검사기는 계속 틀렸다고 말한다.

    돌려주는 것: {stem: [(on, off), ...]} — 프레임 시작을 0으로 잰 값.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import beats as B
    import episodes as E

    sp = os.path.join(lesson_dir, 'SCRIPT.md')
    if not os.path.isfile(sp):
        return {}
    script = B.parse_script(sp)
    steps = B.parse_steps(sp, 5) or B.parse_steps(sp, 8)
    demo_line = 5 if B.parse_steps(sp, 5) else 8
    if steps:
        script[demo_line] = list(steps)
    try:
        cuts = E.cuts_for(slug)
    except SystemExit:
        cuts = []

    demo_total = None
    if steps:
        demo_total = int(round(sum(B.read_seconds(t) for _, t in steps)
                               * B.DEMO_FACTOR / 10.0)) * 10

    expect = []
    for line_no in sorted(script):
        if steps and line_no == demo_line and cuts:
            sl = B.split_steps(steps, cuts)
            lens = B.split_lengths(
                demo_total, [sum(B.read_seconds(t) for _, t in x[1]) for x in sl])
            for segs, dur in zip([x[1] for x in sl], lens):
                expect.append((line_no, segs, dur))
        else:
            expect.append((line_no, script[line_no], None))

    idx = (Path(lesson_dir) / 'index.html').read_text(encoding='utf-8')
    stems = re.findall(r'data-composition-src="compositions/frames/([^"]+)\.html"', idx)
    if len(stems) != len(expect):
        return {}

    out = {}
    for stem, (line_no, segs, part_sec) in zip(stems, expect):
        fixed = part_sec
        if fixed is None:
            fixed = 12 if line_no == 1 else None
            if steps and line_no == demo_line:
                fixed = demo_total
        spans, _ = B.plan(segs, duration=fixed)
        bs = [(a, b) for _i, a, b in B.beat_spans(spans)]
        if bs:
            out[stem] = bs
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args(argv)

    if a.dry:
        return retime_lesson(a.lesson, dry=True)
    return staged_edit(a.lesson, lambda root: retime_lesson(str(root)))


def retime_lesson(lesson, dry=False):

    timing = json.loads((Path(lesson) / 'narration-timing.json').read_text(encoding='utf-8'))
    verify_script_hash(lesson, timing)
    import episodes
    verify_tempo_timing(timing, required=episodes.is_unified(Path(lesson).name))
    idx_path = os.path.join(lesson, 'index.html')
    idx = Path(idx_path).read_text(encoding='utf-8')
    slug = os.path.basename(os.path.normpath(lesson))
    planned = planned_spans(lesson, slug)

    spans, clock = {}, 0.0
    hold = frame_hold(timing)
    for f in timing['frames']:
        d = round(f['duration'] + hold, 3)
        spans[f['id']] = (round(clock, 3), d)
        clock += d

    total = 0
    for f in timing['frames']:
        path = os.path.join(lesson, 'compositions', 'frames', f['id'] + '.html')
        if not os.path.exists(path):
            raise ValueError('Frame is missing: ' + f['id'])
        _fr, bs = beats_of(timing, f['frame'])
        src = '잼'
        if not bs and f['id'] in planned:
            bs, src = planned[f['id']], '대본'
        n, why = retime_frame(path, bs, spans[f['id']][1], dry)
        total += n
        print('   %-24s 박자 %2d(%s) · 시각 %2d개 %s'
              % (f['id'], len(bs), src, n, why))

    idx = SLOT.sub(lambda m: (m.group(1) + format(spans[m.group('id')][0], '.3f') + m.group(4)
                              + format(spans[m.group('id')][1], '.3f') + m.group(6))
                   if m.group('id') in spans else m.group(0), idx)
    idx = MAIN_DUR.sub(lambda m: m.group(1) + format(clock, '.3f') + m.group(3), idx, count=1)
    if not dry:
        Path(idx_path).write_text(idx, encoding='utf-8', newline='\n')
        from refresh_lesson import refresh_inplace
        refresh_inplace(lesson)
    print('   %s · 시각 %d개 · 전체 %.1f초' % (os.path.basename(lesson.rstrip('/\\')), total, clock))
    return 0


if __name__ == '__main__':
    sys.exit(main())
