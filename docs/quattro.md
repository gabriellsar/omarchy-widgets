# Omarchy Quattro: o que vale para estes plugins

Conferido no branch `quattro` (commit d54cde7, 18/11/2026). Na dúvida, o código instalado em `$OMARCHY_PATH` manda.

## Shell

- Um único processo Quickshell, `omarchy-shell`. Waybar, Walker, Mako e SwayOSD foram aposentados.
- Plugins de usuário ficam em `~/.config/omarchy/plugins/<id>/`: um `manifest.json` (`schemaVersion: 1`) e o QML.
  - Kinds: `bar-widget`, `panel`, `overlay`, `menu`, `service`, `bar`. Um plugin pode ter vários (o `omarchy.media` é `service` + `bar-widget`).
  - O validador checa campos obrigatórios, id fora do namespace `omarchy.`, entry points com caminho relativo que existem e **nenhum symlink dentro da pasta**. A pasta inteira pode ser um symlink, e é assim que `scripts/link-plugins.sh` liga este repo.
  - Plugin de terceiro só fica ativo quando o id aparece em `~/.config/omarchy/shell.json`: num slot de `bar.layout`, em `plugins[]` ou em `bar.id`. `omarchy plugin enable <id>` faz isso por você.
  - Recebe uma interface limitada à própria service e ao próprio ciclo de vida. Os built-ins recebem a interface completa do shell. Um clone (`omarchy plugin clone`) mantém só o que o original precisava.
  - Salvar arquivo na pasta recarrega o plugin. `omarchy-shell shell rescanPlugins` redescobre plugins novos.
- **Bar widgets** recebem `bar`, `moduleName` e `settings`.
  - `bar` traz `foreground`, `background`, `urgent`, `fontFamily`, `position`, `vertical` e `barSize` (26 na horizontal).
  - Também traz `run(cmd)` (aspas via `Util.shellQuote`), `showTooltip`/`hideTooltip` e `requestPopout`/`releasePopout`.
  - Para posicionar: `omarchy bar move`, ou edite `bar.layout` em `shell.json`.
- Layout padrão da barra:
  - left = menu, workspaces
  - centerBegin = indicators
  - center = clock
  - centerEnd = elsewhen, weather, system-update
  - right = tray, keyboard-layout, **agents**, bluetooth, network, audio, monitor, power
- `omarchy.agents` (built-in) mostra **uso e limites das assinaturas de IA** e não sabe nada de herdr. O nosso `gabriellsar.agentes` entra **logo à esquerda dele**.
- Padrões que dá para copiar dos built-ins:
  - `agents/Main.qml`: `FileView` em `~/.local/state/...` com `watchChanges: true` e `onFileChanged: reload()`, mais `Process` para chamar scripts. É o modelo exato dos nossos widgets.
  - `dock/DockWindow.qml`: `PanelWindow` com `WlrLayershell.namespace`, `layer: WlrLayer.Top`, `keyboardFocus: WlrKeyboardFocus.None` e `exclusionMode: ExclusionMode.Normal`. Para saber se há janelas, usa `Hyprland.toplevels`.
  - `dock/Dock.qml`: o modo de cada workspace sai de `omarchy-hyprland-workspace-layout-current` e é atualizado por `omarchy-shell omarchy.dock refresh`. A dock lê `dock.position` e `dock.pinned` em `shell.json`.
  - Imports em uso: `QtQuick`, `Quickshell`, `Quickshell.Io`, `Quickshell.Wayland`, `Quickshell.Hyprland`, `qs.Commons` e `qs.Ui`.
  - `Style`: `space`, `spacing.{xxs,xs,sm,md,lg,xl}`, `font.{caption,bodySmall,body,heading,display,family}`, `duration`, `easeOut`, `reduceMotion`, `gapsOut`, `normalBorderWidth`.
  - `Color`: `background`, `foreground`, `accent`, `urgent`, `menu.*`, `popups.*`, `bar.*`.

## Hyprland e tema

- A config é em Lua: `~/.config/hypr/{hyprland,bindings,looknfeel,…}.lua`. Padrões: gaps_in 5, gaps_out 10, border 2, rounding 0.
- Atalhos que os widgets citam:
  - Super+Enter: terminal
  - Super+Shift+B: navegador
  - Super+Shift+N: editor (VS Code)
  - Super+Shift+F: arquivos
  - Super+Shift+M: Spotify
  - Super+Ctrl+Enter: herdr
  - Super+Space: menu
- O tema ativo é `gabriel-s`. As cores estão em `~/.config/omarchy/themes/gabriel-s/colors.toml` e batem com os tokens do design system (veja `design-system.md`).
- Fundo: o `omarchy.background` já mostra o heightmap estático do tema. Fundo animado é opcional (`specs/05-fundo.md`).

## herdr

- O socket fica em `$HERDR_SOCKET_PATH` ou `~/.config/herdr/herdr.sock`. O protocolo é JSON por linha: `{"id","method","params"}` → `{"id","result"|"error"}`.
- Métodos usados:
  - `agent.list` devolve `agent_status`: `idle`, `working`, `blocked`, `done` ou `unknown`.
  - `agent.read` (`source`: `recent` ou `visible`), `agent.send_keys`, `agent.prompt` e `agent.focus`.
- Não chame o herdr direto do QML: use `gw herdr act` (`docs/dados.md`).
