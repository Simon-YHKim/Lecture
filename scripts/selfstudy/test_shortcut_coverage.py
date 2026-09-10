"""Every narrated command must be findable in both self-study command indexes."""
import json
from pathlib import Path
import re
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "part"))
import beats
import lesson_kit


def covers(row, command):
    full = lesson_kit.COMMANDS[command][0]
    aliases = {key for key, value in lesson_kit.COMMANDS.items() if value[0] == full}
    aliases.add(full)
    keys = set(re.split(r"\s*/\s*", row["key"].upper()))
    names = " ".join(row.get("name", {}).values())
    # The same key may be an option only: e.g. M for dimension text is not MOVE.
    option_only = ("옵션" in names or "option" in names.lower()) and not re.search(
        r"(?<![A-Z])" + re.escape(full) + r"(?![A-Z])", names.upper())
    return bool(keys & aliases) and not option_only


class ShortcutCoverageTests(unittest.TestCase):
    def test_each_narrated_command_has_one_local_and_global_entry(self):
        common = json.loads((HERE / "source" / "curriculum.json").read_text(encoding="utf-8"))["shortcutIndex"]
        for number in range(3, 8):
            source = json.loads((HERE / "source" / f"lesson-{number:02}.json").read_text(encoding="utf-8"))
            script = ROOT / "projects" / "autocad-technician" / source["slug"] / "SCRIPT.md"
            for command in beats.shortcuts_in(str(script), 5):
                with self.subTest(lesson=number, command=command):
                    self.assertEqual(sum(covers(row, command) for row in source["shortcuts"]), 1)
                    matching = [row for row in common if covers(row, command)]
                    self.assertEqual(len(matching), 1)
                    self.assertIn(number, matching[0]["lessons"])

    def test_option_key_does_not_satisfy_an_unrelated_command(self):
        option = {"key": "M", "name": {"ko": "여러 줄 문자 옵션", "en": "Multiline text option"}}
        self.assertFalse(covers(option, "M"))
        alias = {"key": "LI / LIST", "name": {"ko": "객체 정보", "en": "Object information"}}
        self.assertTrue(covers(alias, "LIST"))
        self.assertTrue(covers(alias, "LI"))


if __name__ == "__main__":
    unittest.main()
