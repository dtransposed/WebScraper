from download_image import imageloader

import urllib.request as ur
import os
import re
import requests
from bs4 import BeautifulSoup
import cv2

x = imageloader()

# Create a list with url from one site (google.com/images). Args: (query, number of urls)

list_urls = x.get_img_urls("car", 30)

# Download the images found above Arg:(list with urls)
####### AT THIS POINT WE NEED "DOWNLOADER.py" ##############
x.download(list_urls)

# Sort images after downloading them (needs user input, press "a" correct, "b" incorrect)
list_classes = ['correct', 'wrong']
path = os.getcwd()

number_correct, number_all = x.sorting_images(list_classes, path)

# Print score

score = x.score(number_correct, number_all)



