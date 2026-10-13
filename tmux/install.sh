#!/usr/bin/env bash
set -euo pipefail
theme_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
target_dir="${XDG_CONFIG_HOME:-$HOME/.config}/tmux"
target_theme="$target_dir/ink.conf"
target_config="$HOME/.tmux.conf"
if [[ ! -f "$target_config" && -f "$target_dir/tmux.conf" ]]; then
  target_config="$target_dir/tmux.conf"
fi
backup_dir="$HOME/.local/state/tmux-config-backups/$(date +%Y%m%d-%H%M%S-%N)"
mkdir -p "$target_dir" "$backup_dir"
[[ ! -f "$target_theme" ]] || cp -p -- "$target_theme" "$backup_dir/ink.conf"
[[ ! -f "$target_config" ]] || cp -p -- "$target_config" "$backup_dir/tmux.conf"
cp -- "$theme_dir/ink.conf" "$target_theme"
# Quote the absolute path for tmux's config parser.
escaped_theme=${target_theme//\\/\\\\}
escaped_theme=${escaped_theme//\"/\\\"}
source_line="source-file \"$escaped_theme\""
if ! grep -Fqx -- "$source_line" "$target_config" 2>/dev/null; then
  printf '\n# Ink appearance from the config repository\n%s\n' "$source_line" >> "$target_config"
fi
if tmux list-sessions >/dev/null 2>&1; then
  tmux source-file "$target_theme"
fi
printf 'Installed Ink theme. Previous files: %s\n' "$backup_dir"
