''' Code for loading images from URLS
Classes: ImageLoader, ImageRanker
'''

import numpy as np

class ImageLoader:

    def __init__(self):
        '''
        set some necessary attributes here if needed
        '''
        self.image_ranker = ImageRanker() #fill with necessary arguments
        pass

    def rankImages(self, URL_list):
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

    def loadImages(self, URL_list):
        '''
        :param URL_list:
        :return imgs: numpy array of images
        '''

        imgs = np.zeros([1])
        return imgs

    def preprocessImage(self, img):
        '''
        :param img: some image
        :return prep_img: preprocessed image
        '''

        prep_img = None
        return prep_img


class ImageRanker:

    def __init__(self):
        '''
        set some necessary attributes here if needed
        like initializing the a neural network (self.neural_net)
        '''
        pass

    def rankImage(self, img):
        '''
        :param img: image of dim...
        :return: score in [0,1]
        '''

        img_score = 0
        return img_score

    def train(self, loss, **kwargs):
        '''
        :param loss: with respect to user input
        :param kwargs: some keyword arguments, such as: learning rate,...
        :return:
        '''

        return None