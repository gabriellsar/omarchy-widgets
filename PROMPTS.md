# Prompts para os agentes (Claude Code CLI)

Cole um destes no `claude`, aberto no worktree do widget (veja `docs/fluxo.md`). Todos partem do `CLAUDE.md`, que o Claude Code carrega sozinho.

---

## 1 · Pomodoro

```
Implemente o plugin gabriellsar.pomodoro seguindo specs/00-desktop.md e specs/02-pomodoro.md.
Antes de tudo: leia CLAUDE.md, docs/quattro.md, docs/design-system.md, docs/dados.md e o board
specs/ref/PomoPontos.dc.html (a composição final está em specs/ref/Desktop.dc.html). Depois leia o
código instalado do Omarchy: $OMARCHY_PATH/shell/plugins/dock (PanelWindow, layer shell),
agents/Main.qml (FileView + Process) e shell/Commons (Color, Style).
Entre em plan mode e me mostre o plano. Inclua o que você vai mudar em shared/Tokens.qml e em
shared/DesktopState.qml depois de conferir os nomes reais das APIs.
Use `gw fixtures` para os dados e Quickshell.Services.Mpris para a faixa atual.
Valide com `omarchy plugin validate`, ligue com scripts/link-plugins.sh e compare um screenshot com o board.
Commits pequenos em português, sem atribuição a IA. Abra o PR do branch widget/pomodoro para main.
```

## 2 · Carteira

```
Implemente o plugin gabriellsar.carteira seguindo specs/00-desktop.md e specs/01-carteira.md.
Leia CLAUDE.md, docs/*.md e os boards specs/ref/InvestCarteira.dc.html e specs/ref/Desktop.dc.html
(seção "Carteira Quantfury"). Reaproveite shared/Tokens.qml e shared/DesktopState.qml. Se eles
ainda forem esqueletos, confira as APIs no código instalado do Omarchy e ajuste num commit separado.
O dado vem só de ~/.local/state/gabriellsar-widgets/invest.json (rode `gw fixtures`). Desenhe o sino
com Shape/PathSvg como o spec descreve. Teste os estados carregando, erro e vazio.
Plan mode primeiro. Valide, ligue, compare o screenshot, abra o PR widget/carteira, sem atribuição a IA.
```

## 3 · Agentes

```
Implemente o plugin gabriellsar.agentes (service + bar-widget) seguindo specs/00-desktop.md e
specs/03-agentes.md. Leia CLAUDE.md, docs/*.md e os boards specs/ref/AgentesWidget.dc.html,
AgentesRostos.dc.html e DesktopJanelasAgentes.dc.html. AgentesWidget tem a lógica de interação em
JS no fim do arquivo: siga a mesma lógica.
Os rostos e os ícones ficam em shared/Faces.js. Os dados vêm de herdr.json (`gw fixtures` para
começar, depois `gw herdr watch` com o herdr real). As ações são sempre `gw herdr act`.
Confira em $OMARCHY_PATH/docs/omarchy-shell.md e em plugins como omarchy.media como um bar-widget
de terceiro fala com a própria service, e como posicionar o widget à esquerda de omarchy.agents.
Para o botão "Novo agente", adicione `start` ao `gw herdr act` (veja `herdr agent start --help`) e
documente em docs/dados.md.
Plan mode primeiro: esta é a peça maior, quebre em etapas (trilho fechado → painel → permissão →
mensagem → botão da barra → painel chamado por cima das janelas). Abra o PR widget/agentes, sem atribuição a IA.
```

## 4 · Dock

```
Faça a dock seguindo specs/04-dock.md. Clone com `omarchy plugin clone omarchy.dock`, mova o clone
para plugins/ deste repo e ligue com scripts/link-plugins.sh. Mude o mínimo: a regra de
visibilidade (shared/DesktopState.qml) e o visual Régua de specs/ref/DockRegua.dc.html, com ícones
de traço. Pins, arrastar e grade de apps continuam iguais.
Plan mode primeiro. Abra o PR widget/dock, sem atribuição a IA.
```

## 5 · Fundo animado (opcional)

```
Leia specs/05-fundo.md. Proponha, sem implementar ainda, como fazer o heightmap animado como shader
num clone de omarchy.background, com as medidas de consumo. Lembre: sem o ponto/anel laranja.
```
