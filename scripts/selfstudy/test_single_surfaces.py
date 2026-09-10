import re
import unittest
from unittest.mock import patch

import build_single


class WorkbookSymbolTests(unittest.TestCase):
    def test_multiple_lessons_share_one_definition_outside_the_tabs(self):
        definition = '<svg class="sfcdefs"><symbol id="sfc-front"></symbol></svg>'
        lesson = '<section hidden>%s<svg><use href="#sfc-front"></use></svg></section>' % definition
        with patch.object(build_single.B, 'surface_defs', return_value=definition) as definitions:
            output = build_single.consolidate_surfaces('<body>' + lesson + lesson + '</body>')
        self.assertEqual(output.count('id="sfc-front"'), 1)
        self.assertEqual(output.count('href="#sfc-front"'), 2)
        self.assertTrue(output.startswith('<body>' + definition + '<section'))
        definitions.assert_called_once_with({'front'})


if __name__ == '__main__':
    unittest.main()
