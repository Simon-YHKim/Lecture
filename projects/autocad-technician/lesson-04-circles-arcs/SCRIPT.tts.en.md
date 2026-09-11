<!-- 생성물이다. 손으로 고치지 말고 원본 SCRIPT.en.md 를 고친 뒤 다시 뽑아라.
     python scripts/part/tts_script.py lesson-04-circles-arcs
     태그: asking · calm · cautionary · emphatic · light · measured · pointing · warm -->
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

    [calm] Lesson 4, circles, arcs and offset. [calm] You draw the inside of the idler pulley bracket that goes on a car engine.

## Line 2 — Filling in inside the outline (Frame 2)

**Time:** 0:10–1:44

    [calm] Last time you drew the outer profile of the idler pulley bracket. [calm] It is a part that goes on a car engine. [calm] You finished the base, the web and the boss circle. [calm] Today you put four shapes inside it. [calm] Every one of them starts from a circle. [calm] You draw a circle, push it, fit one in, and rotate a copy round.

    (1 card — bore Ø25) [pointing] The first is the bore in the middle. [measured] It goes right through, 25 across, and its centre is where the boss centre is: 60 from the left end, 62 from the bottom. [calm] This hole is the reference of the part, and the shaft sits in here and turns. [calm] If this hole is off, the part is unusable however right the rest of it is. [calm] That is why you draw it first today.

    (2 card — tapped 4-M5 in a polar array) [pointing] The second is the four screw seats. [calm] They sit around the bore. [measured] You cut M5 threads 10 deep. [calm] The four centres lie on a circle 44 across. [calm] The first hole is at 45 degrees. [calm] The rest step round every 90. [cautionary] You do not draw the four one at a time. [calm] You draw one and rotate it round with a polar array. [calm] That way the angle is set by arithmetic, not by hand.

    (3 card — slots 2-R5) [pointing] The third is the two long holes at the bottom. [measured] They are 10 wide and each end is a half-circle of radius 5. [calm] One circle command will not give you that. [calm] You draw the two end circles, join them with tangent lines, and trim the inside away to get the pill shape. [calm] That is where you use the trim command today.

    (4 card — fillets 2-R10) [pointing] The fourth is the inside corner. [calm] It is where the web turns into the base. [calm] You round it at radius 10. [cautionary] You do not draw a separate circle here. [emphatic] You only pick two lines. [calm] The command fits the arc between them itself. [calm] It trims what is left over as well. [emphatic] This is where the load piles up most. [calm] That is why the R is as large as 10. [calm] It is the story from Lesson 2.

## Line 3 — The four commands you use today (Frame 3)

**Time:** 1:44–4:11

    [calm] Before you draw, here are the four commands you use today. [calm] Know what each one is for and the order of work follows easily.

    (1 card — CIRCLE) [light] The circle command. [measured] Its shortcut is `C`. [calm] There are five ways to draw a circle, and today you use the first two. [calm] First, pick the centre and give the radius. [light] That is the default. [measured] Second, pick the centre and, where it asks for the radius, press `D` and give the diameter instead. [calm] The other three are two-point, three-point, and tangent-tangent-radius; knowing their names is enough. [emphatic] Which one you use follows the drawing's notation exactly. [calm] A value written with Ø is a diameter, so that is the second method. [calm] A value written with R is a radius, so that is the first. [calm] Follow the notation and you make fewer mistakes.

    (2 card — OFFSET) [light] Offset. [measured] Its shortcut is `O`. [calm] It copies the object you pick, parallel to itself. [calm] You give the distance yourself. [calm] Offset a straight line and you get a parallel line. [calm] Offset a circle and you get a concentric circle. [calm] You make the pitch circle with this today. [cautionary] You do not pick the centre again. [calm] So the centre cannot go out of line. [calm] It is a command you reach for often on the floor. [calm] You use it when you look at an equipment layout. [calm] You set wall thicknesses; you set walkway clearances. [calm] You push out from one datum line. [light] There are three options. [calm] Through takes a point to pass through instead of a distance. [calm] Erase moves it, deleting the original. [calm] Layer decides where the copy goes. [calm] You choose between the source layer and the current layer. [light] The default is source. [calm] Leave it and the copy follows the original's layer.

    (3 card — FILLET) [light] Fillet. [measured] Its shortcut is `F`. [calm] Pick two lines and it fits an arc between them. [calm] The radius is a value you set beforehand. [calm] It trims what runs past the corner. [light] The order matters. [calm] Set the radius first, then pick the lines. [calm] That is because the default radius is 0. [calm] Run it without setting it and no arc appears — you just get a square corner. [measured] You put the radius in with the `R` option. [calm] There is a polyline option too. [calm] It rounds every corner of a polyline at once.

    (4 card — ARRAYPOLAR) [light] The polar array. [calm] This one has no short form of its own. [calm] You type the whole name. [light] You pick the object. [calm] You pick a centre point. [calm] You say how many, at what angular spacing. [calm] It copies them just so. [calm] There are four options: number of items, angle between them, angle to fill, and whether it is associative. [calm] The angle between is the gap between neighbouring items. [calm] The angle to fill is the angle the whole thing turns through. [calm] You use it with associative off. [calm] Leave it on and the four are bound into one body. [calm] You cannot pick one of them on its own. [calm] Sooner or later you will need to edit one individually.

## Line 4 — On the drawing (Frame 4)

**Time:** 4:11–7:56

    [light] You know the commands. [calm] We will point at the drawing on the right and see what goes where. [calm] There are six, and the order of pointing is the order of work.

    (1 row — bore Ø25 H7) [pointing] The bore in the middle. [measured] Its centre is 60, 62. [calm] The same centre as the boss. [calm] There is one thing to watch here. [light] The drawing says Ø25. [light] That is a diameter. [calm] But what the circle command asks for by default is the radius. [measured] Put 25 in as it stands and you get a hole 50 across. [emphatic] Exactly twice. [measured] So you press `D` to switch to diameter entry. [calm] Then you put 25 in. [calm] H7 is a fit grade. [calm] It has no effect on the shape. [calm] You draw it at 25. [calm] The grade goes on as text when you dimension. [calm] The reason that grade matters is out on the floor. [calm] When a machine stops you have to find a spare in a hurry. [calm] You look at the assembly drawing and find that part drawing. [calm] You hand that drawing to the machine shop. [calm] Leave the grade line off at that moment and the shaft does not go in.

    (2 row — boss Ø56) [pointing] You already drew the boss circle last time. [calm] You drew the two web lines tangent to this circle. [calm] Without this circle the outline does not hold together. [cautionary] Today you do not draw this circle again. [calm] You use it as a reference instead. [calm] You push the next row's pitch circle out of it.

    (3 row — pitch circle PCD Ø44) [pointing] This is the circle the four tapped-hole centres sit on. [calm] It is not a hole itself. [calm] It is a helper circle that fixes where the holes go. [calm] So it is not a visible line. [calm] You draw it on the centerline layer. [calm] On screen it should come out as a red chain line. [calm] The way to make it is offset. [calm] You push the boss Ø56 inward. [measured] The distance is 56 take away 44, divided by 2, which is 6. [calm] Half the difference in diameter is the difference in radius. [calm] That is because offset pushes the radius. [cautionary] Do it this way and you never retype the centre coordinates. [calm] The boss and the pitch circle cannot end up on different centres.

    (4 row — tapped 4-M5) [light] The four screw seats. [measured] The first hole is at 45 degrees and the rest step round every 90. [calm] The order of drawing is this. [measured] From the boss centre, draw one helper line 22 long in the 45 degree direction. [measured] 22 is half of the pitch circle diameter of 44, that is, the radius. [emphatic] Then the end of that helper line lands exactly on the pitch circle at 45 degrees. [calm] You draw one hole there, make four with a polar array, and erase the helper line. [cautionary] You do not set the angle by eye. [emphatic] You fix the direction with polar tracking and type only the distance.

    (5 row — slots 2-R5) [pointing] The long holes at the bottom. [measured] The left slot's centre is at 35, 8. [measured] Halve the 12 between the two end circle centres and you get 6. [measured] Step 6 either side of the centre at 35 and you get 29 and 41. [measured] 29 is written on the drawing as it stands: 29 from the left edge to the first end circle. [light] The two values agree. [calm] The order of drawing is this. [calm] You draw the two end circles at radius 5. [calm] You draw tangent lines above and below. [calm] You trim away the half-circles that point inward. [calm] Once trimmed, a circle becomes an arc. [calm] That is why the word arc is in today's title. [cautionary] You do not draw the right slot again. [light] You mirror it. [measured] The two slot centres are 35 and 85. [calm] Halfway between them is 60. [calm] 60 is the horizontal position of the boss centre. [calm] That is what it means for the part to be symmetrical about this line. [calm] Slots come up often on the floor too — when you propose a jig to make a job easier. [calm] Put the bolt seats in slots and you can shift the position a little at a time.

    (6 row — fillets 2-R10) [pointing] Last is the inside corner where the web meets the base. [calm] Between the web tangent and the top face of the base. [calm] The top face of the base is a horizontal plane at height 16. [calm] You round it here at radius 10. [calm] The drawing gives a centre height of 26. [light] That is for checking. [calm] The top face of the base is at 16. [calm] The fillet is tangent to that face. [measured] So the centre is 16 plus 10, which is 26. [measured] There is one reference dimension in brackets, (95.7). [cautionary] It is a value computed from the others, so you do not type it. [calm] Once the fillet command has bitten on the two lines, the centre lands there by itself.

## Line 5 — Circles, arcs and offset · DEMO-01 screen recording (Frame 5)

**Time:** 7:56–21:48

> This section is a screen recording. Work through the 16 steps below in order and without skipping, speaking as you go.
> A command written in capitals is the command; what is inside backticks is what you actually type.
> You do not place anything by eye. If something is already drawn, catch it with a snap, fix the direction with ortho or polar tracking, and type only the distance.
> A snap is not eyeballing — it takes a point the drawing already holds, so it is more accurate than a typed coordinate. Let a circle centre be out by one millimetre and everything after it is out.

### Step 1 — Open the previous file

    [cautionary] You do not make a new one. [measured] Type `OPEN` and press Enter.
    [calm] Choose the file you saved last lesson. [measured] (on screen · `EDU-IB-02_L03_PROFILE.dwg`)
    [light] Press Open.
    [calm] The base and its chamfers should be on screen. [calm] The two web lines and the boss circle should be there too.
    [calm] That is today's starting state.
    [measured] `Z`, Enter, `A`, Enter to fit the view.
    [calm] Look at object snap in the status bar. [calm] If it is off, press F3.
    [calm] Look at ortho as well. [calm] If it is off, press F8. [measured] Step 8's horizontal copy and step 9's horizontal tangents depend on it.
    [calm] The six you turned on in Lesson 2 are endpoint, midpoint, center, quadrant, intersection and tangent.
    [calm] Today you use endpoint, center and quadrant.

### Step 2 — The bore Ø25

    [calm] Look at the layer list at the top of the screen. [calm] Check that it says visible line.
    [calm] If not, click it and change it to visible line.
    [calm] You can do it from the command line too. [measured] Type `CLAYER` and press Enter. [measured] Type `Visible line` and press Enter.

    [measured] Type `C` and press Enter. [calm] That is the circle command.
    [calm] It asks for the centre point. [cautionary] You do not type coordinates here.
    [measured] Rest the cursor on the rim of the boss circle Ø56, and click when the center marker appears. [calm] The bore shares the boss's centre.
    [calm] It asks for the radius. [cautionary] Do not put a number straight in here. [measured] Type `D` and press Enter.
    [calm] Now it asks the diameter. [measured] Type `25` and press Enter.
    [calm] A small circle has appeared inside the boss circle. [light] That is the bore.

### Step 3 — The pitch circle Ø44, by offset

    [light] First change the layer. [calm] In the layer list choose the centerline.

    [measured] Type `O` and press Enter. [light] That is offset.
    [light] It asks the distance. [calm] Before that you fix one option.
    [measured] Type `L` and press Enter. [calm] That is the layer option.
    [calm] It asks whether to use the source or the current one. [measured] Type `C` and press Enter.
    [calm] That means putting it on the current layer, the centerline.
    [calm] Skip this and the copy follows the original onto the visible line layer.

    [calm] It asks the distance again. [measured] Type `6` and press Enter. [measured] That is 56 take away 44, divided by 2.
    [calm] It asks which object to offset. [measured] Click the line of the boss Ø56 circle.
    [calm] It asks which side to put it on. [calm] Click anywhere inside the circle.
    [calm] Press Enter to end the command.

    [calm] If the pitch circle reads as a continuous line, the linetype scale is out.
    [calm] Click that circle and press Ctrl+1 to open the Properties window.
    [measured] In the linetype scale box type `0.5` and press Enter.
    [calm] The dash spacing opens out and it reads as a chain line.

### Step 4 — The 45 degree helper line

    [measured] Type `DSETTINGS` and press Enter.
    [calm] Open the polar tracking tab of the drafting settings.
    [measured] Select polar tracking on and set the increment angle to 45 degrees.
    [calm] Leave polar angle measurement on absolute. [light] Press OK.
    [measured] F10 should be on and F8 ortho should be off.
    [calm] The current layer is the centerline.
    [measured] Type `L` and press Enter.
    [calm] For the first point, click the center snap of the boss circle.
    [measured] Move the cursor up and to the right and watch for the 45 degree tracking line.
    [measured] When the 45 degree guide shows, type `22` and press Enter.
    [calm] Press Enter once more to end the line command.
    [calm] The end lands on the pitch circle. [calm] That is the first tap centre.

### Step 5 — The first tapped hole

    [calm] In the layer list go back to the visible line.

    [measured] Type `C` and press Enter.
    [calm] It asks for the centre point. [cautionary] You do not type coordinates here.
    [calm] Take the mouse to the outer end of the helper line you just drew.
    [calm] Click when the square endpoint marker appears.
    [calm] It asks for the radius. [measured] Type `D` and press Enter, then `5` and press Enter.

    [measured] The 5 in M5 is the nominal diameter of the thread.
    [calm] On a real drawing a tapped hole is drawn as two circles: the root diameter and the outer diameter.
    [calm] In this exercise you draw it as one circle. [calm] The representation rules are covered separately later.

### Step 6 — Four of them, by polar array

    [measured] Type `ARRAYPOLAR` and press Enter.
    [emphatic] Click only the first tap circle, the one 5 across, and press Enter.
    [calm] For the array centre, click the center snap of the boss circle.
    [measured] When the preview appears, `I`, Enter, number of items `4`, Enter.
    [calm] Among the option names on the command line, click Fill angle. [measured] Type `360` and press Enter.
    [measured] 90 is the gap between neighbouring holes; the value you put in here is one full turn, 360.
    [measured] On the command line, associative option `AS`, Enter, `N`, Enter.
    [calm] That makes the four circles independent objects.
    [measured] `X`, Enter to end the array command. [measured] Check that items is 4, fill angle 360 degrees, and the angle between neighbours 90 degrees.
    [calm] Check that there is one circle in each of the four quadrants around the boss centre.
    [measured] They start at 45 degrees, then 135, 225 and 315.
    [calm] If all four circles are bunched to one side, check the fill angle again.

### Step 7 — Erase the helper line

    [measured] Type `E` and press Enter. [light] That is erase.
    [measured] Click the 45 degree helper line and press Enter.
    [calm] A helper line that has done its job gets erased there and then.
    [calm] Leave it and later you cannot tell them apart. [cautionary] You lose track of what is shape and what is helper.
    [cautionary] Trim or fillet then bites on the wrong line.

### Step 8 — The two slot end circles

    [measured] Press `Esc` to end the command and clear the selection.
    [measured] Change the layer to `Dimension line`.
    [calm] Before you fix the slot centres, you make four construction lines.
    [measured] `XL`, Enter, `H`, Enter.
    [calm] Click the lower left endpoint of the base with the endpoint snap.
    [calm] Press Enter once to finish.
    [measured] `XL`, Enter, `V`, Enter.
    [calm] Click the same endpoint and press Enter to finish.
    [measured] `O`, Enter, distance `8`, Enter.
    [calm] Click the horizontal construction line, click above it, then press Enter to finish.
    [measured] `O`, Enter, distance `29`, Enter.
    [calm] Click the vertical construction line, click to its right, then press Enter to finish.
    [cautionary] You do not offset an edge of the base polyline.

    [measured] Put the layer back to `Visible line`.
    [measured] Type `C` and press Enter.
    [calm] Click the intersection of the two inner construction lines. [measured] It is 8 above the bottom edge and 29 right of the left edge.
    [measured] Radius `5`, Enter. [light] The circle command ends.
    [measured] `COPYMODE`, Enter, `1`, Enter. [emphatic] That copies once only.
    [calm] If the ortho indicator is off, press F8 to turn it on.
    [measured] `CO`, Enter, click the circle you just drew and press Enter.
    [calm] For the copy base point, click the center snap of that circle.
    [measured] Put the cursor to the right and type `12`, Enter.
    [calm] Single copy mode, so the command ends here.
    [cautionary] Do not press Enter again. [measured] The centre distance of the two end circles is 12.

    [measured] `QSELECT`, Enter, to open quick select.
    [calm] Apply to the entire drawing, object type construction line.
    [calm] Operator select all, how to apply include in new selection set.
    [light] Press OK. [measured] Check that only the four construction lines are selected and erase them with `Delete`.
    [calm] The current layer is the visible line. [light] Two circles are left.

### Step 9 — The two tangent lines

    [calm] The two circles have the same radius. [calm] Their centres are at the same height.
    [calm] So the tangent lines are horizontal.
    [measured] The centre height is 8 and the radius is 5.
    [measured] The upper tangent sits at 13 and the lower one at 3.

    [measured] Type `L` and press Enter. [calm] Rest the cursor on the top of the left end circle. [calm] Click when the diamond marker appears. [calm] Check for the same marker on the top of the right end circle and click. [light] Enter. [calm] That is the upper tangent.
    [measured] `L`, Enter. [calm] This time watch for the diamond marker at the bottom of the two end circles and click them in turn. [light] Enter. [calm] That is the lower tangent.
    [calm] The diamond is the quadrant marker. [cautionary] You never work out 13 and 3 and type them; the tangent point is caught exactly.

    [emphatic] Both ends of each line have to touch their circle exactly. [light] Zoom in and check.
    [calm] If one floats clear or cuts in, the trim in the next step will not take.

### Step 10 — Trim the inner half-circles

    [measured] `TRIMEXTENDMODE`, Enter, `0`, Enter.
    [measured] That puts AutoCAD 2024's trim into the standard mode.
    [calm] You pick the boundary first, then the stretch to remove.
    [measured] Type `TR` and press Enter.
    [emphatic] Click only the two straight lines you just drew and press Enter.
    [calm] Click the right half of the left circle.
    [calm] Click the left half of the right circle.
    [calm] Press Enter once to end the trim.
    [calm] Two half-circles and two straight lines left is correct.
    [measured] If nothing trims, end with `Esc`.
    [calm] Check step 9's top and bottom quadrant snaps again.

### Step 11 — The right slot by mirroring

    [measured] Type `MI` and press Enter. [light] That is mirror.
    [light] It asks for objects. [calm] Pick all four pieces that make the slot.
    [calm] Two half-circles and two straight lines.
    [calm] You can click them one by one, but taking them in one box is quicker.
    [calm] Which way you drag the box is itself the rule.
    [emphatic] Drag left to right and it takes only what falls entirely inside the box. [light] That is a window.
    [calm] Drag right to left and it takes anything the box touches. [light] That is a crossing.
    [emphatic] You want the four slot pieces only, so drag left to right.
    [calm] Wrap the slot generously but leave the base outline outside the box. [emphatic] A line the box only touches is not taken.
    [calm] Pick them and press Enter.

    [calm] It asks for the first point of the mirror line. [calm] Take the cursor to the lower end of the vertical centerline.
    [calm] Click when the square endpoint marker appears.
    [calm] It asks for the second point. [calm] Watch for the endpoint marker at the upper end of that same centerline and click.
    [calm] The line you drew in Lesson 3 becomes the mirror axis as it is. [calm] Place it by coordinates and it can sit minutely off the centerline.
    [calm] It asks whether to erase the original. [measured] Type `N` and press Enter.
    [calm] Erase it and the left slot disappears.

    [measured] The right slot's centre has appeared at 85.
    [measured] 25 to the left of 60 is 35. [measured] 25 to the right is 85.

### Step 12 — Trim the top face between the web lines

    [calm] There is something to do before you fillet.
    [measured] The top face of the base runs in one line from 5,16 to 115,16.
    [calm] It is one of the six edges you drew in one go as a polyline in Lesson 3.
    [calm] The web climbs over it.

    [calm] The base and the web are the same plate. [measured] Both are 12 thick.
    [calm] A face that runs continuously has no edge in it.
    [calm] And yet there is a line drawn there. [light] It has to go.

    [measured] Type `TR` and press Enter.
    [calm] It asks for the cutting edges. [calm] Click the two web lines and press Enter.
    [cautionary] You do not take every object as a boundary here.
    [cautionary] Mix the line you are cutting into the boundary set and there is no telling where it breaks.

    [calm] Click the middle of the base's top face. [calm] It is the stretch caught between the two web lines.
    [calm] The stretch that ran between the web lines disappears. [light] Press Enter to finish.

    [calm] The top face is now in two pieces.
    [measured] The left runs from 5 to 20, the right from 100 to 115.
    [measured] 20 and 100 are the theoretical corners we spoke of in Lesson 3.
    [calm] What was a closed polyline has become a single open polyline.
    [emphatic] Its two ends are exactly where the fillets go.

### Step 13 — The right fillet R10

    [measured] `TRIMMODE`, Enter, `1`, Enter, so the lines you pick are cut at the ends of the arc.

    [measured] Type `F` and press Enter. [calm] That is the fillet command.
    [calm] Look at the current radius on the command line. [cautionary] Do not lean on the previous value; set 10.
    [cautionary] You must not pick the lines as things stand.
    [measured] Type `R` and press Enter. [measured] Type `10` and press Enter.

    [light] Now pick the lines. [calm] The first object is the right-hand piece of the top face you just left.
    [measured] Click the horizontal line at height 16 that remains from 100 to 115.
    [calm] Click on the side you want to keep. [calm] This is the right fillet, so to the right of the corner.
    [calm] The second object is the right web line.
    [calm] Again click the side you want to keep, above the corner.

    [light] The arc is fitted. [calm] What ran past the corner has been trimmed.

### Step 14 — The left fillet R10

    [measured] Type `F` and press Enter. [measured] The radius is remembered as 10.
    [measured] `R`, Enter, `10`, Enter to set the same radius.
    [measured] Check that the command line shows a radius of 10.
    [calm] Click the base's top face to the left of the corner.
    [calm] Click the left web line above the corner.

    [calm] The two, left and right, have gone in at the same radius.
    [measured] The 2-R10 on the drawing means these two.

    [calm] Now the outline runs as a single line.
    [calm] From the top face of the base it rides the round and climbs the web line.
    [calm] The web line ends where it is tangent to the boss circle.

    [cautionary] You do not touch the boss circle. [calm] Leave it as a whole circle.
    [calm] The boss stands 8 forward.
    [measured] Only there is the thickness 20. [measured] The web and the base are 12.
    [measured] Inside the circle is 20, outside it 12.
    [calm] Where the thickness changes there is an edge.
    [calm] Seen from the front, the whole way round is visible.

    [calm] The upper half is the outer profile. [calm] Beyond it there is nothing.
    [calm] The lower half is an edge inside the shape. [calm] It is the step sitting on top of the web.
    [calm] They are in different places, but both are lines you can see, so both are continuous.

    [calm] Erase the lower half and it catches up with you in Lesson 5.
    [measured] When you pull projection lines you have to catch the quadrants at 32 and 88, and 34.
    [measured] 32 and 88 are the left and right quadrants; 34 is the bottom quadrant.

### Step 15 — Check the numbers

    [calm] Looking right and being right are different things. [calm] You confirm it with numbers.

    [measured] Type `DI` and press Enter. [light] That is distance.
    [calm] Click the two end circle centres of the left slot in turn. [calm] Click when the center snap catches.
    [measured] The command line should say 12.

    [measured] `DI`, Enter. [calm] This time it is between the two slots.
    [calm] Click the left end circle centre of the left slot and the left end circle centre of the right slot.
    [measured] It should say 50. [measured] That is 29 to 79.

    [cautionary] Do not try to click 35 and 85, the middles of the slots.
    [calm] There is no object to click there.
    [emphatic] A slot is made only of two arcs and two straight lines.
    [measured] The only places a center snap catches are the arc centres: 29 and 41, 79 and 91.
    [calm] Measure like for like and you get the spacing of the two slots.
    [measured] Measure the right end circles against each other and it is 50 as well. [measured] That is 41 to 91.

    [measured] Type `LI` and press Enter. [light] That lists properties. [calm] Click the pitch circle and press Enter.
    [calm] See whether the layer is centerline. [measured] See whether the radius is 22.
    [measured] A radius of 22 is a diameter of 44.
    [calm] Close the text window with F2.

    [calm] Check the bore the same way. [measured] It should be radius 12.5. [measured] That is, 25 across.

    [calm] Last you put centre marks on the holes and the fillets. [calm] Change the current layer to the centerline.
    [measured] `DIMSCALE`, Enter, `1`, Enter to confirm the display scale.
    [measured] `DIMCEN`, Enter, `3`, Enter. [calm] That makes a cross mark 3 from the centre to each end.
    [calm] This 3 is the size of the mark, not a part dimension.
    [measured] `DIMCENTER`, Enter. [calm] Click the rim of one tap circle and press Esc to tidy the command up.
    [calm] Run the same command again for each of the other three tap circles, the two fillet arcs, and the four end arcs of the two slots.
    [emphatic] You start DIMCENTER afresh for each circle or arc and select only that rim.
    [calm] Check that cross marks have appeared at ten centre points.
    [calm] These marks are non-associative objects, so if you move or resize the shape you have to check them with it.
    [calm] Clear the selection with Esc and put the current layer back to the visible line.

### Step 16 — Save under a new name

    [measured] Type `SAVEAS` and press Enter.
    [calm] Change the file name to this lesson's name. [measured] (on screen · `EDU-IB-02_L04_FEATURES`) Leave the file type as dwg.
    [light] Press Save.

    [cautionary] You do not overwrite the previous file; you leave it under a new name.
    [cautionary] That is so you can go back one lesson when something has gone wrong.
    [calm] Next time you open this file and start there.

## Line 6 — Four mistakes that come up often (Frame 6)

**Time:** 21:48–23:37

    [calm] Before we finish, here are the mistakes that come up often. [light] There are four. [calm] All four look perfectly fine on screen. [emphatic] They only show up when you measure.

    (1 card — radius and diameter) [pointing] First, putting a diameter where the radius goes. [calm] The circle command asks for a radius by default. [calm] But the drawing gives Ø25, a diameter. [measured] Put 25 in as it stands and you get a diameter of 50. [emphatic] Exactly twice. [calm] And on screen it just looks like a slightly bigger circle. [calm] It is hard to notice. [light] Make yourself one habit. [measured] If it carries Ø, press `D` first. [calm] If it carries R, put it straight in.

    (2 card — array angle) [pointing] Second, giving the polar array an angle of 45. [calm] The drawing says 45 degrees, so that is the value you reach for. [calm] But 45 degrees is where the first hole sits. [calm] It is not the gap between holes. [measured] The gap is 360 divided by the count of 4, which is 90 degrees. [calm] Put 45 in and the four holes crowd into half a turn. [calm] They bunch to one side. [calm] Then the cover tilts that way. [calm] The whole reason for spacing four evenly is gone.

    (3 card — fillet radius) [pointing] Third, running fillet without setting the radius. [calm] The default radius is 0. [calm] Pick two lines while it is 0 and no arc goes in. [calm] The two lines simply meet at a square corner. [light] The command finishes normally. [calm] There is no error either. [calm] So it is easy to walk past. [calm] When you start the command, the first line on the command line shows the current radius. [calm] Get into the habit of reading that line before you pick.

    (4 card — the lines inside a slot) [pointing] Fourth, not trimming the lines inside a slot. [calm] You draw the two end circles and the two tangent lines. [calm] Then you forget the trim. [calm] That leaves two curves inside the pill. [calm] They are lines the real shape does not have. [calm] Lines like that catch you later. [calm] When you hatch a section, the boundary splits. [cautionary] When you dimension, the snap lands on the wrong point. [calm] Zoom in, check that no line is left inside, and move on.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 23:37–24:31

    (1 left) [pointing] That is the extent of the front view the LG Innotek internal exam asks for. [calm] The commands you used today are not for the exam alone. [calm] You use them just as they are when PM takes a machine down and you draw a jig, and when you check a spare part drawing. [calm] Misread one dimension and have it machined again, and that is rework loss.

    (2 right) [pointing] Next time you make the whole drawing out of that one front view. [calm] You project it in third angle. [calm] The top view goes above, the right side view to the right. [calm] There are two things at the heart of it. [calm] Which point of the front view becomes which point of the top view. [calm] And how you pull construction lines across and use them. [calm] The bore and the tapped holes you drew today are hidden when seen from the side. [calm] So they come out as hidden lines. [calm] That is where you first use the hidden line layer you made in Lesson 2. [calm] The boss stands 8 forward. [calm] The thickness there is 20. [calm] That value too becomes a drawn thing for the first time, in the top view. [calm] When you finish you save it as the next state.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 24:31–27:14

    [calm] Here are today's commands in one place. [emphatic] Rather than the names, remember **when you use them**.
    [calm] That is the part that stays after the exam.

    (1) [measured] `OPEN`. [light] Opens a file. [calm] You use it to carry on every lesson from the previous state.

    (2) [measured] `Z`. [light] ZOOM. [light] Changes the zoom. [calm] You use it when you need to see where a snap landed.

    (3) [measured] `CLAYER`. [light] Changes the current layer. [calm] You use it to change layer from the command line.

    (4) [measured] `C`. [light] CIRCLE. [light] Draws a circle. [calm] You use it for holes, shafts and pitch circles.

    (5) [measured] `O`. [light] OFFSET. [calm] Makes the same shape a set distance away. [calm] You use it for concentric circles and parallel lines without picking the centre again.

    (6) [measured] `DSETTINGS`. [light] Opens the drafting settings. [calm] You use it to set the increment angle for polar tracking.

    (7) [measured] `L`. [light] LINE. [light] Draws a line. [calm] You use it for pieces you need to handle singly.

    (8) [measured] `ARRAYPOLAR`. [light] Arrays around a centre. [calm] You use it for things spaced evenly by angle, like bolt holes.

    (9) [measured] `E`. [light] ERASE. [light] Erases. [calm] You use it to clear away helper lines.

    (10) [measured] `XL`. [light] XLINE. [calm] Draws a construction line that runs on forever. [calm] You use it for projection lines.

    (11) [measured] `COPYMODE`. [calm] Decides whether the copy command repeats. [calm] You use it to end the command after one copy.

    (12) [measured] `CO`. [light] COPY. [calm] Puts the same thing somewhere else. [calm] You use it for repeated parts and identical holes.

    (13) [measured] `QSELECT`. [calm] Picks every object matching a condition at once. [emphatic] You use it to select only the construction lines and erase them.

    (14) [measured] `TRIMEXTENDMODE`. [calm] Sets how trim and extend choose. [calm] You use it to pick the cutting edge first.

    (15) [measured] `TR`. [light] TRIM. [calm] Cuts back to a boundary. [calm] You use it on overlapping lines and stubs that stick out.

    (16) [measured] `MI`. [light] MIRROR. [light] Copies symmetrically. [calm] You use it for shapes symmetrical left and right.

    (17) [measured] `TRIMMODE`. [calm] Decides whether the original lines are tidied after a chamfer or fillet. [calm] You use it to cut the original line back to the end of an arc or a slanted edge.

    (18) [measured] `F`. [light] FILLET. [calm] Puts a round between two lines. [calm] You use it on an inside corner where stress piles up.

    (19) [measured] `DI`. [light] DIST. [calm] Measures the distance between two points. [calm] You use it before you dimension.

    (20) [measured] `LI`. [light] LIST. [light] Shows an object's information. [calm] You use it to check that what you drew really is that value.

    (21) [measured] `DIMSCALE`. [calm] Sets the overall scale of dimensions and centre marks. [calm] You use it to keep the display size at model one to one.

    (22) [measured] `DIMCEN`. [calm] Sets the size and style of the centre mark. [calm] You use it to standardise the mark size at 3.

    (23) [measured] `DIMCENTER`. [calm] Makes the centre mark for a circle or an arc. [calm] You use it to mark the centres of taps, fillets and slot end arcs.

    (24) [measured] `SAVEAS`. [calm] Saves under a new name. [calm] You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 27:14–27:26

    (1) [light] That is today's portion. [warm] Well done.

    (2) [pointing] Next is Lesson 5, third angle projection. [warm] See you then.
