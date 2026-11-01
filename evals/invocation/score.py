#!/usr/bin/env python3
"""Score evals/invocation/run.sh transcripts: which Myelinate skills each session called.

Counts only the plugin's namespaced skills (myelinate:<name>). A call to a standalone skill
that is merely named "myelinate" is reported separately, not as a hit. A session without a
final result event that succeeded or stopped at --max-turns is an error and is left out of both rates. Exits 1 on any error.
"""
import json
import sys
from pathlib import Path

rows, errors = [], []
for path in sorted(Path(sys.argv[1]).glob('*.jsonl')):
    name = path.stem
    plugin, other, ok = set(), set(), False
    for line in path.read_text(errors='replace').splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get('type') == 'assistant':
            for part in event.get('message', {}).get('content', []):
                if part.get('type') == 'tool_use' and part.get('name') == 'Skill':
                    skill = str(part.get('input', {}).get('skill', ''))
                    if skill.startswith('myelinate:'):
                        plugin.add(skill)
                    elif 'myelinate' in skill:
                        other.add(skill)
        if event.get('type') == 'result':
            # A session stopped by --max-turns still made its skill decision on the first turn, so it counts.
            ok = event.get('subtype') == 'error_max_turns' or (event.get('subtype') == 'success' and not event.get('is_error'))
    if not ok:
        errors.append(name)
        print(f'{name} ERROR (no successful result event)')
        continue
    extra = f'  [standalone: {" ".join(sorted(other))}]' if other else ''
    print(f'{name} {" ".join(sorted(plugin)) or "none"}{extra}')
    rows.append((name, bool(plugin)))
pos = [hit for name, hit in rows if name.startswith('P')]
neg = [hit for name, hit in rows if name.startswith('N')]
print(f'loaded on {sum(pos)}/{len(pos)} learning prompts, {sum(neg)}/{len(neg)} work prompts, {len(errors)} errors')
sys.exit(1 if errors else 0)
