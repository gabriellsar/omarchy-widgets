# 02 · Pomodoro (`gabriellsar.pomodoro`)

Escolha: **Pomo A — Anel de pontos**. Board: `ref/PomoPontos.dc.html`; a composição final está em `ref/Desktop.dc.html` (seção "Pomodoro"). Config: `config.json → pomodoro, spotify`. Playlists: `spotify.json`. Faixa atual: MPRIS.

## Estrutura (400px, padding 24, gap 12)

1. **Cabeçalho**: label `0x02 · Foco` e uma Tag com a sessão.
   - No foco: Tag accent `SESSÃO 2/4`.
   - Na pausa: Tag neutral `PAUSA` ou `PAUSA LONGA`.
   - Parado: Tag neutral `PRONTO`.
2. **Anel** (176×176, centralizado):
   - Pontos em um círculo de raio 78 centrado em (88, 88), começando no topo (−90°) e girando no sentido horário.
   - Um ponto por minuto da fase: 25 no foco, 5 na pausa curta, 15 na longa.
   - Pontos passados: r 3 `accent`. Ponto atual: r 4 `textStrong`, com um anel r 7 de 1px `accent`. Pontos futuros: r 3 `lineStrong`.
   - Na pausa, os pontos passados usam `data-2` no lugar de `accent`.
   - No centro: o tempo restante `18:20` (mono 40/44, tracking −0.02em, `textStrong`, `tnum`) e, embaixo, `RESTANTE` (mono 11, tracking 0.14em, `muted`), gap 4.
   - Clique no anel: iniciar/pausar o timer. Clique-direito: pular a fase.
3. **Seletor de playlist**: botão de altura 44, padding 0 14, fundo `inset`, borda 1px `control`, gap 12, mono 12 com tracking 0.08em.
   - Conteúdo: ícone de nota 16px em `accent`, o nome com ellipsis e um chevron 16px em `muted`.
   - Abre uma lista logo abaixo, com a mesma largura, fundo `surface`, borda `lineStrong` e no máximo 6 linhas de 36px.
   - As favoritas vêm primeiro, separadas por uma linha `line`. Hover usa `inset`; a selecionada tem a borda esquerda de 2px em `accent`.
   - Escolher uma playlist roda `gw spotify ctl open <uri>` e salva a escolha em `pomodoro.json`.
   - Com uma faixa tocando, a segunda linha do botão mostra `artista — faixa`, vinda do MPRIS, em mono 11 `muted`.
4. **Controles** (centro, gap 12):
   - Botão ghost "faixa anterior", botão primary play/pausa e botão ghost "próxima". Os ícones são de 18px, stroke 1.5, linecap square, os mesmos paths do board.
   - O botão primary mostra pausa quando o MPRIS está `Playing` e play quando não está.
   - Ações: `gw spotify ctl prev|play-pause|next`.

## Timer

- O estado fica em `~/.local/state/gabriellsar-widgets/pomodoro.json`: `{phase, session, endsAt, pausedRemaining, playlistUri}`.
- O timer conta por `endsAt` (epoch ms) e não por ticks. Assim sobrevive a um reload do plugin e à suspensão.
- Fases: foco, depois pausa curta, e uma pausa longa a cada `sessions` focos.
- No fim de cada fase:
  - Mande uma notificação com `notify-send` (o shell de notificações do Omarchy pega).
  - Se `autoplay` estiver ligado, um foco que começa abre ou retoma a playlist.
  - Se `pause_on_break` estiver ligado, uma pausa que começa pausa o player.
- Sem Spotify aberto: os controles ficam com opacidade 0.4, e o tooltip diz `Abra o Spotify (Super+Shift+M)`.
