# Image Colorization<br>
## Overview <br>
This project aims to develop a deep learning model that can automatically colorize grayscale images. Utilizing an autoencoder architecture, the model learns to map grayscale images to their corresponding colored versions. The project leverages the TensorFlow framework for model building and training, and OpenCV for image processing.
## Objectives <br>
- To create an autoencoder neural network that can transform grayscale images into color images. <br>
- To train the model using a dataset of color images and their grayscale counterparts. <br>
- To evaluate the model's performance by comparing the colorized images with the original colored images. <br>
- To provide a user-friendly interface for colorizing new grayscale images from both local directories and URLs. <br>
## Dataset <br>
The dataset used for training consists of [landscape images](https://www.kaggle.com/datasets/theblackmamba31/landscape-image-colorization) that are divided into two categories: <br>
- Color Images: Original colored images used for training the model.<br>
- Grayscale Images: Grayscale versions of the colored images used as input for the model.<br>
The images are resized to a uniform dimension of 480x480 pixels to ensure consistency during model training. <br>
## Methodology <br>
**1- Data Preprocessing:** <br>
- Images are loaded from specified directories.<br>
- Color images are converted to float32 format and normalized to a range between 0 and 1.<br>
- Grayscale images are also converted to float32 format, normalized, and expanded to include a channel dimension.<br>

**2- Model Architecture:** <br>
<br>
 ![autoencoder](https://github.com/user-attachments/assets/a6f9aa3f-d284-42e7-aa1b-7c48747f660b)

 An autoencoder is built with the following layers: <br>
- Encoder: Comprised of several convolutional layers followed by max pooling layers that downsample the input image. <br>
- Bottleneck: The most compressed representation of the input image. <br>
- Decoder: A series of transposed convolutional layers and upsampling layers that reconstruct the image to its original size. <br>

The output layer utilizes a sigmoid activation function to produce pixel values in the range of 0 to 1. <br>

**3- Training the Model:** <br>
- The model is compiled with the Adam optimizer and trained using the mean squared error loss function.<br>
- The training process involves fitting the model on the grayscale images with their corresponding color images as targets, over a specified number of epochs.<br>

**4- Image Colorization:** <br>
- A function is implemented to colorize any grayscale image by resizing it to the target size and predicting the colorized output using the trained model.
- The resulting colorized image is post-processed and displayed.

**5- Evaluation:** <br>
- The model's performance is evaluated by colorizing a set of test grayscale images and comparing the results with the original colored images.
- Visualization is used to present side-by-side comparisons of the original grayscale images, the original color images, and the generated colorized images.

**6- Online Image Colorization:** <br>

- Additional functionality is implemented to colorize images directly from URLs, making the application more versatile.

## Results <br>
- The colorization results are evaluated visually by displaying original grayscale images alongside their colorized counterparts.<br>
![test1](https://github.com/user-attachments/assets/79bb4108-148f-4c84-82dd-1913411e6db4)
![test2](https://github.com/user-attachments/assets/d92257f0-6f2c-4f50-9694-7fda4052f2ab)
![test3](https://github.com/user-attachments/assets/ca38c133-fa14-4e2f-ab69-b2d0f97832fa)
![test4](https://github.com/user-attachments/assets/6f3e0811-8410-49c9-bd72-d37d7c7b6c15)
![test5](https://github.com/user-attachments/assets/72dd4137-0539-4ec7-a715-040f98a819a8)
![test6](https://github.com/user-attachments/assets/32fae89b-af73-4216-9131-23b921533121)

- The model's performance is assessed based on how accurately the colorization resembles the original grayscale images.<br>
![output1](https://github.com/user-attachments/assets/373ba8e7-a663-48ef-9607-d97597fbeb8e)
![output2](https://github.com/user-attachments/assets/8043960e-ceeb-483f-946a-2893d752119a)
![output3](https://github.com/user-attachments/assets/f6ae99b3-8ccc-4891-86e5-f0b0dd4ebdfe)

## Conclusion <br>
The project successfully demonstrates the ability to utilize deep learning techniques for image colorization. The developed autoencoder effectively learns the mapping from grayscale to color images, enabling the transformation of grayscale images into visually appealing colorized versions. This application has potential uses in various fields such as photography restoration, artistic applications, and enhancing visual content.<br>

Note: The low quality of the colorized images was due to hardware limitations and the use of low-resolution training images. For future projects, I'll address this by using higher-quality images and more advanced models to improve results.
