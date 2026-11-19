"""Testes do gw sem rede nem credenciais: `python3 -m unittest discover tests`."""
import json
import math
import os
import random
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAKES = ROOT / "tests" / "fakes"
sys.path.insert(0, str(ROOT / "collector"))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.env = {**os.environ, "XDG_CONFIG_HOME": f"{self.tmp}/cfg", "XDG_STATE_HOME": f"{self.tmp}/state"}
        self.gw("init")

    def gw(self, *args, env=None):
        return subprocess.run([sys.executable, str(ROOT / "bin" / "gw"), *args], env=env or self.env,
                              capture_output=True, text=True)

    def state(self, name):
        return json.loads(Path(f"{self.tmp}/state/gabriellsar-widgets/{name}.json").read_text())


class TestMarket(unittest.TestCase):
    def test_z_of_outlier(self):
        from gw import market
        random.seed(1)
        c = [100.0]
        for _ in range(92):
            c.append(c[-1] * math.exp(random.gauss(0, 0.02)))
        c[-1] = c[-2] * math.exp(0.06)
        s = market.stats(c)
        self.assertTrue(s["alert"])
        self.assertGreater(s["z"], 2)
        self.assertEqual(s["n"], 91)


class TestFixtures(Base):
    def test_fixtures(self):
        self.assertEqual(self.gw("fixtures").returncode, 0)
        self.assertEqual(len(self.state("invest")["positions"]), 3)
        self.assertEqual(self.state("herdr")["counts"]["blocked"], 1)
        self.assertIn("pomodoro", self.state("config"))


class TestMCP(Base):
    def test_stdio_mapping(self):
        cfg = Path(f"{self.tmp}/mcp.toml")
        cfg.write_text(f'''
[invest]
source = "mcp"
[invest.market]
symbol_map = {{ BTC = "__nope__", ETH = "__nope__" }}
[invest.mcp]
command = ["{sys.executable}", "{FAKES / 'fake_mcp.py'}"]
secret_env = ["QUANTFURY_API_KEY"]
positions_tool = "get_open_positions"
account_tool = "get_account"
[invest.mcp.map]
positions = "data.items"
ticker = "instrument"
side = "direction"
qty = "amount"
entry = "openPrice"
mark = "price"
pnl = "pl"
equity = "balance.equity"
''')
        env = {**self.env, "GW_CONFIG": str(cfg), "HTTPS_PROXY": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9"}
        self.gw("invest", env=env)
        d = self.state("invest")
        self.assertIsNone(d["error"])
        self.assertEqual(d["equity"], 48210.37)
        self.assertEqual([(p["ticker"], p["side"]) for p in d["positions"]], [("BTC", "LONG"), ("ETH", "SHORT")])
        self.assertAlmostEqual(d["positions"][0]["pnlPct"], 0.04869, places=4)


class TestHerdr(Base):
    def test_watch_and_act(self):
        sock = f"{self.tmp}/h.sock"
        log = f"{self.tmp}/h.log"
        srv = subprocess.Popen([sys.executable, str(FAKES / "fake_herdr.py"), sock, log])
        try:
            for _ in range(50):
                if os.path.exists(sock):
                    break
                time.sleep(0.05)
            env = {**self.env, "HERDR_SOCKET_PATH": sock}
            self.assertEqual(self.gw("herdr", "watch", "--once", env=env).returncode, 0)
            d = self.state("herdr")
            self.assertEqual(d["counts"]["blocked"], 1)
            p = d["agents"][1]["prompt"]
            self.assertEqual((p["tool"], p["file"]), ("Update", "model/forecast.py"))
            self.assertEqual(len(p["diff"]), 3)
            self.assertEqual(self.gw("herdr", "act", "tcc-forecast", "approve", env=env).returncode, 0)
            sent = [json.loads(l) for l in Path(log).read_text().splitlines()]
            self.assertEqual(sent[-1]["params"], {"target": "tcc-forecast", "keys": ["1"]})
        finally:
            srv.kill()

    def test_offline(self):
        env = {**self.env, "HERDR_SOCKET_PATH": f"{self.tmp}/none.sock"}
        self.gw("herdr", "watch", "--once", env=env)
        self.assertFalse(self.state("herdr")["running"])


if __name__ == "__main__":
    unittest.main()
