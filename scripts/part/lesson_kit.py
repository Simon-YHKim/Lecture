"""Shared building blocks for every AutoCAD Technician lesson composition.

LESSON_STYLE.md fixes the parts every lesson shares — a title card, the visual
system, and a two-panel closing frame. They live here so a change lands in all
lessons at once instead of being re-typed per lesson.

Scaffolds import this; they do not copy it.
"""

import re

FONTS = (
    '<style>@font-face{font-family:"LG EI Text TTF Regular";src:local("LG EI Text TTF Regular");font-weight:400}'
    '@font-face{font-family:"LG EI Headline TTF Semibold";src:local("LG EI Headline TTF Semibold");font-weight:600}'
    '@font-face{font-family:"Malgun Gothic";src:local("Malgun Gothic");font-weight:400}</style>'
)

BASE_CSS = """
/* Both selectors on purpose. `#root` is the host page in index.html; inside a
   frame the root carries id="<comp>-root", so a bare #root rule reaches
   nothing there — which is how word-break:keep-all sat in this file for a
   commit without ever applying to a single line of Korean on screen. */
#root,[data-composition-id]{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;color:#111;
 font-family:"LG EI Text TTF Regular","Malgun Gothic",sans-serif;
 /* Korean breaks between 어절, not inside one. Without this a word splits
    mid-syllable at the line end and reads as a typo.

    overflow-wrap must be break-word, not anywhere: `anywhere` lets the browser
    break mid-word to fill a line even when the whole 어절 would fit on the
    next one, which put 「모여서 본 / 다」 and 「사번_이 / 름」 on screen with
    keep-all already set. break-word only splits a word that cannot fit a line
    by itself. */
 word-break:keep-all;overflow-wrap:break-word}
*{box-sizing:border-box}
.clip{position:absolute;inset:0;width:100%;height:100%;padding:72px 96px 64px;background:#FFF}
.topline{display:flex;justify-content:space-between;align-items:end;padding-bottom:18px;border-bottom:2px solid #A4A3A4}
.index{color:#C7004C;font-size:24px;font-weight:600;letter-spacing:.08em}
h1{margin:0;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;font-size:58px;letter-spacing:-.035em}
.prompt{color:#666;font-size:26px}
.body{display:grid;gap:38px;height:724px;padding-top:36px}
.panel{background:#F5F5F3;border:2px solid #A4A3A4;display:grid;place-items:center;overflow:hidden}
.panel svg{width:100%;height:100%}
.dwg .outline{fill:none;stroke:#111;stroke-width:.5;stroke-linejoin:round;stroke-linecap:round}
.dwg .hidden{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:2.4 1.2}
.dwg .center{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:6 1.2 1 1.2}
.dwg .dim,.dwg .ext,.dwg .tangent{fill:none;stroke:#111;stroke-width:.25}
.dwg .arrow{fill:#111;stroke:none}
.dwg .hl{fill:none;stroke:#C7004C;stroke-width:1.1;stroke-linejoin:round;stroke-linecap:round;opacity:0}
.card{border:2px solid #A4A3A4;background:#FFF;padding:20px 24px;color:#111}
.ico{fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;display:block}
.card.wide{display:grid;grid-template-columns:auto minmax(0,1fr);gap:20px;align-items:start}
.card b{display:block;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;color:#C7004C;font-size:28px}
.card strong{display:block;margin:6px 0 4px;color:#111;font-size:24px}
.card span{display:block;color:#666;font-size:21px;line-height:1.45}
/* span.kw, not .kw: `.card span{display:block;color:#666;font-size:21px}` has
   the same specificity and would otherwise win by order — every 어절 on its own
   line, and a word inside a coloured label repainted grey while the one-syllable
   words beside it, too short to be wrapped, kept the colour. The inherits put
   the span back to being invisible to the cascade. */
span.kw{display:inline;white-space:nowrap;color:inherit;font:inherit;line-height:inherit;letter-spacing:inherit}
.note{margin-top:14px;padding-top:14px;border-top:4px solid #111;font-size:24px;line-height:1.45}
.note b{color:#C7004C}
table.spec{width:100%;border-collapse:collapse;font-size:22px}
table.spec th{text-align:left;padding:8px 10px;color:#666;font-size:19px;letter-spacing:.06em;border-bottom:2px solid #A4A3A4}
table.spec td{padding:9px 10px;border-bottom:1px solid #DCDBD7}
table.spec.tight th,table.spec.tight td{padding:6px 8px}
.title{position:absolute;inset:0;background:#111;display:grid;align-content:center;padding:0 140px}
.title .brand{font-size:29px;letter-spacing:.22em;color:#FFF}
.title .cert{margin-top:28px;font-size:32px;letter-spacing:.09em;color:#C7004C;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif}
.title h2{margin:18px 0 0;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;font-size:92px;letter-spacing:-.04em;line-height:1.06;color:#FFF}
.title .rule{margin-top:42px;width:220px;height:3px;background:#C7004C}
.title .sub{margin-top:28px;font-size:29px;color:#FFF;letter-spacing:.02em}
.close{position:absolute;inset:0;background:#111;display:grid;align-content:center;padding:0 140px}
.close .rule{width:220px;height:3px;background:#C7004C}
.close h2{margin:40px 0 0;font-family:"LG EI Headline TTF Semibold","Malgun Gothic",sans-serif;font-size:92px;letter-spacing:-.04em;line-height:1.06;color:#FFF}
.close .next{margin-top:34px;font-size:34px;color:#FFF;letter-spacing:.01em}
.close .next em{font-style:normal;color:#C7004C}
.close .brand{margin-top:58px;font-size:25px;letter-spacing:.22em;color:#8A8788}
/* The recording gets the whole frame. Anything the course needs to say during
   it rides on top, because shrinking the video to make room shrinks AutoCAD's
   command line with it — and that is the text a learner follows. */
.film{position:absolute;inset:0;background:#111;overflow:hidden}
.film .rec{position:absolute;inset:0;display:grid;place-content:center;justify-items:center;
 gap:12px;border:2px dashed #4A4749}
.film .recmark{font-size:34px;letter-spacing:.14em;color:#C7004C}
.film .recsub{font-size:25px;color:#8A8788}
.film .tag{position:absolute;top:44px;left:56px;font-size:30px;color:#FFF;
 background:rgba(17,17,17,.82);padding:12px 22px;border-left:3px solid #C7004C}
.film .strip{position:absolute;left:0;right:0;bottom:0;height:132px;
 background:rgba(17,17,17,.93);border-top:1px solid #4A4749}
.film .sp{position:absolute;left:56px;right:56px;top:26px;display:flex;align-items:baseline;
 gap:30px;opacity:0}
.film .sp .no{font-family:ui-monospace,Consolas,monospace;font-size:28px;color:#8A8788;
 letter-spacing:.04em;white-space:nowrap}
.film .sp .no i{font-style:normal;color:#626061}
.film .sp .key{font-family:ui-monospace,Consolas,monospace;font-size:40px;color:#C7004C;
 min-width:190px;white-space:nowrap}
.film .sp .what{font-size:34px;color:#FFF;letter-spacing:-.01em}
.film .track{position:absolute;left:0;right:0;bottom:0;height:5px;background:#333032}
.film .prog{display:block;height:100%;width:100%;background:#C7004C;transform-origin:left center}
"""

HEAD = ('<!DOCTYPE html>\n<html lang="ko"><head><meta charset="UTF-8"></head><body><template>'
        + FONTS + "\n  <style>" + BASE_CSS + "  </style>\n")
TAIL = "</template></body></html>\n"


# Card marks. Drawn in the same pen as the part drawing — thin strokes, no
# fills, no emoji — and wherever the subject already has a symbol for the idea,
# that symbol is used rather than a picture invented for it. Three of these are
# things the course itself teaches: the surface-roughness tick, the third-angle
# projection symbol, and the four line types.
#
# Two rules were learned the hard way here and both are load-bearing.
#
# Geometry that is exactly tangent fuses. A belt line drawn on a circle's top
# tangent shares its pixels with the arc, and at 58px the pair renders as one
# capsule outline instead of a wheel with a belt over it. Everything that
# touches now clears by at least one unit.
#
# stroke-linecap:round steals half a stroke width from each end of every dash,
# so a nominal 2-unit gap renders as 0.5. The dashed paths carry butt caps
# inline; the rest keep the round policy.
#
# Arrowheads: run 3, half-rise 1.0 — an included 36 degrees. ISO wants 15-30,
# but below about 36 the head stops reading as an arrow at this size.
ICONS = {
    # --- 8차시 · 테크니션 업무 ---------------------------------------
    # A jig is locating and clamping: the workpiece sits on supports and
    # something presses it down. That is the whole idea, so that is the mark.
    "jig": '<path d="M4 27h24"/><path d="M11 27v-7M21 27v-7"/>'
           '<rect x="8" y="12" width="16" height="8"/>'
           '<path d="M16 3v6M16 9l-1-3M16 9l1-3"/>',
    # Layout checking is a footprint inside a space with a clearance that has
    # to be measured, not eyeballed — hence the dimension, in the same
    # vocabulary the course already teaches.
    "layout": '<rect x="3" y="6" width="26" height="21"/>'
              '<rect x="15" y="12" width="11" height="10"/>'
              '<path d="M3.5 17h11"/>'
              '<path d="M3.5 17l3-1M3.5 17l3 1M14.5 17l-3-1M14.5 17l-3 1"/>',
    # Finding one part inside an assembly is done with a balloon and a leader.
    # The drawing already has a symbol for this; no picture is invented for it.
    "balloon": '<rect x="4" y="13" width="16" height="13"/><path d="M12 13v13"/>'
               '<circle cx="25.5" cy="7" r="4.3"/><path d="M23.05 10.54L17.47 18.6"/>'
               '<circle cx="16.5" cy="20" r="1.1"/>',
    # a shape with its size on it
    "shape": '<rect x="5" y="5" width="22" height="13"/><path d="M5 21v6M27 21v6"/>'
             '<path d="M5 24.5h22M5 24.5l3-1M5 24.5l3 1M27 24.5l-3-1M27 24.5l-3 1"/>',
    # the position symbol. The first attempt drew datum axes with an offset box
    # and read as neither — a box on a stand.
    "pose": '<circle cx="16" cy="16" r="8.5"/><path d="M16 4v24M4 16h24"/>',
    # the surface-texture symbol. Both legs lean 60 degrees from the surface
    # line and the long-to-short ratio is ISO 1302's 2.1.
    "surface": '<path d="M4 16.5L9.5 26L21 6"/><path d="M21 6h9"/>',
    # two sheets that read the same. Drawn as sheets rather than bare squares so
    # the mark speaks the same vocabulary as "archive".
    "same": '<rect x="2" y="9" width="10" height="14"/><path d="M2 19h10"/>'
            '<rect x="20" y="9" width="10" height="14"/><path d="M20 19h10"/>'
            '<path d="M15 14.5h2M15 17.5h2"/>',
    # a sheet with its title block — the frame they will draw in lesson 2
    "archive": '<rect x="3" y="4" width="26" height="24"/><rect x="7" y="8" width="18" height="16"/>'
               '<rect x="15" y="18" width="10" height="6"/>',
    # an isometric solid. The three internal edges run from the near vertex to
    # the two upper corners and down to the bottom one; drawing the vertical the
    # other way splits the top face and is not an isometric cube at all.
    "iso": '<path d="M16 4l11 6v12l-11 6-11-6V10z"/><path d="M16 16v12M16 16l11-6M16 16L5 10"/>',
    # the AutoCAD crosshair
    "crosshair": '<path d="M2 16h28M16 2v28"/><rect x="12.5" y="12.5" width="7" height="7"/>',
    # The third-angle projection symbol. What separates it from first angle is
    # not which side the circles sit on — it is that the frustum's SMALL end
    # faces them. Drawn the other way this mark teaches first angle, the
    # opposite of what the course teaches. The circle diameters equal the
    # frustum's two ends, so the pair really is one solid in two views.
    "thirdangle": '<circle cx="9" cy="16" r="7.5"/><circle cx="9" cy="16" r="4.2"/>'
                  '<path d="M19.5 11.8l9.5-3.3v15l-9.5-3.3z"/>',
    # outline, centre, hidden, dimension. The patterns divide into the 24-unit
    # run so each line starts and ends on a full dash, and the outline is drawn
    # heavier than the rest because that is half of what tells them apart.
    "linetypes": '<path d="M4 6.25h24" stroke-width="2"/>'
                 '<path d="M4 12.75h24" stroke-dasharray="5 1.5 1.5 1.5" '
                 'stroke-linecap="butt" stroke-width="1.2"/>'
                 '<path d="M4 19.25h24" stroke-dasharray="3.6 1.5" '
                 'stroke-linecap="butt" stroke-width="1.2"/>'
                 '<path d="M4 25.75h24M4 25.75l3-1M4 25.75l3 1'
                 'M28 25.75l-3-1M28 25.75l-3 1" stroke-width="1.2"/>',
    # an idler pressed onto the belt. The belt is a band around both pulleys
    # rather than two tangent lines, so the wheels stay wheels.
    "idler": '<path d="M7 16.5h18a5.5 5.5 0 0 1 0 11H7a5.5 5.5 0 0 1 0-11z"/>'
             '<circle cx="7" cy="22" r="3"/><circle cx="25" cy="22" r="3"/>'
             '<circle cx="16" cy="12" r="3.5"/><path d="M16 4.5v3"/>',
    # slip is relative displacement, so it is drawn as two marks that no longer
    # line up and an arrow measuring the offset.
    "slip": '<circle cx="16" cy="20" r="7"/><path d="M3 11h26M3 13h26"/>'
            '<path d="M16 13v4"/><path d="M21 11v2"/>'
            '<path d="M16 7.5h6M22 7.5l-3-1M22 7.5l-3 1"/>',
    # a conveyor bed carrying a load. Rollers sit inside the bed so this does
    # not end up the same two-circles silhouette as the idler mark.
    "conveyor": '<rect x="3" y="19" width="26" height="4"/>'
                '<circle cx="8" cy="21" r="1.4"/><circle cx="24" cy="21" r="1.4"/>'
                '<rect x="11" y="10" width="10" height="9"/>'
                '<path d="M22 14.5h6M28 14.5l-3-1M28 14.5l-3 1"/>',
    # a V-belt wedged in its sheave groove — where the power actually crosses
    # and where the wear happens. A dial gauge would be generic clip art from
    # another vocabulary entirely.
    "wedge": '<path d="M5 5l8 22M27 5l-8 22M13 27h6"/>'
             '<path d="M8.4 11h15.2l-4.35 12h-6.5z"/>',

    # ---- coordinates and lines -------------------------------------------
    # a point measured from the origin along both axes
    "abscoord": '<path d="M4 4v24h24"/><path d="M4 12h13.5M22 28V14.5" '
                'stroke-dasharray="3 2" stroke-linecap="butt"/>'
                '<circle cx="22" cy="12" r="2.2"/>',
    # how far from the point before it, not from the origin
    "relcoord": '<circle cx="6" cy="24" r="2.2"/><circle cx="26" cy="9" r="2.2"/>'
                '<path d="M8.6 22.1L23.2 11.1M23.2 11.1l-3.4.3M23.2 11.1l.4 3.3"/>',
    # a distance at an angle
    "polarcoord": '<circle cx="5" cy="26" r="2.2"/><path d="M7.6 24.4L27 10"/>'
                  '<path d="M5 26h22"/><path d="M18 26a13 13 0 0 0-3.1-8.3"/>',
    # one closed outline, selected as a whole
    "polyline": '<path d="M4 26V9l7-5h13v22z"/>'
                '<rect x="2" y="24" width="4" height="4"/><rect x="22" y="2" width="4" height="4"/>',
    # separate pieces, each handled on its own
    "segments": '<path d="M4 8h9M17 8h11"/><path d="M4 16h20"/><path d="M9 24h19"/>',
    # the coordinate system itself
    "origin": '<path d="M7 25V7M7 25h18"/><path d="M7 7l-2.2 4M7 7l2.2 4M25 25l-4-2.2M25 25l-4 2.2"/>'
              '<rect x="4" y="22" width="6" height="6"/>',

    # ---- circles and editing ---------------------------------------------
    "circle": '<circle cx="16" cy="16" r="10"/><path d="M16 12.5v7M12.5 16h7"/>'
              '<path d="M16 16l7.1-7.1" stroke-dasharray="3 2" stroke-linecap="butt"/>',
    # a line touching a circle at exactly one point
    "tangentline": '<circle cx="12" cy="20" r="7.5"/><path d="M3 12.5h26"/>'
                   '<path d="M12 12.5v7.5" stroke-dasharray="2 1.6" stroke-linecap="butt"/>'
                   '<path d="M9.5 20h5M12 17.5v5"/>',
    # the same outline repeated at a fixed distance
    "offset": '<path d="M6 25V12l6-5h9v18z"/><path d="M2 28V10l8-7h15v25z"/>',
    # a corner rounded off
    "fillet": '<path d="M5 27V16a8 8 0 0 1 8-8h14"/>'
              '<path d="M5 8h8M13 8v8" stroke-dasharray="2.5 2" stroke-linecap="butt"/>',
    # a corner cut at forty-five degrees
    "chamfer": '<path d="M5 27V16l8-8h14"/>'
               '<path d="M5 8h8M13 8v8" stroke-dasharray="2.5 2" stroke-linecap="butt"/>',
    # four holes spaced evenly round a pitch circle
    "polararray": '<circle cx="16" cy="16" r="10" stroke-dasharray="5 1.5 1.5 1.5" '
                  'stroke-linecap="butt"/><circle cx="16" cy="6" r="2.6"/>'
                  '<circle cx="26" cy="16" r="2.6"/><circle cx="16" cy="26" r="2.6"/>'
                  '<circle cx="6" cy="16" r="2.6"/>',
    # what is past the cutting edge goes
    "trim": '<path d="M16 3v26"/><path d="M4 11h10"/>'
            '<path d="M18 11h10" stroke-dasharray="2.5 2.5" stroke-linecap="butt"/>'
            '<path d="M4 21h10"/>'
            '<path d="M18 21h10" stroke-dasharray="2.5 2.5" stroke-linecap="butt"/>',
    # the same shape the other way round a centre line
    "mirror": '<path d="M4 26V12l7-6v20z"/><path d="M28 26V12l-7-6v20z"/>'
              '<path d="M16 3v26" stroke-dasharray="5 1.5 1.5 1.5" stroke-linecap="butt"/>',
    # one edge pulled, the rest holding
    "stretch": '<path d="M4 9h14v14H4z"/><path d="M18 16h9M27 16l-3-1M27 16l-3 1"/>'
               '<path d="M28 7v18" stroke-dasharray="2.5 2" stroke-linecap="butt"/>',

    # ---- views and representation ----------------------------------------
    # lines carried from one view into the next
    "viewlines": '<rect x="4" y="18" width="13" height="10"/>'
                 '<path d="M4 15V5M17 15V5" stroke-dasharray="2.5 2" stroke-linecap="butt"/>'
                 '<path d="M20 18h9M20 28h9" stroke-dasharray="2.5 2" stroke-linecap="butt"/>'
                 '<rect x="22" y="18" width="7" height="10"/>',
    # what is there but cannot be seen
    "hiddenline": '<rect x="4" y="7" width="24" height="18"/>'
                  '<circle cx="16" cy="16" r="6" stroke-dasharray="3 1.8" stroke-linecap="butt"/>',
    # every line on its own sheet
    "layers": '<path d="M4 21l12-5 12 5-12 5z"/><path d="M4 15l12-5 12 5"/><path d="M4 9l12-5 12 5"/>',
    # the frame that carries a geometric tolerance
    "gdt": '<rect x="2" y="11" width="28" height="10"/><path d="M11 11v10M22 11v10"/>'
           '<circle cx="6.5" cy="16" r="3"/><path d="M6.5 11.5v9M2 16h9"/>',
    # a cut face, hatched
    "material": '<path d="M5 8h22v16H5z"/>'
                '<path d="M7 24l8-8M7 18l10-10M13 24l10-10M19 24l8-8M25 24l2-2"/>',
    # the hardened skin a heat treatment leaves on a cut face
    "hardening": '<rect x="4" y="8" width="24" height="16"/><path d="M4 13h24"/>'
                 '<path d="M7 8v5M10 8v5M13 8v5M16 8v5M19 8v5M22 8v5M25 8v5"/>',

    # ---- dimensioning and release ----------------------------------------
    # a diameter pulled out on a leader
    "dimdia": '<circle cx="12" cy="19" r="8"/><path d="M12 19l5.7-5.7L23 8h6"/>'
              '<path d="M17.7 13.3l.3-3.3M17.7 13.3l3.3-.3"/>',
    # the angle between two lines
    "dimangle": '<path d="M4 27h25M4 27L25 8"/>'
                '<path d="M20 27a16 16 0 0 0-4.4-11"/>'
                '<path d="M20 27l-1.4-3M20 27l3-1.2"/>',
    # the sheet leaving for paper
    "plot": '<rect x="3" y="6" width="17" height="20"/><path d="M6 11h11M6 15h11M6 19h7"/>'
            '<path d="M21 16h8M29 16l-3.2-1.8M29 16l-3.2 1.8"/>',
}


# AutoCAD commands the course actually uses, keyed by what a learner types.
# Each entry is (full name, what it does, when you reach for it). The last field
# is the one that matters outside the exam: a technician who only ever draws the
# exam part will not remember a command, but one who knows the situation will.
#
# A script may only use commands listed here. `beats.shortcuts_in` looks up what
# the steps type, and an unknown entry stops the build rather than quietly
# leaving a gap in the summary table.
COMMANDS = {
    "L": ("LINE", "선을 긋는다", "낱개로 다뤄야 하는 조각. 뒤에 자르거나 둥글릴 선"),
    "PL": ("PLINE", "이어진 선을 하나의 객체로 긋는다",
           "한 바퀴 도는 윤곽. 레이아웃에서 영역 넓이를 재거나 통째로 옮길 때"),
    "C": ("CIRCLE", "원을 그린다", "구멍, 축, 피치원"),
    "REC": ("RECTANG", "직사각형을 폴리선으로 그린다", "도면틀, 표제란, 판재 외곽"),
    "XL": ("XLINE", "무한히 뻗는 구성선을 긋는다", "투상선. 도면에 남기지 않고 뷰를 맞출 때"),
    "O": ("OFFSET", "일정 거리만큼 떨어진 같은 모양을 만든다",
          "중심을 다시 찍지 않고 동심원·평행선. 벽체 두께, 여유 간격"),
    "TR": ("TRIM", "경계까지 잘라낸다", "겹친 선, 튀어나온 토막"),
    "EX": ("EXTEND", "경계까지 늘린다", "교차점에 못 미친 선"),
    "F": ("FILLET", "두 선 사이에 라운드를 넣는다", "응력이 몰리는 안쪽 모서리. 반지름 0이면 각지게 잇는다"),
    "MI": ("MIRROR", "대칭으로 복사한다", "좌우 대칭 형상. 한 번만 그리고 뒤집는다"),
    "CO": ("COPY", "같은 것을 다른 자리에 둔다", "반복되는 부품, 같은 구멍"),
    "M": ("MOVE", "옮긴다", "뷰 배치를 다시 잡을 때"),
    "E": ("ERASE", "지운다", "보조선 정리"),
    "ARRAYPOLAR": ("ARRAYPOLAR", "중심을 두고 원형으로 배열한다", "볼트 구멍처럼 각도로 균등 배치된 것"),
    "MA": ("MATCHPROP", "특성을 다른 객체에 복사한다", "레이어가 틀린 선을 다시 그리지 않고 옮길 때"),
    "LA": ("LAYER", "레이어를 만들고 관리한다", "선 종류·색상을 개체가 아니라 레이어로 정할 때"),
    "OS": ("OSNAP", "객체 스냅 항목을 정한다", "끝점·중심·접점을 정확히 잡아야 할 때"),
    "Z": ("ZOOM", "화면 배율을 바꾼다", "스냅이 어디 붙었는지 봐야 할 때는 크게"),
    "D": ("DIMSTYLE", "치수 스타일을 정한다", "문자 높이·화살표·소수 자릿수를 도면 축척에 맞출 때"),
    "DLI": ("DIMLINEAR", "수평·수직 치수를 넣는다", "가로 세로로 잰 값"),
    "DAL": ("DIMALIGNED", "기울어진 변에 나란한 치수를 넣는다", "경사면의 실제 길이"),
    "DDI": ("DIMDIAMETER", "지름 치수를 넣는다", "원과 구멍"),
    "DRA": ("DIMRADIUS", "반지름 치수를 넣는다", "라운드와 호"),
    "DAN": ("DIMANGULAR", "각도 치수를 넣는다", "두 선 사이의 각"),
    "MLEADER": ("MLEADER", "지시선과 문자를 넣는다", "도형 밖에서 끌어와 설명할 때"),
    "DIMEDIT": ("DIMEDIT", "이미 넣은 치수의 문자를 고친다", "참고 치수 괄호, 접두어"),
    "DTEXT": ("DTEXT", "문자를 쓴다", "표제란, 주석"),
    "LTSCALE": ("LTSCALE", "도면 전체의 선 종류 축척을 바꾼다", "점선이 실선처럼 보일 때"),
    "QSELECT": ("QSELECT", "조건에 맞는 객체를 한 번에 고른다", "구성선만 골라 지울 때"),
    "UCS": ("UCS", "좌표 원점과 방향을 옮긴다", "도면 안 특정 자리를 0,0 으로 삼을 때"),
    "LIMITS": ("LIMITS", "도면 한계를 정한다", "용지 크기를 좌표로 잡을 때"),
    "UNITS": ("UNITS", "단위와 정밀도를 정한다", "밀리미터인지 인치인지 확인"),
    "LINETYPE": ("LINETYPE", "선 종류를 불러온다", "CENTER·HIDDEN 을 레이어에 지정하기 전"),
    "OPEN": ("OPEN", "파일을 연다", "매 차시 지난 상태에서 이어 그릴 때"),
    "SAVEAS": ("SAVEAS", "새 이름으로 저장한다", "차시 종료 상태를 남길 때"),
    "PLOT": ("PLOT", "출력한다", "종이나 PDF 로 내보낼 때"),
    "EXPORTPDF": ("EXPORTPDF", "PDF 로 내보낸다", "제출용 파일"),
    "LI": ("LIST", "객체의 정보를 보여준다", "그린 것이 정말 그 값인지 검산할 때"),
    "DI": ("DIST", "두 점 사이 거리를 잰다", "치수를 넣기 전 확인"),
    "LIST": ("LIST", "객체의 정보를 보여준다", "그린 것이 정말 그 값인지 검산할 때"),
    "LAYER": ("LAYER", "레이어를 만들고 관리한다", "선 종류·색상을 개체가 아니라 레이어로 정할 때"),
    "QSAVE": ("QSAVE", "덮어써 저장한다", "Ctrl+S 와 같다"),
    # System variables. Typed at the prompt like a command, so a learner meets
    # them the same way, but they set a value rather than doing something.
    "CLAYER": ("CLAYER", "현재 레이어를 바꾼다", "명령행으로 레이어를 바꿀 때. 드롭다운과 같은 일"),
    "UCSICON": ("UCSICON", "좌표계 아이콘 표시를 정한다", "옮긴 원점이 어디인지 눈으로 확인할 때"),
    "LWDISPLAY": ("LWDISPLAY", "선가중치를 화면에 보일지 정한다", "굵기 차이를 화면에서 확인할 때"),
    "MIRRTEXT": ("MIRRTEXT", "대칭할 때 문자를 뒤집을지 정한다", "문자가 포함된 것을 대칭 복사하기 전"),
}

# Backticked in the scripts but not something typed at a prompt — a fit grade,
# a value, a file name.
NOT_COMMANDS = {"H7"}

# Typed inside a running command as an option or a snap, not on a blank prompt.
OPTION_KEYS = {"A", "W", "N", "V", "H", "R", "S", "U", "X", "I", "OR", "ON",
               "ALL", "AS", "FROM", "TAN", "CENTER", "HIDDEN", "RE", "SELECT"}

FUNCTION_KEYS = [
    ("F3", "객체 스냅", "끝점·중심·접점에 붙는다. 꺼져 있으면 눈대중이 된다"),
    ("F8", "직교", "수평 수직으로만 움직인다"),
    ("F10", "극좌표 추적", "정해진 각도마다 안내선이 뜬다"),
    ("Ctrl+1", "특성 창", "고른 객체의 레이어·선종류 축척을 그 자리에서 고친다"),
    ("Ctrl+S", "저장", "명령 한 번 끝날 때마다 눌러 두면 잃을 것이 없다"),
    ("Ctrl+Z", "실행 취소", "명령 밖에서. 명령 안에서는 U"),
]


def icon(name, size=46):
    """A card's mark. Sized in the card, coloured by the card's own colour, so
    the read-along tint carries it without a second tween."""
    return ('<svg class="ico" viewBox="0 0 32 32" width="%d" height="%d" '
            'aria-hidden="true">%s</svg>' % (size, size, ICONS[name]))


_SVG_BLOCK = re.compile(r"<svg[ >].*?</svg>", re.S | re.I)
_TAG = re.compile(r"<[^>]*>")
_HANGUL = re.compile(r"[가-힣]{2,}")


def keep_words(html):
    """Wrap every 어절 that contains Hangul in a nowrap span.

    `word-break: keep-all` is the correct way to say this, and in a browser it
    works — the same markup wraps 「모여서 / 본다」 in Chrome. The renderer does
    not honour it: its snapshot of the very same frame put 「…모여서 본」 on one
    line and 「다」 on the next, splitting the word mid-syllable, which reads as
    a typo. `white-space: nowrap` does survive the renderer, so the rule is
    expressed per word instead of per block.

    The declaration stays in BASE_CSS as well — it is the correct statement of
    intent, and it is what governs anything a browser renders directly.

    SVG is skipped whole: a `<span>` inside `<text>` is not valid there, and
    the drawing has no prose to break anyway.
    """
    keep, out = [], []

    def stash(m):
        keep.append(m.group(0))
        return "@@%d@@" % (len(keep) - 1)

    html = _SVG_BLOCK.sub(stash, html)
    pos = 0
    for m in _TAG.finditer(html):
        out.append(_wrap_text(html[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_wrap_text(html[pos:]))
    text = "".join(out)
    for i, block in enumerate(keep):
        text = text.replace("@@%d@@" % i, block)
    return text


_WS = re.compile(r"(\s+)")


def _wrap_text(run):
    """Split on whitespace, keeping it: a run can carry the newlines and indent
    the builders join their fragments with, and folding those into a span would
    turn a line break into a space inside a word."""
    if not run or "@@" in run or not _HANGUL.search(run):
        return run
    return "".join(part if _WS.fullmatch(part) or not _HANGUL.search(part)
                   else '<span class="kw">%s</span>' % part
                   for part in _WS.split(run))


def frame_html(comp_id, duration, body, timeline):
    """Wrap a sub-composition.

    The root id is composition-scoped. A bare id="root" collides with
    index.html and with every other frame on the assembled page, and lint does
    not catch that.
    """
    body = keep_words(body)
    return (HEAD
            + '  <div id="' + comp_id + '-root" data-composition-id="' + comp_id
            + '" data-start="0" data-duration="' + str(duration)
            + '" data-width="1920" data-height="1080">\n'
            + '    <section id="' + comp_id + '" class="clip" data-start="0" data-duration="'
            + str(duration) + '" data-track-index="1">\n' + body + '\n    </section>\n  </div>\n'
            + '  <script>\n    window.__timelines=window.__timelines||{};\n'
            + '    const tl=gsap.timeline({paused:true});\n' + timeline
            + '\n    window.__timelines["' + comp_id + '"]=tl;\n  </script>\n' + TAIL)


def header(index, title, prompt):
    return ('      <header class="topline"><div><div class="index">' + index + '</div><h1>'
            + title + '</h1></div><div class="prompt">' + prompt + '</div></header>')


def title_card(comp_id, duration, subject, sub):
    """LESSON_STYLE.md section 8: every lesson opens on this card."""
    body = ('      <div class="title">'
            '<div class="brand">LG이노텍 &nbsp;·&nbsp; for technician</div>'
            '<div class="cert">「 Green Star 」 테크니션 인증제 · 실습과정</div>'
            '<h2>' + subject + '</h2><div class="rule"></div>'
            '<div class="sub">' + sub + '</div></div>')
    # Cues sit at fractions of the card, not at fixed seconds. Hard-coded times
    # gave a three-second script and a ten-second one exactly the same motion,
    # and both finished inside the first two seconds and then held.
    s = '#' + comp_id
    d = float(duration)

    def at(f):
        return round(d * f, 2)

    tl = ('    tl.fromTo("' + s + ' .brand",{opacity:0,y:14},{opacity:1,y:0,duration:1.0,'
          'ease:"power3.out"},' + str(at(.07)) + ');\n'
          '    tl.fromTo("' + s + ' .cert",{opacity:0,y:14},{opacity:1,y:0,duration:1.0,'
          'ease:"power3.out"},' + str(at(.17)) + ');\n'
          '    tl.fromTo("' + s + ' h2",{opacity:0,y:24},{opacity:1,y:0,duration:1.3,'
          'ease:"power3.out"},' + str(at(.33)) + ');\n'
          '    tl.fromTo("' + s + ' .rule",{scaleX:0,transformOrigin:"left center"},'
          '{scaleX:1,duration:1.0,ease:"power2.inOut"},' + str(at(.46)) + ');\n'
          '    tl.fromTo("' + s + ' .sub",{opacity:0,y:10},{opacity:1,y:0,duration:1.0,'
          'ease:"power2.out"},' + str(at(.53)) + ');\n'
          # No standing drift. A slow y tween across the whole card keeps the
          # text creeping after it has landed, which reads as the letters not
          # having settled rather than as the card being alive.
          '    tl.to("' + s + ' .brand,' + s + ' .cert,' + s + ' h2,' + s + ' .rule,' + s
          + ' .sub",{opacity:0,duration:.8,ease:"power2.in"},' + str(round(d - .95, 2)) + ');')
    return frame_html(comp_id, duration, body, tl)


def closing_card(comp_id, duration, spans, next_no=None, next_title=None, final=None):
    """The sign-off. Same dark ground as the title card, so a lesson opens and
    closes on the same footing and the recap is not the last thing on screen.

    The rule sits above the heading here and below it on the title card — the
    one difference that makes this read as a close rather than another open.

    next_no/next_title name the lesson to come. A lesson with nothing after it
    passes `final` instead.
    """
    import beats

    if final:
        tail = final
    else:
        # The particle attaches to the noun: 「…출도입니다」, not 「…출도 입니다」.
        # Both halves ride in one nowrap span — with no space between them a
        # line could otherwise break between 도 and 입.
        tail = ('다음은 <span class="kw"><em>%d차시 · %s</em>입니다</span><br>'
                '그때 다시 뵙겠습니다' % (next_no, next_title))
    body = ('      <div class="close"><div class="rule"></div>'
            '<h2>고생하셨습니다</h2>'
            '<div class="next">' + tail + '</div>'
            '<div class="brand">LG이노텍 &nbsp;·&nbsp; for technician</div></div>')

    bs = beats.beat_spans(spans)
    at1 = bs[0][1] if bs else 1.0
    at2 = bs[1][1] if len(bs) > 1 else at1 + 2.5
    s = '#' + comp_id
    tl = ('    tl.fromTo("' + s + ' .rule",{scaleX:0,transformOrigin:"left center"},'
          '{scaleX:1,duration:1.0,ease:"power2.inOut"},' + str(round(at1 - 0.8, 2)) + ');\n'
          '    tl.fromTo("' + s + ' h2",{opacity:0,y:22},{opacity:1,y:0,duration:1.2,'
          'ease:"power3.out"},' + str(round(at1, 2)) + ');\n'
          '    tl.fromTo("' + s + ' .next",{opacity:0,y:14},{opacity:1,y:0,duration:1.0,'
          'ease:"power2.out"},' + str(round(at2, 2)) + ');\n'
          '    tl.fromTo("' + s + ' .brand",{opacity:0},{opacity:1,duration:1.0},'
          + str(round(at2 + 1.2, 2)) + ');\n'
          '    tl.to("' + s + ' .rule,' + s + ' h2,' + s + ' .next,' + s
          + ' .brand",{opacity:0,duration:.9,ease:"power2.in"},'
          + str(round(duration - 1.05, 2)) + ');')
    return frame_html(comp_id, duration, body, tl)


def recap_card(comp_id, duration, index, title, prompt, learned, nxt, spans):
    """LESSON_STYLE.md section 8: the closing frame is two panels, never three.

    learned and nxt are (eyebrow, heading, [line, ...]).

    spans comes from the script: beat 1 is the left panel, beat 2 the right. The
    bullets inside a panel are spread across that panel's own span, so they land
    with the sentences that describe them instead of all arriving in the first
    second and then sitting still for half a minute.
    """
    import beats

    def panel(cls, spec):
        eyebrow, heading, items = spec
        lis = "".join('<li class="%s-li">%s</li>' % (cls, t) for t in items)
        return ('<section class="card ' + cls + '" style="padding:30px 34px"><b>' + eyebrow
                + '</b><strong>' + heading + '</strong>'
                + '<ul style="margin:14px 0 0;padding-left:1.1em;color:#666;font-size:22px;'
                  'line-height:1.55">' + lis + '</ul></section>')

    body = (header(index, title, prompt)
            + '\n      <main class="body" style="grid-template-columns:repeat(2,minmax(0,1fr))">'
            + panel("p-done", learned)
            + panel("p-next", nxt) + '</main>')

    bs = beats.beat_spans(spans)
    tl = [beats.chrome(comp_id)]
    for (idx, a, b), (cls, lines) in zip(bs, (("p-done", learned[2]), ("p-next", nxt[2]))):
        tl.append('    tl.fromTo("#%s .%s",{opacity:0,y:26},{opacity:1,y:0,duration:1.0,'
                  'ease:"power3.out"},%s);' % (comp_id, cls, a))
        step = max((b - a - 1.4) / max(len(lines), 1), 0.9)
        tl.append('    tl.fromTo("#%s .%s-li",{opacity:0,x:18},{opacity:1,x:0,duration:.8,'
                  'stagger:%s,ease:"power2.out"},%s);'
                  % (comp_id, cls, round(step, 2), round(a + 0.9, 2)))
    tl.append(beats.outro(comp_id, duration))
    return frame_html(comp_id, duration, body, "\n".join(tl))


def index_html(slots, total):
    """slots: [(slot_id, comp_id, file_stem, start, duration), ...]"""
    rows = "\n".join(
        '  <div id="' + sid + '" class="clip" data-composition-id="' + cid
        + '" data-composition-src="compositions/frames/' + name + '.html"'
        + ' data-start="' + str(start) + '" data-duration="' + str(dur)
        + '" data-track-index="1" data-width="1920" data-height="1080"></div>'
        for sid, cid, name, start, dur in slots)
    return ('<!DOCTYPE html>\n<html lang="ko"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=1920, height=1080">'
            '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>\n'
            '  *{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;'
            'overflow:hidden;background:#FFFFFF}#root{position:relative;width:1920px;height:1080px;'
            'overflow:hidden}#root>[data-composition-src]{position:absolute;inset:0}\n'
            '</style></head><body>'
            '<div id="root" data-composition-id="main" data-start="0" data-duration="' + str(total)
            + '" data-width="1920" data-height="1080">\n' + rows + "\n</div>\n"
            '<script>window.__timelines=window.__timelines||{};'
            'window.__timelines["main"]=gsap.timeline({paused:true});</script>\n'
            "</body></html>\n")


def write_project(lesson_dir, name, slots, total, os_mod, json_mod):
    """Emit index.html and the three project files with LF endings."""
    def put(path, text):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    put(os_mod.path.join(lesson_dir, "index.html"), index_html(slots, total))
    put(os_mod.path.join(lesson_dir, "hyperframes.json"), json_mod.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True},
        "authoringSkill": "general-video",
    }, indent=2, ensure_ascii=False) + "\n")
    put(os_mod.path.join(lesson_dir, "meta.json"),
        json_mod.dumps({"id": name, "name": name}, indent=2, ensure_ascii=False) + "\n")
    put(os_mod.path.join(lesson_dir, "package.json"), json_mod.dumps({
        "name": name, "private": True, "type": "module",
        "scripts": {
            "dev": "npx --yes hyperframes@0.7.111 preview",
            "check": "npx --yes hyperframes@0.7.111 check",
            "render": "npx --yes hyperframes@0.7.111 render",
            "publish": "npx --yes hyperframes@0.7.111 publish",
        },
    }, indent=2, ensure_ascii=False) + "\n")
