def run():
    print("""
This is experiment 9 Perform audio event classification with transfer learning
import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models

# === Feature Extraction Function ===
def extract_mel_spectrogram(file_path, max_pad_len=128):
    try:
        audio, sample_rate = librosa.load(file_path, sr=22050)
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sample_rate)
        log_mel_spec = librosa.power_to_db(mel_spec)
        if log_mel_spec.shape[1] < max_pad_len:
            pad_width = max_pad_len - log_mel_spec.shape[1]
            log_mel_spec = np.pad(log_mel_spec, pad_width=((0, 0), (0, pad_width)))
        else:
            log_mel_spec = log_mel_spec[:, :max_pad_len]
        return log_mel_spec
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# === Dataset Preparation ===
data_dir = 'UrbanSound8K/audio/fold1/'
labels_map = {'air_conditioner': 0, 'car_horn': 1, 'children_playing': 2, 'dog_bark': 3,
              'drilling': 4, 'engine_idling': 5, 'gun_shot': 6, 'jackhammer': 7, 'siren': 8, 'street_music': 9}

X, y = [], []
for file in os.listdir(data_dir):
    if file.endswith(".wav"):
        label = int(file.split('-')[1])
        spec = extract_mel_spectrogram(os.path.join(data_dir, file))
        if spec is not None:
            X.append(spec)
            y.append(label)

X = np.array(X)[..., np.newaxis]
y = to_categorical(y, num_classes=10)

# === Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)

# === Transfer Learning Model ===
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
model = models.Sequential([
    layers.Conv2D(3, (3, 3), padding='same', input_shape=X_train.shape[1:]),
    base_model,
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# === Model Training ===
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))


          """)
