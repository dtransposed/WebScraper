import Scraper


query = 'car'

spider = Scraper.GoogleScraper(query=query)
spider.startCrawling()
