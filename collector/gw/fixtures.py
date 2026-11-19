"""Sample state files so the widgets can be built and screenshotted with no
credentials. Values mirror the design boards in specs/ref/."""
from __future__ import annotations

from .state import write_json


def write_all() -> list[str]:
    invest = {
        "source": "fixture", "currency": "USD", "equity": 48210.37, "dayChangePct": 0.0124, "error": None,
        "positions": [
            {"ticker": "BTC", "side": "LONG", "qty": 0.35, "entry": 88120.0, "mark": 92410.5, "pnl": 1501.68,
             "pnlPct": 0.0487, "market": {"symbol": "BTC-USD", "todayRet": 0.018, "mu": 0.0011, "sigma": 0.028,
                                          "z": 0.6, "alert": False, "n": 89, "last": 92410.5}},
            {"ticker": "NVDA", "side": "LONG", "qty": 40, "entry": 171.2, "mark": 186.9, "pnl": 628.0,
             "pnlPct": 0.0917, "market": {"symbol": "NVDA", "todayRet": 0.061, "mu": 0.0015, "sigma": 0.025,
                                          "z": 2.4, "alert": True, "n": 89, "last": 186.9}},
            {"ticker": "ETH", "side": "SHORT", "qty": 2.0, "entry": 3410.0, "mark": 3322.4, "pnl": 175.2,
             "pnlPct": 0.0257, "market": {"symbol": "ETH-USD", "todayRet": -0.026, "mu": 0.0004, "sigma": 0.033,
                                          "z": -0.8, "alert": False, "n": 89, "last": 3322.4}},
        ],
    }
    spotify = {"player": "spotify", "error": None, "playlists": [
        {"name": "Deep Focus", "uri": "spotify:playlist:37i9dQZF1DWZeKCadgRdKQ", "favorite": True},
        {"name": "Lo-fi Beats", "uri": "spotify:playlist:37i9dQZF1DWWQRwui0ExPn", "favorite": True},
        {"name": "Brain Food", "uri": "spotify:playlist:37i9dQZF1DWXLeA8Omikj7", "favorite": False, "tracks": 120},
    ]}
    agents = [
        {"id": "w1:p1", "target": "api-refactor", "label": "api-refactor", "agent": "claude", "cwd": "~/easyfin",
         "status": "working", "face": "bolha", "tint": "data-1", "focused": False, "workspace": "w1", "seq": 12,
         "log": ["Lendo src/api/routes.ts", "Refatorando handlers para async", "Rodando testes · 42/58"], "prompt": None},
        {"id": "w2:p1", "target": "tcc-forecast", "label": "tcc-forecast", "agent": "claude", "cwd": "~/tcc",
         "status": "blocked", "face": "visor", "tint": "data-2", "focused": False, "workspace": "w2", "seq": 30,
         "log": ["Treinando LSTM · época 14", "Salvando checkpoint"],
         "prompt": {"tool": "Edit", "file": "model/forecast.py",
                    "diff": [{"s": "-", "t": "horizon = 12"}, {"s": "+", "t": "horizon = 24"},
                             {"s": "+", "t": "dropout = 0.2"}],
                    "options": ["1 Yes", "2 Yes, allow all edits this session", "3 No"], "lines": []}},
        {"id": "w3:p1", "target": "portfolio", "label": "portfolio", "agent": "codex", "cwd": "~/portfolio",
         "status": "done", "face": "orelha", "tint": "data-4", "focused": False, "workspace": "w3", "seq": 8,
         "log": ["Build ok · 1.2s", "Deploy preview pronto"], "prompt": None},
        {"id": "w4:p1", "target": "shader-lab", "label": "shader-lab", "agent": "claude", "cwd": "~/quattro",
         "status": "idle", "face": "ciclope", "tint": "data-3", "focused": False, "workspace": "w4", "seq": 3,
         "log": ["Aguardando próxima tarefa"], "prompt": None},
    ]
    herdr = {"running": True, "agents": agents, "error": None,
             "counts": {"working": 1, "blocked": 1, "done": 1, "idle": 1, "unknown": 0}}
    return [str(write_json("invest", invest)), str(write_json("spotify", spotify)),
            str(write_json("herdr", herdr))]
