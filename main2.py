# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:10:32 2018

@author: tatar
"""

from imageloader_numpyarray import ImageLoader
import pickle
from testing import ImageLoader


with open('C:/Users/tatar/Desktop/Gandee/00_Project_Piotr/url_list.p', 'rb') as f:
    url_list = pickle.load(f)
url_list = url_list[100:110]

# Load class
crop = ImageLoader(224)
# Download images from urls and put in a numpy array:
numpy_array, url_list_new = crop.loadImages(url_list)
# Start swiping:
number_correct, number_all, target_array = crop.sort_images(numpy_array)
    









'''

url_list = ['https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/e/44/e44eec08-2c5d-11e8-bfc7-3b36abae01d3/5ab13a6d3230a.image.jpg','https://erc.europa.eu/sites/default/files/setup-your-team-img-hp.jpg']

img_numpy = loadImages(url_list, 224)

url_list2 = []
for i in range(100,120):
    url_list2.append(url_list[i])







'''
