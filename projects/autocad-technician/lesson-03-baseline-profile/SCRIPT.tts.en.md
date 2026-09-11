<!-- 생성물이다. 손으로 고치지 말고 원본 SCRIPT.en.md 를 고친 뒤 다시 뽑아라.
     python scripts/part/tts_script.py lesson-03-baseline-profile
     태그: asking · calm · cautionary · emphatic · light · measured · pointing · warm -->
# SCRIPT — AutoCAD Technician Lesson 3 · Datum lines and the outline (English edition)

**Part:** `idler pulley bracket used on a car engine`<br>
**Checkpoint:** `L02_TEMPLATE → L03_PROFILE`<br>
**Voice:** Windows SAPI · Microsoft Zira Desktop · Rate 0 · pitch-preserving 1.15x<br>
**Voice direction:** Take a beat before a number when you say a dimension. Through the hands-on section (Line 5), say the value first, then move at the speed of pressing Enter.

> Length not measured yet. The times below mirror the Korean script so the frames
> line up; they are replaced by measured values once the English speech exists.

## Line 1 — Title (Frame 1)

**Time:** 0:00–0:05

    (silence)

    [calm] Lesson 3, datum lines and the outline.

## Line 2 — What you draw today (Frame 2)

**Time:** 0:05–2:04

    [calm] Last time you made the A3 border. [calm] You set up four layers as well. [calm] Today you open that file. [calm] For the first time you draw part lines. [calm] Four things go on the screen.

    (1 card — centerlines) [pointing] Start with how not to place a centerline by eye. [calm] This part is symmetrical left and right about the vertical centerline. [calm] There is the boss circle, the bore, the four tapped holes. [calm] Every one of them starts from a point on that centerline. [calm] So if the centerline is exact, everything after it is exact. [asking] Where does an exact centerline come from? [calm] From the midpoint of the base's bottom edge, which you have already drawn. [calm] For a snap to have something to catch, the shape has to exist first. [calm] So today you draw the outline first, and pull the centerline out of that shape.

    (2 card — base 120 × 16 outline) [pointing] You draw the outer profile of the bottom plate. [measured] 120 across, and 16 high seen from the front. [calm] This plate is the first thing you draw today. [calm] This plate decides where the whole part sits. [measured] The 120 across is the whole width of the part. [calm] For the plate's lower left corner you just click an empty spot inside the border. [cautionary] You do not type coordinates. [asking] What happens if that wanders? [calm] Everything that stands on it wanders too.

    (3 card — chamfers 2-C5) [pointing] You cut the two upper corners of the base. [measured] 5 off each, at 45 degrees. [calm] On the drawing that is 2-C5. [calm] The 2 is the count, C is a chamfer, 5 is the length of the side cut off. [calm] Leave a sharp corner and it cuts your hand. [calm] It clashes with another part on assembly. [calm] Paint goes on thin at a sharp edge, too. [calm] Cut it and all three go away at once. [calm] You make the rectangle first and cut it with the chamfer command. [calm] You give the 5 and 5 that are written on the drawing as the two distances.

    (4 card — boss circle Ø56 and the tangent web) [pointing] You draw the outer circle of the boss at the top. [calm] Then you draw the web that climbs from the base to that circle. [light] Two lines. [emphatic] The web lines have to touch the boss circle exactly. [asking] What does touching mean here? [calm] It means meeting at one point, in passing. [calm] Not cutting in, not falling short. [cautionary] Place that one point by eye and it will be wrong every time. [calm] That is why you use the tangent object snap today.

## Line 3 — Four ways to place a point, two commands that make a line (Frame 3)

**Time:** 2:04–4:50

    [calm] A line is made of two points. [calm] So drawing accurately means placing points accurately. [calm] There are four ways to place one. [emphatic] There is only one test for choosing. [asking] Is that point fixed by a drawing dimension? [calm] And there are two commands that string those points into lines.

    (1 card — object snap F3) [pointing] You place the point by catching a feature point of something already drawn. [calm] Six of them: endpoint, midpoint, center, quadrant, intersection and tangent. [calm] Rest the cursor and a marker appears. [calm] You check the marker, then click. [emphatic] This is the way you use most today. [calm] You catch the midpoint of the bottom edge and the centerline intersection this way. [calm] You find the tangent point on the boss circle the same way. [calm] If the shape already holds the answer, there is no reason to type the number again. [cautionary] If what you drew earlier is wrong, what comes after goes wrong with it. [calm] So the error shows up immediately.

    (2 card — ortho and typed values F8, F12) [emphatic] You fix the direction with the mouse and type only the length. [emphatic] Turn ortho on with F8 and the cursor moves only horizontally and vertically. [calm] Put the cursor on the side you are heading and type the number. [measured] For a line 10 upward, put the cursor above that point and type 10. [calm] With F12 dynamic input on, the number goes into the box beside the cursor. [calm] With it off it goes to the command line at the bottom. [calm] The place you type differs; the value is the same. [calm] If you need a slanted direction, fix the angle with F10 polar tracking. [calm] You draw today's two centerlines this way.

    (3 card — snap tracking and FROM, F11) [pointing] This is how you make a point the shape does not have yet. [calm] Turn F11 on and rest the cursor on a feature point for a moment. [calm] A guide line reaches out from that point. [calm] Get a second guide line to reach out from another point. [calm] When a marker appears where the two guides meet, click. [calm] FROM works a little differently. [calm] You catch a reference point, then say how far from it to go. [calm] You place the start of the vertical centerline this way today. [calm] Both of them take a point on the shape as their reference. [cautionary] That is why you do not have to memorise coordinates.

    (4 card — LINE and PLINE and REC) [pointing] An outline that goes all the way round is drawn as one body. [calm] REC makes a rectangle as a single object. [calm] With PLINE the whole run you drew is one object. [calm] One click selects the whole thing. [calm] Offset and area also apply to the whole outline at once. [calm] On the floor you run a polyline around the area a machine will occupy. [calm] Then you get its area in one go. [calm] When you try moving it, you drag the whole thing at once. [calm] LINE is the opposite: draw one after another and each stays a separate line. [calm] A piece you will trim and round later is easier to handle as a single line.

    (5 note — which one to use) [pointing] One thing decides which of the four you use. [calm] Check whether that point is fixed by a drawing dimension. [calm] If it is, pull it out of the shape with a snap or with tracking. [emphatic] If only a length is given, fix the direction with the mouse and type the number. [calm] A point no dimension fixes, you simply click. [calm] The first point of the base outline is one of those. [emphatic] It only has to be somewhere the part fits inside the border. [cautionary] Place a point that a dimension does fix by eye, on the other hand, and the drawing is wrong. [emphatic] In this whole course, the only place you type coordinates is the two corners of the sheet edge.

## Line 4 — On the drawing (Frame 4)

**Time:** 4:50–7:28

    [calm] The front view is on the left, and on the right a table of the values you use today. [calm] We will work down the table and see where each value comes from on the drawing, in order.

    (1 row) [pointing] Start with where the dimensions are measured from. [emphatic] Most of this part's dimensions are measured from the left edge and the bottom. [measured] The 60 and 62 of the boss centre are. [measured] So are the 35 and 85 of the slot centres, and their height of 8. [calm] So you take the lower left corner of the base as your reference. [cautionary] You do not, however, move the coordinate origin there. [calm] You catch that corner by clicking on screen. [calm] Every other position is pulled out of the shape. [calm] It is the same order when you draw a jig to propose it. [calm] You decide what to measure from before you start.

    (2 row) [pointing] Read how the base is set up. [calm] You stand the rectangle up first, without worrying about the chamfers. [calm] With the REC command you click one corner, then press D for the dimensions option. [measured] 120 across, 16 up. [calm] Those two numbers are written on the drawing as they are. [emphatic] All four corners land exactly, in one go. [calm] Which corner you clicked first does not matter. [calm] It is not a point that a dimension fixes.

    (3 row) [pointing] The chamfers go on after the rectangle is standing. [measured] 2-C5 means cutting 5 off at 45 degrees. [calm] The 2 is the count, C is a chamfer, 5 is the length of the side cut off. [emphatic] You give the CHAMFER command 5 and 5 and cut only the top two corners. [cautionary] You never have to type a computed value like 11 or 115. [measured] The numbers on the drawing are 120, 16 and 5. [emphatic] Those three are the only ones we typed. [calm] Make no computed values and you make no arithmetic slips either.

    (4 row) [pointing] Look at the top face of the base. [calm] This height decides half of what you draw today. [calm] The web climbs from here. [calm] The R10 fillet you add next lesson starts here too. [calm] 16 is not the plate thickness but the height seen from the front. [calm] The thickness of 12 is a value you read in the top view. [calm] It does not appear in today's front view.

    (5 row) [pointing] You draw the boss circle first. [light] The diameter is 56. [calm] Its centre goes on the intersection of the two centerlines. [calm] The web lines have to be tangent to this circle. [calm] With no circle on screen to be tangent to, there is no tangent point to catch. [calm] That is why the circle comes before the web. [measured] Add the radius of 28 to the centre height of 62 and you get 90. [calm] That is the overall height of the part. [calm] The top of the boss circle is the top of this part.

    (6 row) [light] Last, the web. [calm] Its foot is 80 wide. [measured] Take 80 from the base width of 120 and 40 is left, 20 on each side. [calm] So the web starts at two points. [calm] On the top face of the base, 40 either side of the vertical centerline. [cautionary] You do not place these two by coordinates either. [calm] You catch the midpoint snap on the top face and step 40 out each way. [calm] Then from those two points you draw tangent lines to the boss circle.

## Line 5 — Datum lines and the outline · DEMO-01 screen recording (Frame 5)

**Time:** 7:28–20:09

> This section is a screen recording. Work through the 16 steps below in order and without skipping, speaking as you go.
> What is inside backticks is what you actually type; everything else you check on screen or click.

### Step 1 — Open last lesson's file

    [measured] Start AutoCAD 2024. [measured] Type `OPEN` and press Enter.
    [calm] Find and open the file you saved last time. [measured] Its name ends in `L02_TEMPLATE`.
    [cautionary] Do not make a new one.
    [calm] It has the A3 border and the centering marks in it. [calm] It has the title block and four layers too.
    [calm] Every lesson you open the previous file like this and draw on top of it.

### Step 2 — Check the state

    [measured] Type `Z` and press Enter. [measured] Then type `A` and press Enter. [light] That is zoom all.
    [calm] The whole border comes onto the screen.
    [calm] Press Esc twice to clear the command and the selection.
    [measured] `OS`, Enter. [calm] On the object snap tab, check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    [emphatic] Press OK to close the dialog, and press F3 only if object snap is off.
    [measured] `L`, Enter. [calm] While it asks for the first point, rest the cursor on a corner of the border. [cautionary] Do not click.
    [calm] See whether the square endpoint marker appears, then press Esc twice to cancel LINE.
    [calm] If there is no marker, check the OS settings and the F3 state again.
    [emphatic] Look at ortho too, and press F8 only if it is off.
    [light] Open the layer dropdown. [calm] Visible line, centerline, hidden line, dimension line.
    [calm] Check that all four are there.
    [asking] What happens if you start drawing without checking here?
    [cautionary] Later on you find a line sitting on the wrong layer.
    [calm] Today you catch almost every position with a snap.
    [calm] With snap off, every click is done by eye.

### Step 3 — Switch to the visible line layer and zoom into the drawing area

    [measured] In the layer dropdown choose `Visible line`. [light] Green, continuous.
    [calm] From here on you are drawing the shape of the part you can see.

    [measured] `Z`, Enter. [measured] At the options type `W` and press Enter. [calm] That is a window zoom.
    [calm] The inside of the rectangle you give fills the screen.
    [calm] In the lower left quarter of the border, drag a rectangle big enough for the part.
    [calm] Click the two corners in turn. [cautionary] You do not type coordinates.
    [measured] The part needs 120 by 90, so leave yourself a bit more than that.
    [calm] Draw it small and you cannot see where the snap landed.
    [calm] Put it up large and your hand has an easier time.

    [calm] The two corners of the zoom window are not fixed by any drawing dimension.
    [calm] Typing coordinates for a place like that costs time and buys no accuracy.

### Step 4 — Make the base rectangle (REC)

    [calm] Check in the status bar that object snap is on.
    [measured] Type `REC` and press Enter.
    [calm] Before you pick the first corner, clear the previous settings.
    [measured] Type `C`, the chamfer option, Enter, first distance `0`, Enter, second distance `0`, Enter.
    [measured] When it asks for the first corner again, type `F`, the fillet option, Enter, radius `0`, Enter.
    [measured] Check `W`, Enter, polyline width `0`, Enter as well.
    [calm] When it comes back to the first corner question, click the lower left of the area you are drawing in.
    [calm] Anywhere inside the border where the part will fit is fine. [light] This position is free.
    [measured] At the opposite corner question, `R`, Enter, rotation angle `0`, Enter.
    [measured] When it asks for the opposite corner again, press `D`, Enter.
    [measured] Length is `120`, Enter. [measured] Width is `16`, Enter.
    [calm] Put the cursor above and to the right of the first point and click once.
    [calm] The rectangle command ends here. [cautionary] Do not press Enter again.
    [measured] A closed rectangle of 120 by 16 should be on screen.
    [emphatic] The chamfers go on in the next two steps, on the top two corners only.

### Step 5 — The right-hand chamfer

    [measured] `TRIMMODE`, Enter, `1`, Enter.
    [calm] That makes the two chamfered edges end on the new boundary.

    [measured] Type `CHA` and press Enter. [calm] That is the chamfer command.
    [measured] Type `D` and press Enter. [calm] That is the distance option.
    [calm] It asks the first distance. [measured] `5`, Enter.
    [calm] It asks the second distance. [calm] It is the same value, so you can simply press Enter.

    [calm] Now click the two edges that make the corner you are cutting, in turn.
    [calm] Click the top edge at the upper right corner, then click the right-hand vertical edge.
    [measured] The corner is cut at 45 degrees. [measured] 5 across and 5 up makes it exactly 45.

    [measured] The 2-C5 on the drawing is this value. [measured] You put in 5 and 5 as they are.
    [measured] Chamfer while drawing the rectangle and you have to work out values like 11 and 110 by hand.
    [calm] Those numbers appear nowhere on the drawing.
    [emphatic] Draw the rectangle first and chamfer separately, and you only ever type numbers the drawing gives you.

### Step 6 — The top face, the left chamfer, and closing

    [calm] The upper left corner works the same way.
    [measured] Type `CHA` again and press Enter. [measured] The distances are still 5 and 5.
    [calm] Click the top edge, then the left-hand vertical edge.

    [calm] Now you have a six-sided outline.
    [calm] The bottom two corners stay square. [measured] The drawing shows 2-C5 at the top two only.

    [calm] There is a way to cut all four corners at once.
    [measured] In `CHA` you press `P` and click the rectangle.
    [calm] That cuts the bottom two as well, though. [calm] So here you take them one at a time.

    [cautionary] The rectangle was closed from the start, so you never place the last edge by hand.
    [calm] Place it by hand and it misses by a fraction below the decimal point.
    [calm] Then it looks like a closed shape but is really open.
    [calm] An open shape cannot be measured for area later.
    [calm] Hatch it and the inside does not fill.

### Step 7 — Check it is one object

    [calm] Rest the cursor on the outline you just drew and click once.
    [asking] Do all six edges get selected? [calm] Then you drew it well, as one polyline.
    [emphatic] If only one edge is selected, you drew it as separate lines.
    [calm] Press Esc to clear the selection.

    [measured] To be more certain, type `LIST` and press Enter.
    [calm] Click the outline and press Enter.
    [light] A text window opens. [calm] You can see the object type, LWPOLYLINE.
    [calm] Whether it is closed, and the vertex coordinates, are listed too.
    [calm] Check that there are six vertices and that closed says yes.
    [calm] Press F2 to close the text window.

    [calm] There is a reason to confirm this before moving on.
    [calm] This outline becomes the reference for every position that follows.
    [calm] The centerlines, the boss centre, the points where the web starts — all of them come out of this shape.

### Step 8 — Switch to the centerline layer

    [measured] Open the layer dropdown at the top of the screen and choose `Centerline`.
    [measured] To do it from the command line, type `CLAYER` and press Enter.
    [measured] For the new value type `Centerline` and press Enter.
    [calm] Check with your eyes that the dropdown now reads centerline.
    [calm] Lines you draw from here go on in red, with the CENTER linetype.

### Step 9 — The vertical centerline (from the midpoint of the bottom edge)

    [calm] Look at the status bar again before you draw. [measured] Object snap F3, ortho F8, both on.
    [measured] Type `L` and press Enter. [calm] That is the line command.
    [calm] It asks for the first point. [measured] Here type `FROM` and press Enter.
    [calm] That means you will place a point a set distance from one you catch with a snap.

    [calm] It asks for the reference point. [calm] Rest the cursor around the middle of the base's bottom edge.
    [calm] When the triangle marker appears, click. [light] That is the midpoint.
    [calm] If a square appears you are still near a corner, so move the cursor a little toward the middle.
    [calm] Put the cursor below that point. [calm] Ortho is on, so it is fixed downward.
    [measured] Type `5` and press Enter. [calm] That is 5 down from the reference point.
    [calm] The cursor decides the direction and the number decides the distance. [cautionary] You never type a sign.

    [calm] It asks for the next point. [calm] Put the cursor above that point.
    [calm] Ortho is on, so the line is fixed vertical.
    [measured] Type `100` and press Enter. [calm] Then press Enter once more to end the command.

    [calm] There are two reasons at once for catching the midpoint of the bottom edge.
    [measured] Half of the base width of 120 is 60.
    [measured] The horizontal position of the boss centre is also 60.
    [calm] That is what it means for the part to be symmetrical about this line.
    [measured] The shape already holds that value, so there is no 60 to remember and type.

    [asking] Why is the length 100?
    [measured] The part is 90 from bottom to top, and you pushed 5 further down and 5 further up.
    [calm] A centerline has to run a little outside the shape.
    [calm] That is what makes the centre readable at a glance.
    [calm] This 5 is not a drawing dimension but a drafting convention. [measured] Anything from 3 to 5 will do.

### Step 10 — The horizontal centerline (62 up from the intersection)

    [calm] First you mark the height of the horizontal centerline.
    [measured] In the layer list choose `Dimension line`.
    [measured] `XL`, Enter, `H`, Enter.
    [calm] Click an endpoint of the base's bottom edge with the endpoint snap.
    [calm] Press Enter once to end the construction line command.
    [measured] `O`, Enter, distance `62`, Enter.
    [calm] Click the horizontal construction line you just made.
    [calm] Click an empty spot above it and press Enter to finish.
    [calm] The intersection of the upper construction line and the vertical centerline is the boss centre.

    [measured] Put the layer back to `Centerline`. [light] Turn F8 on.
    [measured] After `L`, Enter, click an empty spot away from the part.
    [measured] Put the cursor to the right and press `66`, Enter.
    [calm] Press Enter once more to end the line command.
    [measured] `M`, Enter. [calm] That is MOVE, the move command. [calm] Click the line you just drew and press Enter.
    [calm] For the base point, click the midpoint snap of that line.
    [calm] The second point is the intersection of the upper construction line and the vertical centerline.
    [calm] Watch for the intersection marker and click, and the move is done.
    [cautionary] Do not type FROM during the move.

    [measured] `QSELECT`, Enter, to open quick select.
    [calm] Apply to the entire drawing, object type construction line.
    [calm] Operator select all, how to apply include in new selection set.
    [emphatic] Press OK and check that only the two construction lines are selected.
    [measured] Erase them with `Delete`. [calm] What is left is the two centerlines.
    [measured] The horizontal length of 66 is the diameter of 56 plus 5 of margin at each end.

### Step 11 — Set the linetype scale

    [calm] If the centerline reads as a continuous line, set its scale.
    [calm] Click the two lines you just drew, in turn, to select them.
    [measured] Press `Ctrl+1` to open the Properties window.
    [measured] In the linetype scale box type `0.5` and press Enter. [calm] Press Esc to clear the selection.
    [measured] It is the value you wrote down in the layer table last lesson, centerline scale 0.5.
    [calm] This value sets the spacing of the dashes.
    [calm] Too large and the dashed line reads as continuous; too small and the dashes smear together.

    [calm] Leave yourself with an empty command line and nothing selected.
    [emphatic] The next command always starts from there.

### Step 12 — The boss circle Ø56

    [measured] In the layer dropdown go back to `Visible line`. [calm] The circle is a part line.
    [measured] Type `C` and press Enter. [calm] That is the circle command.
    [calm] A moment ago the polyline had a closing option that was also C.
    [light] The test is simple.
    [calm] Typed when no command is running, C is the circle command.

    [calm] It asks for the centre point. [calm] Rest the cursor where the two centerlines meet.
    [calm] When the cross marker appears, click. [cautionary] You do not type coordinates.
    [emphatic] Making this intersection is exactly why you drew the centerlines first.

    [calm] It asks for the radius. [calm] But what is written on the drawing is the diameter.
    [measured] Type `D` and press Enter.
    [calm] Now it asks the diameter. [measured] `56`, Enter.

    [asking] What happens if you skip D and put 56 straight in?
    [measured] You get a circle of radius 56. [calm] Twice the size on the drawing.
    [cautionary] Almost every mistake made with circles is made right here.
    [calm] If the drawing gives a diameter, press D first.

    [calm] Let me tell you a story from the floor about why this matters.
    [calm] At the LG Innotek site, when a machine stops you have to make a spare part in a hurry.
    [calm] In PM, that is preventive maintenance, you open the assembly drawing and find the part. [calm] You take that part drawing to the machine shop and talk it over.
    [calm] Hand it over with diameter and radius swapped and the part comes back twice the size.
    [emphatic] That is where the reason for drawing and reading a drawing exactly sits.

    [calm] Look at the top of the circle you drew. [calm] Its height has to match the top of the part.
    [measured] Add the radius of 28 to the centre height of 62 and you get 90.
    [measured] The overall height of the part was 90.
    [calm] If those two numbers agree, both the centre position and the diameter are right.

### Step 13 — Find the two points where the web starts

    [measured] The web foot is 80 wide. [measured] That is 40 either side of the vertical centre. [cautionary] Since the start points do not exist yet, you make them as construction line intersections. [measured] Change the layer to `Dimension line`. [measured] `XL`, Enter, `V`, Enter. [calm] Click the midpoint snap of the base's bottom edge and press Enter to finish. [measured] `O`, Enter, distance `40`, Enter. [calm] Click the vertical construction line you just made, then click to its left. [calm] Click that same middle construction line again, then click to its right. [calm] Press Enter to end the offset. [measured] `XL`, Enter, `H`, Enter. [calm] Click the top endpoint of the chamfer with the endpoint snap and press Enter to finish. [calm] Where this horizontal line meets the left and right construction lines are the web start points. [cautionary] You do not have to memorise the numbers as coordinates. [measured] Put the layer back to `Visible line`. [calm] If the ortho indicator is on, press F8 to turn it off. [calm] Next you pick a tangent.

### Step 14 — The left web tangent

    [measured] Type `L` and press Enter. [calm] The first point is the intersection of the left vertical construction line and the horizontal construction line on the base's top face. [calm] Hold Shift and press the right mouse button. [calm] From the object snap menu choose intersection, and click that intersection. [measured] At the next point type `TAN` and press Enter. [calm] Put the cursor a little above the left quadrant of the boss circle. [calm] Watch for the tangent marker, click, then press Enter once to finish. [measured] If it catches the quadrant instead of the tangent, undo the line with `U`, Enter, and do it again. [calm] From a point outside a circle there are two lines tangent to it. [calm] Here you take the one that touches the upper left of the boss, on the outer profile.

### Step 15 — The right web tangent

    [measured] `L`, Enter.
    [calm] The first point is the intersection of the right vertical construction line and the horizontal construction line on the base's top face.
    [calm] Watch for the intersection snap marker and click.
    [measured] At the next point type `TAN` and press Enter.
    [calm] Put the cursor a little above the right quadrant of the boss circle.
    [calm] Watch for the tangent marker, click, and press Enter once to finish.
    [calm] See whether the two web lines are symmetrical about the vertical centerline.
    [calm] If one side differs, check the start intersection and the tangent pick again.

    [measured] `QSELECT`, Enter, to open quick select.
    [calm] Apply to the entire drawing, object type construction line.
    [calm] Operator select all, how to apply include in new selection set.
    [light] Press OK. [emphatic] Check that only the four construction lines are selected.
    [measured] Erase them with `Delete` and clear the selection with `Esc`.
    [measured] Leave the current layer as `Visible line`.
    [calm] What remains is the base polyline, two centerlines, the boss circle and two web lines.
    [calm] You do nothing further to join the outline; you save it in this state.

### Step 16 — Save under a new name

    [measured] Type `SAVEAS` and press Enter.
    [measured] Change the end of the file name to `L03_PROFILE`. [calm] Leave the file type as AutoCAD drawing, dwg.
    [light] Press Save.

    [calm] Last lesson's file is not erased; it stays as it is.
    [calm] Every lesson you save under a changed name.
    [calm] Then you can go back to any stage you like.
    [calm] Next time you open this file and start there.

## Line 6 — This is where people go wrong (Frame 6)

**Time:** 20:09–22:29

    [calm] The same mistakes come round again. [light] There are four. [calm] We will look at how to notice each one while drawing, and how to fix it.

    (1 card — how to check the chamfer size) [pointing] Start with the shape after the chamfer. [measured] The first rectangle is 120 across and 16 high. [measured] Cut 5 off each of the top two corners and the vertical edges are left at 11. [measured] The straight part of the top face is 110. [calm] You use these values to check the chamfer result. [measured] To draw it, you give REC 120 and 16, and CHAMFER 5 and 5. [calm] Check by eye that the two chamfers are the same size. [calm] The top face has to be shorter than the bottom edge. [calm] If it looks otherwise, check the chamfer distances. [cautionary] Some people also mistake 16 for the plate thickness. [calm] 16 is the height seen from the front. [calm] The thickness is 12 and you read it in the top view.

    (2 card — typing a length without turning ortho on) [emphatic] You use the method of setting the direction with the mouse and typing only the length. [emphatic] But if F8 ortho is off, the cursor is not exactly horizontal. [calm] The length is right and the direction is half a degree out. [calm] On screen you can barely see it. [calm] There are two ways to notice. [calm] The first is to look at whether the ortho button in the status bar is pressed. [measured] The second is to click the line you drew and use `Ctrl+1` to see whether the start and end Y values are the same. [measured] To fix it, type `U` and press Enter right there. [emphatic] Inside a command, U undoes only the last point. [measured] Once you have left the command it is `Ctrl+Z`.

    (3 card — drawing without changing the layer) [pointing] It is time to draw a centerline. [calm] But you draw it while still on the visible line layer. [calm] A line that should be a red dashed one comes out green and continuous. [light] The reverse happens too. [calm] Draw the visible outline while still on the centerline layer and the part's profile comes out red and dashed. [calm] Once the colors are familiar, you see it at once. [calm] The fix is not to erase it and draw it again. [cautionary] Click the line you drew wrong to select it. [calm] Choose the right layer in the layer dropdown. [light] The line moves across. [calm] Press Esc to clear the selection. [light] There is one habit. [calm] Look at the layer indicator before you type a command.

    (4 card — the tangent snap being off) [pointing] You go to draw the web line and the tangent does not catch. [calm] Some other nearby point gets caught instead. [calm] The line cuts into the circle, or ends short of it. [calm] Zoom right in and look. [cautionary] The circle and the line do not touch; they cross past each other. [calm] There are two places to check. [calm] Whether object snap is on in the status bar, that is F3. [measured] And type `OS` and press Enter. [calm] See whether tangent is ticked on the object snap tab. [measured] Rather than leaving it on all the time, typing `TAN` for a single use as we did today is the surer way.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 22:29–24:43

    (1 left) [pointing] You opened last lesson's template and checked the snap state first. [calm] On the visible line layer you made the base rectangle with REC. [measured] You clicked the first corner and gave 120 and 16 through the dimensions option. [calm] Then you gave CHAMFER 5 and 5. [emphatic] You cut only the top two corners and finished the base outline. [calm] Next you switched to the centerline layer. [calm] From the midpoint of the bottom edge you stood the vertical centerline up. [calm] You made the horizontal centerline 66 long and moved it by its midpoint. [calm] It is the line that sits 62 up from the bottom. [emphatic] This is exactly why a shape has to exist before a snap can catch it. [calm] The boss circle went on the intersection of the two centerlines. [calm] You put 56 in through the diameter option. [calm] For the web you stepped 40 either way from the reference intersection on the base's top face. [calm] From those two points you ran lines to the boss circle with the tangent snap. [calm] Last you checked the top height of 90. [calm] You typed no coordinates at all while drawing the part today. [calm] In this course, typed coordinates are used at the two corners of the sheet edge and nowhere else. [calm] Everything else is caught with snaps, direction and a typed length. [calm] You saved the file under the name L03_PROFILE. [calm] It is the same order when you propose a jig to make a job easier. [calm] You fix the shape, pull the reference out of that shape, and put the circle on the reference.

    (2 right) [pointing] Next time you work with circles, arcs and offset. [calm] You start by tidying up what was left today. [calm] The inside corner where the web line meets the top face of the base. [measured] The 2-R10 fillet goes in there. [calm] The two theoretical corners where the web starts disappear, because they turn into radii. [calm] It is the place that keeps the load from piling onto one point. [calm] That is why it has the largest radius on this part. [calm] Then you trim away the part of the base's top face that runs between the two web lines. [calm] The base and the web are the same plate. [light] Both are 12 thick. [calm] A face that runs continuously has no edge in it. [calm] And yet there is a line drawn there right now. [calm] Next time you erase that stretch. [calm] You tidy the outline into a single run. [calm] The boss circle stays as it is. [calm] It is a whole circle. [calm] The bore and the boss thickness go in next time. [calm] And you will look at offset. [calm] It makes a line a set distance from one already drawn. [calm] It is how you avoid drawing the same shape twice. [emphatic] It is not a command used only on drawings. [calm] You use it to set wall thickness on an equipment layout. [calm] You use it to check the clearance of a walkway too. [calm] You pick up the trim command alongside it here.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 24:43–26:32

    [calm] Here are today's commands in one place. [emphatic] Rather than the names, remember **when you use them**.
    [calm] That is the part that stays after the exam.

    (1) [measured] `OPEN`. [light] Opens a file. [calm] You use it to carry on every lesson from the previous state.

    (2) [measured] `Z`. [light] ZOOM. [light] Changes the zoom. [calm] You use it when you need to see where a snap landed.

    (3) [measured] `OS`. [light] OSNAP. [calm] Chooses which object snaps are on. [emphatic] You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) [measured] `L`. [light] LINE. [light] Draws a line. [calm] You use it for pieces you need to handle singly.

    (5) [measured] `REC`. [light] RECTANG. [calm] Draws a rectangle as one polyline. [calm] You use it for the border, the title block and a plate outline.

    (6) [measured] `TRIMMODE`. [calm] Decides whether the original lines are tidied after a chamfer or fillet. [calm] You use it to cut the original line back to the end of an arc or a slanted edge.

    (7) [measured] `CHA`. [light] CHAMFER. [light] Chamfers between two edges. [calm] You use it to cut a top corner at an angle by a given distance.

    (8) [measured] `LIST`. [light] Shows an object's information. [calm] You use it to check that what you drew really is that value.

    (9) [measured] `CLAYER`. [light] Changes the current layer. [calm] You use it to change layer from the command line.

    (10) [measured] `XL`. [light] XLINE. [calm] Draws a construction line that runs on forever. [calm] You use it for projection lines.

    (11) [measured] `O`. [light] OFFSET. [calm] Makes the same shape a set distance away. [calm] You use it for concentric circles and parallel lines without picking the centre again.

    (12) [measured] `M`. [light] MOVE. [light] Moves something. [calm] You use it to bring a centerline or a view onto a reference point.

    (13) [measured] `QSELECT`. [calm] Picks every object matching a condition at once. [emphatic] You use it to select only the construction lines and erase them.

    (14) [measured] `C`. [light] CIRCLE. [light] Draws a circle. [calm] You use it for holes, shafts and pitch circles.

    (15) [measured] `SAVEAS`. [calm] Saves under a new name. [calm] You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 26:32–26:46

    (1) [light] That is today's portion. [calm] It was the lesson where you drew part lines for the first time. [warm] Well done.

    (2) [pointing] Next is Lesson 4, circles, arcs and offset. [warm] See you then.
