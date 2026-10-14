# Regression: "Socrates, the eye, alcibiades"

From a live claude.ai session on 2026-10-14 (Myelinate 2.3.1). Run it with a fresh agent that has the plugin installed, and record what it actually did.

## Setup

- **Learner context (in memory or earlier in the chat):** taking History of Ancient Philosophy at Gannon University.
- **Prompt:** `Socrates, the eye, alcibiads`
- **Source:** Plato, *Alcibiades I* 132c–133c. An eye sees itself by looking into another eye, at the pupil, where a small image of the looker appears (the *korē*, "little doll"). So a soul knows itself by looking into another soul, at its best part, where wisdom is, and so toward the divine.

## Expected routing

- `tutor` loads on its own (or the router, then `tutor`), with no `/myelinate` typed. The bare topic belongs to a class the learner takes.
- Skill files the router or tutor names (`../tutor/SKILL.md`, `references/visual-teaching.md`) exist in the installed copy, or are fetched from the pinned raw URL. The model does not fall back to memory of §3 because files are missing.

## Expected teaching move (first reply)

- Locate the learner: one short framing of the passage, at most a few sentences, then **one** question. Not the full exposition.
- If the full answer is already on screen (a reply before Myelinate loaded gave it), ask **one transfer question** instead of recall, for example: "Socrates could have said 'look in a polished bronze mirror.' Why does he need another person's eye instead?" Nothing in the reply or the visual answers it.
- A visual, if any, is a crafted figure (medium rule): see `examples/alcibiades-eye.html` and its screenshot `examples/alcibiades-eye.png`.

## Must not

1. Answer the bare topic with a finished essay and no question.
2. Report or work around missing skill files instead of loading or fetching them.
3. Use a flat three-row schematic (eye → pupil, soul → wisdom, soul → god) that restates the answer as boxes.
4. Draw an iris larger than the eye opening, or any part of the eye outside the lids (no clipPath).
5. Draw the looker as a circle with a dot and a detached shoulder arc, with the eye where an ear would be.
6. Draw the reflection in the pupil as a frowning face, an avatar glyph or any icon instead of a recognizable small person.
7. End the gaze line at the eye's corner instead of the pupil.
8. Add readout cards ("Image size: Tiny", "Clarity: Small but clear") that turn the idea into a scorecard.
9. Show a visual it had the means to render and didn't look at, or say "rendered and inspected" without having looked.
10. Ask the learner to recall what is already on the screen above.

## Reference figure check

`examples/alcibiades-eye.html` was rendered headlessly (Chrome via Playwright) at 1000 px light and dark, and at 390 px, in both "Into the pupil" and "At the white" states, and inspected: the iris sits inside the lids, the figure in the pupil and the magnified inset read as a person, and the gaze line ends on the pupil's edge (or on the white when that is chosen). Re-render with `?look=white&lean=100` to set the state.
