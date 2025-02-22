import requests
from bs4 import BeautifulSoup

def get_videos():
    url = "https://www3.animeflv.net/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    video_elements = soup.find_all("div", class_="video-item")

    videos = []
    for video in video_elements:
        title = video.find("h2").text
        thumbnail = video.find("img")["src"]
        video_url = video.find("a")["href"]

        videos.append({"title": title, "thumbnail": thumbnail, "url": video_url})

    return videos