---
name: lab
description: Build interactive learning labs — predict-first simulations, faded worked examples, misconception-based practice, spaced flashcards — as standalone pages or dbaney.com study labs. Use when someone wants a lab, study pack, or interactive lesson built.
---

# Lab

A lab is a page that makes the learner **think with the idea** — predict, manipulate, explain, apply — and then proves what they can do without help. A beautiful page that the learner reads and clicks through is not a lab; it's a brochure. Every element must either (a) make the learner generate something, (b) give feedback on what they generated, or (c) carry a variable of the concept.

The reference implementation is `examples/oxygen-lab.html` (template: `templates/lab-standalone.html`). Open it before building your first lab; copy its engine, not its content.

## 0. Rules that override everything else

1. **Prediction before observation.** Watching a demo without predicting teaches about as much as no demo (Crouch et al. 2004). Lock the simulation until the learner commits a prediction and a confidence.
2. **Guided, not recipe, not sandbox.** Unassisted discovery loses to instruction (d ≈ −0.38); enhanced (guided) discovery beats other instruction (d ≈ +0.30) (Alfieri et al. 2011). Click-by-click instructions kill exploration (9% vs 85% exploring; Chamberlain et al. 2014). Use a driving question, constrained controls, and a hint ladder.
3. **Score only unassisted work as learning.** Hinted, revealed, or sim-visible answers are recorded separately. Students who perform well *with* help often perform worse without it (Bastani et al., PNAS 2025).
4. **Be correct.** Every number, model, label and answer is verified against a source or computed. A lab that teaches a wrong curve is worse than no lab. Run `verify` before shipping anything graded or high-stakes.
5. **Course scope governs.** For a course lab, the official study guide/syllabus decides what's in. Lectures and folders overrun scope.

## 1. Before building: the lab brief

Get or infer (route through `teach` if missing):
- **Why** — course exam, MCAT, clinical, curiosity. Course? Get the **study guide, syllabus, slides/notes, textbook (title/edition/chapters), exam format and date.** Missing materials don't block a provisional lab; they block calling it "aligned."
- **Targets** — 3–7 observable objectives ("predict the direction of an O₂ curve shift from a change in pH and explain why unloading rises"), each tagged confirmed-in-scope or inferred.
- **Target platform** — (a) standalone page (Artifact or HTML file), or (b) **dbaney.com study lab** (see §8), or (c) printable pack.
- **Time budget per session** — a lab section should fit 10–25 minutes.

Then write a one-page **lab spec** (`templates/lab-spec.md`): targets → source page/slide → activity → check item(s) → misconceptions addressed → media needed. Every target gets an explanation and at least one unassisted check. Count from the guide, not from the question bank.

## 2. The learning architecture

Use this arc for each concept cluster. Steps are gated screens with a progress rail, back/forward, and a saved resume point. Skip steps that don't fit the material (pure vocabulary doesn't need a sim); never skip 3, 9 or 10. Without a simulation, step 3 is still a committed prediction — rank cases, pick the product, sketch the trend, choose the next step — revealed against a worked answer or a static figure. Never invent a fake simulation.

| # | Step | What it is | Evidence |
| --- | --- | --- | --- |
| 1 | **Hook puzzle** | A real question the concept answers ("Why does a sprinting muscle get far more O₂ at the same arterial PO₂?"). Not a list of objectives. | Desmos "create intellectual need"; Case |
| 2 | **Meet the parts** | 20–60 s pre-training: name axes, components, symbols *before* the process. | Mayer pre-training |
| 3 | **Predict + confidence** | Learner sketches, places, ranks or picks — then sure / fairly sure / guessing. Then reveal prediction vs actual side by side; ask "explain the gap" in one sentence. | POE; hypercorrection (Metcalfe 2017) |
| 4 | **Explore** | Constrained simulation with linked representations (§3). Driving question beside it, 3-step hint ladder: nudge → principle → worked step. | PhET implicit scaffolding; de Jong 2023 |
| 5 | **Explain** | Self-explanation: pick the principle + "because…" free text. | Bisra 2018, g ≈ 0.55; ICAP |
| 6 | **Formalize** | Now reveal the formal rule/equation as the tool that settles what they explored. Mnemonics go here, *after* understanding (`memory-hooks`). | Schwartz 2011 invent-then-tell; Kapur |
| 7 | **Worked examples, faded** | 3 problems: fully worked + self-explanation prompt → last step blank → independent. Let a confident correct pretest skip ahead. | Atkinson & Renkl 2003; expertise reversal |
| 8 | **Contrast & practice** | Interleaved items mixing confusable types; distractors from named misconceptions; answer → reason tier → confidence. Elaborated feedback per wrong option. Confident-wrong → targeted reteach card. | Brunmair & Richter 2019; Wisniewski 2020 (high-information feedback d ≈ 0.99) |
| 9 | **Transfer** | Same deep structure, new surface (blood-bank RBCs; altitude; a drug's pKa in the stomach). | Schwartz 2011; Butler 2010 |
| 10 | **Exit ticket** | 3–5 retrieval items with the sim and notes hidden. Opening the sim marks them assisted. | Roediger & Karpicke 2006 |
| 11 | **Results + review** | Honest report: unassisted-correct / with help / revealed / incorrect; per-target state; 6–12 flashcards (`flashcards`) in a built-in spaced review + Quizlet/Anki export; next review date. | Dunlosky 2013; Rawson & Dunlosky |

Open later sessions with 2–3 retrieval items from earlier labs (spaced, interleaved).

## 3. Simulations and visuals that teach

- **Model the real mechanism.** Use the actual equation (Hill, Henderson–Hasselbalch, Michaelis–Menten, Nernst/GHK, kinematics, logistic growth, Hardy–Weinberg). State parameters and sources in a "Model notes" disclosure; label approximations. Compute expected values in a script and check the sim reproduces them.
- **Constrain ranges to the productive region.** Every slider value should teach something; no physically meaningless extremes.
- **Linked representations, up and down the ladder of abstraction** (Victor): one concrete instance (a tetramer with 0–4 O₂), the trajectory/curve, and the whole parameter sweep — changing one updates all.
- **Label on the diagram, not in a legend.** Color ties a control to its effect.
- **Every visual element encodes a variable.** No particles, mascots, background music, trivia boxes (seductive details lower learning; Sundararajan & Adesope 2020).
- **Learner-paced.** Start paused; scrubbable timelines, step buttons, slow motion; small multiples beside any process animation. Never auto-play complex dynamics (Tversky 2002).
- **Run their wrong model.** When the learner's prediction is wrong, show what reality would look like if they were right, next to what actually happens. That's the most powerful feedback a lab can give.
- **Not everything needs to be interactive.** If a static labeled figure teaches it as well, use the figure. Interactivity is for relationships the learner should *feel* change.
- For subject-specific moves (mechanism arrow-pushing, anatomy layers, argument maps, proofs), read `references/subject-playbooks.md`. For figures, photos, micrographs and videos, use `find-media` (licensing, attribution, masking).

## 4. Questions, feedback and scoring

- **Every item has:** objective id, source label, correct answer, explanation, and for MCQ a misconception named per distractor.
- **Distractors come from real misconceptions** (concept inventories, the learner's own errors, common exam traps) — never filler.
- **Formats beyond MCQ:** ordering/sequence, matching, label-the-diagram (masked), numeric with tolerance and units, sketch-the-curve, two-tier (answer + reason), confidence-weighted, short answer with rubric. Match the exam's format.
- **Feedback explains**: why the right answer is right, why *their* choice was tempting and wrong, what to do next. Corrective right/wrong feedback d ≈ 0.46; reinforcement/punishment 0.24; high-information feedback 0.99 (Wisniewski et al. 2020).
- **Free text is never keyword-auto-graded.** Show a model answer + rubric checkboxes; record as self-assessed. If an AI grader is wired in (Artifact `sample` capability or an API), give it the answer key and rubric and still label it AI-assessed.
- **Assistance is data.** Record each attempt as *unassisted-correct · hinted-correct · revealed · incorrect · self-assessed*. Never fold assisted into "mastered."
- **Upload your work** (optional): for drawing or paper tasks, let the learner photograph and upload their answer (Artifact `files`/assets capability or a plain file input that stays in the browser); grade it against the rubric with an AI grader only if one is wired in, otherwise show the reference and record self-assessed.
- **Mastery gate**, not a wall: 2 of 3 unassisted correct to mark a target "Independent this session"; on a miss, route to a *different* contrasting case, not the same screen.
- **Embedded AI tutor (optional):** only with the worked solutions and misconception list in its context, one step at a time, never the answer before an attempt, scoped to the current step (Kestin 2025; Bastani 2025). Follow `tutor` rules.

## 5. Engineering standard

- **Model it as a state machine first** — states, transitions, what each shows, which objective each serves — as a comment block at the top of the script. Every state reachable; reset works. (AI-built explorables often fail at interaction logic, not visuals.)
- **Single self-contained file** for standalone labs: inline CSS/JS, inline SVG for charts, no external JS (Google Fonts OK). For an Artifact, follow the Artifact page contract.
- **Progress**: versioned `localStorage` key, every read/write in try/catch, app works when storage throws (show a quiet notice). In-page confirm for "clear progress" — no `window.confirm`.
- **No answer leaks**: answers live in JS and render on reveal; nothing in DOM text, `alt`, `title`, `aria-label`, filenames, captions or tooltips before reveal.
- **Accessibility**: semantic landmarks, visible focus, keyboard-operable controls, `<input type=range>` with labels and `aria-valuetext`, a live region narrating sim state, text alternatives for every figure, AA contrast, 44 px touch targets, `prefers-reduced-motion` honored.
- **Comfort**: light theme default with a real dark mode; no flicker, strobe, grain/noise textures, or looping animation. One question visible at a time on phone.
- **Phone first**: works at 375 px with no horizontal page scroll.
- **Narration** (optional): audio depends on exact text — hash text → clip; a text change invalidates the clip. Ship corrected text with audio marked pending rather than stale audio.

## 6. Verify before you deliver

Run all of these; report which passed, with numbers. Never claim "verified" without a check that could have failed.
1. **Content**: re-read every consequential claim against its source page/slide; soften anything stronger than the source. Run `verify` (adversarial review) for graded or high-stakes labs.
2. **Model**: script-compute key values and confirm the sim shows them (e.g., S(100/40/20 mmHg) ≈ 97/75/32%).
3. **Journey** (Playwright or equivalent): complete every step; use hints; answer right and wrong; check feedback, reteach, assisted/unassisted tallies, export file formats, reload-resume, reset, storage-throws mode; zero console errors.
4. **Render**: desktop 1440×900 and phone 375×812, light and dark; *look* at the screenshots; fix clipping, overlap, cramped controls, label collisions.
5. **Leaks**: grep the served HTML for answer strings before reveal.
6. **Coverage**: every in-scope objective has explanation + unassisted check; list any uncovered.

## 7. Delivery

- Standalone → publish as an Artifact (or deliver the HTML file if asked); one sentence on what it teaches and how long it takes. Offer a printable companion (`print`).
- dbaney.com → see §8.
- Always state: scope source (confirmed vs inferred), what's verified, what's approximate, what's not covered.

## 8. dbaney.com study labs

The site has its own lab engine: `content/<lab>.json` → `scripts/learning-lab.mjs` → `/study/<course>/<folder>/lab.html` + `data.json`, validated by `validateDataset` in `study/learn.js`. Full integration notes: `references/dbaney-study-lab.md`. Read the site repo's `AGENTS.md` first and follow it. Deploy (push to main) only when the request includes publishing; otherwise stop at a verified local build and ask.

Schema (validated): `title, subtitle, course, topics[]`; topic `{id, title, summary, sourceLabel, sourceUrl?, lessons[], questions[]}`; lesson `{id, title, body, bullets[], recallPrompt, recallAnswer, figure?, figureAlt (required only with figure), figureCaption?, audio?, recallAudio?}`; question `{id, type, prompt, explanation, sourceLabel, figure?, …audio}` with type `mcq` (`options[]`, zero-based `answer`), `matching` (`pairs[{left,right}]`, distinct rights), `sequence` (`items[]` in correct order), `short-answer` (`rubric[]`, `referenceAnswer?`, `referenceFigure?`); `practiceTests[{id,title,description,questionIds[],ordered}]`. IDs are unique safe slugs across the file. Template: `templates/dbaney-lab.json`.

Make the engine's format teach well:
- **Lesson body = mental model + one worked example**, not a slide transcript. Bullets are the 3–6 things to retrieve, each source-faithful.
- **recallPrompt** asks for generation (explain, predict, compare), not "list the slide."
- **Prediction first**: lessons and questions are separate arrays, so put the prediction in the lesson's `recallPrompt` or open the topic with a short prediction MCQ in a practice test ordered before the lesson review; the engine supports an uncertainty flag — use it.
- **Refer to options by content, never by number** in explanations (options may be shuffled).
- **MCQ distractors from named misconceptions**; explanation addresses why each wrong option tempts.
- **Interleave** practiceTests across topics; include at least one transfer item per topic and short-answer items with rubrics for mechanisms.
- **Figures**: course figures only behind the site's study login (the `/study/` desk is login-protected and `noindex`), never on public pages; mask labels fully for label questions.
- An interactive simulation needs engine work (the organic lab's Newman projection shows the pattern). Propose it with a spec; build it only when asked.
- Verify with the repo's tests (`npm test`), then render the lab at phone and desktop, exercise it, and confirm on the live site after deploy.

## 9. Anti-patterns

Sandbox with no question · click-by-click recipe · watch-only animation · formula on screen one · decoration · right/wrong-only feedback · quiz items answerable by reading the sim · confidence slider that drives nothing · one scaffolding level for everyone · an embedded AI that gives answers · learning-styles personalization · 20 blocked identical problems · long ungated scroll · text-dump lessons copied from slides · claiming "aligned" without the study guide · claiming "verified" without a run · promising permanent memory or grades.
