# -*- coding: utf-8 -*-
"""복제 음성은 Heami 가 읽던 말을 글자까지 그대로 읽어야 한다.

바깥 엔진에 넘기려고 문단을 토막으로 쪼갠다. 쪼개는 과정에서 한 글자라도 흘리면
선생님 목소리로 **틀린 말**이 나간다. 여기서 지키는 것은 하나다 — 토막을 공백
하나로 이으면 `narrate_tts.synthesis_plan` 이 SAPI 에 보내던 문장이 복원된다.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import narrate_tts as N
import tts_jobs


class ChunkTests(unittest.TestCase):
    def test_chunks_rebuild_the_paragraph_the_engine_was_given(self):
        for lang in ('ko', 'en'):
            _, hard = tts_jobs.SIZE[lang]
            for lesson in tts_jobs.collect(lang):
                src = tts_jobs.COURSE / lesson['slug'] / tts_jobs.SCRIPTS[lang]
                said = dict(N.synthesis_plan(str(src))[0])
                for job in lesson['jobs']:
                    with self.subTest(lesson=lesson['slug'], lang=lang, key=job['key']):
                        self.assertIn(job['key'], said)
                        want = tts_jobs.spoken(said[job['key']])
                        got = ' '.join(c['text'] for c in job['chunks'])
                        self.assertEqual(got, want)
                        self.assertEqual(job['chars'], len(want))
                        # **순환하지 않는 대조.** 위 두 줄은 양쪽이 같은
                        # 함수를 쓰므로 그 함수가 글자를 지워도 통과한다.
                        # 실제로 굵게 표시된 문장이 제어문자 하나로 바뀌었는데
                        # 시험 150개가 전부 통과했다. 그래서 함수를 쓰지 않고
                        # 만든 기대값과 한 번 더 맞춘다.
                        plain = tts_jobs.TAG.sub('', said[job['key']])
                        plain = ' '.join(plain.replace('**', '').split())
                        self.assertEqual(got, plain, '낭독될 글자가 달라졌다')
                        for ch in got:
                            self.assertGreaterEqual(ord(ch), 32, '제어문자가 섞였다')
                        self.assertEqual([c['n'] for c in job['chunks']],
                                         list(range(1, len(job['chunks']) + 1)))
                        for c in job['chunks']:
                            self.assertTrue(c['text'].strip(), '빈 토막')
                            # 공백 없는 한 덩어리는 쪼갤 자리가 없어 넘어갈 수 있다.
                            self.assertTrue(len(c['text']) <= hard or ' ' not in c['text'],
                                            '%d자 토막: %r' % (len(c['text']), c['text'][:60]))

    def test_every_job_of_every_lesson_is_covered(self):
        for lang in ('ko', 'en'):
            got = {(l['slug'], j['key']) for l in tts_jobs.collect(lang) for j in l['jobs']}
            want = set()
            for lesson in sorted(p for p in tts_jobs.COURSE.glob('lesson-*') if p.is_dir()):
                src = lesson / tts_jobs.SCRIPTS[lang]
                if src.is_file():
                    want |= {(lesson.name, k) for k, _ in N.synthesis_plan(str(src))[0]}
            self.assertEqual(got, want)

    def test_no_tag_survives_into_the_spoken_text(self):
        for lang in ('ko', 'en'):
            for lesson in tts_jobs.collect(lang):
                for job in lesson['jobs']:
                    for c in job['chunks']:
                        with self.subTest(lesson=lesson['slug'], lang=lang, key=job['key']):
                            self.assertNotIn('[', c['text'])

    def test_tone_is_one_of_the_named_moods(self):
        for lang in ('ko', 'en'):
            for lesson in tts_jobs.collect(lang):
                for job in lesson['jobs']:
                    self.assertIn(job['tone'], tts_jobs.PRIORITY)


if __name__ == '__main__':
    unittest.main()
