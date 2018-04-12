import tensorflow as tf
import numpy as np
from keras import optimizers
from keras import applications
from keras.preprocessing import image
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential, Model 
from IPython.display import display
from PIL import Image
import os
import random
import matplotlib.pyplot as plt

class Ranker_NN():
        '''
        Ranker takes three arguments: n_classes (=2), number of fully connected nodes for custom layer 1 and 2   
        '''
        def __init__(self,n_classes,n_fully_connected_1,n_fully_connected_2):
            self.n_classes=n_classes     
            self.fc1=n_fully_connected_1 
            self.fc2=n_fully_connected_2
            self.resnet = applications.resnet50.ResNet50(include_top=False, weights='imagenet',input_shape=(224,224,3))
            for layer in self.resnet.layers:
                layer.trainable = False
            self.model_final = self.convolutional_neural_network()
            self.model_final.compile(optimizer=optimizers.Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
        '''
        convolutional_neural_network method creates our custom CNN. 
        CNN is composed out of freezed ResNet layers and additional custom-made
        fully connected layers. It returns an object 'model_final', which is our CNN model.
        '''
        def convolutional_neural_network(self):
            x = self.resnet.output
            x = Flatten()(x)
            x = Dense(self.fc1, activation="relu")(x)
            # x=Dropout(0.5)(x)
            # x=Dense(self.fc2, activation="relu")(x)
            output = Dense(self.n_classes,activation='sigmoid')(x)
            self.model_final = Model(input=self.resnet.input, output=output)
            return self.model_final
            '''
            make_prediction method allows us to perform pass through the CNN.
            It takes images from the string 'raw_image_source', which is the path and
            returns a returns a numpy array of size (no_of_images,2),
            where two elements in every row correspond to two results of sigmoid operation
            (sum up to 1) for each training sample. .
            '''
        def make_prediction(self, img_array):
            # list_of_raw_files=os.listdir(raw_image_source)
            prediction_list=np.array([[0]])
            for img in img_array:
                # img=image.load_img(img_path,target_size=(224,224))
                # x=image.img_to_array(img)
                x=np.expand_dims(img,axis=0)
                x_image = applications.resnet50.preprocess_input(x)
                prediction = self.model_final.predict(x_image)
                prediction  =np.array(prediction)
                print(prediction)
                prediction_list = np.concatenate((prediction_list, prediction), axis=0)
            prediction_list = np.delete(prediction_list, (0), axis=0)
            return prediction_list

        def train_model(self, data, true_labels, batch_size, no_epochs):
            self.history = self.model_final.fit(data, true_labels, epochs=no_epochs, batch_size=batch_size)
            
        def evaluation_plot(self):
            plt.figure()
            plt.plot(self.history.history['loss'])
            plt.plot(self.history.history['acc'])
            plt.title('Result of training')
            plt.xlabel('epoch')
            plt.legend(['loss', 'accuracy'], loc='upper left')
            plt.show()  
        def save_model(self):
            self.model_final.save('GandeeCNN.h5')

def create_dummy_labels(no_of_elements):
    dummy_list=np.array([[0,0]])
    possible_labels=[0,1]
    for number in range(no_of_elements):
        a=random.choice(possible_labels)
        if a==1:
            b=0
        else:
            b=1
        row=np.array([[a,b]])
        print(row)
        dummy_list=np.concatenate((dummy_list, row), axis=0)
    dummy_list = np.delete(dummy_list, (0), axis=0)
    return dummy_list

def create_training_data(raw_image_source):
    list_of_raw_files=os.listdir(raw_image_source)
    dummy_list=np.zeros([1,224,224,3])
    for img_path in list_of_raw_files:
        img=image.load_img(img_path,target_size=(224,224)) 
        x=image.img_to_array(img) 
        x=np.expand_dims(x,axis=0) 
        x_image=applications.resnet50.preprocess_input(x)
        dummy_list=np.vstack((dummy_list, x_image))
    dummy_list = np.delete(dummy_list, (0), axis=0)
    return dummy_list