# omarchy-widgets

Os widgets do meu desktop no Omarchy 4 "Quattro", como plugins do `omarchy-shell`:

| plugin | o quê | dados |
|---|---|---|
| `gabriellsar.carteira` | posições da Quantfury e o dia de cada ativo contra a curva de 90 dias | MCP da Quantfury ou arquivo manual, mais Yahoo |
| `gabriellsar.pomodoro` | timer em anel de pontos, com playlist e controles do Spotify | MPRIS, mais a Web API opcional |
| `gabriellsar.agentes` | sessões do herdr com rosto e cor, permissões e mensagens | socket do herdr |
| dock (clone de `omarchy.dock`) | régua com os meus apps | `shell.json` |

Os widgets ficam no desktop vazio e somem quando uma janela abre. O de agentes também pode ser chamado pela barra, por cima de tudo.

Os designs estão em `specs/` e as regras para os agentes que implementam, em `CLAUDE.md` e `PROMPTS.md`.

## Instalar a parte de dados

```bash
scripts/install.sh   # gw em ~/.local/bin, config local e timers do systemd --user
gw doctor            # mostra o que falta
```

Nada de credencial fica no repo. Só preencha os arquivos locais que o `gw init` criou:

### `~/.config/gabriellsar-widgets/secrets.env` (chmod 600)

| chave | precisa quando |
|---|---|
| `QUANTFURY_API_KEY` | o seu MCP da Quantfury pede chave (o nome é livre: ele tem que bater com `secret_env` ou com `headers`) |
| `BRAPI_TOKEN` | `invest.market.provider = "brapi"` (ações da B3) |
| `SPOTIFY_CLIENT_ID` | `spotify.use_web_api = true`. Crie o app em developer.spotify.com com o redirect `http://127.0.0.1:8888/callback` |
| `SPOTIFY_REFRESH_TOKEN` | é preenchido sozinho por `gw spotify auth` |

### `~/.config/gabriellsar-widgets/config.toml`

- **Carteira via MCP**:
  1. Ponha `invest.source = "mcp"`.
  2. Copie em `invest.mcp.command` o comando do servidor (o mesmo que `claude mcp get <nome>` mostra), ou a `url`, se for HTTP.
  3. Rode `gw mcp tools` e preencha `positions_tool` e, se houver, `account_tool`.
  4. Rode `gw mcp <tool>` para ver o JSON e ajuste `[invest.mcp.map]`.
  5. Confira com `gw invest --print`.
- **Carteira manual**: deixe `invest.source = "file"` e edite `positions.toml`.
- **Spotify**: as favoritas em `[[spotify.playlists]]` já bastam para os controles. Os controles usam `playerctl`.
- **Agentes**: só precisam do herdr rodando. Para fixar rosto e cor por agente, use `agents.assign`.

## Ligar os plugins

```bash
scripts/link-plugins.sh --enable    # todos: symlink em ~/.config/omarchy/plugins/ + validate + enable
```

Para desfazer: `scripts/uninstall.sh` e `omarchy plugin remove <id>`.
