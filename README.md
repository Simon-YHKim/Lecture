# Lecture

Public automation, templates, and sanitized documentation for producing the AutoCAD technician video course.

## Confidentiality boundary

This is a public repository. Original presentation decks, AutoCAD drawings, speaker notes, exports, recordings, captions, archives, and other private course materials must remain outside the repository. Store them only in an approved private location outside this repository, and do not publish its absolute local path.

Only the following belong here:

- production code and reusable templates;
- documentation reviewed for public release;
- synthetic training diagrams authored as inline SVG inside reviewed HTML;
- validation scripts and CI configuration.
- reviewed HyperFrames QA snapshots rendered from the public synthetic course scenes;
- explicitly reviewed public references listed in `docs/autocad-technician/README.md`;
- the `EDU-IB-02` bracket model under `model/`, which the course author built and cleared for publication.

Do not commit a file merely because it was derived from a private source. Slide renders, copied text, transcripts, PDFs, screenshots, and video frames require the same confidentiality review as the source. Raster/vector image files, 3D CAD sources, and embedded image data are blocked by default; an exception requires a deliberate guard change and confidentiality review.

The bracket model is such an exception, and it is the only one. Its four files
ride the same path-and-hash allowlist as the other public artifacts, so renaming
or editing one blocks the commit until
`scripts/update-public-artifact-manifest.ps1` is run again and the change is
reviewed. Any other Inventor, SolidWorks or neutral-exchange file is blocked on
sight.

Narration recordings and the Whisper transcripts produced from them stay private.
Transcript and caption paths are blocked unconditionally and cannot be bypassed by
the approved artifact manifest. Scene timing measured from a recording may be
published only as a numbers-only derivative such as `narration-timing.json`, which
carries scene identifiers, start and end seconds, and cue keys, and never carries
spoken text.

### Approved release downloads

On 2026-09-10 the course author authorized completed lecture videos and self-study
files to be distributed through GitHub Releases after the work is complete and
merged. Reviewed delivery files may be attached to a release with a file manifest
and SHA-256 checksums. This does not add media to Git history or authorize bulk
publication of original materials, separate narration WAVs, transcripts or font
binaries. The latest delivery scope and remaining work are recorded in
[`docs/HANDOFF.md`](docs/HANDOFF.md).

The first preview contains five videos, the eight-lesson self-study package and
one offline review HTML. It preserves the earlier episode layout and voice speed.
The current revision targets **AutoCAD 2024**, **one video per lesson** and
**1.38× narration**, without starter files. Grading and exam operations remain
to be shared; only the two help contacts' names are disclosed. Complete the
Korean edition before producing English self-study, slides, scripts and videos.
Lessons 2–7 still require real AutoCAD recordings. Do not treat the first preview
as a completed delivery of this revision or replace its files silently.

The AutoCAD 2024 revision prepares Korean self-study, lesson slides and scripts
for all eight lessons. Only lessons 1 and 8 have complete integrated MP4s at
this stage; lessons 2–7 require real AutoCAD 2024 recordings and application
validation. Catalog durations describe the measured narration timeline, not
guaranteed hands-on completion time. English text already present in the
workbook is a draft, not a completed English course.

- [First preview release](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.10-preview.1)
- Download `AutoCAD_Review_20260910.html` and open it in a browser. Press **M**
  for slide, element or common notes, **N** to edit the script, and **P** to
  preview animation. This review file has no narration audio.
- Use **Markdown 복사** or **메모 파일 받기** to return feedback. **백업 받기**
  saves notes and script edits as JSON; **백업 불러오기** restores them into
  the same edition. Records are stored in the browser, not inside the HTML,
  and do not sync automatically. Keep the backup when changing computers.
- The review generator supports offline export with
  `python scripts/selfstudy/build_deck_all.py <output.html> <temporary-directory> --standalone <gsap.min.js>`.
  Review transfer regression checks: `node --test scripts/selfstudy/test_review_transfer.cjs`.

Build the English edition by setting `SELFSTUDY_LANG=en`. It takes the English
drawing (`edu_ib_02.py --lang en`) and shows English first. English labels run
longer than Korean, so measure them before shipping: `python
scripts/selfstudy/figure_sheet.py <out.html> en` lays every authored figure on
one page, which a browser can measure for text leaving its viewBox or colliding
with another label. Tabs hide figures inside the workbook, so measuring there
silently skips most of them.

New review editions have different slide and content identifiers. Keep the old
review HTML with its feedback backup; importing old feedback into a revised deck
is deliberately rejected to avoid attaching notes to the wrong slide.

Recording intake preserves the existing narration bindings. Private lecture
preparation verifies and copies registered recordings, retains the authored
overlays, and rejects changed media or a duration differing from its measured
slot by more than one source frame. It does not trim or retime recordings.
See [the recording guide](projects/autocad-technician/RECORDING_GUIDE.md) before
registering takes. The first preview assets remain a fixed review edition;
follow-up source corrections do not replace those downloads automatically.

## Guardrails

The repository uses three layers of protection:

1. `.gitignore` excludes presentation, AutoCAD, image/media, font, archive, and private working paths.
2. A pre-commit hook blocks prohibited files even when they were force-added.
3. GitHub Actions scans every push and pull request.

`.gitattributes` disables end-of-line translation for every tracked file. The
approved artifact manifest binds each reviewed asset to the exact byte count and
SHA-256 of its repository bytes, so a checkout that rewrote line endings would
fail manifest validation and block every manifest-bound artifact. Do not enable
end-of-line translation for this repository.

GitHub Actions is a secondary detection and merge gate; it cannot retract a blob
that has already reached a public remote. Run the local staged guard before every
push. If private material is ever published, follow the incident process to restrict
access, rotate exposed credentials, and purge the affected Git history—reverting the
tip alone is not sufficient.

Enable the repository hook after cloning:

```bash
git config core.hooksPath .githooks
```

Run the checks manually:

```powershell
./scripts/test-private-materials-guard.ps1
./scripts/check-private-materials.ps1 -Mode all
./scripts/check-course-projects.ps1
```

Add `-RunHyperFramesChecks` to run every lesson's pinned HyperFrames validation in sequence:

```powershell
./scripts/check-course-projects.ps1 -RunHyperFramesChecks
```

The course guard also enforces the shared `FRAME_STANDARD.md`, canonical non-overlapping
geometry from `master-part-geometry.json`, exact scene continuity,
Storyboard/HTML/Motion duration parity, registered timeline keys, the declared number
of `USER RECORDING` cues, and the cumulative checkpoint chain for every lesson.

## Narration timing

`frame.md` makes the recorded Korean narration the master timeline, and requires
emphasis animation to lead its narration keyword. Both rules need measured word
times, so the tracked scene durations stay planning values until a recording
exists.

Two scripts close that gap. Create the local Python environment once from the
repository root:

```powershell
py -3.12 -m venv .venv
./.venv/Scripts/python.exe -m pip install faster-whisper
```

Then transcribe the recording and derive its timing:

```powershell
./scripts/transcribe-narration.ps1 -AudioPath <recording> -TranscriptPath <private-output>
./scripts/build-narration-timing.ps1 -LessonPath projects/autocad-technician/lesson-03-baseline-profile -TranscriptPath <private-output>
```

The transcript is private and the first script refuses to write one inside this
repository. Only `narration-timing.json` is publishable: frame identifiers,
measured start and end seconds, drift against the planned window, alignment
confidence, and recording-cue times, with no spoken text. The second script
verifies that before it returns.

Speech recognition supplies only the clock. Canonical identifiers such as
`EDU-IB-02`, `L02_TEMPLATE`, and `L07_RELEASE` cannot be recovered from
audio, because an underscore has no sound, so the words come from `SCRIPT.md` and
the two are aligned character by character. A frame dense in Layer names aligns
less tightly; its `matchedRatio` records that rather than hiding it.

Recognition is not bit-reproducible: two runs over the same recording can place a
scene boundary a few seconds apart. Treat `narration-timing.json` the way the
artifact manifest is treated. Generate it once, review the drift, commit it, and
regenerate only when the recording itself changes. Do not rebuild it in CI.

### Local Heami synthesis

For the current lecture workflow, synthesize the revised script with Windows
SAPI **Microsoft Heami Desktop, Rate 0**, then process the speech at **1.38×**
with pitch preserved and measure the resulting WAVs. SAPI Rate and playback
speed are separate settings. Refresh the complete lesson's clock:

```powershell
python scripts/part/narrate_tts.py projects/autocad-technician/lesson-01-orientation --tempo 1.38 --out <fresh-private-audio-directory>
python scripts/part/retime_frames.py projects/autocad-technician/lesson-01-orientation
python scripts/part/prepare_lecture.py projects/autocad-technician/lesson-01-orientation --out <fresh-private-render-directory> --gsap <local-gsap.min.js>
```

When practice step headings or command labels change, run
`python scripts/part/refresh_recording_labels.py <lesson-directory>` before
preparing the render. This keeps the authored scene and its measured timing while
refreshing the recording captions from `SCRIPT.md`.

Both output directories must be outside Git and new for this generation. Use the
local GSAP 3.14.2 distributable to match the authored compositions. The export
includes private WAV files and must remain private. Run the pinned HyperFrames
check and render commands from that exported project. `prepare_lecture.py`
aggregates scene motion assertions into `index.motion.json`, because the CLI
reads a sidecar only at the project root. For long lessons, the 0.8.33 CLI caps
motion sampling at 300 points; use `prepare_scene_checks.py <private-project>
--out <fresh-private-check-directory>` to check the unchanged scenes on their
own clocks. It preserves every original assertion and adds a short entrance
check, including bounds, where full-scene sampling is too sparse. Run
`hyperframes@0.8.33 check <scene-project> --json --at-transitions` for each entry
in its manifest. These checks are sampled verification, not continuous proof.
The static linter also pools audio from independent episode files; verify each
playlist on its own clock before interpreting overlap warnings.
Missing AutoCAD recordings block a delivery export. `--preview` permits those
placeholders only for validation and records them in the private export manifest.

Export the entire lesson with the command above. Internal recording parts join
the same lesson; they are not separate public episodes. The old `ep*.html` files
remain as production history and are excluded from the current delivery path.
A lesson that still has a recording placeholder cannot be exported for delivery.
`--preview` is a private validation aid and must not be published as a finished
AutoCAD lesson.

If a long render fails the temporary-disk capacity check, use the CLI's
`--low-memory-mode` streaming profile. It uses one screenshot worker and may
take longer. Keep the same resolution and frame rate, and verify the resulting
video and audio rather than treating a successful render as complete validation.

The synthesis records script/step/frame identity and each WAV's SHA-256. Editing
spoken text or step boundaries requires new speech; editorial time headers do
not. Legacy timing files without these identities cannot be reused by retiming
or export. WAV contents and durations are checked again when preparing a render.
Each lesson uses one clock, including the holds between scene WAVs.
Timing updates are prepared in a temporary copy before replacing source files.
The extended recap lists in lessons 2–8 have one measured paragraph per panel,
so their bullets appear together. Their motion checks include the last bullet
to catch delayed or missing content. Title outros follow the measured clip
length; on short titles, late entrances move earlier to leave at least two
seconds of reading time.
Reference-table rows keep their text fully opaque before and after narration;
the active row's background carries the emphasis. This preserves small labels
that became hard to read when the whole row was dimmed. Other cards and notes
keep their authored states, and explicit `read=0` still clears stacked panels.

If Python is not on PATH, pass its executable to the course guard with
`-PythonPath`, or set `LECTURE_PYTHON`. The course guard reports legacy narration
as pending; a course structure pass alone does not verify its private audio.

`scripts/selfstudy/rhythm_report.py` reports formal/informal balance, repeated
final words, and ending diversity in fixed 20-sentence windows. Its global
unique-ending ratio decreases as documents grow; use it as an editorial signal,
not a pass/fail score for an entire textbook.

## AutoCAD Technician course

The course is organized as eight connected HyperFrames projects under
`projects/autocad-technician/`. Seven of them advance the same synthetic
`EDU-IB-02` idler pulley bracket from orientation to an A3 third-angle release
drawing; the eighth covers the exam briefing and its questions. Each lesson owns
its brief, narration script, storyboard, six to eleven scene compositions, motion
assertions, and final assembly. Each of the eight lessons is delivered as one
video; there is no twenty-minute delivery limit or episode subdivision.

The earlier ten-lesson arrangement is kept under
`projects/autocad-technician/_archive/`. It is not built and not checked.

The sanitized curriculum and production contract are documented in
`projects/autocad-technician/COURSE_PLAN.md`. The canonical part, paper, template,
layer, projection, checkpoint, and exam-disclosure rules live in
`projects/autocad-technician/MASTER_DRAWING_SPEC.md` and
`projects/autocad-technician/course-continuity.json`; the reproducible coordinates and
feature-clearance contract live in `projects/autocad-technician/master-part-geometry.json`.
The screen-recording sections and their exact frame sources are locked in
`projects/autocad-technician/recording-map.json`: one section in each of lessons 2
through 7, with 15 internal recording parts retained at practice boundaries.
These parts preserve the recording and narration mapping inside each whole lesson.
All lessons inherit the LG technical-training visual system.
Drawings, recordings, narration, transcripts, presentation sources and direct slide
derivatives remain private.

A self-study edition of the same eight lessons, in Korean and English on one page
each, is published under `docs/autocad-technician/self-study/` and generated by
`scripts/selfstudy/`.

Public HTML resolves installed LG EI families with CSS `local()` and falls back to
`Malgun Gothic`; it contains no private font URL or filesystem path. Font binaries
and their locations remain ignored/private because no redistribution license is
included.

The reviewed public package, including the course MasterPlan, A3 landscape template
reference, QA snapshots, and bilingual completion report, is indexed in
[`docs/autocad-technician/README.md`](docs/autocad-technician/README.md).

## Publishing checklist

Before pushing a course-related change:

- confirm no original deck, drawing, note, recording, transcript, or archive is staged;
- review images and HTML for copied slide content, company identifiers, drawing numbers, equipment names, dimensions, user names, and local paths;
- use synthetic examples unless a sanitized asset has been explicitly approved;
- inspect `git diff --cached --name-only` and run the guard manually.
