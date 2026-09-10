"""Edition checks must distinguish typed commands from dimension text."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    "check_editions", Path(__file__).with_name("check-editions.py"))
editions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(editions)


class EditionChecksTests(unittest.TestCase):
    def test_dimension_values_and_measured_text_are_not_commands(self):
        self.assertEqual(editions.commands_in(
            "`95.7` `(95.7)` `(120)` `(-5.5)` `<>` `(<>)`"), set())

    def test_commands_snaps_and_command_options_remain_checked(self):
        expected = {"DIMCEN", "DIMSCALE", "EX", "INT", "MIRRTEXT", "PER", "U"}
        self.assertEqual(editions.commands_in(
            " ".join(f"`{command}`" for command in expected)), expected)

    def test_unknown_command_candidates_are_not_silently_dropped(self):
        self.assertEqual(editions.commands_in("`FUTURECMD` `(BROKEN)` `<BAD>`"),
                         {"FUTURECMD", "(BROKEN)", "<BAD>"})

    def test_coach_references_match_the_action_target(self):
        cases = [(3, 11, 1, 1, (60, 0), "밑변 중간점"),
                 (3, 11, 4, 2, (5, 16), "모따기 위쪽 끝점"),
                 (4, 14, 2, 1, (10, 16), "베이스 윗면"),
                 (4, 14, 3, 2, (23.403908, 30), "왼쪽 목 선")]
        for lesson, number, action_index, marker, point, target in cases:
            with self.subTest(lesson=lesson, step=number, marker=marker):
                doc = editions.selfstudy(lesson)["doc"]
                step = next(st for section in doc["sections"]
                            for block in section.get("blocks", [])
                            if block.get("type") == "steps"
                            for st in block["items"] if st["n"] == number)
                action = step["actions"][action_index]
                self.assertEqual(action.get("spot"), marker)
                self.assertIn(target, action["do"]["ko"])
                spot = step["spots"][marker - 1]
                self.assertEqual((spot["x"], spot["y"]), point)

    def test_current_editions_keep_command_and_marker_coverage(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = editions.main()
        self.assertEqual(result, 0, out.getvalue())

    def test_missing_real_command_still_fails(self):
        original = editions.selfstudy

        def without_extend(number):
            result = original(number)
            result["cmds"].discard("EX")
            return result

        out = io.StringIO()
        with mock.patch.object(editions, "selfstudy", side_effect=without_extend):
            with contextlib.redirect_stdout(out):
                self.assertEqual(editions.main(), 1)
        self.assertIn("강의용에서만 치는 명령: EX", out.getvalue())

    def test_unexplained_marker_still_fails(self):
        original = editions.selfstudy

        def without_target(number):
            result = original(number)
            if number == 3:
                for section in result["doc"]["sections"]:
                    for block in section.get("blocks", []):
                        if block.get("type") == "steps":
                            for step in block["items"]:
                                if step["n"] == 11:
                                    step["actions"][1].pop("spot", None)
            return result

        out = io.StringIO()
        with mock.patch.object(editions, "selfstudy", side_effect=without_target):
            with contextlib.redirect_stdout(out):
                self.assertEqual(editions.main(), 1)
        self.assertIn("3차시 11단계 — 설명 줄이 없는 코치 마크 [1]", out.getvalue())


if __name__ == "__main__":
    unittest.main()
