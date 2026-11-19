"""Carteira: positions from Quantfury (MCP or a local file) + market stats.

Writes state/invest.json. Quantfury has no public API; the MCP adapter is
configured by tool names and field paths so it fits whichever server you run.
"""
from __future__ import annotations

import tomllib
from typing import Any

from . import market
from .config import CONFIG_DIR, expand
from .mcp import Client
from .state import write_json

CRYPTO = {"BTC", "ETH", "SOL", "XRP", "ADA", "DOGE", "AVAX", "DOT", "LINK", "LTC", "BNB", "MATIC", "TON"}


def dig(obj: Any, dotted: str) -> Any:
    if not dotted:
        return None
    for part in dotted.split("."):
        if isinstance(obj, dict):
            obj = obj.get(part)
        elif isinstance(obj, list) and part.isdigit():
            obj = obj[int(part)] if int(part) < len(obj) else None
        else:
            return None
    return obj


def _num(v: Any) -> float | None:
    try:
        return float(str(v).replace(",", "")) if v is not None and v != "" else None
    except ValueError:
        return None


def _side(v: Any, qty: float | None) -> str:
    s = str(v or "").strip().upper()
    if s in {"BUY", "LONG", "L"}:
        return "LONG"
    if s in {"SELL", "SHORT", "S"}:
        return "SHORT"
    return "SHORT" if (qty or 0) < 0 else "LONG"


def from_mcp(cfg: dict, secrets: dict[str, str]) -> tuple[list[dict], dict]:
    m = cfg["map"]
    with Client(cfg, secrets) as mcp:
        raw = mcp.tool(cfg["positions_tool"], cfg.get("positions_args") or {})
        acct = mcp.tool(cfg["account_tool"], cfg.get("account_args") or {}) if cfg.get("account_tool") else raw
    items = dig(raw, m["positions"]) if m.get("positions") else raw
    if isinstance(items, dict):
        items = list(items.values())
    rows = []
    for it in items or []:
        qty = _num(dig(it, m["qty"]))
        rows.append({
            "ticker": str(dig(it, m["ticker"]) or "?").upper(),
            "side": _side(dig(it, m["side"]), qty),
            "qty": abs(qty) if qty is not None else None,
            "entry": _num(dig(it, m["entry"])),
            "mark": _num(dig(it, m["mark"])),
            "pnl": _num(dig(it, m["pnl"])),
        })
    account = {"equity": _num(dig(acct, m.get("equity", ""))),
               "dayChangePct": _num(dig(acct, m.get("day_change_pct", "")))}
    return rows, account


def from_file(cfg: dict) -> tuple[list[dict], dict]:
    """positions.toml: [[position]] ticker, side, qty, entry; optional equity."""
    p = expand(cfg["path"]) if cfg.get("path") else CONFIG_DIR / "positions.toml"
    with p.open("rb") as fh:
        data = tomllib.load(fh)
    rows = [{"ticker": str(x["ticker"]).upper(), "side": _side(x.get("side"), x.get("qty")),
             "qty": _num(x.get("qty")), "entry": _num(x.get("entry")), "mark": None, "pnl": None}
            for x in data.get("position", [])]
    return rows, {"equity": _num(data.get("equity")), "dayChangePct": None}


def symbol_for(ticker: str, mcfg: dict) -> str:
    mapped = (mcfg.get("symbol_map") or {}).get(ticker)
    if mapped:
        return mapped
    return f"{ticker}-USD" if ticker in CRYPTO else ticker


def enrich(rows: list[dict], account: dict, mcfg: dict, secrets: dict[str, str]) -> None:
    for r in rows:
        try:
            r["market"] = market.for_symbol(symbol_for(r["ticker"], mcfg), mcfg, secrets)
            if r["mark"] is None:
                r["mark"] = r["market"]["last"]
        except Exception as e:  # one bad ticker never blanks the widget
            r["market"] = {"symbol": symbol_for(r["ticker"], mcfg), "error": str(e)}
        sign = 1 if r["side"] == "LONG" else -1
        if r["pnl"] is None and r["qty"] and r["entry"] and r["mark"]:
            r["pnl"] = round(sign * (r["mark"] - r["entry"]) * r["qty"], 2)
        if r["entry"] and r["mark"]:
            r["pnlPct"] = round(sign * (r["mark"] / r["entry"] - 1), 5)
    if account.get("dayChangePct") is None and account.get("equity"):
        move, seen = 0.0, 0
        for r in rows:
            mk = r.get("market", {})
            if "todayRet" in mk and r.get("qty") and r.get("mark"):
                sign = 1 if r["side"] == "LONG" else -1
                move += sign * r["qty"] * r["mark"] * mk["todayRet"]
                seen += 1
        if seen:
            account["dayChangePct"] = round(move / account["equity"], 5)
            account["dayChangeEstimated"] = True


def run(cfg: dict, secrets: dict[str, str]) -> dict:
    icfg = cfg["invest"]
    out: dict = {"source": icfg["source"], "currency": icfg["currency"], "positions": [], "error": None}
    try:
        if icfg["source"] == "mcp":
            rows, account = from_mcp(icfg["mcp"], secrets)
        else:
            rows, account = from_file(icfg["file"])
        enrich(rows, account, icfg["market"], secrets)
        out.update(account)
        out["positions"] = rows
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    write_json("invest", out)
    return out
