
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
       
def loadImages(url_list, dim = 224):
    
    dim_tuple = (dim, dim, 3, 1)
    numpy_array = np.zeros(dim_tuple).astype(int)
    extension = 'jpg'
    i = 0
    for url in url_list:
        i =+ 1
        file_name = (uuid.uuid4().hex) + str(i) + "." + extension 
        ur.urlretrieve(url, file_name)
        #image = ur.urlretrieve(url, file_name) # we need a proper downloader
        image = preprocessImage(file_name, dim) # Preprocessing (currently cropping), image is a file
        image = np.expand_dims(image, 3)
        if numpy_array[0][0][0][0] == 0:    
            numpy_array = np.add(numpy_array, image)
        else:
            numpy_array = np.concatenate((numpy_array, image), axis = 3)
            
    return numpy_array  

##############################################################################
        
def preprocessImage(img, dim = 224):

    # Load image and get dimensions
    prep_img = cv2.imread(img)
    height, width, channels = prep_img.shape
    print(height, width)
    
    # If dimensions are odd, make even
    if height % 2 == 1:
        prep_img = prep_img[0:height-1, 0:width]
    if width % 2 == 1:
        prep_img = prep_img[0:height, 0:width-1]
        
    # Crop to square
    if height > width:
        crop_stripe = int((height-width)/2)
        prep_img = prep_img[crop_stripe:height-crop_stripe, 0:width]
        prep_img = cv2.resize(prep_img, (dim,dim), interpolation = cv2.INTER_AREA)
    if height < width:
        crop_stripe = int((width-height)/2)
        prep_img = prep_img[0:height, crop_stripe:width-crop_stripe]
        prep_img = cv2.resize(prep_img, (dim,dim), interpolation = cv2.INTER_AREA)
    if height == width:
        prep_img = cv2.resize(prep_img, (dim,dim), interpolation = cv2.INTER_AREA)
    name = str(img)
    cv2.imwrite(name, prep_img)
     
    return prep_img
##############################################################################

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
