#!/usr/bin/env python3
"""Apply the bundled Inter desktop font while preserving other live settings."""
from pathlib import Path
import datetime
import shutil
import subprocess

root = Path(__file__).resolve().parent
home = Path.home()
saved = home / '.local/state/kde-config-backups' / ('font-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))


def save(path):
    if path.exists():
        destination = saved / path.relative_to(home)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


fonts = home / '.local/share/fonts/Inter'
fonts.mkdir(parents=True, exist_ok=True)
for source in (root / 'snapshot/assets/fonts/Inter').iterdir():
    destination = fonts / source.name
    save(destination)
    shutil.copy2(source, destination)

paths = [home / '.config/kdeglobals', home / '.config/fontconfig/conf.d/99-jetbrains-mono.conf']
for name in ['gtk-3.0', 'gtk-4.0']:
    paths.extend(p for p in (home / '.config' / name).rglob('*') if p.is_file())
for path in paths:
    if not path.is_file():
        continue
    try:
        original = path.read_text()
    except UnicodeDecodeError:
        continue
    if path.name == 'kdeglobals':
        updated = ''.join(line if line.startswith('fixed=') else line.replace('JetBrainsMono Nerd Font', 'Inter') for line in original.splitlines(keepends=True))
    elif path.name == '99-jetbrains-mono.conf':
        updated = ''.join(line if '<family>monospace</family>' in line else line.replace('JetBrains Mono', 'Inter') for line in original.splitlines(keepends=True))
    else:
        updated = original.replace('JetBrainsMono Nerd Font', 'Inter')
    if original != updated:
        save(path)
        path.write_text(updated)
subprocess.run(['fc-cache', '-f'], check=True)
print(f'Applied Inter. Previous files: {saved}. Log out and back in to refresh all apps.')
