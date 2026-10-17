#!/usr/bin/env python3
"""Install bundled YAMIS icons and select them for KDE and existing GTK settings."""
import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess

home = Path.home()
source = Path(__file__).resolve().parents[1] / 'snapshot/assets/icons/YAMIS'
data = Path(os.environ.get('XDG_DATA_HOME', home / '.local/share'))
config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
target = data / 'icons/YAMIS'
backup = home / '.local/state/kde-config-backups' / (
    'yamis-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)

def save(path, name):
    if path.is_dir():
        shutil.copytree(path, backup / name, symlinks=True)
    elif path.exists():
        shutil.copy2(path, backup / name)

save(target, 'YAMIS')
save(config / 'kdeglobals', 'kdeglobals')
shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
subprocess.run(['kwriteconfig6', '--file', str(config / 'kdeglobals'),
                '--group', 'Icons', '--key', 'Theme', 'YAMIS'], check=True)
for version in ['gtk-3.0', 'gtk-4.0']:
    path = config / version / 'settings.ini'
    if path.exists():
        original = path.read_text()
        updated, count = re.subn(r'^gtk-icon-theme-name=.*$', 'gtk-icon-theme-name=YAMIS',
                                 original, flags=re.MULTILINE)
        if count and updated != original:
            save(path, version + '-settings.ini')
            path.write_text(updated)
if shutil.which('gtk-update-icon-cache'):
    subprocess.run(['gtk-update-icon-cache', '-f', '-t', str(target)], check=True)
if shutil.which('dbus-send'):
    subprocess.run(['dbus-send', '--session', '--type=signal', '/KIconLoader',
                    'org.kde.KIconLoader.iconChanged', 'int32:0'], check=True)
print(f'Installed and selected YAMIS: {target}')
print(f'Backup: {backup}')
