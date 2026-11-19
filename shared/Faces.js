// GERADO a partir de shared/Faces.js por scripts/sync-shared.sh — edite lá, não aqui.
// Rostos 7×7 dos agentes e ícones de estado. `.pragma library` = sem estado por instância.
.pragma library

// X = contorno, E = olho, . = vazio
var FACES = {
  bolha:   [".XXXXX.", "X.....X", "X.E.E.X", "X.....X", "X.XXX.X", "X.....X", ".XXXXX."],
  visor:   ["...X...", "XXXXXXX", "X.....X", "X.EEE.X", "X.....X", "X.....X", "XXXXXXX"],
  orelha:  ["X.....X", "XX...XX", "X.....X", "X.E.E.X", "X.....X", "X.X.X.X", ".XXXXX."],
  ciclope: [".XXXXX.", "X.....X", "X.EEE.X", "X.E.E.X", "X.EEE.X", "X.....X", ".XXXXX."]
}

// Rosto mini da barra (14×14): passo 2, raio 0.85, sempre data-1
var MINI = [".XXXXX.", "X.....X", "X.X.X.X", "X.....X", "X.XXX.X", "X.....X", ".XXXXX."]

// Grade de pontos: passo `step` px, ponto ligado r = 1.7*step/4, desligado r = 0.9*step/4
// (step 4 = chip 28px no trilho, step 6 = rosto grande, step 3 = lista).
function cells(face, step) {
  var rows = FACES[face] || FACES.bolha
  var out = []
  for (var y = 0; y < 7; y++)
    for (var x = 0; x < 7; x++) {
      var ch = rows[y].charAt(x)
      out.push({ x: x * step + step / 2, y: y * step + step / 2, on: ch !== ".", eye: ch === "E",
                 r: (ch !== "." ? 1.7 : 0.9) * step / 4 })
    }
  return out
}

// Ícones de estado (viewBox 24, stroke 2.25, linecap square)
var STATUS_ICON = {
  working: "M12 3a9 9 0 1 0 9 9",                            // gira 1.1s linear
  blocked: "M12 3L2 21h20zM12 10v5M12 18h.01",
  done:    "M5 12l5 5 9-10",
  idle:    "M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z",
  unknown: "M12 18h.01M9 9a3 3 0 1 1 4 2.8c-.6.3-1 .9-1 1.6V14"
}
// token de cor por estado (Tokens.qml)
var STATUS_COLOR = { working: "accent", blocked: "caution", done: "textStrong", idle: "muted", unknown: "muted" }
var STATUS_LABEL = { working: "Trabalhando", blocked: "Bloqueado", done: "Pronto", idle: "Ocioso", unknown: "—" }
// animação dos olhos: working pulsa 1.2s (1→0.2→1), idle pisca a cada 4.5s, done opacidade 0.4
var EYE = { working: "pulse", idle: "blink", done: "dim", blocked: "", unknown: "" }
