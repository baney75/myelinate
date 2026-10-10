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

## Not established

Long-term retention, better grades, clinical benefits, neurological effects, effectiveness across every concept, and compatibility with every assistant have not been demonstrated. A future learning pilot should use consenting learners, baseline and delayed checks, fresh comparable items, and clearly reported assistance.
