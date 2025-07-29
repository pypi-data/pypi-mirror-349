def run():
    print("""
This is experiment 7 Create document summaries using transfer learning
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.layers import Input, Dense, Embedding, MultiHeadAttention, LayerNormalization, Dropout, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.tokenize import sent_tokenize
import re

nltk.download('punkt')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

def load_imdb_data():
    imdb, info = tfds.load('imdb_reviews', with_info=True, as_supervised=True)

    # Prepare the dataset
    train_data = imdb['train']
    train_sentences, train_labels = [], []

    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    return train_sentences, train_labels

def summarize_document(document, model, tokenizer, max_len, top_n=3):
    sentences = sent_tokenize(document)
    sequence_data = tokenizer.texts_to_sequences(sentences)
    padded_sequences = pad_sequences(sequence_data, maxlen=max_len, padding='post')

    # Predict scores for each sentence
    predictions = model.predict(padded_sequences)

    # Get top_n sentences based on predicted scores
    sentence_scores = [(index, score) for index, score in enumerate(predictions)]
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:top_n]

    summary = [sentences[i] for i, _ in top_sentences]
    return ' '.join(summary)

# Load IMDB data
train_sentences, train_labels = load_imdb_data()

# Define parameters
max_len = 100
embedding_dim = 128
max_words = 10000

# Tokenizer for Keras
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)

# Prepare training data
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')

# Build and train the model
model = tf.keras.Sequential([
tf.keras.layers.Embedding(max_words, embedding_dim, input_length=max_len),
tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
tf.keras.layers.GlobalAveragePooling1D(),
tf.keras.layers.Dense(24, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
num_epochs = 5
model.fit(train_padded, np.array(train_labels), epochs=num_epochs, validation_split=0.2)

# Save the trained model
model.save("/content/drive/MyDrive/Temp/imdb_model.h5")

imdb_model = tf.keras.models.load_model('/content/drive/MyDrive/Temp/imdb_model.h5')

for layer in imdb_model.layers:
    layer.trainable = False

max_length = 100
input_shape = (max_length,)
inputs = tf.keras.Input(shape=input_shape)

x = imdb_model(inputs)

x = tf.keras.layers.Dense(64, activation='relu')(x)
x = tf.keras.layers.Dense(32, activation='relu')(x)
x = tf.keras.layers.Dense(1, activation='sigmoid')(x)

summarization_model = tf.keras.Model(inputs=inputs, outputs=x)

summarization_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

summarization_model.summary()

# Example document for summarization with more sentences
example_document = (
  "This movie was fantastic! I loved the plot and the acting was superb. "
  "However, I felt that the ending was a bit rushed. The cinematography was stunning, "
  "and the music added a wonderful depth to the scenes. The character development was rich, "
  "and I appreciated how the film tackled complex themes. I found myself emotionally invested "
  "in the characters and their journeys. There were moments of humor that broke the tension, "
  "which I enjoyed. Overall, it was an enjoyable experience, but it could have been more impactful "
  "if the pacing had been better. I would recommend this film to anyone who loves a good story. "
  "It provided a perfect mix of humor and drama, and I think it will resonate well with many audiences. "
  "The performances were not only entertaining but also very moving, capturing the essence of the story."
)

summary = summarize_document(example_document, model, tokenizer, max_len)

print("Summary:")
print(summary)

 """)
