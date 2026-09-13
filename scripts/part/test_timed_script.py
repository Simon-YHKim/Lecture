"""Review timestamps must follow synthesis units, not physical source lines."""
import json
import re
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import narrate_tts as N
import timed_script


class TimedScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.lesson = Path(self.temp.name) / 'lesson-99-review'
        self.lesson.mkdir()

    def fixture(self, text, name='SCRIPT.md'):
        source = self.lesson / name
        source.write_text(text, encoding='utf-8')
        jobs, units, order = N.synthesis_plan(str(source))
        frames = []
        for seq, (line, part, fid) in enumerate(order):
            frames.append({'id': fid, 'line': line, 'start': seq * 100,
                           'units': [{'beat': beat, 'start': i * 10 + 1,
                                      'end': i * 10 + 8}
                                     for i, (_, beat) in enumerate(units[line, part])]})
        timing = {'spokenTextSha256': N.spoken_hash(str(source)),
                  'totalSeconds': 300, 'frames': frames}
        self.save_timing(timing)
        return timing

    def save_timing(self, timing):
        (self.lesson / 'narration-timing.json').write_text(
            json.dumps(timing), encoding='utf-8')

    def convert(self, lang='ko', name='SCRIPT.md'):
        result = timed_script.convert(self.lesson, lang, name)
        return result[0].read_text(encoding='utf-8')

    def test_multiline_paragraph_does_not_consume_next_timestamp(self):
        self.fixture('## Line 1\n\n    (silence)\n\n'
                     '    (1) First sentence.\n    Continuation.\n\n'
                     '    (2) Next paragraph.\n')
        out = self.convert()
        self.assertIn('    `[0:01–0:08]` (1) First sentence.\n    Continuation.', out)
        self.assertIn('    `[0:11–0:18]` (2) Next paragraph.', out)
        self.assertNotIn('` (silence)', out)

    def test_whole_step_time_is_outside_its_paragraphs(self):
        text = ('## Line 1\n\n### 1단계\n\n    First instruction.\n'
                '    Same paragraph.\n\n    Another paragraph.\n\n'
                '### 2단계\n\n    Second step.\n\n'
                '## Line 2\n\n    Final summary.\n')
        self.fixture(text)
        out = self.convert()
        self.assertIn('### 1단계\n> <!-- timed-step --> `[0:01–0:08]`', out)
        self.assertIn('### 2단계\n> <!-- timed-step --> `[0:11–0:18]`', out)
        self.assertIn('    `[1:41–1:48]` Final summary.', out)
        self.assertNotIn('` First instruction.', out)
        clean = re.sub(r'^<!--.*?-->\n\n', '', out, count=1, flags=re.S)
        clean = re.sub(r'^> <!-- timed-step -->.*\n', '', clean, flags=re.M)
        clean = re.sub(r'`\[\d+:\d+–\d+:\d+\]` ', '', clean)
        self.assertEqual(clean, text)

    def test_stale_or_wrong_language_timing_is_rejected_before_write(self):
        self.fixture('## Line 1\n\n    Original speech.\n')
        (self.lesson / 'SCRIPT.en.md').write_text(
            '## Line 1\n\n    Different speech.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'hash|해시'):
            self.convert('en', 'SCRIPT.en.md')
        self.assertFalse((self.lesson / 'SCRIPT.timed.en.md').exists())

    def test_timing_unit_count_mismatch_is_rejected(self):
        timing = self.fixture('## Line 1\n\n    First.\n\n    Second.\n')
        timing['frames'][0]['units'].pop()
        self.save_timing(timing)
        with self.assertRaisesRegex(ValueError, 'unit|단위'):
            self.convert()

    def test_wrong_frame_identity_is_rejected(self):
        timing = self.fixture('## Line 1\n\n    First.\n')
        timing['frames'][0]['id'] = 'unrelated-frame'
        self.save_timing(timing)
        with self.assertRaisesRegex(ValueError, 'frame|프레임'):
            self.convert()

    def test_english_step_heading_is_supported(self):
        self.fixture('## Line 1\n\n### Step 1\n\n    Type `REC`.\n', 'SCRIPT.en.md')
        out = self.convert('en', 'SCRIPT.en.md')
        self.assertIn('### Step 1\n> <!-- timed-step --> `[0:01–0:08]`', out)
        self.assertIn('entire step', out)
        self.assertIn('    Type `REC`.', out)

    def test_line_headings_accepted_by_synthesis_are_supported(self):
        self.fixture('###Line 1\n\n    First section.\n\n'
                     '##Line 2\n\n    Second section.\n')
        out = self.convert()
        self.assertIn('    `[0:01–0:08]` First section.', out)
        self.assertIn('    `[1:41–1:48]` Second section.', out)

    def test_indented_blockquote_does_not_consume_speech_timestamp(self):
        self.fixture('## Line 1\n\n    > Production note.\n\n'
                     '    Spoken paragraph.\n')
        out = self.convert()
        self.assertIn('    > Production note.', out)
        self.assertIn('    `[0:01–0:08]` Spoken paragraph.', out)
        self.assertNotIn('` > Production note.', out)

    def test_recording_parts_use_their_own_frame_start(self):
        frames = self.lesson / 'compositions/frames'
        frames.mkdir(parents=True)
        for name in ['01-demo-a.html', '01-demo-b.html', '02-summary.html']:
            (frames / name).touch()
        text = ('## Line 1\n\n### Step 1\n\n    First.\n\n'
                '### Step 2\n\n    Second.\n\n'
                '### Step 3\n\n    Third.\n\n'
                '### Step 4\n\n    Fourth.\n\n'
                '## Line 2\n\n    Summary.\n')
        with patch.object(N, 'cuts_for', return_value=[2]):
            self.fixture(text)
            out = self.convert()
        self.assertIn('### Step 2\n> <!-- timed-step --> `[0:11–0:18]`', out)
        self.assertIn('### Step 3\n> <!-- timed-step --> `[1:41–1:48]`', out)
        self.assertIn('### Step 4\n> <!-- timed-step --> `[1:51–1:58]`', out)
        self.assertIn('    `[3:21–3:28]` Summary.', out)

    def test_invalid_beat_or_unit_time_is_rejected_before_write(self):
        for field, value in [('beat', 99), ('start', -1), ('end', 0), ('end', float('nan'))]:
            with self.subTest(field=field, value=value):
                timing = self.fixture('## Line 1\n\n    (1) First.\n')
                timing['frames'][0]['units'][0][field] = value
                self.save_timing(timing)
                with self.assertRaisesRegex(ValueError, '시각/비트'):
                    self.convert()
                self.assertFalse((self.lesson / 'SCRIPT.timed.ko.md').exists())


if __name__ == '__main__':
    unittest.main()
