import numpy as np
import cv2
import os
import time
import urllib.request as ur
import uuid


class ImageLoader:

    def __init__(self, dim):
        self.dim = dim  # dimension of an image
        self.refPt = []
        self.cropping = False

    # loadImages takes url list as an input and returns a numpy array with all images.

    def loadImages(self, url_list):
        dim = self.dim
        url_list = [url for url in url_list if url is not None]
        dim_tuple = (dim, dim, 3, 1)
        numpy_array = np.zeros(dim_tuple).astype(int)
        ii = 0
        url_list_copy = url_list.copy()  # For for-loop
        for url in url_list_copy:
            ii += 1
            print("Numpy array size: ", numpy_array.shape)
            try:
                resp = ur.urlopen(url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                image = self.preprocessImage(image)  # Preprocessing (currently cropping), image is a file
                image = np.expand_dims(image, 3)
                if ii == 1:
                    numpy_array = np.add(numpy_array, image)
                else:
                    numpy_array = np.concatenate((numpy_array, image), axis=3)
                print("Downloaded %s" % (url))
            except Exception as e:
                url_list.remove(url)

        numpy_array = np.rollaxis(numpy_array, 3)
        return numpy_array.astype("uint8"), url_list

    # Swiping

    def sort_images(self, numpy_array):
        if not os.path.isdir("clean_pics"):
            os.makedirs("clean_pics")  # Creates folder for cleaned images
        if not os.path.isdir("garbage_pics"):
            os.makedirs("garbage_pics")  # Creates folder for garbage images

        foto_list_correct = []  # List with clean pictures - for a score
        numpy_array = numpy_array.astype("uint8")
        self.target_array = np.array([]).astype("uint8")

        for i in range(numpy_array.shape[0]):
            time.sleep(1)
            self.next_photo = False
            self.image = numpy_array[i, :, :, :]  # Load one image from numpy array
            self.file_name = uuid.uuid4().hex + ".jpg"  # Image name using hash function
            self.clone = self.image.copy()  # load the image, clone it, and setup the mouse callback function
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", self.click_and_crop)  # Activate mouse
            while True:
                cv2.imshow("image", self.image)
                key = cv2.waitKey(0) & 0xFF
                if key == ord("r"):  # if the 'r' key is pressed, reset the cropping region
                    self.image = self.clone.copy()
                    break
                # if the 'c' key is pressed, break from the loop
                if key == ord("a"):
                    cv2.destroyAllWindows()
                    self.new_path = "clean_pics/" + str(self.file_name)
                    foto_list_correct.append(self.file_name)
                    print(foto_list_correct)
                    # Add 1 to target array for neural network
                    self.target_array = np.append(self.target_array, 1).astype("uint8")
                    # Save file to a folder
                    if len(self.refPt) == 2:
                        self.image = self.image[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
                        self.image = self.preprocessImage(self.image)
                        cv2.imwrite(self.new_path, self.image)
                    else:
                        cv2.imwrite(self.new_path, self.image)
                    print("Moved to Class a")
                    self.next_photo = True
                    break
                if self.next_photo:
                    break
            cv2.destroyAllWindows()
        print("sorting done!")
        number_all = numpy_array.shape[0]
        number_correct = len(foto_list_correct)
        return number_correct, number_all, self.target_array

    # Mouse control for swiping

    def click_and_crop(self, event, x, y, flags, param):
        global refPt, cropping
        image3 = self.image.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.refPt.append((x, y))
            cropping = False
            cv2.rectangle(image3, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", image3)
        elif event == cv2.EVENT_RBUTTONUP:  # reset ROI
            if len(self.refPt) == 2:
                image3 = self.clone.copy()
                self.refPt = []
                cv2.imshow("image", image3)
            else:
                print("Moved to Class b")
                cv2.destroyAllWindows()
                self.new_path = "garbage_pics/" + str(self.file_name)
                # Add 0 to target array for neural network
                target_array = np.append(self.target_array, 0).astype("uint8")
                # Save file to a folder
                cv2.imwrite(self.new_path, self.image)
                self.next_photo = True

    # Squaring image
    def preprocessImage(self, prep_img):
        dim = self.dim

        # Load image and get dimensions
        height, width, channels = prep_img.shape

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

    def score(number_correct, number_all):
        score = 100 * (number_correct / number_all)
        return "In your folder {} % of images were correct.".format(score)
