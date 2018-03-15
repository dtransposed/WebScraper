import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

import LinkRanker as LR
# import ImageLoader

query = 'hi'

class Scraper(scrapy.Spider):
    name = "GandeeScraper"
    start_urls = [
        'http://www.bing.com/images/search?q=' + query
    ]

    def __init__(self):
        super(Scraper, self).__init__()
        self.process = CrawlerProcess()
        self.url_frontier = []
        self.visited_urls = []
        self.link_extractor = LinkExtractor()

    def parse(self, response):
        soup = BeautifulSoup(response.body)

        imgs = soup.find_all('img')
        img_urls = [img['src'] for img in imgs]

        print(img_urls)

        self.visited_urls.append(response.url)

        links = self.link_extractor.extract_links(response)

        for link in links:
            print(link.url)

    def startCrawling(self):
        self.process.crawl(Scraper)
        self.process.start()


s = Scraper()

s.startCrawling()
