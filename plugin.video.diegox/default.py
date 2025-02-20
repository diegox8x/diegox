import xbmcplugin
import xbmcgui
import sys

# Obtiene el handle del plugin
handle = int(sys.argv[1])

# Crea una lista de elementos para el menú
def show_menu():
    url = "plugin://plugin.video.diegox/play"
    list_item = xbmcgui.ListItem(label="Reproducir Video")
    xbmcplugin.addDirectoryItem(handle, url, list_item, isFolder=False)

    xbmcplugin.endOfDirectory(handle)

# Ejecuta la función
show_menu()