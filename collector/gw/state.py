"""Atomic JSON writes into the state dir; QML watches these files."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .config import STATE_DIR


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def path(name: str) -> Path:
    return STATE_DIR / f"{name}.json"


def write_json(name: str, data: dict) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    data = {"schema": 1, "updated": now_iso(), **data}
    target = path(name)
    fd, tmp = tempfile.mkstemp(dir=STATE_DIR, prefix=f".{name}.", suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, target)  # rename is atomic: QML never sees half a file
    return target


def read_json(name: str) -> dict:
    try:
        return json.loads(path(name).read_text())
    except (OSError, ValueError):
        return {}
