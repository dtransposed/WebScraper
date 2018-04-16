import Scraper
import ImageLoader as il
import ImageRankerNN as ir
import numpy as np

query = 'sonniges wetter'
dim = 224

start_url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch" % query
scraper = Scraper.GoogleScraper(224, start_url)

image_loader = il.ImageLoader(dim=dim)
# image_ranker = ir.Ranker_NN(1, 1000, 500)
# our_model = image_ranker.convolutional_neural_network()

while True:
    img_urls = scraper.parseNextURL()
    imgs, urls = image_loader.loadImages(img_urls)
    number_correct, number_all, target_array = image_loader.sort_images(imgs)
    scraper.appendURLFrontier(urls, target_array)
