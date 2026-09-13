"""Resolve the current user's external cover directory; never fall back to cwd."""
import json
from pathlib import Path
import subprocess
import sys


def output_root():
    if sys.platform == 'win32':
        # Respects Windows Pictures redirection (including OneDrive).
        value = subprocess.check_output([
            'powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
            "[Environment]::GetFolderPath('MyPictures')"
        ], encoding='utf-8-sig', timeout=15).strip()
        if not value:
            raise OSError('Windows Pictures directory could not be resolved')
        pictures = Path(value)
    elif sys.platform == 'darwin':
        pictures = Path.home() / 'Pictures'
    else:
        raise OSError('Unsupported OS: configure a user-approved external Pictures directory')
    if not pictures.is_absolute():
        raise OSError('Pictures directory must be absolute')
    return pictures / 'Yzzx Cover'


def initialize_output():
    root = output_root()
    for path in (root / 'covers', root / 'style-tests'):
        path.mkdir(parents=True, exist_ok=True)
    return root


if __name__ == '__main__':
    print(json.dumps({'output_root': str(initialize_output())}, ensure_ascii=False))
