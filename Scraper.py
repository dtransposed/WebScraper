import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pickle

import ImageLoader as IL

query = 'car'

class Scraper(scrapy.Spider):
    name = "GandeeScraper"
    start_urls = [
        "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % query
    ]

    def __init__(self):
        super(Scraper, self).__init__()
        self.process = CrawlerProcess()
        self.url_frontier = []
        self.visited_urls = []
        self.link_extractor = LinkExtractor()
        self.image_loader = IL.ImageLoader()

    def parse(self, response):

        driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS('phantomjs')
        driver.get(response.url)
        all_urls = []
        try:
            for i in range(0, 5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
                # imgs_container = driver.find_element_by_id('search')
                # imgs = imgs_container.find_elements_by_tag_name('img')
                # driver.save_screenshot('out'+str(i)+'.png')
            # html = driver.page_source
            # soup = BeautifulSoup(html)
            # pret = soup.prettify()
            driver.find_element_by_id('smb').click()
            for i in range(0, 4):
                time.sleep(1.5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            pass

        further_searches = []
        imgs_container = driver.find_element_by_id('search')
        imgs = imgs_container.find_elements_by_tag_name('img')
        for img in imgs:
            try:
                img.click()
                time.sleep(0.5)
                similar_imgs_container = driver.find_element_by_id('irc_bg')
                sim_imgs = similar_imgs_container.find_elements_by_tag_name('img')
                img_url_list = []
            except:
                pass
            for im in sim_imgs:
                try:
                    new_search_url = ''
                    average_size = (im.size['height'] + im.size['width']) / 2
                    if average_size > 50 and average_size < 200:
                        parent = im.find_element_by_xpath('..')
                        pt = parent.tag_name
                        phref = parent.get_attribute('href')
                        if parent.tag_name == 'a' and parent.get_attribute('href').startswith('https://www.google.de/imgres?'):
                            time.sleep(0.1)
                            im.click()
                            current_img = imgs_container.find_element_by_xpath('//*[@id="irc_cc"]/div[2]/div[1]/div[2]/div[2]/a/img')
                            img_url_list.append(current_img.get_attribute('src'))
                            pickle.dump(all_urls, open('url_list.p', 'wb'))
                        elif parent.tag_name == 'a' and parent.get_attribute('href').startswith('https://www.google.de/search?'):
                            new_search_url = parent.get_attribute('href')
                except:
                    pass

            self.image_loader.rankImages(img_url_list)
            all_urls = all_urls + img_url_list
            if new_search_url != '': further_searches.append(new_search_url)
            print(len(all_urls))
            # if len(all_urls) >= 1000:
            #     pickle.dump(all_urls, open('url_list.p','wb'))
            #     break

        # soup = BeautifulSoup(driver.page_source)
        # return soup

        # print(soup.prettify())
        #
        # imgs = soup.find_all('img')
        # img_urls = [img['src'] for img in imgs]
        #
        # print(len(img_urls))
        #
        # self.visited_urls.append(response.url)
        #
        # links = self.link_extractor.extract_links(response)
        #
        # # for link in links:
        # #     print(link.url)

    def startCrawling(self):
        self.process.crawl(Scraper)
        self.process.start()

    def scrapeSearchEngine(self, URL):
        if 'google' in URL: soup = SSET.getGoogleFullHTML(URL)
        return soup

s = Scraper()

s.startCrawling()
