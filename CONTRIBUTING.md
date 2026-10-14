# Contributing to Myelinate

Thank you for helping. Myelinate is a set of Markdown skills, so most contributions are careful edits to instructions, plus the evidence for why the edit is better.

Useful contributions include a reproducible tutoring failure, a better-supported source, an accessibility fix, a clearer exercise, or a skill description that triggers when it should and stays quiet when it shouldn't.

## Before you start

Open an issue first for anything that changes teaching behavior, adds a skill, or touches the router's core rules. Small fixes (typos, broken links, wording) can go straight to a pull request. Read [AGENTS.md](AGENTS.md) and [assets/brand.md](assets/brand.md); they set the rules for claims, voice, and the site.

## The rules that matter most

- **No learner data in the repo.** Use fictional or consented, de-identified examples. Do not add private course material, restricted exams, learner records, or health information.
- **Claims need sources and limits.** Do not claim proven efficacy, guaranteed grades, forced permanent memory, clinical benefit, or measured myelination. "Myelinate" is a name, not a mechanism.
- **Honest, not agreeable.** Changes must not make the tutor confirm wrong answers or cave to pushback on a correct correction.
- **Never name or infer a learner's condition.** Asking what helps and what gets in the way, in everyday terms, is fine. Sharing a condition is the learner's choice.
- **Voice.** Direct, warm, adult. No hype, exclamation marks, or emoji.

## Making a change

1. Edit the authored source: `myelinate.md` for the router, `skills/<name>/SKILL.md` for a sub-skill. Do not edit `SKILL.md` at the repo root by hand; it is generated.
2. Regenerate and check the package:

   ```sh
   python3 scripts/check.py --sync   # copies myelinate.md to SKILL.md, then checks
   python3 scripts/check.py          # required files, identical entrypoints, local links
   ```

3. If you touched `.claude-plugin/`, a skill's frontmatter, or the version, validate the plugin:

   ```sh
   claude plugin validate .
   ```

   Keep the version in `.codex-plugin/plugin.json` equal to the `Version` line in `myelinate.md`. Leave `version` out of `.claude-plugin/plugin.json`: installs then update by commit. Edit root sources only; `python3 scripts/check.py --sync` regenerates the copies inside each skill folder.
4. For a behavioral change, run the relevant cases in [evals/scenarios.md](evals/scenarios.md) with a fresh agent, read its actual replies, and record exactly what you tested. Simulated learners do not establish learning gains, and the pull request should say so.
5. For a substantive teaching change, run the `verify` skill's adversarial review (`skills/verify/SKILL.md`).
6. If you changed the lab engine or template, keep `examples/oxygen-lab.html` passing its journey test (`tests/lab_journey.py`).
7. Add a line to [CHANGELOG.md](CHANGELOG.md) under an `Unreleased` heading.

## Site and README changes

`index.html` follows the brand guide: cream paper, dark ink, one rust accent, light and dark themes, no new heavy dependencies. Check it at desktop and phone widths in both color schemes before opening a pull request.

## Pull requests

Describe what changed and why, what you ran, and what you could not check. Keep pull requests focused. By contributing you agree your work is released under the [MIT license](LICENSE).

Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a security or privacy problem, see [SECURITY.md](SECURITY.md) instead of opening a public issue.
