"""영문 대본은 국문 대본과 같은 뼈대 위에 서야 한다.

화면과 음성은 문단 단위로 묶인다. 문단이 하나라도 늘거나 줄면 그 차시의 강조
시점이 통째로 밀린다. 그래서 영문 대본은 번역이기 이전에 **같은 구조**여야
한다 — 같은 Line, 같은 문단 수, 같은 비트 번호.

영문 대본이 없는 차시는 아직 만들지 않은 것이므로 검사하지 않는다.
"""
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COURSE = ROOT / 'projects' / 'autocad-technician'
sys.path.insert(0, str(HERE))
import beats

HANGUL = re.compile(r'[가-힣]')


def editions():
    for korean in sorted(COURSE.glob('lesson-*/SCRIPT.md')):
        english = korean.with_name('SCRIPT.en.md')
        if english.exists():
            yield korean, english


class ScriptEditionTests(unittest.TestCase):
    def test_at_least_one_english_script_exists(self):
        self.assertTrue(list(editions()), '영문 대본이 하나도 없다')

    def test_same_lines_paragraphs_and_beats(self):
        for korean, english in editions():
            ko = beats.parse_script(str(korean))
            en = beats.parse_script(str(english))
            with self.subTest(lesson=korean.parent.name):
                self.assertEqual(sorted(ko), sorted(en))
                for line_no in ko:
                    self.assertEqual([key for key, _ in ko[line_no]],
                                     [key for key, _ in en[line_no]],
                                     'Line %d 의 비트 번호가 다르다' % line_no)

    def test_english_script_carries_no_korean(self):
        for _, english in editions():
            with self.subTest(lesson=english.parent.name):
                found = HANGUL.findall(english.read_text(encoding='utf-8'))
                self.assertEqual(found, [])

    def test_english_paragraphs_are_not_empty(self):
        for _, english in editions():
            for line_no, segs in beats.parse_script(str(english)).items():
                for index, (_, text) in enumerate(segs):
                    with self.subTest(lesson=english.parent.name, line=line_no, para=index):
                        self.assertTrue(text.strip())


if __name__ == '__main__':
    unittest.main()
