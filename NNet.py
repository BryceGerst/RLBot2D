import tensorflow as tf
import numpy as np

def init_nnet():
    optimus_prime = tf.keras.optimizers.Adam(learning_rate = 0.4)
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(10,)))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(16))
    model.add(tf.keras.layers.Dense(5, activation='sigmoid'))
    model.compile(optimizer=optimus_prime, loss='mse')
    return model
