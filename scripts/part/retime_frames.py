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
        # 맞출 트윈이 없어도 길이는 바뀐다. 인사 화면과 녹화 프레임이 그렇다.
        s = ROOT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), head + tl, count=1)
        s = SECT_DUR.sub(lambda x: x.group(1) + ('%g' % dur) + x.group(4), s, count=1)
        if not dry and s != head + tl:
            io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
        if not dry:
            sync_motion(path, dur)
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
        sync_motion(path, dur)
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


def sync_motion(frame_path, dur):
    """`.motion.json` 의 duration 을 프레임과 같게 둔다.

    프레임 HTML 만 고치고 이 파일을 두면 검사기가 「motion.json 길이가 슬롯과
    다르다」로 잡는다. 같은 값을 두 곳에 적어 두는 구조라 한쪽만 고치면 반드시
    어긋난다 — 고치는 자리를 한 곳으로 모은다.
    """
    p = frame_path[:-5] + '.motion.json'
    if not os.path.exists(p):
        return
    doc = json.load(io.open(p, encoding='utf-8'))
    if abs(float(doc.get('duration', 0)) - dur) < 5e-4:
        return
    doc['duration'] = round(dur, 3)
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

    idx = io.open(os.path.join(lesson_dir, 'index.html'), encoding='utf-8').read()
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

    timing = json.load(io.open(os.path.join(a.lesson, 'narration-timing.json'),
                               encoding='utf-8'))
    idx_path = os.path.join(a.lesson, 'index.html')
    idx = io.open(idx_path, encoding='utf-8').read()
    slug = os.path.basename(os.path.normpath(a.lesson))
    planned = planned_spans(a.lesson, slug)

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
        src = '잼'
        if not bs and f['id'] in planned:
            bs, src = planned[f['id']], '대본'
        n, why = retime_frame(path, bs, spans[f['id']][1], a.dry)
        total += n
        print('   %-24s 박자 %2d(%s) · 시각 %2d개 %s'
              % (f['id'], len(bs), src, n, why))

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
