"""Recording intake must preserve narration and publish only complete exports."""
import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import wave

import ingest_recording as intake
import episodes
import prepare_lecture
from narrate_tts import spoken_hash
from prepare_lecture import prepare
from sync_narration import attach


class RecordingIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
            raise unittest.SkipTest('Local FFmpeg and ffprobe are required')
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.clip = Path(cls.temp.name) / 'test-only.mp4'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi',
                        '-i', 'color=c=blue:s=1920x1080:r=30:d=1.8', '-an',
                        '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt',
                        'yuv420p', str(cls.clip)], check=True, timeout=30)

    def setUp(self):
        # These fixtures retain the old 0.2s WAV/1.8s clocks to isolate intake
        # regressions. Current unified/tempo delivery is tested separately.
        legacy = patch.object(episodes, 'is_unified', return_value=False)
        legacy.start()
        self.addCleanup(legacy.stop)
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.base = Path(self.work.name)
        self.lesson = self.base / 'lesson-02-part-and-template'
        self.frames = self.lesson / 'compositions/frames'
        self.frames.mkdir(parents=True)
        (self.lesson / 'compositions/episodes').mkdir()
        self.output = self.base / 'delivery'
        self.gsap = self.base / 'gsap.min.js'
        self.gsap.write_text('// gsap fixture\n' + ' ' * 10000)
        self.input = self.base / 'take.mp4'
        shutil.copyfile(self.clip, self.input)
        self.stems = ['01-title', '08-build-template', '09-recap']
        media, measured = {}, []
        for i, stem in enumerate(self.stems):
            wav = self.base / (stem + '.wav')
            with wave.open(str(wav), 'wb') as audio:
                audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                audio.writeframes(b'\x64\x00' * 1600)
            media[stem] = str(wav)
            measured.append({'id': stem, 'audio': wav.name, 'duration': .2,
                             'audioSha256': hashlib.sha256(wav.read_bytes()).hexdigest()})
            content = ('<div class="film"><div class="rec"><div class="recmark">USER RECORDING</div>'
                       '<div class="recsub">DEMO-01 &#183; L02_TEMPLATE</div></div>'
                       '<div class="strip">Keep this step overlay</div></div>') if i == 1 else stem
            (self.frames / (stem + '.html')).write_text(
                '<div data-composition-id="f%d" data-duration="1.8"><section class="clip" '
                'data-start="0" data-duration="1.8">%s</section></div>' % (i, content), encoding='utf-8')
            self.write_json(self.frames / (stem + '.motion.json'), {
                'duration': 1.8, 'assertions': [{'kind': 'appearsBy', 'selector': 'h1', 'bySec': .5}]})
        (self.lesson / 'SCRIPT.md').write_text('## Line 1 — Test (Frame 1)\n\n    (1) Drawing.\n', encoding='utf-8')
        self.timing = {'frames': measured, 'totalSeconds': .6,
                       'spokenTextSha256': spoken_hash(self.lesson / 'SCRIPT.md')}
        self.write_json(self.lesson / 'narration-timing.json', self.timing)
        self.media = {'narrationDir': str(self.base), 'frames': media, 'otherBinding': {'keep': 7}}
        self.write_json(self.lesson / 'media.local.json', self.media)
        (self.lesson / 'index.html').write_text(self.playlist(self.stems), encoding='utf-8')
        for i, stem in enumerate(self.stems, 1):
            (self.lesson / 'compositions/episodes' / ('ep%d.html' % i)).write_text(self.playlist([stem]), encoding='utf-8')

    @staticmethod
    def write_json(path, data):
        path.write_text(json.dumps(data), encoding='utf-8')

    def playlist(self, stems):
        source = '<div id="root" data-composition-id="main" data-start="0" data-duration="%.3f">' % (1.8 * len(stems))
        for i, stem in enumerate(stems):
            source += ('<div data-composition-id="f%d" data-composition-src="compositions/frames/%s.html" '
                       'data-start="%.3f" data-duration="1.8"></div>' % (self.stems.index(stem), stem, 1.8 * i))
        return attach(source + '</div><script>window.__timelines={};</script>', self.timing)

    def register(self):
        with redirect_stdout(io.StringIO()):
            return intake.ingest(str(self.lesson), [str(self.input)])

    def test_register_preserves_narration_and_other_bindings_and_records_identity(self):
        self.register()
        media = json.loads((self.lesson / 'media.local.json').read_text(encoding='utf-8'))
        for key, value in self.media.items():
            self.assertEqual(media[key], value)
        record = json.loads((self.lesson / 'recording.json').read_text())
        self.assertEqual(record['parts'][0]['sha256'], hashlib.sha256(self.input.read_bytes()).hexdigest())
        self.assertEqual(record['parts'][0]['durationSec'], 1.8)

    def test_missing_file_leaves_metadata_unchanged(self):
        original = (self.lesson / 'media.local.json').read_bytes()
        with self.assertRaises((ValueError, SystemExit)):
            intake.ingest(str(self.lesson), [str(self.base / 'absent.mp4')])
        self.assertEqual((self.lesson / 'media.local.json').read_bytes(), original)
        self.assertFalse((self.lesson / 'recording.json').exists())

    def test_corrupt_recording_is_rejected_before_any_metadata_write(self):
        self.input.write_bytes(b'not a video')
        with self.assertRaises((ValueError, subprocess.CalledProcessError)):
            self.register()
        self.assertFalse((self.lesson / 'recording.json').exists())
        self.assertEqual(json.loads((self.lesson / 'media.local.json').read_text()), self.media)

    def test_export_copies_exact_recording_preserving_local_clock_and_overlay(self):
        self.register()
        original = (self.frames / '08-build-template.html').read_bytes()
        result = prepare(self.lesson, self.output, self.gsap, episode='ep2')
        html = (self.output / 'compositions/frames/08-build-template.html').read_text()
        self.assertNotIn('USER RECORDING', html)
        self.assertIn('Keep this step overlay', html)
        self.assertIn('muted', html)
        self.assertIn('playsinline', html)
        self.assertIn('data-start="0"', html.split('<video', 1)[1].split('>', 1)[0])
        self.assertNotIn('data-start=', html.split('<section', 1)[1].split('>', 1)[0])
        self.assertIn('data-duration="1.8"', html)
        self.assertEqual((self.output / 'assets/recordings/DEMO-01.mp4').read_bytes(), self.input.read_bytes())
        self.assertEqual((self.frames / '08-build-template.html').read_bytes(), original)
        self.assertEqual(result['recordings'], 1)
        self.assertEqual(result['duration'], 1.8)
        manifest = json.loads((self.output / 'source-manifest.json').read_text())
        self.assertEqual(manifest['recordingSources']['DEMO-01']['sha256'], hashlib.sha256(self.input.read_bytes()).hexdigest())
        self.assertEqual(manifest['missingRecordings'], [])
        self.assertEqual(sorted(p.name for p in (self.output / 'assets/narration').iterdir()), ['08-build-template.wav'])

    def test_changed_recording_is_rejected_before_export_directory_exists(self):
        self.register()
        self.input.write_bytes(self.input.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'identity|changed'):
            prepare(self.lesson, self.output, self.gsap, episode='ep2')
        self.assertFalse(self.output.exists())

    def test_short_or_long_video_is_not_silently_stretched_or_trimmed(self):
        self.register()
        for length in [.5, 3.0]:
            with self.subTest(length=length), patch.object(intake, 'probe', return_value={
                    'durationSec': length, 'width': 1920, 'height': 1080, 'fps': 30,
                    'codec': 'h264', 'pixelFormat': 'yuv420p'}):
                record = json.loads((self.lesson / 'recording.json').read_text())
                record['durationSec'] = length
                record['parts'][0]['durationSec'] = length
                self.write_json(self.lesson / 'recording.json', record)
                with self.assertRaisesRegex(ValueError, 'duration|length'):
                    prepare(self.lesson, self.output, self.gsap, episode='ep2')
                self.assertFalse(self.output.exists())

    def test_missing_part_and_wrong_placeholder_do_not_export(self):
        self.register()
        record = json.loads((self.lesson / 'recording.json').read_text())
        record['parts'] = []
        self.write_json(self.lesson / 'recording.json', record)
        with self.assertRaisesRegex(ValueError, 'parts|recording'):
            prepare(self.lesson, self.output, self.gsap, episode='ep2')
        self.assertFalse(self.output.exists())

    def test_removing_or_relabelling_placeholder_cannot_bypass_missing_recording_gate(self):
        path = self.frames / '08-build-template.html'
        original = path.read_text()
        for text in [original.replace('USER RECORDING', 'Complete'), original.replace('DEMO-01 ', 'DEMO-01A ')]:
            with self.subTest(text=text[-90:]):
                path.write_text(text)
                with self.assertRaisesRegex(ValueError, 'placeholder'):
                    prepare(self.lesson, self.output, self.gsap, preview=True, episode='ep2')
                self.assertFalse(self.output.exists())

    def test_failed_second_metadata_replace_restores_first_and_preserves_audio_map(self):
        before = (self.lesson / 'media.local.json').read_bytes()
        original = intake.os.replace
        def fail_local(source, target):
            if Path(source).name == 'media.local.json':
                raise OSError('simulated registration failure')
            return original(source, target)
        with patch.object(intake.os, 'replace', side_effect=fail_local):
            with self.assertRaisesRegex(OSError, 'simulated'):
                self.register()
        self.assertEqual((self.lesson / 'media.local.json').read_bytes(), before)
        self.assertFalse((self.lesson / 'recording.json').exists())

    def test_repository_path_is_rejected_even_from_another_working_directory(self):
        repo = self.base / 'another-checkout'
        repo.mkdir()
        (repo / '.git').mkdir()
        source = repo / 'take.mp4'
        shutil.copyfile(self.input, source)
        with self.assertRaisesRegex(ValueError, 'Git'):
            intake.recording_file(source)

    def test_selected_second_part_uses_its_file_and_zero_local_clock(self):
        second = self.base / 'second.mp4'
        shutil.copyfile(self.input, second)
        path = self.frames / '08-build-template.html'
        path.write_text(path.read_text().replace('DEMO-01 ', 'DEMO-01A '))
        (self.frames / '09-recap.html').write_text(path.read_text().replace('DEMO-01A ', 'DEMO-01B ').replace('f1', 'f2'))
        ids = ['DEMO-01A', 'DEMO-01B']
        with patch.object(intake, 'recording_ids', return_value=ids), patch.object(intake, 'recording_frames', return_value=dict(zip(self.stems[1:], ids))):
            with redirect_stdout(io.StringIO()):
                intake.ingest(str(self.lesson), [str(self.input), str(second)])
            result = prepare(self.lesson, self.output, self.gsap, episode='ep3')
        self.assertEqual(result['recordings'], 1)
        html = (self.output / 'compositions/frames/09-recap.html').read_text()
        self.assertIn('assets/recordings/DEMO-01B.mp4', html)
        self.assertIn('data-media-start="0"', html)
        self.assertEqual([p.name for p in (self.output / 'assets/recordings').iterdir()], ['DEMO-01B.mp4'])
        manifest = json.loads((self.output / 'source-manifest.json').read_text())
        self.assertEqual(manifest['episode'], 'ep3')
        self.assertEqual(manifest['duration'], 1.8)

    def test_all_canonical_recording_parts_are_covered(self):
        expected = {'lesson-02-part-and-template': 1, 'lesson-03-baseline-profile': 2,
                    'lesson-04-circles-arcs': 3, 'lesson-05-three-views': 3,
                    'lesson-06-editing-symbols': 3, 'lesson-07-dimensioning-release': 3}
        self.assertEqual(sum(expected.values()), 15)
        for slug, count in expected.items():
            self.assertEqual(len(intake.recording_frames(slug)), count)

    def test_invalid_video_streams_and_incomplete_decode_are_rejected(self):
        stream = {'codec_type': 'video', 'codec_name': 'h264', 'pix_fmt': 'yuv420p',
                  'width': 1920, 'height': 1080, 'sample_aspect_ratio': '1:1',
                  'avg_frame_rate': '30/1', 'duration': '1.8', 'nb_frames': '54'}
        changes = [{'width': 1280}, {'duration': 'nan'}, {'avg_frame_rate': '0/0'},
                   {'tags': {'rotate': '90'}}, {'sample_aspect_ratio': '2:1'}, {'codec_name': 'hevc'}]
        for change in changes:
            doc = {'streams': [{**stream, **change}], 'format': {'format_name': 'mov,mp4'}}
            with self.subTest(change=change), patch.object(intake.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(doc))):
                with self.assertRaises(ValueError):
                    intake.probe(self.input)
        doc = {'streams': [stream], 'format': {'format_name': 'mov,mp4'}}
        responses = [subprocess.CompletedProcess([], 0, json.dumps(doc)),
                     subprocess.CompletedProcess([], 0, 'frame=20\nout_time_us=666667\nprogress=end\n')]
        with patch.object(intake.subprocess, 'run', side_effect=responses):
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                intake.probe(self.input)

    def test_copy_failure_never_publishes_partial_delivery(self):
        self.register()
        original_copy = shutil.copyfile
        def fail_recording(source, target, *args, **kwargs):
            if str(source).endswith('.mp4'):
                raise OSError('simulated copy failure')
            return original_copy(source, target, *args, **kwargs)
        with patch('prepare_lecture.shutil.copyfile', side_effect=fail_recording):
            with self.assertRaisesRegex(OSError, 'simulated'):
                prepare(self.lesson, self.output, self.gsap, episode='ep2')
        self.assertFalse(self.output.exists())

    def test_partial_section_is_not_retimed_implicitly(self):
        self.register()
        path = self.frames / '08-build-template.html'
        path.write_text(path.read_text().replace('data-start="0"', 'data-start="0.5"'))
        with self.assertRaisesRegex(ValueError, 'complete measured frame'):
            prepare(self.lesson, self.output, self.gsap, episode='ep2')
        self.assertFalse(self.output.exists())

    def test_playlist_change_after_validation_cannot_replace_the_validated_identity(self):
        original = prepare_lecture.motion_spec
        def change_playlist(lesson, source):
            result = original(lesson, source)
            path = self.lesson / 'compositions/episodes/ep3.html'
            path.write_text(path.read_text().replace('data-duration="1.800"', 'data-duration="99"'))
            return result
        with patch.object(prepare_lecture, 'motion_spec', side_effect=change_playlist):
            with self.assertRaisesRegex(ValueError, 'Source changed'):
                prepare(self.lesson, self.output, self.gsap, episode='ep3')
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
