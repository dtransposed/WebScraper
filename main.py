import Scraper


# query = 'car'
#
# spider = Scraper.GoogleScraper(query=query)
# spider.startCrawling()

query = 'car'

scraper = Scraper.GoogleScraper(query)

imgs_generator = scraper.start()

for im in imgs_generator:
    print(im)