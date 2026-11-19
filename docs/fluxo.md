# Fluxo de trabalho com os agentes

## Uma vez

```bash
git clone git@github.com:gabriellsar/omarchy-widgets.git ~/omarchy-widgets
cd ~/omarchy-widgets
scripts/install.sh          # gw no PATH, config local, units do systemd --user
gw fixtures                 # dados de exemplo, para começar sem credenciais
```

## Um agente por widget, cada um no seu worktree

Os widgets não dividem arquivos, só `shared/`. Por isso dá para rodar até 3 agentes em paralelo sem conflito.

```bash
git worktree add ../ow-carteira -b widget/carteira
git worktree add ../ow-pomodoro -b widget/pomodoro
git worktree add ../ow-agentes  -b widget/agentes
```

No herdr (Super+Ctrl+Enter), abra um workspace por worktree e rode `claude` em cada um, com o prompt correspondente de `PROMPTS.md`. A barra do herdr mostra quem está trabalhando, quem está bloqueado e quem terminou.

### Ligar o plugin certo

`scripts/link-plugins.sh` liga a pasta do worktree em que você rodou. Então o plugin ativo é o do último worktree que chamou o script.

- Para testar a carteira: `cd ../ow-carteira && scripts/link-plugins.sh gabriellsar.carteira --enable`.
- Ao terminar, volte o link para `~/omarchy-widgets`.

## Ordem sugerida

1. **Pomodoro**: o mais simples. Ele valida `Tokens.qml`, `DesktopState.qml` e o padrão de `PanelWindow`, que os outros reaproveitam.
2. **Carteira**, em paralelo com o 3.
3. **Agentes**: o maior. Tem service, bar-widget e o painel chamado pela barra.
4. **Dock**: clone e reestilo.
5. **Fundo** (opcional).

Se um agente melhorar algo em `shared/`, isso entra num PR próprio antes, para os outros fazerem rebase.

## Revisão antes do merge

- `omarchy plugin validate plugins/<id>` sem erro.
- Screenshot do widget com `gw fixtures` lado a lado com o board de `specs/ref/`. As medidas do spec batem ±1px.
- Os três estados: carregando (apague o JSON), erro (`error` preenchido) e vazio.
- Abra e feche uma janela: o fade funciona e o widget não fica clicável escondido.
- `omarchy theme set` para outro tema e de volta: nada quebra. As cores fixas de `Tokens.qml` são aceitas.
- Commit sem atribuição a IA (`CLAUDE.md`).

## Se algo der errado

- O shell travou: `omarchy-restart-shell`.
- Um plugin está quebrando o shell: `omarchy plugin disable <id>`.
- Desfazer tudo: `scripts/uninstall.sh`, depois `rm ~/.config/omarchy/plugins/gabriellsar.*` (são só symlinks).
