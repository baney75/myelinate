# Verification of the initial package

Checked **2026-10-02**, with synthetic learner prompts and locally generated examples. These checks assess instructions and software behavior; they do not measure real student learning.

## Teaching behavior

A fresh read-only reviewer produced actual simulated tutor replies to three cases:

- An explanation-first entropy request received an explanation, a bounded analogy, and an inspected source before any diagnostic.
- A biology exam request with a missing syllabus and declined neurodivergence discussion received a provisional lesson, a request for course materials, and no further health inquiry.
- A claim of success after a hint was not upgraded to independent mastery; a permanent-memory guarantee and unsupported reminder claim were rejected.

The reviewer found no material contradiction in the inspected core and references. This is one forward-test, not a benchmark across assistants. A verifiable effective model identifier was not exposed, so no model-specific efficacy claim is made. The other scenarios in [scenarios.md](scenarios.md) are available regression cases, not all executed tests.

## Research and packaging

- The research pass checked ten sources with their reported access scopes. A second source check corrected two paper titles and narrowed a feedback claim that the cited abstract did not establish.
- The native skill validator accepted the frontmatter, name, description, and finished instructions.
- `python3 scripts/check.py` checks the required files, identical `myelinate.md`/`SKILL.md`, and local Markdown/HTML links. It does not validate external URLs or teaching quality.

## Interactive sample

The rendered lesson was inspected in the Codex in-app browser at **1280×900** and **390×844**. Reading and practice controls were legible at both sizes; the phone document width was 390 pixels with no horizontal document overflow. This is browser viewport testing, not a physical phone or screen-reader audit.

Browser interaction checks covered blank and invalid answers, correct and incorrect numeric responses, hint, reveal, keyboard submission, hiding the answer on reset, and preserving prior exposure across reset and repeated submissions. A reset bug found during review was corrected: the same question cannot become an independent attempt merely by clearing it after a hint or revealed answer. Exposure exists only in page memory and clears on reload; the demo has no persistent learner record.

The numerical answer is checked; written reasoning is explicitly ungraded. The page makes no mastery claim and labels delayed retrieval as not yet checked. JavaScript syntax and SVG structure were checked separately. Accessibility coverage is limited to readable layout, labels, contrast, focus styling, and exercised controls; full WCAG conformance is not claimed.

## Production lessons update

Checked **2026-10-04**. A fresh read-only agent read the core and all references, then wrote actual replies to four synthetic cases: a study pack requested before the guide arrived (with notes that duplicate the slides), a corrected lesson whose audio check failed, a hinted success labeled as mastery, and a label-masked diagram quiz. All four met their decisive observations in [scenarios.md](scenarios.md). The reviewer flagged gaps around provisional drafting, alt text that does not reveal answers, how an audio check records a pending clip, and convention versus factual conflicts; these were clarified in the core and [production-lessons.md](../references/production-lessons.md). The revised text was not re-run. This is one forward-test on one model.

## v2.1.0: withholding, honesty and the mind reference

Checked **2026-10-10**. Fresh Sonnet agents, given only the router and `tutor` (plus the mind reference for v2.1), wrote the actual next tutor reply to 13 concrete cases from the *Withholding and honesty* table in [scenarios.md](scenarios.md). Replies were graded by the author against that table's seven criteria.

- **v2.0.0 baseline:** 9 pass, 2 partial, 2 fail. On "3x + 7 = 22 → x = 6" it opened with **"Right."**, a false verdict. After two real attempts and a second explicit demand, it kept withholding instead of giving the answer and making the learner use it.
- **v2.1.0 first draft:** 13/13 pass.
- An adversarial Opus review then found no blocking issues and 13 wording or eval fixes. The most important were these. "Commit, then inform" could block teaching a brand-new concept. "Keep the key private" assumed a private scratchpad. The ladder put the near-answer fill-in below the worked example. Two eval cases contradicted the verdict-first rule. One stress-and-memory summary left out the retrieval finding, which was confirmed from the paper and added. All were fixed.
- **v2.1.0 after fixes:** 14/14 pass. The added case, "I've never heard of entropy", taught first and asked for a prediction afterward.

Limits: one run per version on one model, author-graded, synthetic learners. This shows the instructions change model behavior on these cases. It does not show reliability across models, and it doesn't show learning gains.

## v2.1.1: intake wording and triggers

Checked **2026-10-10** with the Magnus Singularity's `tools/skill_eval.py` (Claude Sonnet, 2 repeats, replies run to the end with regex checks, 13 held-in and 7 held-out cases).

| Version | Held-in | Held-out |
| --- | --- | --- |
| v1, as vendored at the time | 0.85 | 0.79 |
| v2.1.0 | 0.85 | 0.79 |
| v2.1.1 | 1.00 | 1.00 |

v2.1.0 failed for two reasons. The optional intake question named example conditions (ADHD, dyslexia, anxiety), which undid this repo's earlier "never conditions" wording. And a new learner's first reply could skip the question about what helps them study. The description also didn't mention hints on practice problems or counting a revealed answer as known. v2.1.1 keeps the optional, open invitation to share, names no condition, adds the first-reply preference question, and widens the description. Trigger results vary from run to run, so treat 2 repeats as a smoke test, not a rate.

## v2.2.0: course tutoring vs self-directed teaching, assignments, projects, notes, plugin

Checked **2026-10-11**.

- **Package:** `python3 scripts/check.py` PASS (52 required files). `claude plugin validate .` passed, including `--strict`. Installed from the local marketplace with Claude Code 2.1.296: all 15 skills (router plus 14 sub-skills) load; about 2,500 always-on tokens.
- **Automatic invocation (real, not simulated):** headless `claude -p` with the plugin installed and only the Skill tool allowed, one run per prompt, 11 prompts. Learning prompts loaded the expected skill: a class question about Newman projections → `tutor`; "write the abstract for my lab report" → `assignment`; learn-while-building an ESP32 plant monitor → `project`; a full course in a Claude Project → `course-project`; "are my notes good?" with pasted notes → `notes` (its reply led with the swapped Na⁺/K⁺ stoichiometry); flashcards for an exam → `flashcards`. Five work prompts (unit tests, OAuth with token refresh, a failing CI check, a mid-task useEffect question, a team roadmap update) loaded no Myelinate skill. 11/11 as expected. One run each, so treat this as a smoke test, not a rate.
- **Adversarial review:** a fresh agent reviewed the full diff and simulated seven cases. It found three blockers (the phrase "unit tests" in `assess`'s description; opt-out rules visible only in the router; opt-out wording that could read as permission to write graded work) and thirteen should-fix items. All were fixed before release, then the trigger tests above were run on the fixed version.
- **Not tested:** learning outcomes; voice mode; Claude apps' skill upload; other assistants; calendar and notes connectors end to end.

## Not established

Long-term retention, better grades, clinical benefits, neurological effects, effectiveness across every concept, and compatibility with every assistant have not been demonstrated. A future learning pilot should use consenting learners, baseline and delayed checks, fresh comparable items, and clearly reported assistance.

## v2.3.0: head-to-head against Claude's learning skill

Checked **2026-10-11** with `evals/head-to-head/h2h.py` and its 17 scenarios. Each scenario is one simulated claude.ai chat turn with no tools. The responder was Sonnet (`claude -p`, no settings or MCP). It ran under three skill texts: Claude's built-in `learn` skill (2,227 words, a local copy not vendored here), Myelinate's router plus the sub-skills the case routes to, and the router alone, because claude.ai may load only the router. An Opus judge saw the learn reply and one Myelinate reply in random order, blind to which was which, and scored each 1–10 against a per-scenario rubric and a shared standard.

| Version | Runs | learn mean | Myelinate (router + sub-skill) | Router only |
| --- | --- | --- | --- | --- |
| 2.2.1 | 17 × 1 | 7.53 / 7.88 | 6.35, won 4 of 17 | 6.18, won 2 of 17 |
| 2.3.0 draft | 17 × 1 | 7.12 | 7.41, won 9 of 17 | 7.88, won 12 of 17 |
| 2.3.0 | 17 × 2 | 7.00 | **7.76, won 20 of 34** | **7.44, won 19 of 34** (3 ties) |

The 2.2.1 losses had four causes. Turns stacked several questions: preference, confidence and intake on top of the teaching question. A fluent expert ("walk me through monads") got an essay. Broad topics got quizzes, even after "just lay it out". The SQL self-learner got a turn of questions with no foothold. After the draft, the remaining losses were a leak (the prose answered the visual's own question), a lecture before diagnosing a vague "I don't get recursion", and a closing quiz item after the learner had already transferred the idea. Rules were added for each, and the release numbers come from the run after those additions.

An adversarial Opus review then found seven defects, all fixed:
- the graded check-my-answer rule conflicted with verdict-first grading (now: an honest verdict, never the answer or the fix);
- the done-turn rule conflicted with the closing recall;
- the self-learner rule conflicted with `teach` §5a;
- two pressure rules gave no precedence;
- the reference widget's question named what its highlight showed;
- the model-kit direction was backwards;
- the release records were missing.

A targeted rerun of four affected scenarios (×2) after the fixes: Myelinate won 6 of 8 (mean 7.50 vs 6.25), router only won 7 of 8 (7.62 vs 6.00).

Limits:
- One responder model and one judge model.
- Single-turn simulations written by the author.
- The rubric was written from the learn skill's own goals, so it favors learn's standard on those cases.
- 34 judgments per arm separate the versions but don't establish reliability across models.
- No real learners, so nothing here measures learning.

Know-when-done remains weakest: every arm sometimes ends a finished topic on one more quiz item.

`examples/chair-flip.html` was rendered with Playwright Chromium at 820 px light and 390 px dark: no page errors, no horizontal scroll, and the state readout changes correctly on flip and on the face toggle. The reviewer checked the axial/equatorial geometry and the 1,3-diaxial highlighting at C3/C5.
