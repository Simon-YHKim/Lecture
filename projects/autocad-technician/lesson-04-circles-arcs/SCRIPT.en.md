# SCRIPT — AutoCAD Technician Lesson 4 · Circles, arcs and offset (English edition)

**Part:** `idler pulley bracket used on a car engine` (internal drawing number EDU-IB-02)<br>
**Checkpoint:** `L03_PROFILE → L04_FEATURES`<br>
**Voice:** Windows SAPI · Microsoft Zira Desktop · Rate 0 · pitch-preserving 1.15x<br>
**Voice direction:** Say the value first, then where it came from. Do not hurry a question toward its answer; leave a beat and carry on. Through the hands-on section (Line 5), keep to the speed a hand moves.

> Length not measured yet. The times below mirror the Korean script so the frames
> line up; they are replaced by measured values once the English speech exists.
> The parentheses name what lights up on screen at that moment. They are not read.

## Line 1 — Title (Frame 1)

**Time:** 0:00–0:10

    (silence)

    Lesson 4, circles, arcs and offset. You draw the inside of the idler pulley bracket that goes on a car engine.

## Line 2 — Filling in inside the outline (Frame 2)

**Time:** 0:10–1:44

    Last time you drew the outer profile of the idler pulley bracket. It is a part that goes on a car engine. You finished the base, the web and the boss circle. Today you put four shapes inside it. Every one of them starts from a circle. You draw a circle, push it, fit one in, and rotate a copy round.

    (1 card — bore Ø25) The first is the bore in the middle. It goes right through, 25 across, and its centre is where the boss centre is: 60 from the left end, 62 from the bottom. This hole is the reference of the part, and the shaft sits in here and turns. If this hole is off, the part is unusable however right the rest of it is. That is why you draw it first today.

    (2 card — tapped 4-M5 in a polar array) The second is the four screw seats. They sit around the bore. You cut M5 threads 10 deep. The four centres lie on a circle 44 across. The first hole is at 45 degrees. The rest step round every 90. You do not draw the four one at a time. You draw one and rotate it round with a polar array. That way the angle is set by arithmetic, not by hand.

    (3 card — slots 2-R5) The third is the two long holes at the bottom. They are 10 wide and each end is a half-circle of radius 5. One circle command will not give you that. You draw the two end circles, join them with tangent lines, and trim the inside away to get the pill shape. That is where you use the trim command today.

    (4 card — fillets 2-R10) The fourth is the inside corner. It is where the web turns into the base. You round it at radius 10. You do not draw a separate circle here. You only pick two lines. The command fits the arc between them itself. It trims what is left over as well. This is where the load piles up most. That is why the R is as large as 10. It is the story from Lesson 2.

## Line 3 — The four commands you use today (Frame 3)

**Time:** 1:44–4:11

    Before you draw, here are the four commands you use today. Know what each one is for and the order of work follows easily.

    (1 card — CIRCLE) The circle command. Its shortcut is `C`. There are five ways to draw a circle, and today you use the first two. First, pick the centre and give the radius. That is the default. Second, pick the centre and, where it asks for the radius, press `D` and give the diameter instead. The other three are two-point, three-point, and tangent-tangent-radius; knowing their names is enough. Which one you use follows the drawing's notation exactly. A value written with Ø is a diameter, so that is the second method. A value written with R is a radius, so that is the first. Follow the notation and you make fewer mistakes.

    (2 card — OFFSET) Offset. Its shortcut is `O`. It copies the object you pick, parallel to itself. You give the distance yourself. Offset a straight line and you get a parallel line. Offset a circle and you get a concentric circle. You make the pitch circle with this today. You do not pick the centre again. So the centre cannot go out of line. It is a command you reach for often on the floor. You use it when you look at an equipment layout. You set wall thicknesses; you set walkway clearances. You push out from one datum line. There are three options. Through takes a point to pass through instead of a distance. Erase moves it, deleting the original. Layer decides where the copy goes. You choose between the source layer and the current layer. The default is source. Leave it and the copy follows the original's layer.

    (3 card — FILLET) Fillet. Its shortcut is `F`. Pick two lines and it fits an arc between them. The radius is a value you set beforehand. It trims what runs past the corner. The order matters. Set the radius first, then pick the lines. That is because the default radius is 0. Run it without setting it and no arc appears — you just get a square corner. You put the radius in with the `R` option. There is a polyline option too. It rounds every corner of a polyline at once.

    (4 card — ARRAYPOLAR) The polar array. This one has no short form of its own. You type the whole name. You pick the object. You pick a centre point. You say how many, at what angular spacing. It copies them just so. There are four options: number of items, angle between them, angle to fill, and whether it is associative. The angle between is the gap between neighbouring items. The angle to fill is the angle the whole thing turns through. You use it with associative off. Leave it on and the four are bound into one body. You cannot pick one of them on its own. Sooner or later you will need to edit one individually.

## Line 4 — On the drawing (Frame 4)

**Time:** 4:11–7:56

    You know the commands. We will point at the drawing on the right and see what goes where. There are six, and the order of pointing is the order of work.

    (1 row — bore Ø25 H7) The bore in the middle. Its centre is 60, 62. The same centre as the boss. There is one thing to watch here. The drawing says Ø25. That is a diameter. But what the circle command asks for by default is the radius. Put 25 in as it stands and you get a hole 50 across. Exactly twice. So you press `D` to switch to diameter entry. Then you put 25 in. H7 is a fit grade. It has no effect on the shape. You draw it at 25. The grade goes on as text when you dimension. The reason that grade matters is out on the floor. When a machine stops you have to find a spare in a hurry. You look at the assembly drawing and find that part drawing. You hand that drawing to the machine shop. Leave the grade line off at that moment and the shaft does not go in.

    (2 row — boss Ø56) You already drew the boss circle last time. You drew the two web lines tangent to this circle. Without this circle the outline does not hold together. Today you do not draw this circle again. You use it as a reference instead. You push the next row's pitch circle out of it.

    (3 row — pitch circle PCD Ø44) This is the circle the four tapped-hole centres sit on. It is not a hole itself. It is a helper circle that fixes where the holes go. So it is not a visible line. You draw it on the centerline layer. On screen it should come out as a red chain line. The way to make it is offset. You push the boss Ø56 inward. The distance is 56 take away 44, divided by 2, which is 6. Half the difference in diameter is the difference in radius. That is because offset pushes the radius. Do it this way and you never retype the centre coordinates. The boss and the pitch circle cannot end up on different centres.

    (4 row — tapped 4-M5) The four screw seats. The first hole is at 45 degrees and the rest step round every 90. The order of drawing is this. From the boss centre, draw one helper line 22 long in the 45 degree direction. 22 is half of the pitch circle diameter of 44, that is, the radius. Then the end of that helper line lands exactly on the pitch circle at 45 degrees. You draw one hole there, make four with a polar array, and erase the helper line. You do not set the angle by eye. You fix the direction with polar tracking and type only the distance.

    (5 row — slots 2-R5) The long holes at the bottom. The left slot's centre is at 35, 8. Halve the 12 between the two end circle centres and you get 6. Step 6 either side of the centre at 35 and you get 29 and 41. 29 is written on the drawing as it stands: 29 from the left edge to the first end circle. The two values agree. The order of drawing is this. You draw the two end circles at radius 5. You draw tangent lines above and below. You trim away the half-circles that point inward. Once trimmed, a circle becomes an arc. That is why the word arc is in today's title. You do not draw the right slot again. You mirror it. The two slot centres are 35 and 85. Halfway between them is 60. 60 is the horizontal position of the boss centre. That is what it means for the part to be symmetrical about this line. Slots come up often on the floor too — when you propose a jig to make a job easier. Put the bolt seats in slots and you can shift the position a little at a time.

    (6 row — fillets 2-R10) Last is the inside corner where the web meets the base. Between the web tangent and the top face of the base. The top face of the base is a horizontal plane at height 16. You round it here at radius 10. The drawing gives a centre height of 26. That is for checking. The top face of the base is at 16. The fillet is tangent to that face. So the centre is 16 plus 10, which is 26. There is one reference dimension in brackets, (95.7). It is a value computed from the others, so you do not type it. Once the fillet command has bitten on the two lines, the centre lands there by itself.

## Line 5 — Circles, arcs and offset · DEMO-01 screen recording (Frame 5)

**Time:** 7:56–21:48

> This section is a screen recording. Work through the 16 steps below in order and without skipping, speaking as you go.
> A command written in capitals is the command; what is inside backticks is what you actually type.
> You do not place anything by eye. If something is already drawn, catch it with a snap, fix the direction with ortho or polar tracking, and type only the distance.
> A snap is not eyeballing — it takes a point the drawing already holds, so it is more accurate than a typed coordinate. Let a circle centre be out by one millimetre and everything after it is out.

### Step 1 — Open the previous file

    You do not make a new one. Type `OPEN` and press Enter.
    Choose the file you saved last lesson. (on screen · `EDU-IB-02_L03_PROFILE.dwg`)
    Press Open.
    The base and its chamfers should be on screen. The two web lines and the boss circle should be there too.
    That is today's starting state.
    `Z`, Enter, `A`, Enter to fit the view.
    Look at object snap in the status bar. If it is off, press F3.
    Look at ortho as well. If it is off, press F8. Step 8's horizontal copy and step 9's horizontal tangents depend on it.
    The six you turned on in Lesson 2 are endpoint, midpoint, center, quadrant, intersection and tangent.
    Today you use endpoint, center and quadrant.

### Step 2 — The bore Ø25

    Look at the layer list at the top of the screen. Check that it says visible line.
    If not, click it and change it to visible line.
    You can do it from the command line too. Type `CLAYER` and press Enter. Type `Visible line` and press Enter.

    Type `C` and press Enter. That is the circle command.
    It asks for the centre point. You do not type coordinates here.
    Rest the cursor on the rim of the boss circle Ø56, and click when the center marker appears. The bore shares the boss's centre.
    It asks for the radius. Do not put a number straight in here. Type `D` and press Enter.
    Now it asks the diameter. Type `25` and press Enter.
    A small circle has appeared inside the boss circle. That is the bore.

### Step 3 — The pitch circle Ø44, by offset

    First change the layer. In the layer list choose the centerline.

    Type `O` and press Enter. That is offset.
    It asks the distance. Before that you fix one option.
    Type `L` and press Enter. That is the layer option.
    It asks whether to use the source or the current one. Type `C` and press Enter.
    That means putting it on the current layer, the centerline.
    Skip this and the copy follows the original onto the visible line layer.

    It asks the distance again. Type `6` and press Enter. That is 56 take away 44, divided by 2.
    It asks which object to offset. Click the line of the boss Ø56 circle.
    It asks which side to put it on. Click anywhere inside the circle.
    Press Enter to end the command.

    If the pitch circle reads as a continuous line, the linetype scale is out.
    Click that circle and press Ctrl+1 to open the Properties window.
    In the linetype scale box type `0.5` and press Enter.
    The dash spacing opens out and it reads as a chain line.

### Step 4 — The 45 degree helper line

    Type `DSETTINGS` and press Enter.
    Open the polar tracking tab of the drafting settings.
    Select polar tracking on and set the increment angle to 45 degrees.
    Leave polar angle measurement on absolute. Press OK.
    F10 should be on and F8 ortho should be off.
    The current layer is the centerline.
    Type `L` and press Enter.
    For the first point, click the center snap of the boss circle.
    Move the cursor up and to the right and watch for the 45 degree tracking line.
    When the 45 degree guide shows, type `22` and press Enter.
    Press Enter once more to end the line command.
    The end lands on the pitch circle. That is the first tap centre.

### Step 5 — The first tapped hole

    In the layer list go back to the visible line.

    Type `C` and press Enter.
    It asks for the centre point. You do not type coordinates here.
    Take the mouse to the outer end of the helper line you just drew.
    Click when the square endpoint marker appears.
    It asks for the radius. Type `D` and press Enter, then `5` and press Enter.

    The 5 in M5 is the nominal diameter of the thread.
    On a real drawing a tapped hole is drawn as two circles: the root diameter and the outer diameter.
    In this exercise you draw it as one circle. The representation rules are covered separately later.

### Step 6 — Four of them, by polar array

    Type `ARRAYPOLAR` and press Enter.
    Click only the first tap circle, the one 5 across, and press Enter.
    For the array centre, click the center snap of the boss circle.
    When the preview appears, `I`, Enter, number of items `4`, Enter.
    Among the option names on the command line, click Fill angle. Type `360` and press Enter.
    90 is the gap between neighbouring holes; the value you put in here is one full turn, 360.
    On the command line, associative option `AS`, Enter, `N`, Enter.
    That makes the four circles independent objects.
    `X`, Enter to end the array command. Check that items is 4, fill angle 360 degrees, and the angle between neighbours 90 degrees.
    Check that there is one circle in each of the four quadrants around the boss centre.
    They start at 45 degrees, then 135, 225 and 315.
    If all four circles are bunched to one side, check the fill angle again.

### Step 7 — Erase the helper line

    Type `E` and press Enter. That is erase.
    Click the 45 degree helper line and press Enter.
    A helper line that has done its job gets erased there and then.
    Leave it and later you cannot tell them apart. You lose track of what is shape and what is helper.
    Trim or fillet then bites on the wrong line.

### Step 8 — The two slot end circles

    Press `Esc` to end the command and clear the selection.
    Change the layer to `Dimension line`.
    Before you fix the slot centres, you make four construction lines.
    `XL`, Enter, `H`, Enter.
    Click the lower left endpoint of the base with the endpoint snap.
    Press Enter once to finish.
    `XL`, Enter, `V`, Enter.
    Click the same endpoint and press Enter to finish.
    `O`, Enter, distance `8`, Enter.
    Click the horizontal construction line, click above it, then press Enter to finish.
    `O`, Enter, distance `29`, Enter.
    Click the vertical construction line, click to its right, then press Enter to finish.
    You do not offset an edge of the base polyline.

    Put the layer back to `Visible line`.
    Type `C` and press Enter.
    Click the intersection of the two inner construction lines. It is 8 above the bottom edge and 29 right of the left edge.
    Radius `5`, Enter. The circle command ends.
    `COPYMODE`, Enter, `1`, Enter. That copies once only.
    If the ortho indicator is off, press F8 to turn it on.
    `CO`, Enter, click the circle you just drew and press Enter.
    For the copy base point, click the center snap of that circle.
    Put the cursor to the right and type `12`, Enter.
    Single copy mode, so the command ends here.
    Do not press Enter again. The centre distance of the two end circles is 12.

    `QSELECT`, Enter, to open quick select.
    Apply to the entire drawing, object type construction line.
    Operator select all, how to apply include in new selection set.
    Press OK. Check that only the four construction lines are selected and erase them with `Delete`.
    The current layer is the visible line. Two circles are left.

### Step 9 — The two tangent lines

    The two circles have the same radius. Their centres are at the same height.
    So the tangent lines are horizontal.
    The centre height is 8 and the radius is 5.
    The upper tangent sits at 13 and the lower one at 3.

    Type `L` and press Enter. Rest the cursor on the top of the left end circle. Click when the diamond marker appears. Check for the same marker on the top of the right end circle and click. Enter. That is the upper tangent.
    `L`, Enter. This time watch for the diamond marker at the bottom of the two end circles and click them in turn. Enter. That is the lower tangent.
    The diamond is the quadrant marker. You never work out 13 and 3 and type them; the tangent point is caught exactly.

    Both ends of each line have to touch their circle exactly. Zoom in and check.
    If one floats clear or cuts in, the trim in the next step will not take.

### Step 10 — Trim the inner half-circles

    `TRIMEXTENDMODE`, Enter, `0`, Enter.
    That puts AutoCAD 2024's trim into the standard mode.
    You pick the boundary first, then the stretch to remove.
    Type `TR` and press Enter.
    Click only the two straight lines you just drew and press Enter.
    Click the right half of the left circle.
    Click the left half of the right circle.
    Press Enter once to end the trim.
    Two half-circles and two straight lines left is correct.
    If nothing trims, end with `Esc`.
    Check step 9's top and bottom quadrant snaps again.

### Step 11 — The right slot by mirroring

    Type `MI` and press Enter. That is mirror.
    It asks for objects. Pick all four pieces that make the slot.
    Two half-circles and two straight lines.
    You can click them one by one, but taking them in one box is quicker.
    Which way you drag the box is itself the rule.
    Drag left to right and it takes only what falls entirely inside the box. That is a window.
    Drag right to left and it takes anything the box touches. That is a crossing.
    You want the four slot pieces only, so drag left to right.
    Wrap the slot generously but leave the base outline outside the box. A line the box only touches is not taken.
    Pick them and press Enter.

    It asks for the first point of the mirror line. Take the cursor to the lower end of the vertical centerline.
    Click when the square endpoint marker appears.
    It asks for the second point. Watch for the endpoint marker at the upper end of that same centerline and click.
    The line you drew in Lesson 3 becomes the mirror axis as it is. Place it by coordinates and it can sit minutely off the centerline.
    It asks whether to erase the original. Type `N` and press Enter.
    Erase it and the left slot disappears.

    The right slot's centre has appeared at 85.
    25 to the left of 60 is 35. 25 to the right is 85.

### Step 12 — Trim the top face between the web lines

    There is something to do before you fillet.
    The top face of the base runs in one line from 5,16 to 115,16.
    It is one of the six edges you drew in one go as a polyline in Lesson 3.
    The web climbs over it.

    The base and the web are the same plate. Both are 12 thick.
    A face that runs continuously has no edge in it.
    And yet there is a line drawn there. It has to go.

    Type `TR` and press Enter.
    It asks for the cutting edges. Click the two web lines and press Enter.
    You do not take every object as a boundary here.
    Mix the line you are cutting into the boundary set and there is no telling where it breaks.

    Click the middle of the base's top face. It is the stretch caught between the two web lines.
    The stretch that ran between the web lines disappears. Press Enter to finish.

    The top face is now in two pieces.
    The left runs from 5 to 20, the right from 100 to 115.
    20 and 100 are the theoretical corners we spoke of in Lesson 3.
    What was a closed polyline has become a single open polyline.
    Its two ends are exactly where the fillets go.

### Step 13 — The right fillet R10

    `TRIMMODE`, Enter, `1`, Enter, so the lines you pick are cut at the ends of the arc.

    Type `F` and press Enter. That is the fillet command.
    Look at the current radius on the command line. Do not lean on the previous value; set 10.
    You must not pick the lines as things stand.
    Type `R` and press Enter. Type `10` and press Enter.

    Now pick the lines. The first object is the right-hand piece of the top face you just left.
    Click the horizontal line at height 16 that remains from 100 to 115.
    Click on the side you want to keep. This is the right fillet, so to the right of the corner.
    The second object is the right web line.
    Again click the side you want to keep, above the corner.

    The arc is fitted. What ran past the corner has been trimmed.

### Step 14 — The left fillet R10

    Type `F` and press Enter. The radius is remembered as 10.
    `R`, Enter, `10`, Enter to set the same radius.
    Check that the command line shows a radius of 10.
    Click the base's top face to the left of the corner.
    Click the left web line above the corner.

    The two, left and right, have gone in at the same radius.
    The 2-R10 on the drawing means these two.

    Now the outline runs as a single line.
    From the top face of the base it rides the round and climbs the web line.
    The web line ends where it is tangent to the boss circle.

    You do not touch the boss circle. Leave it as a whole circle.
    The boss stands 8 forward.
    Only there is the thickness 20. The web and the base are 12.
    Inside the circle is 20, outside it 12.
    Where the thickness changes there is an edge.
    Seen from the front, the whole way round is visible.

    The upper half is the outer profile. Beyond it there is nothing.
    The lower half is an edge inside the shape. It is the step sitting on top of the web.
    They are in different places, but both are lines you can see, so both are continuous.

    Erase the lower half and it catches up with you in Lesson 5.
    When you pull projection lines you have to catch the quadrants at 32 and 88, and 34.
    32 and 88 are the left and right quadrants; 34 is the bottom quadrant.

### Step 15 — Check the numbers

    Looking right and being right are different things. You confirm it with numbers.

    Type `DI` and press Enter. That is distance.
    Click the two end circle centres of the left slot in turn. Click when the center snap catches.
    The command line should say 12.

    `DI`, Enter. This time it is between the two slots.
    Click the left end circle centre of the left slot and the left end circle centre of the right slot.
    It should say 50. That is 29 to 79.

    Do not try to click 35 and 85, the middles of the slots.
    There is no object to click there.
    A slot is made only of two arcs and two straight lines.
    The only places a center snap catches are the arc centres: 29 and 41, 79 and 91.
    Measure like for like and you get the spacing of the two slots.
    Measure the right end circles against each other and it is 50 as well. That is 41 to 91.

    Type `LI` and press Enter. That lists properties. Click the pitch circle and press Enter.
    See whether the layer is centerline. See whether the radius is 22.
    A radius of 22 is a diameter of 44.
    Close the text window with F2.

    Check the bore the same way. It should be radius 12.5. That is, 25 across.

    Last you put centre marks on the holes and the fillets. Change the current layer to the centerline.
    `DIMSCALE`, Enter, `1`, Enter to confirm the display scale.
    `DIMCEN`, Enter, `3`, Enter. That makes a cross mark 3 from the centre to each end.
    This 3 is the size of the mark, not a part dimension.
    `DIMCENTER`, Enter. Click the rim of one tap circle and press Esc to tidy the command up.
    Run the same command again for each of the other three tap circles, the two fillet arcs, and the four end arcs of the two slots.
    You start DIMCENTER afresh for each circle or arc and select only that rim.
    Check that cross marks have appeared at ten centre points.
    These marks are non-associative objects, so if you move or resize the shape you have to check them with it.
    Clear the selection with Esc and put the current layer back to the visible line.

### Step 16 — Save under a new name

    Type `SAVEAS` and press Enter.
    Change the file name to this lesson's name. (on screen · `EDU-IB-02_L04_FEATURES`) Leave the file type as dwg.
    Press Save.

    You do not overwrite the previous file; you leave it under a new name.
    That is so you can go back one lesson when something has gone wrong.
    Next time you open this file and start there.

## Line 6 — Four mistakes that come up often (Frame 6)

**Time:** 21:48–23:37

    Before we finish, here are the mistakes that come up often. There are four. All four look perfectly fine on screen. They only show up when you measure.

    (1 card — radius and diameter) First, putting a diameter where the radius goes. The circle command asks for a radius by default. But the drawing gives Ø25, a diameter. Put 25 in as it stands and you get a diameter of 50. Exactly twice. And on screen it just looks like a slightly bigger circle. It is hard to notice. Make yourself one habit. If it carries Ø, press `D` first. If it carries R, put it straight in.

    (2 card — array angle) Second, giving the polar array an angle of 45. The drawing says 45 degrees, so that is the value you reach for. But 45 degrees is where the first hole sits. It is not the gap between holes. The gap is 360 divided by the count of 4, which is 90 degrees. Put 45 in and the four holes crowd into half a turn. They bunch to one side. Then the cover tilts that way. The whole reason for spacing four evenly is gone.

    (3 card — fillet radius) Third, running fillet without setting the radius. The default radius is 0. Pick two lines while it is 0 and no arc goes in. The two lines simply meet at a square corner. The command finishes normally. There is no error either. So it is easy to walk past. When you start the command, the first line on the command line shows the current radius. Get into the habit of reading that line before you pick.

    (4 card — the lines inside a slot) Fourth, not trimming the lines inside a slot. You draw the two end circles and the two tangent lines. Then you forget the trim. That leaves two curves inside the pill. They are lines the real shape does not have. Lines like that catch you later. When you hatch a section, the boundary splits. When you dimension, the snap lands on the wrong point. Zoom in, check that no line is left inside, and move on.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 23:37–24:31

    (1 left) That is the extent of the front view the LG Innotek internal exam asks for. The commands you used today are not for the exam alone. You use them just as they are when PM takes a machine down and you draw a jig, and when you check a spare part drawing. Misread one dimension and have it machined again, and that is rework loss.

    (2 right) Next time you make the whole drawing out of that one front view. You project it in third angle. The top view goes above, the right side view to the right. There are two things at the heart of it. Which point of the front view becomes which point of the top view. And how you pull construction lines across and use them. The bore and the tapped holes you drew today are hidden when seen from the side. So they come out as hidden lines. That is where you first use the hidden line layer you made in Lesson 2. The boss stands 8 forward. The thickness there is 20. That value too becomes a drawn thing for the first time, in the top view. When you finish you save it as the next state.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 24:31–27:14

    Here are today's commands in one place. Rather than the names, remember **when you use them**.
    That is the part that stays after the exam.

    (1) `OPEN`. Opens a file. You use it to carry on every lesson from the previous state.

    (2) `Z`. ZOOM. Changes the zoom. You use it when you need to see where a snap landed.

    (3) `CLAYER`. Changes the current layer. You use it to change layer from the command line.

    (4) `C`. CIRCLE. Draws a circle. You use it for holes, shafts and pitch circles.

    (5) `O`. OFFSET. Makes the same shape a set distance away. You use it for concentric circles and parallel lines without picking the centre again.

    (6) `DSETTINGS`. Opens the drafting settings. You use it to set the increment angle for polar tracking.

    (7) `L`. LINE. Draws a line. You use it for pieces you need to handle singly.

    (8) `ARRAYPOLAR`. Arrays around a centre. You use it for things spaced evenly by angle, like bolt holes.

    (9) `E`. ERASE. Erases. You use it to clear away helper lines.

    (10) `XL`. XLINE. Draws a construction line that runs on forever. You use it for projection lines.

    (11) `COPYMODE`. Decides whether the copy command repeats. You use it to end the command after one copy.

    (12) `CO`. COPY. Puts the same thing somewhere else. You use it for repeated parts and identical holes.

    (13) `QSELECT`. Picks every object matching a condition at once. You use it to select only the construction lines and erase them.

    (14) `TRIMEXTENDMODE`. Sets how trim and extend choose. You use it to pick the cutting edge first.

    (15) `TR`. TRIM. Cuts back to a boundary. You use it on overlapping lines and stubs that stick out.

    (16) `MI`. MIRROR. Copies symmetrically. You use it for shapes symmetrical left and right.

    (17) `TRIMMODE`. Decides whether the original lines are tidied after a chamfer or fillet. You use it to cut the original line back to the end of an arc or a slanted edge.

    (18) `F`. FILLET. Puts a round between two lines. You use it on an inside corner where stress piles up.

    (19) `DI`. DIST. Measures the distance between two points. You use it before you dimension.

    (20) `LI`. LIST. Shows an object's information. You use it to check that what you drew really is that value.

    (21) `DIMSCALE`. Sets the overall scale of dimensions and centre marks. You use it to keep the display size at model one to one.

    (22) `DIMCEN`. Sets the size and style of the centre mark. You use it to standardise the mark size at 3.

    (23) `DIMCENTER`. Makes the centre mark for a circle or an arc. You use it to mark the centres of taps, fillets and slot end arcs.

    (24) `SAVEAS`. Saves under a new name. You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 27:14–27:26

    (1) That is today's portion. Well done.

    (2) Next is Lesson 5, third angle projection. See you then.
