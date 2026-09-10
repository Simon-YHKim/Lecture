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

    Lesson 6, editing and representation.

## Line 2 — What has to be done after you draw (Frame 2)

**Time:** 0:05–2:03

    Last time you projected the top view and the right side view from the front view. The shape of the idler pulley bracket used on a car engine is all there. But the file still carries the marks of the work. Hand a spare part drawing over in this state during LG Innotek equipment PM, preventive maintenance, and there is trouble. The reader cannot tell shape lines from helper lines, and it comes back as rework loss. Today you tidy the lines you have already drawn and make them read properly.

    (1 card — clearing projection and helper lines) The first is tidying. The lines you drew long, up and across, to align the views are still there. They are not the shape of the part; they were used as a rule to line things up. Leave them and the reader cannot tell them from shape lines. The drawing's instructions become unclear too. You pick construction lines by object type with QSELECT and erase them in one go. There is no need to trim lines you are going to erase. You only tidy the shape lines that are left, with TRIM and EXTEND.

    (2 card — setting the linetype scale) The second is making the linetypes distinguishable. Centerlines and hidden lines are dashed, but on screen right now they read as continuous. The dashes and gaps are too tight for the size of the drawing. Then they read as continuous both on screen and in print. There is no need to draw the lines again. You adjust the spacing with a scale value.

    (3 card — checking the layers) The third is checking. You confirm that every line drawn over four lessons is on its own layer. Draw in a hurry and a line comes out on a layer you did not change. Draw a centerline on the visible line layer and it shows green and continuous. Later, when you give lineweight by layer, that line goes out at shape line weight as well. Check today so you are not fixing a pile of them in the last lesson.

    (4 card — reading drawing symbols) The fourth is reading practice. A drawing from the floor also carries surface finish, geometric tolerance, material and heat treatment instructions. You do not draw them in this course. But if they are on a drawing you receive, you have to be able to read them. There will be times when a machine stops and you need a spare in a hurry. You find the part in the assembly drawing, check the part drawing, and hand it to the machine shop. Fail to read a symbol at that moment and the instruction goes over missing. Then a part comes back that only looks the same.

## Line 3 — The four things you use today (Frame 3)

**Time:** 2:03–4:09

    Before the hands-on, look at what each command changes. Memorise only the names and nothing comes to mind about where to use them. Know what changes and you can choose the command you need.

    (1 card — TRIM and EXTEND) TRIM cuts and EXTEND lengthens. Both commands settle the reference line first. In TRIM it is called the cutting edge, in EXTEND the boundary edge. Cutting removes up to the reference; lengthening fills up to it. Why cut instead of erase? Because only part of the line has to go. Erase it and the intersection goes too. Cut it and the intersection stays where it was.

    (2 card — making symmetry with MIRROR) This part's front view is symmetrical left and right. What happens if you draw each side of a symmetrical shape by hand? They will be out. Off by one decimal place and the eye will not catch it. MIRROR flips a copy of one side across a reference line. Make one side exactly and the same shape appears on the other. You set the mirror axis with two points. Pick the lower and upper endpoints of the vertical centerline you stood up in Lesson 3, with the endpoint snap. A point caught with a snap has an exact value. Where there is no centerline, put the first point on the boss circle centre with the center snap. Turn ortho on with F8, put the cursor above that point and click. It is the same when you draw a jig to propose it. You do not draw the same support twice, left and right.

    (3 card — carrying properties with MATCHPROP) Say you find a line given the wrong layer. Erase it and draw it again and you have to get its position right again too. MATCHPROP picks one correct line as the source. It carries that line's layer, colour and linetype onto another line. The shape stays and only what it belongs to changes. It is like dipping a brush and painting the colour on. You reach for it often when you take over a drawing someone else made. It is useful when a spare part drawing's layers are all over the place. Rather than redrawing line by line, you bring them into line with this command.

    (4 card — what LTSCALE changes) LTSCALE is the linetype scale for the whole drawing. This is where people get confused. This value does not change a line's length or position. The shape does not move; only the dash length and gap length change. The spacing you see on screen is the drawing-wide value times the object's own value. There are values in two places, so take care not to check only one.

## Line 4 — The instructions on the drawing (Frame 4)

**Time:** 4:09–8:07

    Now we look at how symbols and linetypes appear on a drawing. The first four items are instructions you have to read on a real drawing. You do not draw them in this course. The last two you work on yourself today.

    (1 row — surface finish symbols) It is a symbol like a check mark with a split root. It instructs how finely to finish that face, with an Ra value beside it. As you saw in Lesson 2, the values on this part differ face by face. The bore, where the shaft turns, is instructed fine. The slot, where the bolt only passes through, may be rough. Why instruct differently face by face? Finish everything finely and operations pile up and the machining cost rises. Make everything rough and the face the shaft touches wears. So you instruct the finish you need where you need it. You do not draw this in the course exercises.

    (2 row — geometric tolerance) It is a box split left and right. The symbol goes on the left, the permitted value on the right. How does it differ from a dimensional tolerance? A dimensional tolerance sets how far the size may depart. A diameter of 25 may run to 25.02, that sort of thing. This 25.02 is an example number to explain dimensional tolerance. It is not this part's specified tolerance. Do not carry it over as though the drawing said it. Geometric tolerance does not look at size. It sets how far form, attitude and position may depart. Why is it needed separately? Suppose the bore's diameter is a perfect 25. What if that hole is nonetheless drilled at a tilt to the back face? The shaft does not go in. If it does, it stands crooked. It is the notation that catches what size alone cannot. You do not draw this in the course exercises.

    (3 row — material notation) It says what it is made of. A drawing from the floor has a separate material box inside the title block. On a drawing with several parts on it, it is one column of the parts list. The title block we made in Lesson 2 is 200 by 30. It has only two boxes, name and employee number, so there is no material box. So you do not write it in this course. Why does material have to be on a drawing? The same shape in a different material takes a different load. The machining speed and the tooling change too. This is where things go wrong when you order a spare in a hurry. Misread one material box and an unusable part arrives. When you are actually given the instruction, you copy the material designation from the task sheet as it stands. You do not decide it yourself.

    (4 row — heat treatment instructions) Why apply heat? There are two purposes. One is to make it hard. You harden the surface to slow the rate of wear. The other is the opposite: to release. Cutting leaves force inside the material. Leave it and over time the part bends by itself. Give it heat to release that force and the dimensions hold. Where does it go? It is written as a sentence in the notes area at one side of the drawing. Where it applies to one area only, you draw a leader to that area and write it there. You do not draw this in the course exercises.

    (5 row — linetype scale) From here on is what you work on today. Centerlines and hidden lines are lines of repeating dashes and gaps. Long dashes and short dashes alternate. The value that sets the length of those dashes and gaps is the linetype scale. In the Lesson 2 layer table you set 0.5 for the centerline and the hidden line. Do the dashed lines read as continuous on screen? The spacing is so tight that dash and gap have run together. Raise the value and they open out. The other way round, if the dashes look sparse and scattered, lower it. The value you give to each object goes in through the Properties window. The value that moves the whole drawing at once goes in with LTSCALE. If the screen does not change after you change the value, regenerate the drawing. This matters especially when you look at an equipment layout. Whatever is hidden behind a wall or a plate is drawn as a hidden line. Have that read as continuous and you cannot tell what is hidden.

    (6 row — checking the layers) You cannot tell by eye whether a line you drew is on its own layer. The screen gives you no warning when the layer is wrong. So you have to ask the drawing itself. There are three ways to ask, and we will do each of them in the hands-on section shortly. Why ask today? Because when you give lineweight by layer in the last lesson, that one wrong line goes out at the wrong weight. By then the dimensions are on top of it and it is far harder to fix. You use the same method when you look at a layout drawing. Turn off just the equipment layer and the walkways and traffic lines show up. Turning them on and off finds a clash before it happens.

## Line 5 — Tidying and representation · DEMO-01 screen recording (Frame 5)

**Time:** 8:07–22:54

> This section is a screen recording. Work through the 16 steps below **in order and without skipping**, speaking as you go.
> What is inside backticks is what you actually type. Use the command line rather than the mouse menus.

### Step 1 — Open the previous file

    Type `OPEN` and press Enter. The file selection dialog opens.
    Find the `EDU-IB-02_L05_VIEWS` you saved last time. Select it and press Open.
    You do not make a new drawing. This course carries one file across six lessons.

    Type `Z` and press Enter, then `A` and press Enter. That is zoom all.
    The whole A3 border comes onto the screen.

### Step 2 — Check the basic settings · snaps and ortho

    Press Esc twice to clear the command and the selection.
    Type `OS` and press Enter. Check the six: endpoint, midpoint, center, quadrant, intersection and tangent.
    Press OK to close the dialog. Press F3 to turn object snap on only if the status bar shows it off.
    `L`, Enter. While it asks for the first point, rest the cursor on the endpoint of an existing line. Do not click.
    Watch for the square marker, then press Esc twice to cancel LINE. If there is no marker, look at OS and F3 again.
    Look at ortho too, and press F8 to turn it on only if it is off. On diagonals and tangents you turn it off, as each step says.
    Catch a point on the shape itself and you notice at once when a value has gone out.

### Step 3 — See the state before tidying

    You do not start cutting. First you look at what is left.

    The vertical lines that ran up from the front view to the top view.
    The horizontal lines that ran right from the front view to the right side view.
    They are the projection lines you drew last time to align the views. They stick out beyond the views.

    Click one projection line. The layer indicator at the top of the screen changes to `Dimension line`.
    That is because you drew the projection lines on the dimension line layer in Lesson 5.
    If this line were on the visible line layer, it would print at exactly the shape line weight.
    Whoever reads it hunts for where on the part it is and never finds it. Press Esc to clear the selection.

### Step 4 — Erase the projection lines in one go with QSELECT

    Tidying starts with erasing, not with cutting.
    Let us settle the names first. Projection line is what we call a line drawn to align the views,
    and construction line is that line's object type. Helper line covers both.
    You drew every projection line with XLINE in Lesson 5, so the object type is construction line throughout.
    A construction line is infinitely long, so it is not a line to leave on the drawing.
    If it is not staying, there is no reason to tidy it.

    Type `QSELECT` and press Enter.
    Leave apply to as the entire drawing.
    Under object type choose `Construction Line`.
    Change the operator to select all. How to apply is include in new selection set, and append to current selection set is off.
    Press OK and every construction line is selected.

    Press Delete. The projection lines disappear in one go.
    It is the method mentioned at the end of Lesson 5.

    Look at the screen. Only the shape lines of the three views are left.
    Clicking them one by one, or chopping infinite lines into pieces first, would have taken minutes here.
    There are lines this condition does not catch, though.
    A short helper line drawn with LINE while drafting is not caught as object type construction line, so it stays.
    You erase those separately in step 8.

### Step 5 — Learn the cutting side with TRIM

    The part from Lesson 5 is a finished outline. You do not practise by cutting a real edge.
    You make three short practice lines in an empty area inside the border, clear of the part and the title block.
    Change the current layer to `Dimension line` and turn ortho on.
    `L`, Enter, click a first point in the empty area, put the cursor to the right, `40`, Enter, Enter to finish.
    In another empty spot, `L`, Enter, click a first point, put the cursor above, `20`, Enter, Enter to finish.
    `M`, Enter. That is MOVE, the move command. Click only the vertical line and press Enter to end the selection.
    The base point is the vertical line's midpoint; the second point is the horizontal line's midpoint. The move ends here.
    `COPYMODE`, Enter, `1`, Enter to set copying once.
    `CO`, Enter, click only the vertical line and press Enter. The base point is that line's midpoint.
    Put the cursor to the right and type `10`, Enter. When the copy is done, do not press Enter again.
    One horizontal line is crossed by two vertical boundary lines.

    `TRIMEXTENDMODE`, Enter, `0`, Enter. That puts it into AutoCAD 2024's standard mode.
    `TR`, Enter. Click only the left vertical boundary line and press Enter to end the boundary selection.
    On the horizontal line, click the part that is to the right of the left boundary.
    That half goes and the horizontal line becomes 20 long.
    If you cut the wrong side, recover with `U`, Enter inside the command and pick again.
    Press Enter to end TRIM. You use the three lines in the next step too.


### Step 6 — Lengthen to a boundary with EXTEND

    `EX`, Enter. Click only the right vertical boundary line and press Enter.
    Click near the right end of the horizontal line.
    That end lengthens 10 to the right boundary and the horizontal line becomes 30.
    The end nearer where you clicked is the end that lengthens.
    Pick the other end and it does not go to the boundary you wanted.
    If you lengthened the wrong one, undo it with `U`, Enter inside the command.
    When it is right, press Enter to end EXTEND.


### Step 7 — Switch from lengthening to cutting with Shift

    `EX`, Enter. This time click only the left vertical boundary line and press Enter.
    Hold the Shift key and click the part of the horizontal line between the two vertical boundaries.
    You are inside EXTEND, but that part is cut. The horizontal line is 20 again.
    Release Shift and press Enter to end the command.
    Hold Shift inside TRIM and you get the lengthening function instead.
    Either way you pick the boundary first, and hold Shift only when you swap the function.


### Step 8 — Erase the practice lines and any helper lines left

    Press Esc twice to end the command and the selection.
    Click the one horizontal line and the two vertical boundary lines you just made, one at a time, to select them.
    Check that no part of the drawing or the border got selected, and press Delete.
    All three practice lines should be gone.

    `Z`, Enter, `A`, Enter to see the whole thing.
    If there is a short helper line made separately while drafting, tell it from the real shape, select it and erase it with Delete.
    If there is none, erase nothing further. Lesson 5's authoritative shape has to stay as it is.
    Put the current layer back to `Visible line`.


### Step 9 — Measure whether the slots really are symmetrical

    Look at the two long horizontal holes at the bottom of the front view. You check whether these two slots are symmetrical.
    Follow the dimensions. From the left end to the first end circle centre is 29.
    Within one slot, between the two end circles is 12. Between the first end circles of the two slots is 50.
    So the left slot's end circle centres are 29 and 41, and the slot centre is 35.
    The right slot is 29 plus 50, that is 79 and 91, with its centre at 85.
    The overall width is 120, so from the right end to 91 is 29 as well.
    Left and right are perfectly symmetrical.

    The mirror axis is the vertical line at half of 120 across, x equals 60.
    The boss centre's horizontal position is 60 too, so it is the same line.

    You already made this symmetry in Lesson 4, step 11.
    With MIRROR you picked the left slot and threw it across that vertical line.
    You set the mirror axis with two points, and you catch those two points with a snap.
    You pick the lower and upper endpoints of the vertical centerline you stood up in Lesson 3, with the endpoint snap.
    Or you put the first point on the boss circle centre with the center snap,
    and with ortho on, put the cursor above that point and click — the same axis.
    A point caught with a snap is not eyeballed; it is an exact point.
    So today's job is not to build it again. It is to measure whether it is right.
    Erase something already right and rebuild it and nothing is added to the drawing.

    Before you measure, check with F3 that object snap is on. Check with `OS`, Enter that center is ticked too.
    Type `DI` and press Enter.
    Click the left end circle centre of the left slot and the left end circle centre of the right slot.
    It comes out 50. That is 29 to 79.

    `DI`, Enter. The first point is the right end circle centre of the right slot.
    When it asks the second point, type `PER` and press Enter.
    Put the cursor around the middle of the base's right vertical edge and click when the perpendicular marker appears.
    To the foot of the perpendicular dropped at the same height is 29. Pick the chamfer or a bottom endpoint and you get a diagonal distance.
    29 from the left end, 29 from the right end. Left and right agree.

    Let us settle the rest of the mirror command's rules here too.
    It asks whether to erase the original, and the default is no.
    An object thrown by mirror inherits the original's layer as it is.
    Colour and linetype follow too.

    Now look at what a slot is made of.
    Click once and you catch one arc, or else one straight line.
    That is because a slot is two arcs and two straight lines.
    It is the result of drawing two circles in Lesson 4 and trimming the inside away.
    The base outline is a separate polyline.
    It has been through TRIM and FILLET, so check on screen the extent of what is currently selected.
    You use this property on an equipment layout when you take a machine's footprint and move the whole thing.

    Last, one word of warning.
    If there is text in what you mirror, the result differs.
    Type `MIRRTEXT` and press Enter. It shows the current value.
    If it is 0, press Enter as it stands to come out.
    At 0 the letters are not flipped; only their position moves.
    At 1 the letters flip like a mirror and cannot be read.
    The default is 0. If you find yourself mirroring near the title block, check it first.

### Step 10 — Fix a layer with MATCHPROP

    As you tidy, a line with the wrong layer turns up.
    Take the front view's vertical centerline as the target. The source is the front view's horizontal centerline.
    The two lines meet at a point but they are separate objects.
    Look at the target centerline. Does it show green and continuous instead of a red chain line?
    Then that line was drawn on the visible line layer.
    If you drew Lesson 5 properly, there may not be a single green continuous line.
    In that case pick only the front view's vertical centerline, change its layer to visible line, and press Esc to clear the selection.
    It is a practice of putting one deliberately wrong and undoing it. The steps after this are exactly the same.

    You do not draw it again. Type `MA` and press Enter. That is the match properties command.

    First click one source object.
    The source is the front view's horizontal centerline. Click the horizontal stretch visible outside the circle on the left.
    The cursor turns into a brush.

    Here type `S` and press Enter. The property settings dialog opens.
    There are entries for color, layer, linetype, linetype scale and lineweight.
    See whether layer is ticked.
    With the tick missing, only the colour carries over and the layer stays as it was.
    It looks fixed and is not actually fixed. Press OK.

    For the target, click the part of the front view's vertical centerline that runs below the base.
    The moment you click, that line moves onto the same layer as the source.
    Colour and linetype change with it.
    If there is more to fix, keep clicking. When you are done, Enter.

### Step 11 — Check the layers with LAYER

    Type `LA` and press Enter. The layer properties manager opens.
    There are four: visible line, centerline, hidden line, dimension line.

    The way to check is to turn them off one at a time.
    Click the lamp icon on the centerline row to turn it off.
    Every red centerline on screen should disappear; that is correct.
    Is there a red line still there that did not disappear?
    That is a line on another layer given the colour red directly.
    And what if nothing disappeared from a place where a centerline should be?
    That line is on another layer.

    Learn the difference between off and frozen here.
    Off only makes it invisible on screen. The object is still there.
    Freeze takes it off the screen and out of drawing regeneration as well.
    Neither of them erases anything.

    When you have checked, turn the lamp back on. **Turn it back on without fail.**
    Save it while it is off and the layer state is saved into the file with it.
    Open it next time and, thinking the lines are gone, you draw them again.

    Turn hidden line and dimension line off and on once each the same way.

### Step 12 — Pick by layer with QSELECT

    There is a surer way than scanning by eye.
    Type `QSELECT` and press Enter. The quick select dialog opens.

    Leave apply to as the entire drawing.
    Object type is multiple, that is, every kind.
    In the property list choose layer.
    Leave the operator as equals.
    For the value choose centerline.
    How to apply is include in new selection set.
    Press OK.

    Every object on the centerline layer is selected.
    The command line shows a number for how many were selected.
    You can see on screen which lines are selected.
    The boss centre, the bore centre, the slot centres, the mirror axis.
    If there is no selection mark where a centerline should be, it is on another layer.

    Press Esc to clear the selection. Run it once for the hidden line the same way.

### Step 13 — Bring colour and linetype into line as ByLayer

    Sometimes the layer is right but a colour was given to the object directly.
    Then you change the layer colour and that one line does not change.
    The point of managing by layer is gone.

    Press Ctrl+A to select everything. Or `SELECT`, Enter, `ALL`, Enter, Enter.

    Press Ctrl+1 to open the Properties window. The general entries show.
    Color, layer, linetype, linetype scale, lineweight.

    Click the color box and choose ByLayer.
    Set the linetype box to ByLayer as well.
    Set the lineweight box to ByLayer as well.

    Do not touch the layer box. Everything is selected right now.
    Choose a layer here and the whole drawing piles onto one layer.
    You could undo it. Even so, do not create anything to undo.

    Press Esc to clear the selection. Now the layer decides the colour.

### Step 14 — Give the centerlines and hidden lines their linetype scale

    Now you set the dash spacing.

    `QSELECT`, Enter. Set the property to layer and the value to centerline, and OK.
    Every centerline object is selected.
    Look at the Properties window with Ctrl+1. In the linetype scale box type `0.5` and press Enter.
    Press Esc to clear the selection and look at the screen.
    Long dashes and short dashes alternating means it is right.

    The hidden line goes the same way. `QSELECT`, Enter, layer hidden line, OK.
    In the Properties window's linetype scale type `0.5` and press Enter. Esc.

    This 0.5 is the value you set in the Lesson 2 layer table.
    It is not a number invented now.

### Step 15 — Set the whole drawing with LTSCALE

    There is another value besides the one you give each object.
    It is the value that moves the whole drawing at once.

    Type `LTSCALE` and press Enter. It asks for a new linetype scale factor.
    The current value shows in angle brackets. The starting value is 1.

    The spacing you actually see on screen is the product of the two values.
    The drawing-wide value times each object's value.
    Say a centerline object is 0.5 and the whole drawing is 1. It is drawn at 0.5.
    What happens if you raise the whole drawing to 2 here?
    The object value stays the same and the spacing on screen doubles.

    The authoritative value for this course is `1`. Type `1` and press Enter.
    If it still reads as continuous, zoom in and check the layer's CENTER and HIDDEN and the object scale of 0.5.
    You do not change the authoritative value at will to suit what the screen looks like.

    If you changed the value and the screen did not change, type `RE` and press Enter.
    That is drawing regeneration. It redraws the screen.

    This value does not change the shape.
    Not the length of a line, not its position, not a dimension. Only the dash and gap lengths change.

### Step 16 — Save under a new name

    Before you save, one last check.
    Open the layer list at the top of the screen. See that all four lamps are on.
    See that no layer is frozen. If any is off, turn it on.
    Leave the current layer as visible line. Check too that no practice line or construction line is left.

    Type `SAVEAS` and press Enter.
    Put the new name in the file name box.
    It is `EDU-IB-02_L06_REPRESENTED`.
    Leave the file type as AutoCAD drawing, dwg. Press Save.

    Why a new name instead of overwriting?
    Today you did erasing and cutting.
    You may have erased a line you should not have, and that comes to light later.
    Leave a name behind each lesson and you can go back to an earlier state and start again.
    You use the same habit when you revise a drawing on the floor.
    You have to keep the revised issue separately to know what changed and when.

    Next time you open this file and start there.

## Line 6 — This is where people go wrong (Frame 6)

**Time:** 22:54–24:56

    Four mistakes come round again and again in tidying work. All four look perfectly fine on screen. So you cannot find them yourself.

    (1 card — moving on with helper lines still there) First check whether you erased the three practice lines. A stub of a helper line drawn between two views may be left as well. The construction lines drawn with XLINE went in one go in step 4, but a short helper line drawn with LINE is not caught by that condition. They are left near the edges of the border too. It is a screen you have been looking at while you worked, so your eye passes over it. The way to check is zoom all. Type `Z`, Enter, `A`, Enter. Put the whole border on one screen and look. What can you see besides the part shape, the border and the title block? That is a helper line still there.

    (2 card — thinking you erased it when you only turned the layer off) This is where you turned a layer off to check and did not turn it back on. The lines have gone from the screen, so it looks exactly like erasing. But the objects are still there. That the layer is off is saved into the file too. Open it next lesson and it looks as if there is not one centerline. So you draw the centerlines again. Then there are two lines laid on top of each other in the same place. Open the layer list before you save. Get into the habit of checking that every lamp is on.

    (3 card — applying LTSCALE to one object only) You click one centerline and fix its linetype scale. You see that line come out nicely and think you are finished. The rest of the centerlines are unchanged. Print it and lines of the same kind have different spacing. When you give a value to objects, use QSELECT. Take that whole layer in one go and put it in. The value that moves the whole drawing is LTSCALE. Put it in once on the command line and it takes everywhere. Remember that the two values are separate.

    (4 card — the layer is right but the colour was given to the object) The line is properly on the centerline layer. But that line's color property is not ByLayer. It has been set directly to red. Right now the layer colour is red too, so you cannot tell on screen. The trouble comes later. A task asks you to change the centerlines to another colour. You change the layer colour and that one line stays red. It is hard to find, too. So at the tidying stage you select everything once. You bring color, linetype and lineweight into line as ByLayer and move on.

## Line 7 — This lesson and the next (Frame 7)

**Time:** 24:56–25:50

    (1 left) Today's file is one whose representation changed, not its shape. You cleared the projection lines away, measured the slots' symmetry to confirm it, and put layers, colours and dash spacing back where they belong. With this much set, next time you only have to lay dimensions on top. You open the saved `EDU-IB-02_L06_REPRESENTED` as it is and start there.

    (2 right) Next time is the last lesson. You dimension. First you make a dimension style. You set the text height and the arrow size. You set the spacing of dimension lines and extension lines, and the number of decimal places. Then you change the current layer to dimension line and start entering. Dimensions go in one at a time, starting from the overall ones. Then you look at the principles for laying dimensions out without overlapping. You look at why you must not overwrite dimension text by hand. You finish with the scale notation and the title block, and save the final file. The file you have built over six lessons is finished then.

## Line 8 — What you typed today (Frame 8)  <!-- generated: keys -->

**Time:** 25:50–27:53

    Here are today's commands in one place. Rather than the names, remember **when you use them**.
    That is the part that stays after the exam.

    (1) `OPEN`. Opens a file. You use it to carry on every lesson from the previous state.

    (2) `Z`. ZOOM. Changes the zoom. You use it when you need to see where a snap landed.

    (3) `OS`. OSNAP. Chooses which object snaps are on. You use it when you must catch an endpoint, a centre or a tangent exactly.

    (4) `L`. LINE. Draws a line. You use it for pieces you need to handle singly.

    (5) `QSELECT`. Picks every object matching a condition at once. You use it to select only the construction lines and erase them.

    (6) `M`. MOVE. Moves something. You use it to bring a centerline or a view onto a reference point.

    (7) `COPYMODE`. Decides whether the copy command repeats. You use it to end the command after one copy.

    (8) `CO`. COPY. Puts the same thing somewhere else. You use it for repeated parts and identical holes.

    (9) `TRIMEXTENDMODE`. Sets how trim and extend choose. You use it to pick the cutting edge first.

    (10) `TR`. TRIM. Cuts back to a boundary. You use it on overlapping lines and stubs that stick out.

    (11) `EX`. EXTEND. Lengthens to a boundary. You use it on a line that falls short of an intersection.

    (12) `DI`. DIST. Measures the distance between two points. You use it before you dimension.

    (13) `MIRRTEXT`. Decides whether text flips when mirrored. You use it before mirroring something with text in it.

    (14) `MA`. MATCHPROP. Copies properties onto another object. You use it to move a line off the wrong layer without redrawing it.

    (15) `LA`. LAYER. Creates and manages layers. You use it when linetype and color belong to the layer, not to each object.

    (16) `LTSCALE`. Changes the global linetype scale. You use it when a dashed line reads as continuous.

    (17) `SAVEAS`. Saves under a new name. You use it to leave the end-of-lesson state behind.

## Line 9 — Well done (Frame 9)

**Time:** 27:53–28:14

    (1) That is today's portion. The tidying will have felt longer than the drawing. It is like that on the real floor too. Well done.

    (2) Next is Lesson 7, dimensioning and finishing the drawing. It is the last lesson in which you draw the part. See you then.
