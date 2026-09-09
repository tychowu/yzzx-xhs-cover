#!/usr/bin/env python3
"""Check/install skill dependencies in a portable, isolated environment."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def run(args):
    subprocess.run(args, check=True, timeout=180)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='Install missing Python packages')
    parser.add_argument('--node', action='store_true', help='Require Node.js 18+ for generate.mjs')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cache = Path(os.environ.get('YZZX_RUNTIME_DIR', str(Path.home() / '.cache' / 'yzzx-cover' / 'runtime')))
    py = cache / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    packages = [('yaml', 'PyYAML>=6,<7')]
    if not py.exists() and args.install:
        run([sys.executable, '-m', 'venv', str(cache)])
    missing = []
    for module, package in packages:
        if not py.exists() or subprocess.run([str(py), '-c', 'import ' + module], capture_output=True).returncode:
            missing.append(package)
    if missing and args.install:
        run([str(py), '-m', 'pip', 'install', '--disable-pip-version-check', *missing])
        missing = [package for module, package in packages if subprocess.run(
            [str(py), '-c', 'import ' + module], capture_output=True).returncode]
    issues = ['Missing Python dependency: ' + x for x in missing]
    node = shutil.which('node')
    if args.node:
        try:
            version = subprocess.check_output([node, '--version'], text=True).strip() if node else ''
            if not version or int(version.lstrip('v').split('.')[0]) < 18:
                issues.append('Node.js 18+ required; install a supported LTS runtime with the host package manager.')
        except (OSError, ValueError, subprocess.SubprocessError):
            issues.append('Node.js version check failed.')
    styles = sorted((root / 'references' / 'styles').glob('*.json'))
    if not styles:
        issues.append('Style library missing; install the complete skill folder.')
    for path in styles:
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if not data.get('name') or not data.get('prompt'):
                issues.append('Invalid style: ' + path.name)
        except (ValueError, OSError):
            issues.append('Unreadable style: ' + path.name)
    print(json.dumps({'ready': not issues, 'python': str(py), 'node': node,
                      'styles': len(styles), 'issues': issues},
                     ensure_ascii=False, indent=2))
    return bool(issues)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, subprocess.SubprocessError) as error:
        print('Environment setup failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
