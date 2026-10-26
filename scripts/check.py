#!/usr/bin/env python3
"""Check the published skill package; optionally sync its install entrypoint."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sync', action='store_true', help='Copy myelinate.md to SKILL.md before checking')
args = parser.parse_args()
source = ROOT / 'myelinate.md'
entry = ROOT / 'SKILL.md'
sys.path.insert(0, str(ROOT / 'scripts'))
import package
if args.sync:
    entry.write_bytes(source.read_bytes())
    package.build()
errors = []
required = ['myelinate.md', 'SKILL.md', 'agents/openai.yaml', 'references/evidence.md',
            'references/research-method.md', 'references/inclusive-teaching.md',
            'references/session-template.md', 'references/production-lessons.md', 'README.md', 'LICENSE',
            'examples/lesson.html', 'examples/oxygen-lab.html', 'assets/hero.svg', 'assets/logo.svg',
            'assets/logo-mark.svg', 'index.html', 'evals/scenarios.md', 'evals/verification.md',
            'references/subject-playbooks.md', 'references/media-sources.md',
            'templates/lab-standalone.html', 'templates/dbaney-lab.json', 'templates/lab-spec.md',
            'templates/learner-profile.md', 'templates/practice-test.html', 'references/teaching-methods.md', 'references/how-the-mind-learns.md',
            'references/dbaney-study-lab.md', 'references/first-session.md', 'references/visual-teaching.md', 'references/skill-map.md', 'references/personalization.md',
            'templates/visual-stepper.html', 'NOTICE.md', 'tests/visual_journey.py',
            'templates/course-project-prompt.md', 'templates/gradebook.md', '.claude-plugin/plugin.json',
            '.claude-plugin/marketplace.json', '.codex-plugin/plugin.json', '.agents/plugins/marketplace.json',
            'output-styles/myelinate.md', 'commands/quiz.md', 'commands/review.md', 'agents/key-worker.md',
            'hooks/hooks.json', 'hooks/due_reviews.py', 'references/learner-record.md', 'skills/myelinate/SKILL.md', 'llms.txt', 'scripts/make_pdf.py',
            'scripts/package.py', 'examples/practice-test-oxygen.pdf']
SUBSKILLS = ['teach', 'tutor', 'assignment', 'project', 'code', 'assess', 'course-project', 'notes', 'lab', 'print',
             'flashcards', 'memory-hooks', 'study-plan', 'find-media', 'verify']
required += [f'skills/{name}/SKILL.md' for name in SUBSKILLS]
for name in required:
    if not (ROOT / name).is_file():
        errors.append(f'Missing required file: {name}')
if entry.exists() and source.read_bytes() != entry.read_bytes():
    errors.append('SKILL.md differs from myelinate.md; run --sync and review the diff')
body = source.read_text()
# Skill listings give each skill a shared character budget. When the budget runs
# out, long descriptions are dropped and the skill shows by name only, so it never
# auto-loads. Keep every description short, trigger-first, and valid YAML.
DESCRIPTION_MAX = 175


def check_description(label, raw):
    if raw.startswith('"'):
        if not raw.endswith('"') or '"' in raw[1:-1] or '\\' in raw:
            errors.append(f'{label}: quoted description must be one plain double-quoted string')
            return
        text = raw[1:-1]
    else:
        text = raw
        if ': ' in text or ' #' in text or text[:1] in '\'&*!|>%@`[{':
            errors.append(f'{label}: description is not valid plain YAML; wrap it in double quotes')
    if len(text) > DESCRIPTION_MAX:
        errors.append(f'{label}: description is {len(text)} characters; keep it to {DESCRIPTION_MAX} or less so skill listings keep it')
    if not text.startswith('Use '):
        errors.append(f'{label}: description should open with when to use it ("Use when ..." or "Use for ...")')


frontmatter = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', body)
if not frontmatter or frontmatter.group(1) != 'myelinate':
    errors.append('Invalid required skill frontmatter')
else:
    check_description('myelinate.md', frontmatter.group(2))
for name in SUBSKILLS:
    sub = ROOT / 'skills' / name / 'SKILL.md'
    if sub.is_file():
        match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', sub.read_text())
        if not match or match.group(1) != name:
            errors.append(f'skills/{name}/SKILL.md: invalid frontmatter')
        else:
            check_description(f'skills/{name}/SKILL.md', match.group(2))
    if f'skills/{name}/SKILL.md' not in body:
        errors.append(f'Router does not route to skills/{name}/SKILL.md')
    for public in ('llms.txt', 'index.html', 'README.md'):
        if f'skills/{name}/SKILL.md' not in (ROOT / public).read_text():
            errors.append(f'{public} does not list skills/{name}/SKILL.md')

for manifest in ('.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', '.codex-plugin/plugin.json',
                 '.agents/plugins/marketplace.json'):
    path = ROOT / manifest
    if path.is_file():
        import json
        try:
            data = json.loads(path.read_text())
        except ValueError as exc:
            errors.append(f'{manifest}: invalid JSON ({exc})')
            continue
        if manifest.endswith('plugin.json'):
            version = re.search(r'^Version ([0-9.]+) ', body, re.M)
            if data.get('name') != 'myelinate':
                errors.append(f'{manifest}: name must be myelinate')
            # Claude Code treats a plugin without a version as versioned by commit,
            # so installs that track a branch update on every push.
            if manifest.startswith('.claude-plugin') and 'version' in data:
                errors.append(f'{manifest}: leave out version so installs update by commit')
            if manifest.startswith('.claude-plugin') and 'skills' in data:
                errors.append(f'{manifest}: leave out skills; the router lives at skills/myelinate')
            if manifest.startswith('.claude-plugin') and data.get('description') != json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())['plugins'][0].get('description'):
                errors.append('.claude-plugin/marketplace.json: plugin description differs from plugin.json (claude.ai shows the marketplace one)')
            if manifest.startswith('.codex-plugin') and version and data.get('version') != version.group(1):
                errors.append(f'{manifest}: version differs from myelinate.md')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
    def handle_starttag(self, tag, attrs):
        self.targets.extend(value for key, value in attrs if key in ('href', 'src') and value)

count = 0
for path in sorted(ROOT.rglob('*')):
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
        continue
    if path.suffix not in ('.md', '.html') or not path.is_file():
        continue
    content = path.read_text()
    links = Links()
    links.feed(content)
    targets = links.targets + re.findall(r'\]\(([^\s)]+)\)', content)
    for target in targets:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        dest = (path.parent / unquote(parsed.path)).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():
            errors.append(f'{path.relative_to(ROOT)}: broken/escaping local link: {target}')
        count += 1
# The SessionStart hook must stay silent without a record and list due reviews with one.
import json, os, subprocess, tempfile
with tempfile.TemporaryDirectory() as home:
    env = {**os.environ, 'MYELINATE_HOME': home, 'MYELINATE_TODAY': '2026-10-14'}
    hook = [sys.executable, str(ROOT / 'hooks' / 'due_reviews.py')]
    if subprocess.run(hook, env=env, capture_output=True, text=True).stdout.strip():
        errors.append('hooks/due_reviews.py: prints output with no learner record')
    Path(home, 'learner.json').write_text(json.dumps({'version': 1, 'topics': [
        {'topic': 'Limiting reactants', 'course': 'CHEM 111', 'next_review': '2026-10-13'},
        {'topic': 'Hess law', 'next_review': '2026-10-20'}]}))
    out = subprocess.run(hook, env=env, capture_output=True, text=True).stdout
    if 'Limiting reactants (CHEM 111)' not in out or 'Hess' in out or '1 review' not in out:
        errors.append(f'hooks/due_reviews.py: wrong due list: {out!r}')
    Path(home, 'learner.json').write_text('{not json')
    if subprocess.run(hook, env=env, capture_output=True, text=True).returncode != 0:
        errors.append('hooks/due_reviews.py: a broken record must not fail the session')
package_errors, package_counts = package.verify()
errors += package_errors
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(required)} required files, identical skill entrypoints, {count} local links')
print(f'PASS: {len(package_counts)} skills in {package.ZIP.relative_to(ROOT)}; '
      f'all {sum(package_counts.values())} referenced paths present in the package')
print('This checks packaging, not teaching quality, external URLs, or learning outcomes.')
