# Ignoring warnings only because they are deprecation warnings
import warnings
warnings.filterwarnings("ignore")

import os
import glob
import numpy as np
import cv2
#import hairanalysis
#import importlib
#importlib.reload(hairanalysis)

import keras
from keras.preprocessing.image import image 
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras import backend as K


def predict_class(uploaded_img):
    warnings.filterwarnings("ignore")

    # First apply the binary classification for hair/not hair
    img_width, img_height = 200,200

    img = image.load_img(uploaded_img, target_size = (img_width, img_height))
    img_arr = image.img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    img_arr /= 255

    if K.image_data_format() == 'channels_first': 
        input_shape = (3, img_width, img_height) 
    else: 
        input_shape = (img_width, img_height, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.load_weights('model_binary_saved_sigmoid.h5')

    model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    
    pred = model.predict(img_arr)

    K.clear_session()

    dict_labels = {0: 'hair', 1:'nonhair'}
    if pred[0] > 0.5:
        return 'nonhair'
 
    # Then apply the classifier for type of hair
    img_width, img_height = 400, 400
    nb_classes = 5

    # Mask the uploaded image to just hair
    #im = cv2.imread(uploaded_img)
    #mask = hairanalysis.predict_mask(im)
    #dst = hairanalysis.transfer_mask(im, mask)
    
    img = image.load_img(uploaded_img, target_size = (img_width, img_height))
    img_arr = image.img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    img_arr /= 255

    if K.image_data_format() == 'channels_first': 
        input_shape = (3, img_width, img_height) 
    else: 
        input_shape = (img_width, img_height, 3)

    conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=input_shape)

    model = Sequential()
    model.add(conv_base)
    model.add(Flatten())
    model.add(Dense(512*4, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(512*4, activation='relu'))
    model.add(Dense(nb_classes, activation='softmax'))

    model.load_weights('model_saved_VGG_5cat.h5')

    model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    
    pred = model.predict(img_arr)

    K.clear_session()
    
    index_predict = np.argmax(pred[0])

    if pred[0][index_predict] <= 0.5:
        return "unsure"

    dict_labels = {0:'curly', 1: 'quite curly', 2:'short', 3:'straight', 4:'wavy'}  
    
    return dict_labels[index_predict]

