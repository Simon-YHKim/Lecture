# Lecture

Public automation, templates, and sanitized documentation for producing the AutoCAD technician video course.

## Confidentiality boundary

This is a public repository. Original presentation decks, AutoCAD drawings, speaker notes, exports, recordings, captions, archives, and other private course materials must remain outside the repository. A separate local directory such as `C:\Lecture_Private` should be used for those files.

Only the following belong here:

- production code and reusable templates;
- documentation reviewed for public release;
- synthetic or explicitly approved training assets;
- validation scripts and CI configuration.

Do not commit a file merely because it was derived from a private source. Slide renders, copied text, transcripts, PDFs, screenshots, and video frames require the same confidentiality review as the source.

## Guardrails

The repository uses three layers of protection:

1. `.gitignore` excludes presentation, AutoCAD, media, archive, and private working paths.
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
```

## Publishing checklist

Before pushing a course-related change:

- confirm no original deck, drawing, note, recording, transcript, or archive is staged;
- review images and HTML for copied slide content, company identifiers, drawing numbers, equipment names, dimensions, user names, and local paths;
- use synthetic examples unless a sanitized asset has been explicitly approved;
- inspect `git diff --cached --name-only` and run the guard manually.
