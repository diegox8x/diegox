import scrapy

class AnimeFLVSpider(scrapy.Spider):
    name = "animeflv"
    start_urls = ["https://www3.animeflv.net/" ]

    def parse(self, response):
        for anime in response.css(".ListAnimes .Item a::attr(href)").getall():
            anime_url = response.urljoin(anime)
            yield scrapy.Request(anime_url, callback=self.parse_anime)
    
    def parse_anime(self, response):
        title = response.css(".Ficha.fchlt h1::text").get()
        image = response.css(".Ficha.fchlt .Image img::attr(src)").get()
        
        episodes = []
        for episode in response.css(".ListCaps a"):  
            ep_number = episode.css("::text").get()
            ep_link = response.urljoin(episode.attrib["href"])
            episodes.append({"number": ep_number, "url": ep_link})
        
        yield {
            "title": title,
            "image": image,
            "episodes": episodes,
        }
