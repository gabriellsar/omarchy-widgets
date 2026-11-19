#!/usr/bin/env bash
# Instala a parte de dados: `gw` no PATH, config local e as units do systemd --user.
# Não toca em nada do Omarchy. Desfazer: scripts/uninstall.sh
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$HOME/.local/bin"
ln -sfn "$REPO/bin/gw" "$HOME/.local/bin/gw"
echo "gw -> $HOME/.local/bin/gw"

"$REPO/bin/gw" init

command -v playerctl >/dev/null || echo "aviso: instale o playerctl (omarchy-pkg-add playerctl) para os controles do Spotify"

for unit in "$REPO"/systemd/*; do
  systemctl --user link "$unit" >/dev/null
done
systemctl --user daemon-reload
systemctl --user enable --now gw-invest.timer gw-spotify.timer gw-config.path gw-herdr.service
echo
echo "Pronto. Agora:"
echo "  1. edite ~/.config/gabriellsar-widgets/config.toml e secrets.env"
echo "  2. gw doctor"
echo "  3. gw invest --print"
