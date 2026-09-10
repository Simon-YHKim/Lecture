"""Place measured narration at its owning frame in the current delivery master.

The WAV already includes its opening silence. Audio starts at the frame start;
the extra hold at the end of a frame is not part of that WAV. Accumulating only
WAV lengths would make the voice arrive progressively earlier than the picture.
"""
import argparse
import html
import json
import math
from pathlib import Path
import re

import lesson_docs
import episodes
from narrate_tts import verify_script_hash, verify_tempo_timing


NARRATION = re.compile(
    r'\s*<audio\b(?=[^>]*\bsrc="assets/narration/)[^>]*>\s*</audio>', re.S)
ROOT_END = re.compile(r'\s*</div>(\s*<script>window\.__timelines)')


def attach(source, timing):
    rows = lesson_docs._SLOT.findall(source)
    if not rows:
        raise ValueError('No lesson frame slots were found')
    measured = {f['id']: f for f in timing['frames']}
    if len(measured) != len(timing['frames']):
        raise ValueError('Duplicate narration frame identifier')
    tags = []
    for comp, stem, start, duration in rows:
        if stem not in measured:
            raise ValueError('Missing recorded narration: ' + stem)
        f = measured[stem]
        start, duration, audio_duration = float(start), float(duration), float(f['duration'])
        if not all(math.isfinite(n) for n in (start, duration, audio_duration)):
            raise ValueError('Narration and frame times must be finite')
        if start < 0 or duration <= 0 or audio_duration <= 0 or audio_duration > duration + .002:
            raise ValueError('Narration does not fit its frame: ' + stem)
        name = f['audio']
        if Path(name).name != name or not re.fullmatch(r'[a-zA-Z0-9_-]+\.wav', name):
            raise ValueError('Invalid narration filename')
        tags.append('  <audio id="narration-%s" class="clip" data-role="narration" '
                    'src="assets/narration/%s" preload="metadata" data-start="%s" '
                    'data-duration="%s" data-track-index="2" data-has-audio="true"></audio>'
                    % (html.escape(comp, quote=True), name, format(start, '.3f').rstrip('0').rstrip('.'),
                       format(float(f['duration']), '.3f').rstrip('0').rstrip('.')))
    source = NARRATION.sub('', source)
    source, count = ROOT_END.subn(lambda m: '\n' + '\n'.join(tags) + '\n</div>' + m[1], source)
    if count != 1:
        raise ValueError('Expected one root timeline closing tag')
    return source


def sync(lesson_dir):
    root = Path(lesson_dir)
    timing = json.loads((root / 'narration-timing.json').read_text(encoding='utf-8'))
    verify_script_hash(root, timing)
    verify_tempo_timing(timing, required=episodes.is_unified(root.name))
    files = [root / 'index.html']
    if not episodes.is_unified(root.name):
        files += sorted((root / 'compositions/episodes').glob('ep*.html'))
    prepared = {}
    for path in files:
        source = path.read_text(encoding='utf-8')
        result = attach(source, timing)
        if result != source:
            prepared[path] = result
    for path, result in prepared.items():
        path.write_text(result, encoding='utf-8', newline='\n')
    return len(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('lesson', type=Path)
    args = ap.parse_args()
    print('Narration linked to %d compositions.' % sync(args.lesson))


if __name__ == '__main__':
    main()
