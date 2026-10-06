<p align="center"><img src="assets/hero.svg" alt="Myelinate. Understand it. Retrieve it. Use it. An open-source skill suite for learning: courses, live tutoring, labs, printable tests, flashcards and study plans. Honest, not agreeable, with an adversarial accuracy review before high-stakes material ships." width="100%"></p>

**An open-source agent skill suite that turns “teach me this” into explanation, practice, feedback, and a reason to come back.**

Ask about a concept. Bring your course materials if you have them. Myelinate routes the request to the right skill, teaches in manageable steps, and checks what you can do with it. It is honest, not agreeable: it won’t confirm a wrong answer or cave when you push back on a correct correction, and it changes its mind on evidence. It is a set of Markdown skills for a capable AI assistant, not a separate model or a hosted tutoring service.

[Website](https://baney75.github.io/myelinate/) · [Read the router skill](myelinate.md) · [Try the sample lesson](https://baney75.github.io/myelinate/examples/lesson.html) · [See the evidence](references/evidence.md)

## Use it in any chat

No install needed. Paste this into an assistant that can open links, in chat or voice mode:

```text
Use the Myelinate learning skill: https://github.com/baney75/myelinate — read SKILL.md and follow it to teach me.
```

The assistant fetches [SKILL.md](SKILL.md) and follows it. If yours can't browse, [install the folder](#install) or paste SKILL.md itself.

![Sample Myelinate lesson on limiting reactants](assets/sample-lesson.jpg)

## What's inside

`SKILL.md` is a router. It reads what you are after and hands the request, with your context, to one of nine skills:

| Skill | What it does |
| --- | --- |
| [teach](skills/teach/SKILL.md) | Finds out why you're learning and how you learn, gathers your syllabus, study guide, notes and textbook (including uploads), designs the course and teaches it with the best classroom methods. |
| [tutor](skills/tutor/SKILL.md) | Live teaching in chat or voice, one step at a time, with predictions, hints and feedback. |
| [lab](skills/lab/SKILL.md) | Builds interactive learning labs and simulations as web pages. |
| [print](skills/print/SKILL.md) | Printable PDFs: practice tests with separate answer keys, labeled and blank diagrams, worksheets. |
| [flashcards](skills/flashcards/SKILL.md) | Makes cards ready for Quizlet, Anki or Obsidian. |
| [memory-hooks](skills/memory-hooks/SKILL.md) | Writes research-backed mnemonics for material that will not stick. |
| [study-plan](skills/study-plan/SKILL.md) | Works back from the exam date: spaced relearning, practice and sleep. |
| [find-media](skills/find-media/SKILL.md) | Finds diagrams, photos and videos (including YouTube) and notes their licenses. |
| [verify](skills/verify/SKILL.md) | Adversarial review of accuracy and currency before high-stakes material ships. |

On the first session, Myelinate asks a few questions about how you learn (pace, chunk size, what's hard) and saves that profile to your assistant's memory or a file you keep, then reads it at the start of later sessions. Sharing a learning condition is optional and never required.

## Start with one good question

```text
Use $myelinate to teach me limiting reactants.
I understand moles, but I keep choosing the wrong reactant.
I have 20 minutes. Explain first, then help me practice.
```

Or:

```text
Use $myelinate with my study guide and notes.
Map the tested objectives, teach my weak spots, and give me
new problems in the format my course uses.
```

The tutor asks about the goal, course context, and optional access preferences. For courses, it asks for the **study guide, syllabus, notes/slides, and textbook edition**. Missing materials do not block a first lesson. It asks how you learn, such as pacing, chunk size, or what's hard. You may mention a learning condition if you choose, but it is never required and never labeled; “shorter steps help” is enough.

## What makes the lesson useful

| From the learner | From Myelinate |
| --- | --- |
| “I don't get it.” | A clear explanation, a worked example, and the limits of the analogy. |
| “I think I know it.” | A question you answer before seeing the solution, with specific feedback. |
| “I can do that example.” | A changed application that checks whether you can choose and use the idea. |
| “My exam is next week.” | Course-aligned practice and a realistic queue for revisiting the gaps. |
| “I need a different pace.” | Options for chunk size, steps, response format, and distractions. |
| “Make me something I can study.” | A source-linked study pack with original practice and a separate explained answer key. |

**Explain → retrieve → get feedback → apply → revisit.** The sequence adapts. You can ask for an explanation, request a hint, skip a test, or stop at any time. Flashcards are available when useful; application stays central.

## Install

### Claude

In the Claude apps, [download this repository as a ZIP](https://github.com/baney75/myelinate/archive/refs/heads/main.zip) and upload it where Claude lets you add a skill (in Settings, under Skills). Then start a chat with “Use myelinate to…”.

In Claude Code, clone the repository and link it into your skills directory (macOS/Linux):

```sh
git clone https://github.com/baney75/myelinate.git
mkdir -p ~/.claude/skills
ln -s "$PWD/myelinate" ~/.claude/skills/myelinate
```

### Codex

Clone this repository and link it into your skill directory (macOS/Linux):

```sh
git clone https://github.com/baney75/myelinate.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/myelinate" "${CODEX_HOME:-$HOME/.codex}/skills/myelinate"
```

Run the link command from the directory containing the clone. If a `myelinate` skill already exists, inspect it before replacing anything. For Windows, copy `SKILL.md`, `skills/`, `references/`, and `agents/` into a `myelinate` folder under your configured skills directory. Open a new chat if the client needs to refresh discovery, then use `$myelinate`.

### Other assistants

Use an environment's supported skill importer with this folder, or provide [myelinate.md](myelinate.md) as instructions. The router file is usable by itself; supply `skills/` and `references/` for the full suite and its research guidance. Browsing and file-reading tools enable current research and course-source inspection. Without them, the tutor must label its limits. Native invocation and automatic discovery vary by product; compatibility has not been tested in every assistant.

No API keys, package installation, or external service is required by the skill itself. Your assistant's ordinary access, tools, and usage limits still apply.

## See the approach

The [interactive sample](https://baney75.github.io/myelinate/examples/lesson.html) teaches limiting reactants with a worked example, a fresh numerical problem, hints, and answer feedback. It distinguishes independent, hinted, and revealed work. It does not collect responses or pretend to measure long-term retention. [Open the source](examples/lesson.html) to use it offline.

For course material, Myelinate can produce a compact scope map, concept explanation, practice set, explained answer key, and review queue. The included [templates](references/session-template.md) keep those outputs consistent without forcing every lesson into a document.

## Evidence without mythology

Retrieval, spacing, feedback, and worked examples have substantial research behind them. Their effects depend on the task, learner, timing, and comparison. The [evidence ledger](references/evidence.md) links the sources, inspected scope, and limits. The [research method](references/research-method.md) explains how the tutor evaluates sources for a new topic.

“Myelinate” is a name, not a claim that a prompt changes your myelin. This package cannot force permanent memory or guarantee a grade. A good-looking study guide is not a learning outcome. The tutor reports actual attempts and delays; the complete skill's learning efficacy has not been established.

Learner health disclosures and course records stay out of public outputs. Saving preferences or progress requires agreement. A suggested review time is not a scheduled notification.

## Improve it

Useful contributions include a reproducible tutoring failure, a better-supported source, an accessibility fix, or a clearer exercise. Use fictional or consented, de-identified examples; do not upload private course material, learner health information, or restricted exams.

```sh
python3 scripts/check.py          # package integrity and local links
python3 scripts/check.py --sync   # regenerate SKILL.md after editing myelinate.md
```

`myelinate.md` is the authored source; `SKILL.md` is an identical generated entrypoint for skill discovery. [Behavioral scenarios](evals/scenarios.md) test decisions that a syntax checker cannot. [Verification notes](evals/verification.md) describe what has actually been checked.

MIT licensed. Research and linked third-party material retain their own rights.
