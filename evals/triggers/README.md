# Trigger eval

Checks that each skill's frontmatter `description` makes an agent load the right skill, and that ordinary work requests load none of them.

## What it measures

- `prompts.jsonl`: realistic first messages. Each has `accept` (the skills that may fire) and `kind`. Positives should fire a Myelinate skill; negatives are near misses (coding, PDF conversion, calendar events, proofreading) that must not fire any Myelinate skill. `holdout.jsonl` is a second set that was kept out of description tuning; run it the same way to check for overfitting.
- `distractors.json`: generic skills (PDF, office files, front end, code review, debugging, calendar, editing) installed beside the suite so a near miss has a realistic place to go.
- **Hit rate**: share of positive prompt runs where the chosen skill is in `accept`.
- **False-fire rate**: share of negative prompt runs where any Myelinate skill fired.

## Method

`run.py` installs a stub of every skill (its real `name` and `description`, no body) plus the distractors into the user skill folder of an isolated, temporary HOME, then runs `codex exec` once per prompt and pass. Codex lists the stubs the way it lists any installed skill, and the model is asked which one skill, if any, it would load before replying. Host skills, AGENTS.md files and plugins do not leak in. The model and reasoning effort are fixed (default `gpt-5.6-luna`, effort `low`). The Codex CLI does not expose temperature, so the default is 3 passes and the report includes per-pass counts, majority-vote rates and the unstable prompts.

## Required local step

Any change to a skill `description` must be followed by:

```sh
python3 evals/triggers/run.py --passes 3 --out evals/triggers/results/latest.json
python3 evals/triggers/run.py --passes 3 --prompts evals/triggers/holdout.jsonl --out evals/triggers/results/holdout.json
python3 evals/triggers/check.py
```

It needs the Codex CLI signed in (`codex login status`). It makes about 150 small model calls per run.

## CI

`check.py` runs on every push and pull request with no model and no secrets. It fails when a prompt names an unknown skill, a suite skill has no positive prompt, or a committed result in `results/` is partial, malformed, or run with a different model, effort or pass count than `thresholds.json` requires. It also fails when a result was produced for different skill descriptions, prompts, labels, distractors or question wording (each result carries fingerprints of both), when the rates it reports disagree with the rates recomputed from its per-prompt choices, or when the recomputed rates fall below the floors. `test_check.py` feeds it empty, partial, malformed, inconsistent, stale and below-floor results and fails if any of them passes. The floors are main's scores before the trigger rewrite; raise them when a change beats them, and never lower them without a written reason in the pull request. The eval measures the skill a model says it would load from the listing, not an observed skill load, so treat it as a routing signal rather than proof of runtime behavior.

A manual `trigger-eval` job in `.github/workflows/check.yml` reruns the model eval when the repository has an `OPENAI_API_KEY` secret, and skips with a notice when it does not.
