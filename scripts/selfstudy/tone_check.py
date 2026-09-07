# -*- coding: utf-8 -*-
"""Measure the 합쇼체 / 해요체 mix of the Korean prose inside a self-study lesson JSON.

Target set by the requester: 합쇼체 70-80%, 해요체 20-30%.

A "sentence" is any Korean clause that ends in a verb ending. Labels, table cells
that are bare nouns, command tokens and coordinates carry no ending and are
excluded rather than counted as violations.
"""
import io, json, re, sys, os

# 합쇼체 — 모든 '…니다 / …니까' 종결. 조합형이라 '만듭니다·세웁니다'처럼 받침이 달라도 '니다'로 끝난다.
HAP = re.compile(r'(니다|니까|십시오|합시다|십시다)$')
# 해요체 — '…요 / …죠' 종결.
HAE = re.compile(r'[가-힣](요|죠)$')
# 문어체 — 합쇼체가 아니면서 '다'로 끝나는 종결. LESSON_STYLE 24번이 금지한다.
MUNEO = re.compile(r'[가-힣]다$')

SPLIT = re.compile(r'(?<=[.!?])\s+|\n+')
STRIP_TAIL = re.compile(r'["\'\)\]\}»”’\s.!?…]+$')


def sentences(text):
    for raw in SPLIT.split(text):
        s = raw.strip()
        if not s:
            continue
        core = STRIP_TAIL.sub('', s)
        if not core:
            continue
        if not re.search(r'[가-힣]', core):
            continue
        yield s, core


def classify(core):
    if HAP.search(core):
        return 'hap'
    if HAE.search(core):
        return 'hae'
    if MUNEO.search(core):
        return 'muneo'
    return 'other'


def walk(node, out, path=''):
    """Collect every Korean prose string reachable under a 'ko' key."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == 'ko' and isinstance(v, str):
                out.append((path + '/ko', v))
            elif k == 'svg':
                continue
            else:
                walk(v, out, f'{path}/{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, out, f'{path}[{i}]')


def report(path, verbose=False):
    with io.open(path, encoding='utf-8') as f:
        data = json.load(f)
    fields = []
    walk(data, fields)
    counts = {'hap': 0, 'hae': 0, 'muneo': 0, 'other': 0}
    muneo_hits, hae_hits = [], []
    for fpath, text in fields:
        for s, core in sentences(text):
            kind = classify(core)
            counts[kind] += 1
            if kind == 'muneo':
                muneo_hits.append((fpath, s))
            elif kind == 'hae':
                hae_hits.append((fpath, s))
    graded = counts['hap'] + counts['hae']
    hap_pct = 100.0 * counts['hap'] / graded if graded else 0.0
    hae_pct = 100.0 * counts['hae'] / graded if graded else 0.0
    verdict = 'PASS' if (70.0 <= hap_pct <= 80.0 and 20.0 <= hae_pct <= 30.0) else 'FAIL'
    if counts['muneo']:
        verdict = 'FAIL'
    print(f"{os.path.basename(path)}  {verdict}")
    print(f"  종결 문장 {graded}개 · 합쇼체 {counts['hap']} ({hap_pct:.1f}%) · 해요체 {counts['hae']} ({hae_pct:.1f}%)")
    print(f"  문어체(금지) {counts['muneo']} · 종결 없음(레이블·명령·좌표) {counts['other']}")
    if counts['muneo']:
        for fpath, s in muneo_hits[:12]:
            print(f"    문어체 {fpath}: {s[:70]}")
    if verbose:
        for fpath, s in hae_hits[:40]:
            print(f"    해요체 {fpath}: {s[:70]}")
    return verdict == 'PASS', hap_pct, hae_pct, counts


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    verbose = '-v' in sys.argv
    allok = True
    for p in args:
        ok, *_ = report(p, verbose)
        allok = allok and ok
        print()
    sys.exit(0 if allok else 1)
