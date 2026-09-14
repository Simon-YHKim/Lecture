"""Publication boundary regressions using synthetic delivery fixtures."""
from pathlib import Path
import json
import tempfile
import unittest
import zipfile

from package_narrated import package, selected_files, validate_text
from build_narrated_review import document, review_data
from narrated_delivery import digest
from prepare_narrated import write_json


class NarratedPackageTests(unittest.TestCase):
    def test_delivery_uses_exact_names_and_omits_private_neighbors(self):
        names = {p.name for p in selected_files(Path('fixture'), 'ko')}
        self.assertEqual(len(names), 40)
        self.assertIn('AutoCAD_KO_L08_SELFSTUDY.mp4', names)
        for private in ['reference.wav', 'SAMPLE_REVIEW_KO.html', 'done.jsonl', 'feedback.json']:
            self.assertNotIn(private, names)

    def test_private_path_is_rejected_but_literal_cad_text_is_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'script.md'
            path.write_text('Enter <>. Diameter Ø25. Press F8.', encoding='utf-8')
            validate_text(path)
            path.write_text((Path(temp)/'reference.wav').as_uri(), encoding='utf-8')
            with self.assertRaises(ValueError):
                validate_text(path)

    def test_partial_review_cannot_create_a_delivery_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, 'eight verified'):
                package(root, root/'delivery', 'a'*40, 'autocad-2026.09.15-selfstudy-review.1')
            self.assertFalse((root/'delivery').exists())

    def test_existing_delivery_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); existing = root/'keep.txt'; existing.write_text('existing')
            with self.assertRaises(FileExistsError):
                package(root, root, 'a'*40, 'autocad-2026.09.15-selfstudy-review.1')
            self.assertEqual(existing.read_text(), 'existing')

    def test_review_rejects_deck_or_video_changed_after_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); folder = root/'packages/en'; folder.mkdir(parents=True)
            stem = 'AutoCAD_EN_L01_SELFSTUDY'
            video = folder/(stem+'.mp4'); video.write_bytes(b'synthetic video')
            deck = folder/(stem+'.html'); deck.write_bytes(b'<html>synthetic slide</html>')
            source = root/'source.json'; write_json(source, {'title': {'en': 'Fixture'}})
            assembled = root/'assembled/en/L01.json'
            write_json(assembled, {'package':str(folder),'stem':stem,'source':str(source),
                'lesson':1,'duration':1,'deckSha256':digest(deck),'cues':[]})
            write_json(root/'validation/en/L01.json', {'ok':True,'sha256':digest(video),
                                                      'planSha256':digest(assembled)})
            self.assertFalse(review_data(root, 'en', complete=False)['complete'])
            deck.write_bytes(b'changed deck')
            with self.assertRaisesRegex(ValueError, 'Deck changed'):
                review_data(root, 'en', complete=False)
            video.write_bytes(b'changed video')
            with self.assertRaisesRegex(ValueError, 'Video changed'):
                review_data(root, 'en', complete=False)

    def test_review_json_cannot_inject_a_script(self):
        text = document({'language':'en','complete':False,'lessons':[],
                         'reviewId':'</script><script>alert(1)</script>'})
        self.assertNotIn('</script><script>alert(1)</script>', text)
        self.assertIn(chr(92)+'u003c/script>', text)

    def test_complete_package_excludes_private_neighbors_and_checksums_zip_contents(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for lang in ['ko', 'en']:
                folder = root/'packages'/lang; folder.mkdir(parents=True)
                for private in ['reference.wav', 'SAMPLE_REVIEW_EN.html', 'asr.json']:
                    (folder/private).write_bytes(b'must remain private')
                for n in range(1, 9):
                    stem = 'AutoCAD_%s_L%02d_SELFSTUDY' % (lang.upper(), n)
                    for ext in ['.html', '.mp4', '.md', '.vtt', '.srt']:
                        (folder/(stem+ext)).write_bytes(b'synthetic fixture')
                    source = root/('%s-%d-source.json'%(lang,n))
                    write_json(source, {'title': {lang: 'Fixture %d'%n}})
                    assembled = root/'assembled'/lang/('L%02d.json'%n)
                    write_json(assembled, {'package':str(folder),'stem':stem,'source':str(source),
                        'lesson':n,'duration':1,'deckSha256':digest(folder/(stem+'.html')),'cues':[]})
                    write_json(root/'validation'/lang/('L%02d.json'%n),
                        {'ok':True,'sha256':digest(folder/(stem+'.mp4')),'planSha256':digest(assembled),
                         'slides':1,'shots':1,'cues':0,'fullDecode':True,'literalCaptions':True})
            output = root/'delivery'
            result = package(root, output, 'a'*40, 'autocad-2026.09.15-selfstudy-review.1')
            self.assertEqual(result['coreFileCount'], 32)
            self.assertEqual(len(list(output.iterdir())), 37)
            for lang in ['ko', 'en']:
                with zipfile.ZipFile(output/('AutoCAD_%s_SELFSTUDY.zip'%lang.upper())) as z:
                    self.assertEqual(len(z.namelist()), 44)
                    self.assertNotIn('reference.wav', z.namelist())
                    self.assertNotIn('asr.json', z.namelist())
                    self.assertFalse(any('SAMPLE' in name for name in z.namelist()))
                    entries = json.loads(z.read('release-manifest.json'))['files']
                    import hashlib
                    for entry in entries:
                        self.assertEqual(hashlib.sha256(z.read(entry['file'])).hexdigest(), entry['sha256'])
            self.assertNotIn(str(root), json.dumps(result))


if __name__ == '__main__':
    unittest.main()
