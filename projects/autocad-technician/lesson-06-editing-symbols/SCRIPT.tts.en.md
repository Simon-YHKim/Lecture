<!-- 생성물이다. 손으로 고치지 말고 원본 SCRIPT.en.md 를 고친 뒤 다시 뽑아라.
     python scripts/part/tts_script.py lesson-06-editing-symbols
     태그: asking · calm · cautionary · emphatic · light · measured · pointing · warm -->
# SCRIPT — AutoCAD Technician Lesson 6 · Editing and representation (English edition)

**Part:** `idler pulley bracket used on a car engine`<br>
**Checkpoint:** `L05_VIEWS → L06_REPRESENTED`<br>
**Voice:** Windows SAPI · Microsoft Zira Desktop · Rate 0 · pitch-preserving 1.15x<br>
**Voice direction:** The tone of looking over a finished drawing together and tidying it up. Through the hands-on section (Line 5), leave a beat for every click.

> Length not measured yet. The times below mirror the Korean script so the frames
> line up; they are replaced by measured values once the English speech exists.
> The parentheses name what lights up on screen at that moment. They are not read.

## Line 1 — Title (Frame 1)

**Time:** 0:00–0:05

    (silence)

    [calm] Lesson 6, editing and representation.

## Line 2 — What has to be done after you draw (Frame 2)

**Time:** 0:05–2:03

    [calm] Last time you projected the top view and the right side view from the front view. [calm] The shape of the idler pulley bracket used on a car engine is all there. [calm] But the file still carries the marks of the work. [calm] Hand a spare part drawing over in this state during LG Innotek equipment PM, preventive maintenance, and there is trouble. [calm] The reader cannot tell shape lines from helper lines, and it comes back as rework loss. [calm] Today you tidy the lines you have already drawn and make them read properly.

    (1 card — clearing projection and helper lines) [light] The first is tidying. [calm] The lines you drew long, up and across, to align the views are still there. [calm] They are not the shape of the part; they were used as a rule to line things up. [calm] Leave them and the reader cannot tell them from shape lines. [calm] The drawing's instructions become unclear too. [calm] You pick construction lines by object type with QSELECT and erase them in one go. [calm] There is no need to trim lines you are going to erase. [emphatic] You only tidy the shape lines that are left, with TRIM and EXTEND.

    (2 card — setting the linetype scale) [pointing] The second is making the linetypes distinguishable. [calm] Centerlines and hidden lines are dashed, but on screen right now they read as continuous. [calm] The dashes and gaps are too tight for the size of the drawing. [calm] Then they read as continuous both on screen and in print. [calm] There is no need to draw the lines again. [calm] You adjust the spacing with a scale value.

    (3 card — checking the layers) [light] The third is checking. [calm] You confirm that every line drawn over four lessons is on its own layer. [calm] Draw in a hurry and a line comes out on a layer you did not change. [calm] Draw a centerline on the visible line layer and it shows green and continuous. [calm] Later, when you give lineweight by layer, that line goes out at shape line weight as well. [calm] Check today so you are not fixing a pile of them in the last lesson.

    (4 card — reading drawing symbols) [pointing] The fourth is reading practice. [calm] A drawing from the floor also carries surface finish, geometric tolerance, material and heat treatment instructions. [cautionary] You do not draw them in this course. [calm] But if they are on a drawing you receive, you have to be able to read them. [calm] There will be times when a machine stops and you need a spare in a hurry. [calm] You find the part in the assembly drawing, check the part drawing, and hand it to the machine shop. [cautionary] Fail to read a symbol at that moment and the instruction goes over missing. [emphatic] Then a part comes back that only looks the same.

## Line 3 — The four things you use today (Frame 3)

**Time:** 2:03–4:09

    [calm] Before the hands-on, look at what each command changes. [emphatic] Memorise only the names and nothing comes to mind about where to use them. [calm] Know what changes and you can choose the command you need.

    (1 card — TRIM and EXTEND) [pointing] TRIM cuts and EXTEND lengthens. [calm] Both commands settle the reference line first. [calm] In TRIM it is called the cutting edge, in EXTEND the boundary edge. [calm] Cutting removes up to the reference; lengthening fills up to it. [asking] Why cut instead of erase? [emphatic] Because only part of the line has to go. [calm] Erase it and the intersection goes too. [calm] Cut it and the intersection stays where it was.

    (2 card — making symmetry with MIRROR) [pointing] This part's front view is symmetrical left and right. [asking] What happens if you draw each side of a symmetrical shape by hand? [light] They will be out. [calm] Off by one decimal place and the eye will not catch it. [calm] MIRROR flips a copy of one side across a reference line. [emphatic] Make one side exactly and the same shape appears on the other. [calm] You set the mirror axis with two points. [calm] Pick the lower and upper endpoints of the vertical centerline you stood up in Lesson 3, with the endpoint snap. [calm] A point caught with a snap has an exact value. [calm] Where there is no centerline, put the first point on the boss circle centre with the center snap. [calm] Turn ortho on with F8, put the cursor above that point and click. [calm] It is the same when you draw a jig to propose it. [cautionary] You do not draw the same support twice, left and right.

    (3 card — carrying properties with MATCHPROP) [cautionary] Say you find a line given the wrong layer. [calm] Erase it and draw it again and you have to get its position right again too. [calm] MATCHPROP picks one correct line as the source. [calm] It carries that line's layer, colour and linetype onto another line. [emphatic] The shape stays and only what it belongs to changes. [calm] It is like dipping a brush and painting the colour on. [calm] You reach for it often when you take over a drawing someone else made. [calm] It is useful when a spare part drawing's layers are all over the place. [calm] Rather than redrawing line by line, you bring them into line with this command.

    (4 card — what LTSCALE changes) [pointing] LTSCALE is the linetype scale for the whole drawing. [calm] This is where people get confused. [calm] This value does not change a line's length or position. [emphatic] The shape does not move; only the dash length and gap length change. [calm] The spacing you see on screen is the drawing-wide value times the object's own value. [emphatic] There are values in two places, so take care not to check only one.

## Line 4 — The instructions on the drawing (Frame 4)

**Time:** 4:09–8:07

    [calm] Now we look at how symbols and linetypes appear on a drawing. [calm] The first four items are instructions you have to read on a real drawing. [cautionary] You do not draw them in this course. [calm] The last two you work on yourself today.

    (1 row — surface finish symbols) [pointing] It is a symbol like a check mark with a split root. [calm] It instructs how finely to finish that face, with an Ra value beside it. [calm] As you saw in Lesson 2, the values on this part differ face by face. [calm] The bore, where the shaft turns, is instructed fine. [emphatic] The slot, where the bolt only passes through, may be rough. [asking] Why instruct differently face by face? [calm] Finish everything finely and operations pile up and the machining cost rises. [calm] Make everything rough and the face the shaft touches wears. [calm] So you instruct the finish you need where you need it. [cautionary] You do not draw this in the course exercises.

    (2 row — geometric tolerance) [pointing] It is a box split left and right. [calm] The symbol goes on the left, the permitted value on the right. [asking] How does it differ from a dimensional tolerance? [calm] A dimensional tolerance sets how far the size may depart. [measured] A diameter of 25 may run to 25.02, that sort of thing. [measured] This 25.02 is an example number to explain dimensional tolerance. [calm] It is not this part's specified tolerance. [cautionary] Do not carry it over as though the drawing said it. [calm] Geometric tolerance does not look at size. [calm] It sets how far form, attitude and position may depart. [asking] Why is it needed separately? [calm] Suppose the bore's diameter is a perfect 25. [asking] What if that hole is nonetheless drilled at a tilt to the back face? [calm] The shaft does not go in. [calm] If it does, it stands crooked. [calm] It is the notation that catches what size alone cannot. [cautionary] You do not draw this in the course exercises.

    (3 row — material notation) [pointing] It says what it is made of. [calm] A drawing from the floor has a separate material box inside the title block. [calm] On a drawing with several parts on it, it is one column of the parts list. [measured] The title block we made in Lesson 2 is 200 by 30. [emphatic] It has only two boxes, name and employee number, so there is no material box. [cautionary] So you do not write it in this course. [asking] Why does material have to be on a drawing? [calm] The same shape in a different material takes a different load. [calm] The machining speed and the tooling change too. [cautionary] This is where things go wrong when you order a spare in a hurry. [calm] Misread one material box and an unusable part arrives. [calm] When you are actually given the instruction, you copy the material designation from the task sheet as it stands. [cautionary] You do not decide it yourself.

    (4 row — heat treatment instructions) [asking] Why apply heat? [light] There are two purposes. [calm] One is to make it hard. [calm] You harden the surface to slow the rate of wear. [calm] The other is the opposite: to release. [calm] Cutting leaves force inside the material. [calm] Leave it and over time the part bends by itself. [calm] Give it heat to release that force and the dimensions hold. [asking] Where does it go? [calm] It is written as a sentence in the notes area at one side of the drawing. [emphatic] Where it applies to one area only, you draw a leader to that area and write it there. [cautionary] You do not draw this in the course exercises.

    (5 row — linetype scale) [pointing] From here on is what you work on today. [calm] Centerlines and hidden lines are lines of repeating dashes and gaps. [calm] Long dashes and short dashes alternate. [calm] The value that sets the length of those dashes and gaps is the linetype scale. [measured] In the Lesson 2 layer table you set 0.5 for the centerline and the hidden line. [asking] Do the dashed lines read as continuous on screen? [calm] The spacing is so tight that dash and gap have run together. [calm] Raise the value and they open out. [calm] The other way round, if the dashes look sparse and scattered, lower it. [calm] The value you give to each object goes in through the Properties window. [calm] The value that moves the whole drawing at once goes in with LTSCALE. [calm] If the screen does not change after you change the value, regenerate the drawing. [calm] This matters especially when you look at an equipment layout. [calm] Whatever is hidden behind a wall or a plate is drawn as a hidden line. [calm] Have that read as continuous and you cannot tell what is hidden.

    (6 row — checking the layers) [pointing] You cannot tell by eye whether a line you drew is on its own layer. [cautionary] The screen gives you no warning when the layer is wrong. [calm] So you have to ask the drawing itself. [calm] There are three ways to ask, and we will do each of them in the hands-on section shortly. [asking] Why ask today? [cautionary] Because when you give lineweight by layer in the last lesson, that one wrong line goes out at the wrong weight. [calm] By then the dimensions are on top of it and it is far harder to fix. [calm] You use the same method when you look at a layout drawing. [calm] Turn off just the equipment layer and the walkways and traffic lines show up. [calm] Turning them on and off finds a clash before it happens.

## Line 5 — Tidying and representation · DEMO-01 screen recording (Frame 5)

**Time:** 8:07–22:54

> This section is a screen recording. Work through the 16 steps below **in order and without skipping**, speaking as you go.
> What is inside backticks is what you actually type. Use the command line rather than the mouse menus.

### Step 1 — Open the previous file

    [measured] Type `OPEN` and press Enter. [calm] The file selection dialog opens.
    [measured] Find the `EDU-IB-02_L05_VIEWS` you saved last time. [calm] Select it and press Open.
    [cautionary] You do not make a new drawing. [calm] This course carries one file across six lessons.

    [measured] Type `Z` and press Enter, then `A` and press Enter. [light] That is zoom all.
    [calm] The whole A3 border comes onto the screen.

### Step 2 — Check the basic settings · snaps and ortho

    [calm] Press Esc twice to clear the command and the selection.
    [measured] Type `OS` and press Enter. [calm] Check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    [calm] Press OK to close the dialog. [emphatic] Press F3 to turn object snap on only if the status bar shows it off.
    [measured] `L`, Enter. [calm] While it asks for the first point, rest the cursor on the endpoint of an existing line. [cautionary] Do not click.
    [calm] Watch for the square marker, then press Esc twice to cancel LINE. [calm] If there is no marker, look at OS and F3 again.
    [emphatic] Look at ortho too, and press F8 to turn it on only if it is off. [calm] On diagonals and tangents you turn it off, as each step says.
    [calm] Catch a point on the shape itself and you notice at once when a value has gone out.

### Step 3 — See the state before tidying

    [cautionary] You do not start cutting. [calm] First you look at what is left.

    [calm] The vertical lines that ran up from the front view to the top view.
    [calm] The horizontal lines that ran right from the front view to the right side view.
    [calm] They are the projection lines you drew last time to align the views. [calm] They stick out beyond the views.

    [light] Click one projection line. [measured] The layer indicator at the top of the screen changes to `Dimension line`.
    [calm] That is because you drew the projection lines on the dimension line layer in Lesson 5.
    [emphatic] If this line were on the visible line layer, it would print at exactly the shape line weight.
    [cautionary] Whoever reads it hunts for where on the part it is and never finds it. [calm] Press Esc to clear the selection.

### Step 4 — Erase the projection lines in one go with QSELECT

    [calm] Tidying starts with erasing, not with cutting.
    [calm] Let us settle the names first. [calm] Projection line is what we call a line drawn to align the views,
    [calm] and construction line is that line's object type. [light] Helper line covers both.
    [calm] You drew every projection line with XLINE in Lesson 5, so the object type is construction line throughout.
    [calm] A construction line is infinitely long, so it is not a line to leave on the drawing.
    [calm] If it is not staying, there is no reason to tidy it.

    [measured] Type `QSELECT` and press Enter.
    [calm] Leave apply to as the entire drawing.
    [measured] Under object type choose `Construction Line`.
    [calm] Change the operator to select all. [calm] How to apply is include in new selection set, and append to current selection set is off.
    [calm] Press OK and every construction line is selected.

    [light] Press Delete. [calm] The projection lines disappear in one go.
    [calm] It is the method mentioned at the end of Lesson 5.

    [light] Look at the screen. [emphatic] Only the shape lines of the three views are left.
    [calm] Clicking them one by one, or chopping infinite lines into pieces first, would have taken minutes here.
    [calm] There are lines this condition does not catch, though.
    [calm] A short helper line drawn with LINE while drafting is not caught as object type construction line, so it stays.
    [calm] You erase those separately in step 8.

### Step 5 — Learn the cutting side with TRIM

    [calm] The part from Lesson 5 is a finished outline. [cautionary] You do not practise by cutting a real edge.
    [calm] You make three short practice lines in an empty area inside the border, clear of the part and the title block.
    [measured] Change the current layer to `Dimension line` and turn ortho on.
    [measured] `L`, Enter, click a first point in the empty area, put the cursor to the right, `40`, Enter, Enter to finish.
    [measured] In another empty spot, `L`, Enter, click a first point, put the cursor above, `20`, Enter, Enter to finish.
    [measured] `M`, Enter. [calm] That is MOVE, the move command. [emphatic] Click only the vertical line and press Enter to end the selection.
    [calm] The base point is the vertical line's midpoint; the second point is the horizontal line's midpoint. [light] The move ends here.
    [measured] `COPYMODE`, Enter, `1`, Enter to set copying once.
    [measured] `CO`, Enter, click only the vertical line and press Enter. [calm] The base point is that line's midpoint.
    [measured] Put the cursor to the right and type `10`, Enter. [cautionary] When the copy is done, do not press Enter again.
    [calm] One horizontal line is crossed by two vertical boundary lines.

    [measured] `TRIMEXTENDMODE`, Enter, `0`, Enter. [measured] That puts it into AutoCAD 2024's standard mode.
    [measured] `TR`, Enter. [emphatic] Click only the left vertical boundary line and press Enter to end the boundary selection.
    [calm] On the horizontal line, click the part that is to the right of the left boundary.
    [measured] That half goes and the horizontal line becomes 20 long.
    [cautionary] If you cut the wrong side, recover with `U`, Enter inside the command and pick again.
    [calm] Press Enter to end TRIM. [calm] You use the three lines in the next step too.


### Step 6 — Lengthen to a boundary with EXTEND

    [measured] `EX`, Enter. [emphatic] Click only the right vertical boundary line and press Enter.
    [calm] Click near the right end of the horizontal line.
    [measured] That end lengthens 10 to the right boundary and the horizontal line becomes 30.
    [calm] The end nearer where you clicked is the end that lengthens.
    [calm] Pick the other end and it does not go to the boundary you wanted.
    [cautionary] If you lengthened the wrong one, undo it with `U`, Enter inside the command.
    [calm] When it is right, press Enter to end EXTEND.


### Step 7 — Switch from lengthening to cutting with Shift

    [measured] `EX`, Enter. [emphatic] This time click only the left vertical boundary line and press Enter.
    [calm] Hold the Shift key and click the part of the horizontal line between the two vertical boundaries.
    [calm] You are inside EXTEND, but that part is cut. [measured] The horizontal line is 20 again.
    [calm] Release Shift and press Enter to end the command.
    [calm] Hold Shift inside TRIM and you get the lengthening function instead.
    [emphatic] Either way you pick the boundary first, and hold Shift only when you swap the function.


### Step 8 — Erase the practice lines and any helper lines left

    [calm] Press Esc twice to end the command and the selection.
    [calm] Click the one horizontal line and the two vertical boundary lines you just made, one at a time, to select them.
    [calm] Check that no part of the drawing or the border got selected, and press Delete.
    [calm] All three practice lines should be gone.

    [measured] `Z`, Enter, `A`, Enter to see the whole thing.
    [calm] If there is a short helper line made separately while drafting, tell it from the real shape, select it and erase it with Delete.
    [calm] If there is none, erase nothing further. [calm] Lesson 5's authoritative shape has to stay as it is.
    [measured] Put the current layer back to `Visible line`.


### Step 9 — Measure whether the slots really are symmetrical

    [calm] Look at the two long horizontal holes at the bottom of the front view. [calm] You check whether these two slots are symmetrical.
    [light] Follow the dimensions. [measured] From the left end to the first end circle centre is 29.
    [measured] Within one slot, between the two end circles is 12. [measured] Between the first end circles of the two slots is 50.
    [measured] So the left slot's end circle centres are 29 and 41, and the slot centre is 35.
    [measured] The right slot is 29 plus 50, that is 79 and 91, with its centre at 85.
    [measured] The overall width is 120, so from the right end to 91 is 29 as well.
    [calm] Left and right are perfectly symmetrical.

    [measured] The mirror axis is the vertical line at half of 120 across, x equals 60.
    [measured] The boss centre's horizontal position is 60 too, so it is the same line.

    [measured] You already made this symmetry in Lesson 4, step 11.
    [calm] With MIRROR you picked the left slot and threw it across that vertical line.
    [calm] You set the mirror axis with two points, and you catch those two points with a snap.
    [calm] You pick the lower and upper endpoints of the vertical centerline you stood up in Lesson 3, with the endpoint snap.
    [calm] Or you put the first point on the boss circle centre with the center snap.
    [calm] Then with ortho on, put the cursor above that point and click. [calm] It is the same axis.
    [calm] A point caught with a snap is not eyeballed; it is an exact point.
    [calm] So today's job is not to build it again. [calm] It is to measure whether it is right.
    [calm] Erase something already right and rebuild it and nothing is added to the drawing.

    [calm] Before you measure, check with F3 that object snap is on. [measured] Check with `OS`, Enter that center is ticked too.
    [measured] Type `DI` and press Enter.
    [calm] Click the left end circle centre of the left slot and the left end circle centre of the right slot.
    [measured] It comes out 50. [measured] That is 29 to 79.

    [measured] `DI`, Enter. [calm] The first point is the right end circle centre of the right slot.
    [measured] When it asks the second point, type `PER` and press Enter.
    [calm] Put the cursor around the middle of the base's right vertical edge and click when the perpendicular marker appears.
    [measured] To the foot of the perpendicular dropped at the same height is 29. [calm] Pick the chamfer or a bottom endpoint and you get a diagonal distance.
    [measured] 29 from the left end, 29 from the right end. [light] Left and right agree.

    [calm] Let us settle the rest of the mirror command's rules here too.
    [calm] It asks whether to erase the original, and the default is no.
    [calm] An object thrown by mirror inherits the original's layer as it is.
    [calm] Colour and linetype follow too.

    [calm] Now look at what a slot is made of.
    [calm] Click once and you catch one arc, or else one straight line.
    [calm] That is because a slot is two arcs and two straight lines.
    [calm] It is the result of drawing two circles in Lesson 4 and trimming the inside away.
    [calm] The base outline is a separate polyline.
    [calm] It has been through TRIM and FILLET, so check on screen the extent of what is currently selected.
    [calm] You use this property on an equipment layout when you take a machine's footprint and move the whole thing.

    [calm] Last, one word of warning.
    [calm] If there is text in what you mirror, the result differs.
    [measured] Type `MIRRTEXT` and press Enter. [calm] It shows the current value.
    [calm] If it is 0, press Enter as it stands to come out.
    [emphatic] At 0 the letters are not flipped; only their position moves.
    [calm] At 1 the letters flip like a mirror and cannot be read.
    [light] The default is 0. [calm] If you find yourself mirroring near the title block, check it first.

### Step 10 — Fix a layer with MATCHPROP

    [cautionary] As you tidy, a line with the wrong layer turns up.
    [calm] Take the front view's vertical centerline as the target. [calm] The source is the front view's horizontal centerline.
    [calm] The two lines meet at a point but they are separate objects.
    [calm] Look at the target centerline. [asking] Does it show green and continuous instead of a red chain line?
    [calm] Then that line was drawn on the visible line layer.
    [calm] If you drew Lesson 5 properly, there may not be a single green continuous line.
    [emphatic] In that case pick only the front view's vertical centerline, change its layer to visible line, and press Esc to clear the selection.
    [cautionary] It is a practice of putting one deliberately wrong and undoing it. [emphatic] The steps after this are exactly the same.

    [cautionary] You do not draw it again. [measured] Type `MA` and press Enter. [calm] That is the match properties command.

    [calm] First click one source object.
    [calm] The source is the front view's horizontal centerline. [calm] Click the horizontal stretch visible outside the circle on the left.
    [calm] The cursor turns into a brush.

    [measured] Here type `S` and press Enter. [calm] The property settings dialog opens.
    [calm] There are entries for color, layer, linetype, linetype scale and lineweight.
    [calm] See whether layer is ticked.
    [emphatic] With the tick missing, only the colour carries over and the layer stays as it was.
    [calm] It looks fixed and is not actually fixed. [light] Press OK.

    [calm] For the target, click the part of the front view's vertical centerline that runs below the base.
    [calm] The moment you click, that line moves onto the same layer as the source.
    [calm] Colour and linetype change with it.
    [calm] If there is more to fix, keep clicking. [calm] When you are done, Enter.

### Step 11 — Check the layers with LAYER

    [measured] Type `LA` and press Enter. [calm] The layer properties manager opens.
    [calm] There are four: visible line, centerline, hidden line, dimension line.

    [calm] The way to check is to turn them off one at a time.
    [calm] Click the lamp icon on the centerline row to turn it off.
    [calm] Every red centerline on screen should disappear; that is correct.
    [asking] Is there a red line still there that did not disappear?
    [calm] That is a line on another layer given the colour red directly.
    [asking] And what if nothing disappeared from a place where a centerline should be?
    [calm] That line is on another layer.

    [calm] Learn the difference between off and frozen here.
    [emphatic] Off only makes it invisible on screen. [calm] The object is still there.
    [calm] Freeze takes it off the screen and out of drawing regeneration as well.
    [calm] Neither of them erases anything.

    [calm] When you have checked, turn the lamp back on. [cautionary] **Turn it back on without fail.**
    [calm] Save it while it is off and the layer state is saved into the file with it.
    [calm] Open it next time and, thinking the lines are gone, you draw them again.

    [calm] Turn hidden line and dimension line off and on once each the same way.

### Step 12 — Pick by layer with QSELECT

    [calm] There is a surer way than scanning by eye.
    [measured] Type `QSELECT` and press Enter. [calm] The quick select dialog opens.

    [calm] Leave apply to as the entire drawing.
    [calm] Object type is multiple, that is, every kind.
    [calm] In the property list choose layer.
    [calm] Leave the operator as equals.
    [calm] For the value choose centerline.
    [calm] How to apply is include in new selection set.
    [light] Press OK.

    [calm] Every object on the centerline layer is selected.
    [calm] The command line shows a number for how many were selected.
    [calm] You can see on screen which lines are selected.
    [calm] The boss centre, the bore centre, the slot centres, the mirror axis.
    [calm] If there is no selection mark where a centerline should be, it is on another layer.

    [calm] Press Esc to clear the selection. [calm] Run it once for the hidden line the same way.

### Step 13 — Bring colour and linetype into line as ByLayer

    [calm] Sometimes the layer is right but a colour was given to the object directly.
    [calm] Then you change the layer colour and that one line does not change.
    [calm] The point of managing by layer is gone.

    [calm] Press Ctrl+A to select everything. [measured] Or `SELECT`, Enter, `ALL`, Enter, Enter.

    [calm] Press Ctrl+1 to open the Properties window. [light] The general entries show.
    [calm] Color, layer, linetype, linetype scale, lineweight.

    [calm] Click the color box and choose ByLayer.
    [calm] Set the linetype box to ByLayer as well.
    [calm] Set the lineweight box to ByLayer as well.

    [cautionary] Do not touch the layer box. [calm] Everything is selected right now.
    [calm] Choose a layer here and the whole drawing piles onto one layer.
    [light] You could undo it. [cautionary] Even so, do not create anything to undo.

    [calm] Press Esc to clear the selection. [calm] Now the layer decides the colour.

### Step 14 — Give the centerlines and hidden lines their linetype scale

    [calm] Now you set the dash spacing.

    [measured] `QSELECT`, Enter. [calm] Set the property to layer and the value to centerline, and OK.
    [calm] Every centerline object is selected.
    [calm] Look at the Properties window with Ctrl+1. [measured] In the linetype scale box type `0.5` and press Enter.
    [calm] Press Esc to clear the selection and look at the screen.
    [calm] Long dashes and short dashes alternating means it is right.

    [calm] The hidden line goes the same way. [measured] `QSELECT`, Enter, layer hidden line, OK.
    [measured] In the Properties window's linetype scale type `0.5` and press Enter. [light] Esc.

    [measured] This 0.5 is the value you set in the Lesson 2 layer table.
    [calm] It is not a number invented now.

### Step 15 — Set the whole drawing with LTSCALE

    [calm] There is another value besides the one you give each object.
    [calm] It is the value that moves the whole drawing at once.

    [measured] Type `LTSCALE` and press Enter. [calm] It asks for a new linetype scale factor.
    [calm] The current value shows in angle brackets. [calm] The starting value is 1.

    [calm] The spacing you actually see on screen is the product of the two values.
    [calm] The drawing-wide value times each object's value.
    [measured] Say a centerline object is 0.5 and the whole drawing is 1. [measured] It is drawn at 0.5.
    [asking] What happens if you raise the whole drawing to 2 here?
    [calm] The object value stays the same and the spacing on screen doubles.

    [measured] The authoritative value for this course is `1`. [measured] Type `1` and press Enter.
    [measured] If it still reads as continuous, zoom in and check the layer's CENTER and HIDDEN and the object scale of 0.5.
    [cautionary] You do not change the authoritative value at will to suit what the screen looks like.

    [measured] If you changed the value and the screen did not change, type `RE` and press Enter.
    [light] That is drawing regeneration. [light] It redraws the screen.

    [calm] This value does not change the shape.
    [calm] Not the length of a line, not its position, not a dimension. [emphatic] Only the dash and gap lengths change.

### Step 16 — Save under a new name

    [calm] Before you save, one last check.
    [calm] Open the layer list at the top of the screen. [calm] See that all four lamps are on.
    [calm] See that no layer is frozen. [calm] If any is off, turn it on.
    [calm] Leave the current layer as visible line. [calm] Check too that no practice line or construction line is left.

    [measured] Type `SAVEAS` and press Enter.
    [calm] Put the new name in the file name box.
    [measured] It is `EDU-IB-02_L06_REPRESENTED`.
    [calm] Leave the file type as AutoCAD drawing, dwg. [light] Press Save.

    [asking] Why a new name instead of overwriting?
    [calm] Today you did erasing and cutting.
    [calm] You may have erased a line you should not have, and that comes to light later.
    [calm] Leave a name behind each lesson and you can go back to an earlier state and start again.
    [calm] You use the same habit when you revise a drawing on the floor.
    [calm] You have to keep the revised issue separately to know what changed and when.

    [calm] Next time you open this file and start there.

## Line 6 — This is where people go wrong (Frame 6)

**Time:** 22:54–24:56

    [calm] Four mistakes come round again and again in tidying work. [calm] All four look perfectly fine on screen. [calm] So you cannot find them yourself.

    (1 card — moving on with helper lines still there) [pointing] First check whether you erased the three practice lines. [calm] A stub of a helper line drawn between two views may be left as well. [calm] The construction lines drawn with XLINE went in one go in step 4, but a short helper line drawn with LINE is not caught by that condition. [calm] They are left near the edges of the border too. [calm] It is a screen you have been looking at while you worked, so your eye passes over it. [calm] The way to check is zoom all. [measured] Type `Z`, Enter, `A`, Enter. [calm] Put the whole border on one screen and look. [asking] What can you see besides the part shape, the border and the title block? [calm] That is a helper line still there.

    (2 card — thinking you erased it when you only turned the layer off) [cautionary] This happens when you turn a layer off to check and do not turn it back on. [emphatic] The lines have gone from the screen, so it looks exactly like erasing. [calm] But the objects are still there. [calm] That the layer is off is saved into the file too. [calm] Open it next lesson and it looks as if there is not one centerline. [calm] So you draw the centerlines again. [calm] Then there are two lines laid on top of each other in the same place. [calm] Open the layer list before you save. [calm] Get into the habit of checking that every lamp is on.

    (3 card — applying LTSCALE to one object only) [pointing] You click one centerline and fix its linetype scale. [calm] You see that line come out nicely and think you are finished. [calm] The rest of the centerlines are unchanged. [calm] Print it and lines of the same kind have different spacing. [calm] When you give a value to objects, use QSELECT. [calm] Take that whole layer in one go and put it in. [calm] The value that moves the whole drawing is LTSCALE. [calm] Put it in once on the command line and it takes everywhere. [calm] Remember that the two values are separate.

    (4 card — the layer is right but the colour was given to the object) [pointing] The line is properly on the centerline layer. [calm] But that line's color property is not ByLayer. [calm] It has been set directly to red. [calm] Right now the layer colour is red too, so you cannot tell on screen. [light] The trouble comes later. [calm] A task asks you to change the centerlines to another colour. [calm] You change the layer colour and that one line stays red. [calm] It is hard to find, too. [calm] So at the tidying stage you select everything once. [calm] You bring color, linetype and lineweight into line as ByLayer and move on.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 24:56–25:50

    (1 left) [pointing] Today's file is one whose representation changed, not its shape. [calm] You cleared the projection lines away, measured the slots' symmetry to confirm it, and put layers, colours and dash spacing back where they belong. [emphatic] With this much set, next time you only have to lay dimensions on top. [measured] You open the saved `EDU-IB-02_L06_REPRESENTED` as it is and start there.

    (2 right) [pointing] Next time is the last lesson. [light] You dimension. [calm] First you make a dimension style. [calm] You set the text height and the arrow size. [calm] You set the spacing of dimension lines and extension lines, and the number of decimal places. [calm] Then you change the current layer to dimension line and start entering. [calm] Dimensions go in one at a time, starting from the overall ones. [calm] Then you look at the principles for laying dimensions out without overlapping. [cautionary] You look at why you must not overwrite dimension text by hand. [calm] You finish with the scale notation and the title block, and save the final file. [calm] The file you have built over six lessons is finished then.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 25:50–27:53

    [calm] Here are today's commands in one place. [emphatic] Rather than the names, remember **when you use them**.
    [calm] That is the part that stays after the exam.

    (1) [measured] `OPEN`. [light] Opens a file. [calm] You use it to carry on every lesson from the previous state.

    (2) [measured] `Z`. [light] ZOOM. [light] Changes the zoom. [calm] You use it when you need to see where a snap landed.

    (3) [measured] `OS`. [light] OSNAP. [calm] Chooses which object snaps are on. [emphatic] You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) [measured] `L`. [light] LINE. [light] Draws a line. [calm] You use it for pieces you need to handle singly.

    (5) [measured] `QSELECT`. [calm] Picks every object matching a condition at once. [emphatic] You use it to select only the construction lines and erase them.

    (6) [measured] `M`. [light] MOVE. [light] Moves something. [calm] You use it to bring a centerline or a view onto a reference point.

    (7) [measured] `COPYMODE`. [calm] Decides whether the copy command repeats. [calm] You use it to end the command after one copy.

    (8) [measured] `CO`. [light] COPY. [calm] Puts the same thing somewhere else. [calm] You use it for repeated parts and identical holes.

    (9) [measured] `TRIMEXTENDMODE`. [calm] Sets how trim and extend choose. [calm] You use it to pick the cutting edge first.

    (10) [measured] `TR`. [light] TRIM. [calm] Cuts back to a boundary. [calm] You use it on overlapping lines and stubs that stick out.

    (11) [measured] `EX`. [light] EXTEND. [light] Lengthens to a boundary. [calm] You use it on a line that falls short of an intersection.

    (12) [measured] `DI`. [light] DIST. [calm] Measures the distance between two points. [calm] You use it before you dimension.

    (13) [measured] `MIRRTEXT`. [calm] Decides whether text flips when mirrored. [calm] You use it before mirroring something with text in it.

    (14) [measured] `MA`. [light] MATCHPROP. [calm] Copies properties onto another object. [cautionary] You use it to move a line off the wrong layer without redrawing it.

    (15) [measured] `LA`. [light] LAYER. [light] Creates and manages layers. [calm] You use it when linetype and color belong to the layer, not to each object.

    (16) [measured] `LTSCALE`. [calm] Changes the global linetype scale. [calm] You use it when a dashed line reads as continuous.

    (17) [measured] `SAVEAS`. [calm] Saves under a new name. [calm] You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 27:53–28:14

    (1) [light] That is today's portion. [calm] The tidying will have felt longer than the drawing. [calm] It is like that on the real floor too. [warm] Well done.

    (2) [pointing] Next is Lesson 7, dimensioning and finishing the drawing. [calm] It is the last lesson in which you draw the part. [warm] See you then.
