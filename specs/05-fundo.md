# 05 · Fundo (opcional, por último)

Hoje o fundo é a imagem estática `backgrounds/1-heightmap.png` do tema `gabriel-s` (repo dotfiles). Ela é gerada por `.tools/wallpaper/heightmap.py` e o `omarchy.background` já a mostra. **Não há nada a fazer aqui para o desktop funcionar.**

## Se for animar

O board `ref/Desktop.dc.html` tem a versão animada:

- Grade de pontos com passo 28, linhas alternadas deslocadas meio passo.
- Campo de altura com três senoides, de semente 42, e 7 níveis.
- Os pontos perto de uma curva de nível ficam com opacidade 0.55; os outros, 0.09.
- Uma onda de 12s percorre os níveis.

Regras:

- **Sem o ponto laranja.** O anel `signal`, a linha e o rótulo "PICO" do board saem: foi pedido explicitamente.
- Faça como shader (`ShaderEffect` com um `.frag` compilado por `qsb`) num clone de `omarchy.background`, nunca como milhares de itens QML.
- Pause quando houver janela, com `DesktopState`, e também com `reduceMotion`. O motor OWE do original já pausa quando nada está visível; aproveite isso.
- O consumo de GPU parado deve ficar perto de zero. Meça antes de abrir o PR.
