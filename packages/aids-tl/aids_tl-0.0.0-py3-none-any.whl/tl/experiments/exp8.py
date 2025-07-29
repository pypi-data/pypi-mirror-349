def run():
    print("""
This is experiment 8 Build multiclass classification with CNN model
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2

# 1. Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Resize images from 32x32 to 224x224 for VGG16
x_train_resized = np.array([cv2.resize(img, (224, 224)) for img in x_train])
x_test_resized = np.array([cv2.resize(img, (224, 224)) for img in x_test])

# Preprocess input for VGG16
x_train_preprocessed = preprocess_input(x_train_resized.astype('float32'))
x_test_preprocessed = preprocess_input(x_test_resized.astype('float32'))

# One-hot encode the labels
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# 2. Load VGG16 base model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze the convolutional base

# 3. Build the model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dense(10, activation='softmax')
])

# 4. Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 5. Train the model
model.fit(x_train_preprocessed, y_train_cat, epochs=5, validation_split=0.1, batch_size=32)

# 6. Evaluate the model
loss, accuracy = model.evaluate(x_test_preprocessed, y_test_cat)
print(f"Test Accuracy on CIFAR-10 with VGG16: {accuracy:.4f}")

          """)
