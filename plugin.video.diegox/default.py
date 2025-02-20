import xbmcplugin
import xbmcgui
import sys

# Obtener el handle del plugin
handle = int(sys.argv[1])
url_base = sys.argv[0]

def agregar_item(nombre, url, isFolder):
    """Función para agregar un ítem al menú"""
    item = xbmcgui.ListItem(label=nombre)
    xbmcplugin.addDirectoryItem(handle, url, item, isFolder)

def menu_principal():
    """Menú principal con categorías"""
    agregar_item("Películas", f"{url_base}?action=peliculas", True)
    agregar_item("Series", f"{url_base}?action=series", True)
    agregar_item("Favoritos", f"{url_base}?action=favoritos", True)
    xbmcplugin.endOfDirectory(handle)

def mostrar_peliculas():
    """Lista de películas"""
    agregar_item("Película 1", "plugin://plugin.video.miaddon/play?video_id=123", False)
    agregar_item("Película 2", "plugin://plugin.video.miaddon/play?video_id=456", False)
    xbmcplugin.endOfDirectory(handle)

def mostrar_series():
    """Lista de series"""
    agregar_item("Serie 1", "plugin://plugin.video.miaddon/play?video_id=789", False)
    agregar_item("Serie 2", "plugin://plugin.video.miaddon/play?video_id=101", False)
    xbmcplugin.endOfDirectory(handle)

def mostrar_favoritos():
    """Lista de favoritos"""
    agregar_item("Favorito 1", "plugin://plugin.video.miaddon/play?video_id=555", False)
    agregar_item("Favorito 2", "plugin://plugin.video.miaddon/play?video_id=666", False)
    xbmcplugin.endOfDirectory(handle)

# Obtener parámetros de la URL
import urllib.parse as urlparse
params = dict(urlparse.parse_qsl(sys.argv[2][1:]))

# Enrutamiento según la acción seleccionada
action = params.get("action")

if action is None:
    menu_principal()
elif action == "peliculas":
    mostrar_peliculas()
elif action == "series":
    mostrar_series()
elif action == "favoritos":
    mostrar_favoritos()