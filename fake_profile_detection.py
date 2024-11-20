# -*- coding: utf-8 -*-
"""Fake Profile Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aszXkhp4xwqwv1EwiKi1XKImkYTdcGbT
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# Load datasets
df_users = pd.read_csv("users.csv")
df_fakeusers = pd.read_csv("fakeusers.csv")

# Add `isFake` column
df_users["isFake"] = 0  # Not fake
df_fakeusers["isFake"] = 1  # Fake

# Combine datasets
df_allUsers = pd.concat([df_users, df_fakeusers], ignore_index=True)

# Shuffle the data
df_allUsers = df_allUsers.sample(frac=1).reset_index(drop=True)

# Select features and target
features = [
    "statuses_count", "followers_count", "friends_count",
    "favourites_count", "listed_count", "geo_enabled",
    "profile_use_background_image", "lang"
]
df_allUsers["lang"] = df_allUsers["lang"].astype("category").cat.codes  # Encode categorical data
X = df_allUsers[features].fillna(0)  # Replace missing values
Y = df_allUsers["isFake"]

"""# **Dataset Split**"""

# Split data
train_X, test_X, train_y, test_y = train_test_split(X, Y, test_size=0.2, random_state=0)
train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size=0.2, random_state=0)

"""# **Compilation of ANN Model**"""

# Initialize the model
model = Sequential()

# Add layers
model.add(Dense(32, activation='relu', input_dim=train_X.shape[1]))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Output layer for binary classification

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Display model summary
model.summary()

"""# **Train the Model**"""

# Train the model
history = model.fit(
    train_X, train_y,
    validation_data=(val_X, val_y),
    epochs=50,  # You can adjust this number
    batch_size=32,
    verbose=2
)

"""# **Evaluation of Model**"""

# Evaluate the model
loss, accuracy = model.evaluate(test_X, test_y, verbose=0)
print(f"Test Accuracy: {accuracy:.2f}")

"""# **Loading the Model**"""

# Save model
model.save("fake_real_profile_model.h5")

# Load model
from keras.models import load_model
loaded_model = load_model("fake_real_profile_model.h5")

"""# **Visualization of Training process**"""

import matplotlib.pyplot as plt

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()