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
import tempfile

import ingest_recording as recordings
import episodes
from lesson_docs import _SLOT
from narrate_tts import frame_hold, private_output, verify_script_hash, verify_tempo_timing, wav_seconds
from sync_narration import attach


GSAP_URL = re.compile(r'https://cdn\.jsdelivr\.net/npm/gsap@[\d.]+/dist/gsap\.min\.js')
EXTERNAL = re.compile(r'<(?:script|link|img|audio|video|iframe)\b[^>]*\b(?:src|href)=["\'](?:https?:)?//', re.I)
EPISODE = re.compile(r'ep[1-9][0-9]*')
FRAME_SOURCE = re.compile(r'compositions/frames/([a-zA-Z0-9_-]+)\.html')
RECORDING = re.compile(r'<div class="rec"><div class="recmark">USER RECORDING</div>'
                       r'<div class="recsub">(DEMO-01[A-H]?)\b[^<]*</div></div>')


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


def unified_master_slots(source, timing):
    """Validate the whole lesson clock against its measured audio and hold."""
    rows, tags = episode_slots(source)
    if len(rows) != len(timing['frames']) or len(tags.roots) != 1:
        raise ValueError('Unified master needs one root and every measured narration frame')
    clock, hold = 0.0, frame_hold(timing)
    for index, ((_, stem, start, length), frame) in enumerate(zip(rows, timing['frames'])):
        start, length = float(start), float(length)
        expected_length = round(frame['duration'] + hold, 3)
        if (stem != frame['id'] or not all(math.isfinite(n) for n in (start, length))
                or length <= 0 or (index == 0 and start != 0)
                or abs(start - clock) > .002 or abs(length - expected_length) > .002):
            raise ValueError('Unified master slots must be continuous from zero with measured narration and hold')
        clock += expected_length
    root = tags.roots[0]
    root_start = float(root.get('data-start', 'nan'))
    root_duration = float(root.get('data-duration', 'nan'))
    if root_start != 0 or not math.isfinite(root_duration) or abs(root_duration - clock) > .002:
        raise ValueError('Unified master root must end with its complete measured frame sequence')
    return rows


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


def recording_parts(lesson, media):
    path = lesson / 'recording.json'
    if not path.is_file():
        if any(str(key).startswith('DEMO-') for key in media):
            raise ValueError('Recording bindings have no recording metadata')
        return {}, None
    original = path.read_bytes()
    doc = json.loads(original)
    parts = doc.get('parts', [])
    expected = recordings.recording_ids(lesson.name)
    if (doc.get('schemaVersion') != 2 or doc.get('lesson') != lesson.name
            or not isinstance(parts, list) or any(not isinstance(p, dict) for p in parts)
            or [p.get('demoId') for p in parts] != expected):
        raise ValueError('Recording parts must match the complete canonical recording plan')
    for part in parts:
        duration, fps = part.get('durationSec'), part.get('fps')
        if (not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0
                or not isinstance(fps, (int, float)) or not math.isfinite(fps) or not 1 <= fps <= 120
                or not re.fullmatch(r'[0-9a-f]{64}', part.get('sha256', ''))
                or not isinstance(media.get(part['demoId']), str)):
            raise ValueError('Recording metadata needs complete durations, identities and local bindings; register again')
    total = doc.get('durationSec')
    if not isinstance(total, (int, float)) or not math.isfinite(total) or abs(total - sum(p['durationSec'] for p in parts)) > .003:
        raise ValueError('Recording total duration differs from its parts')
    return {p['demoId']: p for p in parts}, original


def connect_recording(text, comp, length, part, media, used):
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', comp):
        raise ValueError('Recording composition ID is not a safe HTML identifier')
    matches = list(RECORDING.finditer(text))
    if len(matches) != 1 or text.count('USER RECORDING') != 1:
        raise ValueError('Recording placeholder does not match the authored frame')
    wrappers = list(re.finditer(r'<section\b[^>]*>', text))
    if len(wrappers) != 1 or wrappers[0].end() > matches[0].start():
        raise ValueError('Recording needs one authored full-frame section')
    wrapper = wrappers[0]
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', wrapper[0]))
    if float(attrs.get('data-start', 'nan')) != 0 or abs(float(attrs.get('data-duration', 'nan')) - length) > .002 or not math.isfinite(float(attrs.get('data-duration', 'nan'))):
        raise ValueError('Recording section must cover the complete measured frame from zero')
    demo_id = matches[0][1]
    if demo_id not in part or demo_id in used:
        raise ValueError('A recording must match exactly one canonical frame')
    spec = part[demo_id]
    source = recordings.recording_file(media[demo_id])
    if recordings.file_sha256(source) != spec['sha256']:
        raise ValueError('Recording identity changed; register again: ' + demo_id)
    info = recordings.probe(source)
    for key in ('durationSec', 'fps', 'width', 'height', 'codec', 'pixelFormat'):
        if spec.get(key) != info[key]:
            raise ValueError('Recording metadata differs from the actual stream: ' + demo_id)
    tolerance = 1 / info['fps'] + .003
    if abs(info['durationSec'] - length) > tolerance:
        raise ValueError('Recording duration must match its measured slot within one source frame; '
                         'no automatic trim or speed change: ' + demo_id)
    if recordings.file_sha256(source) != spec['sha256']:
        raise ValueError('Recording changed during validation: ' + demo_id)
    relative = 'assets/recordings/' + demo_id + '.mp4'
    # HyperFrames requires a timed video and rejects a plain timed ancestor.
    # This section covers the whole scene, so its composition retains exactly
    # the same visibility window when the redundant section start is removed.
    text = text[:wrapper.start()] + re.sub(r'\sdata-start="[^"]*"', '', wrapper[0]) + text[wrapper.end():]
    match = RECORDING.search(text)
    video = ('<div class="rec"><video id="%s-recording" class="clip" src="%s" '
             'data-start="0" data-duration="%s" data-media-start="0" data-volume="0" muted playsinline '
             'style="position:absolute;inset:0;width:1920px;height:1080px;object-fit:contain">'
             '</video></div>') % (comp, relative, format(length, '.3f').rstrip('0').rstrip('.'))
    used[demo_id] = {'path': source, 'relative': relative, 'sha256': spec['sha256'], **info}
    return text[:match.start()] + video + text[match.end():]


def prepare(lesson, output, gsap, preview=False, episode=None):
    unified = episodes.is_unified(Path(lesson).name)
    if unified and episode is not None:
        raise ValueError('Current delivery exports the whole lesson; episode selection is retired')
    if episode is not None and (not isinstance(episode, str) or not EPISODE.fullmatch(episode)):
        raise ValueError('Episode must have the form ep1, ep2, ...')
    lesson, gsap = Path(lesson).resolve(), Path(gsap).resolve()
    output = private_output(output)
    if output.exists():
        raise ValueError('Choose a fresh output directory: ' + str(output))
    timing_original = (lesson / 'narration-timing.json').read_bytes()
    script_original = (lesson / 'SCRIPT.md').read_bytes()
    timing = json.loads(timing_original)
    verify_script_hash(lesson, timing)
    verify_tempo_timing(timing, required=unified)
    if not timing.get('spokenTextSha256'):
        raise ValueError('Regenerate speech to record its script identity before exporting')
    media_original = (lesson / 'media.local.json').read_bytes()
    media = json.loads(media_original)
    playlists, playlist_originals = {}, {}
    active_playlists = [lesson / 'index.html']
    if not unified:
        active_playlists += sorted((lesson / 'compositions/episodes').glob('ep*.html'))
    for playlist in active_playlists:
        original = playlist.read_bytes()
        # Match read_text's universal-newline behavior while hashing raw bytes.
        source = original.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
        if attach(source, timing) != source:
            raise ValueError('Playlist narration is stale; refresh timing: ' + playlist.name)
        playlists[playlist] = source
        playlist_originals[playlist] = original
    entry = lesson / 'index.html'
    slots = _SLOT.findall(playlists[entry])
    stems = [stem for _, stem, _, _ in slots]
    measured = [f['id'] for f in timing['frames']]
    if len({stem.casefold() for stem in stems}) != len(stems) or stems != measured:
        raise ValueError('Narration frames must match the complete master playlist in order')
    if unified:
        slots = unified_master_slots(playlists[entry], timing)
    if episode is not None:
        episode_slots(playlists[entry])
        entry, slots = selected_entry(lesson, episode, playlists, slots)
    selected_ids = [stem for _, stem, _, _ in slots]
    wave_files, wave_names, source_wave_files = {}, set(), {}
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
        if 'tempo' in timing:
            if not re.fullmatch(r'[a-zA-Z0-9_-]+\.wav', f.get('sourceAudio', '')):
                raise ValueError('Invalid source narration filename')
            source_audio = private_output(media.get('sourceFrames', {}).get(f['id'], ''))
            if (not source_audio.is_file() or recordings.file_sha256(source_audio) != f['sourceAudioSha256']
                    or abs(wav_seconds(source_audio) - f['sourceDuration']) > .003):
                raise ValueError('Rate 0 source narration identity or duration changed: ' + f['id'])
            source_wave_files[source_audio] = f['sourceAudioSha256']
        wave_files[f['audio']] = audio
    if 'gsap' not in gsap.read_text(encoding='utf-8') or gsap.stat().st_size < 10000:
        raise ValueError('A local GSAP distributable is required')
    files = [lesson / name for name in ['package.json', 'meta.json',
              'hyperframes.json', 'BRIEF.md', 'SCRIPT.md', 'narration-timing.json']
             if (lesson / name).is_file()]
    files.insert(0, entry)
    if episode is None and not unified:
        files += sorted((lesson / 'compositions').rglob('*.html'))
        files += sorted((lesson / 'compositions').rglob('*.motion.json'))
    else:
        for stem in selected_ids:
            files += [local_file(lesson, 'compositions/frames/' + stem + suffix, 'compositions/frames')
                      for suffix in ('.html', '.motion.json')]
    prepared, hashes, missing_recordings = {}, {}, []
    recording_specs, recording_original, used_recordings = None, None, {}
    selected_slots = {stem: (comp, float(length)) for comp, stem, _, length in slots}
    canonical_recordings = recordings.recording_frames(lesson.name)
    for source in files:
        relative = source.relative_to(lesson)
        content = source.read_bytes()
        hashes[relative.as_posix()] = hashlib.sha256(content).hexdigest()
        if source.suffix == '.html':
            text = GSAP_URL.sub('assets/vendor/gsap.min.js', content.decode('utf-8'))
            if relative.parent == Path('compositions/frames') and source.stem in canonical_recordings:
                matches = RECORDING.findall(text)
                if matches != [canonical_recordings[source.stem]]:
                    raise ValueError('Canonical recording placeholder is missing or has the wrong part ID')
            if (episode is not None or unified) and source != entry:
                tags = CompositionTags(text)
                if tags.refs or tags.audio:
                    raise ValueError('Nested frame or audio references require an explicit export plan: ' + str(relative))
            if 'USER RECORDING' in text:
                if recording_specs is None:
                    recording_specs, recording_original = recording_parts(lesson, media)
                if recording_specs:
                    if source.stem not in selected_slots or relative.parent != Path('compositions/frames'):
                        raise ValueError('Recording placeholder must belong to a selected canonical frame')
                    comp, length = selected_slots[source.stem]
                    text = connect_recording(text, comp, length, recording_specs, media, used_recordings)
                    used_recordings[RECORDING.search(content.decode('utf-8'))[1]]['frame'] = source.stem
                else:
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
        'deliveryMode': 'lesson' if unified else 'legacy-episodes',
        'narrationTempo': timing.get('tempo', 1.0), 'narrationRate': timing.get('rate'),
        'narrationTimingSha256': timing.get('timingSha256'),
        'entrySource': entry.relative_to(lesson).as_posix(), 'episode': episode,
        'sourceFiles': hashes, 'audioFrames': len(wave_files),
        'audioFrameIds': selected_ids, 'audioSources': audio_sources,
        'audioSeconds': audio_seconds, 'duration': motion['duration'],
        'validationSources': {p.relative_to(lesson).as_posix(): hashlib.sha256(original).hexdigest()
                               for p, original in {**playlist_originals,
                                   lesson / 'media.local.json': media_original,
                                   lesson / 'narration-timing.json': timing_original,
                                   lesson / 'SCRIPT.md': script_original}.items()},
        'gsapSha256': hashlib.sha256(gsap.read_bytes()).hexdigest(),
        'purpose': 'validation-preview' if preview else 'lecture',
        'missingRecordings': missing_recordings,
        'recordingSources': {key: {field: value for field, value in spec.items() if field != 'path'}
                             for key, spec in used_recordings.items()}}
    if recording_original is not None:
        manifest['validationSources']['recording.json'] = hashlib.sha256(recording_original).hexdigest()
    for relative in hashes.keys() & manifest['validationSources'].keys():
        if hashes[relative] != manifest['validationSources'][relative]:
            raise ValueError('Source changed after validation: ' + relative)
    prepared[Path('source-manifest.json')] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    # All source identities and audio durations are checked before any copy.
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.lecture-', dir=output.parent) as temp:
        stage = Path(temp) / 'project'
        for relative, content in prepared.items():
            dest = stage / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
        (stage / 'assets/narration').mkdir(parents=True)
        for name, source in wave_files.items():
            dest = stage / 'assets/narration' / name
            shutil.copyfile(source, dest)
            if recordings.file_sha256(dest) != audio_sources[name]['sha256']:
                raise ValueError('Narration changed during export: ' + name)
        for spec in used_recordings.values():
            dest = stage / spec['relative']
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(spec['path'], dest)
            if recordings.file_sha256(dest) != spec['sha256'] or recordings.file_sha256(spec['path']) != spec['sha256']:
                raise ValueError('Recording changed during export')
        (stage / 'assets/vendor').mkdir(parents=True)
        shutil.copyfile(gsap, stage / 'assets/vendor/gsap.min.js')
        if recordings.file_sha256(stage / 'assets/vendor/gsap.min.js') != manifest['gsapSha256']:
            raise ValueError('GSAP changed during export')
        if (lesson / 'media.local.json').read_bytes() != media_original:
            raise ValueError('Media bindings changed during export')
        for relative, identity in {**hashes, **manifest['validationSources']}.items():
            if recordings.file_sha256(lesson / relative) != identity:
                raise ValueError('Source changed during export: ' + relative)
        for source, identity in source_wave_files.items():
            if recordings.file_sha256(source) != identity:
                raise ValueError('Rate 0 source narration changed during export')
        if output.exists():
            raise ValueError('Output appeared during export; choose a fresh directory')
        stage.rename(output)
    return {'project': str(output), 'audioFrames': len(wave_files),
            'audioSeconds': audio_seconds, 'duration': motion['duration'], 'sourceFiles': len(files),
            'recordings': len(used_recordings)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('lesson', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--gsap', required=True, type=Path)
    ap.add_argument('--preview', action='store_true', help='Allow recording placeholders for validation only')
    ap.add_argument('--episode', help='Legacy projects only; the current course is exported as whole lessons')
    args = ap.parse_args()
    print(json.dumps(prepare(args.lesson, args.out, args.gsap, args.preview, args.episode), ensure_ascii=False))


if __name__ == '__main__':
    main()
