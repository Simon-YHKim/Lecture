"""Temporary geometry, view transforms and source-to-marker integrity."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

import coach

HERE = Path(__file__).resolve().parent


class CoachTests(unittest.TestCase):
    def test_top_and_side_construction_use_canonical_transforms(self):
        st={"construction":[{"kind":"line","view":"top","points":[[32,0],[32,8]]},
                            {"kind":"line","view":"side","points":[[8,34],[8,68]]}]}
        svg=coach.construction_for(st,"three")
        self.assertIn("M90.000000 84.000000 L90.000000 76.000000",svg)
        self.assertIn("M232.000000 174.000000 L232.000000 140.000000",svg)
        ET.fromstring("<svg>"+svg+"</svg>")

    def test_invalid_geometry_fails_closed(self):
        for item in [{"kind":"line","points":[[0,0],[float("nan"),2]]},
                     {"kind":"line","view":"untrusted","points":[[0,0],[1,2]]},
                     {"kind":"circle","centre":[0,0],"radius":-1},
                     {"kind":"script","points":[]}]:
            with self.subTest(item=item), self.assertRaises(ValueError):
                coach.construction_for({"construction":[item]},"front")

    def test_focus_uses_view_orientation(self):
        vb=list(map(float,coach.figure_viewbox(
            {"focus":{"view":"side","bounds":[0,0,20,90],"padding":5}},"three",'<svg viewBox="0 0 296 274"></svg>').split()))
        self.assertEqual(vb,[206.5,113.0,55.0,100.0])

    def test_practice_symbol_omits_final_dimensions_but_keeps_geometry(self):
        src='<svg viewBox="0 0 100 100"><line class="outline" x1="0" y1="0" x2="1" y2="1"/><line class="dim" x1="2" y1="2" x2="3" y2="3"/><text class="dimtext">120</text></svg>'
        out=coach.to_symbol(src,"sfc-front",css=False)
        self.assertIn('class="outline"',out)
        self.assertNotIn('class="dim"',out)
        self.assertNotIn(">120<",out)

    def test_all_authored_steps_have_valid_construction_and_marker_indices(self):
        count=0
        for n in range(3,8):
            d=json.loads((HERE/"source"/f"lesson-{n:02}.json").read_text(encoding="utf-8"))
            for section in d["sections"]:
                for block in section.get("blocks",[]):
                    if block.get("type")!="steps": continue
                    for step in block["items"]:
                        with self.subTest(lesson=n,step=step["n"]):
                            spots=step.get("spots",[])
                            for action in step["actions"]:
                                for mark in coach.spot_badges(action):
                                    self.assertTrue(1<=mark<=len(spots),(n,step["n"],mark))
                            svg=coach.construction_for(step,step.get("on","front"))
                            if svg:
                                ET.fromstring("<svg>"+svg+"</svg>")
                                count+=1
                            coach.figure_viewbox(step,step.get("on","front"),'<svg viewBox="0 0 296 274"></svg>')
        self.assertGreaterEqual(count,35)

    def test_reference_text_keeps_measured_placeholder(self):
        d=json.loads((HERE/"source"/"lesson-07.json").read_text(encoding="utf-8"))
        steps=[s for sec in d["sections"] for b in sec.get("blocks",[]) if b.get("type")=="steps" for s in b["items"]]
        reference=next(s for s in steps if s["n"]==15)
        tokens=[a.get("type") for a in reference["actions"]]
        self.assertIn("(<>)",tokens)
        self.assertNotIn("(95.7)",tokens)

    def test_lesson_six_layer_table_matches_canonical_values_in_both_languages(self):
        source=json.loads((HERE/"source"/"lesson-06.json").read_text(encoding="utf-8"))
        standard=json.loads((HERE.parents[1]/"projects"/"autocad-technician"/"course-standards.json").read_text(encoding="utf-8"))
        table=next(b for s in source["sections"] for b in s.get("blocks",[])
                   if b.get("caption",{}).get("ko")=="이 과정의 레이어 넷 · 정본 값")
        self.assertEqual(len(table["rows"]),len(standard["layers"]["rows"]))
        english={3:"Green",1:"Red",2:"Yellow",7:"white"}
        for row,want in zip(table["rows"],standard["layers"]["rows"]):
            self.assertEqual(row[0]["ko"],want["name"])
            self.assertEqual(row[1]["ko"],f'{want["colorName"]} {want["aci"]}')
            self.assertEqual(re.findall(r"\d+",row[1]["en"]),[str(want["aci"])])
            self.assertIn(english[want["aci"]].lower(),row[1]["en"].lower())
            for lang in ("ko","en"):
                self.assertEqual(row[2][lang].upper(),want["linetype"].upper())
                self.assertEqual(float(row[3][lang]),want["lineweight"])
                if want["ltscale"] is not None:
                    self.assertEqual(float(row[4][lang].strip("`")),want["ltscale"])

    def test_each_authored_marker_is_inside_its_explicit_focus(self):
        for n in range(3,8):
            source=json.loads((HERE/"source"/f"lesson-{n:02}.json").read_text(encoding="utf-8"))
            for section in source["sections"]:
                for block in section.get("blocks",[]):
                    if block.get("type")!="steps": continue
                    for step in block["items"]:
                        if not step.get("focus"): continue
                        surface=step.get("on","front")
                        x,y,w,h=map(float,coach.figure_viewbox(step,surface,'<svg viewBox="0 0 296 274"></svg>').split())
                        for mark in step.get("spots",[]):
                            px,py=coach.place(mark,surface)
                            with self.subTest(lesson=n,step=step["n"],mark=mark):
                                self.assertTrue(x<=px<=x+w and y<=py<=y+h)


if __name__=="__main__":
    unittest.main()
