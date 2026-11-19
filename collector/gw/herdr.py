"""Agentes: herdr sessions for the widget, and the actions it can take.

Talks to the herdr socket (newline-delimited JSON). No credentials: the socket
is $HERDR_SOCKET_PATH or ~/.config/herdr/herdr.sock. `watch` keeps
state/herdr.json current; `act` is what the QML calls on a button press.
"""
from __future__ import annotations

import json
import os
import re
import socket
import time
from pathlib import Path

from .state import read_json, write_json

STATUSES = ("working", "blocked", "done", "idle", "unknown")


def socket_path() -> Path:
    if os.environ.get("HERDR_SOCKET_PATH"):
        return Path(os.environ["HERDR_SOCKET_PATH"])
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "herdr" / "herdr.sock"


class HerdrError(RuntimeError):
    pass


_seq = 0


def request(method: str, params: dict | None = None, timeout: float = 5.0) -> dict:
    global _seq
    _seq += 1
    rid = f"gw_{os.getpid()}_{_seq}"
    msg = json.dumps({"id": rid, "method": method, "params": params or {}}) + "\n"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect(str(socket_path()))
        except OSError as e:
            raise HerdrError(f"herdr não está rodando ({socket_path()}): {e}") from e
        s.sendall(msg.encode())
        buf = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                reply = json.loads(line)
                if reply.get("id") == rid:
                    if "error" in reply:
                        raise HerdrError(reply["error"].get("message", str(reply["error"])))
                    return reply.get("result", {})
    raise HerdrError("no reply")


def _faces(cfg: dict, names: list[str]) -> dict[str, dict]:
    """Stable face+tint per agent name. Config `assign` wins; new names round-robin."""
    acfg = cfg["agents"]
    saved = read_json("herdr-faces").get("assign", {})
    assign = {**saved, **acfg.get("assign", {})}
    faces, tints = acfg["faces"], acfg["tints"]
    for n in names:
        if n not in assign:
            k = len(assign)
            assign[n] = {"face": faces[k % len(faces)], "tint": tints[(k // len(faces) + k) % len(tints)]}
    if assign != saved:
        write_json("herdr-faces", {"assign": assign})
    return assign


CALL = re.compile(r"\b(Edit|MultiEdit|Write|Update|Create|Bash|Read|WebFetch|WebSearch|NotebookEdit)\(([^)]*)\)")
ASK_FILE = re.compile(r"(?:to|edit|write|create|read)\s+([\w./~-]+\.\w+)", re.I)
DIFF = re.compile(r"^\s*\d*\s*([+-])\s?(\S.*)$")
OPTION = re.compile(r"^\s*[❯>]?\s*(\d)\.\s+(.+)$", re.M)


def parse_prompt(text: str) -> dict:
    """Best effort over the visible screen of a blocked agent (Claude Code style).
    The widget shows `lines` verbatim when tool/file/diff come back empty."""
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    tail = lines[-16:]
    joined = "\n".join(tail)
    call = CALL.search(joined)
    ask = ASK_FILE.search(joined)
    diff = []
    for l in tail:
        m = DIFF.match(l)
        if m and not OPTION.match(l):
            diff.append({"s": m.group(1), "t": m.group(2).strip()})
    return {
        "tool": call.group(1) if call else "",
        "file": (call.group(2) if call and call.group(2) else (ask.group(1) if ask else "")),
        "diff": diff[:6],
        "options": [f"{m.group(1)} {m.group(2).strip()}" for m in OPTION.finditer(joined)][:3],
        "lines": tail[-10:],
    }


def snapshot(cfg: dict) -> dict:
    res = request("agent.list")
    agents = res.get("agents", res if isinstance(res, list) else [])
    names = [a.get("name") or a.get("pane_id") for a in agents]
    faces = _faces(cfg, names)
    n = int(cfg["agents"]["log_lines"])
    out = []
    for a, name in zip(agents, names):
        st = a.get("agent_status", "unknown")
        target = a.get("name") or a["pane_id"]
        log: list[str] = []
        prompt = None
        try:
            text = request("agent.read", {"target": target, "source": "recent", "lines": 40})["read"]["text"]
            log = [l.rstrip() for l in text.splitlines() if l.strip()][-n:]
            if st == "blocked":
                screen = request("agent.read", {"target": target, "source": "visible"})["read"]["text"]
                prompt = parse_prompt(screen)
        except (HerdrError, KeyError, ValueError):
            pass
        cwd = a.get("foreground_cwd") or a.get("cwd") or ""
        out.append({
            "id": a["pane_id"], "target": target, "label": name,
            "agent": a.get("display_agent") or a.get("agent") or "",
            "cwd": cwd.replace(str(Path.home()), "~"),
            "status": st if st in STATUSES else "unknown",
            "focused": a.get("focused", False),
            "workspace": a.get("workspace_id"), "seq": a.get("state_change_seq", 0),
            "face": faces[name]["face"], "tint": faces[name]["tint"],
            "log": log, "prompt": prompt,
        })
    counts = {s: sum(1 for x in out if x["status"] == s) for s in STATUSES}
    return {"running": True, "agents": out, "counts": counts, "error": None}


def watch(cfg: dict, once: bool = False) -> None:
    delay = int(cfg["agents"]["poll_ms"]) / 1000
    last = None
    while True:
        try:
            data = snapshot(cfg)
        except HerdrError as e:
            data = {"running": False, "agents": [], "counts": {}, "error": str(e)}
        key = json.dumps(data, sort_keys=True)
        if key != last:  # only touch the file when something changed
            write_json("herdr", data)
            last = key
        if once:
            return
        time.sleep(delay if data["running"] else 5)


MODES_KEY = "shift+tab"


def act(target: str, action: str, text: str = "") -> dict:
    """approve | always | deny | stop | mode | compact | send <text> | focus"""
    if action in ("approve", "always", "deny"):
        key = {"approve": "1", "always": "2", "deny": "3"}[action]
        return request("agent.send_keys", {"target": target, "keys": [key]})
    if action == "stop":
        return request("agent.send_keys", {"target": target, "keys": ["esc"]})
    if action == "mode":
        return request("agent.send_keys", {"target": target, "keys": [MODES_KEY]})
    if action == "compact":
        return request("agent.prompt", {"target": target, "text": "/compact"})
    if action == "send":
        if not text.strip():
            raise HerdrError("mensagem vazia")
        return request("agent.prompt", {"target": target, "text": text})
    if action == "focus":
        return request("agent.focus", {"target": target})
    raise HerdrError(f"ação desconhecida: {action}")
