"""Minimal MCP client (stdio or Streamable HTTP), stdlib only.

Only what the collector needs: initialize, tools/list, tools/call.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from typing import Any

PROTOCOL = "2025-06-18"
CLIENT = {"name": "gabriellsar-widgets", "version": "0.1.0"}


class MCPError(RuntimeError):
    pass


class _Stdio:
    def __init__(self, command: list[str], env: dict[str, str]):
        if not command:
            raise MCPError("invest.mcp.command is empty")
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env={**os.environ, **env},
            text=True,
            bufsize=1,
        )

    def send(self, msg: dict) -> None:
        assert self.proc.stdin
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def request(self, msg: dict) -> dict:
        self.send(msg)
        assert self.proc.stdout
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise MCPError("MCP server closed stdout")
            try:
                reply = json.loads(line)
            except ValueError:
                continue  # servers sometimes log to stdout
            if reply.get("id") == msg["id"]:
                return reply

    def close(self) -> None:
        try:
            self.proc.terminate()
            self.proc.wait(timeout=3)
        except Exception:
            self.proc.kill()


class _Http:
    def __init__(self, url: str, headers: dict[str, str]):
        self.url = url
        self.headers = headers
        self.session: str | None = None

    def _post(self, msg: dict) -> dict | None:
        hdrs = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL,
            **self.headers,
        }
        if self.session:
            hdrs["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(self.url, json.dumps(msg).encode(), hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=30) as res:
            self.session = res.headers.get("Mcp-Session-Id", self.session)
            body = res.read().decode()
            ctype = res.headers.get("Content-Type", "")
        if not body.strip():
            return None
        if "text/event-stream" in ctype:
            for block in body.split("\n\n"):
                data = "".join(l[5:].strip() for l in block.splitlines() if l.startswith("data:"))
                if data:
                    reply = json.loads(data)
                    if reply.get("id") == msg.get("id"):
                        return reply
            return None
        return json.loads(body)

    def send(self, msg: dict) -> None:
        self._post(msg)

    def request(self, msg: dict) -> dict:
        reply = self._post(msg)
        if reply is None:
            raise MCPError("empty MCP reply")
        return reply

    def close(self) -> None:
        pass


class Client:
    def __init__(self, cfg: dict, secrets: dict[str, str]):
        env = {k: secrets[k] for k in cfg.get("secret_env", []) if k in secrets}
        # header values may reference secrets as ${NAME}
        headers = {k: _sub(str(v), secrets) for k, v in cfg.get("headers", {}).items()}
        if cfg.get("url"):
            self.t = _Http(cfg["url"], headers)
        else:
            self.t = _Stdio(list(cfg.get("command", [])), env)
        self._id = 0

    def __enter__(self) -> "Client":
        self.call("initialize", {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": CLIENT})
        self.t.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return self

    def __exit__(self, *exc) -> None:
        self.t.close()

    def call(self, method: str, params: dict | None = None) -> Any:
        self._id += 1
        reply = self.t.request({"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}})
        if "error" in reply:
            raise MCPError(f"{method}: {reply['error'].get('message', reply['error'])}")
        return reply.get("result")

    def tools(self) -> list[dict]:
        return (self.call("tools/list") or {}).get("tools", [])

    def tool(self, name: str, args: dict | None = None) -> Any:
        res = self.call("tools/call", {"name": name, "arguments": args or {}}) or {}
        if res.get("isError"):
            raise MCPError(f"tool {name}: {_text(res)}")
        if res.get("structuredContent") is not None:
            return res["structuredContent"]
        text = _text(res)
        try:
            return json.loads(text)
        except ValueError:
            return {"text": text}


def _text(res: dict) -> str:
    return "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")


def _sub(value: str, secrets: dict[str, str]) -> str:
    for k, v in secrets.items():
        value = value.replace("${" + k + "}", v)
    return value
