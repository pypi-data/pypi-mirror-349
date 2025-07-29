def run():
    print("""
This is experiment 4 Apply transfer learning for dog breed identification dataset
Experiment 4
!pip install kagglehub
import kagglehub
path = kagglehub.dataset_download("bhuviranga/mini-dog-breed-identification")
print("Path to dataset files:", path)
import os
dataset_path = '/root/.cache/kagglehub/datasets/bhuviranga/mini-dog-breed-identification/versions/1'
dataset_files = os.listdir(dataset_path)
print("Files in the dataset:", dataset_files)
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image_dataset_from_directory
from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout

dog_breed_data_path = os.path.join(dataset_path, 'Mini Dog Breed Data')
train_dir = dog_breed_data_path
val_dir = dog_breed_data_path

train_dataset = image_dataset_from_directory(train_dir, image_size=(128, 128), batch_size=32)
val_dataset = image_dataset_from_directory(val_dir, image_size=(128, 128), batch_size=32)
class_names = train_dataset.class_names
print("\nClass names:", class_names)
normalization_layer = keras.layers.Rescaling(1./255)
train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
vgg_base.trainable = False
model = Sequential([
    vgg_base,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(class_names), activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
logs = model.fit(train_dataset, epochs=5, validation_data=val_dataset)

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.plot(logs.history['accuracy'], label='Train Acc')
plt.plot(logs.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(logs.history['loss'], label='Train Loss')
plt.plot(logs.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.legend()
plt.tight_layout()
plt.show()

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

y_true = []
y_pred = []
for images, labels in val_dataset:
    preds = model.predict(images)
    y_pred.extend(np.argmax(preds, axis=1))
    y_true.extend(labels.numpy())
y_true = np.array(y_true)
y_pred = np.array(y_pred)
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix for Dog Breed Classification")
plt.show()

          """)
