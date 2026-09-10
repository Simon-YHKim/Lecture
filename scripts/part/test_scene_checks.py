import unittest
from prepare_scene_checks import scopes


class SceneScopesTests(unittest.TestCase):
    def test_long_recording_preserves_assertions_and_full_bounds_duration(self):
        assertions = [{'kind': 'appearsBy', 'selector': '#f .strip', 'bySec': 3},
                      {'kind': 'staysInFrame', 'selector': '#f .strip'}]
        result = scopes({'duration': 960, 'assertions': assertions})
        self.assertEqual([(n, d) for n, d, _ in result], [('entrance', 10), ('full', 960)])
        self.assertEqual(result[0][2], assertions)
        self.assertEqual(result[1][2], [assertions[1]])

    def test_short_scene_keeps_the_original_spec(self):
        spec = {'duration': 12, 'assertions': [{'kind': 'appearsBy', 'selector': '#f', 'bySec': 3}]}
        self.assertEqual(scopes(spec), [('full', 12, spec['assertions'])])

    def test_order_with_no_known_deadline_is_not_truncated(self):
        spec = {'duration': 960, 'assertions': [
            {'kind': 'appearsBy', 'selector': '#a', 'bySec': 3},
            {'kind': 'before', 'a': '#a', 'b': '#b'},
            {'kind': 'staysInFrame', 'selector': '#a'}]}
        self.assertEqual(scopes(spec), [('full', 960, spec['assertions'])])


if __name__ == '__main__':
    unittest.main()
