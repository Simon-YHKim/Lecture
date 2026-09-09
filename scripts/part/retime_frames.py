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
import os
import re
import sys

# tl.to("#l1f3 .tk1",{ … },9.34);  ―  마지막 인자가 시각이다
CALL = re.compile(
    r'(?P<head>tl\.(?P<kind>fromTo|to|from|set)\(")(?P<sel>[^"]+)"(?P<mid>.*?),\s*'
    r'(?P<time>-?\d+(?:\.\d+)?)\s*\);', re.S)
FAMILY = re.compile(r'#\w+\s+\.([a-zA-Z][\w-]*?)(\d+)\b')
ROOT_DUR = re.compile(r'(data-composition-id="(?P<cid>[^"]+)"[^>]*?data-duration=")(?P<d>[\d.]+)(")')
SECT_DUR = re.compile(r'(<section id="(?P<cid>[^"]+)"[^>]*?data-duration=")(?P<d>[\d.]+)(")')
SLOT = re.compile(
    r'(data-composition-src="compositions/frames/(?P<id>[^"]+)\.html"\s+data-start=")'
    r'(?P<s>[\d.]+)("\s+data-duration=")(?P<d>[\d.]+)(")')
MAIN_DUR = re.compile(r'(id="root"[^>]*?data-duration=")(?P<d>[\d.]+)(")')

TAIL = 1.6          # 말이 끝난 뒤 프레임이 더 서 있는 시간
LEAD = 0.9          # 첫 박자 전에 등장 연출을 끝내 둘 여유


def beats_of(timing, frame):
    f = [x for x in timing['frames'] if x['frame'] == frame][0]
    bs = [(b['observedStart'] - f['start'], b['observedEnd'] - f['start'])
          for b in timing['beats'] if b['frame'] == frame]
    bs.sort()
    return f, bs


def retime_frame(path, beats, dur, dry=False):
    """이 프레임의 tl.* 호출 시각을 새 박자에 맞춘다."""
    s = io.open(path, encoding='utf-8').read()
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

    newtime = {}
    for key, items in streams.items():
        if key.startswith('fam:'):
            seen = {}
            for idx, m in items:
                seen.setdefault(idx, []).append(m)
            keys = sorted(seen)
            groups = [sorted(seen[k], key=lambda x: float(x.group('time'))) for k in keys]
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

    order = streams          # 아래 홑 요소 처리가 쓰는 이름을 맞춰 둔다

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

    # 등장 연출(계열 전체를 한 번에 잡는 호출)과 퇴장을 양 끝으로 옮긴다.
    first_on = beats[0][0] if beats else 0.0
    for m in calls:
        sel = m.group('sel')
        if m.start() in newtime:
            continue
        if sel.count(',') >= 1 and FAMILY.search(sel):
            newtime[m.start()] = round(max(0.0, first_on - LEAD), 2)
        elif '.topline' in sel and '.body' in sel:
            newtime[m.start()] = round(max(0.0, dur - 1.05), 2)

    if not newtime:
        return 0, '맞출 것 없음'

    out, last, n = [], 0, 0
    for m in calls:
        if m.start() not in newtime:
            continue
        out.append(tl[last:m.start()])
        out.append('%s%s"%s,%s);' % (m.group('head'), m.group('sel'),
                                     m.group('mid'), newtime[m.start()]))
        last = m.end()
        n += 1
    out.append(tl[last:])
    s = head + ''.join(out)

    s = ROOT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
    s = SECT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
    if not dry:
        io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    return n, ''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args(argv)

    timing = json.load(io.open(os.path.join(a.lesson, 'narration-timing.json'),
                               encoding='utf-8'))
    idx_path = os.path.join(a.lesson, 'index.html')
    idx = io.open(idx_path, encoding='utf-8').read()

    spans, clock = {}, 0.0
    for f in timing['frames']:
        d = round(f['duration'] + TAIL, 3)
        spans[f['id']] = (round(clock, 3), d)
        clock += d

    total = 0
    for f in timing['frames']:
        path = os.path.join(a.lesson, 'compositions', 'frames', f['id'] + '.html')
        if not os.path.exists(path):
            print('   %-24s 파일 없음' % f['id'])
            continue
        _fr, bs = beats_of(timing, f['frame'])
        n, why = retime_frame(path, bs, spans[f['id']][1], a.dry)
        total += n
        print('   %-24s 박자 %2d · 시각 %2d개 %s' % (f['id'], len(bs), n, why))

    idx = SLOT.sub(lambda m: (m.group(1) + ('%g' % spans[m.group('id')][0]) + m.group(4)
                              + ('%g' % spans[m.group('id')][1]) + m.group(6))
                   if m.group('id') in spans else m.group(0), idx)
    idx = MAIN_DUR.sub(lambda m: m.group(1) + ('%g' % round(clock, 3)) + m.group(3), idx, count=1)
    if not a.dry:
        io.open(idx_path, 'w', encoding='utf-8', newline='\n').write(idx)
    print('   %s · 시각 %d개 · 전체 %.1f초' % (os.path.basename(a.lesson.rstrip('/\\')), total, clock))
    return 0


if __name__ == '__main__':
    sys.exit(main())
