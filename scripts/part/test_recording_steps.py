"""Prevent recording overlays drifting from the lesson's actual spoken steps."""
from pathlib import Path
import html
import json
import re
import tempfile
import unittest

import beats

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'projects/autocad-technician/lesson-07-dimensioning-release'


class ShortcutContextTests(unittest.TestCase):
    def commands(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'SCRIPT.md'
            path.write_text('## Line 5 — 녹화\n' + text, encoding='utf-8', newline='\n')
            return beats.shortcuts_in(path, 5)

    def step_commands(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'SCRIPT.md'
            body = '\n'.join('    ' + row for row in text.splitlines())
            path.write_text('## Line 5 — 녹화\n### 1단계 — 연습\n' + body,
                            encoding='utf-8', newline='\n')
            return beats.step_keys(path, 5)[0]

    def test_rectangle_fillet_option_is_not_a_fillet_command(self):
        for row in (
            '다시 첫 구석점을 물으면 `F` 엔터, 반지름 `0` 엔터입니다.',
            '`F` 엔터. RECTANG의 Fillet 옵션 반지름에 0을 넣습니다.',
            '`F` 엔터. 사각형 모깎기 옵션입니다.',
        ):
            with self.subTest(row=row):
                self.assertNotIn('F', self.commands('`REC` 엔터.\n' + row))

    def test_real_fillet_and_long_system_variable_are_collected(self):
        for row in ('`F` 입력하고 엔터. 모깎기입니다.',
                    '`F` 엔터. FILLET 명령입니다.',
                    '`F` 엔터. 필렛 명령을 시작합니다.'):
            with self.subTest(row=row):
                self.assertIn('F', self.commands(row))
        self.assertEqual(self.commands('`TRIMEXTENDMODE` 엔터, `0` 엔터.'), ['TRIMEXTENDMODE'])

    def test_current_rectangle_and_fillet_recordings_keep_distinct_keys(self):
        course = ROOT / 'projects/autocad-technician'
        for slug, expected in (('lesson-03-baseline-profile', False), ('lesson-04-circles-arcs', True)):
            text = (course / slug / 'SCRIPT.md').read_text(encoding='utf-8')
            recording = text.split('## Line 5', 1)[1].split('## Line 6', 1)[0]
            f_rows = '\n'.join(row for row in recording.splitlines() if '`F`' in row)
            self.assertTrue(f_rows, slug)
            self.assertEqual('F' in self.commands(f_rows), expected, slug)

    def test_step_label_drops_fillet_option_but_keeps_repeated_command(self):
        for option in ('다시 첫 구석점을 물으면 `F` 엔터, 반지름 `0` 엔터입니다.',
                       '`F` 엔터. RECTANG의 Fillet 옵션 반지름에 0을 넣습니다.'):
            with self.subTest(option=option):
                self.assertEqual(self.step_commands(option), '')
        self.assertEqual(self.step_commands('`F` 입력하고 엔터. 반지름은 10으로 기억되어 있어요.'), 'F')

    def test_mixed_step_classifies_each_f_occurrence_in_order(self):
        option = '다시 첫 구석점을 물으면 `F` 엔터, 반지름 `0` 엔터입니다.'
        command = '`F` 엔터. 모깎기입니다.'
        for separator in ('.', ';'):
            option_first = (option + ' `XL` 엔터. ' + command).replace('.', separator)
            command_first = (command + ' `XL` 엔터. ' + option).replace('.', separator)
            with self.subTest(separator=separator):
                self.assertEqual(self.step_commands(option_first), 'XL · F')
                self.assertEqual(self.step_commands(command_first), 'F · XL')
                self.assertEqual(self.commands(option_first), ['XL', 'F'])
                self.assertEqual(self.commands(command_first), ['F', 'XL'])

    def test_current_step_labels_exclude_rectangle_f_and_keep_both_fillets(self):
        course = ROOT / 'projects/autocad-technician'
        rectangle = beats.step_keys(course / 'lesson-03-baseline-profile/SCRIPT.md', 5)
        self.assertFalse(any('F' in label.split(' · ') for label in rectangle))
        fillets = beats.step_keys(course / 'lesson-04-circles-arcs/SCRIPT.md', 5)
        for number in (13, 14):
            self.assertIn('F', fillets[number - 1].split(' · '))

    def test_circle_options_do_not_claim_a_circle_command(self):
        for option in ('`C` 엔터, 첫 거리 `0` 엔터, 둘째 거리 `0` 엔터입니다.',
                       '`C` 엔터. RECTANG의 모따기 옵션입니다.',
                       '마지막으로 `C` 입력하고 엔터. 시작점까지 닫으면서 명령이 끝납니다.',
                       '원본으로 할지 현재로 할지 물어봅니다. `C` 입력하고 엔터. 현재 레이어에 넣습니다.'):
            with self.subTest(option=option):
                self.assertNotIn('C', self.commands(option))
                self.assertEqual(self.step_commands(option), '')
        for command in ('`C` 입력하고 엔터. 원 명령입니다.',
                        '`C` 입력하고 엔터. 중심점을 물어봅니다.',
                        '`C` 엔터. 교차점을 클릭합니다. 반지름 `5` 엔터입니다.'):
            with self.subTest(command=command):
                self.assertEqual(self.commands(command), ['C'])
                self.assertEqual(self.step_commands(command), 'C')

    def test_circle_first_use_order_ignores_options_in_mixed_step(self):
        text = ('`C` 엔터, 첫 거리 `0` 엔터, 둘째 거리 `0` 엔터입니다. '
                '`XL` 엔터. `C` 엔터. 원 명령입니다. '
                '마지막으로 `C` 엔터. 시작점까지 닫습니다.')
        self.assertEqual(self.commands(text), ['XL', 'C'])
        self.assertEqual(self.step_commands(text), 'XL · C')

    def test_offset_layer_option_is_not_line(self):
        text = '`O` 엔터. `L` 입력하고 엔터. 도면층 옵션입니다.'
        self.assertEqual(self.commands(text), ['O'])
        self.assertEqual(self.step_commands(text), 'O')
        mixed = text + ' `C` 엔터. 원 명령입니다. `L` 엔터. LINE 명령입니다.'
        self.assertEqual(self.commands(mixed), ['O', 'C', 'L'])

    def test_current_circle_command_order_and_close_only_lesson(self):
        course = ROOT / 'projects/autocad-technician'
        path = course / 'lesson-03-baseline-profile/SCRIPT.md'
        commands = beats.shortcuts_in(path, 5)
        self.assertGreater(commands.index('C'), commands.index('XL'))
        self.assertEqual(beats.step_keys(path, 5)[3], 'REC')
        path = course / 'lesson-05-three-views/SCRIPT.md'
        self.assertNotIn('C', beats.shortcuts_in(path, 5))
        self.assertFalse(any('C' in label.split(' · ') for label in beats.step_keys(path, 5)))
        path = course / 'lesson-04-circles-arcs/SCRIPT.md'
        commands = beats.shortcuts_in(path, 5)
        self.assertGreater(commands.index('L'), commands.index('DSETTINGS'))
        self.assertEqual(beats.step_keys(path, 5)[2], 'O · Ctrl+1')


class RecordingStepTests(unittest.TestCase):
    def test_lesson_three_move_is_in_spoken_command_recap(self):
        path = ROOT / 'projects/autocad-technician/lesson-03-baseline-profile/SCRIPT.md'
        self.assertIn('M', beats.shortcuts_in(path, 5))
        recap = path.read_text(encoding='utf-8').split('## Line 8', 1)[1].split('## Line 9', 1)[0]
        self.assertIn('`M`. MOVE.', recap)

    def test_lesson_seven_derived_steps_and_overlays_follow_script(self):
        script = (PROJECT / 'SCRIPT.md').read_text(encoding='utf-8')
        headings = re.findall(r'^### (\d+)단계 — (.+)$', script, re.M)
        self.assertEqual([int(n) for n, _ in headings], list(range(1, 18)))
        derived = json.loads((ROOT / 'scripts/part/lesson_data_3_7.json').read_text(encoding='utf-8'))
        self.assertEqual(derived['7']['data']['steps'], [title for _, title in headings])
        counts = []
        labels = []
        for suffix in 'abc':
            text = (PROJECT / f'compositions/frames/05-demo-{suffix}.html').read_text(encoding='utf-8')
            numbers = re.findall(r'<span class="no">(\d+)<i>&#8201;/&#8201;(\d+)</i>', text)
            labels += [(int(n), int(total)) for n, total in numbers]
            titles = re.findall(r'<span class="what">(.*?)</span></div>', text)
            plain = [html.unescape(re.sub(r'<[^>]*>', '', t)) for t in titles]
            start = sum(counts)
            self.assertEqual(plain, [title for _, title in headings[start:start + len(numbers)]])
            counts.append(len(numbers))
        self.assertEqual(counts, [5, 9, 3])
        self.assertEqual(labels, [(n, 17) for n in range(1, 18)])


if __name__ == '__main__':
    unittest.main()
