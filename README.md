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

## Guardrails

The repository uses three layers of protection:

1. `.gitignore` excludes presentation, AutoCAD, image/media, font, archive, and private working paths.
2. A pre-commit hook blocks prohibited files even when they were force-added.
3. GitHub Actions scans every push and pull request.

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

## AutoCAD Technician course

The course is organized as ten connected HyperFrames projects under
`projects/autocad-technician/`. Every lesson advances the same synthetic
`EDU-SB-01` sensor-mounting bracket from exam-brief analysis to an A3 third-angle
release drawing. Each lesson owns its brief, narration script, storyboard, six scene
compositions, motion assertions, and final assembly.

The sanitized curriculum and production contract are documented in
`projects/autocad-technician/COURSE_PLAN.md`. The canonical part, paper, template,
layer, projection, checkpoint, and exam-disclosure rules live in
`projects/autocad-technician/MASTER_DRAWING_SPEC.md` and
`projects/autocad-technician/course-continuity.json`; the reproducible coordinates and
feature-clearance contract live in `projects/autocad-technician/master-part-geometry.json`.
The 29 screen-recording slots and their exact frame sources are locked in
`projects/autocad-technician/recording-map.json`.
All lessons inherit the LG technical-training visual system. Selected QA snapshots
rendered solely from the public synthetic scenes are tracked as review evidence.
Drawings, recordings, narration, transcripts, presentation sources and direct slide
derivatives remain private.

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
