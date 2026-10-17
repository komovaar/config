#!/usr/bin/env python3
"""Install and activate the square Paper Aurorae window decoration."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess

home = Path.home()
config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
data = Path(os.environ.get('XDG_DATA_HOME', home / '.local/share'))
source = Path(__file__).with_name('aurorae') / 'Paper'
target = data / 'aurorae/themes/Paper'
backup = home / '.local/state/kde-config-backups' / (
    'paper-decoration-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
shutil.copy2(config / 'kwinrc', backup / 'kwinrc')
if target.exists():
    shutil.copytree(target, backup / 'Paper', symlinks=True)
shutil.copytree(source, target, dirs_exist_ok=True)
for key, value in [('library', 'org.kde.kwin.aurorae'),
                   ('theme', '__aurorae__svg__Paper')]:
    subprocess.run(['kwriteconfig6', '--file', str(config / 'kwinrc'),
                    '--group', 'org.kde.kdecoration2', '--key', key, value], check=True)
subprocess.run(['/usr/lib64/qt6/bin/qdbus', 'org.kde.KWin', '/KWin',
                'org.kde.KWin.reconfigure'], check=True)
print(f'Activated Paper window decoration. Backup: {backup}')
