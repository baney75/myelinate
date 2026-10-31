#!/usr/bin/env python3
"""Rejection tests for check.py: it must pass a complete, consistent result and
fail every empty, partial, malformed, inconsistent, stale or below-floor one.

Uses synthetic results, so it needs no model. Run: python3 evals/triggers/test_check.py
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import HERE, descriptions_sha256, inputs_sha256, load_prompts, score, suite

ROOT = HERE.parents[1]
THRESHOLDS = json.loads((HERE / 'thresholds.json').read_text())
PROTOCOL = THRESHOLDS['protocol']
SKILLS = suite(ROOT)


def perfect(prompt_set):
    prompts = load_prompts(HERE / prompt_set)
    choices = {p['id']: [p['accept'][0]] * PROTOCOL['passes'] for p in prompts}
    rows = [{'id': p['id'], 'kind': p['kind'], 'accept': p['accept'], 'choices': choices[p['id']],
             'ok': PROTOCOL['passes']} for p in prompts]
    return {**PROTOCOL, 'prompt_set': prompt_set, 'partial': False,
            'descriptions_sha256': descriptions_sha256(SKILLS), 'inputs_sha256': inputs_sha256(prompts),
            **score(prompts, choices, set(SKILLS), PROTOCOL['passes']), 'rows': rows}


def run(tmp, latest, holdout, root=ROOT):
    paths = []
    for name, data in (('latest.json', latest), ('holdout.json', holdout)):
        path = Path(tmp) / name
        path.write_text(data if isinstance(data, str) else json.dumps(data))
        paths += ['--result', f'{name}={path}']
    proc = subprocess.run([sys.executable, str(HERE / 'check.py'), '--root', str(root), *paths],
                          capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout + proc.stderr


def rescore(r):
    present = {row['id'] for row in r['rows']}
    prompts = [p for p in load_prompts(HERE / r['prompt_set']) if p['id'] in present]
    r.update(score(prompts, {row['id']: row['choices'] for row in r['rows']}, set(SKILLS), PROTOCOL['passes']))
    return r


def mutate(fn):
    r = perfect('prompts.jsonl')
    fn(r)
    return r


def miss_positives(r, count):
    for row in [row for row in r['rows'] if row['kind'] == 'positive'][:count]:
        row['choices'] = ['none'] * PROTOCOL['passes']
    rescore(r)


CASES = {
    'empty rows': lambda r: (r.update(rows=[]), rescore(r)),
    'zero passes': lambda r: r.update(passes=0),
    'partial run flag': lambda r: r.update(partial=True),
    'two-prompt report': lambda r: (r.update(rows=r['rows'][:2]), rescore(r)),
    'missing rows key': lambda r: r.pop('rows'),
    'short choices': lambda r: r['rows'][0].update(choices=r['rows'][0]['choices'][:1]),
    'empty choice': lambda r: r['rows'][0].update(choices=[''] * PROTOCOL['passes']),
    'duplicate row': lambda r: r['rows'].append(copy.deepcopy(r['rows'][0])),
    'unknown row': lambda r: r['rows'].append({**copy.deepcopy(r['rows'][0]), 'id': 'zz99'}),
    'changed labels': lambda r: r['rows'][0].update(accept=['print']),
    'summary disagrees with rows': lambda r: (miss_positives(r, 1), r.update(hit_rate=1.0)),
    'stale prompts or protocol': lambda r: r.update(inputs_sha256='0' * 64),
    'stale descriptions': lambda r: r.update(descriptions_sha256='0' * 64),
    'different model': lambda r: r.update(model='another-model'),
    'different effort': lambda r: r.update(effort='high'),
    'wrong prompt set': lambda r: r.update(prompt_set='holdout.jsonl'),
    'below hit floor': lambda r: miss_positives(r, 3),
    'model errors': lambda r: (r['rows'][0].update(choices=['ERROR'] * PROTOCOL['passes']), rescore(r)),
}


EXPECT = {
    'empty rows': 'missing rows',
    'zero passes': 'passes is 0',
    'partial run flag': 'partial run',
    'two-prompt report': 'missing rows',
    'missing rows key': 'malformed result',
    'short choices': 'non-empty choices',
    'empty choice': 'non-empty choices',
    'duplicate row': 'duplicate row',
    'unknown row': 'unknown prompts',
    'changed labels': 'labels that differ',
    'summary disagrees with rows': 'does not match',
    'stale prompts or protocol': 'different prompts',
    'stale descriptions': 'different skill descriptions',
    'different model': 'model is',
    'different effort': 'effort is',
    'wrong prompt set': 'prompt set',
    'below hit floor': 'below the baseline',
    'model errors': 'model calls failed',
}


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run(tmp, perfect('prompts.jsonl'), perfect('holdout.jsonl'))
        if code != 0:
            failures.append(f'complete result should pass:\n{out}')
        for name, fn in CASES.items():
            code, out = run(tmp, mutate(fn), perfect('holdout.jsonl'))
            if code == 0:
                failures.append(f'{name}: should fail but passed')
            elif EXPECT[name] not in out:
                failures.append(f'{name}: failed for another reason:\n{out}')
        code, _ = run(tmp, '{not json', perfect('holdout.jsonl'))
        if code == 0:
            failures.append('malformed JSON: should fail but passed')
        copy_root = Path(tmp) / 'repo'
        shutil.copytree(ROOT / 'skills', copy_root / 'skills')
        target = copy_root / 'skills' / 'tutor' / 'SKILL.md'
        target.write_text(target.read_text().replace('description: "', 'description: "Changed. ', 1))
        code, out = run(tmp, perfect('prompts.jsonl'), perfect('holdout.jsonl'), root=copy_root)
        if code == 0 or 'different skill descriptions' not in out:
            failures.append('edited description: should fail but passed')
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        sys.exit(1)
    print(f'PASS: check.py accepts a complete result and rejects {len(CASES) + 2} broken ones')


main()
