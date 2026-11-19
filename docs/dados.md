# Dados: contratos entre `gw` e os widgets

O `gw` (Python stdlib, `collector/gw/`) é o único que fala com rede, credenciais e herdr. Ele grava JSON de forma atômica em `~/.local/state/gabriellsar-widgets/`, e o QML só observa esses arquivos.

| arquivo | quem escreve | quando | widget |
|---|---|---|---|
| `config.json` | `gw config` | quando `config.toml` muda (`gw-config.path`) | todos |
| `invest.json` | `gw invest` | a cada 5 min (`gw-invest.timer`) | carteira |
| `spotify.json` | `gw spotify playlists` | a cada 1 h (`gw-spotify.timer`) | pomodoro |
| `herdr.json` | `gw herdr watch` | a cada 1,5 s, só quando algo muda (`gw-herdr.service`) | agentes |
| `herdr-faces.json` | `gw herdr watch` | quando surge um agente novo | — |
| `pomodoro.json` | o próprio QML | a cada mudança de fase | pomodoro |

Todo arquivo traz `schema: 1` e `updated` (ISO com fuso). Quando `error` não é `null`, o widget mostra o último dado bom junto de uma Tag `signal` curta e não apaga nada.

## invest.json

```json
{ "source": "mcp|file|fixture", "currency": "USD", "equity": 48210.37, "dayChangePct": 0.0124,
  "dayChangeEstimated": true, "error": null,
  "positions": [{ "ticker": "NVDA", "side": "LONG|SHORT", "qty": 40, "entry": 171.2, "mark": 186.9,
                  "pnl": 628.0, "pnlPct": 0.0917,
                  "market": { "symbol": "NVDA", "todayRet": 0.061, "mu": 0.0015, "sigma": 0.025,
                              "z": 2.4, "alert": true, "n": 89, "last": 186.9 } }] }
```

- `z` é o retorno de hoje (log) contra os 90 dias anteriores, e `alert` vale `|z| > 2`.
- Se o mercado falhar, `market` chega como `{symbol, error}` e a linha aparece sem o ponto no sino.
- Ação: `gw invest` força uma atualização (clique na Tag de sync).

## spotify.json e controles

```json
{ "player": "spotify", "error": null,
  "playlists": [{ "name": "Deep Focus", "uri": "spotify:playlist:…", "favorite": true, "tracks": 120 }] }
```

- Faixa atual, play/pause e capa: use `Quickshell.Services.Mpris` direto no QML (filtre por `identity`/`dbusName` contendo `config.spotify.player`). MPRIS é local e não precisa de credencial.
- Ações via `Process`:
  - `gw spotify ctl prev | play-pause | next | pause | play`
  - `gw spotify ctl open <uri>` (começa a playlist)

## herdr.json e ações

```json
{ "running": true, "error": null,
  "counts": { "working": 1, "blocked": 1, "done": 1, "idle": 1, "unknown": 0 },
  "agents": [{ "id": "w2:p1", "target": "tcc-forecast", "label": "tcc-forecast", "agent": "claude",
               "cwd": "~/tcc", "status": "blocked", "face": "visor", "tint": "data-2",
               "focused": false, "workspace": "w2", "seq": 30,
               "log": ["Treinando LSTM · época 14", "Salvando checkpoint"],
               "prompt": { "tool": "Edit", "file": "model/forecast.py",
                           "diff": [{ "s": "-", "t": "horizon = 12" }, { "s": "+", "t": "horizon = 24" }],
                           "options": ["1 Yes", "2 Yes, allow all edits…", "3 No…"],
                           "lines": ["…últimas 10 linhas visíveis…"] } }] }
```

- `prompt` só aparece quando `status = "blocked"`. É lido da tela por heurística: se `tool`, `file` e `diff` vierem vazios, mostre `lines` cru no bloco de permissão.
- Com o herdr desligado, o arquivo traz `running: false` e o widget mostra o estado vazio (spec de agentes).
- Ações, sempre `gw herdr act <target> <ação>`:

| ação | efeito no herdr |
|---|---|
| `approve` / `always` / `deny` | envia as teclas `1` / `2` / `3` |
| `stop` | `esc` |
| `mode` | `shift+tab` (alterna o modo de permissão) |
| `compact` | prompt `/compact` |
| `send <texto>` | prompt com o texto |
| `focus` | foca a pane no herdr |

  O `act` não espera resposta do agente: o `watch` reflete o novo estado em até 1,5 s.
- "Abrir pane": `gw herdr act <t> focus` e depois foque ou abra a janela do herdr. Se já existir uma janela do terminal com o herdr, use `hyprctl dispatch focuswindow`; se não, abra como Super+Ctrl+Enter abriria (veja o binding em `bindings.lua`).

## config.json

São as partes não secretas do `config.toml`: `pomodoro`, `spotify`, `agents`, `dock` e `invest.{source,refresh_sec,currency}`. Os nomes das chaves são os do `config/config.example.toml`.

## Credenciais (só local)

| onde | o quê |
|---|---|
| `~/.config/gabriellsar-widgets/config.toml` | preferências e o mapeamento do MCP |
| `~/.config/gabriellsar-widgets/secrets.env` (600) | `QUANTFURY_API_KEY`, `BRAPI_TOKEN`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_REFRESH_TOKEN` |
| `~/.config/gabriellsar-widgets/positions.toml` | posições manuais quando `invest.source = "file"` |

`gw init` cria os três a partir de `config/*.example*` e `gw doctor` mostra o que falta.
