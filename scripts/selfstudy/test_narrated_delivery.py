"""Regressions for native audio, private metadata and multi-slide exports."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import wave

from narrated_delivery import assemble, capture_state, public_manifest, shot_starts, timestamp
from prepare_narrated import manifest_of, replace_manifest, write_json
from render_narrated import quote_concat
import build_deck_selfstudy as deck


class NarratedDeliveryTests(unittest.TestCase):
    def test_short_and_late_beats_keep_their_own_picture(self):
        self.assertEqual(shot_starts('reuse',[.5,1.5,9.5],10),[0,1.5,9.5])

    def test_generated_figure_description_escapes_attribute_quotes(self):
        text='A "quoted" description, <> and Ø25.'
        made=deck.concept_slide({'label':{'ko':'검사','en':'Check'},'blocks':[{'type':'figure',
             'svg':'<svg></svg>','alt':{'ko':text,'en':text},'caption':{'ko':'설명','en':'Description'}}]},'fixture',0)
        self.assertIn('&quot;quoted&quot;',made[0][0])
        self.assertEqual(made[0][2]['notes'],text)
    def test_figure_notes_use_the_selected_description_not_hidden_svg_languages(self):
        page=[('fig',['<figure data-narration="Diameter &lt;&gt;, Ø25."><svg>'
                      '<text>국문 숨은 레이어</text><text>English layer</text></svg></figure>'])]
        self.assertEqual(deck.part_notes({},page,0,''),'Diameter <>, Ø25.')

    def test_concept_capture_includes_last_card_and_figure_entrance(self):
        self.assertEqual(capture_state('generate',0,[1,2,3,4,5,6],6),6)
        self.assertEqual(capture_state('generate',0,[1],1),1)

    def test_title_capture_skips_staggered_intro_without_seeking_outro(self):
        self.assertGreater(capture_state('reuse',0,[],12.975),7.36)
        self.assertLess(capture_state('reuse',0,[],12.975),11.92)

    def test_embedded_script_cannot_close_its_json_island(self):
        value={'slides':[{'notes':'Enter <> then </script><script>alert(1)</script>'}]}
        doc='<script type="application/hyperframes-slideshow+json">{}</script>'
        result=replace_manifest(doc,value)
        self.assertEqual(manifest_of(result),value)
        self.assertEqual(result.count('</script>'),1)

    def test_private_audio_paths_do_not_enter_downloaded_deck(self):
        private={'slides':[{'sceneId':'one','notes':'Narration','audio':{'path':'private/voice.wav'}}]}
        self.assertNotIn('private',json.dumps(public_manifest(private)))
        self.assertIn('audio',private['slides'][0])

    def test_concat_path_escapes_apostrophe(self):
        quoted=quote_concat(Path(tempfile.gettempdir())/"a'b.png")
        self.assertIn("'\\''",quoted)

    def test_assembly_keeps_native_pcm_and_moves_captions_with_slides(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            audio=root/'original.wav'
            pcm=b'\x10\x01'*2400
            with wave.open(str(audio),'wb') as f:
                f.setparams((1,2,24000,0,'NONE','not compressed'));f.writeframes(pcm)
            gsap=root/'gsap.js';gsap.write_text('/* fixture */')
            slides=[]
            for n in range(2):
                slides.append({'sceneId':'scene%d'%n,'notes':'Enter <>. Diameter Ø25.',
                               'audio':{'mode':'reuse','path':str(audio),'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
                                        'duration':.1,'cues':[{'start':0,'end':.1,'text':'Enter <>. Diameter Ø25.'}]}})
            plan={'slides':slides,'language':'en','lessons':[{'no':1,'title':'Test','at':1,'count':2}]}
            plan_path=root/'plan.json';write_json(plan_path,plan)
            raw=root/'raw.html'
            raw.write_text('<html><head><script src="https://cdn.jsdelivr.net/npm/gsap/x.js"></script></head><body>'
                           '<script type="application/hyperframes-slideshow+json">{}</script>'
                           +''.join('<div data-composition-id="scene%d" data-start="%d" data-duration="10"></div>'%(n,n*10) for n in range(2))
                           +'</body></html>')
            write_json(root/'projects-en.json',[{'lang':'en','lesson':1,'slug':'lesson-01','plan':str(plan_path),
                'raw':str(raw),'gsap':str(gsap),'slides':2}])
            assemble(root,'en')
            built=json.loads((root/'assembled/en/L01.json').read_text())
            self.assertEqual(built['slides'],2)
            self.assertEqual(built['shots'][0]['state'],6.5)
            self.assertAlmostEqual(built['cues'][1]['start'],.9)
            self.assertAlmostEqual(built['duration'],1.8)
            with wave.open(built['audio'],'rb') as f:
                output=f.readframes(f.getnframes())
            self.assertEqual(output[:len(pcm)],pcm)
            self.assertEqual(output[43200:43200+len(pcm)],pcm)
            downloaded=Path(built['package'])/(built['stem']+'.html')
            doc=downloaded.read_text(encoding='utf-8')
            self.assertNotIn(str(root),doc)
            self.assertEqual(len(manifest_of(doc)['slides']),2)
            vtt=(Path(built['package'])/(built['stem']+'.vtt')).read_text(encoding='utf-8')
            self.assertIn('&lt;&gt;',vtt)
            self.assertIn('Ø25',vtt)
            # Once its MP4 exists, assembling again must not replace the deck
            # or captions while leaving the old video behind.
            before=downloaded.read_bytes()
            (Path(built['package'])/(built['stem']+'.mp4')).write_bytes(b'fixture video')
            with self.assertRaises(FileExistsError):assemble(root,'en')
            self.assertEqual(downloaded.read_bytes(),before)


if __name__=='__main__': unittest.main()
