#!/usr/bin/env python3
"""Capture and restore selected KDE settings without changing a running desktop."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
FILES = ['kdeglobals', 'plasmarc', 'kwinrc', 'kglobalshortcutsrc',
         'plasma-org.kde.plasma.desktop-appletsrc', 'kcminputrc',
         'kscreenlockerrc', 'kfontinst', 'gtkrc', 'gtkrc-2.0']
DIRS = ['gtk-3.0', 'gtk-4.0', 'fontconfig']
TOKEN = '@KDE_HOME@'


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def backup(home):
    manifest = {}
    stage = ROOT / 'snapshot.new'
    if stage.exists():
        raise SystemExit('snapshot.new already exists; inspect it before retrying.')
    stage.mkdir()

    def capture(source, destination):
        relative = str(source.relative_to(home))
        copy(source, stage / destination)
        manifest[destination] = relative

    for name in FILES:
        source = home / '.config' / name
        if source.is_file():
            capture(source, 'config/' + name)
    for name in DIRS:
        directory = home / '.config' / name
        if directory.exists():
            for source in directory.rglob('*'):
                if source.is_file():
                    capture(source, 'config/' + str(source.relative_to(home / '.config')))

    # Preserve user-installed appearance assets, excluding Plasma caches.
    for name in ['icons', 'color-schemes', 'plasma/desktoptheme',
                 'plasma/look-and-feel', 'plasma/plasmoids', 'aurorae/themes']:
        directory = home / '.local/share' / name
        if directory.exists():
            for source in directory.rglob('*'):
                if source.is_file():
                    capture(source, 'assets/' + str(source.relative_to(home / '.local/share')))

    # Capture all faces of the font families selected in kdeglobals.
    globals_file = home / '.config/kdeglobals'
    families = set()
    if globals_file.exists():
        for line in globals_file.read_text().splitlines():
            if '=' in line and (line.split('=', 1)[0].lower().endswith('font')
                               or line.split('=', 1)[0] == 'fixed'):
                families.add(line.split('=', 1)[1].split(',', 1)[0])
    if shutil.which('fc-list'):
        for family in sorted(families):
            result = subprocess.run(['fc-list', family, '--format=%{file}\n'],
                                    capture_output=True, text=True, check=True)
            for filename in set(result.stdout.splitlines()):
                source = Path(filename)
                if source.is_file() and source.is_relative_to(home):
                    capture(source, 'assets/fonts/' + source.parent.name + '/' + source.name)
                    for license_name in ['LICENSE.txt', 'LICENSE', 'OFL.txt']:
                        license_file = source.parent / license_name
                        if license_file.is_file():
                            capture(license_file, 'assets/fonts/' + source.parent.name + '/' + license_name)

    for source in (stage / 'config').rglob('*'):
        if not source.is_file():
            continue
        try:
            content = source.read_text()
        except UnicodeDecodeError:
            continue
        lines = []
        for line in content.splitlines(keepends=True):
            if line.startswith(('Image=', 'PreviewImage=')):
                key = line.split('=', 1)[0]
                filename = line.strip().split('=', 1)[1].removeprefix('file://')
                wallpaper = Path(filename)
                if wallpaper.is_file():
                    digest = hashlib.sha256(wallpaper.read_bytes()).hexdigest()[:12]
                    name = digest + '-' + wallpaper.name
                    destination = 'wallpapers/' + name
                    copy(wallpaper, stage / destination)
                    manifest[destination] = '.local/share/wallpapers/config-repo/' + name
                    line = key + '=' + TOKEN + '/' + manifest[destination] + '\n'
            lines.append(line.replace(str(home), TOKEN))
        source.write_text(''.join(lines))
    (stage / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    old = ROOT / 'snapshot'
    if old.exists():
        shutil.rmtree(old)
    stage.rename(old)
    print(f'Captured {len(manifest)} files in {old}')


def restore(home, apply):
    snapshot = ROOT / 'snapshot'
    manifest = json.loads((snapshot / 'manifest.json').read_text())
    # Validate every path before writing anything.
    for source, destination in manifest.items():
        if Path(source).is_absolute() or '..' in Path(source).parts:
            raise SystemExit('Invalid source path in manifest')
        if Path(destination).is_absolute() or '..' in Path(destination).parts:
            raise SystemExit('Invalid destination path in manifest')
        if not (snapshot / source).is_file():
            raise SystemExit(f'Missing snapshot file: {source}')
        if not (home / destination).resolve().is_relative_to(home.resolve()):
            raise SystemExit(f'Destination escapes home: {destination}')
    if not apply:
        print(f'Would restore {len(manifest)} files under {home}. Use --apply to write.')
        return
    if subprocess.run(['pgrep', '-u', str(os.getuid()), '-x', 'plasmashell'],
                      stdout=subprocess.DEVNULL).returncode == 0:
        raise SystemExit('Log out of Plasma and run restore from a TTY to avoid settings being overwritten.')
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    previous = home / '.local/state/kde-config-backups' / stamp
    for source, destination in manifest.items():
        target = home / destination
        if target.exists():
            copy(target, previous / destination)
        copy(snapshot / source, target)
        if source.startswith('config/'):
            try:
                content = target.read_text()
            except UnicodeDecodeError:
                continue
            target.write_text(content.replace(TOKEN, str(home)))
    if shutil.which('fc-cache'):
        subprocess.run(['fc-cache', '-f'], check=True)
    print(f'Restored {len(manifest)} files. Previous files: {previous}. Log in to Plasma.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['backup', 'restore'])
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--apply', action='store_true', help='Write restored settings (default: preview)')
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    backup(home) if args.action == 'backup' else restore(home, args.apply)
