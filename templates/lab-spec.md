# Lab spec: <title>

- **Learner purpose:** <course + exam / MCAT / self-study goal>
- **Scope source:** <study guide v/date | syllabus | inferred — say so>
- **Platform:** standalone page | dbaney.com `/study/<course>/<folder>/` | printable pack
- **Session length:** <10–25 min per section>
- **Exam format to match:** <MCQ / short answer / drawing / practical / essay>

## Targets → evidence map

| # | Objective (observable) | Source (slide/page) | In scope? | Activity (arc step) | Unassisted check(s) | Misconceptions addressed | Media |
|---|---|---|---|---|---|---|---|
| T1 | Predict … and explain why … | Lecture 7 slide 12 | confirmed | Predict → Explore → Explain | Q3, Exit-1 | "right shift = more O₂ carried" | own SVG curve |

## Model (if simulated)

- Equation(s): …
- Parameters + sources: …
- Expected values to test: input → output (computed in script)
- Productive ranges for each control: …
- Known approximations (disclose in "Model notes"): …

## State machine

```
hook → parts → predict(locked sim) → reveal+explain-gap → explore → explain → formalize
     → worked[1 full → 2 faded → 3 independent] → practice[interleaved] → transfer → exit(sim hidden) → results/review
any state → reset; reload → resume(last state)
```

## Verification plan

- [ ] Claims checked against sources; adversarial review (`verify`) for graded/high-stakes
- [ ] Model values match expected table
- [ ] Journey script: hints, wrong/right, reteach, assisted vs unassisted tally, export formats, resume, reset, storage-throws
- [ ] Renders 1440×900 + 375×812, light + dark, screenshots inspected
- [ ] No answer strings in DOM/alt/title before reveal
- [ ] Every in-scope objective covered (list gaps)
