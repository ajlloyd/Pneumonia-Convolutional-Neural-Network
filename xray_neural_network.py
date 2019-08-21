import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
import pickle
import time

NAME = "Pneumonia-vs-unaffected-64x2-{}".format(int(time.time()))
tensorboard = TensorBoard(log_dir=".\logs\\".format(NAME))


test_data = pickle.load(open("testing_data.pickle", "rb"))
training_data = pickle.load(open("training_data.pickle", "rb"))
validation_data = pickle.load(open("validation_data.pickle", "rb"))

def create_X_and_y(data):
    X = []
    y = []
    for features, labels in data[0]:
        X.append(features)
        y.append(labels)
    X = np.array(X).reshape(-1,100,100,1)                                       # len dataset(600) // pixels_dim1(100) // pixels_dim2(100) // colour_numbers(1)
    y = np.array(y)
    return X,y

X_test, y_test = create_X_and_y(test_data)
X_train, y_train = create_X_and_y(training_data)
X_val, y_val = create_X_and_y(validation_data)

X_train = tf.keras.utils.normalize(X_train, axis=1)

model = Sequential()
# Layer 1:
model.add(Conv2D(64, (3,3), padding="same", activation="relu", input_shape = X_train.shape[1:]))
model.add(MaxPooling2D(pool_size=(2,2)))
# Layer 2:
model.add(Conv2D(64, (3,3), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
# Layer 3:
model.add(Flatten())
model.add(Dense(1, activation="sigmoid"))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=30, epochs=5, validation_split=0.2, callbacks=[tensorboard])
