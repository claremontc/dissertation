# python/anomaly_detection/anomaly_detection.py
import tensorflow as tf
import numpy as np
from process_and_normalize import normalized_data

input_dim = normalized_data.shape[1] 

autoencoder = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_dim,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(input_dim, activation='sigmoid')
])

autoencoder.compile(optimizer='adam', loss='mse')

autoencoder.fit(normalized_data, normalized_data, epochs=50, batch_size=32)

