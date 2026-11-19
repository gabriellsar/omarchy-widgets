# 01 · Carteira (`gabriellsar.carteira`)

Escolha: **Invest B — Carteira**. Board: `ref/InvestCarteira.dc.html`; a composição final está em `ref/Desktop.dc.html` (seção "Carteira Quantfury"). Dados: `invest.json` (`docs/dados.md`).

## Estrutura (400px, padding 24, gap 16)

1. **Cabeçalho** (space-between):
   - Label `0x01 · Quantfury`.
   - Tag neutral `MCP · SYNC 14:32`. Quando a fonte é `file`, fica `MANUAL · 14:32`. A hora vem de `updated`. Clicar roda `gw invest`.
2. **Patrimônio** (gap 4):
   - Label `PATRIMÔNIO`.
   - Linha space-between, alinhada embaixo:
     - Valor: mono 32/36, `textStrong`, `tnum`, formato `$ 48.210,37` (pt-BR, símbolo de `currency`).
     - Variação: mono 12/16, `▲ +1,24% hoje` em `accent` ou `▼ −0,80% hoje` em `signal`. Com `dayChangeEstimated`, use o prefixo `~`.
3. **Tabela**: grid `96px | 1fr | 88px`, gap 12.
   - Cabeçalho: mono 11 caixa-alta, tracking 0.14em, `muted`, padding-bottom 8, borda inferior 1px `lineStrong`. Colunas: `ATIVO`, `HOJE VS 90D` e `P&L` alinhado à direita.
   - Linha: altura 44, borda inferior 1px `line`.
     - Ativo: ticker mono 13/16 `textStrong`, com o lado (`LONG`/`SHORT`) embaixo em mono 11/12, tracking 0.14em, `muted`.
     - Sino: SVG 72×24, detalhado abaixo. Quando `alert`, o texto `FORA DE 2σ` fica ao lado (mono 11, tracking 0.08em, `signal`, gap 8).
     - P&L: mono 13 `text`, `tnum`, à direita, formato `+$ 628,00`. Negativo ganha o sinal `−` e cor `signal`.
   - Ordem: os alertas primeiro, depois `|pnl|` decrescente. Máximo 5 linhas; o excedente vira `+2 posições`.
4. **Rodapé**: `FIG.02 — POSIÇÕES ABERTAS · QUANTFURY MCP`, mono 11/16, tracking 0.14em, `muted`.

## O sino (por linha)

Use `Shape`/`PathSvg` ou `Canvas`; o desenho é o mesmo do board:

- Base: linha em y 23.5, de 0 a 72, 1px `lineStrong`.
- Curva: normal padrão com z de −3.5 a 3.5 mapeado em x = (z+3.5)/7·72 e y = 24 − 20·e^(−z²/2), com 43 pontos, 1px `control`, sem preenchimento.
- Marcador: ponto r 3 em (x(z), y(z)), `textStrong`. Com `alert`, o ponto passa a `signal` e ganha um anel r 6 sem preenchimento, 1px `signal`.
- Clampe z em ±3.4 só para o desenho; o texto continua mostrando o valor real.
- Tooltip no sino: `hoje +6,1% · μ 0,15% · σ 2,5% · z 2,4 · 89 dias`.

## Vazio, erro e movimento

- Sem posições: uma linha só, `SEM POSIÇÕES ABERTAS`, em `muted`.
- Erro: conforme `00-desktop.md`. Se `error` começa com `MCPError`, a Tag diz `SEM MCP`.
- Movimento: os números trocam por crossfade de 120ms e não contam para cima. O ponto do sino desliza até a nova posição em 320ms ease-out.
