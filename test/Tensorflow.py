import numpy as np
import matplotlib.pyplot as plt
from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader
from tensorflow.keras.datasets import mnist

# Überprüfen der tflite_model_maker-Version
import tflite_model_maker
print("tflite_model_maker-Version:", tflite_model_maker.__version__)

# Laden des MNIST-Datensets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Konvertieren des MNIST-Datensets in RGB-Bilder
def convert_to_rgb(images):
    return np.stack((images,)*3, axis=-1)

x_train_rgb = convert_to_rgb(x_train)
x_test_rgb = convert_to_rgb(x_test)

# Normalisieren der Bilder
x_train_rgb = x_train_rgb / 255.0
x_test_rgb = x_test_rgb / 255.0

# Umwandeln der Daten in das erwartete Format für DataLoader
train_data = DataLoader.from_array(x_train_rgb, y_train)
test_data = DataLoader.from_array(x_test_rgb, y_test)

# Erstellen und Trainieren des Modells
model = image_classifier.create(train_data, epochs=5)

# Evaluieren des Modells
loss, accuracy = model.evaluate(test_data)
print(f'\nTest accuracy: {accuracy}')

# Vorhersagen mit dem Modell
predictions = model.predict_top_k(test_data, k=1)

# Eine Grafik mit matplotlib erstellen
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_test[i], cmap=plt.cm.binary)
    predicted_label = predictions[i][0].id
    true_label = y_test[i]
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel(f"{predicted_label} ({true_label})", color=color)
plt.show()
