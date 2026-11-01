#!/usr/bin/env python3
"""Score evals/invocation/run.sh transcripts: which Myelinate skills each session loaded.

Counts a skill only when its Skill tool call came back without an error, and only the plugin's
namespaced skills (myelinate:<name>); a call to a standalone skill merely named "myelinate" and a
failed call are listed separately. A session is an error, left out of both rates, when it has no
final result event that succeeded or stopped at --max-turns, or when its init event shows a
myelinate plugin loaded from anywhere but the plugin under test (argv[2]). Exits 1 on any error.
"""
import json
import sys
from pathlib import Path

under_test = str(Path(sys.argv[2]).resolve()) if len(sys.argv) > 2 else None
rows, errors = [], []
for path in sorted(Path(sys.argv[1]).glob('*.jsonl')):
    name = path.stem
    calls, results, other, ok, stray = {}, {}, set(), False, []
    for line in path.read_text(errors='replace').splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind = event.get('type')
        if kind == 'system' and event.get('subtype') == 'init' and under_test:
            stray = [p.get('source') or p.get('name') for p in event.get('plugins', [])
                     if 'myelinate' in str(p.get('name', '')) and str(Path(p.get('path', '')).resolve()) != under_test]
        for part in event.get('message', {}).get('content', []) if kind in ('assistant', 'user') else []:
            if not isinstance(part, dict):
                continue
            if part.get('type') == 'tool_use' and part.get('name') == 'Skill':
                skill = str(part.get('input', {}).get('skill', ''))
                if skill.startswith('myelinate:'):
                    calls[part.get('id')] = skill
                elif 'myelinate' in skill:
                    other.add(skill)
            if part.get('type') == 'tool_result' and part.get('tool_use_id') in calls:
                results[part['tool_use_id']] = not part.get('is_error')
        if kind == 'result':
            # A session stopped by --max-turns still made its skill decision on the first turn, so it counts.
            ok = event.get('subtype') == 'error_max_turns' or (event.get('subtype') == 'success' and not event.get('is_error'))
    if stray:
        errors.append(name)
        print(f'{name} ERROR (another myelinate plugin loaded: {", ".join(stray)})')
        continue
    if not ok:
        errors.append(name)
        print(f'{name} ERROR (no successful result event)')
        continue
    loaded = {skill for cid, skill in calls.items() if results.get(cid)}
    failed = {skill for cid, skill in calls.items() if not results.get(cid)}
    notes = (f'  [standalone: {" ".join(sorted(other))}]' if other else '') + \
            (f'  [failed or no result: {" ".join(sorted(failed))}]' if failed else '')
    print(f'{name} {" ".join(sorted(loaded)) or "none"}{notes}')
    rows.append((name, bool(loaded)))
pos = [hit for name, hit in rows if name.startswith('P')]
neg = [hit for name, hit in rows if name.startswith('N')]
print(f'loaded on {sum(pos)}/{len(pos)} learning prompts, {sum(neg)}/{len(neg)} work prompts, {len(errors)} errors')
sys.exit(1 if errors else 0)
