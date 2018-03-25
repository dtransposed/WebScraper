import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
import json

import ImageLoader as IL

############# Insert Query Here: spaces should be + signs (i guess) ############
query = 'car'
################################################################################
'''
Known Error: For some URLs I'm running into errors dues to japanese, chinese sign... gotta fix that
                error occured for 'car+red'
'''

class Scraper(scrapy.Spider):
    name = "GandeeScraper"
    start_urls = [
        "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % query
    ]

    def __init__(self, query=''):
        # To-Do´: parse query as argument to constructor
        super(Scraper, self).__init__()
        self.process = CrawlerProcess()     # for running as a process
        self.url_frontier = []
        self.url_history = []
        self.img_urls_history = []
        self.image_loader = IL.ImageLoader()    # Image loader object which holds the functionality of downloading a classification
        # header object, necessary to get proper response when requesting urls
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def parse(self, response):
        img_urls = []
        try:
            # getting google search and parsing HTML to BeautifulSoup
            response = requests.get(response.url, headers=self.header)
            soup = BeautifulSoup(response.content)

            # Extracting all image URLs
            original_tag_list = soup.findAll("div", {"class": "rg_meta notranslate"})
            img_urls = [json.loads(tag.text)['ou'] for tag in original_tag_list]

        except Exception as e:
            print(e)

        ############### CALLING IMAGE RANKER ###############################
        self.image_loader.rankImages(img_urls)
        ####################################################################

        # Appending current Image URLs to history
        self.img_urls_history = self.img_urls_history + img_urls
        if len(img_urls) > 0:
            try:

                # To-Do: run similar image URL extraction as subprocess since it is very slow
                # extracting similar image URL via image search with first image url
                self.url_frontier = self.url_frontier + img_urls.copy()
                img_url = self.url_frontier.pop(0)
                current_response = requests.get('https://www.google.com/searchbyimage?image_url=' +
                                                     img_url, headers=self.header)
                current_soup = BeautifulSoup(current_response.content)
                link_to_visual_neighbours = 'https://www.google.com' + current_soup.find('a', {"class": "iu-card-header"})['href']

                # recursively calling self.parse again to scrape the first similar image search result
                yield scrapy.Request(link_to_visual_neighbours, self.parse)
            except Exception as e:
                print(e)
        else:
            return None

    def startCrawling(self):
        self.process.crawl(Scraper)
        self.process.start()

    def sortURLFrontier(self):
        pass


s = Scraper()

s.startCrawling()
