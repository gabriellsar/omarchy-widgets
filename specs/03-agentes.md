# 03 · Agentes (`gabriellsar.agentes`)

Escolha: **Agentes v2 B — painel duplo**, com os estados aberto e fechado. Boards:

- `ref/AgentesWidget.dc.html`: o componente, com props `side`/`collapsed` e toda a lógica de interação.
- `ref/AgentesRostos.dc.html`: os rostos e os estados.
- `ref/DesktopJanelasAgentes.dc.html`: o painel chamado por cima das janelas.

Dados em `herdr.json`; ações via `gw herdr act`. Rostos e ícones em `common/Faces.js`.

## Partes do plugin

- **service** `Agentes.qml`: lê `herdr.json`, guarda a seleção e o estado aberto/fechado em `agentes.json` no state dir e cria os PanelWindows.
- **bar-widget** `BarWidget.qml`: fica à esquerda do `omarchy.agents` na barra e chama o painel.

## Trilho (sempre visível, 76px de largura)

- Padding 16 0 20, coluna centralizada, gap 12. Do topo para baixo:
  - Botão ghost sm de abrir/recolher. O ícone é `M9 6l6 6-6 6M4 6v12` ou o espelhado, conforme o lado e o estado.
  - Divisória 24×1 `line`.
  - Um chip por agente.
  - Divisória.
  - Botão ghost sm `+` ("Novo agente"), que roda `herdr agent start` via `gw`. Se ainda não existir no `gw`, adicione e documente.
- **Chip**: botão 48×48 com o rosto em uma grade 7×7 de passo 4 (28×28).
  - Ponto ligado: r 1.7, na cor `tint` do agente. Ponto desligado: r 0.9, `lineStrong`.
  - Borda: 1px `accent` se selecionado e aberto, `caution` se bloqueado, `lineStrong` nos outros casos. Fundo `inset` quando selecionado.
  - Badge de estado no canto inferior direito, em (−5, −5): 18×18, fundo `surface`, borda `lineStrong`, ícone de 12px na cor do estado. O ícone de `working` gira.
  - Os olhos (`E`) animam conforme o estado: `working` pulsa, `idle` pisca e `done` fica com opacidade 0.4.
- Com o widget à direita da tela, o trilho fica do lado direito (`row-reverse`) e a borda interna dele é 1px `line`.

## Painel aberto (580px no total; conteúdo com padding 20 e gap 16)

1. **Cabeçalho**:
   - Label `0x03 · Agentes`, com `· herdr` em `control`.
   - À direita, o estado do selecionado: ícone de 16px mais o rótulo em caixa-alta (`TRABALHANDO`, `BLOQUEADO`, `PRONTO`, `OCIOSO`), na cor do estado.
2. **Identidade**:
   - O `label` em Geist 300, 28/34, `textStrong`.
   - Embaixo, `cwd · agent` em mono 11, `muted`.
3. **Log**: bloco `inset` com padding 12 14, mono 12/18, com as últimas 4 linhas de `log`.
   - Cada linha começa com `│ ` em `control` e usa ellipsis.
4. **Permissão** (só com `blocked`): borda 1px `caution`, fundo `cautionSubtle`, padding 16, gap 12.
   - Topo: `PERMISSÃO · {tool}` (mono 11 caixa-alta, `caution`) e, à direita, `{file}` (mono 13, `textStrong`).
   - Diff: bloco `inset` com padding 8 12 e mono 12/20. O sinal `+` fica em `accent` e o `-` em `signal`, com o texto em `text`.
     - Se `tool`, `file` e `diff` vierem vazios, mostre `prompt.lines` cru.
   - Três botões em grid: primary `1 Sim`, secondary `2 Sempre` e ghost `3 Não`, que chamam `approve`, `always` e `deny`.
     - As teclas 1, 2 e 3 também funcionam quando o painel tem foco.
5. **Mensagem** (todo estado, menos `blocked`): Input mono mais o botão primary `Enviar`, que chama `send`.
   - Placeholder: `Mensagem para a fila…` no `working` e `Próxima tarefa…` nos outros.
   - Enter envia. Vazio não envia.
6. **Ações** (grid de 4, gap 4, padding-top 12, borda superior `line`), todas ghost sm:
   - `Esc Parar` → `stop`
   - `⇧⇥ Modo` → `mode`
   - `/compact` → `compact`
   - `Abrir pane` → `focus` + focar ou abrir a janela do herdr

## Fechado (78px)

Só o trilho. Um clique em qualquer chip abre o painel com esse agente selecionado.

## Botão na barra

- Altura 26, padding 0 8, gap 6, fonte da barra.
- Conteúdo: o rosto mini 14×14 (`Faces.MINI`, passo 2, r 0.85, `data-1`), o total de agentes e, se houver bloqueados, um ⚠ de 11px seguido do número, em `caution`.
- Sublinhado de 2px `accent` enquanto o painel chamado estiver aberto.
- `aria`/tooltip: `Agentes: 4, 1 bloqueado`.
- Com o herdr desligado, o número vira `—` e o tooltip diz `herdr não está rodando`.

## Chamado pela barra (com janelas abertas)

- O painel aparece **aberto**, em top 32 e right 10 (abaixo da barra, no gaps_out). A layer é `Top` e o teclado fica `OnDemand`.
- Um scrim transparente cobre o resto da tela, abaixo da barra: clicar nele fecha. Esc com o input vazio também fecha.
- Entra com fade e um slide de 8px para baixo, em 200ms ease-out. Sai com fade em 120ms.
- Um agente que passa a `blocked` **não** abre o painel sozinho: só atualiza o badge da barra.

## Vazio

- `running: false`: o trilho mostra um único chip vazio, só com pontos `lineStrong`, e o painel diz `herdr parado · Super+Ctrl+Enter`.
- Lista vazia: `Nenhum agente · + para começar`.
