# 04 · Dock (clone de `omarchy.dock`)

Escolha: **Dock A — Régua**. Board: `ref/DockRegua.dc.html`; a composição final está em `ref/Desktop.dc.html`.

## Como começar

```bash
omarchy plugin clone omarchy.dock        # cria ~/.config/omarchy/plugins/<usuário>.dock e já troca o shell para ela
mv ~/.config/omarchy/plugins/<usuário>.dock plugins/
scripts/link-plugins.sh <usuário>.dock
omarchy plugin list | grep dock          # confirme que o clone segue ativo no lugar do built-in
```

Mantenha o id que o clone gerou, porque o roteamento do built-in para o clone depende dele. Mexa o mínimo no comportamento: pins, ordem por arrastar, grade de apps e casamento janela↔desktop entry continuam do original.

## O que muda

### Visibilidade

O original aparece em workspaces *floating* e some nos *tiled*. A regra nova é a de `00-desktop.md`: aparece com o workspace vazio, seja qual for o layout, e some com a primeira janela ou em tela cheia. Use `common/DesktopState.qml`. O `autohide` do original pode continuar como opção.

### Visual

- Barra na posição `bottom`, a 32px da borda, centralizada.
- Contêiner: padding 6, gap 4, fundo `surface`, borda 1px `lineStrong` e raio 0.
- Item: 44×44, ícone de **traço** monocromático de 20px (stroke 1.5, linecap square, join miter) em vez do ícone colorido do app.
  - Cor `muted` no normal e `textStrong` no ativo ou no hover. Hover troca o fundo para `inset`.
  - Ativo (janela focada no workspace atual): sublinhado de 2px `accent` com inset de 10px.
  - Rodando sem foco: ponto de 4px `muted`, centrado, a 3px da base.
- Paths dos traços: estão no board para ghostty, vscode, chrome, yazi, spotify, godot e btop.
  - Faça um mapa `desktop id → path` em `common/` (via `shared/`).
  - App sem path no mapa usa o ícone do tema, dessaturado e com opacidade 0.7.
- Tooltip: 56px acima do item, padding 6 10, `surface` com borda `lineStrong`, mono 11 com tracking 0.14em, `textStrong`. O formato é `VS CODE · SUPER ⇧ N`, com o atalho em `muted`. Os atalhos estão em `docs/quattro.md`.
- Depois dos apps vem um separador de 1×28 em `lineStrong` (margin 0 6) e o botão de 44×44 com borda **tracejada** 1px `control` e um `+` em `muted`, que abre a grade de apps do original.

### Apps

`config.json → dock.apps`, quando não está vazio, sobrescreve os pins de `shell.json`. Se a sobrescrita complicar o clone, mantenha os pins do `shell.json` e documente.
