# Import necessary libraries
import numpy as np
from matplotlib import pyplot as plt
import os
import random
#import re
import cv2
from skimage.color import rgb2lab, lab2rgb
from tqdm import tqdm
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, LeakyReLU, Conv2DTranspose, Dropout, ReLU, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from data import *
from Model import *
from utils import *
from train import *

# Paths to image sources
color_paths = [
    '/kaggle/input/landscape-pictures',
    '/kaggle/input/flickrfaceshq-dataset-ffhq',
    '/kaggle/input/image-colorization/unlabeled2017_subsample'
]

# Image size and selection sizes
SIZE = 512 #image_size
SIZES = [4314, 20000, 11000]  # all images from landscape-pictures and image-colorization and 20000 random images from flickrfaceshq

# Set random seed for reproducibility (optional)
random.seed(42)

# Load the dataset using the strategy scope
l_channel, ab_channels = load_and_preprocess_data(color_paths, SIZES, SIZE)

# convert l_channel and ab_cahnnel to tensorflow datasets
l_dataset = tf.data.Dataset.from_tensor_slices(l_channel).batch(256)
ab_dataset = tf.data.Dataset.from_tensor_slices(ab_channels).batch(256)

# Combine the datasets
combined_dataset = tf.data.Dataset.zip((l_dataset, ab_dataset))

generator = Generator()
discriminator = Discriminator()

cross_entropy = BinaryCrossentropy(from_logits=True)
generator_optimizer = Adam(2e-4, beta_1=0.5)
discriminator_optimizer = Adam(2e-4, beta_1=0.5)

num_epochs = 100

fit(combined_dataset, epochs=num_epochs)

# checking results for train(optional)
for i in range(len(l_channel)):
    pred_ab_channels = generator(l_channel[i:i+1], training=False)
    # Display the comparison
    display_comparison(l_channel[i:i+1], ab_channels[i:i+1], pred_ab_channels)

# Testing on new data
# Paths to image sources
color_paths = ['any path you have desired images']
num_images = 500 #any size of images you want in your test path

# Image size and selection sizes
SIZE = 512 #size must be equal with model input size
SIZES = [num_images]  

# Set random seed for reproducibility (optional)
#random.seed(42)

# Load the dataset using the strategy scope
new_l_channel, new_ab_channels = load_and_preprocess_data(color_paths, SIZES, SIZE)

new_l_dataset = tf.data.Dataset.from_tensor_slices(new_l_channel).batch(256)
new_ab_dataset = tf.data.Dataset.from_tensor_slices(new_ab_channels).batch(256)

combined_dataset = tf.data.Dataset.zip((new_l_dataset, new_ab_dataset))
new_pred_ab_channels = generator(new_l_channel, training=False)
for i in range(len(new_l_channel)):
    display_test(new_l_channel[i:i+1], new_ab_channels[i:i+1], new_pred_ab_channels[i:i+1])
