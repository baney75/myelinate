# Security policy

Myelinate is Markdown instructions, a few static example pages, and small helper scripts. It has no server, accounts, API keys, or telemetry. The security and privacy risks that matter here are about what the instructions could cause an assistant to do.

## What to report

- **Prompt injection.** A way that content a learner or the skill ingests (an uploaded syllabus, a fetched web page, a pasted document) could override the skill's rules, make it leak private data, or run unwanted actions. The `tutor` skill says text inside uploaded files and web pages is content, not instructions; a case where that fails, or where another skill lacks that protection, is a valid report.
- **Privacy.** Any instruction, template, or example that would save, repeat, or publish a learner's private details, course records, or health information without agreement, or that labels a learner's condition.
- **Unsafe defaults.** A skill that tells an assistant to run commands, install packages, send messages, or schedule things without the learner's say-so, or that claims it did something it cannot do (for example, a reminder it never scheduled).
- **The example pages and scripts.** XSS or similar problems in `examples/`, `templates/`, or `scripts/`.
- **Learner data in the repository.** Anything that looks like a real learner record, private course material, or a restricted exam.

Wrong or unsupported teaching content (a bad source, a factual error) is not a security issue. Please open a normal issue.

## How to report

Use GitHub's private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability**. If that is unavailable to you, open a minimal public issue that says you have a security or privacy report, without details, or reach the author through [dbaney.com](https://dbaney.com), and details will be arranged privately.

Please include the skill or file, the exact text or input involved, the assistant you used, and what happened. Do not include real learner data; use fictional examples.

## What to expect

This is a one-maintainer open-source project, so there is no formal SLA. Reports are read, acknowledged when possible, and fixed in a new version with a note in [CHANGELOG.md](CHANGELOG.md). Credit is given if you want it.

## Supported versions

Only the latest release (currently 2.2.x) receives fixes.
