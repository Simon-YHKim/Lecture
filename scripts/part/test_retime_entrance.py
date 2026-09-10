from pathlib import Path
import tempfile
import unittest
import json
import re

from retime_frames import CALL, retime_frame, validate_beats


class IntroductionTimingTests(unittest.TestCase):
    def test_title_remains_visible_through_speech_and_exits_inside_its_clip(self):
        source = '''<div data-composition-id="f" data-duration="16"></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f h2",{opacity:0},{opacity:1,duration:1},2);
tl.fromTo("#f .sub",{opacity:0},{opacity:1,duration:1},6.36);
tl.to("#f .brand,#f .cert,#f h2,#f .rule,#f .sub",{opacity:0,duration:.8},11.05);
'''
        for duration in (8.0, 16.0):
            with self.subTest(duration=duration), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'frame.html'
                path.write_text(source, encoding='utf-8')
                retime_frame(str(path), [], duration)
                result = path.read_text(encoding='utf-8')
                fade = next(m for m in CALL.finditer(result) if m.group('kind') == 'to')
                at = float(fade.group('time'))
                self.assertGreaterEqual(at, duration - 1.6)
                self.assertLessEqual(at + .8, duration)
                for entry in (m for m in CALL.finditer(result) if m.group('kind') == 'fromTo'):
                    reveal = float(re.search(r'duration:([\d.]+)', entry.group('mid'))[1])
                    self.assertLessEqual(float(entry.group('time')) + reveal + 2, at + .01,
                        'Title text needs two seconds to read before its fade starts')
                retime_frame(str(path), [], duration)
                self.assertEqual(path.read_text(encoding='utf-8'), result)

    def test_recap_lists_are_readable_when_their_paragraph_starts(self):
        source = '''<div data-composition-id="f" data-duration="50"></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .p-done",{opacity:0},{opacity:1,duration:1},2);
tl.fromTo("#f .p-done-li",{opacity:0},{opacity:1,duration:.8,stagger:5},2);
tl.fromTo("#f .p-next",{opacity:0},{opacity:1,duration:1},25);
tl.fromTo("#f .p-next-li",{opacity:0},{opacity:1,duration:.8,stagger:5},25);
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'frame.html'
            path.write_text(source, encoding='utf-8')
            spec = path.with_suffix('.motion.json')
            spec.write_text(json.dumps({'duration': 50, 'assertions': []}), encoding='utf-8')
            spans = [(3, 20), (22, 47)]
            retime_frame(str(path), spans, 50)
            result = path.read_text(encoding='utf-8')
            for panel, (on, _) in zip(('p-done', 'p-next'), spans):
                call = next(m for m in CALL.finditer(result)
                            if m.group('sel') == '#f .' + panel + '-li')
                duration = float(re.search(r'duration:([\d.]+)', call.group('mid'))[1])
                stagger = float(re.search(r'stagger:([\d.]+)', call.group('mid'))[1])
                last_visible = float(call.group('time')) + duration + 4 * stagger
                self.assertLessEqual(last_visible, on + 1.0,
                    'Five bullets share one spoken paragraph, not five measured beats')
            retime_frame(str(path), spans, 50)
            self.assertEqual(path.read_text(encoding='utf-8'), result)
            assertions = json.loads(spec.read_text(encoding='utf-8'))['assertions']
            self.assertEqual({a['selector'] for a in assertions},
                {'#f .p-done-li:last-child', '#f .p-next-li:last-child'})
            self.assertEqual(len(assertions), 2)

    def test_sparse_highlights_keep_their_explicit_beat_instead_of_shifting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'frame.html'
            source='''<div data-composition-id="f" data-duration="50"></div>
const tl=gsap.timeline({paused:true});
tl.to("#f [data-feature='fillet']",{stroke:'red',duration:.7},3); // narration-beat: 3 on
tl.to("#f [data-feature='fillet']",{stroke:'black',duration:.7},8); // narration-beat: 3 off
'''
            path.write_text(source,encoding='utf-8')
            retime_frame(str(path),[(2,10),(13,20),(23,30),(33,40)],50)
            result=path.read_text(encoding='utf-8')
            self.assertIn('},23); // narration-beat: 3 on',result)
            self.assertIn('},33); // narration-beat: 3 off',result)
            retime_frame(str(path),[(2,10),(13,20),(23,30),(33,40)],50)
            self.assertEqual(path.read_text(encoding='utf-8'),result)

    def test_narration_entrance_updates_its_motion_deadline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'frame.html'
            path.write_text('''<div data-composition-id="f" data-duration="30"></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .c1",{opacity:0},{opacity:1,duration:1},3);
''', encoding='utf-8')
            spec=path.with_suffix('.motion.json')
            spec.write_text(json.dumps({'duration':30,'assertions':[
                {'kind':'appearsBy','selector':'#f .c1','bySec':5},
                {'kind':'appearsBy','selector':'#f h1','bySec':3}]}),encoding='utf-8')
            retime_frame(str(path),[(10,20)],30)
            assertions=json.loads(spec.read_text(encoding='utf-8'))['assertions']
            self.assertEqual(assertions[0]['bySec'],12.4)
            self.assertEqual(assertions[1]['bySec'],3)
            retime_frame(str(path),[(2,20)],30)
            self.assertEqual(json.loads(spec.read_text(encoding='utf-8'))['assertions'][0]['bySec'],4.4)

    def test_explicit_mixed_selectors_follow_their_named_beats(self):
        html = '''<div data-composition-id="f" data-duration="30"></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .paper",{opacity:0},{opacity:1,duration:1},3);
tl.fromTo("#f .size",{opacity:0},{opacity:1,duration:1},3.4);
tl.fromTo("#f .note1",{opacity:0},{opacity:1,duration:1},18);
tl.to("#f .note1",{opacity:.6,duration:1},22);
// narration-beats: [["#f .paper", "#f .size"], ["#f .note1"]]
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'frame.html'; path.write_text(html, encoding='utf-8')
            retime_frame(str(path), [(6, 12), (15, 27)], 30)
            result = path.read_text(encoding='utf-8')
            self.assertEqual(result.count('duration:1},6);'), 2)
            self.assertIn('duration:1},15);', result)
            self.assertIn('duration:1},27);', result)

    def test_leading_decimal_does_not_swallow_later_caption_calls(self):
        html = '''<div data-composition-id="f" data-duration="30">USER RECORDING</div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .tag",{opacity:0},{opacity:1,duration:.8},.35);
tl.fromTo("#f .strip",{opacity:0,y:26},{opacity:0,y:0,duration:.9},.7);
tl.fromTo("#f .sp1",{opacity:0},{opacity:1,duration:1.1},1.6);
tl.to("#f .sp1",{opacity:0,duration:.8},1.6);
tl.fromTo("#f .sp2",{opacity:0},{opacity:1,duration:1.1},12);
tl.to("#f .sp2",{opacity:0,duration:.8},25);
'''
        self.assertEqual(len(list(CALL.finditer(html))), 6)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'frame.html'; path.write_text(html, encoding='utf-8')
            retime_frame(str(path), [(1.6, 11.5), (12, 25)], 30)
            once = path.read_text(encoding='utf-8')
            self.assertIn('opacity:0,duration:0.18},11.8);', once)
            self.assertNotIn('y:26', once)
            self.assertIn('"#f .strip",{opacity:0,y:0},{opacity:1,y:0', once)
            retime_frame(str(path), [(1.6, 11.5), (12, 25)], 30)
            self.assertEqual(path.read_text(encoding='utf-8'), once)

    def test_invalid_cue_times_are_rejected_before_editing(self):
        for spans in ([(float('nan'), 4)], [(2, float('inf'))], [(4, 3)],
                      [(-1, 2)], [(2, 31)], [(2, 8), (7, 9)]):
            with self.assertRaises(ValueError):
                validate_beats(spans, 30)

    def test_an_early_overview_remains_visible_before_the_first_named_beat(self):
        html = '''<div data-composition-id="f" data-duration="30"></div>
const tl=gsap.timeline({paused:true});
tl.fromTo("#f .rd1,#f .rd2",{opacity:0},{opacity:.5,duration:.5},2);
tl.to("#f .rd1",{opacity:1,duration:.5},10);
tl.to("#f .rd2",{opacity:1,duration:.5},20);
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'frame.html'
            path.write_text(html, encoding='utf-8')
            retime_frame(str(path), [(12, 18), (22, 28)], 30)
            result = path.read_text(encoding='utf-8')
            self.assertIn('duration:.5},2.0);', result)
            self.assertIn('duration:.5},12', result)


if __name__ == '__main__':
    unittest.main()
