# -*- coding: utf-8 -*-
"""Sandstone Segmentation

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/sandstone-segmentation-11cd4497-2111-47a8-ab8f-7b0f51cbd278.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20241119/auto/storage/goog4_request%26X-Goog-Date%3D20241119T040149Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D971f392237f16b55547b605bc860a9255950d406b8ae57a15c5e52c462431da73ee18cd3b7178d50908556a49124c6f788deb145eda6058e774886bad48de88b144539fb7768b30c78f191a26e7dc0a7e3decb3acf7c11f07423a0b98b1279dc469e90c22e9764ebcd53be67e07711ade6ac1aabc79e26ade6d008d439f55bc6cbb99e5b40d3ba55fa15a348517229197bedb69ae0ea17ec4e2c872246492feac2c032dfc564da3e25b47eb80c9939a2aa7f858d38ac71e473398984ac1a4b149025231f7c2ea9d91b3150f7f5d018ea35dbe5d7db247f4253e5787fd4646ac182bcc6730990101ed061d0c9fee7472d24ee53c2a4b8ce5e1a884014ea4ff759
"""

# IMPORTANT: SOME KAGGLE DATA SOURCES ARE PRIVATE
# RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES.
import kagglehub
kagglehub.login()

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

fatmasaeed123_sandstone_dataset_path = kagglehub.dataset_download('fatmasaeed123/sandstone-dataset')

print('Data source import complete.')

"""Import Dataset"""

dataset="/kaggle/input/sandstone-dataset/sandstone"

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
img = mpimg.imread('/kaggle/input/sandstone-dataset/sandstone/images/image_1.tif')
imgplot = plt.imshow(img)
plt.show()

import cv2
import matplotlib.pyplot as plt
mask = cv2.imread('/kaggle/input/sandstone-dataset/sandstone/masks/image_1.tif', 0)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(mask, cmap='gray')

img = mpimg.imread('/kaggle/input/sandstone-dataset/sandstone/images/image_1022.tif')
imgplot = plt.imshow(img)
plt.show()
img.shape

print(img.flatten())

print(np.unique(mask))

"""**Build Muiticlass U_net Model **"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical

def unet_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)

    # Encoder
    conv1 = layers.Conv2D(64, 3, activation="relu", padding="same")(inputs)
    conv1 = layers.Conv2D(64, 3, activation="relu", padding="same")(conv1)
    pool1 = layers.MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = layers.Conv2D(128, 3, activation="relu", padding="same")(pool1)
    conv2 = layers.Conv2D(128, 3, activation="relu", padding="same")(conv2)
    pool2 = layers.MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = layers.Conv2D(256, 3, activation="relu", padding="same")(pool2)
    conv3 = layers.Conv2D(256, 3, activation="relu", padding="same")(conv3)
    pool3 = layers.MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = layers.Conv2D(512, 3, activation="relu", padding="same")(pool3)
    conv4 = layers.Conv2D(512, 3, activation="relu", padding="same")(conv4)
    pool4 = layers.MaxPooling2D(pool_size=(2, 2))(conv4)

    # Bottleneck
    conv5 = layers.Conv2D(1024, 3, activation="relu", padding="same")(pool4)
    conv5 = layers.Conv2D(1024, 3, activation="relu", padding="same")(conv5)

    # Decoder
    up6 = layers.Conv2DTranspose(512, 2, strides=(2, 2), padding="same")(conv5)
    merge6 = layers.concatenate([conv4, up6], axis=3)
    conv6 = layers.Conv2D(512, 3, activation="relu", padding="same")(merge6)
    conv6 = layers.Conv2D(512, 3, activation="relu", padding="same")(conv6)

    up7 = layers.Conv2DTranspose(256, 2, strides=(2, 2), padding="same")(conv6)
    merge7 = layers.concatenate([conv3, up7], axis=3)
    conv7 = layers.Conv2D(256, 3, activation="relu", padding="same")(merge7)
    conv7 = layers.Conv2D(256, 3, activation="relu", padding="same")(conv7)

    up8 = layers.Conv2DTranspose(128, 2, strides=(2, 2), padding="same")(conv7)
    merge8 = layers.concatenate([conv2, up8], axis=3)
    conv8 = layers.Conv2D(128, 3, activation="relu", padding="same")(merge8)
    conv8 = layers.Conv2D(128, 3, activation="relu", padding="same")(conv8)

    up9 = layers.Conv2DTranspose(64, 2, strides=(2, 2), padding="same")(conv8)
    merge9 = layers.concatenate([conv1, up9], axis=3)
    conv9 = layers.Conv2D(64, 3, activation="relu", padding="same")(merge9)
    conv9 = layers.Conv2D(64, 3, activation="relu", padding="same")(conv9)

    outputs = layers.Conv2D(num_classes, 1, activation="softmax")(conv9)

    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

# Example usage:
input_shape = (128, 128, 3)  # Replace with your actual input shape
num_classes = 4
model = unet_model(input_shape, num_classes)
model.summary()

import os
import numpy as np
from PIL import Image

image_dir = '/kaggle/input/sandstone-dataset/sandstone/images'
mask_dir = '/kaggle/input/sandstone-dataset/sandstone/masks'

image_files = sorted(os.listdir(image_dir))
mask_files = sorted(os.listdir(mask_dir))

images = []
masks = []

for i in range(len(image_files)):
  try:
    # Open image and convert to RGB if necessary
    img = Image.open(os.path.join(image_dir, image_files[i])).convert('RGB')  # Ensure RGB format
    img = img.resize((128, 128))
    img_arr = np.array(img)
    images.append(img_arr)

    mask = Image.open(os.path.join(mask_dir, mask_files[i]))
    mask = mask.resize((128, 128))
    mask_arr = np.array(mask)
    masks.append(mask_arr)
  except Exception as e:
    print(f"Error processing file {image_files[i]} or {mask_files[i]}: {e}")
    continue

import os
import numpy as np
from PIL import Image
from tensorflow.keras.utils import to_categorical

image_dir = '/kaggle/input/sandstone-dataset/sandstone/images'
mask_dir = '/kaggle/input/sandstone-dataset/sandstone/masks'

image_files = sorted(os.listdir(image_dir))
mask_files = sorted(os.listdir(mask_dir))

images = []
masks = []

for i in range(len(image_files)):
    try:
        # Open image and convert to RGB if necessary
        img = Image.open(os.path.join(image_dir, image_files[i])).convert('RGB')  # Ensure RGB format
        img = img.resize((128, 128))
        img_arr = np.array(img)
        images.append(img_arr)

        mask = Image.open(os.path.join(mask_dir, mask_files[i]))
        mask = mask.resize((128, 128))
        mask_arr = np.array(mask)

        # Ensure mask values are within the expected range (0-3 for 4 classes)
        mask_arr[mask_arr >= 4] = 3 # If they are not, change the values to the max of the desired range(3)

        masks.append(mask_arr)
    except Exception as e:
        print(f"Error processing file {image_files[i]} or {mask_files[i]}: {e}")
        continue

# Shift masks values by 1 to be within range 0-3

masks = [mask - 1 for mask in masks] # Use list comprehension to subtract 1 from each NumPy array in the list.


masks = to_categorical(masks, num_classes=4) # masks must be within range 0-3 for this to work

# Normalize pixel values
images = np.array(images)

images = images / 255.0

# Split data into training and validation sets
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(images, masks, test_size=0.2, random_state=42)


# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=15, batch_size=16, validation_data=(X_val, y_val))

# prompt: plot the loss curve and accuracy

import matplotlib.pyplot as plt
# Plot the loss curve
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot the accuracy curve
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Predict on the validation set
predictions = model.predict(X_val)

# Choose a random image from the validation set
import random
random_index = random.randint(0, len(X_val) - 1)
predicted_mask = np.argmax(predictions[random_index], axis=-1)
true_mask = np.argmax(y_val[random_index], axis=-1)

# Display the image, true mask, and predicted mask
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(X_val[random_index])
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(true_mask)
plt.title('True Mask')

plt.subplot(1, 3, 3)
plt.imshow(predicted_mask)
plt.title('Predicted Mask')

plt.show()