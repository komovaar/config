#!/usr/bin/env python3
"""Install Paper for Konsole and set the default profile's color scheme."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess

home = Path.home()
config = Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
data = Path(os.environ.get('XDG_DATA_HOME', home / '.local/share'))
profile = subprocess.check_output(['kreadconfig6', '--file', str(config / 'konsolerc'),
    '--group', 'Desktop Entry', '--key', 'DefaultProfile'], text=True).strip()
if not profile or Path(profile).name != profile:
    raise SystemExit('No valid default Konsole profile; no changes made.')
profile_path = data / 'konsole' / profile
if not profile_path.exists():
    raise SystemExit('Default profile is not user-local; no changes made.')
scheme = data / 'konsole/Paper.colorscheme'
backup = home / '.local/state/kde-config-backups' / (
    'konsole-paper-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.mkdir(parents=True)
shutil.copy2(profile_path, backup / profile)
if scheme.exists():
    shutil.copy2(scheme, backup / scheme.name)
shutil.copy2(Path(__file__).with_name('Paper.colorscheme'), scheme)
subprocess.run(['kwriteconfig6', '--file', str(profile_path), '--group', 'Appearance',
                '--key', 'ColorScheme', 'Paper'], check=True)
print(f'Applied Paper to {profile_path}. Backup: {backup}')
