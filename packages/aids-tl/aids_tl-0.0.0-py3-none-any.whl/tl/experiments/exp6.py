def run():
    print("""
This is experiment 6 Apply transfer learning for IMDB dataset with word embeddings
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, GlobalMaxPooling1D, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.initializers import Constant
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
import os
import zipfile
import requests

# Clean text
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower()

# Load IMDB dataset
def load_imdb_data():
    imdb = tfds.load('imdb_reviews', as_supervised=True)
    train_data, test_data = imdb['train'], imdb['test']

    train_sentences, train_labels = [], []
    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    test_sentences, test_labels = [], []
    for sentence, label in tfds.as_numpy(test_data):
        test_sentences.append(clean_text(sentence.decode('utf-8')))
        test_labels.append(int(label))

    return train_sentences, train_labels, test_sentences, test_labels

# Download and load GloVe
def load_glove_embeddings(glove_path='glove.6B.100d.txt', embedding_dim=100):
    if not os.path.exists(glove_path):
        # Download GloVe
        url = 'http://nlp.stanford.edu/data/glove.6B.zip'
        r = requests.get(url)
        with open('glove.6B.zip', 'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile('glove.6B.zip', 'r') as zip_ref:
            zip_ref.extractall()

    embeddings_index = {}
    with open(glove_path, encoding='utf-8') as f:
        for line in f:
            values = line.strip().split()
            word = values[0]
            coeffs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coeffs
    return embeddings_index

# Parameters
max_len = 100
embedding_dim = 100
max_words = 10000

# Load and tokenize data
train_sentences, train_labels, test_sentences, test_labels = load_imdb_data()
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

train_seq = tokenizer.texts_to_sequences(train_sentences)
test_seq = tokenizer.texts_to_sequences(test_sentences)

train_pad = pad_sequences(train_seq, maxlen=max_len, padding='post')
test_pad = pad_sequences(test_seq, maxlen=max_len, padding='post')
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

# Load pretrained GloVe embeddings
embeddings_index = load_glove_embeddings()
embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    if i < max_words and word in embeddings_index:
        embedding_matrix[i] = embeddings_index[word]

# Build model using pretrained embeddings
model = Sequential([
    Embedding(max_words, embedding_dim,
              embeddings_initializer=Constant(embedding_matrix),
              input_length=max_len, trainable=False),
    Bidirectional(LSTM(64, return_sequences=True)),
    GlobalMaxPooling1D(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
X_train, X_val, y_train, y_val = train_test_split(train_pad, train_labels, test_size=0.2, random_state=42)
model.fit(X_train, y_train, epochs=2, batch_size=128, validation_data=(X_val, y_val), verbose=1)

# Evaluate
y_pred = (model.predict(test_pad) > 0.5).astype("int32")
print(classification_report(test_labels, y_pred))
          """)
