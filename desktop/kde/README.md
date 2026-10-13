# KDE desktop backup

This snapshot stores KDE appearance, fonts, icons, shortcuts, panels, widgets,
GTK appearance settings, and wallpaper images. Neovim configuration remains at
the repository root. Requires Python 3; font discovery uses Fontconfig.

Refresh the snapshot after customizing your desktop:

```sh
./desktop/kde/backup.sh
git diff -- desktop/kde/snapshot/config
```

Backup reads your settings and writes only to this repository. It replaces the
previous snapshot, so commit snapshots you want to keep. Home paths are replaced
with `@KDE_HOME@`; wallpaper files are restored to a stable directory under
`~/.local/share/wallpapers/config-repo/`.

Preview restore:

```sh
./desktop/kde/restore.sh
```

To restore, log out of Plasma, switch to a TTY (Ctrl+Alt+F3), log in, navigate to
this repository, then run:

```sh
./desktop/kde/restore.sh --apply
```

Existing destination files are copied to
`~/.local/state/kde-config-backups/<timestamp>/` before replacement. Log back in
to Plasma afterward. Restore does not install packages or delete extra files.
Use the same Plasma major version when possible; panel layouts can need manual
adjustment on different monitors. System-installed themes and widgets require
their original packages on the destination machine.
`packages.txt` lists the relevant installed Fedora packages at initial capture.

User-installed icon themes, color schemes, Plasma themes/widgets, and window
decorations are included. User-installed fonts matching the selected KDE font
families are included; system fonts are supplied by the destination OS.
Login-screen themes, monitor hardware configuration, and application data are
outside this backup. Review custom shortcuts and asset licenses before publishing.
