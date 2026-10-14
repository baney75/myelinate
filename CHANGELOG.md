# Changelog

All notable changes to Myelinate are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as applied to a skill package: a change to teaching behavior bumps the version in `myelinate.md`.

What was actually tested for each version, and its limits, is in [evals/verification.md](evals/verification.md). The behavioral checks are in [evals/scenarios.md](evals/scenarios.md).

## [2.4.0] - 2026-10-14

Myelinate is now one plugin for Claude Code, the Claude apps and Codex, it loads on bare class topics, and its visuals are held to a stricter bar. Driven by a claude.ai session on Plato's *Alcibiades I* that exposed four failures (`evals/regressions/alcibiades-eye.md`).

### Fixed
- **Installed copies missing their files.** The router was registered as the whole repository root (`"skills": ["./"]`), so a host that copies a skill's own folder got `SKILL.md` and nothing else. The router now lives at `skills/myelinate/`, and every skill folder carries a copy of each reference, template and example it names. `scripts/package.py` generates the copies and `dist/myelinate-plugin.zip`; `scripts/check.py` fails on drift or on any referenced path missing from the zip.
- **Missing-file fallback.** The router and every sub-skill say to fetch a missing file from the pinned raw URL, and never to report the gap to the learner or stall on it.
- **Bare class topics.** The router and `tutor` descriptions now trigger on a bare topic from a class the learner takes ("Socrates, the eye"), without widening to tasks.

### Added
- **Plugin for three hosts.** `.claude-plugin` (Claude Code and the Claude apps) and `.codex-plugin` manifests with marketplaces for both. The Claude manifest carries no version, so installs update by commit.
- **`code` skill.** Learn code you have to own: what you need to do with it, a one-picture map, a traced behavior with a prediction first, a run for the verdict, and one `TODO(human)` for the piece that carries the idea. Off for ordinary coding.
- **Myelinate output style** (Claude Code): learn while you code. Claude does the engineering and hands over one decision at a time.
- **Visual rules that stand alone** (router rule 14, `tutor` §3d, `references/visual-teaching.md`): pick the medium by what carries the lesson (a crafted figure or real image when the image itself is the content), clip children to parents, end gaze lines and rays on the target, no icon stand-ins, no scorecards, render and look before sending, and a one-minute checklist. Rule 16 adds "rendered and inspected".
- **When the answer is already on screen** (router rule 1, `tutor` §2a): one transfer or "why this and not that" question instead of a recall quiz.
- **Reference figure** `examples/alcibiades-eye.html` with its rendered screenshot, and the regression case `evals/regressions/alcibiades-eye.md`.

## [2.3.1] - 2026-10-14

Myelinate now loads on its own in long skill lists.

### Fixed
- **Auto-invocation.** Skill listings share a character budget, and once it runs out, long descriptions are dropped and a skill appears by name alone, so it never loads by itself. On claude.ai the 923-character router description was being dropped this way while shorter descriptions in the same list survived. Every description is now 175 characters or less and opens with when to use it, in the words learners type ("teach me", "quiz me", "help me understand", a question from a class).
- **Valid frontmatter.** The router, `teach` and `tutor` descriptions contained `: ` unquoted, which strict YAML parsers reject. All descriptions are now double-quoted.
- **Opt-outs still hold.** The "stay off if opted out" clause moved from the descriptions into the bodies of `teach`, `assess`, `notes`, `flashcards` and `study-plan` (`tutor`, `assignment` and `project` already had it).

### Added
- `scripts/check.py` fails on a description over 175 characters, one that isn't valid YAML, or one that doesn't open with "Use when" or "Use for".
- Trigger scenarios in `evals/scenarios.md`.

## [2.3.0] - 2026-10-11

Myelinate now beats Claude's built-in learning skill in a blind head-to-head on chat tutoring. Version 2.2.1 lost to it (see `evals/verification.md`).

### Added
- **Locate them before you teach** (router rule 1, `tutor` §1, `teach` §5). Fluent field terms set the level, not the format. A beginner missing the concept gets a short direct explanation first. A broad or contested topic gets the shape of help it needs instead of a quiz, and "just lay it out" gets structured exposition with sources.
- **One step forward, every turn.** Each turn has exactly one question and one scaffold. No confidence rating, preference question or intake question is stacked on top, and no turn is questions only.
- **Impatient vs. stuck, early vs. late time claims.** A deadline plus a concrete blocker in the opening message gets a direct answer. A time claim that appears after questioning starts is treated as impatience, and the tutor holds the line more directly.
- **Know when they're done.** After an unaided transfer, the tutor says so, names what they can now do, and points to what comes next, with no new item to answer.
- **Integrity only where it applies.** Self-learners get working answers. When it's unclear whether work is graded, the tutor asks in one line while it starts helping. "My professor allows AI" gets matched to the specific use allowed. Graded answer checks get an honest verdict but never the answer.
- **Visuals on claude.ai.** If `show_widget` is available, call `read_me` once, then show the widget with the prose outside it. Each visual shows one relationship. Neither the visual nor the prose answers the question the tutor is about to ask. Each visual says what the model simplifies.
- **Make what they ask for:** flashcards, quizzes and guides are made right away, built for active recall.
- **Build a live-turn widget** in `references/visual-teaching.md`, with `examples/chair-flip.html` as the reference: a library-free canvas projection, one state value, color that encodes the rule, highlights only where they matter, three controls, host theme tokens and phone-first sizing.
- **Learn-mode parity** scenarios in `evals/scenarios.md`.

## [2.2.1] - 2026-10-11

### Added
- **Crafted figures** in `references/visual-teaching.md`: rendered real apparatus and phenomena across fields (lab setups before lab day, physics demos, chemistry glassware and reactions, engineering mechanisms, measurement instruments), and, for abstract concepts, a recognizable machine whose working is the concept, each driven by one true model, with the mapping and its limits stated, physics-driven shaders only where lines can't draw it, one accented part to watch, prediction before motion, a framed card with a live readout, calm learner-driven motion, critic-style render verification, and honest sizing. Adapted with credit from Anatomy by Ryan (wheresryan22/anatomy, MIT); recommends that skill as an optional companion for crafted figures. `lab` points to it.

## [2.2.0] - 2026-10-11

Myelinate is now a Claude Code plugin with fourteen skills behind the router, and its aim is stated: the Socratic midwife who draws out the learner's own thinking.

### Added
- **Claude Code plugin.** `.claude-plugin/plugin.json` and a `baney75` marketplace. Install with `/plugin install myelinate --marketplace baney75/myelinate` (older Claude Code: `/plugin marketplace add baney75/myelinate`, then `/plugin install myelinate@baney75`). Every skill loads on its own description; slash commands such as `/myelinate:tutor` force one.
- **`assignment`**: coaches graded work (problem sets, lab reports, essays, coding assignments) instead of doing it. Separates tool help from authorship, follows the course's AI policy, and cites the deskilling and never-skilling evidence.
- **`project`**: learn while building, in the mix the learner chooses (build and learn, teach me, or just tell me). Used only when asked; it stays out of ordinary coding and work.
- **`assess`**: tests written to the objectives, graded against a key and rubric (key first), honest scores, optional bonus work, and a gradebook.
- **`notes`**: reads the learner's own notes (Google Drive, OneDrive, Notion, Obsidian or photos of handwritten pages) to see how they are grasping a subject, flags misconceptions and notes that only copy the slides, coaches note-taking, and turns the notes into practice.
- **`course-project`**: turns a big goal into a university-level course researched against accredited syllabi, with a lesson plan, assignments, tests and teacher instructions, to run as a Claude Project. Adds `templates/course-project-prompt.md` and `templates/gradebook.md`.
- **`print`** now builds study guides for active recall: questions first, answers at the back, blank diagrams, contrast tables for confusables, and a mixed self-test.
- **`study-plan`** offers opt-in reminders on a calendar the learner has connected, and earlier personal deadlines by agreement, labeled so they are never confused with the real date.
- **`references/personalization.md`**: an evidence-based learner model that improves over time; adapts to what works, never to a fixed learning-style label.
- **`references/first-session.md`** (shared intake for `tutor` and `teach`) and **`references/visual-teaching.md`** (rendered diagrams, linked representations, interactive 3D models, chemistry tables).
- Router: the Socratic-midwife aim, zero-config use, automatic use, slash commands, opt-outs, and a "no false starts" rule so learning intent triggers Myelinate and ordinary tasks do not.
- Community files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, issue and pull request templates.
- Site: Open Graph and Twitter card tags, canonical link, JSON-LD, `sitemap.xml`, `robots.txt`.

### Changed
- **`tutor`** now serves a course the learner is enrolled in: it loads from memory or the conversation, owns course intake (materials and uploads), and teaches live in chat or voice in the course's scope and notation.
- **`teach`** is rewritten for learning that is not for an enrolled course (personal goals, work skills, projects): the agent designs the curriculum and lesson plans at university standard, anchored in the learner's project and driven by memory.
- Complex anatomy uses the learner's textbook or lecture figures, or licensed real images, instead of generated SVG.
- Router route table and core rules; chemistry playbook additions; new v2.2 scenarios in `evals/scenarios.md`.
- Website and README present fourteen skills and the plugin install path.
- Real headless `claude -p` trigger test with the plugin installed, one run per prompt: 11 of 11 as expected, including five coding and work prompts that loaded no Myelinate skill. One run each, so a smoke test, not a rate. Details and what was not tested are in [evals/verification.md](evals/verification.md).
- Plain words (previously drafted as 2.1.2, never released on its own): checks are called a quick check or warm-up, and clinical words stay out of the intake.

## [2.1.1] - 2026-10-10

### Fixed
- The optional intake invitation listed example conditions, which undid the earlier "never name conditions" wording. It stays open and optional and names nothing.
- A new learner's first reply could skip the question about what helps them study; it now includes one optional what-helps question.

### Changed
- The `tutor` description now mentions hints on practice problems and counting a revealed answer as known, widening its triggers.
- Skill-eval smoke test (Claude Sonnet, 2 repeats): 1.00 held-in and 1.00 held-out, up from 0.85 and 0.79. See [evals/verification.md](evals/verification.md) for limits.

## [2.1.0] - 2026-10-10

### Added
- **`references/how-the-mind-learns.md`**: prediction error, generation, desirable difficulty, consolidation, stress and metacognitive illusions, each tied to a tutor move, with the limits of the myelination evidence (mostly mice).
- `tutor`: seven override rules (verdict from the key; withhold what the learner can generate, give what they can't), a silent pre-reply check, a six-rung help ladder, an answer-leak table, and a sycophancy pressure table.
- Router core rules carry commit-then-inform and key-first honesty so they hold when the router is pasted alone.

### Fixed
- A wrong answer could be opened with "Right." Forward test (one model, author-graded): v2.0.0 passed 9 of 13 cases; v2.1.0 passed 14 of 14 after an adversarial review and one added case.

## [2.0.0] - 2026-10-06

### Changed
- Rebuilt as a router (`SKILL.md`) over nine sub-skills: `teach`, `tutor`, `lab`, `print`, `flashcards`, `memory-hooks`, `study-plan`, `find-media` and `verify`.
- Memory-first: read the learner profile at the start, save at the end, ask before saving anything personal. Honest, not agreeable.
- New brand, landing page, hero and social card.

### Added
- Interactive lab engine with an oxygen-unloading reference lab and a journey test; printable practice tests with separate answer keys; `llms.txt` for the paste-the-link route.

## [0.1.0] - 2026-10-02

### Added
- First release: a single source-grounded teaching skill with course-aware practice, feedback and spaced retrieval, an evidence ledger, a research method, an interactive sample lesson and a package check (`scripts/check.py`). Later additions before 2.0 asked about study preferences rather than conditions, added exam-clock planning and production lessons for study packs.

[2.3.1]: https://github.com/baney75/myelinate/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/baney75/myelinate/compare/v2.2.1...v2.3.0
[2.2.1]: https://github.com/baney75/myelinate/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/baney75/myelinate/compare/v2.1.1...v2.2.0
[2.1.1]: https://github.com/baney75/myelinate/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/baney75/myelinate/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/baney75/myelinate/compare/v0.1.0...v2.0.0
[0.1.0]: https://github.com/baney75/myelinate/releases/tag/v0.1.0
