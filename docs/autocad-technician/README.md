# AutoCAD Technician public course package

This directory indexes the reviewed public artifacts for the connected ten-lesson
AutoCAD technician course. The course builds one synthetic `EDU-SB-01` bracket from
exam-input analysis through a timed release drawing.

## Public artifacts

- [Course MasterPlan](master-plan/AutoCAD_Technician_Video_Course_MasterPlan_260811.html)
- [A3 landscape template reference](reference/a3-landscape-template-reference.png)
- [Bilingual completion report](reports/AutoCAD_Technician_All_Lessons_Completion_260812.html)
- [Public release completion report](reports/AutoCAD_Technician_Publication_Completion_260814.html)
- [Approved artifact hash manifest](public-artifact-manifest.json)
- 125 reviewed HyperFrames QA images under
  `projects/autocad-technician/lesson-*/snapshots/`
- Course briefs, scripts, storyboards, frame HTML, motion sidecars, canonical
  geometry, continuity contracts, and recording-slot specifications under
  `projects/autocad-technician/`

The supplied paper dimensions are ISO A3. The course therefore uses landscape
`420 × 297 mm`, a 10 mm inset border, and a `200 × 30 mm` title block with two
100 mm cells. Actual exam-provided templates and instructions always override the
training defaults.

## Rebuild the report

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-course-completion-report.ps1 -HyperFramesChecksPassed
```

The report is a self-contained HTML file. Its embedded contact sheets are copies of
the reviewed synthetic QA images already tracked in each lesson.

After intentionally replacing an approved snapshot or reference, review it and then
refresh the path-and-hash allowlist:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\update-public-artifact-manifest.ps1
```

The privacy guard rejects renamed or modified images until the manifest is reviewed
and updated in the same change.

## Confidentiality boundary

The following are intentionally excluded even when their extension is not `.pptx`:

- PPT/PPTX sources, notes, and direct slide-derived images, layouts, and review boards;
- real AutoCAD drawings, recordings, narration, captions, and transcripts;
- LG font binaries, because no redistribution license is included;
- `node_modules`, `.hyperframes`, `.thumbnails`, and other reproducible caches.

The visual method was informed by the linked
[HyperFrames workflow video](https://www.youtube.com/watch?v=RRXFWi06hQg&t=501s).
The video transcript is not copied into this repository.
