"""Context pages retain every action while removing unnecessary slide breaks."""
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import build_deck_frames as frames
import build_deck_selfstudy as deck


class DeckGroupingTests(unittest.TestCase):
    def step(self, count=10):
        return {'n': 1, 'title': {'ko': '선을 그리고 확인합니다'},
                'actions': [{'type': str(i), 'kind': 'type',
                             'do': {'ko': '입력하고 엔터를 누릅니다.'}} for i in range(count)],
                'spots': [{'x': 0, 'y': 0, 'snap': 'end', 'hover': {'ko': '끝점'}}],
                'expect': {'ko': '선이 남습니다.'}, 'why': {'ko': '기준을 잡습니다.'},
                'pitfall': {'ko': '끝점 표식을 다시 확인합니다.'}}

    def test_readable_command_context_stays_on_one_page(self):
        st = self.step()
        with patch.object(deck, 'fig_block', return_value='<figure class="fig"></figure>'):
            made = deck.step_slide(st, 'demo', 0, '작도', 1, {'front': '<svg/>'})
        self.assertEqual(len(made), 1)
        html, _, manifest, _ = made[0]
        self.assertEqual(manifest['sourceActions'], list(range(1, 11)))
        self.assertEqual(len(manifest['fragments']), 1)
        self.assertIn('font-size:28px', html)
        self.assertIn('<div class="guide"><figure', html)
        self.assertIn(st['pitfall']['ko'], manifest['notes'])

    def test_pages_keep_action_order_and_original_memo_numbers(self):
        st = self.step(27)
        with patch.object(deck, 'fig_block', return_value='<figure class="fig"></figure>'):
            made = deck.step_slide(st, 'demo', 0, '작도', 1, {'front': '<svg/>'})
        self.assertGreater(len(made), 1)
        self.assertEqual([n for _, _, m, _ in made for n in m['sourceActions']], list(range(1, 28)))
        self.assertEqual([int(n) for html, _, _, _ in made
                          for n in re.findall(r'data-action="(\d+)"', html)], list(range(1, 28)))
        self.assertEqual(len({m['sceneId'] for _, _, m, _ in made}), len(made))

    def test_question_and_answer_are_not_separated_at_page_end(self):
        acts = self.step(11)['actions']
        acts[10] = {'kind': 'ask', 'do': {'ko': '거리를 입력하라는 질문입니다.'}}
        acts.append({'type': '120', 'do': {'ko': '입력하고 엔터를 누릅니다.'}})
        acts += self.step(8)['actions']
        pages = deck.action_pages(acts, narrow=True)
        self.assertEqual([a for page in pages for a in page], acts)
        self.assertTrue(all(page[-1].get('kind') != 'ask' for page in pages[:-1]))

    def test_oversized_single_action_fails_instead_of_clipping(self):
        with self.assertRaisesRegex(ValueError, 'One action exceeds'):
            deck.action_pages([{'do': {'ko': '설명을 확인합니다. ' * 100}}], narrow=True)

    def test_course_actions_all_fit_and_survive_grouping(self):
        for path in sorted((Path(__file__).parent / 'source').glob('lesson-??.json')):
            lesson = json.loads(path.read_text(encoding='utf-8'))
            for sec in lesson['sections']:
                for block in sec.get('blocks', []):
                    if block['type'] != 'steps':
                        continue
                    for st in block['items']:
                        with self.subTest(lesson=lesson['no'], step=st['n']):
                            has_fig = bool(st.get('spots') or st.get('construction'))
                            pages = deck.action_pages(st['actions'], has_fig)
                            self.assertEqual([a for page in pages for a in page], st['actions'])
                            for page in pages:
                                size, height, cap = deck.ops_font(page, has_fig)
                                self.assertEqual(size, 28)
                                self.assertLessEqual(height, cap)

    def test_temporary_geometry_and_focus_reach_the_same_figure(self):
        st = self.step(2)
        st['focus'] = {'view': 'front', 'bounds': [0, 0, 120, 20]}
        st['construction'] = [{'kind': 'line', 'points': [[0, 16], [120, 16]],
                               'role': 'before'}]
        fig = deck.fig_block(st['spots'], deck.surfaces(), step=st)
        self.assertIn('class="construction" data-role="before"', fig)
        self.assertIn('점선: 이 단계의 임시선', fig)
        self.assertIn('viewBox="%s"' % deck._coach.figure_viewbox(
            st, 'front', deck.surfaces()['front']), fig)
        self.assertLess(fig.index('<use'), fig.index('class="construction"'))
        self.assertLess(fig.index('class="construction"'), fig.index('<g class="coach"'))

    def test_separate_practice_diagram_does_not_show_the_finished_part(self):
        st = self.step(2)
        st.pop('spots')
        st['diagramOnly'] = True
        st['focus'] = {'view': 'front', 'bounds': [0, 0, 40, 30]}
        st['construction'] = [{'kind': 'line', 'points': [[0, 0], [40, 0]],
                               'role': 'practice'}]
        html = deck.step_slide(st, 'temporary', 0, '연습', 1, deck.surfaces())[0][0]
        self.assertIn('이 단계의 작도 도해', html)
        self.assertIn('class="construction"', html)
        self.assertNotIn('<use', html)

    def test_legacy_command_uses_the_same_builder(self):
        with patch.object(deck, 'main', return_value=0) as main:
            self.assertEqual(frames.main('lesson-02-part-and-template', 'out.html'), 0)
        self.assertEqual(main.call_args.args[0], 'lesson-02-part-and-template')
        self.assertTrue(main.call_args.args[1].endswith('lesson-02.json'))
        self.assertEqual(main.call_args.args[2], 'out.html')


if __name__ == '__main__':
    unittest.main()
