"""Create a private, offline HyperFrames render project with measured audio.

Public sources keep relative media references. This command copies verified
WAVs into a fresh directory outside Git, where HyperFrames can resolve them.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import shutil

from lesson_docs import _SLOT
from narrate_tts import private_output, verify_script_hash, wav_seconds
from sync_narration import attach


GSAP_URL = re.compile(r'https://cdn\.jsdelivr\.net/npm/gsap@[\d.]+/dist/gsap\.min\.js')
EXTERNAL = re.compile(r'<(?:script|link|img|audio|video|iframe)\b[^>]*\b(?:src|href)=["\'](?:https?:)?//', re.I)
EPISODE = re.compile(r'ep[1-9][0-9]*')
FRAME_SOURCE = re.compile(r'compositions/frames/([a-zA-Z0-9_-]+)\.html')


class CompositionTags(HTMLParser):
    """Collect real references, including attributes the canonical regex skips."""
    def __init__(self, source):
        super().__init__()
        self.refs, self.roots, self.audio = [], [], []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'data-composition-src' in values or values.get('id') == 'root' or tag == 'audio':
            if len(values) != len(attrs):
                raise ValueError('Duplicate attributes in a timeline element')
        if 'data-composition-src' in values:
            self.refs.append(values)
        if values.get('id') == 'root':
            self.roots.append(values)
        if tag == 'audio':
            self.audio.append(values)


def local_file(lesson, relative, folder=None):
    path = lesson / relative
    boundary = lesson / folder if folder else lesson
    if not path.resolve().is_relative_to(boundary.resolve()) or not path.resolve().is_relative_to(lesson):
        raise ValueError('Source path leaves its lesson directory: ' + str(relative))
    if not path.is_file():
        raise ValueError('Required source file is missing: ' + str(relative))
    return path


def episode_slots(source):
    tags = CompositionTags(source)
    rows = _SLOT.findall(source)
    if not rows or len(rows) != len(tags.refs):
        raise ValueError('Every composition reference must be a canonical measured frame slot')
    if len({r[0] for r in rows}) != len(rows) or len({r[1].casefold() for r in rows}) != len(rows):
        raise ValueError('Duplicate episode composition or frame')
    for attrs, (comp, stem, start, length) in zip(tags.refs, rows):
        match = FRAME_SOURCE.fullmatch(attrs['data-composition-src'] or '')
        if not match or match[1] != stem or attrs.get('data-composition-id') != comp:
            raise ValueError('Invalid episode frame reference')
        if attrs.get('data-start') != start or attrs.get('data-duration') != length:
            raise ValueError('Episode slot attributes differ from the canonical timeline')
    # attach() verifies values and freshness; this additionally excludes audio
    # outside its generated narration tags, which would otherwise stay behind.
    if len(tags.audio) != len(rows) or any(a.get('data-role') != 'narration' for a in tags.audio):
        raise ValueError('Episode audio must belong one-to-one to its measured frames')
    return rows, tags


def selected_entry(lesson, episode, playlists, master):
    """Prove the episode partition before selecting any files for export."""
    entry = local_file(lesson, 'compositions/episodes/' + episode + '.html', 'compositions/episodes')
    episode_paths = [p for p in playlists if p != lesson / 'index.html']
    if any(not EPISODE.fullmatch(p.stem) for p in episode_paths):
        raise ValueError('Invalid canonical episode filename')
    episode_paths.sort(key=lambda p: int(p.stem[2:]))
    if [p.stem for p in episode_paths] != ['ep%d' % i for i in range(1, len(episode_paths) + 1)]:
        raise ValueError('The episode sequence has a missing entry')
    canonical = {stem: (comp, float(length)) for comp, stem, _, length in master}
    partition, selected = [], None
    for path in episode_paths:
        local_file(lesson, path.relative_to(lesson), 'compositions/episodes')
        rows, tags = episode_slots(playlists[path])
        end = 0.0
        for comp, stem, start, length in rows:
            start, length = float(start), float(length)
            if stem not in canonical or canonical[stem][0] != comp or abs(canonical[stem][1] - length) > .002:
                raise ValueError('Episode frame differs from the measured master: ' + stem)
            if not all(math.isfinite(n) for n in (start, length)) or length <= 0 or abs(start - end) > .002:
                raise ValueError('Episode slots must fill a continuous local clock from zero')
            end = start + length
        if len(tags.roots) != 1:
            raise ValueError('Expected one episode root timeline')
        root = tags.roots[0]
        root_start, root_duration = float(root.get('data-start', 'nan')), float(root.get('data-duration', 'nan'))
        if not math.isfinite(root_duration) or root_start != 0 or abs(root_duration - end) > .002:
            raise ValueError('Episode root duration differs from its frame slots')
        partition.extend(stem for _, stem, _, _ in rows)
        if path == entry:
            selected = rows
    if partition != [stem for _, stem, _, _ in master]:
        raise ValueError('Episodes must cover the complete master exactly once in order')
    if selected is None:
        raise ValueError('Selected episode is not in the canonical playlist set')
    return entry, selected


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
        if not math.isfinite(spec['duration']) or abs(spec['duration'] - length) > .002:
            raise ValueError('Motion duration differs from its frame: ' + stem)
        for original in spec['assertions']:
            assertion = dict(original)
            if assertion['kind'] == 'appearsBy':
                if not math.isfinite(assertion['bySec']) or not 0 <= assertion['bySec'] <= length:
                    raise ValueError('Motion deadline is outside its frame: ' + stem)
                assertion['bySec'] = round(start + assertion['bySec'], 3)
            elif assertion['kind'] not in ('before', 'staysInFrame'):
                raise ValueError('Cannot lift this assertion to the lesson clock: ' + assertion['kind'])
            assertions.append(assertion)
    if not assertions:
        raise ValueError('No frame motion assertions found')
    return {'duration': round(duration, 3), 'assertions': assertions}


def prepare(lesson, output, gsap, preview=False, episode=None):
    if episode is not None and (not isinstance(episode, str) or not EPISODE.fullmatch(episode)):
        raise ValueError('Episode must have the form ep1, ep2, ...')
    lesson, gsap = Path(lesson).resolve(), Path(gsap).resolve()
    output = private_output(output)
    if output.exists():
        raise ValueError('Choose a fresh output directory: ' + str(output))
    timing = json.loads((lesson / 'narration-timing.json').read_text(encoding='utf-8'))
    verify_script_hash(lesson, timing)
    if not timing.get('spokenTextSha256'):
        raise ValueError('Regenerate speech to record its script identity before exporting')
    media = json.loads((lesson / 'media.local.json').read_text(encoding='utf-8'))
    playlists = {}
    for playlist in [lesson / 'index.html', *sorted((lesson / 'compositions/episodes').glob('ep*.html'))]:
        source = playlist.read_text(encoding='utf-8')
        if attach(source, timing) != source:
            raise ValueError('Playlist narration is stale; refresh timing: ' + playlist.name)
        playlists[playlist] = source
    entry = lesson / 'index.html'
    slots = _SLOT.findall(playlists[entry])
    stems = [stem for _, stem, _, _ in slots]
    measured = [f['id'] for f in timing['frames']]
    if len({stem.casefold() for stem in stems}) != len(stems) or stems != measured:
        raise ValueError('Narration frames must match the complete master playlist in order')
    if episode is not None:
        episode_slots(playlists[entry])
        entry, slots = selected_entry(lesson, episode, playlists, slots)
    selected_ids = [stem for _, stem, _, _ in slots]
    wave_files, wave_names = {}, set()
    for f in timing['frames']:
        if not re.fullmatch(r'[a-zA-Z0-9_-]+\.wav', f['audio']):
            raise ValueError('Invalid narration filename')
        if f['audio'].casefold() in wave_names:
            raise ValueError('Duplicate narration filename')
        wave_names.add(f['audio'].casefold())
        audio = private_output(media['frames'][f['id']])
        if not f.get('audioSha256') or hashlib.sha256(audio.read_bytes()).hexdigest() != f['audioSha256']:
            raise ValueError('WAV identity is missing or changed; regenerate speech: ' + f['id'])
        if abs(wav_seconds(audio) - float(f['duration'])) > .003:
            raise ValueError('WAV duration differs from measured timing: ' + f['id'])
        wave_files[f['audio']] = audio
    if 'gsap' not in gsap.read_text(encoding='utf-8') or gsap.stat().st_size < 10000:
        raise ValueError('A local GSAP distributable is required')
    files = [lesson / name for name in ['package.json', 'meta.json',
              'hyperframes.json', 'BRIEF.md', 'SCRIPT.md', 'narration-timing.json']
             if (lesson / name).is_file()]
    files.insert(0, entry)
    if episode is None:
        files += sorted((lesson / 'compositions').rglob('*.html'))
        files += sorted((lesson / 'compositions').rglob('*.motion.json'))
    else:
        for stem in selected_ids:
            files += [local_file(lesson, 'compositions/frames/' + stem + suffix, 'compositions/frames')
                      for suffix in ('.html', '.motion.json')]
    prepared, hashes, missing_recordings = {}, {}, []
    for source in files:
        relative = source.relative_to(lesson)
        content = source.read_bytes()
        hashes[relative.as_posix()] = hashlib.sha256(content).hexdigest()
        if source.suffix == '.html':
            text = GSAP_URL.sub('assets/vendor/gsap.min.js', content.decode('utf-8'))
            if episode is not None and source != entry:
                tags = CompositionTags(text)
                if tags.refs or tags.audio:
                    raise ValueError('Nested frame or audio references require an explicit export plan: ' + str(relative))
            if 'USER RECORDING' in text:
                missing_recordings.append(relative.as_posix())
            if EXTERNAL.search(text):
                raise ValueError('An external runtime dependency remains: ' + str(relative))
            content = text.encode('utf-8')
        prepared[Path('index.html') if source == entry else relative] = content
    if missing_recordings and not preview:
        raise ValueError('AutoCAD recording is missing. Use --preview only for validation, not delivery.')
    motion = motion_spec(lesson, playlists[entry])
    prepared[Path('index.motion.json')] = (json.dumps(motion, indent=2) + '\n').encode('utf-8')
    selected_frames = [f for f in timing['frames'] if f['id'] in selected_ids]
    audio_sources = {f['audio']: {'frame': f['id'], 'sha256': f['audioSha256'], 'duration': f['duration']}
                     for f in selected_frames}
    wave_files = {name: source for name, source in wave_files.items() if name in audio_sources}
    audio_seconds = round(sum(float(f['duration']) for f in selected_frames), 3) if episode else timing['totalSeconds']
    manifest = {
        'lesson': lesson.name, 'spokenTextSha256': timing['spokenTextSha256'],
        'entrySource': entry.relative_to(lesson).as_posix(), 'episode': episode,
        'sourceFiles': hashes, 'audioFrames': len(wave_files),
        'audioFrameIds': selected_ids, 'audioSources': audio_sources,
        'audioSeconds': audio_seconds, 'duration': motion['duration'],
        'validationSources': {p.relative_to(lesson).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [*playlists, lesson / 'media.local.json']},
        'gsapSha256': hashlib.sha256(gsap.read_bytes()).hexdigest(),
        'purpose': 'validation-preview' if preview else 'lecture',
        'missingRecordings': missing_recordings}
    prepared[Path('source-manifest.json')] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
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
    return {'project': str(output), 'audioFrames': len(wave_files),
            'audioSeconds': audio_seconds, 'duration': motion['duration'], 'sourceFiles': len(files)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('lesson', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--gsap', required=True, type=Path)
    ap.add_argument('--preview', action='store_true', help='Allow recording placeholders for validation only')
    ap.add_argument('--episode', help='Export one canonical episode, for example ep1 or ep3')
    args = ap.parse_args()
    print(json.dumps(prepare(args.lesson, args.out, args.gsap, args.preview, args.episode), ensure_ascii=False))


if __name__ == '__main__':
    main()
