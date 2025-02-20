import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc

# Identificación del addon
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'videos')

# Crear menú de opciones
def build_menu():
    url = sys.argv[0] + "?action=play"
    li = xbmcgui.ListItem("Reproducir Video de Prueba")
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

# Procesar acciones
def router(paramstring):
    if "action=play" in paramstring:
        play_video()
    else:
        build_menu()

# Función para reproducir un video
def play_video():
    url = "https://www.example.com/video.mp4"  # URL de prueba
    li = xbmcgui.ListItem("Video de prueba")
    li.setInfo('video', {'title': 'Video de prueba'})
    li.setPath(url)
    xbmc.Player().play(url, li)

# Ejecutar router
if __name__ == '__main__':
    router(sys.argv[2])
