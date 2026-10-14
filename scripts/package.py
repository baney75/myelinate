#!/usr/bin/env python3
"""Build Myelinate's plugin package and verify it.

Hosts install a plugin skill by skill, and some copy only a skill's own
folder. So every skill folder carries a copy of each shared file it names
(references, templates, examples, scripts, assets), and the router gets a
folder of its own at skills/myelinate. The sources stay at the repository
root; the copies are generated here and checked for drift.

    python3 scripts/package.py build    # regenerate copies and dist/myelinate-plugin.zip
    python3 scripts/package.py verify   # fail on drift or any referenced path missing from the zip
"""
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SHARED = ('references', 'templates', 'examples', 'scripts', 'assets')
# Paths that belong to the dbaney.com site repository, named in lab instructions.
EXTERNAL = {'scripts/learning-lab.mjs', 'scripts/icons.mjs'}
ZIP = ROOT / 'dist' / 'myelinate-plugin.zip'
# Files and folders that make up the installed plugin.
PLUGIN_FILES = ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json', 'LICENSE', 'README.md']
PLUGIN_DIRS = ['skills', 'output-styles', 'commands', 'agents', 'hooks']

SHARED_RE = re.compile(r"(?<![/\w.<>…-])((?:%s)/[\w.-]+\.[a-z0-9]+)" % '|'.join(SHARED))
SIBLING_RE = re.compile(r"(?<![/\w.<>…-])\.\./([a-z-]+)/SKILL\.md")
REPO_SKILL_RE = re.compile(r"(?<![/\w.<>…-])skills/([a-z-]+)/SKILL\.md")
BARE_MD_RE = re.compile(r"(?<![/\w.<>…-])([a-z][a-z0-9-]*\.md)\b")


def skill_names():
    return sorted(p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md') if p.parent.name != 'myelinate')


def localize(text):
    """Rewrite repository-root skill paths to sibling paths (relative to a skill folder)."""
    return REPO_SKILL_RE.sub(r'../\1/SKILL.md', text)


def shared_refs(text, in_references=False):
    refs = set(SHARED_RE.findall(text))
    if in_references:
        refs |= {f'references/{name}' for name in BARE_MD_RE.findall(text) if (ROOT / 'references' / name).is_file()}
    return {r for r in refs if r not in EXTERNAL}


def closure(entry_text):
    """Every shared file a skill needs: what its SKILL.md names, plus what those files name."""
    todo, seen = list(shared_refs(entry_text)), set()
    while todo:
        rel = todo.pop()
        if rel in seen or not (ROOT / rel).is_file():
            seen.add(rel)
            continue
        seen.add(rel)
        if rel.endswith('.md'):
            todo += shared_refs((ROOT / rel).read_text(), rel.startswith('references/'))
    return sorted(seen)


def generated(skill):
    """Map of path (relative to ROOT) -> bytes for one skill's generated files."""
    out = {}
    if skill == 'myelinate':
        entry = localize((ROOT / 'myelinate.md').read_text())
        out['skills/myelinate/SKILL.md'] = entry.encode()
        out['skills/myelinate/agents/openai.yaml'] = (ROOT / 'agents' / 'openai.yaml').read_bytes()
    else:
        entry = (ROOT / 'skills' / skill / 'SKILL.md').read_text()
    for rel in closure(entry):
        src = ROOT / rel
        if not src.is_file():
            continue  # verify() reports it
        data = src.read_bytes()
        if src.suffix == '.md':
            data = localize(data.decode()).encode()
        out[f'skills/{skill}/{rel}'] = data
    return out


def all_generated():
    out = {}
    for skill in ['myelinate'] + skill_names():
        out.update(generated(skill))
    return out


def owned_paths():
    """Existing files the build owns: the router folder and shared-file copies in skill folders."""
    paths = set()
    for d in (ROOT / 'skills').iterdir():
        if not d.is_dir():
            continue
        if d.name == 'myelinate':
            paths |= {p for p in d.rglob('*') if p.is_file()}
        for sub in SHARED:
            if (d / sub).is_dir():
                paths |= {p for p in (d / sub).rglob('*') if p.is_file()}
    return {str(p.relative_to(ROOT)) for p in paths if p.name != '.DS_Store'}


def build_zip(files):
    ZIP.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(files):
            info = zipfile.ZipInfo(f'myelinate/{rel}', date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (ROOT / rel).read_bytes())


def plugin_files():
    files = [f for f in PLUGIN_FILES if (ROOT / f).is_file()]
    for d in PLUGIN_DIRS:
        files += [str(p.relative_to(ROOT)) for p in sorted((ROOT / d).rglob('*'))
                  if p.is_file() and p.name != '.DS_Store']
    return files


def build():
    for rel in owned_paths():
        (ROOT / rel).unlink()
    for rel, data in all_generated().items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    for d in sorted((ROOT / 'skills').rglob('*'), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    build_zip(plugin_files())
    print(f'built {len(all_generated())} generated files and {ZIP.relative_to(ROOT)}')


def verify():
    errors = []
    want = all_generated()
    have = owned_paths()
    for rel, data in want.items():
        if rel not in have or (ROOT / rel).read_bytes() != data:
            errors.append(f'{rel}: out of date; run python3 scripts/package.py build')
    for rel in sorted(have - set(want)):
        errors.append(f'{rel}: stale generated file; run python3 scripts/package.py build')
    if not ZIP.is_file():
        build_zip(plugin_files())  # the zip is a build artifact; the committed copies are what must not drift
    with zipfile.ZipFile(ZIP) as z:
        names = {n[len('myelinate/'):] for n in z.namelist()}
        zipped = {n[len('myelinate/'):]: z.read(n) for n in z.namelist()}
    for rel in plugin_files():
        if rel not in names or zipped[rel] != (ROOT / rel).read_bytes():
            errors.append(f'{ZIP.relative_to(ROOT)}: {rel} missing or stale; run python3 scripts/package.py build')
    # Every path a skill or its copied files name must exist in the zip.
    counts = {}
    skills = sorted({PurePosixPath(n).parts[1] for n in names if n.startswith('skills/') and n.endswith('/SKILL.md')})
    for skill in skills:
        base = f'skills/{skill}'
        n = 0
        for rel in sorted(x for x in names if x.startswith(base + '/') and x.endswith('.md')):
            text = zipped[rel].decode()
            in_refs = '/references/' in rel
            for ref in shared_refs(text):
                n += 1
                if f'{base}/{ref}' not in names:
                    errors.append(f'{rel}: names {ref}, missing from the package at {base}/{ref}')
            for sib in SIBLING_RE.findall(text):
                n += 1
                if f'skills/{sib}/SKILL.md' not in names:
                    errors.append(f'{rel}: names ../{sib}/SKILL.md, missing from the package')
            if in_refs:
                for bare in BARE_MD_RE.findall(text):
                    if (ROOT / 'references' / bare).is_file():
                        n += 1
                        if f'{base}/references/{bare}' not in names:
                            errors.append(f'{rel}: names {bare}, missing from the package')
        counts[skill] = n
    router = zipped.get('skills/myelinate/SKILL.md', b'').decode()
    for name in skill_names():
        if f'../{name}/SKILL.md' not in router:
            errors.append(f'skills/myelinate/SKILL.md does not route to ../{name}/SKILL.md')
    return errors, counts


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    if cmd == 'build':
        build()
    errors, counts = verify()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    total = sum(counts.values())
    print(f'PASS: {len(counts)} skills in {ZIP.relative_to(ROOT)}; all {total} referenced paths present in the package')
    for skill, n in counts.items():
        print(f'  {skill}: {n} paths')
