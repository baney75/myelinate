#!/usr/bin/env python3
"""Deterministic trigger guard for CI (no model, no secrets).

Fails when:
- a prompt label names a skill that does not exist (suite, distractor or "none");
- a skill has fewer than two positive prompts that accept it;
- the committed eval result was produced for different skill descriptions
  (descriptions changed without rerunning `evals/triggers/run.py`);
- the committed result is below the baseline thresholds in thresholds.json.

The model eval itself is a required local step: see evals/triggers/README.md.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FM = re.compile(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n', re.DOTALL)
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--result', action='append', default=[], metavar='NAME=PATH',
                help='check a fresh result file against the floor for NAME (for example latest.json=/tmp/r.json)')
args = ap.parse_args()
errors = []

skills = {}
for path in sorted((ROOT / 'skills').glob('*/SKILL.md')):
    m = FM.match(path.read_text())
    if not m:
        errors.append(f'skills/{path.parent.name}/SKILL.md: no name/description frontmatter')
        continue
    skills[m.group(1)] = m.group(2).strip().strip('"')
fingerprint = hashlib.sha256('\n'.join(f'{k}: {v}' for k, v in sorted(skills.items())).encode()).hexdigest()

distractors = {d['name'] for d in json.loads((HERE / 'distractors.json').read_text())}
known = set(skills) | distractors | {'none'}
coverage = {name: 0 for name in skills}
ids = set()
lines = [('prompts.jsonl', n, line) for n, line in enumerate((HERE / 'prompts.jsonl').read_text().splitlines(), 1)]
lines += [('holdout.jsonl', n, line) for n, line in enumerate((HERE / 'holdout.jsonl').read_text().splitlines(), 1)]
for src, n, line in lines:
    if not line.strip():
        continue
    p = json.loads(line)
    if p['id'] in ids:
        errors.append(f'{src}:{n}: duplicate id {p["id"]}')
    ids.add(p['id'])
    if p['kind'] not in ('positive', 'negative'):
        errors.append(f'{src}:{n}: kind must be positive or negative')
    for label in p['accept']:
        if label not in known:
            errors.append(f'{src}:{n}: unknown skill label {label!r}')
        elif p['kind'] == 'positive' and label in coverage and src == 'prompts.jsonl':
            coverage[label] += 1
    if p['kind'] == 'negative' and set(p['accept']) & set(skills):
        errors.append(f'{src}:{n}: a negative prompt must not accept a suite skill')
for name, count in coverage.items():
    if count < 1:
        errors.append(f'skill {name} has {count} positive trigger prompts; add at least 1 to evals/triggers/prompts.jsonl')

thresholds = json.loads((HERE / 'thresholds.json').read_text())
overrides = dict(item.split('=', 1) for item in args.result)
for result_name in thresholds['required_results']:
    path = Path(overrides[result_name]) if result_name in overrides else HERE / 'results' / result_name
    if not path.is_file():
        errors.append(f'missing eval result {path}; run evals/triggers/run.py')
        continue
    r = json.loads(path.read_text())
    if r.get('prompt_set') != thresholds['results'][result_name]['prompts']:
        errors.append(f'{result_name}: was run on prompt set {r.get("prompt_set")!r}, expected {thresholds["results"][result_name]["prompts"]!r}')
    if r['descriptions_sha256'] != fingerprint:
        errors.append(f'{path.name} was run on different skill descriptions; rerun evals/triggers/run.py and write evals/triggers/results/{result_name}')
    if r['errors']:
        errors.append(f'{path.name}: {r["errors"]} model calls failed')
    floor = thresholds['results'][result_name]
    if r['hit_rate'] < floor['min_hit_rate']:
        errors.append(f'{path.name}: hit rate {r["hit_rate"]:.1%} is below the baseline {floor["min_hit_rate"]:.1%}')
    if r['false_fire_rate'] > floor['max_false_fire_rate']:
        errors.append(f'{path.name}: false-fire rate {r["false_fire_rate"]:.1%} is above the baseline {floor["max_false_fire_rate"]:.1%}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(ids)} trigger prompts cover {len(skills)} skills; committed eval results match current descriptions and meet baseline thresholds')
