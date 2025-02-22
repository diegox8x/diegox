import xbmcaddon
import xbmcplugin
import xbmcgui
import sys

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'videos')

xbmcgui.Dialog().ok("Mi Addon", "¡Hola desde Kodi!"