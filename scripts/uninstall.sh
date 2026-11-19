#!/usr/bin/env bash
# Para e remove as units e o link do gw. Config e segredos locais ficam.
set -euo pipefail
for u in gw-invest.timer gw-spotify.timer gw-config.path gw-herdr.service; do
  systemctl --user disable --now "$u" 2>/dev/null || true
done
for u in gw-invest.service gw-invest.timer gw-spotify.service gw-spotify.timer gw-herdr.service gw-config.path gw-config.service; do
  rm -f "$HOME/.config/systemd/user/$u"
done
systemctl --user daemon-reload
rm -f "$HOME/.local/bin/gw"
echo "removido. ~/.config/gabriellsar-widgets ficou intacto."
