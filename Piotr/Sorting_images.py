# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:58:20 2018

@author: tatar
"""
import cv2
import os
import shutil


def sort_images(list_classes, path_to_images):
    foto_list = os.listdir(path_to_images)
    
    #Create as many folders as classes
    new_folders = [] 
    for classes in list_classes:
        newpath = path_to_images + "/" + str(classes) 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            new_folders.append(newpath)

    
    foto_list_correct = []
    for image in foto_list:    
    
    #display resized image
        img = cv2.imread(image)
        try:
            height_or, width_or = img.shape[:2]
            ratio = height_or/width_or
            resized = cv2.resize(img, (400, int(400*ratio)), interpolation = cv2.INTER_AREA)
        except:
            print("Format wrong!")
            
        endProgram = False

        cv2.imshow('Image', resized)
        
        # sorting into folders 
        
        while not endProgram:
        ############ CORRECT: PRESS "A"  ####################
            if cv2.waitKey(33) == ord('a'):
                print("Moved to Class a")
                cv2.destroyAllWindows()
                current_path = str(os.getcwd()) + "/" +str(image)
                new_path = new_folders[0]
                shutil.move(current_path, new_path)
                foto_list_correct.append(img)
                endProgram = True
        
        ############ INCORRECT: PRESS "B"  ####################
            if cv2.waitKey(33) == ord('b'):
                print("Moved to Class b")
                cv2.destroyAllWindows()
                current_path = str(os.getcwd()) + "/" +str(image)
                new_path = new_folders[1]
                shutil.move(current_path, new_path)
        
                endProgram = True
    
    print("sorting done!")
    number_all = len(foto_list)
    number_correct = len(foto_list_correct)
    return number_correct, number_all
######################################################################
######################################################################
######################################################################
    
def score(number_correct, number_all):
    score = 100*(number_correct/number_all)
    return "In your folder {} % of images were correct.".format(score)
    
  
    
path = "C:/Users/tatar/Desktop/GANs/00_Project_Piotr/foto_test"
list_classes = ["shapes", "faces"]


number_correct, number_all = sort_images(list_classes, path)

score(number_correct, number_all)
