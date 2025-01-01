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
