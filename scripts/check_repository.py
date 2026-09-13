"""Small, dependency-free team checks. Never print secret values."""
import argparse
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def check(root, base=None):
    errors = []
    files = git('ls-files', '-z').split('\0')
    for name in filter(None, files):
        path = root / name
        if not path.is_file():
            continue
        parts = {p.lower() for p in Path(name).parts}
        if parts & {'output', 'node_modules', '.venv'} or (path.name.startswith('.env') and path.name != '.env.example') or path.suffix in {'.pem', '.key'}:
            errors.append(f'Forbidden tracked file: {name}')
        if any(word in path.name for word in ['角色控制', '换装控制', '人物控制']):
            errors.append(f'Possible private reference: {name}')
        if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and not name.startswith(('references/styles/source-references/', 'references/styles/approved-examples/')):
            errors.append(f'Image outside approved library directories: {name}')
        if path.suffix.lower() in {'.md', '.py', '.yml', '.yaml', '.json', '.mjs', '.txt'}:
            text = path.read_text(encoding='utf-8')
            patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}', r'sk-[A-Za-z0-9_-]{32,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
            if any(re.search(p, text) for p in patterns):
                errors.append(f'Possible secret in: {name}')
        if path.suffix == '.md':
            for link in re.findall(r'\]\(([^\n]+?)\)', path.read_text(encoding='utf-8')):
                link = link.strip().strip('<>')
                if re.match(r'^[a-zA-Z][\w+.-]*:', link) or link.startswith(('#', '/', '~')) or '<' in link:
                    continue
                target = unquote(link.split('#')[0])
                if target and not (path.parent / target).exists():
                    errors.append(f'Broken link in {name}: {target}')
    styles = list((root / 'references/styles').glob('*.json'))
    if not styles:
        errors.append('Missing style library')
    for path in styles:
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if not all(isinstance(data.get(k), str) and data[k].strip() for k in ['name', 'prompt']):
                raise ValueError('name/prompt must be nonempty strings')
            for ref in data.get('source_references', []):
                if not (path.parent / ref).is_file():
                    errors.append(f'Missing reference in {path.name}: {ref}')
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append(f'Invalid style {path.name}: {exc}')
    version = (root / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        errors.append('Invalid VERSION')
    if f'## {version} · ' not in (root / 'CHANGELOG.md').read_text():
        errors.append('Current version missing from CHANGELOG.md')
    if base and re.fullmatch(r'[0-9a-fA-F]{40}', base) and set(base) != {'0'}:
        old = subprocess.run(['git', 'show', f'{base}:VERSION'], capture_output=True, text=True)
        if old.returncode == 0 and re.fullmatch(r'\d+\.\d+\.\d+', version):
            if tuple(map(int, version.split('.'))) <= tuple(map(int, old.stdout.strip().split('.'))):
                errors.append('Bump VERSION above the base version before merging')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    import os
    os.chdir(root)
    problems = check(root, args.base)
    for problem in problems:
        print(problem)
    print(f'{len(problems)} error(s)')
    raise SystemExit(bool(problems))
