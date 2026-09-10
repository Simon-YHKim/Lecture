from pathlib import Path
import re
import tempfile
import unittest

import beats
import retime_frames


def calls(source):
    return list(retime_frames.CALL.finditer(source))


class RowReadabilityTests(unittest.TestCase):
    def test_row_default_is_opaque_without_changing_other_items(self):
        self.assertEqual(beats.item('.row', kind='row')['read'], 1)
        self.assertEqual(beats.item('.card')['read'], beats.READ)
        self.assertEqual(beats.item('.plain', kind='plain')['read'], beats.READ)
        self.assertEqual(beats.item('.row', kind='row', read=0)['read'], 0)

    def test_mixed_overview_runs_preserve_original_stagger_positions(self):
        items = [beats.item('.r1', kind='row'), beats.item('.r2', kind='row'),
                 beats.item('.note1'), beats.item('.r3', kind='row'),
                 beats.item('.note2', kind='plain')]
        spans = [(i + 1, 10 + i * 10, 18 + i * 10) for i in range(5)]
        source = beats.read_along('f', items, spans, group_stagger=.2)
        overview = [m for m in calls(source) if m['kind'] == 'fromTo']
        self.assertEqual([m['sel'] for m in overview],
                         ['#f .r1,#f .r2', '#f .note1', '#f .r3', '#f .note2'])
        self.assertEqual([float(m['time']) for m in overview], [7.6, 8.0, 8.2, 8.4])
        for m, opacity in zip(overview, (1, beats.UNREAD, 1, beats.UNREAD)):
            self.assertEqual(float(re.search(r'\},\{opacity:([\d.]+)', m['mid'])[1]), opacity)
            self.assertIn('duration:0.95,stagger:0.2', m['mid'])

    def test_row_background_emphasis_and_explicit_stacked_zero_remain(self):
        source = beats.read_along('f', [beats.item('.r1', kind='row')], [(1, 10, 18)])
        states = calls(source)
        self.assertIn('},{opacity:1', states[0]['mid'])
        self.assertIn("opacity:1.0,backgroundColor:'#F5F5F3',duration:0.8", states[1]['mid'])
        self.assertIn("opacity:1,backgroundColor:'rgba(0,0,0,0)',duration:0.8", states[2]['mid'])
        self.assertEqual([float(m['time']) for m in states], [7.6, 10, 18])
        stacked = beats.read_along('f', [beats.item('.r1', kind='row', mode='reveal', read=0)], [(1, 10, 18)])
        self.assertIn('duration:0.25', stacked)
        self.assertIn('opacity:0,backgroundColor:', stacked)
        self.assertIn('duration:0.18', stacked)
        self.assertEqual(float(calls(stacked)[-1]['time']), 17.8)

    def test_existing_html_changes_only_actual_rows_and_keeps_call_timing(self):
        source = '''<div id="f" data-composition-id="f" data-duration="30">
<table><tr class="r1"><td><span class="child">row</span></td></tr><tr class="r2"><td>row</td></tr></table>
<div class="note1">note</div><svg><path class="shape1"/></svg></div><div class="r1">outside</div>
<script>const tl=gsap.timeline({paused:true});
tl.fromTo("#f .r1,#f .r2",{opacity:0},{opacity:0.34,duration:.95,stagger:.1},1);
tl.to("#f .r1",{opacity:0.64,backgroundColor:'rgba(0,0,0,0)',duration:.8},10);
tl.to("#f .r2",{opacity:0,duration:.8},18);
tl.to("#f .note1",{opacity:0.64,duration:.8},10);
tl.to("#f .shape1",{opacity:0.34,duration:.8},10);
tl.to("#f .r1 .child",{opacity:0.64,duration:.8},10);
</script>'''
        fixed = retime_frames.fix_row_readability(source)
        before, after = calls(source), calls(fixed)
        self.assertEqual([(m['sel'], m['time']) for m in before], [(m['sel'], m['time']) for m in after])
        self.assertIn('},{opacity:1,duration:.95,stagger:.1}', after[0]['mid'])
        self.assertIn("opacity:1,backgroundColor:'rgba(0,0,0,0)',duration:.8", after[1]['mid'])
        for i in (2, 3, 4, 5):
            self.assertEqual(before[i].group(0), after[i].group(0))
        self.assertEqual(retime_frames.fix_row_readability(fixed), fixed)

    def test_existing_mixed_group_preserves_stagger_and_nonrow_opacity(self):
        source = '''<div id="f"><table><tr class="r1"><td>row</td></tr></table><div class="note1">note</div></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .r1,#f .note1",{opacity:0},{opacity:.34,duration:.95,stagger:.2},7.6);
'''
        fixed = retime_frames.fix_row_readability(source)
        self.assertEqual(len(calls(fixed)), 1)
        call = calls(fixed)[0]
        self.assertEqual(call['sel'], '#f .r1,#f .note1')
        self.assertEqual(call['time'], '7.6')
        self.assertIn('duration:.95,stagger:.2', call['mid'])
        self.assertIn("target.tagName==='TR'?1:.34", call['mid'])
        self.assertEqual(retime_frames.fix_row_readability(fixed), fixed)

    def test_retime_applies_readability_without_repeated_visual_changes(self):
        source = '''<div id="f" data-composition-id="f" data-duration="30"><table><tr class="r1"><td>row</td></tr></table></div>
const tl=gsap.timeline({paused:true});
tl.to("#f .r1",{opacity:1,backgroundColor:'#F5F5F3',duration:.8},5);
tl.to("#f .r1",{opacity:.64,backgroundColor:'rgba(0,0,0,0)',duration:.8},18);
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'frame.html'
            path.write_text(source, encoding='utf-8')
            retime_frames.retime_frame(str(path), [(5, 18)], 30)
            once = path.read_text(encoding='utf-8')
            self.assertNotIn('opacity:.64', once)
            self.assertEqual([float(m['time']) for m in calls(once)], [5, 18])
            retime_frames.retime_frame(str(path), [(5, 18)], 30)
            self.assertEqual(path.read_text(encoding='utf-8'), once)


if __name__ == '__main__':
    unittest.main()
