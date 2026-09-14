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

On 2026-09-14 the course author authorized Korean and English review videos,
integrated scripts, slides and self-study files to be distributed through GitHub
Releases. Reviewed delivery files may be attached to a release with a file manifest
and SHA-256 checksums. This does not add media to Git history or authorize bulk
publication of original materials, separate narration WAVs, transcripts or font
binaries. Subtitles generated from the approved scripts belong in the explicitly
authorized review downloads, outside Git history. The latest delivery scope and remaining work are recorded in
[`docs/HANDOFF.md`](docs/HANDOFF.md).

The current revision targets **AutoCAD 2024**, **eight lessons per language** and
**native 1.00× cloned instructor narration**, without starter files. The measured
video timelines total **211:43 Korean** and **253:27 English**. Grading and exam
operations remain to be shared. Lessons 2–7 contain PREVIEW placeholders for
15 unrecorded AutoCAD demonstrations; hands-on validation and human listening
approval remain pending. A review release is not final instructional signoff.

The review package combines an offline video player, synchronized script,
timestamped feedback export, MP4 subtitles, original scripts, slides and workbooks.
The decks contain **222 Korean / 263 English slides** and all eight original
lesson scripts through **Full lesson script / 차시별 전체 대본**. Presenter notes
on practice slides retain their step-specific guidance. Self-study pages open in
their edition language and retain a saved language preference. Every split page
must remain within 100 KB, including its diagrams and navigation.

### Current review downloads

[2026-09-14 bilingual review release](https://github.com/Simon-YHKim/Lecture/releases/tag/autocad-2026.09.14-review.1) provides all **16 MP4s** and
the integrated review materials. Download the [Korean full ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.14-review.1/AutoCAD_KO_REVIEW.zip),
[English full ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.14-review.1/AutoCAD_EN_REVIEW.zip), or
[materials only ZIP](https://github.com/Simon-YHKim/Lecture/releases/download/autocad-2026.09.14-review.1/AutoCAD_MATERIALS_KO_EN.zip).
Extract the whole ZIP and open `START_REVIEW_KO.html` or `START_REVIEW_EN.html`.
Click the transcript to seek, then export timestamped feedback as JSON.

All 16 videos passed subtitle text/timing roundtrips, full decoding and per-scene
audio/visual comparisons. The release includes a manifest and SHA-256 checksums;
all 28 asset downloads were verified without authentication. It remains a
**review prerelease**: 15 demonstration slots per language are PREVIEW guidance,
and human listening and hands-on AutoCAD signoff remain pending.

### Per-lesson self-study video production

The September 14 release contains lecture-frame videos and one combined self-study
deck per language. It does **not** contain eight separate self-study-slide videos
per language. The September 15 corrective delivery is being produced as **eight
HTML decks plus eight matching MP4s in each language**, 32 core files in total.
Its practice pages use the existing illustrated self-study steps. The videos show
those pages with their own narration; they do not contain AutoCAD screen recordings.

The private production pipeline is:

1. Run `scripts/selfstudy/prepare_narrated.py` with the approved private lesson
   stage, captions and local GSAP script. Set `SELFSTUDY_LANG` to the same language
   as `--lang` before running it.
2. Run `narrated_delivery.py jobs --work <private-work> --lang ko` (or `en`).
   Original slide audio is hash-bound and reused. New slide narration is derived
   from its selected-language text and exact visible action subset. Displayed CAD
   literals remain intact; pronunciation substitutions are separate synthesis input.
   Checkpoint filenames pronounce their letters, leading zeroes and separators
   explicitly; their displayed names remain unchanged.
3. Generate the new jobs with the existing local `scripts/part/speak_clone.py`
   workflow and the generated pronunciation map. Keep voice references, WAVs and
   ASR output private. Use the instructor's native 1.00× voice rate.
4. For each completed lesson, run `narrated_delivery.py assemble`,
   `render_narrated.py capture`, `render_narrated.py render` and
   `verify_narrated.py`, each with `--work <private-work> --lang ko --lesson 1`
   (substitute the required language and lesson).
5. Run `package_narrated.py --work <private-work> --out <new-private-delivery>`
   with `--source-commit <full-sha>` and `--tag <selfstudy-review-tag>` after all
   sixteen videos pass. Packaging creates language ZIPs, 32 individual core
   downloads, an HTML review guide, a public manifest and SHA-256 checksums.
   Publishing is a separate, explicitly authorized operation.

Capture opens the actual offline HyperFrames/GSAP slide player and seeks each
slide to its visible state. FFmpeg holds these stills for measured narration
durations; later emphasis beats from reused lecture frames keep separate shots.
Passing the whole multi-root deck directly to a single-composition renderer would
export only its first slide. New self-study pages are captured after their final
entrance so that all cards and diagrams are visible.

The renderer uses FFmpeg/FFprobe with H.264 NVENC, Playwright Chromium, Pillow,
NumPy and SciPy from the existing local production environment. It exports
1920×1080/30fps H.264/AAC with embedded captions. Verification checks full decoding,
exact subtitle text/timing, source PCM samples and every encoded shot against its
captured slide. These checks do not replace human listening or hands-on validation.
An existing MP4 prevents its deck and script from being silently reassembled;
use a new private revision directory when narration changes.

Each language ZIP opens through `START_REVIEW_KO.html` or `START_REVIEW_EN.html`.
The offline player supports script seeking, matching-slide links and timestamped
feedback export. Packaging selects exact filenames and excludes sample players,
audio references, WAVs, ASR and other private neighboring files.

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

Python regression tests use Python 3.12 and the NumPy version pinned in
`requirements-test.txt`. Install it with `python -m pip install -r
requirements-test.txt` and make `ffmpeg`/`ffprobe` available on PATH. CI installs
these dependencies so synthetic audio and recording tests run instead of failing
or being skipped. No cloned voice model or private recordings are downloaded.

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

### Earlier local Heami synthesis

The earlier local workflow synthesizes a script with Windows
SAPI **Microsoft Heami Desktop, Rate 0**, then processes the speech at **1.38×**
with pitch preserved and measures the resulting WAVs. The current review edition
uses cloned instructor narration at **1.00×**; do not use the earlier Heami
settings to regenerate it. SAPI Rate and playback speed are separate settings.
For the earlier workflow, refresh the complete lesson's clock:

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
Missing AutoCAD recordings block a final delivery export. `--preview` records
every placeholder in the private export manifest. The course author's explicit
2026-09-14 authorization permits labeled review downloads containing those
placeholders, with the missing demonstrations disclosed.

Export the entire lesson with the command above. Internal recording parts join
the same lesson; they are not separate public episodes. The old `ep*.html` files
remain as production history and are excluded from the current delivery path.
A lesson that still has a recording placeholder must not be described as a
finished AutoCAD lesson. The authorized review prerelease retains PREVIEW labels
and keeps hands-on validation and final instructional signoff pending.

The current private render projects use HyperFrames 0.8.36 at 1920×1080, 30 fps,
high quality. Remaining renders use four `beginFrame` workers and streaming encode:
`PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600`,
`HF_DE_PARALLEL_ROUTER=false`, `HF_CAPTURE_PARALLEL_STREAM=true`, and
`PRODUCER_EXPERIMENTAL_FAST_CAPTURE=false`; render options are
`--no-low-memory-mode --gpu --workers 4 --experimental-fast-capture=false`.
This avoids accumulating every frame on disk. Earlier completed experimental
captures are retained only after independent encoded-frame checks.
Canonical project pins remain unchanged. Validate the finished MP4's duration,
subtitle text and timing roundtrips, full decode, and narration alignment.
Compare each encoded scene midpoint with an ordinary browser snapshot as well
as running the source scene checks. Font substitution can move otherwise intact
text; inspect flagged differences and record the exact source and MP4 hashes.
These samples do not replace complete human viewing or listening.

When embedding captions, feed escaped WebVTT to FFmpeg's `mov_text` encoder.
Its SRT decoder treats the literal AutoCAD measurement placeholder `<>` as a
tag and removes it; the VTT decoder preserves it when written as `&lt;&gt;`.
Verify all cue text and millisecond timestamps after extracting the MP4 track.
The review player, embedded MP4 captions, and VTT preserve this notation.
Raw SRT remains available for interchange, but some players hide its angle
brackets. This format difference must not be treated as a script edit.

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
