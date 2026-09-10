"""Prepare private scene checks without the CLI's long-lesson sampling aliasing.

HyperFrames 0.8.33 caps motion sampling at 300 points. Scene-local checks keep
the original deadlines. For a long recording, a separate opening-window check
verifies entrance assertions while the full-duration check retains all bounds
assertions. This does not change any authored scene or its animation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from lesson_docs import _SLOT
from narrate_tts import private_output


def scopes(spec):
    assertions = spec['assertions']
    deadlines = [a['bySec'] for a in assertions if a['kind'] == 'appearsBy']
    if not deadlines or spec['duration'] / 299 <= min(deadlines) / 2:
        return [('full', spec['duration'], assertions)]
    entrance = [a for a in assertions if a['kind'] != 'staysInFrame']
    bounds = [a for a in assertions if a['kind'] == 'staysInFrame']
    if any(a['kind'] not in ('appearsBy', 'before', 'staysInFrame') for a in assertions):
        raise ValueError('Unsupported motion assertion')
    # Every before selector must also have an explicit entrance deadline;
    # otherwise a short window cannot establish the intended ordering.
    named = {a['selector'] for a in entrance if a['kind'] == 'appearsBy'}
    for a in entrance:
        if a['kind'] == 'before' and not {a['a'], a['b']} <= named:
            return [('full', spec['duration'], assertions)]
    window = min(spec['duration'], max(10, max(deadlines) + 2))
    result = [('entrance', window, entrance + bounds)]
    # Full scene runtime/layout/contrast must still be checked even if it has
    # no bounds assertion. Existing sources all have at least one assertion.
    if not bounds:
        return [('full', spec['duration'], assertions)]
    result.append(('full', spec['duration'], bounds))
    return result


def prepare(project, out, scenes=None):
    project, out = Path(project).resolve(), private_output(out)
    if out.exists():
        raise ValueError('Choose a fresh scene-check directory')
    index = (project / 'index.html').read_text(encoding='utf-8')
    slots = _SLOT.findall(index)
    if not slots:
        raise ValueError('No source scenes found')
    if scenes:
        if not set(scenes) <= {stem for _, stem, _, _ in slots}:
            raise ValueError('A requested scene is absent from the master playlist')
        slots = [slot for slot in slots if slot[1] in scenes]
    jobs = []
    for cid, stem, start, duration in slots:
        source = project / 'compositions/frames' / (stem + '.html')
        spec = json.loads(source.with_suffix('.motion.json').read_text(encoding='utf-8'))
        if abs(spec['duration'] - float(duration)) > .002:
            raise ValueError('Scene duration mismatch: ' + stem)
        variants = scopes(spec)
        combined = [a for _, _, assertions in variants for a in assertions]
        key = lambda a: json.dumps(a, sort_keys=True)
        if set(map(key, combined)) != set(map(key, spec['assertions'])):
            raise ValueError('Scene checks must retain every original assertion unchanged')
        for scope, length, assertions in variants:
            dest = out / (stem + '-' + scope)
            (dest / 'compositions/frames').mkdir(parents=True)
            (dest / 'assets/vendor').mkdir(parents=True)
            shutil.copyfile(source, dest / 'compositions/frames' / source.name)
            shutil.copyfile(project / 'assets/vendor/gsap.min.js', dest / 'assets/vendor/gsap.min.js')
            html = '''<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<script src="assets/vendor/gsap.min.js"></script><style>
*{box-sizing:border-box;margin:0;padding:0}html,body,#root{width:1920px;height:1080px;overflow:hidden}
#root{position:relative}#root>[data-composition-src]{position:absolute;inset:0}
</style></head><body><div id="root" data-composition-id="main" data-start="0"
data-duration="%s" data-width="1920" data-height="1080">
<div id="scene-under-check" class="clip" data-composition-id="%s" data-composition-src="compositions/frames/%s.html"
data-start="0" data-duration="%s" data-track-index="1" data-width="1920" data-height="1080"></div>
</div><script>window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true});</script></body></html>
''' % (length, cid, stem, length)
            (dest / 'index.html').write_text(html, encoding='utf-8')
            (dest / 'index.motion.json').write_text(json.dumps(
                {'duration': length, 'assertions': assertions}, indent=2), encoding='utf-8')
            jobs.append({'project': dest.as_posix(), 'scene': stem, 'scope': scope,
                         'checkedSeconds': length, 'originalSeconds': float(duration),
                         'masterStart': float(start), 'assertions': len(assertions),
                         'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    (out / 'manifest.json').write_text(json.dumps(jobs, indent=2), encoding='utf-8')
    return jobs


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--scene', action='append', help='Limit a regression check to these scene stems')
    args = ap.parse_args()
    jobs = prepare(args.project, args.out, args.scene)
    print(json.dumps({'checks': len(jobs), 'assertions': sum(j['assertions'] for j in jobs)}))
