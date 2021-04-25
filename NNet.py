import tensorflow as tf
import numpy as np

optimus_prime = tf.keras.optimizers.Adam(learning_rate = 0.001)

def init_nnet():
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(10,)))
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dense(5, activation='sigmoid'))
    model.compile(optimizer=optimus_prime, loss='mae')
    return model

def train_nnet(nnet, x, y):
    new_nnet = tf.keras.models.clone_model(nnet)
    new_nnet.compile(optimizer=optimus_prime, loss='mae')
    new_nnet.fit(x, y, epochs = 50, verbose = 2)
    return new_nnet
