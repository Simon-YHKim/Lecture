"""A faster voice keeps pitch and exact measured paragraph boundaries."""
import array
from contextlib import redirect_stdout
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import wave

import episodes
import narrate_tts as speech
import prepare_lecture
import write_course_docs
import verify_course
from prepare_lecture import prepare
from sync_narration import attach, sync
import lesson_kit
import os


def tone(path, seconds, hz=440):
    samples = array.array('h', (int(7000 * math.sin(2 * math.pi * hz * i / 22050))
                               for i in range(round(seconds * 22050))))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as output:
        output.setparams((1, 2, 22050, 0, 'NONE', 'not compressed'))
        output.writeframes(samples.tobytes())


class TempoDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.lesson = self.base / 'lesson'
        self.lesson.mkdir()
        self.script = self.lesson / 'SCRIPT.md'
        self.script.write_text('## Line 1 — 확인 (Frame 1)\n\n    (1) 원을 읽습니다.\n\n'
                               '    (2) 선을 읽습니다.\n', encoding='utf-8')

    def make_speech(self):
        if not shutil.which('ffmpeg'):
            self.skipTest('FFmpeg is required for pitch-preserving tempo conversion')
        def fake_sapi(jobs, outdir, voice):
            result = {}
            for i, (key, text) in enumerate(jobs):
                path = Path(outdir) / (key + '.wav')
                tone(path, 1.2 + .4 * i)
                result[key] = str(path)
            return result
        with patch.object(speech, 'speak_many', side_effect=fake_sapi), redirect_stdout(io.StringIO()):
            return speech.narrate(str(self.lesson), str(self.base / 'audio'), speech.VOICE, tempo=1.38)

    def test_atempo_preserves_pitch_and_source_bytes(self):
        if not shutil.which('ffmpeg'):
            self.skipTest('FFmpeg is required')
        source, target = self.base / 'source.wav', self.base / 'fast.wav'
        tone(source, 5)
        before = source.read_bytes()
        speech.change_tempo(source, target, 1.38)
        self.assertEqual(source.read_bytes(), before)
        self.assertLess(abs(speech.wav_seconds(target) - 5 / 1.38), .08)
        for path in (source, target):
            with wave.open(str(path)) as audio:
                samples = array.array('h', audio.readframes(audio.getnframes()))
                rate = audio.getframerate()
            samples = samples[rate // 4:-rate // 4]
            crossings = sum(a <= 0 < b for a, b in zip(samples, samples[1:]))
            self.assertLess(abs(crossings * rate / len(samples) - 440), 2)

    def test_measured_fast_boundaries_and_base_identity_are_recorded(self):
        timing = self.make_speech()
        self.assertEqual(timing['rate'], 0)
        self.assertEqual(timing['tempo'], 1.38)
        speech.verify_tempo_timing(timing, required=True)
        self.assertNotIn(b'\r', (self.lesson / 'narration-timing.json').read_bytes())
        frame = timing['frames'][0]
        media = json.loads((self.lesson / 'media.local.json').read_text())
        self.assertAlmostEqual(frame['duration'], speech.wav_seconds(media['frames'][frame['id']]), places=3)
        self.assertEqual(frame['sourceAudioSha256'], hashlib.sha256(Path(media['sourceFrames'][frame['id']]).read_bytes()).hexdigest())
        self.assertEqual(len(frame['units']), 2)
        for beat, unit in zip(timing['beats'], frame['units']):
            self.assertEqual(beat['observedStart'], unit['start'])
            self.assertEqual(beat['observedEnd'], unit['end'])
            self.assertEqual(beat['sourceObservedStart'], unit['sourceStart'])
        self.assertLess(abs(frame['units'][1]['start'] - frame['units'][0]['end'] - .45 / 1.38), .002)
        self.assertAlmostEqual(speech.frame_hold(timing), 1.6 / 1.38)

    def test_timing_or_speed_edit_breaks_profile_identity(self):
        timing = self.make_speech()
        for field, value in [('tempo', 1.3), ('rate', 1)]:
            changed = {**timing, field: value}
            with self.assertRaises(ValueError):
                speech.verify_tempo_timing(changed, required=True)
        timing['beats'][0]['observedStart'] += .2
        with self.assertRaisesRegex(ValueError, 'identity'):
            speech.verify_tempo_timing(timing, required=True)

    def test_old_rate_zero_timing_is_not_accepted_as_138_percent(self):
        with self.assertRaisesRegex(ValueError, '1.38|tempo'):
            speech.verify_tempo_timing({'source': 'synthesised', 'rate': 0}, required=True)

    def test_fresh_output_required_and_existing_media_keys_survive(self):
        (self.lesson / 'media.local.json').write_text(json.dumps({'DEMO-01': 'keep-this-binding'}))
        self.make_speech()
        media = json.loads((self.lesson / 'media.local.json').read_text())
        self.assertEqual(media['DEMO-01'], 'keep-this-binding')
        with self.assertRaisesRegex(ValueError, 'fresh'):
            self.make_speech()

    def test_one_delivery_per_lesson_preserves_internal_recording_cuts(self):
        self.assertEqual(len(episodes.slugs()), 8)
        self.assertIsNone(episodes.CAP_SEC)
        for slug in episodes.slugs():
            self.assertTrue(episodes.is_unified(slug))
            self.assertEqual(len(episodes.episodes_for(slug)), 1)
            self.assertEqual(episodes.episodes_for(slug)[0]['frames'], episodes.frames_for(slug))
        self.assertEqual(episodes.cuts_for('lesson-04-circles-arcs'), [6, 14])

    def test_narration_cuts_use_the_canonical_contract_without_generated_docs(self):
        lesson = self.base / 'lesson-04-circles-arcs'
        with patch.object(speech, 'ROOT', str(self.base / 'missing-generated-docs')):
            self.assertEqual(speech.cuts_for(str(lesson)), [6, 14])

    def test_delivery_policy_must_match_executable_tempo_and_all_eight_masters(self):
        policy = {'narrationPlaybackRate': 1.38, 'deliveryUnit': 'lesson', 'lessonCount': 8}
        verify_course.check_delivery_policy(policy)
        for key, value in [('narrationPlaybackRate', 1.25), ('deliveryUnit', 'episode'), ('lessonCount', 20)]:
            with self.subTest(field=key), self.assertRaises(ValueError):
                verify_course.check_delivery_policy({**policy, key: value})
        with patch.object(episodes, 'is_unified', return_value=False), self.assertRaises(ValueError):
            verify_course.check_delivery_policy(policy)
        with patch.object(episodes, 'slugs', return_value=episodes.slugs()[:-1]), self.assertRaises(ValueError):
            verify_course.check_delivery_policy(policy)

    def test_course_docs_reject_master_not_yet_retimed_to_current_audio(self):
        timing = self.make_speech()
        frame = timing['frames'][0]
        length = round(frame['duration'] + speech.frame_hold(timing), 3)
        source = ('<div data-composition-id="f1" data-composition-src="compositions/frames/%s.html" '
                  'data-start="0" data-duration="%s"></div>')
        index = self.lesson / 'index.html'
        index.write_text(source % (frame['id'], length + 10), encoding='utf-8')
        with patch.object(write_course_docs, 'ROOT', str(self.base)), \
                patch.object(write_course_docs.vc, 'LESSONS', [('lesson', None, None)]), \
                patch.object(write_course_docs, 'TOPIC', {'lesson': '테스트'}), \
                patch.object(episodes, 'cuts_for', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'master.*timing|retime'):
                write_course_docs.scan()
            index.write_text(source % (frame['id'], length), encoding='utf-8')
            result = write_course_docs.scan()
        self.assertEqual(result[0]['delivery']['lengthSec'], length)

    def test_legacy_episode_option_is_rejected_for_current_course(self):
        with self.assertRaisesRegex(ValueError, 'whole lesson|통합'):
            prepare(self.base / 'lesson-02-part-and-template', self.base / 'out', self.base / 'gsap', episode='ep1')

    def test_unified_export_ignores_old_episodes_and_validates_both_wave_identities(self):
        timing = self.make_speech()
        frame = timing['frames'][0]
        length = round(frame['duration'] + speech.frame_hold(timing), 3)
        frames = self.lesson / 'compositions/frames'
        frames.mkdir(parents=True)
        (frames / (frame['id'] + '.html')).write_text('<div>Current lesson</div>')
        (frames / (frame['id'] + '.motion.json')).write_text(json.dumps({
            'duration': length, 'assertions': [{'kind': 'appearsBy', 'selector': 'div', 'bySec': .2}]}))
        old = self.lesson / 'compositions/episodes/ep99.html'
        old.parent.mkdir()
        old.write_text('Historical content that is not a valid current playlist')
        source = ('<div id="root" data-composition-id="main" data-start="0" data-duration="%s">'
                  '<div id="slot" data-composition-id="f1" data-composition-src="compositions/frames/%s.html" '
                  'data-start="0" data-duration="%s"></div></div><script>window.__timelines={};</script>') % (length, frame['id'], length)
        (self.lesson / 'index.html').write_text(attach(source, timing), encoding='utf-8', newline='\n')
        gsap = self.base / 'gsap.min.js'
        gsap.write_text('// gsap fixture\n' + ' ' * 10000)
        with patch.object(episodes, 'is_unified', return_value=True):
            self.assertEqual(sync(self.lesson), 1)
            result = prepare(self.lesson, self.base / 'delivery', gsap)
            media = json.loads((self.lesson / 'media.local.json').read_text())
            original = Path(media['sourceFrames'][frame['id']])
            original_motion = prepare_lecture.motion_spec
            def change_base_after_validation(*args):
                result = original_motion(*args)
                original.write_bytes(original.read_bytes() + b'changed')
                return result
            with patch.object(prepare_lecture, 'motion_spec', side_effect=change_base_after_validation):
                with self.assertRaisesRegex(ValueError, 'source narration changed during export'):
                    prepare(self.lesson, self.base / 'changed-during-export', gsap)
            self.assertFalse((self.base / 'changed-during-export').exists())
            with self.assertRaisesRegex(ValueError, 'source narration identity'):
                prepare(self.lesson, self.base / 'blocked', gsap)
        self.assertFalse((self.base / 'delivery/compositions/episodes').exists())
        self.assertEqual(old.read_text(), 'Historical content that is not a valid current playlist')
        self.assertAlmostEqual(result['duration'], length)
        manifest = json.loads((self.base / 'delivery/source-manifest.json').read_text())
        self.assertEqual(manifest['narrationTempo'], 1.38)
        self.assertEqual(manifest['deliveryMode'], 'lesson')
        self.assertNotIn('compositions/episodes/ep99.html', manifest['validationSources'])

    def test_builder_returns_master_without_touching_historical_episode(self):
        slug = 'lesson-01-orientation'
        lesson = self.base / slug
        old = lesson / 'compositions/episodes/ep1.html'
        old.parent.mkdir(parents=True)
        old.write_text('Historical preview')
        slots = [('s%d' % i, 'f%d' % i, stem, float(i * 10), 10.0)
                 for i, stem in enumerate(episodes.frames_for(slug))]
        result = lesson_kit.write_episodes(str(lesson), slots, episodes.episodes_for(slug), os)
        self.assertEqual(result[0][0], 'index.html')
        self.assertEqual(len(result), 1)
        self.assertEqual(old.read_text(), 'Historical preview')

    def test_unified_master_clock_is_checked_before_creating_output(self):
        self.script.write_text('## Line 1 — 첫 화면 (Frame 1)\n\n    (1) 원을 읽습니다.\n\n'
                               '## Line 2 — 다음 화면 (Frame 2)\n\n    (1) 선을 읽습니다.\n',
                               encoding='utf-8')
        timing = self.make_speech()
        frames = self.lesson / 'compositions/frames'
        frames.mkdir(parents=True)
        lengths = [round(f['duration'] + speech.frame_hold(timing), 3) for f in timing['frames']]
        for frame in timing['frames']:
            (frames / (frame['id'] + '.html')).write_text('<div>Clock fixture</div>')
        gsap = self.base / 'gsap.min.js'
        gsap.write_text('// gsap fixture\n' + ' ' * 10000)

        def playlist(starts, durations, root_duration, root_start=0, extra=''):
            slots = []
            for index, (frame, start, duration) in enumerate(zip(timing['frames'], starts, durations)):
                slots.append('<div id="slot%d" data-composition-id="f%d" '
                             'data-composition-src="compositions/frames/%s.html" '
                             'data-start="%s" data-duration="%s"></div>'
                             % (index, index, frame['id'], start, duration))
                (frames / (frame['id'] + '.motion.json')).write_text(json.dumps({
                    'duration': duration, 'assertions': [{'kind': 'appearsBy', 'selector': 'div', 'bySec': .2}]}))
            source = ('<div id="root" data-composition-id="main" data-start="%s" data-duration="%s">'
                      '%s%s</div><script>window.__timelines={};</script>') % (
                          root_start, root_duration, ''.join(slots), extra)
            (self.lesson / 'index.html').write_text(attach(source, timing), encoding='utf-8', newline='\n')

        total = sum(lengths)
        cases = [
            ('short-root', [0, lengths[0]], lengths, 1, 0, ''),
            ('nonzero-root', [0, lengths[0]], lengths, total, 1, ''),
            ('nonzero-first-slot', [10, 10 + lengths[0]], lengths, total + 10, 0, ''),
            ('gap', [0, lengths[0] + 1], lengths, total + 1, 0, ''),
            ('overlap', [0, lengths[0] - 1], lengths, total - 1, 0, ''),
            ('wrong-hold', [0, lengths[0] + 1], [lengths[0] + 1, lengths[1]], total + 1, 0, ''),
            ('unparsed-reference', [0, lengths[0]], lengths, total, 0,
             '<div data-composition-src="other.html"></div>'),
        ]
        with patch.object(episodes, 'is_unified', return_value=True):
            for label, starts, durations, root_duration, root_start, extra in cases:
                with self.subTest(case=label):
                    playlist(starts, durations, root_duration, root_start, extra)
                    output = self.base / label
                    with self.assertRaises(ValueError):
                        prepare(self.lesson, output, gsap)
                    self.assertFalse(output.exists())
            playlist([0, lengths[0]], lengths, total)
            result = prepare(self.lesson, self.base / 'valid-master', gsap)
            self.assertAlmostEqual(result['duration'], total, places=3)


if __name__ == '__main__':
    unittest.main()
