"""
File name: q_learning_model.py
Author(s): Liam Lawless
Date created: November 29, 2023
Last modified: November 29, 2023

Description:

Dependencies:

"""

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
import random
from collections import deque
import numpy as np

def build_q_network(state_size, action_size, learning_rate=0.001):
    model = Sequential([
        Dense(24, input_dim=state_size, activation='relu'),
        Dense(24, activation='relu'),
        Dense(action_size, activation='linear')
    ])
    model.compile(loss='mse', optimizer=tf.keras.optimizers.legacy.Adam(learning_rate))
    return model

def train_q_network(model, replay_buffer, batch_size, discount_factor):
    minibatch = replay_buffer.sample(batch_size)
    for state, action, reward, next_state, done in minibatch:
        # Reshape state and next_state for neural network input
        state = np.expand_dims(state, axis=0)
        state = state.reshape(-1, 4)  # Reshape state to 2D with second dimension as 4
        next_state = np.expand_dims(next_state, axis=0)

        target = reward
        if not done:
            target = reward + discount_factor * np.amax(model.predict(next_state)[0])

        target_f = model.predict(state)
        target_f = target_f.flatten()  # Flatten to a 1D array
        target_f[action] = target
        target_f = target_f.reshape(1, -1)  # Reshape back to (1, 4) for fitting the model
        model.fit(state, target_f, epochs=1, verbose=0)




class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)