#!/usr/bin/env python3
"""Install upstream Iosevka for this user and apply it to KDE, GTK and Konsole."""
import datetime
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request
import zipfile


def main():
    home = Path.home()
    release_url = 'https://api.github.com/repos/be5invis/Iosevka/releases/latest'
    with urllib.request.urlopen(release_url, timeout=60) as response:
        release = json.load(response)
    asset = next(a for a in release['assets']
                 if re.fullmatch(r'PkgTTF-Iosevka-\d[^/]*\.zip', a['name']))
    print(f"Downloading {asset['name']}", flush=True)
    with urllib.request.urlopen(asset['browser_download_url'], timeout=120) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
    # Only install the core weights; the release also contains width variants.
    wanted = {'Iosevka-Regular.ttf', 'Iosevka-Italic.ttf',
              'Iosevka-Bold.ttf', 'Iosevka-BoldItalic.ttf'}
    members = [n for n in archive.namelist() if Path(n).name in wanted]
    if {Path(n).name for n in members} != wanted:
        raise RuntimeError('Upstream font layout changed; no files modified.')
    backup = home / '.local/state/kde-config-backups' / (
        'iosevka-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True)

    def save(path):
        if path.exists():
            target = backup / path.relative_to(home)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        else:
            with (backup / 'created-files.txt').open('a') as out:
                out.write(str(path) + '\n')

    fonts = home / '.local/share/fonts/Iosevka'
    fonts.mkdir(parents=True, exist_ok=True)
    for member in members:
        target = fonts / Path(member).name
        save(target)
        target.write_bytes(archive.read(member))
    subprocess.run(['fc-cache', '-f', str(fonts)], check=True)
    kde = home / '.config/kdeglobals'
    save(kde)
    for key, size in [('font', 11), ('menuFont', 11), ('toolBarFont', 11),
                      ('smallestReadableFont', 9), ('fixed', 12)]:
        subprocess.run(['kwriteconfig6', '--file', str(kde), '--group', 'General',
                        '--key', key, f'Iosevka,{size},-1,5,400,0,0,0,0,0'], check=True)
    subprocess.run(['kwriteconfig6', '--file', str(kde), '--group', 'WM',
                    '--key', 'activeFont', 'Iosevka,11,-1,5,400,0,0,0,0,0'], check=True)
    for version in ['gtk-3.0', 'gtk-4.0']:
        path = home / '.config' / version / 'settings.ini'
        if path.exists():
            original = path.read_text()
            updated, count = re.subn(r'^gtk-font-name=.*$', 'gtk-font-name=Iosevka 11',
                                     original, flags=re.MULTILINE)
            if count and updated != original:
                save(path)
                path.write_text(updated)
    # Keep terminal color preferences and the existing default profile.
    config = home / '.config/konsolerc'
    profile = subprocess.check_output(['kreadconfig6', '--file', str(config),
        '--group', 'Desktop Entry', '--key', 'DefaultProfile'], text=True).strip()
    if profile and Path(profile).name == profile:
        path = home / '.local/share/konsole' / profile
        path.parent.mkdir(parents=True, exist_ok=True)
        save(path)
        subprocess.run(['kwriteconfig6', '--file', str(path), '--group', 'Appearance',
                        '--key', 'Font', 'Iosevka,12,-1,5,50,0,0,0,0,0'], check=True)
    print(f"Installed {release['tag_name']}. Backup: {backup}")
    print('Log out and back in to refresh fonts in all applications.')


if __name__ == '__main__':
    main()
