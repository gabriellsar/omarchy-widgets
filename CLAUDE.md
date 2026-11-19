# omarchy-widgets — regras para agentes

Widgets do desktop do Gabriel no **Omarchy 4 "Quattro"** (Arch + Hyprland), feitos como plugins do `omarchy-shell` (Quickshell/QML). O design já está fechado: você implementa, não redesenha.

## Antes de escrever código

1. Leia `docs/quattro.md`, `docs/design-system.md` e o spec do seu widget em `specs/`.
2. Leia o código do Omarchy **instalado na máquina**, que vale mais que qualquer doc:
   - `$OMARCHY_PATH/shell/plugins/` (padrão `/usr/share/omarchy`): `dock/`, `agents/`, `background/` e `bar/README.md`.
   - `$OMARCHY_PATH/shell/Commons/` (`Color.qml`, `Style.qml`) e `$OMARCHY_PATH/docs/omarchy-shell.md`. Se `docs/` não estiver instalado, use o branch `quattro` de github.com/omacom/omarchy.
3. Se a skill `omarchy` estiver disponível, carregue-a. Leia também `agents/skills/shell-dev.md`, `visual-verification.md` e `motion.md` do repositório do Omarchy.
4. Comece em plan mode e mostre o plano antes de editar.

## Regras fixas

- **Não edite nada em `$OMARCHY_PATH`.** Para mudar um built-in, use `omarchy plugin clone omarchy.<x>`.
- IDs seguem `gabriellsar.<nome>`. A exceção é a dock, que fica com o id gerado pelo clone.
- O validador recusa symlink dentro de um plugin. O código compartilhado vive em `shared/` e `scripts/sync-shared.sh` copia para `plugins/<id>/common/`. Edite sempre em `shared/`.
- Os dados vêm de `~/.local/state/gabriellsar-widgets/*.json`, escritos pelo `gw` (veja `docs/dados.md`). O QML **só lê** esses arquivos com `FileView { watchChanges: true }` e age chamando `gw … ` com `Process`.
  - Nada de rede, credencial ou parsing de TOML no QML.
  - Se faltar um dado, mude o `gw` e o contrato em `docs/dados.md` no mesmo commit.
- Para desenvolver sem credenciais, rode `gw fixtures`: grava os dados de exemplo dos boards.
- Cores, espaço, tipo e movimento vêm de `Tokens.qml`. Hex solto no QML não passa.
- Visual: zero cantos arredondados, linhas de 1px, marca de canto 12px/2px em accent, labels mono 11px caixa-alta com tracking 0.14em, números com `font.features: { "tnum": 1 }`.
- Respeite `Style.reduceMotion`: com ele ligado, nenhuma animação em loop.
- Segredos não entram no repo. `config.toml`, `secrets.env` e `positions.toml` ficam só em `~/.config/gabriellsar-widgets/`.

## Testar

```bash
scripts/link-plugins.sh gabriellsar.<nome> --enable   # liga e valida
omarchy plugin validate plugins/gabriellsar.<nome>
journalctl --user -f -t omarchy-shell                 # ou o log que shell-dev.md indicar
omarchy-restart-shell                                 # se o shell travar
python3 -m unittest discover tests                    # se mexer no gw
```

Salvar um arquivo em `~/.config/omarchy/plugins/` recarrega o plugin sozinho. Faça a verificação visual como `visual-verification.md` manda, com screenshot comparado ao board em `specs/ref/`.

## Git

- Commits pequenos, em português, no formato `feat(pomodoro): …`.
- **Sem atribuição a IA em commit ou PR.** Nada de linha `Co-Authored-By` de Claude, link de sessão ou rodapé "Generated with". Isso vale para todos os repositórios do Gabriel.
- Autor: `GABRIEL LOBO DE SANT ANNA ROSAS <gabrielsrosas@gmail.com>`.
- Um branch por widget (`widget/<nome>`) e PR para `main`.
