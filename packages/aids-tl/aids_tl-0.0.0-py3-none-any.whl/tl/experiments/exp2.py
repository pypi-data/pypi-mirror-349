def run():
    print("""
This is experiment 2 Implement transfer learning with pre-trained CNN model
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import cv2
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = np.stack([cv2.resize(img, (224, 224)) for img in x_train])
x_test = np.stack([cv2.resize(img, (224, 224)) for img in x_test])
x_train = np.repeat(x_train[..., np.newaxis], 3, -1)
x_test = np.repeat(x_test[..., np.newaxis], 3, -1)

x_train = preprocess_input(x_train.astype('float32'))
x_test = preprocess_input(x_test.astype('float32'))

y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# Evaluate
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy with ResNet50: {acc:.4f}")
          
if vgg16 having use this
          
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input 
# Use previously preprocessed x_train, x_test, y_train, y_test

# Build VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base

model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# Evaluate
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy with VGG16: {acc:.4f}")
"""
)
