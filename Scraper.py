import scrapy
from scrapy.crawler import CrawlerProcess

class Scraper(scrapy.Spider):
    name = "GandeeScraper"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

process = CrawlerProcess()

process.crawl(Scraper)

process.start()