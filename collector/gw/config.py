"""Config and secrets, both local and outside the repo.

~/.config/gabriellsar-widgets/config.toml   preferences (no secrets)
~/.config/gabriellsar-widgets/secrets.env   KEY=VALUE, chmod 600
~/.local/state/gabriellsar-widgets/*.json   what the QML plugins read
"""
from __future__ import annotations

import os
import tomllib
from pathlib import Path

HOME = Path.home()
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config")) / "gabriellsar-widgets"
STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", HOME / ".local" / "state")) / "gabriellsar-widgets"
CONFIG_FILE = Path(os.environ.get("GW_CONFIG", CONFIG_DIR / "config.toml"))
SECRETS_FILE = Path(os.environ.get("GW_SECRETS", CONFIG_DIR / "secrets.env"))

DEFAULTS: dict = {
    "invest": {
        "source": "file",
        "refresh_sec": 300,
        "currency": "USD",
        "mcp": {
            "command": [],
            "url": "",
            "secret_env": [],
            "headers": {},
            "positions_tool": "",
            "positions_args": {},
            "account_tool": "",
            "account_args": {},
            "map": {
                "positions": "positions",
                "ticker": "symbol",
                "side": "side",
                "qty": "quantity",
                "entry": "entry_price",
                "mark": "mark_price",
                "pnl": "unrealized_pnl",
                "equity": "equity",
                "day_change_pct": "",
            },
        },
        "file": {"path": str(CONFIG_DIR / "positions.toml")},
        "market": {"provider": "yahoo", "window_days": 90, "symbol_map": {}},
    },
    "pomodoro": {
        "focus_min": 25,
        "short_break_min": 5,
        "long_break_min": 15,
        "sessions": 4,
        "autoplay": True,
        "pause_on_break": True,
        "default_playlist": "",
    },
    "spotify": {"player": "spotify", "use_web_api": False, "playlists": []},
    "agents": {
        "poll_ms": 1500,
        "log_lines": 4,
        "faces": ["bolha", "visor", "orelha", "ciclope"],
        "tints": ["data-1", "data-2", "data-4", "data-3"],
        "assign": {},
    },
    "dock": {"apps": []},
}


def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load() -> dict:
    data = {}
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("rb") as fh:
            data = tomllib.load(fh)
    return _merge(DEFAULTS, data)


def secrets() -> dict[str, str]:
    """KEY=VALUE lines; the process env wins so systemd overrides work."""
    out: dict[str, str] = {}
    if SECRETS_FILE.exists():
        for line in SECRETS_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    for k in list(out):
        if os.environ.get(k):
            out[k] = os.environ[k]
    return out


def secret(name: str) -> str:
    return secrets().get(name, "")


def expand(path: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def export_public(cfg: dict | None = None) -> Path:
    """Write the non-secret preferences as JSON for QML (QML can't read TOML)."""
    cfg = cfg or load()
    public = {k: cfg[k] for k in ("pomodoro", "spotify", "agents", "dock")}
    public["invest"] = {k: cfg["invest"][k] for k in ("source", "refresh_sec", "currency")}
    from .state import write_json
    return write_json("config", public)
