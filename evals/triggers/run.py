#!/usr/bin/env python3
"""Model-based trigger eval: which skill would an agent load for each prompt?

Installs a stub of every skill (its real name and description, no body) plus a
fixed set of distractor skills into an isolated HOME, so the agent lists them
the way it lists any installed skill. Then it asks, once per prompt and pass,
which skill it would load before replying. No skill bodies are read.

usage: python3 evals/triggers/run.py [--root REPO] [--model M] [--effort E]
                                     [--passes N] [--jobs J] [--out FILE]

Needs the Codex CLI, signed in. The isolated HOME links to your Codex auth file
(it is never read or copied by this script), so host skills, AGENTS.md files
and plugins do not leak into the listing. Default model and effort are fixed so
runs are comparable; the CLI does not expose temperature, so run several passes.
"""
import argparse, concurrent.futures as cf, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('--root', default=str(HERE.parents[1]), help='repo whose skills to evaluate')
ap.add_argument('--model', default='gpt-5.6-luna')
ap.add_argument('--effort', default='low')
ap.add_argument('--passes', type=int, default=3)
ap.add_argument('--jobs', type=int, default=6)
ap.add_argument('--out', default=None, help='results JSON (default: print summary only)')
ap.add_argument('--codex', default=shutil.which('codex') or 'codex')
ap.add_argument('--auth', default=str(Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'auth.json'))
ap.add_argument('--only', default='', help='comma-separated prompt ids')
ap.add_argument('--prompts', default=str(HERE / 'prompts.jsonl'), help='prompt set (JSONL)')
args = ap.parse_args()

FM = re.compile(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n', re.S)


def suite(root):
    skills = {}
    for path in sorted(Path(root, 'skills').glob('*/SKILL.md')):
        m = FM.match(path.read_text())
        if m:
            skills[m.group(1)] = m.group(2).strip().strip('"')
    return skills


def fingerprint(skills):
    blob = '\n'.join(f'{k}: {v}' for k, v in sorted(skills.items()))
    return hashlib.sha256(blob.encode()).hexdigest()


ASK = """This is a skill-routing check. Below is the first message a user sent you in a new chat.
Do not answer it, run commands or open files. Using your normal rules for when to load a skill,
decide which ONE of your available skills you would load before replying, or none if no skill fits.
Reply with JSON only: {{"skill": "<exact skill name>"}} or {{"skill": "none"}}.

User message:
<<<
{prompt}
>>>"""
SCHEMA = {"type": "object", "properties": {"skill": {"type": "string"}}, "required": ["skill"], "additionalProperties": False}


def main():
    skills = suite(args.root)
    distractors = json.loads((HERE / 'distractors.json').read_text())
    prompts = [json.loads(l) for l in Path(args.prompts).read_text().splitlines() if l.strip()]
    if args.only:
        keep = set(args.only.split(','))
        prompts = [p for p in prompts if p['id'] in keep]
    home = Path(tempfile.mkdtemp(prefix='myel-trigger-'))
    try:
        codex_home = home / '.codex'
        codex_home.mkdir()
        (codex_home / 'auth.json').symlink_to(args.auth)
        work = home / 'work'
        work.mkdir()
        for name, desc in list(skills.items()) + [(d['name'], d['description']) for d in distractors]:
            d = home / '.agents' / 'skills' / name
            d.mkdir(parents=True)
            (d / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: "{desc}"\n---\n\nStub for trigger evaluation.\n')
        schema = home / 'schema.json'
        schema.write_text(json.dumps(SCHEMA))
        env = {**os.environ, 'HOME': str(home), 'CODEX_HOME': str(codex_home)}

        def ask(job):
            pid, pas, text = job
            out = home / f'{pid}-{pas}.txt'
            cmd = [args.codex, 'exec', '-m', args.model, '-c', f'model_reasoning_effort={args.effort}',
                   '-s', 'read-only', '--skip-git-repo-check', '--ephemeral', '--ignore-rules', '--color', 'never',
                   '--output-schema', str(schema), '-C', str(work), '-o', str(out), '-']
            for attempt in range(3):
                r = subprocess.run(cmd, input=ASK.format(prompt=text), env=env, capture_output=True, text=True, timeout=300)
                try:
                    return pid, pas, json.loads(out.read_text())['skill'].strip()
                except Exception:
                    continue
            return pid, pas, 'ERROR'

        jobs = [(p['id'], n, p['prompt']) for n in range(args.passes) for p in prompts]
        choices = {p['id']: [None] * args.passes for p in prompts}
        with cf.ThreadPoolExecutor(args.jobs) as pool:
            for pid, pas, skill in pool.map(ask, jobs):
                choices[pid][pas] = skill.split(':')[-1]
    finally:
        shutil.rmtree(home, ignore_errors=True)

    names = set(skills)
    pos = [p for p in prompts if p['kind'] == 'positive']
    neg = [p for p in prompts if p['kind'] == 'negative']
    per_pass = []
    for n in range(args.passes):
        hit = sum(choices[p['id']][n] in p['accept'] for p in pos)
        ff = sum(choices[p['id']][n] in names for p in neg)
        per_pass.append({'hit': hit, 'false_fire': ff})
    majority = {pid: Counter(c).most_common(1)[0][0] for pid, c in choices.items()}
    rows = []
    for p in prompts:
        c = choices[p['id']]
        ok = [(x in p['accept']) if p['kind'] == 'positive' else (x not in names) for x in c]
        rows.append({'id': p['id'], 'kind': p['kind'], 'accept': p['accept'], 'choices': c, 'ok': sum(ok)})
    result = {
        'model': args.model, 'effort': args.effort, 'passes': args.passes, 'harness': 'codex exec, isolated HOME, skills in ~/.agents/skills', 'prompt_set': Path(args.prompts).name,
        'descriptions_sha256': fingerprint(skills), 'skills': sorted(names),
        'positives': len(pos), 'negatives': len(neg),
        'hit_rate': round(sum(x['hit'] for x in per_pass) / (len(pos) * args.passes), 4) if pos else None,
        'false_fire_rate': round(sum(x['false_fire'] for x in per_pass) / (len(neg) * args.passes), 4) if neg else None,
        'majority_hit_rate': round(sum(majority[p['id']] in p['accept'] for p in pos) / len(pos), 4) if pos else None,
        'majority_false_fire_rate': round(sum(majority[p['id']] in names for p in neg) / len(neg), 4) if neg else None,
        'per_pass': per_pass,
        'unstable': [r['id'] for r in rows if len(set(r['choices'])) > 1],
        'errors': sum(c.count('ERROR') for c in choices.values()),
        'rows': rows,
    }
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=1) + '\n')
    print(f"model {args.model} ({args.effort}), {args.passes} passes, {len(pos)} positives, {len(neg)} negatives")
    print(f"hit rate {result['hit_rate']:.1%} (majority {result['majority_hit_rate']:.1%}); "
          f"false-fire rate {result['false_fire_rate']:.1%} (majority {result['majority_false_fire_rate']:.1%}); errors {result['errors']}")
    for r in rows:
        if r['ok'] < args.passes:
            print(f"  {r['id']} {r['kind']}: got {r['choices']} want {r['accept']}")


main()
