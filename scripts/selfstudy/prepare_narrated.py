"""Prepare eight offline self-study decks and their private narration plans.

The source lecture scripts remain unchanged. Run once per language with
SELFSTUDY_LANG set to that language. All outputs belong in private storage.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_deck_selfstudy as deck

ISLAND = re.compile(r'(<script type="application/hyperframes-slideshow\+json">)(.*?)(</script>)', re.S)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes((json.dumps(data, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))


def manifest_of(source):
    match = ISLAND.search(source)
    if not match:
        raise ValueError('Missing slideshow manifest')
    return json.loads(match[2])


def replace_manifest(source, manifest):
    body = json.dumps(manifest, ensure_ascii=False, indent=1).replace('<', '\\u003c')
    return ISLAND.sub(lambda m: m[1] + '\n' + body + '\n' + m[3], source, count=1)


def standalone(source, manifest, gsap, script):
    lib = '<script>' + Path(gsap).read_text(encoding='utf-8').replace('</script>', '<\\/script>') + '</script>'
    source, count = re.subn(r'<script src="https://cdn.jsdelivr.net/[^\"]+"></script>', lambda _: lib, source, count=1)
    if count != 1:
        raise ValueError('Expected one GSAP dependency')
    manifest['reviewId'] = hashlib.sha256(json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    manifest['lessons'][0]['script'] = script
    source = replace_manifest(source, manifest)
    panel = (HERE / 'assets/deck_full_script.html').read_text(encoding='utf-8')
    source = source.replace('</body>', panel + '\n</body>')
    if re.search(r'<(?:script|link)[^>]+(?:src|href)="https?://', source):
        raise ValueError('Offline deck still has a network dependency')
    return source


def prepare(stage, captions, out, gsap, lang):
    if deck.LANG != lang:
        raise ValueError('Set SELFSTUDY_LANG to match --lang before starting Python')
    rows = []
    for source_path in sorted((HERE / 'source').glob('lesson-*.json')):
        lesson = read_json(source_path)
        slug, number = lesson['slug'], lesson['no']
        folder = stage / slug
        raw = out / 'raw' / lang / ('L%02d.html' % number)
        deck.main(str(folder), str(source_path), str(raw))
        source = raw.read_text(encoding='utf-8')
        manifest = manifest_of(source)
        timing = read_json(folder / 'narration-timing.json')
        media = read_json(folder / 'media.local.json')
        prior = read_json(captions / lang / ('AutoCAD_%s_L%02d_REVIEW.json' % (lang.upper(), number)))
        frame_clock = 0.0
        frames = {}
        for frame in timing['frames']:
            frames[frame['id']] = dict(frame, videoStart=frame_clock)
            frame_clock += frame['duration'] + timing['frameHoldSeconds']
        for slide in manifest['slides']:
            frame_id = slide.get('sourceFrame')
            if frame_id:
                frame = frames[frame_id]
                cues = [dict(c, start=round(c['start']-frame['videoStart'], 3),
                             end=round(c['end']-frame['videoStart'], 3))
                        for c in prior['cues'] if c['frame'] == frame_id]
                if not cues:
                    raise ValueError('No approved narration for ' + frame_id)
                slide['notes'] = ' '.join(c['text'] for c in cues)
                slide['audio'] = {'mode': 'reuse', 'path': media['frames'][frame_id],
                                  'sha256': frame['audioSha256'], 'duration': frame['duration'],
                                  'cues': cues}
            else:
                slide['audio'] = {'mode': 'generate'}
        manifest.update(language=lang, lesson=number, slug=slug,
                        lessons=[{'no': number, 'title': lesson['title'][lang], 'at': 1,
                                  'count': len(manifest['slides'])}],
                        delivery='self-study-slides-with-matching-narration')
        plan = out / 'plans' / lang / ('L%02d.json' % number)
        write_json(plan, manifest)
        rows.append({'lang': lang, 'lesson': number, 'slug': slug, 'raw': str(raw),
                     'plan': str(plan), 'source': str(source_path), 'gsap': str(gsap),
                     'slides': len(manifest['slides']),
                     'newNarrations': sum(s['audio']['mode']=='generate' for s in manifest['slides'])})
    write_json(out / ('projects-%s.json' % lang), rows)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage', type=Path, required=True)
    ap.add_argument('--captions', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--gsap', type=Path, required=True)
    ap.add_argument('--lang', choices=['ko', 'en'], required=True)
    a = ap.parse_args()
    rows = prepare(a.stage, a.captions, a.out, a.gsap, a.lang)
    print(json.dumps({'lang':a.lang, 'lessons':len(rows), 'slides':sum(r['slides'] for r in rows),
                      'newNarrations':sum(r['newNarrations'] for r in rows)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
