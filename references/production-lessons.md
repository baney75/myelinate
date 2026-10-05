# Production lessons for course study packs

Lessons from building a multi-part exam study pack with practice, figures, and narration. Each rule names the failure it prevents. Apply the ones that fit the artifact; a short chat lesson needs few of them.

## Confirm the assessment boundary first

Find the official study guide, review sheet, or instructor scope statement **before** drafting lessons. Lectures and textbook chapters overrun exam scope, and material for the next exam often sits in the same folder. In one build, lessons were drafted from lectures before the guide surfaced, and a chapter belonging to the following exam was nearly included.

- Record the scope source, its date or version, and the exact boundary (chapters, lectures, sections).
- If no official scope exists, say so and label coverage as inferred. Ask before including adjacent material.
- While the guide is missing, keep drafting small and provisional (one section, not the whole pack) so less work is at risk.
- When a guide appears mid-build, re-check every drafted lesson against it rather than patching forward.

## Map every objective to sources and questions

Keep a coverage map: **guide bullet → source page/slide → explanation → practice item(s)**. Every guide bullet gets at least one practice item and at least one explanation. Count from the guide, not from the question bank. An earlier build had 42 items yet left many guide bullets untested, and one mechanism topic had questions but no explanation at all.

- Flag rows with no source, no explanation, or no item before calling the pack complete.
- Weight items toward bullets the guide emphasizes; do not let easy-to-write recall items crowd out mechanisms and applications.
- The map describes the pack's coverage, not the learner's proficiency.

## Weigh the learner's notes honestly

A learner's "notes" may be slide exports with the note sections empty. Check before treating them as independent evidence. If they duplicate the slides, say so plainly and count them once. Do not cite an empty notes file as corroboration, and do not infer what the instructor emphasized from blank space.

## Inspect figures at display size

Render each figure at the size the learner will see it. Check for clipped labels, overlapping callouts, and answer labels that leak into a question.

- When masking labels for a quiz, mask **every** instance: the image itself, duplicated crops, captions, alt text, filenames, nearby text, and any answer-revealing tooltip.
- Keep the text alternative useful without naming answers: describe marker positions ("marker 3, upper right") rather than structures.
- Re-inspect after masking; a mask that covers the label but leaves the alt text gives the answer away to screen-reader users and to anyone who reads the source.

## Treat narration as dependent on text

Audio is derived from text. Any change to the text invalidates its clip.

- Keep a map from a hash of the exact narrated text to its clip. A changed hash means the clip is stale.
- Deduplicate identical prompts deliberately (one clip, several uses), and record that choice so a later edit to one use does not silently change the others.
- An audio-presence check must not block shipping corrected content. Define the fallback in advance: ship the corrected text, mark its audio as pending, and regenerate later. The audio check should report "pending for changed text" as a recorded state and still fail on clips missing for no recorded reason; do not delete or silence the check. Unlink or disable a stale clip so it cannot play; never ship stale audio that contradicts the text.

## Keep evidence inside the project

Store receipts, renders, check output, and source excerpts in the project, not in `/tmp` or another location that disappears. Record which checkout and branch is canonical when more than one copy exists, so later fixes land in the version the learner actually uses. Keep private course material out of public repositories.

## Self-check claims against primary sources

Before delivery, re-read each consequential claim against the primary slide, page, or guide line it cites. Soften wording that is stronger than the source: "is associated with" stays associated, "can" does not become "always," and a single example does not become a rule. Where the course and a reliable outside source differ by convention, show both; where the course is factually wrong or outdated, correct it respectfully with the supporting source.
