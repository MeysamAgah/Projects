# Import necessary libraries
import numpy as np
import os
import random
import cv2
from skimage.color import rgb2lab, lab2rgb
from tqdm import tqdm


#this function will load and preproces images from different datasets
def load_and_preprocess_data(color_paths, sizes, size):
    l_channel, ab_channels = [], []
    for path, num_images in zip(color_paths, sizes):
        all_files = os.listdir(path)
        selected_files = random.sample(all_files, min(num_images, len(all_files))) #pick a random sample from dataset
        # Create a tqdm progress bar for this path
        progress_bar = tqdm(
            selected_files, 
            desc=f'Processing images from {os.path.basename(path)}', 
            total=len(selected_files),
            position=0,
            leave=True
        )
        
        for file in progress_bar:
            img_path = os.path.join(path, file)
            img = cv2.imread(img_path, 1)
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize image
            img = cv2.resize(img, (size, size))
            
            # Convert to LAB color space
            lab_img = rgb2lab(img)
            lab_img = lab_img.astype('float32')
            
            # Normalize channels
            l_channel.append(lab_img[:, :, 0] / 100.0)  # L channel to [0, 1]
            ab_channels.append(lab_img[:, :, 1:] / 128.0)  # AB channels to [-1, 1]
    
    # Convert to numpy arrays
    l_channel = np.expand_dims(np.array(l_channel), axis=-1)  # Add channel dimension
    ab_channels = np.array(ab_channels)
  
    return l_channel, ab_channels

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