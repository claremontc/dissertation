import joblib
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils import class_weight


X_train, X_test, y_train, y_test = joblib.load('preprocessed_data.pkl')

input_dim = X_train.shape[1]
classes = np.array([0, 1])


weights = class_weight.compute_class_weight('balanced', classes=classes, y=y_train)
print(weights)


autoencoder = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(input_dim,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(input_dim, activation='sigmoid')
])


autoencoder.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())


history = autoencoder.fit(
    X_train,
    X_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=2
)


reconstructed = autoencoder.predict(X_test)


mse = np.mean(np.power(X_test - reconstructed, 2), axis=1)


plt.hist(mse, bins=50, alpha=0.75, color='blue')
plt.title('Reconstruction Error Distribution')
plt.xlabel('Reconstruction Error')
plt.ylabel('Frequency')
plt.savefig('reconstruction_plot.png')


threshold = np.mean(mse) + 2 * np.std(mse)
print(f"Anomaly detection threshold: {threshold}")


anomalies = mse > threshold
print(f"Number of anomalies detected: {np.sum(anomalies)}")


plt.scatter(range(len(mse)), mse, c=anomalies, cmap='coolwarm', alpha=0.6)
plt.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
plt.title('Anomaly Detection')
plt.xlabel('Sample Index')
plt.ylabel('Reconstruction Error')
plt.legend()
plt.savefig('anomaly_detection_plot.png')


if y_test is not None:
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, anomalies))

    print("Classification Report:")
    print(classification_report(y_test, anomalies))
