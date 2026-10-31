#!/usr/bin/env python3
"""Deterministic trigger guard for CI (no model, no secrets).

Fails when:
- a prompt label names a skill that does not exist (suite, distractor or "none");
- a suite skill has no positive prompt in prompts.jsonl that accepts it;
- a committed eval result is partial, malformed, or run with a different model,
  effort or pass count than thresholds.json requires;
- a committed result was produced for different skill descriptions, prompts,
  labels, distractors or question protocol (rerun `evals/triggers/run.py`);
- the scores recomputed from the result's per-prompt choices disagree with its
  summary, or fall below the baseline floors in thresholds.json.

The model eval itself is a required local step: see evals/triggers/README.md.
"""
import argparse
import json
import sys
from pathlib import Path

from common import (
    HERE,
    descriptions_sha256,
    inputs_sha256,
    load_distractors,
    load_prompts,
    score,
    suite,
)

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--root', default=str(HERE.parents[1]), help='repo whose skills to check')
ap.add_argument('--result', action='append', default=[], metavar='NAME=PATH',
                help='check a fresh result file against the floor for NAME (for example latest.json=/tmp/r.json)')
args = ap.parse_args()
errors = []

skills = suite(args.root)
if not skills:
    errors.append(f'no skills/*/SKILL.md with name and description frontmatter under {args.root}')
names = set(skills)
known = names | {d['name'] for d in load_distractors()} | {'none'}
coverage = dict.fromkeys(skills, 0)
ids = set()
sets = {src: load_prompts(HERE / src) for src in ('prompts.jsonl', 'holdout.jsonl')}
for src, prompts in sets.items():
    for p in prompts:
        where = f'{src}:{p.get("id")}'
        if p['id'] in ids:
            errors.append(f'{where}: duplicate id')
        ids.add(p['id'])
        if p['kind'] not in ('positive', 'negative'):
            errors.append(f'{where}: kind must be positive or negative')
        if not p['accept']:
            errors.append(f'{where}: accept list is empty')
        for label in p['accept']:
            if label not in known:
                errors.append(f'{where}: unknown skill label {label!r}')
            elif p['kind'] == 'positive' and label in coverage and src == 'prompts.jsonl':
                coverage[label] += 1
        if p['kind'] == 'negative' and set(p['accept']) & names:
            errors.append(f'{where}: a negative prompt must not accept a suite skill')
for name, count in coverage.items():
    if count < 1:
        errors.append(f'skill {name} has no positive trigger prompt; add one to evals/triggers/prompts.jsonl')


def check_result(result_name, path, floor, protocol):
    try:
        r = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [f'{result_name}: unreadable result ({exc})']
    if not isinstance(r, dict) or not isinstance(r.get('rows'), list):
        return [f'{result_name}: malformed result (no rows)']
    out = []
    for key in ('model', 'effort', 'passes'):
        if r.get(key) != protocol[key]:
            out.append(f'{result_name}: {key} is {r.get(key)!r}; the baseline protocol requires {protocol[key]!r}')
    if r.get('partial') is not False:
        out.append(f'{result_name}: partial run (--only) or missing "partial": false; run the full set')
    if r.get('prompt_set') != floor['prompts']:
        out.append(f'{result_name}: was run on prompt set {r.get("prompt_set")!r}, expected {floor["prompts"]!r}')
    prompts = sets[floor['prompts']]
    if r.get('descriptions_sha256') != descriptions_sha256(skills):
        out.append(f'{result_name}: was run on different skill descriptions; rerun evals/triggers/run.py')
    if r.get('inputs_sha256') != inputs_sha256(prompts):
        out.append(f'{result_name}: was run on different prompts, labels, distractors or protocol; rerun evals/triggers/run.py')
    passes = protocol['passes']
    by_id = {}
    for row in r['rows']:
        if not isinstance(row, dict) or not isinstance(row.get('choices'), list):
            out.append(f'{result_name}: malformed row {row!r}')
            continue
        if len(row['choices']) != passes or not all(isinstance(c, str) and c for c in row['choices']):
            out.append(f'{result_name}: row {row.get("id")} needs {passes} non-empty choices, got {row["choices"]!r}')
        if row.get('id') in by_id:
            out.append(f'{result_name}: duplicate row {row.get("id")}')
        by_id[row.get('id')] = row
    want = {p['id']: p for p in prompts}
    missing, extra = sorted(set(want) - set(by_id)), sorted(set(by_id) - set(want), key=str)
    if missing:
        out.append(f'{result_name}: missing rows for {", ".join(missing)}')
    if extra:
        out.append(f'{result_name}: rows for unknown prompts {extra}')
    for pid, row in by_id.items():
        if pid in want and (row.get('kind'), row.get('accept')) != (want[pid]['kind'], want[pid]['accept']):
            out.append(f'{result_name}: row {pid} has labels that differ from {floor["prompts"]}')
    if out:
        return out
    got = score(prompts, {pid: by_id[pid]['choices'] for pid in want}, names, passes)
    for key, value in got.items():
        if r.get(key) != value:
            out.append(f'{result_name}: reported {key} {r.get(key)!r} does not match {value!r} recomputed from its rows')
    if not got['positives'] or not got['negatives']:
        out.append(f'{result_name}: needs both positive and negative prompts')
        return out
    if got['errors']:
        out.append(f'{result_name}: {got["errors"]} model calls failed')
    if got['hit_rate'] < floor['min_hit_rate']:
        out.append(f'{result_name}: hit rate {got["hit_rate"]:.1%} is below the baseline {floor["min_hit_rate"]:.1%}')
    if got['false_fire_rate'] > floor['max_false_fire_rate']:
        out.append(f'{result_name}: false-fire rate {got["false_fire_rate"]:.1%} is above the baseline {floor["max_false_fire_rate"]:.1%}')
    return out


thresholds = json.loads((HERE / 'thresholds.json').read_text())
overrides = dict(item.split('=', 1) for item in args.result)
if not thresholds.get('required_results'):
    errors.append('thresholds.json lists no required results')
for result_name in thresholds.get('required_results', []):
    path = Path(overrides[result_name]) if result_name in overrides else HERE / 'results' / result_name
    if not path.is_file():
        errors.append(f'missing eval result {path}; run evals/triggers/run.py')
        continue
    errors += check_result(result_name, path, thresholds['results'][result_name], thresholds['protocol'])

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(ids)} trigger prompts cover {len(skills)} skills; committed eval results are complete, '
      'match the current descriptions and prompts, and meet the baseline floors')
