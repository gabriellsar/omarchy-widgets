"""Market data for the bell curve: where today's move sits against the last N days.

Default provider is Yahoo's public chart endpoint (no key). Optional: brapi.dev
for B3 tickers, with BRAPI_TOKEN in secrets.env.
"""
from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) gabriellsar-widgets"}


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode())


def closes_yahoo(symbol: str, days: int) -> list[float]:
    rng = "6mo" if days <= 120 else "1y"
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}"
           f"?range={rng}&interval=1d")
    res = _get(url)["chart"]["result"][0]
    closes = res["indicators"]["quote"][0]["close"]
    live = res.get("meta", {}).get("regularMarketPrice")
    vals = [c for c in closes if c is not None]
    if live and vals and abs(vals[-1] - live) / live > 1e-9:
        vals[-1] = live  # intraday: last close is the live price
    return vals[-(days + 2):]


def closes_brapi(symbol: str, days: int, token: str) -> list[float]:
    url = f"https://brapi.dev/api/quote/{urllib.parse.quote(symbol)}?range=6mo&interval=1d&token={token}"
    hist = _get(url)["results"][0]["historicalDataPrice"]
    return [h["close"] for h in hist if h.get("close") is not None][-(days + 2):]


def stats(closes: list[float]) -> dict:
    """Daily log returns; z of the latest return against the previous ones."""
    rets = [math.log(b / a) for a, b in zip(closes, closes[1:]) if a and b]
    if len(rets) < 10:
        raise ValueError("not enough history")
    today, hist = rets[-1], rets[:-1]
    mu = sum(hist) / len(hist)
    sigma = math.sqrt(sum((r - mu) ** 2 for r in hist) / (len(hist) - 1))
    z = (today - mu) / sigma if sigma > 0 else 0.0
    return {
        "todayRet": round(math.expm1(today), 6),
        "mu": round(mu, 6),
        "sigma": round(sigma, 6),
        "z": round(z, 3),
        "alert": abs(z) > 2,
        "n": len(hist),
        "last": closes[-1],
    }


def for_symbol(symbol: str, cfg: dict, secrets: dict[str, str]) -> dict:
    days = int(cfg.get("window_days", 90))
    provider = cfg.get("provider", "yahoo")
    if provider == "brapi":
        closes = closes_brapi(symbol, days, secrets.get("BRAPI_TOKEN", ""))
    else:
        closes = closes_yahoo(symbol, days)
    return {"symbol": symbol, "provider": provider, **stats(closes)}
