---
description: "Start my spaced review of what's due today, retrieval first."
---

Run a spaced review session for the learner. $ARGUMENTS

Use the Myelinate `tutor` skill. The record format is in the tutor skill's `references/learner-record.md` (in Claude Code: `${CLAUDE_PLUGIN_ROOT}/skills/tutor/references/learner-record.md`).

1. Find what's due: their learner record (`~/.myelinate/learner.json`, if it exists and you can read files), then platform memory. If nothing is recorded, ask in one line what they're studying and when the exam is.
2. Start with retrieval on the most overdue target: one question, no review of the material first. Fresh items, not the ones they saw last time.
3. Verdict from your own key; hinted or revealed answers don't count as independent.
4. Move through due targets, a few items each, interleaved. Teach only what they miss.
5. Close with their recall, honest states, and the next review dates. Update the record if they keep one, and say in one line what changed.
