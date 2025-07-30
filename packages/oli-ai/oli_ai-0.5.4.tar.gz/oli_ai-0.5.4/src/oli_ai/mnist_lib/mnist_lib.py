from keras.datasets import mnist
from matplotlib import pyplot as plt
import numpy as np
from numpy import dot
from numpy.linalg import norm


def plot_img(image):
    image = image.reshape((28, 28))
    plt.imshow(image, cmap='gray')
    plt.show()


def plot_imgs_labels(imgs, labels, rows=2, cols=5):
    figure = plt.figure(figsize=(10, 3))
    # plotting images from the training set
    for i in range(0, rows*cols):
        plt.subplot(rows, cols, i+1)
        plt.subplots_adjust(hspace=1, wspace=1)
        plt.title(f"Label: {labels[i]}")
        img = imgs[i].reshape((28, 28))
        plt.imshow(img, cmap='gray')       
        # Rimuovere le indicazioni numeriche dagli assi
        plt.xticks([])
        plt.yticks([])

def plot_imgs(imgs, labels, rows=2, cols=5):
    figure = plt.figure(figsize=(10, 3))
    # plotting images from the training set
    for i in range(0, rows*cols):
        plt.subplot(rows, cols, i+1)
        plt.subplots_adjust(hspace=1, wspace=1)
        #plt.title(f"Label: {labels[i]}")
        img = imgs[i].reshape((28, 28))
        plt.imshow(img, cmap='gray')
        
        # Rimuovere le indicazioni numeriche dagli assi
        plt.xticks([])
        plt.yticks([])



def predict(model,image):
  image = image.reshape(1, 28, 28)  # Aggiungi dimensione batch
  prediction = model.predict(image)
  #print(f"Raw prediction: {prediction}")  # [0.01, 0.02, 0.95, 0.01, ...]
  # Classe predetta
  predicted_class = np.argmax(prediction)
  return predicted_class


# Funzione per visualizzare i pesi
def visualize_weights(weights, title):
   normalized_weights = (weights - np.min(weights)) / (np.max(weights) - np.min(weights))
   
   fig, axes = plt.subplots(1, 10, figsize=(15, 2))  # Altezza dimezzata
   
   for i in range(10):
       axes[i].imshow(normalized_weights[:, i].reshape(28, 28), cmap='gray')
       axes[i].axis('off')
       axes[i].set_title(f'{i}', fontsize=6)  # Font più piccolo
   
   fig.suptitle(title, fontsize=10, y=0.95)  # Titolo più piccolo
   plt.subplots_adjust(top=0.65, bottom=0.02, hspace=0, wspace=0.05)  # Margini ultra-mini
   plt.show()
