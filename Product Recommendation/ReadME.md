# Objective
The objective of this project is to create a fashion recommendation system using ResNET that provides personalized fashion recommendations to users based on images they upload. The system will perform the following steps:

1. Analyze the visual features of the uploaded image using computer vision techniques and machine learning algorithms, such as ResNET, to identify the type of clothing or accessory in the image.
2. Compare the features of the image with a database of fashion products and styles to find similar items.
3. Provide the user with a list of recommendations for similar products that are available for purchase.

# Key learnings
1. The project uses transfer learning on 44,000 images by leveraging the ResNET architecture.
2. The ResNET model is used to extract the features of the images in the database and to extract the features of the test images.
3. The 2048 features extracted by ResNET from each image are also known as embeddings.
4. Image embeddings are lower-dimensional representations of the images that can be used for various tasks such as classification.
5. In this project, the ResNET model is used to create image embeddings and the trainable parameters of the model have been turned off as we are using a pre-trained model.

# Plan of attack
The following steps will be taken to create the fashion recommendation system:

1. Import the ResNET model
2. Extract the features of the images in the database
3. Export the extracted features
4. Generate recommendations based on the extracted features

# Code snippet

Here is a sample code snippet that shows the process of extracting the features of the images in the database:
### Load the ResNET model with pre-trained weights and set the model to be untrainable
```
  model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))
  model.trainable = False
```

### Add a global max pooling layer to the model
```
model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])
```
```
def extract_features(img_path, model):
    
    # Load the image and preprocess it
   
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    
    # Use the model to predict the features of the image
    
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    
    return normalized_result
```
### Load the filenames of the images in the database
```
filenames = []
for file in os.listdir('images'):
    filenames
```
