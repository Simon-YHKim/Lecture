# -*- coding: utf-8 -*-
"""태그본은 말을 바꾸지 않는다.

음성 복제 서비스가 읽는 것은 이 파일이다. 생성기가 문장을 하나 흘리거나 순서를
바꾸면 선생님 목소리로 **틀린 말**이 나간다. 태그만 걷어내면 원본과 글자까지
같아야 한다 — 그것만 지키면 나머지는 태그말의 취향 문제다.
"""
import os
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import beats
import tts_script

COURSE = HERE.parents[1] / 'projects' / 'autocad-technician'
TAG = re.compile(r'\[[^\[\]]{1,12}\]\s*')


def pairs():
    for lesson in sorted(p for p in COURSE.glob('lesson-*') if p.is_dir()):
        for name, lang in (('SCRIPT.md', 'ko'), ('SCRIPT.en.md', 'en')):
            src = lesson / name
            tagged = lesson / ('SCRIPT.tts.%s.md' % lang)
            if src.is_file() and tagged.is_file():
                yield lesson.name, lang, src, tagged


class TaggedScriptTests(unittest.TestCase):
    def test_every_script_has_a_tagged_twin(self):
        found = {(name, lang) for name, lang, _, _ in pairs()}
        want = set()
        for lesson in sorted(p for p in COURSE.glob('lesson-*') if p.is_dir()):
            for name, lang in (('SCRIPT.md', 'ko'), ('SCRIPT.en.md', 'en')):
                if (lesson / name).is_file():
                    want.add((lesson.name, lang))
        self.assertEqual(found, want)

    def test_stripping_the_tags_gives_the_script_back(self):
        for name, lang, src, tagged in pairs():
            want = beats.parse_script(str(src))
            got = beats.parse_script(str(tagged))
            with self.subTest(lesson=name, lang=lang):
                self.assertEqual(sorted(want), sorted(got))
                for line_no in want:
                    self.assertEqual(
                        [(key, TAG.sub('', text).strip()) for key, text in got[line_no]],
                        [(key, text.strip()) for key, text in want[line_no]],
                        'Line %d 의 말이 달라졌다' % line_no)

    def test_the_recording_steps_survive(self):
        """단계 제목과 그 안의 조작 줄이 그대로여야 녹화가 대본을 따라갈 수 있다."""
        for name, lang, src, tagged in pairs():
            demo = 8 if 'lesson-02' in name and lang == 'ko' else None
            for line_no in beats.parse_script(str(src)):
                want = beats.parse_steps(str(src), line_no)
                if not want:
                    continue
                got = beats.parse_steps(str(tagged), line_no)
                with self.subTest(lesson=name, lang=lang, line=line_no):
                    self.assertEqual([n for n, _ in want], [n for n, _ in got])
                    self.assertEqual([TAG.sub('', t).strip() for _, t in got],
                                     [t.strip() for _, t in want])
            del demo

    def test_screen_markers_and_silence_keep_no_tag(self):
        """화면 표식과 (무음) 은 읽히지 않는다. 태그가 붙으면 엔진이 읽어 버린다."""
        for name, lang, _src, tagged in pairs():
            for line_no, segs in beats.parse_script(str(tagged)).items():
                for key, text in segs:
                    if key is None and not text.startswith('('):
                        continue
                    with self.subTest(lesson=name, lang=lang, line=line_no):
                        self.assertFalse(text.startswith('['), text[:40])

    def test_tag_words_come_from_the_fixed_set(self):
        for name, lang, _src, tagged in pairs():
            allowed = set(tts_script.TAGS[lang].values())
            source = tagged.read_text(encoding='utf-8')
            body = source.split('-->', 1)[1] if '-->' in source else source
            for word in re.findall(r'\[([^\[\]]{1,12})\]', body):
                with self.subTest(lesson=name, lang=lang, tag=word):
                    self.assertIn(word, allowed)


if __name__ == '__main__':
    unittest.main()
