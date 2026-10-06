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
if args.sync:
    entry.write_bytes(source.read_bytes())
errors = []
required = ['myelinate.md', 'SKILL.md', 'agents/openai.yaml', 'references/evidence.md',
            'references/research-method.md', 'references/inclusive-teaching.md',
            'references/session-template.md', 'references/production-lessons.md', 'README.md', 'LICENSE',
            'examples/lesson.html', 'examples/oxygen-lab.html', 'assets/hero.svg', 'assets/logo.svg',
            'assets/logo-mark.svg', 'index.html', 'evals/scenarios.md', 'evals/verification.md',
            'references/subject-playbooks.md', 'references/media-sources.md',
            'templates/lab-standalone.html', 'templates/dbaney-lab.json', 'templates/lab-spec.md',
            'templates/learner-profile.md', 'templates/practice-test.html', 'references/teaching-methods.md',
            'references/dbaney-study-lab.md', 'llms.txt', 'scripts/make_pdf.py', 'examples/practice-test-oxygen.pdf']
SUBSKILLS = ['teach', 'tutor', 'lab', 'print', 'flashcards', 'memory-hooks', 'study-plan', 'find-media', 'verify']
required += [f'skills/{name}/SKILL.md' for name in SUBSKILLS]
for name in required:
    if not (ROOT / name).is_file():
        errors.append(f'Missing required file: {name}')
if entry.exists() and source.read_bytes() != entry.read_bytes():
    errors.append('SKILL.md differs from myelinate.md; run --sync and review the diff')
body = source.read_text()
frontmatter = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', body)
if not frontmatter or frontmatter.group(1) != 'myelinate':
    errors.append('Invalid required skill frontmatter')
for name in SUBSKILLS:
    sub = ROOT / 'skills' / name / 'SKILL.md'
    if sub.is_file():
        match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', sub.read_text())
        if not match or match.group(1) != name:
            errors.append(f'skills/{name}/SKILL.md: invalid frontmatter')
        elif len(match.group(2)) > 1024:
            errors.append(f'skills/{name}/SKILL.md: description over 1024 characters')
    if f'skills/{name}/SKILL.md' not in body:
        errors.append(f'Router does not route to skills/{name}/SKILL.md')

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
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(required)} required files, identical skill entrypoints, {count} local links')
print('This checks packaging, not teaching quality, external URLs, or learning outcomes.')
