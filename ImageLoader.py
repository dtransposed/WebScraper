# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:32:35 2018

@author: tatar
"""

import numpy as np
import cv2
import os
import urllib.request as ur
import uuid
from matplotlib import pyplot as plt
import pickle
import shutil


class ImageLoader:

    def __init__(self, dim):
        '''
        set some necessary attributes here if needed
        '''
        # self.image_ranker = ImageRanker() #fill with necessary arguments
        self.dim = dim  # dimension of an image

        pass

    def rankImages(self):
        '''
        :param URL_list:
        :return score:
        '''
        '''
        for every url in list
            load image
            preprocess image
            get score from ImageRanker
            get feedback from crowd
            if good image:
                store
                number of good images +1
            else:
                delete
            train ImageRanker
        '''

        imgs_score = 0
        return imgs_score

    #############################################################################

    def loadImages(self, url_list):
        dim = self.dim
        url_list = [url for url in url_list if url != None]
        dim_tuple = (dim, dim, 3, 1)
        numpy_array = np.zeros(dim_tuple).astype(int)
        ii = 0
        url_list_copy = url_list.copy()
        for url in url_list_copy:
            ii += 1
            print("Numpy array size: ", numpy_array.shape)
            try:
                resp = ur.urlopen(url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                # image = ur.urlretrieve(url, file_name) # we need a proper downloader
                image = self.preprocessImage(image)  # Preprocessing (currently cropping), image is a file
                image = np.expand_dims(image, 3)
                # if numpy_array[0][0][0][0] == 0:
                if ii == 1:
                    numpy_array = np.add(numpy_array, image)
                else:
                    numpy_array = np.concatenate((numpy_array, image), axis=3)
                print("Downloaded %s" % (url))
            except Exception as e:
                url_list.remove(url)
        numpy_array = np.rollaxis(numpy_array, 3)
        return numpy_array.astype("uint8"), url_list

    ##############################################################################

    def preprocessImage(self, prep_img):
        dim = self.dim
        # Load image and get dimensions
        # prep_img = cv2.imread(img)
        height, width, channels = prep_img.shape
        print(height, width)

        # If dimensions are odd, make even
        if height % 2 == 1:
            prep_img = prep_img[0:height - 1, 0:width]
        if width % 2 == 1:
            prep_img = prep_img[0:height, 0:width - 1]

        # Crop to square
        if height > width:
            crop_stripe = int((height - width) / 2)
            prep_img = prep_img[crop_stripe:height - crop_stripe, 0:width]
            prep_img = cv2.resize(prep_img, (dim, dim), interpolation=cv2.INTER_AREA)
        if height < width:
            crop_stripe = int((width - height) / 2)
            prep_img = prep_img[0:height, crop_stripe:width - crop_stripe]
            prep_img = cv2.resize(prep_img, (dim, dim), interpolation=cv2.INTER_AREA)
        if height == width:
            prep_img = cv2.resize(prep_img, (dim, dim), interpolation=cv2.INTER_AREA)

        return prep_img

    ##############################################################################

    def sort_images(self, numpy_array):
        # Create folder for cleaned images
        if os.path.isdir("clean_pics") == False:
            os.makedirs("clean_pics")
        if os.path.isdir("garbage_pics") == False:
            os.makedirs("garbage_pics")

        # List with clean pictures - for a score
        foto_list_correct = []
        numpy_array = numpy_array.astype("uint8")
        target_array = np.array([]).astype("uint8")
        for i in range(numpy_array.shape[0]):
            # Load one image from numpy array
            img = numpy_array[i, :, :, :]
            # Object for infinite loop
            endProgram = False
            cv2.imshow('Image', img)
            # Image name using hash function
            file_name = (uuid.uuid4().hex) + ".jpg"

            # sorting into folders
            while not endProgram:
                ############ CORRECT: PRESS "A"  ####################
                if cv2.waitKey(33) == ord('a'):
                    print("Moved to Class a")
                    cv2.destroyAllWindows()
                    new_path = "clean_pics/" + str(file_name)
                    foto_list_correct.append(img)
                    # Add 1 to target array for neural network
                    target_array = np.append(target_array, 1).astype("uint8")
                    # Save file to a folder
                    cv2.imwrite(new_path, img)
                    endProgram = True

                ############ INCORRECT: PRESS "B"  ####################
                if cv2.waitKey(33) == ord('b'):
                    print("Moved to Class b")
                    cv2.destroyAllWindows()
                    new_path = "garbage_pics/" + str(file_name)
                    # Add 0 to target array for neural network
                    target_array = np.append(target_array, 0).astype("uint8")
                    # Save file to a folder
                    cv2.imwrite(new_path, img)
                    endProgram = True

        print("sorting done!")
        number_all = numpy_array.shape[0]
        number_correct = len(foto_list_correct)
        return number_correct, number_all, target_array

    ######################################################################

    def score(number_correct, number_all):
        score = 100 * (number_correct / number_all)
        return "In your folder {} % of images were correct.".format(score)

######################################################################