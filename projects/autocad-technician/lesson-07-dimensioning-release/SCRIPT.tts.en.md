<!-- 생성물이다. 손으로 고치지 말고 원본 SCRIPT.en.md 를 고친 뒤 다시 뽑아라.
     python scripts/part/tts_script.py lesson-07-dimensioning-release
     태그: asking · calm · cautionary · emphatic · light · measured · pointing · warm -->
# SCRIPT — AutoCAD Technician Lesson 7 · Dimensioning and release (English edition)

**Part:** `EDU-IB-02 idler pulley bracket`<br>
**Checkpoint:** `L06_REPRESENTED → L07_RELEASE`<br>
**Voice:** Windows SAPI · Microsoft Zira Desktop · Rate 0 · pitch-preserving 1.15x<br>
**Voice direction:** Dimensioning is not drawing; it is instructing. Keep it level. Through the hands-on section, leave a beat as if pointing at each dialog entry in turn.

> Length not measured yet. The times below mirror the Korean script so the frames
> line up; they are replaced by measured values once the English speech exists.
> The parentheses name what lights up on screen at that moment. They are not read.

## Line 1 — Title (Frame 1)

**Time:** 0:00–0:05

    (silence)

    [calm] Lesson 7, dimensioning and release.

## Line 2 — What you draw today (Frame 2)

**Time:** 0:05–1:57

    [calm] The shape was finished last lesson and the lines are where they belong. [calm] But hand this drawing to the floor as it stands and nobody can make anything. [calm] Because how big it is is not written on it.

    [calm] An LG Innotek machine has stopped and a spare part is urgent. [calm] It is a part that preventive maintenance, PM, did not cover in advance. [calm] You find the part in the assembly drawing and take that drawing to the machine shop to talk it over. [calm] At that moment you need not just the shape but exact dimension values. [calm] The idler pulley bracket for a car engine that you draw today goes over the same way. [cautionary] One wrong number comes back as rework loss. [calm] Today you put dimensions on the drawing and export it as a file.

    (1 card — making a dimension style) [pointing] There is something to do before you put a number up. [calm] You settle what shape that number will come out in. [calm] How large to write the text. [calm] How large to make the arrowheads. [calm] How many decimal places to show. [calm] The place where those three are gathered is the dimension style. [calm] Settle it first and the dozens of dimensions you add afterwards all come out the same. [calm] Start entering without settling it and you end up catching each one later to fix it.

    (2 card — entering dimensions) [pointing] Then you put the values up one at a time, starting from the overall size. [calm] The boss centre, the slots, diameters and radii, the pitch circle and the angle. [calm] Here you have to judge what you are measuring first. [calm] There is a separate command for measuring across and down. [calm] There are separate commands for a sloped face, for a circle, and for an angle. [calm] You choose the command to match what you are measuring.

    (3 card — reference dimensions and counts) [cautionary] Some notations do not carry their meaning as a number alone. [calm] That there are four of the same hole. [cautionary] That a value is for reference only and must not be inspected. [calm] You put a count in front, and you put brackets round it. [calm] What will not fit inside the shape you pull out with a leader and write outside.

    (4 card — checking the scale and exporting) [pointing] Last you check the drawing against the paper size and export it as a PDF. [calm] It can look right on screen and be out on paper. [calm] The screen zooms as you like, but paper has a fixed size. [calm] You check the scale yourself in the plot dialog. [calm] The PDF you make this way is the drawing that goes to the floor.

## Line 3 — Concepts (Frame 3)

**Time:** 1:57–3:55

    [calm] Four things to settle before you press a command.

    (1 card — what the dimension style settles) [pointing] You open the dimension style with the DIMSTYLE command. [calm] Three of the things you set here are used straight away in today's exercise. [calm] Text height, arrow size, and decimal places. [calm] Text height decides whether it is readable when printed on paper. [calm] You match the arrow size to roughly the text height. [asking] What happens if the two are badly out of step? [calm] One dimension looks as if it were pasted in from another drawing. [calm] Decimal places change how the value itself appears. [measured] Leave it at 0 and this part's 95.7 comes out as 96. [measured] Set it to one and everything else comes out like 120.0.

    (2 card — five kinds of dimension) [pointing] You use five commands according to what you are measuring. [calm] Linear dimension, DIMLINEAR, measures a horizontal or a vertical distance. [calm] Aligned dimension, DIMALIGNED, measures the real distance between two points. [calm] That is the length of the sloped face itself. [calm] Diameter dimension, DIMDIAMETER, marks a circle's diameter. [calm] Radius dimension, DIMRADIUS, marks an arc's radius. [calm] Angular dimension, DIMANGULAR, measures the angle between two lines. [calm] You also have to tell whether a circle takes a diameter or a radius. [calm] On this drawing the bore and the boss are instructed by diameter, the fillets and the slot end arcs by radius. [calm] The command will let you put a diameter on an arc, but you follow this drawing's notation standard.

    (3 card — leaders) [pointing] You draw a leader with the MLEADER command. [calm] It points at the shape with an arrowhead. [calm] It pulls a line outward and you write at the end of it. [asking] Why is it needed? [calm] First, when the shape is small. [calm] Put a dimension line inside it and nothing can be seen. [calm] Second, when what you have to write is not a single number. [calm] A tapped hole has to carry count, thread and depth on one line. [calm] One dimension line will not hold that.

    (4 card — the brackets on a reference dimension) [pointing] Put brackets round a value and it means a reference dimension. [calm] It is a value computed from other dimensions. [calm] It instructs you to use it while making but not to measure it on inspection. [asking] Then why put it on the drawing at all? [calm] So the reader does not have to compute it every time. [calm] When you see brackets, know it is a value excluded from inspection. [measured] On this drawing, the 95.7 between the two fillet centres is the one.

## Line 4 — On the drawing (Frame 4)

**Time:** 3:55–7:22

    [calm] Now we go through this part's values one at a time. [calm] Something matters more than which value it is. [calm] It is where you measure from and to. [measured] Even for the same 120, two different points caught means a different object comes out.

    (1 row) [measured] The overall size, 120 and 90. [measured] The 120 is from the left end of the base's bottom to its right end. [calm] You measure it on the bottom edge, not the top one. [calm] The top edge has had its left and right corners cut away by the chamfers. [calm] Its endpoints are not where they originally were. [calm] The 90 is from the bottom to the very top of the part. [asking] And where is that top? [calm] The top of the boss circle. [calm] The boss centre is 62 from the bottom. [measured] The radius is half of 56, which is 28. [measured] 62 plus 28 is 90. [calm] So the second point of the 90 is the circle's top quadrant. [calm] Pick a corner and the value changes.

    (2 row) [measured] The boss centre, 60 and 62. [calm] 60 across from the left end. [calm] 62 up from the bottom. [calm] Both are measured from the part's left edge and its bottom edge. [asking] Why gather the references onto these two faces? [calm] Move your reference about and each dimension's error piles onto the next. [emphatic] Measure everything from one face and only that one face has to be right. [calm] Everything else lands where it belongs. [calm] These two values fix where the shaft sits.

    (3 row) [measured] The long horizontal holes at the bottom — the slot dimensions 29, 50, 12 and 8. [calm] A slot has no corner, so there is no point to catch. [calm] So you measure from the end circle centres. [calm] From the left end to the first end circle centre is 29. [calm] Within one slot, between the two end circle centres is 12. [calm] From the left slot's first end circle to the right slot's first end circle is 50. [calm] From the bottom, the end circle centre height is 8. [calm] Those four values fix the positions of both slots completely. [cautionary] You do not write the width of 10 separately. [calm] Two end circles of radius 5 already fix the width. [calm] Write 10 as well and the same thing is said twice.

    (4 row) [light] Diameters and radii. [measured] Ø25 H7 is the bore. [calm] Ø56 is the outside of the boss. [calm] Both are whole circles, so they are written as diameters. [calm] R5 is the half-circle at the end of a slot. [calm] R10 is the fillet where the web turns into the base. [calm] Both are arcs, parts of a circle, so they are written as radii. [calm] And these four have their dimension lines running outside the shape. [calm] It is because the inside of a circle is too narrow to hold a dimension line and its text. [calm] Diameter and radius commands are built to pull the dimension outward.

    (5 row) [measured] PCD Ø44 and 45 degrees. [calm] PCD is the pitch circle diameter. [calm] The pitch circle is not a shape that actually gets cut. [calm] It is an imaginary circle the four tapped-hole centres sit on. [calm] So you draw it as a centerline. [calm] You put PCD in front of the diameter to show that it is not a hole. [asking] How does it read without PCD? [calm] It reads as one more hole, 44 across. [calm] The 45 degrees is the angle at which the first hole sits on that circle. [calm] It is 45 degrees up from the horizontal line through the boss centre. [calm] The other three step round from there every 90. [calm] Here you use the angular dimension's two-line selection method.

    (6 row) [measured] The reference dimension 95.7, and the thicknesses 12 and 20. [measured] The 95.7 is the distance between the two fillet centres. [calm] You put brackets round this one. [calm] It is a value that follows from the fillets' radius of 10 and the slope of the web lines. [calm] So it comes out as a decimal. [calm] Being a decimal is not what makes it a reference dimension. [calm] On this drawing it is a duplicate value determined by other dimensions, so it is left as reference. [calm] The same fillets' centre height of 26, on the other hand, is written plainly with no brackets. [light] And the two thicknesses. [calm] You cannot read thickness in the front view. [calm] It runs front to back, so from the front it all overlaps into one line. [calm] You measure it in the top view. [light] The plate is 12. [measured] Where the boss stands 8 forward it is 12 plus 8, which is 20.

## Line 5 — Dimensioning and release · DEMO-01 screen recording (Frame 5)

**Time:** 7:22–25:36

> This section is a screen recording. Work through the 17 steps below **in order and without skipping**, speaking as you go.
> What is inside backticks is what you actually type. Rely on snaps when you place a point, and always check the value with your eyes once it appears.

### Step 1 — Open the previous file

    [light] Start AutoCAD. [measured] Type `OPEN` and press Enter. [light] Or Ctrl+O.
    [calm] Choose the file you saved last time. [calm] It is the file with the idler pulley bracket drawn up to Lesson 6. [light] Press Open.
    (`EDU-IB-02_L06_REPRESENTED.dwg`)
    [cautionary] You do not make a new one. [calm] You lay today's dimensions on top of the file that already holds the shape.
    [measured] `Z`, Enter, `A`, Enter. [light] That is zoom all. [calm] The border comes onto the screen too.

### Step 2 — Check the basic settings · snaps and ortho

    [calm] Press Esc twice to clear the command and the selection.
    [measured] Type `OS` and press Enter. [calm] Check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    [calm] Press OK to close the dialog. [emphatic] Press F3 to turn object snap on only if the status bar shows it off.
    [measured] `L`, Enter. [calm] While it asks for the first point, rest the cursor on the endpoint of an existing line. [cautionary] Do not click.
    [calm] Watch for the square marker, then press Esc twice to cancel LINE. [calm] If there is no marker, look at OS and F3 again.
    [emphatic] Look at ortho too, and press F8 to turn it on only if it is off. [calm] On diagonals and tangents you turn it off, as each step says.
    [calm] Catch a point on the shape itself and you notice at once when a value has gone out.

### Step 3 — Make the dimension line layer current

    [measured] Type `LAYER` and press Enter. [calm] The layer properties manager opens.
    [measured] Select the `Dimension line` row and press Set Current. [light] Close the dialog.
    [calm] See that the layer indicator at the top of the screen has changed to dimension line. [light] White, 7.

    [asking] Why do this before you enter any dimensions?
    [calm] To move them afterwards you would have to pick out every dimension you had entered.
    [calm] Dimensions overlap the visible lines, so catching them one by one catches shape lines with them.
    [calm] Changing it once before you draw is far better.

    [calm] Keep the layers apart and later you can turn off just the dimensions and look at the shape alone.
    [calm] That is how you use it when you check a machine's footprint on a drawing.
    [calm] With fewer lines overlapping, traffic routes and clashes come into view.

### Step 4 — Make a new dimension style

    [measured] Type `D` and press Enter. [calm] That is the DIMSTYLE command. [calm] The dimension style manager opens.
    [measured] Right now the style list will have only ISO-25 in it.
    [cautionary] You do not edit that one directly. [calm] You make a new one.
    [cautionary] Leave the original and you have something to compare against when a setting goes wrong.

    [light] Press the New button.
    [measured] For the new style name type `EDU-A3`.
    [measured] Leave start with as ISO-25. [calm] That means starting from it as a base.
    [calm] Leave use for as all dimensions.
    [light] Press Continue.

### Step 5 — Set text, arrows and decimal places, and make it current

    [calm] The new dimension style dialog opens. [calm] There are seven tabs across the top. [emphatic] You touch only four.

    [light] Open the Text tab.
    [measured] For text height type `5`.
    [calm] Leave text color as ByLayer. [calm] You already gave white, 7, on the layer.
    [calm] Leave text placement vertical above, horizontal centered. [calm] The number sits centred above the dimension line.

    [calm] Open the Symbols and Arrows tab.
    [calm] Leave the first arrowhead as closed filled. [calm] The second follows the first.
    [measured] For arrow size type `5`. [calm] It is the same value as the text height.
    [calm] Leave center marks as none. [cautionary] You do not lay an automatic mark over the centre marks from the earlier lesson.
    [calm] If the two are badly out of step, one dimension stands apart from the rest.

    [light] Open the Fit tab.
    [calm] Look at the scale for dimension features at the lower right. [measured] Check that use overall scale of is `1`.
    [measured] If this is not 1, a text height of 5 grows or shrinks by that multiple.
    [asking] Fix the text height as often as you like and the size on screen still will not match? [calm] Usually this value is the culprit.

    [calm] Open the Primary Units tab.
    [calm] The unit format is decimal. [measured] Leave the precision at `0` decimal places.
    [calm] This part's dimensions are all whole numbers apart from one reference dimension.
    [measured] Leave a decimal place and 120 comes out as 120.00.
    [measured] Leave the measurement scale factor at `1`.
    [calm] You drew at one to one in model space, so the measured value has to come out as it is.
    [light] Press OK.

    [calm] You are back at the dimension style manager.
    [measured] Select `EDU-A3` in the list and press Set Current. [calm] The current marker appears beside the name.
    [light] Press Close.
    [calm] Making one and using one are different things.
    [asking] What happens if you leave out Set Current?
    [measured] The style is made and the dimensions go in as ISO-25.

### Step 6 — The overall size, 120 and 90

    [measured] Type `DLI` and press Enter. [light] DIMLINEAR, the linear dimension.
    [calm] It asks for the first extension line origin.
    [calm] Put the mouse on the left end corner of the front view's base bottom.
    [calm] Click when the endpoint snap marker appears.
    [calm] It asks for the second origin. [calm] Click the bottom's right end corner the same way.
    [calm] It asks where to put the dimension line. [calm] Take the mouse down to an empty spot and click.
    [measured] 120 has gone in.
    [calm] You set the dimension line generously clear of the shape.
    [calm] Set it close and visible lines and dimension lines mix together.
    [calm] You cannot tell where the part ends and the explanation begins.

    [measured] `DLI`, Enter. [light] This time vertically.
    [calm] The first origin is the same point as before. [calm] The left end corner of the base bottom.
    [calm] The second origin is the very top of the boss circle.
    [calm] Put the mouse above the circle and the quadrant snap appears. [light] Click then.
    [calm] Put the dimension line in the empty space to the left of the drawing. [measured] 90 has gone in.
    [measured] Check that this 90 agrees with 62 plus 28.
    [cautionary] If a different value comes out, the dimension is not wrong. [light] The shape is.

### Step 7 — Base height 16 and boss centre 60, 62

    [measured] `DLI`, Enter.
    [calm] The first origin is the left end corner of the base bottom.
    [calm] The second origin is the upper endpoint of the chamfer.
    [calm] Go up the left vertical edge and part way it turns off at an angle. [calm] It is the upper end of that turned line.
    [measured] The chamfer cut 5 off at 45 degrees.
    [measured] So the left vertical edge only rises to 11, not 16. [measured] 16 take away 5.
    [calm] Pull the dimension line out to the left and set it there. [measured] 16 comes out.
    [asking] The two points are diagonally apart, so why is it 16?
    [calm] A linear dimension does not measure the straight distance between two points.
    [emphatic] It measures only the component in the direction you set the dimension line. [calm] Pull it out to the side and it measures the vertical component.

    [measured] `DLI`, Enter.
    [calm] The first origin is the left end corner of the base bottom.
    [calm] The second origin is the boss centre.
    [calm] Rest the mouse on the boss circle for a moment.
    [calm] The center snap appears at the middle of the circle.
    [calm] Pull the dimension line down and set it. [measured] That is 60.

    [measured] `DLI`, Enter. [calm] Pick the very same two points again.
    [calm] This time pull the dimension line out to the left and set it. [measured] 62 comes out.
    [calm] The same two points, and a different value.
    [calm] Where you pull the dimension line decides whether you measure across or down.
    [calm] To measure the real slanted distance between two points, you use an aligned dimension. [light] It comes later.

### Step 8 — The slots, 29, 50, 12 and 8

    [measured] `DLI`, Enter.
    [calm] The first origin is the left end corner of the base bottom.
    [calm] The second origin is the left end circle centre of the left slot.
    [calm] Rest the mouse on the end arc and a snap appears at the half-circle's centre. [light] Click then.
    [calm] Pull the dimension line down and set it. [measured] That is 29.

    [measured] `DLI`, Enter. [calm] The left end circle centre of the left slot, then the right end circle centre of the same slot.
    [calm] Set the dimension line below. [measured] That is 12. [calm] That value is the range of adjustment.

    [measured] `DLI`, Enter. [calm] The left end circle centre of the left slot, then the left end circle centre of the right slot.
    [calm] Set the dimension line below. [measured] That is 50.
    [calm] Three dimensions of the same character go side by side at the same height.
    [calm] If they look overlapped, click a dimension. [calm] Take the middle grip and drag it up or down to tier them.

    [measured] `DLI`, Enter. [calm] The left end corner of the base bottom, then the left end circle centre of the left slot.
    [calm] This time pull the dimension line out to the left and set it. [light] That is 8.
    [calm] It is the height from the bottom to the slot centre.

    [cautionary] You do not put the slot width of 10 in. [calm] End circles of radius 5 already fix the width.

### Step 9 — The web foot, 80

    [measured] The 80 is the horizontal gap between the two places where the web lines met the base's top face before the fillets went in.
    [calm] It is not a dimension measuring the gap between the actual tangent points of the fillets.
    [calm] Rather than finding the points by eye, you restore them with three helper construction lines.
    [calm] The current layer is dimension line. [light] Turn ortho off.
    [measured] `XL`, Enter. [calm] Click the lower endpoint and then the upper endpoint of the left web line with the endpoint snap, and press Enter.
    [measured] `XL`, Enter. [calm] Click the lower and upper endpoints of the right web line and press Enter.
    [calm] Construction lines appear along the same direction as the web lines.
    [measured] `XL`, Enter, `H`, Enter. [calm] Click the chamfer's upper endpoint and press Enter to finish.

    [measured] `DLI`, Enter. [calm] Click the intersection of the left web construction line and the horizontal construction line.
    [calm] The second point is the intersection of the right web construction line and the same horizontal construction line.
    [calm] Set the dimension line in the empty space below the base. [measured] Check that the measured value really is 80.
    [measured] `QSELECT`, Enter. [calm] Choose apply to entire drawing, object type construction line, operator select all.
    [calm] Confirm with how to apply include in new selection set. [emphatic] Erase only the three selected construction lines with Delete.
    [measured] See that the dimension of 80 and the original shape are still there.
    [calm] You erased the helper lines, so if you change the web shape later you catch this theoretical intersection again and re-check.


### Step 10 — The diameters Ø25 H7 and Ø56

    [measured] Type `DDI` and press Enter. [light] DIMDIAMETER, the diameter dimension.
    [calm] It asks you to select an arc or a circle. [calm] Click the bore circle in the middle.
    [calm] It asks where to put the dimension line. [calm] Drag it out to an empty spot outside the circle and click. [measured] Ø25 has gone in.
    [calm] The Ø symbol in front is not something we typed. [calm] The diameter dimension command puts it on itself.
    [calm] There are times you have to type it. [calm] When you put a Ø into a note or leader text.
    [measured] Then you type `%%c`. [calm] Two percent signs and a c. [calm] It turns into Ø on screen.
    [measured] The degree symbol is `%%d` and plus-minus is `%%p`.
    [calm] All three work the same in the text commands and in a dimension text override.

    [calm] Now you add the fit grade to it.
    [measured] Type `DIMEDIT` and press Enter.
    [calm] It asks the type of dimension edit. [measured] Type `N` and press Enter. [light] That is new.
    [calm] The text editor appears with the measured value's place marked.
    [cautionary] You do not touch that place. [measured] Leave a space after it and type `H7`.
    [calm] Click outside the editor to close it.
    [calm] It asks you to select objects. [measured] Click the Ø25 dimension you just put in and press Enter.
    [measured] It has become Ø25 H7.

    [cautionary] You must not delete the measured value's place and type the number yourself.
    [calm] Do that and the dimension does not follow when you change the shape later.
    [calm] It clings to the old number.

    [measured] `DDI`, Enter. [calm] Click the boss's outer circle.
    [calm] Drag the dimension line out to an empty spot and click. [measured] That is Ø56.

### Step 11 — The radii 2-R10 and 2-SLOT R5

    [measured] Type `DRA` and press Enter. [light] DIMRADIUS, the radius dimension.
    [calm] It asks you to select an arc or a circle. [calm] Click the right fillet arc.
    [calm] It asks where to put the dimension line. [cautionary] You do not place it yet. [calm] First you add the count.
    [measured] Type `M` and press Enter. [calm] That is the multiline text option.
    [measured] When the editor appears, type `2-` in front of the measured value. [calm] Click outside the editor to close it.
    [calm] Click where the dimension line goes. [measured] 2-R10 has gone in.
    [cautionary] You do not put another one on the left fillet. [calm] The 2 in front means the two of them, left and right.

    [measured] `DRA`, Enter. [calm] Click the left end arc of the left slot.
    [measured] `M`, Enter. [measured] Type `2-SLOT ` in front of the measured value. [light] Close the editor.
    [calm] Set the dimension line in the empty space below the slot. [measured] That is 2-SLOT R5.
    [emphatic] There are four end arcs but you put only one dimension.
    [calm] Put all four in and the same value has gone in four times — duplicate dimensions.

### Step 12 — PCD Ø44 and 45 degrees

    [measured] `DDI`, Enter.
    [calm] Click the pitch circle that the four tapped-hole centres lie on.
    [calm] It is the circle drawn as a red chain line on the centerline layer.
    [measured] `M`, Enter. [measured] Type `PCD ` in front of the measured value. [light] Close the editor.
    [calm] Set the dimension line in the empty space outside the boss. [measured] That is PCD Ø44.

    [calm] This time you select two lines and measure the angle.
    [measured] But the 45 degree line was used as a helper in Lesson 4 and erased.
    [calm] So you draw it again first. [calm] This time it is a centerline you keep on the drawing rather than erase.
    [measured] In the layer list at the top of the screen choose `Centerline`. [light] Turn ortho off.
    [measured] `L`, Enter. [calm] For the first point rest the mouse on the boss circle's rim and catch it with the center snap.
    [calm] The next point is the first tapped hole at the upper right. [calm] Rest the mouse on that circle's rim, catch it with the center snap and press Enter to finish.
    [measured] It is a line running 22 out from the boss centre at 45 degrees.
    [calm] You use the point already placed on the pitch circle as it is, so there is nothing to remember.
    [measured] Put the layer back to `Dimension line`.

    [measured] Type `DAN` and press Enter. [light] DIMANGULAR, the angular dimension.
    [calm] It asks you to select an arc, a circle or a line. [calm] Click the horizontal centerline through the boss centre.
    [calm] It asks for the second line. [measured] Click the 45 degree centerline you just drew.
    [calm] It asks where to put the dimension arc. [calm] Drag it into the space opening between the two lines and click.
    [measured] 45 degrees has gone in.

    [calm] Here you put the angular dimension in by picking two lines.
    [measured] The horizontal centerline was drawn in an earlier lesson, and the 45 degree line you have just drawn on the centerline layer.
    [calm] You changed layer while drawing that line, so check again that you are back on dimension line.
    [cautionary] You do not put angles on the other three holes.
    [calm] With an even array, the first hole's angle and the count fix the rest.

### Step 13 — The chamfers 2-C5

    [measured] A chamfer face is sloped at 45 degrees.
    [calm] Let us look at the aligned dimension here once.

    [measured] Type `DAL` and press Enter. [light] DIMALIGNED, the aligned dimension.
    [calm] The first origin is the lower endpoint of the left chamfer line.
    [calm] The second origin is that line's upper endpoint.
    [calm] Pull the dimension line out beyond the sloped face and set it.
    [measured] The value that comes out is about 7.07.
    [measured] It is the hypotenuse of a right triangle 5 across and 5 up. [measured] 5 times the square root of 2.
    [measured] The precision is at 0 places, so the screen shows 7.
    [calm] An aligned dimension measures the real length of the sloped face itself, like this.
    [calm] Had you measured the same two points with a linear dimension, you would have got 5.

    [calm] But the value the drawing needs is not 7.
    [calm] A chamfer is instructed by the length of the side cut off.
    [calm] Click the aligned dimension you just added to select it and erase it with the Delete key. [calm] You looked at it and now you erase it.

    [measured] Type `MLEADER` and press Enter. [light] That is the multileader.
    [calm] It asks where the leader arrowhead goes. [calm] Click on the right chamfer's sloped face.
    [calm] It asks where the leader landing goes. [calm] Drag it out to an empty spot outside the drawing and click.
    [light] The text editor opens. [measured] Type `2-C5` and click outside the editor.
    [light] C means a chamfer. [calm] The 5 is the length of the side cut off. [calm] The 2 in front is the two of them, left and right.

### Step 14 — The taps, 4-M5 depth 10

    [measured] `MLEADER`, Enter.
    [calm] The arrowhead goes on the circle of one of the four tapped holes.
    [calm] Drag the landing out to an empty spot outside the boss and click.
    [measured] In the text editor type `4-M5 DEPTH 10` and click outside the editor.
    [calm] Count, thread, depth, written on one line in that order.

    [asking] Why pull this out with a leader?
    [emphatic] A diameter dimension shows only the diameter of the circle drawn on screen. [calm] The thread and the depth you state on a leader.
    [calm] M5 is not a value that comes out of measuring. [calm] It is an instruction to cut a particular thread.
    [measured] The depth of 10 is not visible from the front either.
    [calm] What does not come out of measuring, and what has to carry several pieces of information on one line.
    [calm] Those two are the notations that go on a leader.

    [calm] You use this notation when you draw a jig yourself to propose it and make a job easier.
    [calm] Where to clamp and how many clamps, what thread to cut.
    [calm] You write that requirement on the drawing in one line and hand it over.

### Step 15 — Thicknesses 12 and 20, reference dimensions (95.7) and 26

    [calm] Thickness is not visible in the front view, so you go up to the top view. [calm] It is third angle, so the top view is directly above the front view.

    [measured] `DLI`, Enter.
    [calm] In the top view, pick two points: an endpoint of the plate's back face line and one of its front face line.
    [calm] Pull the dimension line out to the side and set it. [measured] That is 12.

    [measured] `DLI`, Enter.
    [calm] This time pick an endpoint of the plate's back face line and one of the face where the boss stands forward.
    [calm] Set the dimension line to the side. [measured] That is 20. [measured] It is the plate's 12 plus the boss's 8.
    [calm] You can see that both dimensions start from the same back face.
    [calm] The back face is one plane the whole way across. [calm] Nothing projects rearward, so the reference faces gather into one.

    [light] Now the reference dimension.
    [measured] `DLI`, Enter.
    [calm] Come back down to the front view. [calm] Pick the left fillet arc's centre with the center snap.
    [calm] Then pick the right fillet arc's centre the same way.
    [calm] Set the dimension line below. [measured] 96 comes out.
    [measured] The real centre spacing is about 95.72. [measured] The default precision is 0 places, so it shows rounded to 96.

    [emphatic] Click only the dimension you just added and open the Properties palette with Ctrl+1.
    [measured] Under primary units set the precision to one decimal place, 0.0.
    [measured] In text override put `(<>)` and press Enter.
    [measured] `<>` is the place that shows the current measured value. [cautionary] You do not overwrite the number yourself.
    [measured] Press Esc to clear the selection and check that it reads `(95.7)`.
    [measured] Only this one dimension is at one decimal place; EDU-A3's default precision of 0 is unchanged.
    [calm] A reference dimension too has to have its measured value follow when the shape changes.

    [measured] Last, `DLI`, Enter.
    [calm] The left end corner of the base bottom, and the right fillet arc's centre.
    [calm] This time pull the dimension line out to the side and set it vertically. [measured] That is 26. [calm] It is the fillet centre's height.
    [cautionary] You do not put brackets round this 26.
    [emphatic] Only the horizontal position is left as reference; the height is instructed plainly.

### Step 16 — Check the scale and release

    [measured] Type `PLOT` and press Enter. [light] The plot dialog opens.

    [calm] Under printer or plotter name, choose the device to output on.
    [emphatic] To produce a file only, with no paper, choose DWG To PDF.
    [measured] For paper size choose ISO A3, 420 by 297.
    [calm] For plot area choose Window. [calm] Press the Window button and it returns to the screen for a moment.
    [calm] You use the sheet edge you drew in Lesson 2.
    [calm] Click the lower left corner and then the upper right corner.
    [calm] Under plot offset, tick center the plot.

    [calm] The plot scale is the heart of today.
    [calm] Turn off the fit to paper tick.
    [calm] Leave it on and AutoCAD settles the scale for you.
    [measured] The drawing's 120 becomes 118 on paper, or 126. [calm] It simply fits it to the paper.
    [calm] Turn the tick off and the scale list opens. [measured] Choose 1:1. [measured] That is 1 millimetre to 1 unit.
    [calm] You drew at one to one in model space, so it has to be one to one here as well.
    [measured] Only then does the drawing's 120 measure 120 millimetres when you lay a rule on the paper.
    [calm] The drawing orientation is landscape.

    [calm] Scale matters because on the floor people put a rule on a printed drawing.
    [calm] Where a machine will go, walkway clearance, clash with the equipment beside it.
    [emphatic] Only paper that came out one to one lets you check any of that.

    [light] Press the Preview button.
    [calm] See that the border is not cut off.
    [calm] See that no dimension text overlaps the shape or another dimension.
    [calm] See that the title block is in.
    [asking] Does text that looked fine on screen look tiny here?
    [cautionary] Then the text height or the overall scale is wrong.
    [calm] Press Esc to go back to the dialog.
    [calm] If there is something to fix, cancel, fix it, and come back.
    [calm] If it is fine, press OK to plot.

    [measured] For the PDF file name put `EDU-IB-02_L07_RELEASE` and save.
    [calm] Open the PDF that comes out and check the A3 landscape page, the border and any dimension overlap once more.
    [calm] This exercise uses PLOT's PDF output.
    [calm] EXPORTPDF is a possible command too, but you check the current page setup before using it.


### Step 17 — Save under a new name

    [measured] Type `SAVEAS` and press Enter.
    [measured] Change the file name to `EDU-IB-02_L07_RELEASE`.
    [calm] Leave the file type as AutoCAD drawing, dwg.
    [light] Press Save.

    [cautionary] You do not overwrite the previous file.
    [calm] Leave a name behind for each lesson.
    [cautionary] You can trace back where and what went wrong.
    [calm] With that, one drawing sheet is finished.

## Line 6 — Checks (Frame 6)

**Time:** 25:36–27:29

    [calm] Four things to check before you finish. [emphatic] They are the mistakes that come up most often in dimensioning. [calm] All four you can see on this drawing right now.

    (1 card — entering without changing the layer) [pointing] This is entering dimensions without switching to the dimension line layer. [calm] A dimension that goes on the visible line layer comes out green. [calm] You cannot tell it from the shape. [calm] You also cannot do the trick of turning the visible line layer off and on to check. [light] Checking is simple. [calm] Click one dimension and look at the layer indicator at the top of the screen. [calm] There is a way to fix it, too. [calm] Click one dimension and then press the right mouse button. [calm] Choose Select Similar and everything of the same kind is caught at once. [calm] In that state choose dimension line in the layer list at the top and they all move across.

    (2 card — text height not matching the drawing) [pointing] On screen it looks fine because you are zoomed in. [calm] But print it on A3 and the numbers are tiny. [calm] The other way round, the dimension text can cover the shape. [calm] The way to check is the plot preview. [emphatic] You only know by looking on paper terms, not on screen. [light] There are two causes. [calm] The text height on the dimension style's Text tab. [calm] And the overall scale on the Fit tab. [calm] If the text height is not what you expect, check the overall scale and the text style's fixed height too. [calm] That value multiplies the text height.

    (3 card — the same dimension twice) [light] Duplicate dimensions. [measured] Writing both the width of 10 and R5 on a slot. [calm] Writing R10 on each of the left and right fillets. [measured] Writing the same 120 twice, in the front view and the top view. [asking] Why is it a problem? [emphatic] When the drawing is revised and only one side is corrected, the two values say different things. [calm] Whoever makes it does not know which to believe. [calm] The time spent coming to ask is a straight loss. [calm] One value is written once.

    (4 card — brackets missing from a reference dimension) [measured] Leave the brackets off 95.7 and that value becomes an inspection item. [calm] The inspector actually measures it. [calm] But this is a value computed from other dimensions. [calm] Rounding puts it minutely out. [cautionary] A part with nothing wrong with it goes over as a failure. [light] The reverse happens too. [calm] Put brackets round a value that really has to be inspected and nobody measures it. [cautionary] One pair of brackets separates measure this from do not measure this.

## Line 7 — Wrapping up (Frame 7)

**Time:** 27:29–29:19

    (1 left) [pointing] Here is what to check on screen before you hand the drawing over. [measured] See that the dimension style EDU-A3 is set current, with text height 5, arrow size 5 and 0 decimal places. [measured] Count that the overall size 120 and 90, the base height 16, the boss centre 60 and 62, the slots 29 and 50 and 12 and 8, and the web foot 80 are all in. [measured] Look also at the bore Ø25 H7, the boss Ø56, and the fillets 2-R10 and 2-SLOT R5. [measured] Then check the pitch circle PCD Ø44 and 45 degrees, the thicknesses 12 and 20, the reference dimension (95.7) and the fillet centre height 26. [measured] The notations that a number alone cannot carry are the two leaders, 2-C5 and 4-M5 depth 10. [calm] Last, check in the plot dialog that it is A3 at one to one, export the PDF, and save under a new name.

    (2 right) [pointing] Now let us see what you can do with this drawing. [calm] First, you can inspect it yourself. [calm] Turn the layers off and on one at a time. [calm] It shows up whether the dimensions really went on the dimension line layer. [calm] Whether the hidden lines are on the hidden line layer shows at a glance too. [calm] Second, the plot preview is the final verdict. [calm] The habit of checking on paper terms has to stay with you. [calm] Third, the values used today are the defaults for when the task gives no instruction. [calm] An instruction sometimes sets its own text height or layer names. [calm] The same goes for colours and scales. [emphatic] When it does, that instruction always wins. [calm] Fourth, the order of judgement is the same whatever part you are given. [calm] You read what this part is for. [calm] You settle the reference faces. [calm] You measure dimensions from that reference. [cautionary] It is never memorising the shape; it is reading the reason, all the way through. [calm] Fifth, once you are here you use drawings on the floor. [calm] You draw a jig yourself to propose it and make a job easier. [calm] You see in advance on a drawing where a machine will go and how people will move around it. [calm] When a spare part is urgent, the language of the conversation with the machine shop is the numbers you put up today. [calm] A drawing is not a picture; it is an instruction document.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 29:19–31:16

    [calm] Here are today's commands in one place. [emphatic] Rather than the names, remember **when you use them**.
    [calm] That is the part that stays after the exam.

    (1) [measured] `OPEN`. [light] Opens a file. [calm] You use it to carry on every lesson from the previous state.

    (2) [measured] `Z`. [light] ZOOM. [light] Changes the zoom. [calm] You use it when you need to see where a snap landed.

    (3) [measured] `OS`. [light] OSNAP. [calm] Chooses which object snaps are on. [emphatic] You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) [measured] `L`. [light] LINE. [light] Draws a line. [calm] You use it for pieces you need to handle singly.

    (5) [measured] `LAYER`. [light] Creates and manages layers. [calm] You use it when linetype and color belong to the layer, not to each object.

    (6) [measured] `D`. [light] DIMSTYLE. [light] Sets the dimension style. [calm] You use it to fit text height, arrows and decimal places to the drawing scale.

    (7) [measured] `DLI`. [light] DIMLINEAR. [calm] Puts in a horizontal or vertical dimension. [calm] You use it for values measured across and down.

    (8) [measured] `XL`. [light] XLINE. [calm] Draws a construction line that runs on forever. [calm] You use it for projection lines.

    (9) [measured] `QSELECT`. [calm] Picks every object matching a condition at once. [emphatic] You use it to select only the construction lines and erase them.

    (10) [measured] `DDI`. [light] DIMDIAMETER. [calm] Puts in a diameter dimension. [calm] You use it on circles and holes.

    (11) [measured] `DIMEDIT`. [calm] Edits the text of a dimension already placed. [calm] You use it for reference brackets and prefixes.

    (12) [measured] `DRA`. [light] DIMRADIUS. [calm] Puts in a radius dimension. [calm] You use it on rounds and arcs.

    (13) [measured] `DAN`. [light] DIMANGULAR. [calm] Puts in an angular dimension. [calm] You use it on the angle between two lines.

    (14) [measured] `DAL`. [light] DIMALIGNED. [calm] Puts in a dimension parallel to a slanted edge. [calm] You use it for the real length of a sloped face.

    (15) [measured] `MLEADER`. [calm] Puts in a leader with text. [calm] You use it to pull an explanation out beyond the shape.

    (16) [measured] `PLOT`. [light] Plots. [calm] You use it to send it out on paper or as a PDF.

    (17) [measured] `SAVEAS`. [calm] Saves under a new name. [calm] You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 31:16–31:36

    (1) [light] That is today's portion. [warm] Well done.

    (2) [pointing] You started by reading one part. [calm] And you finished one A3 drawing yourself. [calm] The drawing work ends here. [calm] Next is Lesson 8, the exam briefing and Q and A. [warm] See you then.
