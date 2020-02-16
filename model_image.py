# Ignoring warnings only because they are deprecation warnings
import warnings
warnings.filterwarnings("ignore")

import numpy as np
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
    # N.B. image shape is is specified so all input images can be given the same size
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

    # Binary model trained on augmented CIFAR-10 images and Figaro1k hair dataset
    model.load_weights('model_binary_saved_sigmoid.h5')

    model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    
    pred = model.predict(img_arr)

    K.clear_session()
    print(pred[0])
    dict_labels = {0: 'hair', 1:'nonhair'}
    if pred[0] > 0.5:
        return 'nonhair'
 
    # Then apply the classifier for type of hair
    img_width, img_height = 400, 400
    nb_classes = 4
    
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

    # VGG16 pretrained model with 2 fully connected layers added
    # Trained on Figaro1k images
    model.load_weights('model_saved_VGG_4cat.h5')

    model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
    
    pred = model.predict(img_arr)

    K.clear_session()
    
    index_predict = np.argmax(pred[0])

    # If not category has probability >50%, returns unsure
    if pred[0][index_predict] <= 0.5:
        return "unsure"

    dict_labels = {0:'curly', 1: 'quite curly', 2:'straight', 3:'wavy'}  
    
    return dict_labels[index_predict]

