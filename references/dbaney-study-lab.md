# Integration: dbaney.com study labs

Myelinate's author runs course study labs at dbaney.com ("Study with Me"). This note tells an agent with access to that site's repository how to add or improve a lab there. Other sites can copy the pattern.

## Engine

- Content lives in `content/<lab>.json`; `scripts/learning-lab.mjs` builds `/study/<course>/<folder>/lab.html` + `data.json`; `study/learn.js` (`validateDataset`) validates and renders it.
- The `/study/` desk is behind the site's study login and marked `noindex`. Course figures and audio may live there; never on public pages.
- Read the site repo's `AGENTS.md` first and follow it: maroon/cream/gold editorial design; SVG icons from `scripts/icons.mjs` (no emoji, Unicode arrows or icon fonts); OS-style folder browser with sidebar, toolbar and breadcrumb; only approved public assets; keep saved-progress compatibility.

## Schema (validated)

`title, subtitle, course, topics[]`; topic `{id, title, summary, sourceLabel, sourceUrl?, lessons[], questions[]}`; lesson `{id, title, body, bullets[], recallPrompt, recallAnswer, figure?, figureAlt (required with figure), figureCaption?, audio?, recallAudio?}`; question `{id, type, prompt, explanation, sourceLabel, figure?, questionAudio?, answerAudio?, reteachAudio?}` with `mcq` (`options[]`, zero-based `answer`), `matching` (`pairs[{left,right}]`, distinct rights), `sequence` (`items[]` in correct order), `short-answer` (`rubric[]`, `referenceAnswer?`, `referenceFigure?` + alt); `practiceTests[{id, title, description, questionIds[], ordered}]`. IDs are unique safe slugs across the file. Starter: `templates/dbaney-lab.json`.

## Make the format teach

Follow `skills/lab/SKILL.md` §8. In short: lesson body = mental model + one worked example (not a slide transcript); recall prompts ask for generation; distractors from named misconceptions; explanations refer to options by content; interleaved practice tests with transfer items; short-answer rubrics for mechanisms; use the uncertainty flag. Simulations need engine work (the organic lab's Newman projection shows the pattern) — propose a spec, build only when asked.

## Ship

1. Validate: build and `npm test` in the site repo.
2. Render the lab at phone and desktop; exercise lesson → recall → quiz → review → reset.
3. Commit with a clear message. Push to `main` (Cloudflare deploys automatically) only when the request includes publishing; otherwise stop and ask.
4. Confirm the change on the live site after deploy and report what was confirmed.
