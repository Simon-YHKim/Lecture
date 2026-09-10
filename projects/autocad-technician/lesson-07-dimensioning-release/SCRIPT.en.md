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

    Lesson 7, dimensioning and release.

## Line 2 — What you draw today (Frame 2)

**Time:** 0:05–1:57

    The shape was finished last lesson and the lines are where they belong. But hand this drawing to the floor as it stands and nobody can make anything. Because how big it is is not written on it.

    An LG Innotek machine has stopped and a spare part is urgent. It is a part that preventive maintenance, PM, did not cover in advance. You find the part in the assembly drawing and take that drawing to the machine shop to talk it over. At that moment you need not just the shape but exact dimension values. The idler pulley bracket for a car engine that you draw today goes over the same way. One wrong number comes back as rework loss. Today you put dimensions on the drawing and export it as a file.

    (1 card — making a dimension style) There is something to do before you put a number up. You settle what shape that number will come out in. How large to write the text. How large to make the arrowheads. How many decimal places to show. The place where those three are gathered is the dimension style. Settle it first and the dozens of dimensions you add afterwards all come out the same. Start entering without settling it and you end up catching each one later to fix it.

    (2 card — entering dimensions) Then you put the values up one at a time, starting from the overall size. The boss centre, the slots, diameters and radii, the pitch circle and the angle. Here you have to judge what you are measuring first. There is a separate command for measuring across and down. There are separate commands for a sloped face, for a circle, and for an angle. You choose the command to match what you are measuring.

    (3 card — reference dimensions and counts) Some notations do not carry their meaning as a number alone. That there are four of the same hole. That a value is for reference only and must not be inspected. You put a count in front, and you put brackets round it. What will not fit inside the shape you pull out with a leader and write outside.

    (4 card — checking the scale and exporting) Last you check the drawing against the paper size and export it as a PDF. It can look right on screen and be out on paper. The screen zooms as you like, but paper has a fixed size. You check the scale yourself in the plot dialog. The PDF you make this way is the drawing that goes to the floor.

## Line 3 — Concepts (Frame 3)

**Time:** 1:57–3:55

    Four things to settle before you press a command.

    (1 card — what the dimension style settles) You open the dimension style with the DIMSTYLE command. Three of the things you set here are used straight away in today's exercise. Text height, arrow size, and decimal places. Text height decides whether it is readable when printed on paper. You match the arrow size to roughly the text height. What happens if the two are badly out of step? One dimension looks as if it were pasted in from another drawing. Decimal places change how the value itself appears. Leave it at 0 and this part's 95.7 comes out as 96. Set it to one and everything else comes out like 120.0.

    (2 card — five kinds of dimension) You use five commands according to what you are measuring. Linear dimension, DIMLINEAR, measures a horizontal or a vertical distance. Aligned dimension, DIMALIGNED, measures the real distance between two points. That is the length of the sloped face itself. Diameter dimension, DIMDIAMETER, marks a circle's diameter. Radius dimension, DIMRADIUS, marks an arc's radius. Angular dimension, DIMANGULAR, measures the angle between two lines. You also have to tell whether a circle takes a diameter or a radius. On this drawing the bore and the boss are instructed by diameter, the fillets and the slot end arcs by radius. The command will let you put a diameter on an arc, but you follow this drawing's notation standard.

    (3 card — leaders) You draw a leader with the MLEADER command. It points at the shape with an arrowhead. It pulls a line outward and you write at the end of it. Why is it needed? First, when the shape is small. Put a dimension line inside it and nothing can be seen. Second, when what you have to write is not a single number. A tapped hole has to carry count, thread and depth on one line. One dimension line will not hold that.

    (4 card — the brackets on a reference dimension) Put brackets round a value and it means a reference dimension. It is a value computed from other dimensions. It instructs you to use it while making but not to measure it on inspection. Then why put it on the drawing at all? So the reader does not have to compute it every time. When you see brackets, know it is a value excluded from inspection. On this drawing, the 95.7 between the two fillet centres is the one.

## Line 4 — On the drawing (Frame 4)

**Time:** 3:55–7:22

    Now we go through this part's values one at a time. Something matters more than which value it is. It is where you measure from and to. Even for the same 120, two different points caught means a different object comes out.

    (1 row) The overall size, 120 and 90. The 120 is from the left end of the base's bottom to its right end. You measure it on the bottom edge, not the top one. The top edge has had its left and right corners cut away by the chamfers. Its endpoints are not where they originally were. The 90 is from the bottom to the very top of the part. And where is that top? The top of the boss circle. The boss centre is 62 from the bottom. The radius is half of 56, which is 28. 62 plus 28 is 90. So the second point of the 90 is the circle's top quadrant. Pick a corner and the value changes.

    (2 row) The boss centre, 60 and 62. 60 across from the left end. 62 up from the bottom. Both are measured from the part's left edge and its bottom edge. Why gather the references onto these two faces? Move your reference about and each dimension's error piles onto the next. Measure everything from one face and only that one face has to be right. Everything else lands where it belongs. These two values fix where the shaft sits.

    (3 row) The long horizontal holes at the bottom — the slot dimensions 29, 50, 12 and 8. A slot has no corner, so there is no point to catch. So you measure from the end circle centres. From the left end to the first end circle centre is 29. Within one slot, between the two end circle centres is 12. From the left slot's first end circle to the right slot's first end circle is 50. From the bottom, the end circle centre height is 8. Those four values fix the positions of both slots completely. You do not write the width of 10 separately. Two end circles of radius 5 already fix the width. Write 10 as well and the same thing is said twice.

    (4 row) Diameters and radii. Ø25 H7 is the bore. Ø56 is the outside of the boss. Both are whole circles, so they are written as diameters. R5 is the half-circle at the end of a slot. R10 is the fillet where the web turns into the base. Both are arcs, parts of a circle, so they are written as radii. And these four have their dimension lines running outside the shape. It is because the inside of a circle is too narrow to hold a dimension line and its text. Diameter and radius commands are built to pull the dimension outward.

    (5 row) PCD Ø44 and 45 degrees. PCD is the pitch circle diameter. The pitch circle is not a shape that actually gets cut. It is an imaginary circle the four tapped-hole centres sit on. So you draw it as a centerline. You put PCD in front of the diameter to show that it is not a hole. How does it read without PCD? It reads as one more hole, 44 across. The 45 degrees is the angle at which the first hole sits on that circle. It is 45 degrees up from the horizontal line through the boss centre. The other three step round from there every 90. Here you use the angular dimension's two-line selection method.

    (6 row) The reference dimension 95.7, and the thicknesses 12 and 20. The 95.7 is the distance between the two fillet centres. You put brackets round this one. It is a value that follows from the fillets' radius of 10 and the slope of the web lines. So it comes out as a decimal. Being a decimal is not what makes it a reference dimension. On this drawing it is a duplicate value determined by other dimensions, so it is left as reference. The same fillets' centre height of 26, on the other hand, is written plainly with no brackets. And the two thicknesses. You cannot read thickness in the front view. It runs front to back, so from the front it all overlaps into one line. You measure it in the top view. The plate is 12. Where the boss stands 8 forward it is 12 plus 8, which is 20.

## Line 5 — Dimensioning and release · DEMO-01 screen recording (Frame 5)

**Time:** 7:22–25:36

> This section is a screen recording. Work through the 17 steps below **in order and without skipping**, speaking as you go.
> What is inside backticks is what you actually type. Rely on snaps when you place a point, and always check the value with your eyes once it appears.

### Step 1 — Open the previous file

    Start AutoCAD. Type `OPEN` and press Enter. Or Ctrl+O.
    Choose the file you saved last time. It is the file with the idler pulley bracket drawn up to Lesson 6. Press Open.
    (`EDU-IB-02_L06_REPRESENTED.dwg`)
    You do not make a new one. You lay today's dimensions on top of the file that already holds the shape.
    `Z`, Enter, `A`, Enter. That is zoom all. The border comes onto the screen too.

### Step 2 — Check the basic settings · snaps and ortho

    Press Esc twice to clear the command and the selection.
    Type `OS` and press Enter. Check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    Press OK to close the dialog. Press F3 to turn object snap on only if the status bar shows it off.
    `L`, Enter. While it asks for the first point, rest the cursor on the endpoint of an existing line. Do not click.
    Watch for the square marker, then press Esc twice to cancel LINE. If there is no marker, look at OS and F3 again.
    Look at ortho too, and press F8 to turn it on only if it is off. On diagonals and tangents you turn it off, as each step says.
    Catch a point on the shape itself and you notice at once when a value has gone out.

### Step 3 — Make the dimension line layer current

    Type `LAYER` and press Enter. The layer properties manager opens.
    Select the `Dimension line` row and press Set Current. Close the dialog.
    See that the layer indicator at the top of the screen has changed to dimension line. White, 7.

    Why do this before you enter any dimensions?
    To move them afterwards you would have to pick out every dimension you had entered.
    Dimensions overlap the visible lines, so catching them one by one catches shape lines with them.
    Changing it once before you draw is far better.

    Keep the layers apart and later you can turn off just the dimensions and look at the shape alone.
    That is how you use it when you check a machine's footprint on a drawing.
    With fewer lines overlapping, traffic routes and clashes come into view.

### Step 4 — Make a new dimension style

    Type `D` and press Enter. That is the DIMSTYLE command. The dimension style manager opens.
    Right now the style list will have only ISO-25 in it.
    You do not edit that one directly. You make a new one.
    Leave the original and you have something to compare against when a setting goes wrong.

    Press the New button.
    For the new style name type `EDU-A3`.
    Leave start with as ISO-25. That means starting from it as a base.
    Leave use for as all dimensions.
    Press Continue.

### Step 5 — Set text, arrows and decimal places, and make it current

    The new dimension style dialog opens. There are seven tabs across the top. You touch only four.

    Open the Text tab.
    For text height type `5`.
    Leave text color as ByLayer. You already gave white, 7, on the layer.
    Leave text placement vertical above, horizontal centered. The number sits centred above the dimension line.

    Open the Symbols and Arrows tab.
    Leave the first arrowhead as closed filled. The second follows the first.
    For arrow size type `5`. It is the same value as the text height.
    Leave center marks as none. You do not lay an automatic mark over the centre marks from the earlier lesson.
    If the two are badly out of step, one dimension stands apart from the rest.

    Open the Fit tab.
    Look at the scale for dimension features at the lower right. Check that use overall scale of is `1`.
    If this is not 1, a text height of 5 grows or shrinks by that multiple.
    Fix the text height as often as you like and the size on screen still will not match? Usually this value is the culprit.

    Open the Primary Units tab.
    The unit format is decimal. Leave the precision at `0` decimal places.
    This part's dimensions are all whole numbers apart from one reference dimension.
    Leave a decimal place and 120 comes out as 120.00.
    Leave the measurement scale factor at `1`.
    You drew at one to one in model space, so the measured value has to come out as it is.
    Press OK.

    You are back at the dimension style manager.
    Select `EDU-A3` in the list and press Set Current. The current marker appears beside the name.
    Press Close.
    Making one and using one are different things.
    What happens if you leave out Set Current?
    The style is made and the dimensions go in as ISO-25.

### Step 6 — The overall size, 120 and 90

    Type `DLI` and press Enter. DIMLINEAR, the linear dimension.
    It asks for the first extension line origin.
    Put the mouse on the left end corner of the front view's base bottom.
    Click when the endpoint snap marker appears.
    It asks for the second origin. Click the bottom's right end corner the same way.
    It asks where to put the dimension line. Take the mouse down to an empty spot and click.
    120 has gone in.
    You set the dimension line generously clear of the shape.
    Set it close and visible lines and dimension lines mix together.
    You cannot tell where the part ends and the explanation begins.

    `DLI`, Enter. This time vertically.
    The first origin is the same point as before. The left end corner of the base bottom.
    The second origin is the very top of the boss circle.
    Put the mouse above the circle and the quadrant snap appears. Click then.
    Put the dimension line in the empty space to the left of the drawing. 90 has gone in.
    Check that this 90 agrees with 62 plus 28.
    If a different value comes out, the dimension is not wrong. The shape is.

### Step 7 — Base height 16 and boss centre 60, 62

    `DLI`, Enter.
    The first origin is the left end corner of the base bottom.
    The second origin is the upper endpoint of the chamfer.
    Go up the left vertical edge and part way it turns off at an angle. It is the upper end of that turned line.
    The chamfer cut 5 off at 45 degrees.
    So the left vertical edge only rises to 11, not 16. 16 take away 5.
    Pull the dimension line out to the left and set it there. 16 comes out.
    The two points are diagonally apart, so why is it 16?
    A linear dimension does not measure the straight distance between two points.
    It measures only the component in the direction you set the dimension line. Pull it out to the side and it measures the vertical component.

    `DLI`, Enter.
    The first origin is the left end corner of the base bottom.
    The second origin is the boss centre.
    Rest the mouse on the boss circle for a moment.
    The center snap appears at the middle of the circle.
    Pull the dimension line down and set it. That is 60.

    `DLI`, Enter. Pick the very same two points again.
    This time pull the dimension line out to the left and set it. 62 comes out.
    The same two points, and a different value.
    Where you pull the dimension line decides whether you measure across or down.
    To measure the real slanted distance between two points, you use an aligned dimension. It comes later.

### Step 8 — The slots, 29, 50, 12 and 8

    `DLI`, Enter.
    The first origin is the left end corner of the base bottom.
    The second origin is the left end circle centre of the left slot.
    Rest the mouse on the end arc and a snap appears at the half-circle's centre. Click then.
    Pull the dimension line down and set it. That is 29.

    `DLI`, Enter. The left end circle centre of the left slot, then the right end circle centre of the same slot.
    Set the dimension line below. That is 12. That value is the range of adjustment.

    `DLI`, Enter. The left end circle centre of the left slot, then the left end circle centre of the right slot.
    Set the dimension line below. That is 50.
    Three dimensions of the same character go side by side at the same height.
    If they look overlapped, click a dimension. Take the middle grip and drag it up or down to tier them.

    `DLI`, Enter. The left end corner of the base bottom, then the left end circle centre of the left slot.
    This time pull the dimension line out to the left and set it. That is 8.
    It is the height from the bottom to the slot centre.

    You do not put the slot width of 10 in. End circles of radius 5 already fix the width.

### Step 9 — The web foot, 80

    The 80 is the horizontal gap between the two places where the web lines met the base's top face before the fillets went in.
    It is not a dimension measuring the gap between the actual tangent points of the fillets.
    Rather than finding the points by eye, you restore them with three helper construction lines.
    The current layer is dimension line. Turn ortho off.
    `XL`, Enter. Click the lower endpoint and then the upper endpoint of the left web line with the endpoint snap, and press Enter.
    `XL`, Enter. Click the lower and upper endpoints of the right web line and press Enter.
    Construction lines appear along the same direction as the web lines.
    `XL`, Enter, `H`, Enter. Click the chamfer's upper endpoint and press Enter to finish.

    `DLI`, Enter. Click the intersection of the left web construction line and the horizontal construction line.
    The second point is the intersection of the right web construction line and the same horizontal construction line.
    Set the dimension line in the empty space below the base. Check that the measured value really is 80.
    `QSELECT`, Enter. Choose apply to entire drawing, object type construction line, operator select all.
    Confirm with how to apply include in new selection set. Erase only the three selected construction lines with Delete.
    See that the dimension of 80 and the original shape are still there.
    You erased the helper lines, so if you change the web shape later you catch this theoretical intersection again and re-check.


### Step 10 — The diameters Ø25 H7 and Ø56

    Type `DDI` and press Enter. DIMDIAMETER, the diameter dimension.
    It asks you to select an arc or a circle. Click the bore circle in the middle.
    It asks where to put the dimension line. Drag it out to an empty spot outside the circle and click. Ø25 has gone in.
    The Ø symbol in front is not something we typed. The diameter dimension command puts it on itself.
    There are times you have to type it. When you put a Ø into a note or leader text.
    Then you type `%%c`. Two percent signs and a c. It turns into Ø on screen.
    The degree symbol is `%%d` and plus-minus is `%%p`.
    All three work the same in the text commands and in a dimension text override.

    Now you add the fit grade to it.
    Type `DIMEDIT` and press Enter.
    It asks the type of dimension edit. Type `N` and press Enter. That is new.
    The text editor appears with the measured value's place marked.
    You do not touch that place. Leave a space after it and type `H7`.
    Click outside the editor to close it.
    It asks you to select objects. Click the Ø25 dimension you just put in and press Enter.
    It has become Ø25 H7.

    You must not delete the measured value's place and type the number yourself.
    Do that and the dimension does not follow when you change the shape later.
    It clings to the old number.

    `DDI`, Enter. Click the boss's outer circle.
    Drag the dimension line out to an empty spot and click. That is Ø56.

### Step 11 — The radii 2-R10 and 2-SLOT R5

    Type `DRA` and press Enter. DIMRADIUS, the radius dimension.
    It asks you to select an arc or a circle. Click the right fillet arc.
    It asks where to put the dimension line. You do not place it yet. First you add the count.
    Type `M` and press Enter. That is the multiline text option.
    When the editor appears, type `2-` in front of the measured value. Click outside the editor to close it.
    Click where the dimension line goes. 2-R10 has gone in.
    You do not put another one on the left fillet. The 2 in front means the two of them, left and right.

    `DRA`, Enter. Click the left end arc of the left slot.
    `M`, Enter. Type `2-SLOT ` in front of the measured value. Close the editor.
    Set the dimension line in the empty space below the slot. That is 2-SLOT R5.
    There are four end arcs but you put only one dimension.
    Put all four in and the same value has gone in four times — duplicate dimensions.

### Step 12 — PCD Ø44 and 45 degrees

    `DDI`, Enter.
    Click the pitch circle that the four tapped-hole centres lie on.
    It is the circle drawn as a red chain line on the centerline layer.
    `M`, Enter. Type `PCD ` in front of the measured value. Close the editor.
    Set the dimension line in the empty space outside the boss. That is PCD Ø44.

    This time you select two lines and measure the angle.
    But the 45 degree line was used as a helper in Lesson 4 and erased.
    So you draw it again first. This time it is a centerline you keep on the drawing rather than erase.
    In the layer list at the top of the screen choose `Centerline`. Turn ortho off.
    `L`, Enter. For the first point rest the mouse on the boss circle's rim and catch it with the center snap.
    The next point is the first tapped hole at the upper right. Rest the mouse on that circle's rim, catch it with the center snap and press Enter to finish.
    It is a line running 22 out from the boss centre at 45 degrees.
    You use the point already placed on the pitch circle as it is, so there is nothing to remember.
    Put the layer back to `Dimension line`.

    Type `DAN` and press Enter. DIMANGULAR, the angular dimension.
    It asks you to select an arc, a circle or a line. Click the horizontal centerline through the boss centre.
    It asks for the second line. Click the 45 degree centerline you just drew.
    It asks where to put the dimension arc. Drag it into the space opening between the two lines and click.
    45 degrees has gone in.

    Here you put the angular dimension in by picking two lines.
    The horizontal centerline was drawn in an earlier lesson, and the 45 degree line you have just drawn on the centerline layer.
    You changed layer while drawing that line, so check again that you are back on dimension line.
    You do not put angles on the other three holes.
    With an even array, the first hole's angle and the count fix the rest.

### Step 13 — The chamfers 2-C5

    A chamfer face is sloped at 45 degrees.
    Let us look at the aligned dimension here once.

    Type `DAL` and press Enter. DIMALIGNED, the aligned dimension.
    The first origin is the lower endpoint of the left chamfer line.
    The second origin is that line's upper endpoint.
    Pull the dimension line out beyond the sloped face and set it.
    The value that comes out is about 7.07.
    It is the hypotenuse of a right triangle 5 across and 5 up. 5 times the square root of 2.
    The precision is at 0 places, so the screen shows 7.
    An aligned dimension measures the real length of the sloped face itself, like this.
    Had you measured the same two points with a linear dimension, you would have got 5.

    But the value the drawing needs is not 7.
    A chamfer is instructed by the length of the side cut off.
    Click the aligned dimension you just added to select it and erase it with the Delete key. You looked at it and now you erase it.

    Type `MLEADER` and press Enter. That is the multileader.
    It asks where the leader arrowhead goes. Click on the right chamfer's sloped face.
    It asks where the leader landing goes. Drag it out to an empty spot outside the drawing and click.
    The text editor opens. Type `2-C5` and click outside the editor.
    C means a chamfer. The 5 is the length of the side cut off. The 2 in front is the two of them, left and right.

### Step 14 — The taps, 4-M5 depth 10

    `MLEADER`, Enter.
    The arrowhead goes on the circle of one of the four tapped holes.
    Drag the landing out to an empty spot outside the boss and click.
    In the text editor type `4-M5 DEPTH 10` and click outside the editor.
    Count, thread, depth, written on one line in that order.

    Why pull this out with a leader?
    A diameter dimension shows only the diameter of the circle drawn on screen. The thread and the depth you state on a leader.
    M5 is not a value that comes out of measuring. It is an instruction to cut a particular thread.
    The depth of 10 is not visible from the front either.
    What does not come out of measuring, and what has to carry several pieces of information on one line.
    Those two are the notations that go on a leader.

    You use this notation when you draw a jig yourself to propose it and make a job easier.
    Where to clamp and how many clamps, what thread to cut.
    You write that requirement on the drawing in one line and hand it over.

### Step 15 — Thicknesses 12 and 20, reference dimensions (95.7) and 26

    Thickness is not visible in the front view, so you go up to the top view. It is third angle, so the top view is directly above the front view.

    `DLI`, Enter.
    In the top view, pick two points: an endpoint of the plate's back face line and one of its front face line.
    Pull the dimension line out to the side and set it. That is 12.

    `DLI`, Enter.
    This time pick an endpoint of the plate's back face line and one of the face where the boss stands forward.
    Set the dimension line to the side. That is 20. It is the plate's 12 plus the boss's 8.
    You can see that both dimensions start from the same back face.
    The back face is one plane the whole way across. Nothing projects rearward, so the reference faces gather into one.

    Now the reference dimension.
    `DLI`, Enter.
    Come back down to the front view. Pick the left fillet arc's centre with the center snap.
    Then pick the right fillet arc's centre the same way.
    Set the dimension line below. 96 comes out.
    The real centre spacing is about 95.72. The default precision is 0 places, so it shows rounded to 96.

    Click only the dimension you just added and open the Properties palette with Ctrl+1.
    Under primary units set the precision to one decimal place, 0.0.
    In text override put `(<>)` and press Enter.
    `<>` is the place that shows the current measured value. You do not overwrite the number yourself.
    Press Esc to clear the selection and check that it reads `(95.7)`.
    Only this one dimension is at one decimal place; EDU-A3's default precision of 0 is unchanged.
    A reference dimension too has to have its measured value follow when the shape changes.

    Last, `DLI`, Enter.
    The left end corner of the base bottom, and the right fillet arc's centre.
    This time pull the dimension line out to the side and set it vertically. That is 26. It is the fillet centre's height.
    You do not put brackets round this 26.
    Only the horizontal position is left as reference; the height is instructed plainly.

### Step 16 — Check the scale and release

    Type `PLOT` and press Enter. The plot dialog opens.

    Under printer or plotter name, choose the device to output on.
    To produce a file only, with no paper, choose DWG To PDF.
    For paper size choose ISO A3, 420 by 297.
    For plot area choose Window. Press the Window button and it returns to the screen for a moment.
    You use the sheet edge you drew in Lesson 2.
    Click the lower left corner and then the upper right corner.
    Under plot offset, tick center the plot.

    The plot scale is the heart of today.
    Turn off the fit to paper tick.
    Leave it on and AutoCAD settles the scale for you.
    The drawing's 120 becomes 118 on paper, or 126. It simply fits it to the paper.
    Turn the tick off and the scale list opens. Choose 1:1. That is 1 millimetre to 1 unit.
    You drew at one to one in model space, so it has to be one to one here as well.
    Only then does the drawing's 120 measure 120 millimetres when you lay a rule on the paper.
    The drawing orientation is landscape.

    Scale matters because on the floor people put a rule on a printed drawing.
    Where a machine will go, walkway clearance, clash with the equipment beside it.
    Only paper that came out one to one lets you check any of that.

    Press the Preview button.
    See that the border is not cut off.
    See that no dimension text overlaps the shape or another dimension.
    See that the title block is in.
    Does text that looked fine on screen look tiny here?
    Then the text height or the overall scale is wrong.
    Press Esc to go back to the dialog.
    If there is something to fix, cancel, fix it, and come back.
    If it is fine, press OK to plot.

    For the PDF file name put `EDU-IB-02_L07_RELEASE` and save.
    Open the PDF that comes out and check the A3 landscape page, the border and any dimension overlap once more.
    This exercise uses PLOT's PDF output.
    EXPORTPDF is a possible command too, but you check the current page setup before using it.


### Step 17 — Save under a new name

    Type `SAVEAS` and press Enter.
    Change the file name to `EDU-IB-02_L07_RELEASE`.
    Leave the file type as AutoCAD drawing, dwg.
    Press Save.

    You do not overwrite the previous file.
    Leave a name behind for each lesson.
    You can trace back where and what went wrong.
    With that, one drawing sheet is finished.

## Line 6 — Checks (Frame 6)

**Time:** 25:36–27:29

    Four things to check before you finish. They are the mistakes that come up most often in dimensioning. All four you can see on this drawing right now.

    (1 card — entering without changing the layer) This is entering dimensions without switching to the dimension line layer. A dimension that goes on the visible line layer comes out green. You cannot tell it from the shape. You also cannot do the trick of turning the visible line layer off and on to check. Checking is simple. Click one dimension and look at the layer indicator at the top of the screen. There is a way to fix it, too. Click one dimension and then press the right mouse button. Choose Select Similar and everything of the same kind is caught at once. In that state choose dimension line in the layer list at the top and they all move across.

    (2 card — text height not matching the drawing) On screen it looks fine because you are zoomed in. But print it on A3 and the numbers are tiny. The other way round, the dimension text can cover the shape. The way to check is the plot preview. You only know by looking on paper terms, not on screen. There are two causes. The text height on the dimension style's Text tab. And the overall scale on the Fit tab. If the text height is not what you expect, check the overall scale and the text style's fixed height too. That value multiplies the text height.

    (3 card — the same dimension twice) Duplicate dimensions. Writing both the width of 10 and R5 on a slot. Writing R10 on each of the left and right fillets. Writing the same 120 twice, in the front view and the top view. Why is it a problem? When the drawing is revised and only one side is corrected, the two values say different things. Whoever makes it does not know which to believe. The time spent coming to ask is a straight loss. One value is written once.

    (4 card — brackets missing from a reference dimension) Leave the brackets off 95.7 and that value becomes an inspection item. The inspector actually measures it. But this is a value computed from other dimensions. Rounding puts it minutely out. A part with nothing wrong with it goes over as a failure. The reverse happens too. Put brackets round a value that really has to be inspected and nobody measures it. One pair of brackets separates measure this from do not measure this.

## Line 7 — Wrapping up (Frame 7)

**Time:** 27:29–29:19

    (1 left) Here is what to check on screen before you hand the drawing over. See that the dimension style EDU-A3 is set current, with text height 5, arrow size 5 and 0 decimal places. Count that the overall size 120 and 90, the base height 16, the boss centre 60 and 62, the slots 29 and 50 and 12 and 8, and the web foot 80 are all in. Look also at the bore Ø25 H7 and the boss Ø56, the fillets 2-R10 and 2-SLOT R5, the pitch circle PCD Ø44 and 45 degrees, the thicknesses 12 and 20, the reference dimension (95.7) and the fillet centre height 26. The notations that a number alone cannot carry are the two leaders, 2-C5 and 4-M5 depth 10. Last, check in the plot dialog that it is A3 at one to one, export the PDF, and save under a new name.

    (2 right) Now let us see what you can do with this drawing. First, you can inspect it yourself. Turn the layers off and on one at a time. It shows up whether the dimensions really went on the dimension line layer. Whether the hidden lines are on the hidden line layer shows at a glance too. Second, the plot preview is the final verdict. The habit of checking on paper terms has to stay with you. Third, the values used today are the defaults for when the task gives no instruction. An instruction sometimes sets its own text height or layer names. The same goes for colours and scales. When it does, that instruction always wins. Fourth, the order of judgement is the same whatever part you are given. You read what this part is for. You settle the reference faces. You measure dimensions from that reference. It is never memorising the shape; it is reading the reason, all the way through. Fifth, once you are here you use drawings on the floor. You draw a jig yourself to propose it and make a job easier. You see in advance on a drawing where a machine will go and how people will move around it. When a spare part is urgent, the language of the conversation with the machine shop is the numbers you put up today. A drawing is not a picture; it is an instruction document.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 29:19–31:16

    Here are today's commands in one place. Rather than the names, remember **when you use them**.
    That is the part that stays after the exam.

    (1) `OPEN`. Opens a file. You use it to carry on every lesson from the previous state.

    (2) `Z`. ZOOM. Changes the zoom. You use it when you need to see where a snap landed.

    (3) `OS`. OSNAP. Chooses which object snaps are on. You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) `L`. LINE. Draws a line. You use it for pieces you need to handle singly.

    (5) `LAYER`. Creates and manages layers. You use it when linetype and color belong to the layer, not to each object.

    (6) `D`. DIMSTYLE. Sets the dimension style. You use it to fit text height, arrows and decimal places to the drawing scale.

    (7) `DLI`. DIMLINEAR. Puts in a horizontal or vertical dimension. You use it for values measured across and down.

    (8) `XL`. XLINE. Draws a construction line that runs on forever. You use it for projection lines.

    (9) `QSELECT`. Picks every object matching a condition at once. You use it to select only the construction lines and erase them.

    (10) `DDI`. DIMDIAMETER. Puts in a diameter dimension. You use it on circles and holes.

    (11) `DIMEDIT`. Edits the text of a dimension already placed. You use it for reference brackets and prefixes.

    (12) `DRA`. DIMRADIUS. Puts in a radius dimension. You use it on rounds and arcs.

    (13) `DAN`. DIMANGULAR. Puts in an angular dimension. You use it on the angle between two lines.

    (14) `DAL`. DIMALIGNED. Puts in a dimension parallel to a slanted edge. You use it for the real length of a sloped face.

    (15) `MLEADER`. Puts in a leader with text. You use it to pull an explanation out beyond the shape.

    (16) `PLOT`. Plots. You use it to send it out on paper or as a PDF.

    (17) `SAVEAS`. Saves under a new name. You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 31:16–31:36

    (1) That is today's portion. Well done.

    (2) You started by reading one part. And you finished one A3 drawing yourself. The drawing work ends here. Next is Lesson 8, the exam briefing and Q and A. See you then.
