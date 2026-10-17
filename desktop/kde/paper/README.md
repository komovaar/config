# Paper

A native KDE Plasma color scheme for Fedora KDE: soft white surfaces, near-black
text, neutral gray secondary text, and white-on-charcoal selections. All color
roles are grayscale, including links and semantic status colors.

## Use

Open **System Settings → Colors & Themes → Colors → Install from File…**
(the wording can vary by Plasma version), select `Paper.colors`, then select
**Paper** and apply it. Use the **Breeze** application style and Plasma style
so supported desktop surfaces follow the scheme.

Alternatively, install the file for your user:

```sh
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/color-schemes"
cp desktop/kde/paper/Paper.colors "${XDG_DATA_HOME:-$HOME/.local/share}/color-schemes/"
```

Then select Paper in System Settings. To return to your previous appearance,
select your previous color scheme. This file does not change fonts, icons,
wallpaper, panel layout, terminal profiles, or editor configuration.

The palette uses `#F3F3F3` for windows, `#FAFAFA` for content and buttons,
`#202020` for text and selection backgrounds, and `#626262` for secondary text.
Applications with their own themes may need separate configuration. Errors,
warnings, and success messages share neutral colors; their text and icons
provide the distinction.

## Iosevka fonts

`python3 desktop/kde/paper/apply-iosevka.py` downloads the latest standard
Iosevka TTF release from the official `be5invis/Iosevka` GitHub repository.
It installs regular, italic, bold, and bold italic for the current user,
sets KDE and existing GTK settings to 11 pt (small text 9 pt), and sets
KDE's fixed-width font and the default Konsole profile to 12 pt.
Existing files are backed up under `~/.local/state/kde-config-backups/iosevka-*`.
The backup's `created-files.txt` lists newly created files. To undo, restore
backed-up files to their corresponding home-relative paths and remove only
files listed as newly created. Run `fc-cache -f` afterward.
Log out and back in to refresh all applications. Editor fonts are unchanged.

## Window decoration

Run `python3 desktop/kde/paper/apply-decoration.py` to install and activate the
Paper Aurorae decoration: square corners, opaque paper surfaces, thin borders,
and plain monochrome minimize, maximize/restore, and close buttons. Hovered
buttons invert to white on charcoal. Existing KWin settings are backed up.
Applications drawing their own title bars may retain their own styling.
Select Breeze in System Settings to return to the standard decoration.

`square-windows.py` is the earlier Breeze-only adjustment; it disables bottom
corner rounding but does not square the title bar. Use `apply-decoration.py`
for all four corners.

## Icons and terminal

- `python3 desktop/kde/paper/install-icons.py` installs the repository's bundled
  YAMIS icons and selects them in KDE and existing GTK settings.
- `python3 desktop/kde/paper/apply-konsole.py` installs `Paper.colorscheme` and
  selects it in the current user-local default Konsole profile, preserving its
  font. Open a new Konsole window afterward.
- Copy `fastfetch/config.jsonc` to `~/.config/fastfetch/config.jsonc` to use the
  terminal's default foreground for the logo, labels, values, and percentages.
  Back up an existing configuration first.

The installers save previous files under `~/.local/state/kde-config-backups/`.
The desktop scripts require KDE's `kwriteconfig6`; decoration activation uses
Fedora's `/usr/lib64/qt6/bin/qdbus`.

## Classic cursor

`python3 desktop/kde/paper/apply-cursor.py` downloads the pinned v1.0 DMZ Black
cursor archive from https://github.com/rhizoome/dmz-cursors and activates it at
24 px using `plasma-apply-cursortheme`, also matching existing GTK settings.
An optional argument supplies an already-downloaded archive. Existing settings
and an existing user-local copy of the cursor theme are backed up.
Select Breeze Light in System Settings to return to the previous cursor.

## Wallpaper studies

`wallpapers/` contains generated abstract wallpaper studies. `ink-mark.png` is
the initial brushstroke; `pencil-study.png` is the graphite alternative;
`pencil-study-dim.png` uses slightly dimmer paper. They are 1672 × 941 images,
not native 4K. None of the installers changes the wallpaper.
