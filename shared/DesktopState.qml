// GERADO a partir de shared/DesktopState.qml por scripts/sync-shared.sh — edite lá, não aqui.
//
// A regra do desktop: os widgets só aparecem quando o workspace ativo do
// monitor está vazio. Abriu uma janela, tudo some (fade durBase). A exceção é
// o painel de agentes chamado pelo botão da barra, que fica por cima.
//
// Uso: Gw.DesktopState { id: desk; screen: window.screen }  ->  desk.empty
// Confira os nomes contra o Quickshell instalado (Quickshell.Hyprland):
// HyprlandMonitor.activeWorkspace, HyprlandWorkspace.toplevels, hasFullscreen.
import QtQuick
import Quickshell
import Quickshell.Hyprland

QtObject {
  property var screen: null
  readonly property var monitor: screen ? Hyprland.monitorFor(screen) : Hyprland.focusedMonitor
  readonly property var workspace: monitor ? monitor.activeWorkspace : null
  // janelas reais: ignora as que não têm appId e os popups (parent)
  readonly property int windowCount: {
    if (!workspace || !workspace.toplevels) return 0
    var n = 0, list = workspace.toplevels.values
    for (var i = 0; i < list.length; i++) {
      var w = list[i].wayland
      if (w && w.appId && !w.parent) n++
    }
    return n
  }
  readonly property bool fullscreen: !!workspace && workspace.hasFullscreen === true
  readonly property bool empty: windowCount === 0 && !fullscreen
}
