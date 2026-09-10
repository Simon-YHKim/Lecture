"""Create a private, offline HyperFrames render project with measured audio.

Public sources keep relative media references. This command copies verified
WAVs into a fresh directory outside Git, where HyperFrames can resolve them.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

from lesson_docs import _SLOT
from narrate_tts import private_output, verify_script_hash, wav_seconds
from sync_narration import attach


GSAP_URL = re.compile(r'https://cdn\.jsdelivr\.net/npm/gsap@[\d.]+/dist/gsap\.min\.js')
EXTERNAL = re.compile(r'<(?:script|link|img|audio|video|iframe)\b[^>]*\b(?:src|href)=["\'](?:https?:)?//', re.I)


def motion_spec(lesson, index):
    """The CLI reads only a root sidecar, so lift frame deadlines to its clock."""
    assertions, duration = [], 0
    for _, stem, start, length in _SLOT.findall(index):
        start, length = float(start), float(length)
        duration = max(duration, start + length)
        sidecar = lesson / 'compositions' / 'frames' / (stem + '.motion.json')
        if not sidecar.is_file():
            raise ValueError('A frame has no motion specification: ' + stem)
        spec = json.loads(sidecar.read_text(encoding='utf-8'))
        if abs(spec['duration'] - length) > .002:
            raise ValueError('Motion duration differs from its frame: ' + stem)
        for original in spec['assertions']:
            assertion = dict(original)
            if assertion['kind'] == 'appearsBy':
                assertion['bySec'] = round(start + assertion['bySec'], 3)
            elif assertion['kind'] not in ('before', 'staysInFrame'):
                raise ValueError('Cannot lift this assertion to the lesson clock: ' + assertion['kind'])
            assertions.append(assertion)
    if not assertions:
        raise ValueError('No frame motion assertions found')
    return {'duration': round(duration, 3), 'assertions': assertions}


def prepare(lesson, output, gsap, preview=False):
    lesson, gsap = Path(lesson).resolve(), Path(gsap).resolve()
    output = private_output(output)
    if output.exists():
        raise ValueError('Choose a fresh output directory: ' + str(output))
    timing = json.loads((lesson / 'narration-timing.json').read_text(encoding='utf-8'))
    verify_script_hash(lesson, timing)
    if not timing.get('spokenTextSha256'):
        raise ValueError('Regenerate speech to record its script identity before exporting')
    media = json.loads((lesson / 'media.local.json').read_text(encoding='utf-8'))
    for playlist in [lesson / 'index.html', *sorted((lesson / 'compositions/episodes').glob('ep*.html'))]:
        source = playlist.read_text(encoding='utf-8')
        if attach(source, timing) != source:
            raise ValueError('Playlist narration is stale; refresh timing: ' + playlist.name)
    slots = _SLOT.findall((lesson / 'index.html').read_text(encoding='utf-8'))
    stems = [stem for _, stem, _, _ in slots]
    measured = [f['id'] for f in timing['frames']]
    if len(set(stems)) != len(stems) or stems != measured:
        raise ValueError('Narration frames must match the complete master playlist in order')
    wave_files = {}
    for f in timing['frames']:
        if not re.fullmatch(r'[a-zA-Z0-9_-]+\.wav', f['audio']):
            raise ValueError('Invalid narration filename')
        if f['audio'] in wave_files:
            raise ValueError('Duplicate narration filename')
        audio = private_output(media['frames'][f['id']])
        if not f.get('audioSha256') or hashlib.sha256(audio.read_bytes()).hexdigest() != f['audioSha256']:
            raise ValueError('WAV identity is missing or changed; regenerate speech: ' + f['id'])
        if abs(wav_seconds(audio) - float(f['duration'])) > .003:
            raise ValueError('WAV duration differs from measured timing: ' + f['id'])
        wave_files[f['audio']] = audio
    if 'gsap' not in gsap.read_text(encoding='utf-8') or gsap.stat().st_size < 10000:
        raise ValueError('A local GSAP distributable is required')
    files = [lesson / name for name in ['index.html', 'package.json', 'meta.json',
              'hyperframes.json', 'BRIEF.md', 'SCRIPT.md', 'narration-timing.json']
             if (lesson / name).is_file()]
    files += sorted((lesson / 'compositions').rglob('*.html'))
    files += sorted((lesson / 'compositions').rglob('*.motion.json'))
    prepared, hashes, missing_recordings = {}, {}, []
    for source in files:
        relative = source.relative_to(lesson)
        content = source.read_bytes()
        hashes[relative.as_posix()] = hashlib.sha256(content).hexdigest()
        if source.suffix == '.html':
            text = GSAP_URL.sub('assets/vendor/gsap.min.js', content.decode('utf-8'))
            if 'USER RECORDING' in text:
                missing_recordings.append(relative.as_posix())
            if EXTERNAL.search(text):
                raise ValueError('An external runtime dependency remains: ' + str(relative))
            content = text.encode('utf-8')
        prepared[relative] = content
    if missing_recordings and not preview:
        raise ValueError('AutoCAD recording is missing. Use --preview only for validation, not delivery.')
    prepared[Path('index.motion.json')] = (json.dumps(
        motion_spec(lesson, (lesson / 'index.html').read_text(encoding='utf-8')),
        indent=2) + '\n').encode('utf-8')
    # All source identities and audio durations are checked before any copy.
    output.mkdir(parents=True)
    for relative, content in prepared.items():
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
    (output / 'assets/narration').mkdir(parents=True)
    for name, source in wave_files.items():
        shutil.copyfile(source, output / 'assets/narration' / name)
    (output / 'assets/vendor').mkdir(parents=True)
    shutil.copyfile(gsap, output / 'assets/vendor/gsap.min.js')
    (output / 'source-manifest.json').write_text(json.dumps({
        'lesson': lesson.name, 'spokenTextSha256': timing['spokenTextSha256'],
        'sourceFiles': hashes, 'audioFrames': len(wave_files),
        'purpose': 'validation-preview' if preview else 'lecture',
        'missingRecordings': missing_recordings}, indent=2) + '\n', encoding='utf-8')
    return {'project': str(output), 'audioFrames': len(wave_files),
            'audioSeconds': timing['totalSeconds'], 'sourceFiles': len(files)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('lesson', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--gsap', required=True, type=Path)
    ap.add_argument('--preview', action='store_true', help='Allow recording placeholders for validation only')
    args = ap.parse_args()
    print(json.dumps(prepare(args.lesson, args.out, args.gsap, args.preview), ensure_ascii=False))


if __name__ == '__main__':
    main()
