# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, LeakyReLU, Conv2DTranspose, Dropout, ReLU, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy


def downsample(filters, size, apply_batchnorm=True):
    result = tf.keras.Sequential()
    result.add(Conv2D(filters, size, strides=2, padding='same', 
                      kernel_initializer='he_normal', use_bias=False))
    
    if apply_batchnorm:
        result.add(BatchNormalization())
    
    result.add(LeakyReLU())
    return result

def upsample(filters, size, apply_dropout=False):
    result = tf.keras.Sequential()
    result.add(Conv2DTranspose(filters, size, strides=2, padding='same', 
                               kernel_initializer='he_normal', use_bias=False))
    result.add(BatchNormalization())

def Generator():
    inputs = Input(shape=[512, 512, 1])  # Single-channel input (L-channel)
    
    # Downsampling stack to encode the input image
    down_stack = [
        downsample(64, 4, apply_batchnorm=False),   # Downsample to 256x256
        downsample(128, 4),                         # Downsample to 128x128
        downsample(256, 4),                         # Downsample to 64x64
        downsample(512, 4),                         # Downsample to 32x32
        downsample(512, 4),                         # Downsample to 16x16
        downsample(1024, 4),                        # Downsample to 8x8
        downsample(1024, 4),                        # Downsample to 4x4
        downsample(1024, 4),                        # Downsample to 2x2
        downsample(1024, 4),                        # Downsample to 1x1
    ]
    
    # Upsampling stack to decode the features back to the original image size
    up_stack = [
        upsample(1024, 4, apply_dropout=True),      # Upsample to 2x2
        upsample(1024, 4, apply_dropout=True),      # Upsample to 4x4
        upsample(1024, 4, apply_dropout=True),      # Upsample to 8x8
        upsample(512, 4),                           # Upsample to 16x16
        upsample(512, 4),                           # Upsample to 32x32
        upsample(256, 4),                           # Upsample to 64x64
        upsample(128, 4),                           # Upsample to 128x128
        upsample(64, 4),                            # Upsample to 256x256
    ]
    
    # Initialize the last convolution layer
    initializer = tf.random_normal_initializer(0., 0.02)
    
    # Last layer to generate 2-channel (AB) output, with 'tanh' activation for pixel value range [-1, 1]
    last = Conv2DTranspose(2, 4, strides=2, padding='same', 
                           kernel_initializer=initializer, activation='tanh')  # 2-channel output (AB)
    
    # Define the model architecture
    x = inputs
    skips = []
    
    # Apply the downsampling layers (encoding part)
    for down in down_stack:
        x = down(x)
        skips.append(x)
    
    # Reverse the skip connections to match the upsampling sequence
    skips = reversed(skips[:-1])  # Remove the last skip layer, as it's not needed for concatenation
    
    # Apply the upsampling layers (decoding part)
    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = Concatenate()([x, skip])  # Concatenate the skip connection with the upsampled output
    
    # Generate the final output
    x = last(x)
    
    # Return the complete model
    return Model(inputs=inputs, outputs=x)

    
    if apply_dropout:
        result.add(Dropout(0.5))
    
    result.add(ReLU())
    return result

def Discriminator():
    initializer = tf.random_normal_initializer(0., 0.02)
    
    # Inputs for 512x512 size
    inp = Input(shape=[512, 512, 1], name='input_image')     # Single-channel input (L-channel)
    tar = Input(shape=[512, 512, 2], name='target_image')    # Two-channel target (AB-channel)
    
    x = Concatenate()([inp, tar])
    
    # More downsampling layers for 512x512 input
    down1 = downsample(64, 4, False)(x)     # 256x256
    down2 = downsample(128, 4)(down1)       # 128x128
    down3 = downsample(256, 4)(down2)       # 64x64
    down4 = downsample(512, 4)(down3)       # 32x32
    down5 = downsample(1024, 4)(down4)
    
    zero_pad1 = tf.keras.layers.ZeroPadding2D()(down5)
    conv = Conv2D(512, 4, strides=1, kernel_initializer=initializer, use_bias=False)(zero_pad1)
    batchnorm1 = BatchNormalization()(conv)
    leaky_relu = LeakyReLU()(batchnorm1)
    
    zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu)
    last = Conv2D(1, 4, strides=1, kernel_initializer=initializer)(zero_pad2)
    
    return Model(inputs=[inp, tar], outputs=last)
