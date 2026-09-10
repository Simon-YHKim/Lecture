"""Selected exports retain whole-lesson identity and the episode's local clock."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import wave

from narrate_tts import spoken_hash
from prepare_lecture import GSAP_URL, prepare
from sync_narration import attach


class PrepareEpisodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.lesson = self.base / 'lesson'
        self.frames = self.lesson / 'compositions/frames'
        self.episodes = self.lesson / 'compositions/episodes'
        self.frames.mkdir(parents=True)
        self.episodes.mkdir()
        self.output = self.base / 'export'
        self.gsap = self.base / 'gsap.min.js'
        self.gsap.write_text('// gsap fixture\n' + ' ' * 10000)
        script = self.lesson / 'SCRIPT.md'
        script.write_text('## Line 1 — Test (Frame 1)\n\n    (1) Read the drawing.\n', encoding='utf-8')
        measured, media = [], {}
        self.stems = ['01-title', '02-demo', '03-recap', '04-closing']
        for i, stem in enumerate(self.stems):
            wav = self.base / (stem + '.wav')
            with wave.open(str(wav), 'wb') as audio:
                audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
                audio.writeframes(b'\x64\x00' * 1600)
            measured.append({'id': stem, 'audio': wav.name, 'duration': .2,
                             'audioSha256': hashlib.sha256(wav.read_bytes()).hexdigest()})
            media[stem] = str(wav)
            self.write(self.frames / (stem + '.html'),
                       '<div>' + ('USER RECORDING' if i == 1 else stem) + '</div>')
            self.write_json(self.frames / (stem + '.motion.json'), {
                'duration': 1.8, 'assertions': [
                    {'kind': 'appearsBy', 'selector': '#f%d h1' % i, 'bySec': .5}]})
        self.timing = {'frames': measured, 'totalSeconds': .8,
                       'spokenTextSha256': spoken_hash(script)}
        self.write_json(self.lesson / 'narration-timing.json', self.timing)
        self.write_json(self.lesson / 'media.local.json', {'frames': media})
        self.write(self.lesson / 'index.html', self.playlist(self.stems))
        for number, stems in enumerate([self.stems[:1], self.stems[1:2], self.stems[2:]], 1):
            self.write(self.episodes / ('ep%d.html' % number), self.playlist(stems))

    @staticmethod
    def write(path, text):
        path.write_text(text, encoding='utf-8', newline='\n')

    def write_json(self, path, value):
        self.write(path, json.dumps(value))

    def playlist(self, stems):
        content = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n'
        content += '<div id="root" data-composition-id="main" data-start="0" data-duration="%g">\n' % (1.8 * len(stems))
        for i, stem in enumerate(stems):
            content += ('<div data-composition-id="f%d" data-composition-src="compositions/frames/%s.html" '
                        'data-start="%g" data-duration="1.8"></div>\n' % (self.stems.index(stem), stem, 1.8 * i))
        return attach(content + '</div>\n<script>window.__timelines={};</script>', self.timing)

    def assert_rejected(self, episode='ep3', pattern=None):
        with self.assertRaisesRegex((ValueError, FileNotFoundError), pattern or '.'):
            prepare(self.lesson, self.output, self.gsap, episode=episode)
        self.assertFalse(self.output.exists(), 'Validation must finish before creating output')

    def test_lecture_only_export_keeps_episode_clock_and_selected_dependencies(self):
        result = prepare(self.lesson, self.output, self.gsap, episode='ep3')
        entry = self.episodes / 'ep3.html'
        self.assertEqual((self.output / 'index.html').read_text(encoding='utf-8'),
                         GSAP_URL.sub('assets/vendor/gsap.min.js', entry.read_text(encoding='utf-8')))
        self.assertEqual(sorted(p.name for p in (self.output / 'compositions/frames').iterdir()),
                         ['03-recap.html', '03-recap.motion.json', '04-closing.html', '04-closing.motion.json'])
        self.assertEqual(sorted(p.name for p in (self.output / 'assets/narration').iterdir()),
                         ['03-recap.wav', '04-closing.wav'])
        self.assertFalse((self.output / 'compositions/episodes').exists())
        motion = json.loads((self.output / 'index.motion.json').read_text())
        self.assertEqual(motion['duration'], 3.6)
        self.assertEqual([a['bySec'] for a in motion['assertions']], [.5, 2.3])
        manifest = json.loads((self.output / 'source-manifest.json').read_text())
        self.assertEqual(manifest['entrySource'], 'compositions/episodes/ep3.html')
        self.assertEqual(manifest['episode'], 'ep3')
        self.assertEqual(manifest['audioFrameIds'], self.stems[2:])
        self.assertEqual(manifest['sourceFiles'][manifest['entrySource']], hashlib.sha256(entry.read_bytes()).hexdigest())
        self.assertEqual(manifest['audioSources']['03-recap.wav']['sha256'], self.timing['frames'][2]['audioSha256'])
        self.assertEqual((result['audioFrames'], result['audioSeconds'], result['duration']), (2, .4, 3.6))

    def test_selected_recording_is_rejected(self):
        self.assert_rejected('ep2', 'recording is missing')

    def test_selected_preview_keeps_only_its_recording_and_wav(self):
        result = prepare(self.lesson, self.output, self.gsap, preview=True, episode='ep2')
        manifest = json.loads((self.output / 'source-manifest.json').read_text())
        self.assertEqual(result['audioFrames'], 1)
        self.assertEqual(manifest['purpose'], 'validation-preview')
        self.assertEqual(manifest['missingRecordings'], ['compositions/frames/02-demo.html'])
        self.assertEqual([p.name for p in (self.output / 'assets/narration').iterdir()], ['02-demo.wav'])

    def test_full_export_still_rejects_recording_and_preview_copies_all(self):
        self.assert_rejected(None, 'recording is missing')
        result = prepare(self.lesson, self.output, self.gsap, preview=True)
        self.assertEqual(result['audioFrames'], 4)
        self.assertTrue((self.output / 'compositions/episodes/ep2.html').is_file())

    def test_unselected_stale_wav_is_rejected(self):
        wav = self.base / '02-demo.wav'
        wav.write_bytes(wav.read_bytes()[:-2] + b'\x00\x00')
        self.assert_rejected(pattern='WAV identity')

    def test_hashed_wav_with_wrong_duration_is_rejected(self):
        wav = self.base / '02-demo.wav'
        with wave.open(str(wav), 'wb') as audio:
            audio.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
            audio.writeframes(b'\x64\x00' * 2400)
        self.timing['frames'][1]['audioSha256'] = hashlib.sha256(wav.read_bytes()).hexdigest()
        self.write_json(self.lesson / 'narration-timing.json', self.timing)
        self.assert_rejected(pattern='WAV duration')

    def test_case_only_wav_collision_is_rejected_before_copy(self):
        self.timing['frames'][3]['audio'] = '03-RECAP.wav'
        other = self.base / 'other'
        other.mkdir()
        audio = other / '03-RECAP.wav'
        audio.write_bytes((self.base / '04-closing.wav').read_bytes())
        media = json.loads((self.lesson / 'media.local.json').read_text())
        media['frames']['04-closing'] = str(audio)
        self.write_json(self.lesson / 'media.local.json', media)
        self.write_json(self.lesson / 'narration-timing.json', self.timing)
        for path in [self.lesson / 'index.html', *self.episodes.glob('ep*.html')]:
            self.write(path, attach(path.read_text(), self.timing))
        self.assert_rejected(pattern='Duplicate narration filename')

    def test_case_only_frame_collision_is_rejected(self):
        self.stems[3] = '03-RECAP'
        self.timing['frames'][3]['id'] = '03-RECAP'
        self.write_json(self.lesson / 'narration-timing.json', self.timing)
        self.write(self.lesson / 'index.html', self.playlist(self.stems))
        self.write(self.episodes / 'ep3.html', self.playlist(self.stems[2:]))
        self.assert_rejected(pattern='complete master')

    def test_whole_script_identity_is_required(self):
        self.write(self.lesson / 'SCRIPT.md', '## Line 1 — Test (Frame 1)\n\n    (1) Changed speech.\n')
        self.assert_rejected(pattern='TTS')

    def test_invalid_and_missing_episode(self):
        for episode in ['../ep1', 'ep0', 'ep01', 'ep-1', 'ep1.html', 'ep1/ep3', '', 'ep9']:
            with self.subTest(episode=episode):
                self.assert_rejected(episode)

    def test_unparsed_reference_is_not_silently_omitted(self):
        entry = self.episodes / 'ep3.html'
        content = entry.read_text(encoding='utf-8').replace('</div>\n<script>',
            '<div data-composition-src="../unexpected.html"></div></div>\n<script>')
        self.write(entry, content)
        self.assert_rejected()

    def test_frame_path_escape_is_rejected(self):
        entry = self.episodes / 'ep3.html'
        original = entry.read_text(encoding='utf-8')
        absolute_reference = (self.base / 'outside' / '03-recap.html').as_posix()
        for reference in ['../03-recap.html', 'compositions/frames/../03-recap.html',
                          absolute_reference, 'compositions/frames/03-recap\\extra.html']:
            with self.subTest(reference=reference):
                self.write(entry, original.replace('compositions/frames/03-recap.html', reference))
                self.assert_rejected()

    def test_symlink_frame_escape_is_rejected(self):
        frame = self.frames / '03-recap.html'
        outside = self.base / 'outside.html'
        self.write(outside, '<div>External frame</div>')
        frame.unlink()
        try:
            frame.symlink_to(outside)
        except OSError as error:
            self.skipTest('This host does not permit creating a symlink: ' + str(error))
        self.assert_rejected(pattern='leaves its lesson directory')

    def test_duplicate_composition_and_frame_are_rejected(self):
        entry = self.episodes / 'ep3.html'
        original = entry.read_text(encoding='utf-8')
        self.write(entry, attach(original.replace('data-composition-id="f3"', 'data-composition-id="f2"'), self.timing))
        self.assert_rejected()
        self.write(entry, self.playlist(['03-recap', '03-recap']))
        self.assert_rejected()

    def test_episode_omission_and_unmeasured_frame_are_rejected(self):
        entry = self.episodes / 'ep3.html'
        self.write(entry, self.playlist(['03-recap']))
        self.assert_rejected()
        self.write(entry, self.playlist(self.stems[2:]).replace('03-recap.html', 'unknown.html'))
        self.assert_rejected()

    def test_stale_unselected_playlist_is_rejected(self):
        entry = self.episodes / 'ep1.html'
        self.write(entry, entry.read_text().replace('data-duration="0.2"', 'data-duration="0.1"'))
        self.assert_rejected(pattern='Playlist narration is stale')

    def test_missing_frame_or_motion_is_rejected(self):
        for suffix in ['.html', '.motion.json']:
            path = self.frames / ('03-recap' + suffix)
            content = path.read_bytes()
            path.unlink()
            self.assert_rejected()
            path.write_bytes(content)

    def test_nested_frame_dependency_is_rejected_instead_of_omitted(self):
        self.write(self.frames / '03-recap.html', '<div data-composition-src="compositions/frames/02-demo.html"></div>')
        self.assert_rejected()

    def test_episode_clock_and_nonfinite_motion_are_rejected(self):
        entry = self.episodes / 'ep3.html'
        original = entry.read_text()
        self.write(entry, attach(original.replace('data-start="1.8"', 'data-start="2"'), self.timing))
        self.assert_rejected()
        self.write(entry, original)
        sidecar = self.frames / '03-recap.motion.json'
        self.write_json(sidecar, {'duration': float('nan'), 'assertions': []})
        self.assert_rejected()

    def test_root_duration_and_motion_deadline_are_rejected(self):
        entry = self.episodes / 'ep3.html'
        original = entry.read_text()
        self.write(entry, original.replace('data-duration="3.6"', 'data-duration="3.7"'))
        self.assert_rejected(pattern='root duration')
        self.write(entry, original)
        for deadline in [float('nan'), float('inf'), -1, 2]:
            with self.subTest(deadline=deadline):
                self.write_json(self.frames / '03-recap.motion.json', {
                    'duration': 1.8, 'assertions': [{'kind': 'appearsBy', 'selector': 'h1', 'bySec': deadline}]})
                self.assert_rejected(pattern='Motion deadline')


if __name__ == '__main__':
    unittest.main()
