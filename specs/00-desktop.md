# 00 · Camada do desktop (vale para todos os widgets)

Board: `ref/Desktop.dc.html` (1920×1080), `ref/DesktopJanelas.dc.html` e `ref/DesktopJanelasAgentes.dc.html`.

## Onde fica cada coisa (1920×1080, barra de 26px no topo)

| widget | âncora | posição | largura |
|---|---|---|---|
| Carteira | top-left | x 48, y 74 | 400 |
| Pomodoro | top-left | x 48, y 450 | 400 |
| Agentes | top-right | right 48, y 74 | 580 aberto / 78 fechado |
| Dock | bottom-center | bottom 32 | conteúdo |

O y é medido do topo da tela, então já desconta os 26px da barra. Em outras resoluções, mantenha as margens (48 nas laterais, 74 no topo, 32 embaixo) e nunca escale.

## Visibilidade

- Os widgets só existem com o **workspace vazio**: `common/DesktopState.qml` → `empty`.
- Quando uma janela abre, todos somem com fade de opacidade 1→0 em `durBase` 200ms ease-out, sem slide, e ao fim ficam `visible: false` (não roubam clique).
- Quando a última janela fecha, voltam com fade 0→1.
- Tela cheia esconde tudo, inclusive a dock.
- Cada monitor mostra o próprio conjunto: um `PanelWindow` por tela via `Variants { model: Quickshell.screens }`.
- Layer: `WlrLayer.Bottom`, acima do fundo e abaixo das janelas, com `exclusionMode: ExclusionMode.Ignore` e `keyboardFocus: None`.
  - Exceção 1: o painel de agentes chamado pela barra (spec 03).
  - Exceção 2: o input de mensagem dos agentes, que pede foco `OnDemand`.
- O `PanelWindow` tem o tamanho do cartão, não da tela inteira. Assim o resto do desktop continua clicável (o clique no fundo é do `omarchy.background`).

## Estados que todo widget precisa ter

- **Carregando:** sem arquivo ainda. O cartão aparece com os labels e um traço `—` no lugar dos números, em `muted`.
- **Erro:** `error` diferente de null. Mantém o último dado bom e troca a Tag de status por `signal` com uma palavra (`OFFLINE`, `SEM MCP`, `HERDR OFF`). O tooltip traz o erro completo.
- **Vazio:** o texto do próprio spec, em `muted`.
