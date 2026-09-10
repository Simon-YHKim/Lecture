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

    Lesson 3, datum lines and the outline.

## Line 2 — What you draw today (Frame 2)

**Time:** 0:05–2:04

    Last time you made the A3 border. You set up four layers as well. Today you open that file. For the first time you draw part lines. Four things go on the screen.

    (1 card — centerlines) Start with how not to place a centerline by eye. This part is symmetrical left and right about the vertical centerline. There is the boss circle, the bore, the four tapped holes. Every one of them starts from a point on that centerline. So if the centerline is exact, everything after it is exact. Where does an exact centerline come from? From the midpoint of the base's bottom edge, which you have already drawn. For a snap to have something to catch, the shape has to exist first. So today you draw the outline first, and pull the centerline out of that shape.

    (2 card — base 120 × 16 outline) You draw the outer profile of the bottom plate. 120 across, and 16 high seen from the front. This plate is the first thing you draw today. This plate decides where the whole part sits. The 120 across is the whole width of the part. For the plate's lower left corner you just click an empty spot inside the border. You do not type coordinates. What happens if that wanders? Everything that stands on it wanders too.

    (3 card — chamfers 2-C5) You cut the two upper corners of the base. 5 off each, at 45 degrees. On the drawing that is 2-C5. The 2 is the count, C is a chamfer, 5 is the length of the side cut off. Leave a sharp corner and it cuts your hand. It clashes with another part on assembly. Paint goes on thin at a sharp edge, too. Cut it and all three go away at once. You make the rectangle first and cut it with the chamfer command. You give the 5 and 5 that are written on the drawing as the two distances.

    (4 card — boss circle Ø56 and the tangent web) You draw the outer circle of the boss at the top. Then you draw the web that climbs from the base to that circle. Two lines. The web lines have to touch the boss circle exactly. What does touching mean here? It means meeting at one point, in passing. Not cutting in, not falling short. Place that one point by eye and it will be wrong every time. That is why you use the tangent object snap today.

## Line 3 — Four ways to place a point, two commands that make a line (Frame 3)

**Time:** 2:04–4:50

    A line is made of two points. So drawing accurately means placing points accurately. There are four ways to place one. There is only one test for choosing. Is that point fixed by a drawing dimension? And there are two commands that string those points into lines.

    (1 card — object snap F3) You place the point by catching a feature point of something already drawn. Six of them: endpoint, midpoint, center, quadrant, intersection and tangent. Rest the cursor and a marker appears. You check the marker, then click. This is the way you use most today. You catch the midpoint of the bottom edge and the centerline intersection this way. You find the tangent point on the boss circle the same way. If the shape already holds the answer, there is no reason to type the number again. If what you drew earlier is wrong, what comes after goes wrong with it. So the error shows up immediately.

    (2 card — ortho and typed values F8, F12) You fix the direction with the mouse and type only the length. Turn ortho on with F8 and the cursor moves only horizontally and vertically. Put the cursor on the side you are heading and type the number. For a line 10 upward, put the cursor above that point and type 10. With F12 dynamic input on, the number goes into the box beside the cursor. With it off it goes to the command line at the bottom. The place you type differs; the value is the same. If you need a slanted direction, fix the angle with F10 polar tracking. You draw today's two centerlines this way.

    (3 card — snap tracking and FROM, F11) This is how you make a point the shape does not have yet. Turn F11 on and rest the cursor on a feature point for a moment. A guide line reaches out from that point. Get a second guide line to reach out from another point. When a marker appears where the two guides meet, click. FROM works a little differently. You catch a reference point, then say how far from it to go. You place the start of the vertical centerline this way today. Both of them take a point on the shape as their reference. That is why you do not have to memorise coordinates.

    (4 card — LINE and PLINE and REC) An outline that goes all the way round is drawn as one body. REC makes a rectangle as a single object. With PLINE the whole run you drew is one object. One click selects the whole thing. Offset and area also apply to the whole outline at once. On the floor you run a polyline around the area a machine will occupy. Then you get its area in one go. When you try moving it, you drag the whole thing at once. LINE is the opposite: draw one after another and each stays a separate line. A piece you will trim and round later is easier to handle as a single line.

    (5 note — which one to use) One thing decides which of the four you use. Check whether that point is fixed by a drawing dimension. If it is, pull it out of the shape with a snap or with tracking. If only a length is given, fix the direction with the mouse and type the number. A point no dimension fixes, you simply click. The first point of the base outline is one of those. It only has to be somewhere the part fits inside the border. Place a point that a dimension does fix by eye, on the other hand, and the drawing is wrong. In this whole course, the only place you type coordinates is the two corners of the sheet edge.

## Line 4 — On the drawing (Frame 4)

**Time:** 4:50–7:28

    The front view is on the left, and on the right a table of the values you use today. We will work down the table and see where each value comes from on the drawing, in order.

    (1 row) Start with where the dimensions are measured from. Most of this part's dimensions are measured from the left edge and the bottom. The 60 and 62 of the boss centre are. So are the 35 and 85 of the slot centres, and their height of 8. So you take the lower left corner of the base as your reference. You do not, however, move the coordinate origin there. You catch that corner by clicking on screen. Every other position is pulled out of the shape. It is the same order when you draw a jig to propose it. You decide what to measure from before you start.

    (2 row) Read how the base is set up. You stand the rectangle up first, without worrying about the chamfers. With the REC command you click one corner, then press D for the dimensions option. 120 across, 16 up. Those two numbers are written on the drawing as they are. All four corners land exactly, in one go. Which corner you clicked first does not matter. It is not a point that a dimension fixes.

    (3 row) The chamfers go on after the rectangle is standing. 2-C5 means cutting 5 off at 45 degrees. The 2 is the count, C is a chamfer, 5 is the length of the side cut off. You give the CHAMFER command 5 and 5 and cut only the top two corners. You never have to type a computed value like 11 or 115. The numbers on the drawing are 120, 16 and 5. Those three are the only ones we typed. Make no computed values and you make no arithmetic slips either.

    (4 row) Look at the top face of the base. This height decides half of what you draw today. The web climbs from here. The R10 fillet you add next lesson starts here too. 16 is not the plate thickness but the height seen from the front. The thickness of 12 is a value you read in the top view. It does not appear in today's front view.

    (5 row) You draw the boss circle first. The diameter is 56. Its centre goes on the intersection of the two centerlines. The web lines have to be tangent to this circle. With no circle on screen to be tangent to, there is no tangent point to catch. That is why the circle comes before the web. Add the radius of 28 to the centre height of 62 and you get 90. That is the overall height of the part. The top of the boss circle is the top of this part.

    (6 row) Last, the web. Its foot is 80 wide. Take 80 from the base width of 120 and 40 is left, 20 on each side. So the web starts at two points. On the top face of the base, 40 either side of the vertical centerline. You do not place these two by coordinates either. You catch the midpoint snap on the top face and step 40 out each way. Then from those two points you draw tangent lines to the boss circle.

## Line 5 — Datum lines and the outline · DEMO-01 screen recording (Frame 5)

**Time:** 7:28–20:09

> This section is a screen recording. Work through the 16 steps below in order and without skipping, speaking as you go.
> What is inside backticks is what you actually type; everything else you check on screen or click.

### Step 1 — Open last lesson's file

    Start AutoCAD 2024. Type `OPEN` and press Enter.
    Find and open the file you saved last time. Its name ends in `L02_TEMPLATE`.
    Do not make a new one.
    It has the A3 border and the centering marks in it. It has the title block and four layers too.
    Every lesson you open the previous file like this and draw on top of it.

### Step 2 — Check the state

    Type `Z` and press Enter. Then type `A` and press Enter. That is zoom all.
    The whole border comes onto the screen.
    Press Esc twice to clear the command and the selection.
    `OS`, Enter. On the object snap tab, check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    Press OK to close the dialog, and press F3 only if object snap is off.
    `L`, Enter. While it asks for the first point, rest the cursor on a corner of the border. Do not click.
    See whether the square endpoint marker appears, then press Esc twice to cancel LINE.
    If there is no marker, check the OS settings and the F3 state again.
    Look at ortho too, and press F8 only if it is off.
    Open the layer dropdown. Visible line, centerline, hidden line, dimension line.
    Check that all four are there.
    What happens if you start drawing without checking here?
    Later on you find a line sitting on the wrong layer.
    Today you catch almost every position with a snap.
    With snap off, every click is done by eye.

### Step 3 — Switch to the visible line layer and zoom into the drawing area

    In the layer dropdown choose `Visible line`. Green, continuous.
    From here on you are drawing the shape of the part you can see.

    `Z`, Enter. At the options type `W` and press Enter. That is a window zoom.
    The inside of the rectangle you give fills the screen.
    In the lower left quarter of the border, drag a rectangle big enough for the part.
    Click the two corners in turn. You do not type coordinates.
    The part needs 120 by 90, so leave yourself a bit more than that.
    Draw it small and you cannot see where the snap landed.
    Put it up large and your hand has an easier time.

    The two corners of the zoom window are not fixed by any drawing dimension.
    Typing coordinates for a place like that costs time and buys no accuracy.

### Step 4 — Make the base rectangle (REC)

    Check in the status bar that object snap is on.
    Type `REC` and press Enter.
    Before you pick the first corner, clear the previous settings.
    Type `C`, the chamfer option, Enter, first distance `0`, Enter, second distance `0`, Enter.
    When it asks for the first corner again, type `F`, the fillet option, Enter, radius `0`, Enter.
    Check `W`, Enter, polyline width `0`, Enter as well.
    When it comes back to the first corner question, click the lower left of the area you are drawing in.
    Anywhere inside the border where the part will fit is fine. This position is free.
    At the opposite corner question, `R`, Enter, rotation angle `0`, Enter.
    When it asks for the opposite corner again, press `D`, Enter.
    Length is `120`, Enter. Width is `16`, Enter.
    Put the cursor above and to the right of the first point and click once.
    The rectangle command ends here. Do not press Enter again.
    A closed rectangle of 120 by 16 should be on screen.
    The chamfers go on in the next two steps, on the top two corners only.

### Step 5 — The right-hand chamfer

    `TRIMMODE`, Enter, `1`, Enter.
    That makes the two chamfered edges end on the new boundary.

    Type `CHA` and press Enter. That is the chamfer command.
    Type `D` and press Enter. That is the distance option.
    It asks the first distance. `5`, Enter.
    It asks the second distance. It is the same value, so you can simply press Enter.

    Now click the two edges that make the corner you are cutting, in turn.
    Click the top edge at the upper right corner, then click the right-hand vertical edge.
    The corner is cut at 45 degrees. 5 across and 5 up makes it exactly 45.

    The 2-C5 on the drawing is this value. You put in 5 and 5 as they are.
    Chamfer while drawing the rectangle and you have to work out values like 11 and 110 by hand.
    Those numbers appear nowhere on the drawing.
    Draw the rectangle first and chamfer separately, and you only ever type numbers the drawing gives you.

### Step 6 — The top face, the left chamfer, and closing

    The upper left corner works the same way.
    Type `CHA` again and press Enter. The distances are still 5 and 5.
    Click the top edge, then the left-hand vertical edge.

    Now you have a six-sided outline.
    The bottom two corners stay square. The drawing shows 2-C5 at the top two only.

    There is a way to cut all four corners at once.
    In `CHA` you press `P` and click the rectangle.
    That cuts the bottom two as well, though. So here you take them one at a time.

    The rectangle was closed from the start, so you never place the last edge by hand.
    Place it by hand and it misses by a fraction below the decimal point.
    Then it looks like a closed shape but is really open.
    An open shape cannot be measured for area later.
    Hatch it and the inside does not fill.

### Step 7 — Check it is one object

    Rest the cursor on the outline you just drew and click once.
    Do all six edges get selected? Then you drew it well, as one polyline.
    If only one edge is selected, you drew it as separate lines.
    Press Esc to clear the selection.

    To be more certain, type `LIST` and press Enter.
    Click the outline and press Enter.
    A text window opens. You can see the object type, LWPOLYLINE.
    Whether it is closed, and the vertex coordinates, are listed too.
    Check that there are six vertices and that closed says yes.
    Press F2 to close the text window.

    There is a reason to confirm this before moving on.
    This outline becomes the reference for every position that follows.
    The centerlines, the boss centre, the points where the web starts — all of them come out of this shape.

### Step 8 — Switch to the centerline layer

    Open the layer dropdown at the top of the screen and choose `Centerline`.
    To do it from the command line, type `CLAYER` and press Enter.
    For the new value type `Centerline` and press Enter.
    Check with your eyes that the dropdown now reads centerline.
    Lines you draw from here go on in red, with the CENTER linetype.

### Step 9 — The vertical centerline (from the midpoint of the bottom edge)

    Look at the status bar again before you draw. Object snap F3, ortho F8, both on.
    Type `L` and press Enter. That is the line command.
    It asks for the first point. Here type `FROM` and press Enter.
    That means you will place a point a set distance from one you catch with a snap.

    It asks for the reference point. Rest the cursor around the middle of the base's bottom edge.
    When the triangle marker appears, click. That is the midpoint.
    If a square appears you are still near a corner, so move the cursor a little toward the middle.
    Put the cursor below that point. Ortho is on, so it is fixed downward.
    Type `5` and press Enter. That is 5 down from the reference point.
    The cursor decides the direction and the number decides the distance. You never type a sign.

    It asks for the next point. Put the cursor above that point.
    Ortho is on, so the line is fixed vertical.
    Type `100` and press Enter. Then press Enter once more to end the command.

    There are two reasons at once for catching the midpoint of the bottom edge.
    Half of the base width of 120 is 60.
    The horizontal position of the boss centre is also 60.
    That is what it means for the part to be symmetrical about this line.
    The shape already holds that value, so there is no 60 to remember and type.

    Why is the length 100?
    The part is 90 from bottom to top, and you pushed 5 further down and 5 further up.
    A centerline has to run a little outside the shape.
    That is what makes the centre readable at a glance.
    This 5 is not a drawing dimension but a drafting convention. Anything from 3 to 5 will do.

### Step 10 — The horizontal centerline (62 up from the intersection)

    First you mark the height of the horizontal centerline.
    In the layer list choose `Dimension line`.
    `XL`, Enter, `H`, Enter.
    Click an endpoint of the base's bottom edge with the endpoint snap.
    Press Enter once to end the construction line command.
    `O`, Enter, distance `62`, Enter.
    Click the horizontal construction line you just made.
    Click an empty spot above it and press Enter to finish.
    The intersection of the upper construction line and the vertical centerline is the boss centre.

    Put the layer back to `Centerline`. Turn F8 on.
    After `L`, Enter, click an empty spot away from the part.
    Put the cursor to the right and press `66`, Enter.
    Press Enter once more to end the line command.
    `M`, Enter. That is MOVE, the move command. Click the line you just drew and press Enter.
    For the base point, click the midpoint snap of that line.
    The second point is the intersection of the upper construction line and the vertical centerline.
    Watch for the intersection marker and click, and the move is done.
    Do not type FROM during the move.

    `QSELECT`, Enter, to open quick select.
    Apply to the entire drawing, object type construction line.
    Operator select all, how to apply include in new selection set.
    Press OK and check that only the two construction lines are selected.
    Erase them with `Delete`. What is left is the two centerlines.
    The horizontal length of 66 is the diameter of 56 plus 5 of margin at each end.

### Step 11 — Set the linetype scale

    If the centerline reads as a continuous line, set its scale.
    Click the two lines you just drew, in turn, to select them.
    Press `Ctrl+1` to open the Properties window.
    In the linetype scale box type `0.5` and press Enter. Press Esc to clear the selection.
    It is the value you wrote down in the layer table last lesson, centerline scale 0.5.
    This value sets the spacing of the dashes.
    Too large and the dashed line reads as continuous; too small and the dashes smear together.

    Leave yourself with an empty command line and nothing selected.
    The next command always starts from there.

### Step 12 — The boss circle Ø56

    In the layer dropdown go back to `Visible line`. The circle is a part line.
    Type `C` and press Enter. That is the circle command.
    A moment ago the polyline had a closing option that was also C.
    The test is simple.
    Typed when no command is running, C is the circle command.

    It asks for the centre point. Rest the cursor where the two centerlines meet.
    When the cross marker appears, click. You do not type coordinates.
    Making this intersection is exactly why you drew the centerlines first.

    It asks for the radius. But what is written on the drawing is the diameter.
    Type `D` and press Enter.
    Now it asks the diameter. `56`, Enter.

    What happens if you skip D and put 56 straight in?
    You get a circle of radius 56. Twice the size on the drawing.
    Almost every mistake made with circles is made right here.
    If the drawing gives a diameter, press D first.

    Let me tell you a story from the floor about why this matters.
    At the LG Innotek site, when a machine stops you have to make a spare part in a hurry.
    In PM, that is preventive maintenance, you open the assembly drawing and find the part. You take that part drawing to the machine shop and talk it over.
    Hand it over with diameter and radius swapped and the part comes back twice the size.
    That is where the reason for drawing and reading a drawing exactly sits.

    Look at the top of the circle you drew. Its height has to match the top of the part.
    Add the radius of 28 to the centre height of 62 and you get 90.
    The overall height of the part was 90.
    If those two numbers agree, both the centre position and the diameter are right.

### Step 13 — Find the two points where the web starts

    The web foot is 80 wide. That is 40 either side of the vertical centre. Since the start points do not exist yet, you make them as construction line intersections. Change the layer to `Dimension line`. `XL`, Enter, `V`, Enter. Click the midpoint snap of the base's bottom edge and press Enter to finish. `O`, Enter, distance `40`, Enter. Click the vertical construction line you just made, then click to its left. Click that same middle construction line again, then click to its right. Press Enter to end the offset. `XL`, Enter, `H`, Enter. Click the top endpoint of the chamfer with the endpoint snap and press Enter to finish. Where this horizontal line meets the left and right construction lines are the web start points. You do not have to memorise the numbers as coordinates. Put the layer back to `Visible line`. If the ortho indicator is on, press F8 to turn it off. Next you pick a tangent.

### Step 14 — The left web tangent

    Type `L` and press Enter. The first point is the intersection of the left vertical construction line and the horizontal construction line on the base's top face. Hold Shift and press the right mouse button. From the object snap menu choose intersection, and click that intersection. At the next point type `TAN` and press Enter. Put the cursor a little above the left quadrant of the boss circle. Watch for the tangent marker, click, then press Enter once to finish. If it catches the quadrant instead of the tangent, undo the line with `U`, Enter, and do it again. From a point outside a circle there are two lines tangent to it. Here you take the one that touches the upper left of the boss, on the outer profile.

### Step 15 — The right web tangent

    `L`, Enter.
    The first point is the intersection of the right vertical construction line and the horizontal construction line on the base's top face.
    Watch for the intersection snap marker and click.
    At the next point type `TAN` and press Enter.
    Put the cursor a little above the right quadrant of the boss circle.
    Watch for the tangent marker, click, and press Enter once to finish.
    See whether the two web lines are symmetrical about the vertical centerline.
    If one side differs, check the start intersection and the tangent pick again.

    `QSELECT`, Enter, to open quick select.
    Apply to the entire drawing, object type construction line.
    Operator select all, how to apply include in new selection set.
    Press OK. Check that only the four construction lines are selected.
    Erase them with `Delete` and clear the selection with `Esc`.
    Leave the current layer as `Visible line`.
    What remains is the base polyline, two centerlines, the boss circle and two web lines.
    You do nothing further to join the outline; you save it in this state.

### Step 16 — Save under a new name

    Type `SAVEAS` and press Enter.
    Change the end of the file name to `L03_PROFILE`. Leave the file type as AutoCAD drawing, dwg.
    Press Save.

    Last lesson's file is not erased; it stays as it is.
    Every lesson you save under a changed name.
    Then you can go back to any stage you like.
    Next time you open this file and start there.

## Line 6 — This is where people go wrong (Frame 6)

**Time:** 20:09–22:29

    The same mistakes come round again. There are four. We will look at how to notice each one while drawing, and how to fix it.

    (1 card — how to check the chamfer size) Start with the shape after the chamfer. The first rectangle is 120 across and 16 high. Cut 5 off each of the top two corners and the vertical edges are left at 11. The straight part of the top face is 110. You use these values to check the chamfer result. To draw it, you give REC 120 and 16, and CHAMFER 5 and 5. Check by eye that the two chamfers are the same size. The top face has to be shorter than the bottom edge. If it looks otherwise, check the chamfer distances. Some people also mistake 16 for the plate thickness. 16 is the height seen from the front. The thickness is 12 and you read it in the top view.

    (2 card — typing a length without turning ortho on) You use the method of fixing direction with the mouse and typing only the length. But if F8 ortho is off, the cursor is not exactly horizontal. The length is right and the direction is half a degree out. On screen you can barely see it. There are two ways to notice. The first is to look at whether the ortho button in the status bar is pressed. The second is to click the line you drew and use `Ctrl+1` to see whether the start and end Y values are the same. To fix it, type `U` and press Enter right there. Inside a command, U undoes only the last point. Once you have left the command it is `Ctrl+Z`.

    (3 card — drawing without changing the layer) It is time to draw a centerline. But you draw it while still on the visible line layer. A line that should be a red dashed one comes out green and continuous. The reverse happens too. Draw the visible outline while still on the centerline layer and the part's profile comes out red and dashed. Once the colors are familiar, you see it at once. The fix is not to erase it and draw it again. Click the line you drew wrong to select it. Choose the right layer in the layer dropdown. The line moves across. Press Esc to clear the selection. There is one habit. Look at the layer indicator before you type a command.

    (4 card — the tangent snap being off) You go to draw the web line and the tangent does not catch. Some other nearby point gets caught instead. The line cuts into the circle, or ends short of it. Zoom right in and look. The circle and the line do not touch; they cross past each other. There are two places to check. Whether object snap is on in the status bar, that is F3. And type `OS` and press Enter. See whether tangent is ticked on the object snap tab. Rather than leaving it on all the time, typing `TAN` for a single use as we did today is the surer way.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 22:29–24:43

    (1 left) You opened last lesson's template and checked the snap state first. On the visible line layer you made the base rectangle with REC. You clicked the first corner and gave 120 and 16 through the dimensions option. Then you gave CHAMFER 5 and 5. You cut only the top two corners and finished the base outline. Next you switched to the centerline layer. From the midpoint of the bottom edge you stood the vertical centerline up. You made the horizontal centerline 66 long and moved it by its midpoint. It is the line that sits 62 up from the bottom. This is exactly why a shape has to exist before a snap can catch it. The boss circle went on the intersection of the two centerlines. You put 56 in through the diameter option. For the web you stepped 40 either way from the reference intersection on the base's top face. From those two points you ran lines to the boss circle with the tangent snap. Last you checked the top height of 90. You typed no coordinates at all while drawing the part today. In this course, typed coordinates are used at the two corners of the sheet edge and nowhere else. Everything else is caught with snaps, direction and a typed length. You saved the file under the name L03_PROFILE. It is the same order when you propose a jig to make a job easier. You fix the shape, pull the reference out of that shape, and put the circle on the reference.

    (2 right) Next time you work with circles, arcs and offset. You start by tidying up what was left today. The inside corner where the web line meets the top face of the base. The 2-R10 fillet goes in there. The two theoretical corners where the web starts disappear, because they turn into radii. It is the place that keeps the load from piling onto one point. That is why it has the largest radius on this part. Then you trim away the part of the base's top face that runs between the two web lines. The base and the web are the same plate. Both are 12 thick. A face that runs continuously has no edge in it. And yet there is a line drawn there right now. Next time you erase that stretch. You tidy the outline into a single run. The boss circle stays as it is. It is a whole circle. The bore and the boss thickness go in next time. And you will look at offset. It makes a line a set distance from one already drawn. It is how you avoid drawing the same shape twice. It is not a command used only on drawings. You use it to set wall thickness on an equipment layout. You use it to check the clearance of a walkway too. You pick up the trim command alongside it here.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 24:43–26:32

    Here are today's commands in one place. Rather than the names, remember **when you use them**.
    That is the part that stays after the exam.

    (1) `OPEN`. Opens a file. You use it to carry on every lesson from the previous state.

    (2) `Z`. ZOOM. Changes the zoom. You use it when you need to see where a snap landed.

    (3) `OS`. OSNAP. Chooses which object snaps are on. You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) `L`. LINE. Draws a line. You use it for pieces you need to handle singly.

    (5) `REC`. RECTANG. Draws a rectangle as one polyline. You use it for the border, the title block and a plate outline.

    (6) `TRIMMODE`. Decides whether the original lines are tidied after a chamfer or fillet. You use it to cut the original line back to the end of an arc or a slanted edge.

    (7) `CHA`. CHAMFER. Chamfers between two edges. You use it to cut a top corner at an angle by a given distance.

    (8) `LIST`. Shows an object's information. You use it to check that what you drew really is that value.

    (9) `CLAYER`. Changes the current layer. You use it to change layer from the command line.

    (10) `XL`. XLINE. Draws a construction line that runs on forever. You use it for projection lines.

    (11) `O`. OFFSET. Makes the same shape a set distance away. You use it for concentric circles and parallel lines without picking the centre again.

    (12) `M`. MOVE. Moves something. You use it to bring a centerline or a view onto a reference point.

    (13) `QSELECT`. Picks every object matching a condition at once. You use it to select only the construction lines and erase them.

    (14) `C`. CIRCLE. Draws a circle. You use it for holes, shafts and pitch circles.

    (15) `SAVEAS`. Saves under a new name. You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 26:32–26:46

    (1) That is today's portion. It was the lesson where you drew part lines for the first time. Well done.

    (2) Next is Lesson 4, circles, arcs and offset. See you then.
