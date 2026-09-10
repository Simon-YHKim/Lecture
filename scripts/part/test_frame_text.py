"""프레임 글자를 뽑고 갈아 끼우는 규칙을 지킨다."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COURSE = ROOT / 'projects' / 'autocad-technician'
sys.path.insert(0, str(HERE))
import frame_text


class FrameTextTests(unittest.TestCase):
    def test_sentence_with_emphasis_is_one_unit(self):
        """강조를 품은 문장을 쪼개면 영어 어순이 무너진다."""
        html = '<div><p>설비 앞에서 <b>누가 읽어도 같게</b> 만드는 수단입니다.</p></div>'
        self.assertEqual(frame_text.runs(html),
                         ['설비 앞에서 누가 읽어도 같게 만드는 수단입니다.'])

    def test_block_children_split_units(self):
        html = '<div><p>첫째 문장.</p><p>둘째 문장.</p></div>'
        self.assertEqual(frame_text.runs(html), ['첫째 문장.', '둘째 문장.'])

    def test_void_tag_does_not_break_pairing(self):
        """`<br>` 은 닫는 태그가 없다. 쌓아 두면 그 뒤가 전부 어긋난다."""
        html = '<div><p>앞줄<br>뒷줄</p><p>다음 문단</p></div>'
        self.assertEqual(frame_text.runs(html), ['앞줄뒷줄', '다음 문단'])

    def test_kw_spans_and_entities_do_not_change_the_key(self):
        html = '<p><span class="kw">도면은</span>&nbsp;<span class="kw">말입니다</span></p>'
        self.assertEqual(frame_text.runs(html), ['도면은 말입니다'])

    def test_script_and_style_are_ignored(self):
        html = '<div><style>/* 주석 */</style><script>var x="한글";</script><p>본문</p></div>'
        self.assertEqual(frame_text.runs(html), ['본문'])

    def test_localise_touches_only_the_unit(self):
        html = '<div class="a"><p class="b">본문입니다</p><span>ASCII</span></div>'
        out, missing = frame_text.localise(html, {'본문입니다': 'This is the body'})
        self.assertEqual(missing, [])
        self.assertEqual(out, '<div class="a"><p class="b">This is the body</p><span>ASCII</span></div>')

    def test_missing_translation_is_reported_and_nothing_changes(self):
        html = '<p>옮기지 않은 문장</p>'
        out, missing = frame_text.localise(html, {})
        self.assertEqual(out, html)
        self.assertEqual(missing, ['옮기지 않은 문장'])

    def test_every_map_covers_its_lesson(self):
        """지도가 있는 차시는 빠짐없이 덮어야 한다. 빠지면 영문판에 한글이 남는다."""
        maps = sorted((HERE / 'frames_en').glob('lesson-*.json'))
        self.assertTrue(maps, '프레임 영문 지도가 하나도 없다')
        for path in maps:
            lesson = COURSE / path.stem
            with self.subTest(lesson=path.stem):
                self.assertTrue(lesson.is_dir())
                english = json.loads(path.read_text(encoding='utf-8'))
                missing = []
                for frame in frame_text.frames(str(lesson)):
                    source = Path(frame).read_text(encoding='utf-8')
                    for text in frame_text.runs(source):
                        if text not in english:
                            missing.append(text)
                self.assertEqual(missing, [])
                self.assertEqual([k for k, v in english.items() if not v.strip()], [])


if __name__ == '__main__':
    unittest.main()
