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
- explicitly reviewed public references listed in `docs/autocad-technician/README.md`.

Do not commit a file merely because it was derived from a private source. Slide renders, copied text, transcripts, PDFs, screenshots, and video frames require the same confidentiality review as the source. Raster/vector image files and embedded image data are blocked by default; an exception requires a deliberate guard change and confidentiality review.

Narration recordings and the Whisper transcripts produced from them stay private.
Transcript and caption paths are blocked unconditionally and cannot be bypassed by
the approved artifact manifest. Scene timing measured from a recording may be
published only as a numbers-only derivative such as `narration-timing.json`, which
carries scene identifiers, start and end seconds, and cue keys, and never carries
spoken text.

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

## AutoCAD Technician course

The course is organized as eight connected HyperFrames projects under
`projects/autocad-technician/`. Seven of them advance the same synthetic
`EDU-IB-02` idler pulley bracket from orientation to an A3 third-angle release
drawing; the eighth covers the exam briefing and its questions. Each lesson owns
its brief, narration script, storyboard, six to eleven scene compositions, motion
assertions, and final assembly, and the eight lessons are cut into 19 episodes of
at most twenty minutes each.

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
through 7, cut into 15 pieces so that no episode runs past twenty minutes.
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
