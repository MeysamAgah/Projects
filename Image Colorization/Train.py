#requirements
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import requests

#setting directory for train and test
train_dir = '/kaggle/input/landscape-image-colorization/landscape Images/color'
test_dir = '/kaggle/input/landscape-image-colorization/landscape Images/gray'

#Function to load and preprocess images
def load_and_preprocess_images(dir_path, target_size=(480, 480), color_mode=cv2.COLOR_BGR2RGB):
    images = []
    for image_name in os.listdir(dir_path):
        image_path = os.path.join(dir_path, image_name)
        image = cv2.imread(image_path)
        if color_mode == cv2.COLOR_BGR2GRAY:
            image = cv2.cvtColor(image, color_mode)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image, target_size)
        images.append(image_resized)
    return np.array(images)

# Load training and testing data
train_images = load_and_preprocess_images(train_dir)
grayscale_images = load_and_preprocess_images(test_dir, color_mode=cv2.COLOR_BGR2GRAY)

# Normalize images
train_images = train_images.astype('float32') / 255.0
grayscale_images = grayscale_images.astype('float32') / 255.0

# Expand dimensions for grayscale images
grayscale_images = np.expand_dims(grayscale_images, axis=-1)

def build_autoencoder():
    input_img = Input(shape=(480, 480, 1))  # Input shape (None, None, 1) for flexibility

    # Encoder
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)    
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x) 
    x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    # Decoder
    x = Conv2DTranspose(512, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)  
    x = Conv2DTranspose(256, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(128, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(64, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2DTranspose(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)

    # Output layer
    output_img = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)  # Output shape (None, None, 3)

    autoencoder = Model(input_img, output_img)
    return autoencoder

autoencoder = build_autoencoder()
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
autoencoder.fit(grayscale_images, train_images, epochs=100, batch_size=128, shuffle=True, validation_split=0.2)
autoencoder.save('autoencoder_model.h5')