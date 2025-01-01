# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, LeakyReLU, Conv2DTranspose, Dropout, ReLU, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy

@tf.function
def train_step(l_channel, ab_channels, epoch):
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_image = generator(l_channel, training=True)

        disc_real_image = discriminator([l_channel, ab_channels], training=True)
        disc_generated_image = discriminator([l_channel, generated_image], training=True)

        gen_total_loss, gen_gan_loss, gen_l1_loss = generator_loss(disc_generated_image, generated_image, ab_channels)
        disc_loss = discriminator_loss(disc_real_image, disc_generated_image)

    generator_gradients = gen_tape.gradient(gen_total_loss,
                                            generator.trainable_variables)
    discriminator_gradients = disc_tape.gradient(disc_loss,
                                                 discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(generator_gradients,
                                            generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(discriminator_gradients,
                                                discriminator.trainable_variables))

def fit(dataset, epochs):
    for e in range(epochs):
        print("Epoch: ", e+1)
        for l_channel1, ab_channels1 in dataset:
            strategy.run(train_step, args=(l_channel1, ab_channels1, e))

        pred_ab_channels = generator(l_channel[750:751], training=False) #750 is a random pic in dataset could be any number
        # Display the comparison
        display_comparison(l_channel[750:751], ab_channels[750:751], pred_ab_channels)
        print()
