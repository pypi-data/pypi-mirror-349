def run():
    print("""
This is experiment 10  Build a coloring deep neural network
import os
import kagglehub
from tensorflow.keras.layers import Conv2D, UpSampling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from skimage.color import rgb2lab
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Download dataset from Kaggle
aishwr_coco2017_path = kagglehub.dataset_download('aishwr/coco2017')
print('Data source import complete.')
print(aishwr_coco2017_path)

dataset_path = '/root/.cache/kagglehub/datasets/aishwr/coco2017/versions/1'
val_path = os.path.join(dataset_path, 'val2017')

if not os.path.exists(val_path):
    raise FileNotFoundError(f"Could not find images at {val_path}. Contents: {os.listdir(dataset_path)}")

# Image data generator to load and rescale images
train_datagen = ImageDataGenerator(rescale=1./255)
train = train_datagen.flow_from_directory(
    val_path,
    target_size=(256, 256),
    batch_size=560,
    class_mode=None,
    shuffle=True
)
print(f"Successfully loaded {train.samples} images")

# Convert RGB images to LAB color space and prepare inputs/outputs
X = []
Y = []
for img in train[0]:
    lab = rgb2lab(img)
    X.append(lab[:, :, 0])          # L channel (lightness)
    Y.append(lab[:, :, 1:] / 128)   # AB channels normalized to [-1, 1]

X = np.array(X)
Y = np.array(Y)
X = X.reshape(X.shape + (1,))  # add channel dimension for CNN

print("X shape:", X.shape)
print("Y shape:", Y.shape)

# Define the model architecture
model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2, input_shape=(256, 256, 1)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same', strides=2))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(512, (3,3), activation='relu', padding='same'))
model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
model.add(UpSampling2D((2, 2)))
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
model.summary()
model_history = model.fit(X, Y, validation_split=0.1, epochs=5, batch_size=16)

# Plot accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
""")
