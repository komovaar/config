#!/usr/bin/env python3
"""Download and activate classic DMZ Black cursors for the current user."""
import datetime
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

URL = 'https://github.com/rhizoome/dmz-cursors/releases/download/v1.0/dmz-black.tar.xz'
home = Path.home()
config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
data = Path(os.environ.get('XDG_DATA_HOME', home / '.local/share'))
payload = Path(sys.argv[1]).read_bytes() if len(sys.argv) > 1 else urllib.request.urlopen(URL, timeout=60).read()
target = data / 'icons/dmz-black'
backup = home / '.local/state/kde-config-backups' / (
    'dmz-black-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
with tempfile.TemporaryDirectory() as directory:
    with tarfile.open(fileobj=io.BytesIO(payload), mode='r:xz') as archive:
        archive.extractall(directory, filter='data')
    source = Path(directory) / 'dmz-black'
    if not (source / 'cursors/left_ptr').exists():
        raise SystemExit('Invalid cursor archive; no settings changed.')
    backup.mkdir(parents=True)
    if target.exists():
        shutil.copytree(target, backup / 'dmz-black', symlinks=True)
    for name in ['kcminputrc', 'gtk-3.0/settings.ini', 'gtk-4.0/settings.ini']:
        path = config / name
        if path.exists():
            saved = backup / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
    shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
subprocess.run(['plasma-apply-cursortheme', '--size', '24', 'dmz-black'], check=True)
for version in ['gtk-3.0', 'gtk-4.0']:
    path = config / version / 'settings.ini'
    if path.exists():
        text = path.read_text()
        text = re.sub(r'^gtk-cursor-theme-name=.*$', 'gtk-cursor-theme-name=dmz-black', text, flags=re.MULTILINE)
        text = re.sub(r'^gtk-cursor-theme-size=.*$', 'gtk-cursor-theme-size=24', text, flags=re.MULTILINE)
        path.write_text(text)
print(f'Applied DMZ Black at 24 px. Backup: {backup}')
