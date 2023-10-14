import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()

print(X_train.shape)
print(y_train.shape)

plt.imshow(X_train[17], cmap='binary')
plt.axis('off')
print(y_train[12])
