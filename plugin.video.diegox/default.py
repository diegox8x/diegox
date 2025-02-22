import sys
import xbmcplugin
import xbmcgui
import urllib.parse
import scraper  # Archivo donde haremos el scraping

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'videos')

BASE_URL = sys.argv[0]

def build_url(query):
    return BASE_URL + '?' + urllib.parse.urlencode(query)

def main_menu():
    add_directory("Lista de Videos", {"action": "list_videos"})
    xbmcplugin.endOfDirectory(addon_handle)

def list_videos():
    videos = scraper.get_videos()  # Obtenemos los videos desde scraper.py
    for video in videos:
        url = build_url({"action": "play", "url": video["url"]})
        list_item = xbmcgui.ListItem(video["title"])
        list_item.setArt({'thumb': video["thumbnail"]})
        list_item.setInfo('video', {'title': video["title"]})
        xbmcplugin.addDirectoryItem(addon_handle, url, list_item, False)
    xbmcplugin.endOfDirectory(addon_handle)

def play_video(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    if params:
        if params["action"] == "list_videos":
            list_videos()
        elif params["action"] == "play":
            play_video(params["url"])
    else:
        main_menu()

if __name__ == '__main__':
    router(sys.argv[2][1:])
