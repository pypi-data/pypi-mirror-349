def run():
    print("""
This is experiment 5 Build review sentiment classifier using transfer learning
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
from gensim.models import Word2Vec
import re

# Clean text
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower()

# Load IMDB dataset
def load_imdb_data():
    imdb = tfds.load('imdb_reviews', as_supervised=True)
    train_data = imdb['train']
    test_data = imdb['test']

    train_sentences, train_labels = [], []
    for sentence, label in tfds.as_numpy(train_data):
        train_sentences.append(clean_text(sentence.decode('utf-8')))
        train_labels.append(int(label))

    test_sentences, test_labels = [], []
    for sentence, label in tfds.as_numpy(test_data):
        test_sentences.append(clean_text(sentence.decode('utf-8')))
        test_labels.append(int(label))

    return train_sentences, train_labels, test_sentences, test_labels

# Load and preprocess data
train_sentences, train_labels, test_sentences, test_labels = load_imdb_data()

max_len = 100
embedding_dim = 128
max_words = 10000

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

tokenized = [s.split() for s in train_sentences]
w2v_model = Word2Vec(sentences=tokenized, vector_size=embedding_dim, window=5, min_count=1, sg=0)

embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    if i < max_words and word in w2v_model.wv:
        embedding_matrix[i] = w2v_model.wv[word]

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=max_len, padding='post')
train_labels = np.array(train_labels)

# Define model
model = Sequential([
    Embedding(max_words, embedding_dim, embeddings_initializer=Constant(embedding_matrix),
              input_length=max_len, trainable=False),
    Bidirectional(LSTM(64, return_sequences=True)),
    GlobalMaxPooling1D(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
X_train, X_val, y_train, y_val = train_test_split(train_padded, train_labels, test_size=0.2, random_state=42)
model.fit(X_train, y_train, epochs=2, batch_size=128, validation_data=(X_val, y_val), verbose=1)

# Evaluate
test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=max_len, padding='post')
y_pred = (model.predict(test_padded) > 0.5).astype("int32")
print(classification_report(test_labels, y_pred))

          """)
