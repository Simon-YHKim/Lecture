"""Static geometry regressions; no AutoCAD or generated files are required."""
import math
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent


def drawing(profile="full", lang=None):
    source = (HERE / "edu_ib_02.py").read_text(encoding="utf-8")
    namespace = {}
    argv = (["edu_ib_02.py", "unused.svg"]
            + (["--profile", profile] if profile != "full" else [])
            + (["--lang", lang] if lang else []))
    with patch("sys.argv", argv):
        exec(compile(source.split("target = sys.argv[1]")[0], str(HERE / "edu_ib_02.py"), "exec"), namespace)
    return namespace, ET.fromstring(namespace["svg"])


def texts(root):
    return [(el.text or "").strip() for el in root.iter() if el.tag.endswith("}text")]


def lines(root, css="outline"):
    return [tuple(float(el.attrib[k]) for k in ("x1","y1","x2","y2"))
            for el in root.iter() if el.tag.endswith("}line") and el.get("class")==css]


class ProjectionTests(unittest.TestCase):
    def test_top_plate_front_keeps_only_two_outboard_edges(self):
        n, svg = drawing()
        y = n["T"](0, 8)[1]
        edges = [q for q in lines(svg) if abs(q[1]-y)<.001 and abs(q[3]-y)<.001]
        expected = [(*n["T"](0,8),*n["T"](n["TL"][0],8)),
                    (*n["T"](n["TR"][0],8),*n["T"](120,8))]
        self.assertEqual(len(edges), 2)
        for got, want in zip(edges,expected):
            for a,b in zip(got,want): self.assertAlmostEqual(a,b,places=3)
        self.assertLess(n["TL"][0]-32,1)
        self.assertGreater(n["TL"][0]-32,0)

    def test_right_step_ends_at_web_tangency_not_boss_top(self):
        n, svg = drawing()
        x,y = n["R"](8,34)
        edges = [q for q in lines(svg) if q[0]==x and q[2]==x and q[1]==y]
        self.assertEqual(len(edges),1)
        self.assertAlmostEqual(edges[0][3], n["R"](8,n["TR"][1])[1], places=3)
        self.assertGreater(edges[0][3], n["R"](8,90)[1])

    def test_tangent_point_matches_independent_line_circle_equations(self):
        n,_ = drawing()
        x,y = n["TR"]
        self.assertAlmostEqual(math.hypot(x-60,y-62),28,places=10)
        self.assertAlmostEqual((x-100)*(x-60)+(y-16)*(y-62),0,places=10)
        # At x=87.6 the web silhouette is above the boss, so the short step is real.
        m=(y-16)/(x-100)
        self.assertGreater(16+m*(87.6-100),62+math.sqrt(28**2-(87.6-60)**2))

    def test_r5_leader_points_to_the_retained_left_slot_arc(self):
        n, svg = drawing()
        first = next(el for el in svg.iter()
                     if el.tag.endswith("}line") and el.get("data-dim")=="sr5")
        x=float(first.get("x1"))-n["FX"]
        y=n["FY"]-float(first.get("y1"))
        self.assertLess(x,29)
        self.assertAlmostEqual(math.hypot(x-29,y-8),5,places=3)

    def test_reference_dimension_is_computed_between_fillet_centres(self):
        n,_=drawing()
        self.assertAlmostEqual(n["FC"][0]-n["FC_L"][0],95.71993942524836,places=10)
        self.assertEqual(f'{n["FC"][0]-n["FC_L"][0]:.1f}',"95.7")

    def test_front_shape_is_unchanged_by_projection_rule(self):
        n,svg=drawing("front")
        outlines=[el for el in svg.iter() if el.get("class")=="outline"]
        self.assertTrue(outlines)
        self.assertEqual(n["BASE_W"],120)
        self.assertEqual(n["TOP_Y"],90)
        self.assertEqual(n["SLOT_CTC"],12)
        # All ten DIMCENTER crosses have two strokes of length 6.
        crosses=[q for q in lines(svg,"center") if abs(math.hypot(q[2]-q[0],q[3]-q[1])-6)<.001]
        self.assertEqual(len(crosses),20)


class DrawingLanguageTests(unittest.TestCase):
    """영문판은 학습자가 도면의 글자를 그대로 보고 타이핑한다."""

    def test_korean_drawing_still_carries_the_korean_callouts(self):
        _, svg = drawing()
        found = texts(svg)
        self.assertIn("4-M5 깊이 10", found)
        self.assertIn("2-장공 R5", found)
        self.assertIn("정면도", found)

    def test_english_drawing_has_no_korean_left(self):
        _, svg = drawing(lang="en")
        found = texts(svg)
        self.assertEqual([t for t in found if re.search(r"[가-힣]", t)], [])
        for expected in ("4-M5 DEPTH 10", "2-SLOT R5",
                         "FRONT VIEW", "TOP VIEW", "RIGHT SIDE VIEW"):
            self.assertIn(expected, found)

    def test_geometry_is_identical_in_both_languages(self):
        """말이 바뀌어도 선은 한 줄도 움직이지 않는다."""
        korean, _ = drawing()
        english, _ = drawing(lang="en")
        strip = re.compile(r"<text[^>]*>.*?</text>", re.S)
        self.assertEqual(strip.sub("", korean["svg"]), strip.sub("", english["svg"]))

    def test_front_profile_localises_the_two_callouts(self):
        _, svg = drawing("frontdim", lang="en")
        found = texts(svg)
        self.assertIn("4-M5 DEPTH 10", found)
        self.assertIn("2-SLOT R5", found)


if __name__ == "__main__":
    unittest.main()
