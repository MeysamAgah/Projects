# Load Autoencoder model
autoencoder = tf.keras.models.load_model('autoencoder_model.h5')

# Function to colorize images of any size
def colorize_image(model, image_path, target_size=(480, 480)):
    # Load and preprocess the image
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray_resized = cv2.resize(img_gray, target_size)
    img_gray_resized = img_gray_resized.astype('float32') / 255.0
    img_gray_resized = np.expand_dims(img_gray_resized, axis=-1)  # Add channel dimension
    img_gray_resized = np.expand_dims(img_gray_resized, axis=0)  # Add batch dimension

    # Predict the colorized image
    predicted_image = model.predict(img_gray_resized)
    predicted_image = np.clip(predicted_image.squeeze() * 255.0, 0, 255).astype(np.uint8)

    return predicted_image

#this will colorize train set images
def evaluate_images(image_name):
    train_image_path = f'/kaggle/input/landscape-image-colorization/landscape Images/color/{image_name}.jpg'
    test_image_path = f'/kaggle/input/landscape-image-colorization/landscape Images/gray/{image_name}.jpg'
    colorized_image = colorize_image(autoencoder, test_image_path)
    
    # Display the results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.title("Original Grayscale Image")
    plt.imshow(cv2.cvtColor(cv2.imread(test_image_path), cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("Original Color Image")
    plt.imshow(cv2.cvtColor(cv2.imread(train_image_path), cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Colorized Image")
    plt.imshow(colorized_image)
    plt.axis('off')

    plt.show()

#this will colorize new photoes by url
def colorize_online_image(model, url, target_size=(480, 480)):
    try:
        # Download the image from the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Convert the image content to a numpy array
        image_array = np.frombuffer(response.content, np.uint8)
        
        # Decode the image array to a format suitable for OpenCV
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode the image. Please check the URL.")

        # Convert from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert the image to grayscale
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        
        # Resize the grayscale image
        img_gray_resized = cv2.resize(img_gray, target_size)
        img_gray_resized = img_gray_resized.astype('float32') / 255.0
        img_gray_resized = np.expand_dims(img_gray_resized, axis=-1)  # Add channel dimension
        img_gray_resized = np.expand_dims(img_gray_resized, axis=0)  # Add batch dimension

        # Predict the colorized image
        predicted_image = model.predict(img_gray_resized)
        predicted_image = np.clip(predicted_image.squeeze() * 255.0, 0, 255).astype(np.uint8)

        return img_gray_resized.squeeze(), predicted_image

    except Exception as e:
        print(f"An error occurred while processing the image from URL: {e}")
        return None, None

