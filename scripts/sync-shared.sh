#!/usr/bin/env bash
# Copia shared/* para plugins/<id>/common/ (cópia, não symlink: o validador recusa
# symlinks dentro do plugin). Edite sempre em shared/, nunca em common/.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
for dir in "$REPO"/plugins/*/; do
  mkdir -p "$dir/common"
  for f in "$REPO"/shared/*; do
    cp "$f" "$dir/common/"
  done
done
