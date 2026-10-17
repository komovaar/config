#!/usr/bin/env python3
"""Disable Breeze window corner rounding, preserving all other settings."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess

home = Path.home()
config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
path = config / 'breezerc'
backup = home / '.local/state/kde-config-backups' / (
    'square-windows-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
if path.exists():
    shutil.copy2(path, backup / 'breezerc')
else:
    (backup / 'created-files.txt').write_text(str(path) + '\n')
subprocess.run(['kwriteconfig6', '--file', str(path), '--group', 'Common',
                '--key', 'RoundedCorners', '--type', 'bool', 'false'], check=True)
subprocess.run(['/usr/lib64/qt6/bin/qdbus', 'org.kde.KWin', '/KWin',
                'org.kde.KWin.reconfigure'], check=True)
print(f'Breeze square corners enabled. Backup: {backup}')
