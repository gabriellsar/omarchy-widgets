# Boards de referência

Estes arquivos são o código-fonte dos boards do canvas "Omarchy Desktop — Widgets". Não abrem soltos no navegador, porque dependem do runtime do canvas. Leia-os como HTML: o markup tem as medidas e os estilos exatos; o `<script>` no fim (`renderVals`) tem a lógica, as listas e as fórmulas. `{{x}}` é um valor que vem do script, `sc-for` é um loop, `sc-if` é uma condição e `x-import GS.*` é um componente do design system (veja `docs/design-system.md`).

`tokens.css` traz os tokens do design system gabriel.s (escuro primeiro, claro depois).

O anel e a linha laranja do "PICO" em `Desktop.dc.html` **não** entram em nada: foram removidos de propósito.
