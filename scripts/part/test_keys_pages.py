"""A dense command recap must keep every spoken row readable."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
import unittest

import lesson_kit as kit
from lesson_build import f_keys
from retime_frames import CALL, retime_frame


class Rows(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tables = []
        self.pages = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table':
            self.tables.append([])
        if tag == 'tr' and attrs.get('class', '').startswith('ky '):
            self.tables[-1].append(attrs['class'])
        if 'keys-page' in attrs.get('class', '').split():
            self.pages.append(attrs)


class KeysPageTests(unittest.TestCase):
    def setUp(self):
        self.keys = list(kit.COMMANDS)[:24]
        self.spans = [(i, 3.0 + (i - 1) * 6, 8.0 + (i - 1) * 6)
                      for i in range(1, 25)]

    def build(self, count=24):
        return f_keys('test', 150, self.spans[:count], {'keys': self.keys[:count]})

    def test_twenty_four_rows_use_two_pages_without_smaller_type(self):
        html, assertions = self.build()
        parsed = Rows(html)
        self.assertEqual(len(parsed.pages), 2)
        self.assertEqual([len(rows) for rows in parsed.tables], [6, 6, 6, 6])
        self.assertEqual([row for table in parsed.tables for row in table],
                         ['ky ky%d' % i for i in range(1, 25)])
        body = html.split('<main', 1)[1].split('</main>', 1)[0]
        self.assertEqual(body.count('font-size:22px'), 24)
        self.assertEqual(body.count('font-size:19px'), 24)
        text = re.sub(r'<[^>]+>', '', body)
        for key in self.keys:
            self.assertIn('>%s</td>' % key, html)
            self.assertIn(kit.COMMANDS[key][1], text)
            self.assertIn(kit.COMMANDS[key][2], text)
        for key, meaning, _ in kit.FUNCTION_KEYS:
            self.assertIn(meaning, text)
        for i in range(1, 25):
            selector = '#test .ky%d' % i
            self.assertTrue(any(a['kind'] == 'appearsBy' and a['selector'] == selector
                                for a in assertions))
            self.assertIn({'kind': 'staysInFrame', 'selector': selector}, assertions)

    def test_page_boundary_tracks_thirteenth_beat_and_survives_retime(self):
        html, assertions = self.build()
        def page_calls(source):
            return [m for m in CALL.finditer(source) if 'keys-earlier' in m['sel']
                    or 'keys-later' in m['sel']]
        for call in page_calls(html):
            self.assertEqual(float(call['time']), self.spans[12][1])
            self.assertIn('duration:0', call['mid'])
        self.assertEqual(len(page_calls(html)), 2)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'frame.html'
            path.write_text(html, encoding='utf8')
            path.with_suffix('.motion.json').write_text(json.dumps({
                'duration': 150, 'assertions': assertions}), encoding='utf8')
            new = [(a * 1.1, b * 1.1) for _, a, b in self.spans]
            retime_frame(str(path), new, 165)
            changed = path.read_text(encoding='utf8')
            for call in page_calls(changed):
                self.assertEqual(float(call['time']), round(new[12][0], 2))
            retime_frame(str(path), new, 165)
            self.assertEqual(path.read_text(encoding='utf8'), changed)

    def test_other_current_command_counts_keep_their_single_page_layout(self):
        for count in (9, 11, 15, 17):
            with self.subTest(count=count):
                html, _ = self.build(count)
                parsed = Rows(html)
                self.assertEqual(parsed.pages, [])
                self.assertEqual(len(parsed.tables), 1 if count <= 9 else 2)
                self.assertEqual(sum(map(len, parsed.tables)), count)
                self.assertNotIn('keys-earlier', html)
                self.assertNotIn('keys-later', html)


if __name__ == '__main__':
    unittest.main()
