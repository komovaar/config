# Ink for tmux

A compact charcoal theme matching the Neovim Ink palette in this repository.
Requires tmux 3.3 or newer. Uses plain text, with no plugins or Nerd Font required.
The terminal app controls the font family and size; this theme controls colors
and layout. Prefix, mouse behavior, pane shortcuts, and window numbering stay
as configured before installation.

```sh
./tmux/install.sh
```

The installer copies the theme to `~/.config/tmux/ink.conf` (or
`$XDG_CONFIG_HOME/tmux/ink.conf`), adds a source line to your existing tmux config,
and applies it to running sessions. It saves existing files under
`~/.local/state/tmux-config-backups/` first. Re-run after editing the repo theme.

The bar shows the session on the left, window tabs in the middle, and date/time
on the right. PREFIX, COPY, and ZOOM indicators appear when relevant.
