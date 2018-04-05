# import scrapy
# from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
import json

import ImageLoader as il

'''
Known Error: For some URLs I'm running into errors dues to japanese, chinese sign... gotta fix that
                error occured for 'car+red'
'''

class GoogleScraper:

    def __init__(self, dim, start_url):

        self.start_url = start_url

        self.url_frontier = []
        self.url_history = []
        self.img_urls_history = []

        self.image_loader = il.ImageLoader(dim)

        # header object, necessary to get proper response when requesting urls
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def parseNextURL(self):
        if len(self.url_frontier) == 0 and self.start_url != '':
            img_urls = self.getImgURLS(self.start_url)
        elif len(self.url_frontier) > 0:
            query_url = self.constructQuery(self.url_frontier.pop(0)[0])
            img_urls = self.getImgURLS(query_url)
        else:
            return None
        return img_urls

    def appendURLFrontier(self, urls, keys):
        self.url_frontier = self.url_frontier + [[urls[i], keys[i]] for i in range(len(urls))]
        self.sortURLFrontier()

    def sortURLFrontier(self):
        self.url_frontier = sorted(self.url_frontier, key=lambda tup: tup[1], reverse=True)

    def getImgURLS(self, URL):
        img_urls = []
        try:
            # getting google search and parsing HTML to BeautifulSoup
            response = requests.get(URL, headers=self.header)
            soup = BeautifulSoup(response.content)

            # Extracting all image URLs
            original_tag_list = soup.findAll("div", {"class": "rg_meta notranslate"})
            img_urls = [json.loads(tag.text)['ou'] for tag in original_tag_list]

        except Exception as e:
            print(e)
        return img_urls

    def constructQuery(self, img_url):
        current_response = requests.get('https://www.google.com/searchbyimage?image_url=' +
                                        img_url, headers=self.header)
        current_soup = BeautifulSoup(current_response.content)
        link_to_visual_neighbours = 'https://www.google.com' + \
                                    current_soup.find('a', {"class": "iu-card-header"})['href']
        return link_to_visual_neighbours
