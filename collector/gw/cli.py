"""gw: data side of gabriellsar-widgets.

  gw init                     cria config.toml / secrets.env / positions.toml locais
  gw doctor                   checa config, credenciais, dependências
  gw config                   exporta preferências para state/config.json (QML)
  gw invest                   Quantfury + mercado -> state/invest.json
  gw mcp tools                lista as tools do MCP configurado (para preencher os nomes)
  gw spotify playlists        -> state/spotify.json
  gw spotify auth             login PKCE único (salva o refresh token)
  gw spotify ctl prev|play-pause|next|open URI
  gw herdr watch [--once]     -> state/herdr.json
  gw herdr act TARGET ACTION [TEXT]
  gw fixtures                 escreve dados de exemplo (sem credenciais)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from . import config as C

REPO = Path(__file__).resolve().parents[2]


def cmd_init(_: argparse.Namespace) -> int:
    C.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    for src, dst, mode in (("config.example.toml", C.CONFIG_FILE, 0o644),
                           ("secrets.example.env", C.SECRETS_FILE, 0o600),
                           ("positions.example.toml", C.CONFIG_DIR / "positions.toml", 0o644)):
        if dst.exists():
            print(f"mantido  {dst}")
            continue
        shutil.copy(REPO / "config" / src, dst)
        os.chmod(dst, mode)
        print(f"criado   {dst}")
    C.export_public()
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    cfg, sec = C.load(), C.secrets()
    ok = True

    def line(good: bool, msg: str) -> None:
        nonlocal ok
        ok &= good
        print(("  ok  " if good else "  --  ") + msg)

    print("arquivos")
    line(C.CONFIG_FILE.exists(), f"config   {C.CONFIG_FILE}")
    line(C.SECRETS_FILE.exists(), f"secrets  {C.SECRETS_FILE}")
    if C.SECRETS_FILE.exists():
        line(oct(C.SECRETS_FILE.stat().st_mode & 0o777) == "0o600", "secrets.env com chmod 600")
    print("carteira")
    inv = cfg["invest"]
    if inv["source"] == "mcp":
        m = inv["mcp"]
        line(bool(m["command"] or m["url"]), "invest.mcp.command ou invest.mcp.url definido")
        line(bool(m["positions_tool"]), "invest.mcp.positions_tool definido (rode `gw mcp tools`)")
        for k in m.get("secret_env", []):
            line(bool(sec.get(k)), f"secrets.env tem {k}")
    else:
        pf = C.expand(inv["file"]["path"]) if inv["file"]["path"] else C.CONFIG_DIR / "positions.toml"
        line(pf.exists(), f"positions file {pf}")
    if inv["market"]["provider"] == "brapi":
        line(bool(sec.get("BRAPI_TOKEN")), "secrets.env tem BRAPI_TOKEN")
    print("spotify")
    line(bool(shutil.which("playerctl")), "playerctl instalado (controle via MPRIS)")
    if cfg["spotify"]["use_web_api"]:
        line(bool(sec.get("SPOTIFY_CLIENT_ID")), "secrets.env tem SPOTIFY_CLIENT_ID")
        line(bool(sec.get("SPOTIFY_REFRESH_TOKEN")), "secrets.env tem SPOTIFY_REFRESH_TOKEN (rode `gw spotify auth`)")
    else:
        line(bool(cfg["spotify"]["playlists"]), "spotify.playlists com favoritas (Web API desligada)")
    print("agentes")
    from .herdr import socket_path
    line(bool(shutil.which("herdr")), "herdr instalado")
    line(socket_path().exists(), f"socket {socket_path()}")
    return 0 if ok else 1


def cmd_config(_: argparse.Namespace) -> int:
    print(C.export_public())
    return 0


def cmd_invest(a: argparse.Namespace) -> int:
    from . import invest
    out = invest.run(C.load(), C.secrets())
    if a.print:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    return 1 if out.get("error") else 0


def cmd_mcp(a: argparse.Namespace) -> int:
    from .mcp import Client
    cfg = C.load()["invest"]["mcp"]
    with Client(cfg, C.secrets()) as mcp:
        if a.what == "tools":
            for t in mcp.tools():
                print(f"{t['name']}\n    {(t.get('description') or '').strip()[:160]}")
        else:
            print(json.dumps(mcp.tool(a.what, json.loads(a.args or "{}")), indent=1, ensure_ascii=False))
    return 0


def cmd_spotify(a: argparse.Namespace) -> int:
    from . import spotify
    cfg, sec = C.load(), C.secrets()
    if a.what == "auth":
        spotify.auth(sec.get("SPOTIFY_CLIENT_ID", ""))
        return 0
    if a.what == "playlists":
        out = spotify.playlists(cfg, sec)
        return 1 if out.get("error") else 0
    if a.what == "ctl":
        return spotify.control(a.rest[0], cfg["spotify"]["player"], a.rest[1] if len(a.rest) > 1 else "")
    return 2


def cmd_herdr(a: argparse.Namespace) -> int:
    from . import herdr
    if a.what == "watch":
        herdr.watch(C.load(), once=a.once)
        return 0
    if a.what == "act":
        target, action, *text = a.rest
        try:
            herdr.act(target, action, " ".join(text))
        except herdr.HerdrError as e:
            print(e, file=sys.stderr)
            return 1
        return 0
    return 2


def cmd_fixtures(_: argparse.Namespace) -> int:
    from . import fixtures
    C.export_public()
    for p in fixtures.write_all():
        print(p)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gw", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    sub.add_parser("config").set_defaults(fn=cmd_config)
    s = sub.add_parser("invest")
    s.add_argument("--print", action="store_true")
    s.set_defaults(fn=cmd_invest)
    s = sub.add_parser("mcp")
    s.add_argument("what", help="`tools` ou o nome de uma tool para testar")
    s.add_argument("args", nargs="?", help="argumentos JSON da tool")
    s.set_defaults(fn=cmd_mcp)
    s = sub.add_parser("spotify")
    s.add_argument("what", choices=["auth", "playlists", "ctl"])
    s.add_argument("rest", nargs="*")
    s.set_defaults(fn=cmd_spotify)
    s = sub.add_parser("herdr")
    s.add_argument("what", choices=["watch", "act"])
    s.add_argument("--once", action="store_true")
    s.add_argument("rest", nargs="*")
    s.set_defaults(fn=cmd_herdr)
    sub.add_parser("fixtures").set_defaults(fn=cmd_fixtures)
    a = p.parse_args(argv)
    return a.fn(a)
