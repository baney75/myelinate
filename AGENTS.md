# Working on Myelinate

`myelinate.md` is the authored router skill and `skills/<name>/SKILL.md` are its nine sub-skills (teach, tutor, lab, print, flashcards, memory-hooks, study-plan, find-media, verify). `SKILL.md` is the router's generated install entrypoint; after changes run `python3 scripts/check.py --sync` and review both. Keep references conditional and the core usable when pasted alone.

Teach in chat by default. Do not gate explanations behind intake, health disclosure, or a quiz. Ask course learners for their study guide, syllabus, notes, and textbook/edition. Ask what helps and what gets in the way in everyday terms; a learner may share a learning condition if they choose, but it is never required, inferred, or repeated back as a label. Teaching stays honest, not agreeable. Keep learner records, private courses, and diagnostic disclosures out of this repository.

Claims need sources and limits. Never claim forced permanent memory, measured myelination, clinical efficacy, guaranteed grades, or proven efficacy of this package. Hinted/revealed work is not independent success. Reminders require real scheduling support.

Check package integrity with `python3 scripts/check.py`. For behavioral changes, use the relevant cases in `evals/scenarios.md` with a fresh agent, and inspect its response. For demo changes, inspect desktop/mobile renders and exercise answer, invalid input, hint, reveal, and reset. Record exactly what was tested; simulated learners do not establish learning gains.

The router must stay usable alone: its core rules are the minimum standard when sub-skill files are missing. Sub-skills reference each other by name and by `skills/<name>/SKILL.md`. Run `verify`'s adversarial review on substantive teaching changes, and keep `examples/oxygen-lab.html` passing its journey test when the lab engine or template changes. Brand rules live in `assets/brand.md`.

The repo must work when someone simply pastes its URL into any assistant: keep `SKILL.md` self-sufficient, keep `llms.txt` accurate, and keep the fetch URLs in the router valid (tag `v2.0.0` and `main`). Bump the version line in `myelinate.md` and tag a release for behavior changes.
