"""Shared definitions for the trigger eval (run.py) and its CI guard (check.py).

Both scripts fingerprint their inputs from here, so a committed result is tied
to the exact skill descriptions, prompt set, distractors and question protocol
it was produced with.
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FM = re.compile(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n', re.DOTALL)
HARNESS = 'codex exec, isolated HOME, skills in ~/.agents/skills'
ASK = """This is a skill-routing check. Below is the first message a user sent you in a new chat.
Do not answer it, run commands or open files. Using your normal rules for when to load a skill,
decide which ONE of your available skills you would load before replying, or none if no skill fits.
Reply with JSON only: {{"skill": "<exact skill name>"}} or {{"skill": "none"}}.

User message:
<<<
{prompt}
>>>"""
SCHEMA = {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"], "additionalProperties": False}


def suite(root):
    """Name and description of every skills/*/SKILL.md under root."""
    skills = {}
    for path in sorted(Path(root, 'skills').glob('*/SKILL.md')):
        m = FM.match(path.read_text())
        if m:
            skills[m.group(1)] = m.group(2).strip().strip('"')
    return skills


def descriptions_sha256(skills):
    blob = '\n'.join(f'{k}: {v}' for k, v in sorted(skills.items()))
    return hashlib.sha256(blob.encode()).hexdigest()


def load_prompts(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def load_distractors():
    return json.loads((HERE / 'distractors.json').read_text())


def inputs_sha256(prompts):
    """Fingerprint of everything besides descriptions that shapes a result."""
    blob = json.dumps({'prompts': prompts, 'distractors': load_distractors(), 'ask': ASK,
                       'schema': SCHEMA, 'harness': HARNESS}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def score(prompts, choices, suite_names, passes):
    """Recompute rates from per-prompt choices. choices maps id to a list of skill names."""
    pos = [p for p in prompts if p['kind'] == 'positive']
    neg = [p for p in prompts if p['kind'] == 'negative']
    hits = sum(c in p['accept'] for p in pos for c in choices[p['id']])
    fires = sum(c in suite_names for p in neg for c in choices[p['id']])
    return {
        'positives': len(pos), 'negatives': len(neg),
        'hit_rate': round(hits / (len(pos) * passes), 4) if pos else None,
        'false_fire_rate': round(fires / (len(neg) * passes), 4) if neg else None,
        'errors': sum(c.count('ERROR') for c in choices.values()),
    }
