# Design system gabriel.s → QML

Fonte: o artefato "Design System - Gabriel" (namespace `gabriel-s`). Os tokens estão copiados em `specs/ref/tokens.css`, no modo escuro. Em QML, use sempre `common/Tokens.qml`.

## Cores

| token CSS | Tokens.qml | hex | colors.toml | uso |
|---|---|---|---|---|
| `--bg` | `bg` | #0a0c0d | background | fundo |
| `--surface` | `surface` | #10181a | lighter_background | cartão de widget |
| `--inset` | `inset` | #0b1214 | — | áreas internas, linha selecionada, log |
| `--line` | `line` | #1a2628 | — | divisórias internas |
| `--line-strong` | `lineStrong` | #263638 | — | borda de cartão, cabeçalho de tabela |
| `--control` | `control` | #56696c | muted | borda de controle, curva do sino |
| `--text` | `text` | #d3e1e2 | foreground | texto |
| `--text-strong` | `textStrong` | #f4fbfb | bright_foreground | números, títulos |
| `--muted` | `muted` | #8fa3a6 | dark_foreground | labels, secundário |
| `--accent` | `accent` | #7cf0d4 | accent | foco, ativo, positivo |
| `--accent-subtle` | `accentSubtle` | #12302b | selection | fundo de seleção |
| `--signal` | `signal` | #ff8a6b | red | alerta: fora de 2σ, diff `-` |
| `--caution` | `caution` | #ffb454 | yellow | agente bloqueado |
| `--caution-subtle` | `cautionSubtle` | #33240f | — | fundo do bloco de permissão |
| `--data-1…4` | `data["data-1"]`… | #7cf0d4 #a8c5ff #ffb454 #c9a8ff | green blue yellow magenta | cor do rosto de cada agente |

Positivo usa accent e não existe verde separado. Negativo no P&L usa `signal`.

## Forma

- **Raio 0 em tudo.** O único círculo é o ponto (status de app, células dos rostos e do anel).
- Cartão de widget: `surface`, borda 1px `lineStrong`, padding 24 (20 no painel de agentes).
- Marca de canto: uma linha de 12×12 px no canto superior esquerdo, com 2px de `accent` em cima e à esquerda, posicionada em −1,−1 sobre a borda.
- Divisórias de 1px: `line` dentro do cartão e `lineStrong` sob cabeçalhos.
- Ativo e selecionado ganham um sublinhado de 2px em `accent`, com inset de 8 a 10px nas laterais.
- Espaço só em múltiplos da escala 4, 8, 12, 16, 24, 32, 48, 72 e 88.

## Tipo

- `Geist` (sans) para títulos grandes: peso 300, 28/34, tracking −0.01em.
- `Geist Mono` para o resto:
  - **Label** (`gs-label`): 11/16, caixa-alta, tracking 0.14em, cor `muted`, formato `0x01 · Quantfury`.
  - Número grande: 32/36 (patrimônio) e 40/44 (timer), tracking −0.02em, `textStrong`, `tnum`.
  - Corpo: 12–13/16.
  - Rodapé de figura: `FIG.02 — POSIÇÕES ABERTAS · QUANTFURY MCP`, 11/16, tracking 0.14em, `muted`.
- Na barra, siga a fonte da barra (`bar.fontFamily`, 12px).

## Componentes (equivalentes do GS.*)

| componente | altura | estilo |
|---|---|---|
| Button primary | 44 (sm 32) | fundo `accent`, texto `onAccent` |
| Button secondary | 44 (sm 32) | borda 1px `control`, texto `text` |
| Button ghost | 44 (sm 32) | sem borda; hover `inset` |
| Tag neutral | 20 | borda `lineStrong`, mono 11 caixa-alta, `muted` |
| Tag accent | 20 | borda `accent`, texto `accent` |
| Input mono | 44 | fundo `inset`, borda `control`; foco = borda `accent` + anel 2px |

Foco visível sempre com um anel de 2px `accent` e um respiro de 2px `bg`.

## Movimento

- Durações: 120 (hover), 200 (padrão, fade dos widgets) e 320 (abrir/recolher painel).
- Ease-out `cubic-bezier(0.2, 0, 0, 1)`. Em QML use `Easing.Bezier` com `easing.bezierCurve: tk.easeOut`.
- Loops: spinner 1.1s linear, pulso dos olhos 1.2s, piscar 4.5s. Todos desligam com `reduceMotion`.
