# Import necessary libraries
import numpy as np
from matplotlib import pyplot as plt
import random
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, LeakyReLU, Conv2DTranspose, Dropout, ReLU, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

# Loss functions
def generator_loss(disc_generated_image, generated_image, real_image):
    gan_loss = cross_entropy(tf.ones_like(disc_generated_image), disc_generated_image)
    l1_loss = tf.reduce_mean(tf.abs(real_image - generated_image))
    total_gen_loss = gan_loss + (100 * l1_loss)
    return total_gen_loss, gan_loss, l1_loss

def discriminator_loss(disc_real_image, disc_generated_image):
    real_loss = cross_entropy(tf.ones_like(disc_real_image), disc_real_image)
    gen_loss = cross_entropy(tf.zeros_like(disc_generated_image), disc_generated_image)
    total_loss = real_loss + gen_loss
    return total_loss

def merge_l_ab(l_channel, ab_channel):
    l_channel = l_channel * 100.0  # scale back to original range [0, 100]
    ab_channel = ab_channel * 128.0  # scale back to original range [-128, 128]
    
    lab_image = np.concatenate([l_channel, ab_channel], axis=-1)
    rgb_image = lab2rgb(lab_image)  # Convert from LAB to RGB
    return rgb_image

def display_comparison(l_channel, ab_true, ab_pred):
    """Displays grayscale image (L), original colorized (ground truth), and predicted colorized image."""
    # Merge L with true AB for ground truth colorized image
    ground_truth = merge_l_ab(l_channel[0], ab_true[0])  # Take the first image for batch
    
    # Merge L with predicted AB for predicted colorized image
    predicted_image = merge_l_ab(l_channel[0], ab_pred[0])  # Take the first image for batch
    
    # Create subplots to display all three images
    plt.figure(figsize=(12, 8))
    
    # Display Grayscale Image (L-channel)
    plt.subplot(1, 3, 1)
    plt.imshow(l_channel[0], cmap='gray')
    plt.title('Grayscale Image (Input)')
    plt.axis('off')
    
    # Display Ground Truth Colorized Image
    plt.subplot(1, 3, 2)
    plt.imshow(ground_truth)
    plt.title('Ground Truth in Color')
    plt.axis('off')
    
    # Display Predicted Colorized Image
    plt.subplot(1, 3, 3)
    plt.imshow(predicted_image)
    plt.title('Colorized By Model')
    plt.axis('off')
  
    plt.tight_layout()
    plt.show()

def display_test(l_channel, ab_true, ab_pred):
    """Displays grayscale image (L), and predicted colorized image."""
    # Merge L with true AB for ground truth colorized image
    ground_truth = merge_l_ab(l_channel[0], ab_true[0])  # Take the first image for batch
    
    # Merge L with predicted AB for predicted colorized image
    predicted_image = merge_l_ab(l_channel[0], ab_pred[0])  # Take the first image for batch
    
    # Create subplots to display all three images
    plt.figure(figsize=(24, 12))
    
    # Display Ground Truth Colorized Image
    plt.subplot(1, 2, 1)
    plt.imshow(ground_truth)
    plt.title('Original Grayscale Image')
    plt.axis('off')
    
    # Display Predicted Colorized Image
    plt.subplot(1, 2, 2)
    plt.imshow(predicted_image)
    plt.title('Colorized By Model')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
