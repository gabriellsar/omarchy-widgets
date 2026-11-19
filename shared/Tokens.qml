// GERADO a partir de shared/Tokens.qml por scripts/sync-shared.sh — edite lá, não aqui.
//
// Tokens do design system gabriel.s em QML. Uso dentro de um plugin:
//   import "common" as Gw
//   Gw.Tokens { id: tk }
//   color: tk.surface
//
// Regra: cores que existem no tema do Omarchy vêm de Commons.Color, para
// acompanhar `omarchy theme set`. As que o tema não tem (line, inset…) ficam
// fixas aqui com o valor do tema gabriel-s. Ao começar, leia
// $OMARCHY_PATH/shell/Commons/Color.qml e troque os fixos que tiverem par.
import QtQuick
import qs.Commons as Commons

QtObject {
  // superfícies
  readonly property color bg: Commons.Color.background          // #0a0c0d
  readonly property color surface: "#10181a"                     // colors.toml lighter_background
  readonly property color inset: "#0b1214"
  readonly property color line: "#1a2628"
  readonly property color lineStrong: "#263638"
  readonly property color control: "#56696c"                     // colors.toml muted
  readonly property color dot: "#1c2729"
  // texto
  readonly property color text: Commons.Color.foreground         // #d3e1e2
  readonly property color textStrong: "#f4fbfb"                  // bright_foreground
  readonly property color muted: "#8fa3a6"                       // dark_foreground
  // estado
  readonly property color accent: Commons.Color.accent           // #7cf0d4
  readonly property color onAccent: "#0a0c0d"
  readonly property color accentSubtle: "#12302b"                // selection
  readonly property color signal: "#ff8a6b"                      // red  — alerta, fora de 2σ
  readonly property color signalSubtle: "#3a1d16"
  readonly property color caution: "#ffb454"                     // yellow — bloqueado
  readonly property color cautionSubtle: "#33240f"
  // dados (rostos dos agentes)
  readonly property var data: ({ "data-1": "#7cf0d4", "data-2": "#a8c5ff", "data-3": "#ffb454", "data-4": "#c9a8ff", "data-5": "#8fa3a6" })

  // espaço (px): 4 8 12 16 24 32 48 72 88
  readonly property var space: [0, 4, 8, 12, 16, 24, 32, 48, 72, 88]
  readonly property int radius: 0          // sem cantos arredondados, nunca
  readonly property int hair: 1
  readonly property int mark: 2            // marca de canto e sublinhado ativo
  readonly property int cornerMark: 12
  readonly property int controlSm: 32
  readonly property int controlMd: 44

  // tipo
  readonly property string sans: "Geist"
  readonly property string mono: "Geist Mono"
  readonly property real labelTracking: 0.14   // em; labels mono 11px caixa-alta

  // movimento
  readonly property int durFast: 120
  readonly property int durBase: 200
  readonly property int durSlow: 320
  // ease-out cubic-bezier(0.2, 0, 0, 1)
  readonly property var easeOut: [0.2, 0, 0, 1, 1, 1]
}
