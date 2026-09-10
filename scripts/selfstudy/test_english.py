"""학습자에게 나가는 영문에 한글이 남거나 용어가 흔들리면 실패한다."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_english


class EnglishEditionTests(unittest.TestCase):
    def files(self):
        return sorted(p.name for p in (HERE / 'source').glob('*.json'))

    def test_no_open_violation_outside_the_pending_list(self):
        open_rows = [row for row in check_english.check(self.files())
                     if (row[0], row[1]) not in check_english.PENDING]
        self.assertEqual(open_rows, [])

    def test_pending_entries_still_exist(self):
        """고쳐진 자리가 목록에 남아 있으면 목록이 썩는다. 지우도록 실패시킨다."""
        found = {(row[0], row[1]) for row in check_english.check(self.files())}
        self.assertEqual(check_english.PENDING - found, set())

    def test_checker_catches_a_planted_violation(self):
        rows = [
            ('한글 잔존', {'ko': '외형선을 그립니다', 'en': '외형선을 그립니다'}),
            ('outline layer', {'ko': '외형선 레이어', 'en': 'Switch to the outline layer'}),
            ('center line', {'ko': '중심선', 'en': 'Draw the center line'}),
            ('third angle', {'ko': '제3각법', 'en': 'in third angle projection'}),
            ('oblong', {'ko': '장공', 'en': 'the oblong hole on the base'}),
        ]
        for label, node in rows:
            with self.subTest(case=label):
                found = check_english.violations('t.json', '/x', node['ko'], node['en'])
                self.assertTrue(found, 'planted %s went unnoticed' % label)

    def test_shape_words_are_not_mistaken_for_the_layer_name(self):
        clean = [
            'Draw the base outline first, then the web.',
            'Does the bolt circle look like a solid line?',
            'That template is the millimetre one. An inch template is wrong.',
            'The prompt reads "Dist1 = 0.0000".',
        ]
        for text in clean:
            with self.subTest(text=text[:32]):
                self.assertEqual(check_english.violations('t.json', '/x', '보기', text), [])

    def test_figure_text_is_paired(self):
        """도해의 한글 글자마다 같은 자리에 영문 글자가 있어야 한다."""
        svg = ('<svg viewBox="0 0 10 10">'
               '<text class="a k" x="1" y="1">외형선</text>'
               '<text class="a e" x="1" y="1">visible line</text></svg>')
        self.assertEqual(check_english.figure_rows(svg, 't.json', '/x'), [])

    def test_unpaired_figure_text_is_caught(self):
        svg = '<svg viewBox="0 0 10 10"><text x="1" y="1">외형선</text></svg>'
        self.assertTrue(check_english.figure_rows(svg, 't.json', '/x'))

    def test_duplicated_class_attribute_is_caught(self):
        """`class` 가 두 번이면 파서가 뒤엣것을 버려 짝이 무효가 된다."""
        svg = ('<svg viewBox="0 0 10 10">'
               '<text class=\'a\' x="1" class="k">외형선</text>'
               '<text class=\'a\' x="1" class="e">visible line</text></svg>')
        found = check_english.figure_rows(svg, 't.json', '/x')
        self.assertEqual(len(found), 2)

    def test_source_files_stay_valid_json(self):
        for name in self.files():
            with self.subTest(file=name):
                json.loads((HERE / 'source' / name).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
