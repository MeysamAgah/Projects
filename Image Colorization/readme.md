# Image Colorization<br>
## Overview <br>
This project aims to develop a deep learning model that can automatically colorize grayscale images. Utilizing a Generative Adversarial Network (GAN) architecture, the model employs a generator to predict the colored version of grayscale images and a discriminator to evaluate the realism of the generated outputs. The project leverages the TensorFlow framework for model building and training, and OpenCV for image processing.
## Dataset <br>
For training, multiple image datasets from Kaggle were utilized. These include 20,000 random sample images from the [Flickr-Faces-HQ (FFHQ)](https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq) Dataset, the [Landscape Pictures](https://www.kaggle.com/datasets/arnaud58/landscape-pictures) Dataset, and the [Image Colorization](https://www.kaggle.com/datasets/mariomatos/image-colorization) Dataset.
## Methodology <br>
**LAB channel:** <br>
The Lab color space is preferred over RGB for this project due to its perceptual advantages and the simplified nature of the prediction task. The Lab space separates luminance (lightness) information from chrominance (color) information. This separation allows the model to focus on predicting only the color components ('a' and 'b' channels) while retaining the luminance channel ('L') directly from the grayscale input.

One of the key benefits of using Lab is its perceptual uniformity. In Lab, changes in color values correspond more closely to perceived changes in color by the human eye, making it easier for the model to generate colorized images that look realistic and natural. This is especially important in colorization tasks where visual coherence and accuracy are crucial.

Additionally, by predicting only the chrominance channels ('a' and 'b'), the model's task is simplified compared to predicting all three RGB channels. This results in a more efficient learning process, as the model can focus on generating the color information while maintaining the luminance structure of the image, which is already provided by the grayscale input.<br>
**GAN:** <br> 
A Generative Adversarial Network (GAN) is a type of deep learning model composed of two neural networks: a generator and a discriminator. These networks work in opposition to each other, which is why it's called "adversarial."
The generator creates synthetic data (in this case, colorized images) from random noise or input data (grayscale images).
The discriminator evaluates the authenticity of the generated data, distinguishing between real images (from the training set) and fake images (produced by the generator).<br>
The generator and discriminator are trained simultaneously in a game-like process, where the generator tries to improve its ability to create realistic images, and the discriminator tries to get better at identifying fake images. Over time, this adversarial training helps the generator produce highly realistic outputs that are indistinguishable from real data.<br>
Why Use GANs for Image Colorization?<br>
In this project, GANs are used for image colorization because of their ability to generate high-quality, realistic images. Traditional approaches, such as autoencoders, focus on learning a compressed representation of the input, but they may struggle with generating detailed, realistic colors. GANs, on the other hand, are well-suited for this task as they learn to generate data that closely resembles real-world images by refining their outputs through adversarial feedback.<br>
The use of GANs helps in producing more vibrant and natural-looking colorized images. By employing both the generator and discriminator, GANs ensure that the generated colors are not only plausible but also consistent with real-world color distributions. This makes GANs a powerful tool for tasks such as image colorization, where the goal is to generate high-quality, perceptually accurate colors.
**Generator:** <br>
**Discriminator:** <br>
**Optimizers:** <br>
Two Adam optimizers are used, one for the generator and another for the discriminator:<br>
Both optimizers use a learning rate of 2e-4 and The beta_1 parameter is set to 0.5.<br>
**Loss Functions:** <br>
Generator Loss:<br>
$`
\mathcal{L}_{\text{gen}} = \mathcal{L}_{\text{GAN}} + 100 \cdot \mathcal{L}_1
`$
<br> Where:<br>
$`
\mathcal{L}_{\text{GAN}} = - \mathbb{E}[\log D(G(z))]
`$
<br> and <br>
$`
\mathcal{L}_1 = \frac{1}{N} \sum_{i=1}^{N} |x_i - \hat{x}_i|
`$
<br> Discriminator Loss:<br>
$`
\mathcal{L}_{\text{disc}} = \mathcal{L}_{\text{real}} + \mathcal{L}_{\text{fake}}
`$
<br> Where: <br>
$`
\mathcal{L}_{\text{real}} = - \mathbb{E}[\log D(x)]
`$
<br> and <br>
$`
\mathcal{L}_{\text{fake}} = - \mathbb{E}[\log (1 - D(G(z)))]
`$
## Results <br>
**Sample output on training:** <br>
**Sample output on new images:** <br>
## Conclusion <br>
The project successfully demonstrates the capability of leveraging Generative Adversarial Networks (GANs) for image colorization. The GAN architecture effectively learns to generate realistic and visually appealing colorized images from grayscale inputs by combining the strengths of a generator and discriminator. This approach holds potential for applications in fields such as photography restoration, artistic enhancements, and visual content creation.
