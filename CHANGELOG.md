# Changelog

## Unreleased

### Changed

- Align all eight AutoCAD lesson scripts and self-study prose with the course's formal/conversational style balance, and update the self-study video durations.
- Match lesson 3's explanations and command recap to its current snap/distance and rectangle/chamfer workflow.
- Regenerate measured narration timing with Microsoft Heami Desktop, Rate 0, and synchronize frames and 20 episode playlists.
- Pin the active lesson projects and generator to HyperFrames 0.8.33.

### Fixed

- Prevent overlapping recording captions and explanation paragraphs during transitions.
- Bind sparse drawing highlights and mixed sheet/layer explanations to their explicit narration beats.
- Preserve early overview visibility while refreshing narration-driven motion deadlines.
- Show each recap list with its measured spoken paragraph, including bullets previously delayed beyond the end of the clip.
- Keep titles visible through their narration and leave at least two seconds to read all title text before the outro.
- Keep reference-table text readable before and after narration while preserving row background emphasis and all scene timing.
- Reject stale scripts, missing audio identities, changed WAV files, and invalid timing before private lecture export.
- Share SVG definitions once in the combined workbook to avoid duplicate drawing IDs.
- Open lesson tabs within the combined workbook instead of following missing separate-page links.

### Added

- Publishable five-video preview, eight-lesson self-study bundle and a single offline review HTML.
- Markdown feedback download and edition-checked JSON backup/restore for review notes and script edits.
- Preserve script edits while navigating or exporting; focus newly added common notes correctly.

- Private offline lecture preparation and scene-level checks for the CLI's bounded motion sampling.
- Selected-episode lecture export with local timing, complete source/audio validation, and recording checks limited to the selected frames.
- Narration identity, staged-edit, timeline, SVG-definition and sentence-rhythm regression checks.

Actual AutoCAD recordings and original teaching materials remain required for application-level validation and complete practice videos. Generated speech, rendered video and private review artifacts are not included in this repository.
