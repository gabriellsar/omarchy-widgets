#!/usr/bin/env bash
# Liga cada plugins/<id>/ deste repo em ~/.config/omarchy/plugins/<id> (symlink da pasta;
# dentro da pasta não pode haver symlinks) e valida. Use --enable para ligar no shell.
#   scripts/link-plugins.sh                 todos
#   scripts/link-plugins.sh gabriellsar.pomodoro --enable
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.config/omarchy/plugins"
ENABLE=0; IDS=()
for a in "$@"; do [[ $a == --enable ]] && ENABLE=1 || IDS+=("$a"); done
mkdir -p "$DEST"
"$REPO/scripts/sync-shared.sh"

for dir in "$REPO"/plugins/*/; do
  id="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["id"])' "$dir/manifest.json")"
  [[ ${#IDS[@]} -gt 0 && ! " ${IDS[*]} " =~ " $id " ]] && continue
  target="$DEST/$id"
  if [[ -e $target && ! -L $target ]]; then
    mv "$target" "$target.bak.$(date +%s)"; echo "backup de $target"
  fi
  ln -sfn "${dir%/}" "$target"
  echo "ligado $id"
  omarchy plugin validate "${dir%/}"
  [[ $ENABLE == 1 ]] && omarchy plugin enable "$id"
done
omarchy-shell shell rescanPlugins >/dev/null 2>&1 || true
