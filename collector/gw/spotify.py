"""Spotify for the pomodoro.

Playback (prev / play-pause / next / open playlist) goes through MPRIS with
playerctl: no credentials. The playlist list comes from config favourites and,
if you opt in, from the Web API (PKCE: only SPOTIFY_CLIENT_ID is needed; the
refresh token is saved in secrets.env by `gw spotify auth`).
"""
from __future__ import annotations

import base64
import hashlib
import http.server
import json
import os
import secrets as pysecrets
import subprocess
import threading
import urllib.parse
import urllib.request
import webbrowser

from .config import SECRETS_FILE
from .state import write_json

REDIRECT = "http://127.0.0.1:8888/callback"
SCOPES = "playlist-read-private playlist-read-collaborative"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def _post(url: str, data: dict) -> dict:
    req = urllib.request.Request(url, urllib.parse.urlencode(data).encode(),
                                 {"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode())


def _api(path: str, token: str) -> dict:
    req = urllib.request.Request("https://api.spotify.com/v1" + path, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.loads(res.read().decode())


def save_secret(key: str, value: str) -> None:
    SECRETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = SECRETS_FILE.read_text().splitlines() if SECRETS_FILE.exists() else []
    lines = [l for l in lines if not l.startswith(key + "=")] + [f"{key}={value}"]
    SECRETS_FILE.write_text("\n".join(lines) + "\n")
    os.chmod(SECRETS_FILE, 0o600)


def auth(client_id: str) -> None:
    """One-time PKCE login in the browser; stores SPOTIFY_REFRESH_TOKEN."""
    if not client_id:
        raise SystemExit("SPOTIFY_CLIENT_ID missing in secrets.env (create an app at developer.spotify.com,"
                         f" redirect URI {REDIRECT})")
    verifier = base64.urlsafe_b64encode(pysecrets.token_bytes(48)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = pysecrets.token_urlsafe(16)
    got: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"gabriellsar-widgets: ok, pode fechar esta aba.")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 8888), H)
    threading.Thread(target=srv.handle_request, daemon=True).start()
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": client_id, "response_type": "code", "redirect_uri": REDIRECT,
        "code_challenge_method": "S256", "code_challenge": challenge, "scope": SCOPES, "state": state})
    print("Abrindo o navegador para o login do Spotify…\n" + url)
    webbrowser.open(url)
    srv.timeout = 300
    while "code" not in got and "error" not in got:
        srv.handle_request()
    if got.get("state") != state or "code" not in got:
        raise SystemExit(f"login falhou: {got.get('error', 'state inválido')}")
    tok = _post(TOKEN_URL, {"grant_type": "authorization_code", "code": got["code"], "redirect_uri": REDIRECT,
                            "client_id": client_id, "code_verifier": verifier})
    save_secret("SPOTIFY_REFRESH_TOKEN", tok["refresh_token"])
    print(f"Refresh token salvo em {SECRETS_FILE}")


def access_token(sec: dict[str, str]) -> str:
    tok = _post(TOKEN_URL, {"grant_type": "refresh_token", "refresh_token": sec["SPOTIFY_REFRESH_TOKEN"],
                            "client_id": sec["SPOTIFY_CLIENT_ID"]})
    if tok.get("refresh_token"):  # Spotify may rotate it
        save_secret("SPOTIFY_REFRESH_TOKEN", tok["refresh_token"])
    return tok["access_token"]


def playlists(cfg: dict, sec: dict[str, str]) -> dict:
    scfg = cfg["spotify"]
    items = [{"name": p["name"], "uri": p["uri"], "favorite": True} for p in scfg.get("playlists", [])]
    error = None
    if scfg.get("use_web_api"):
        try:
            token = access_token(sec)
            url = "/me/playlists?limit=50"
            seen = {p["uri"] for p in items}
            while url:
                page = _api(url, token)
                for p in page.get("items", []):
                    if p and p["uri"] not in seen:
                        items.append({"name": p["name"], "uri": p["uri"], "favorite": False,
                                      "tracks": (p.get("tracks") or {}).get("total")})
                nxt = page.get("next")
                url = nxt.replace("https://api.spotify.com/v1", "") if nxt else None
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
    out = {"player": scfg.get("player", "spotify"), "playlists": items, "error": error}
    write_json("spotify", out)
    return out


def control(action: str, player: str = "spotify", uri: str = "") -> int:
    """prev | play-pause | next | open <uri>. Used by the QML via Process."""
    cmd = {"prev": ["previous"], "play-pause": ["play-pause"], "next": ["next"],
           "pause": ["pause"], "play": ["play"], "open": ["open", uri]}[action]
    return subprocess.call(["playerctl", "-p", player, *cmd])
