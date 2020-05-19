# -*- coding: utf-8 -*-
"""LogisticRegression.ipynb

Author: Vignesha Jayakumar Copyright. 2020
Credits: Mark Jay, Tech with Tim

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GoSSJHVEnHMDgveYxhXHhFAPl_cPCIqG
All rights reserved Copyright. 2020 Vignesha Jayakumar
"""

import seaborn as sns
import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import time, random
from sklearn.model_selection import train_test_split
import cv2
import imutils
import os
from PIL import Image
from glob import glob
from contourFinder import ContourFinder

tf.compat.v1.disable_eager_execution()


(x_train, y_train), (xt, yt) = tf.keras.datasets.mnist.load_data()

cf = ContourFinder()
x_test, y_test = cf.find_contours()

fig, axes = plt.subplots(1, 4, figsize=(7, 3))
for img, label, ax in zip(x_train[:4],y_train[:4], axes):
    ax.set_title(label)
    ax.imshow(img)
    ax.axis('off')
plt.show()

x_train = x_train.reshape(x_train.shape[0],784) / 255
x_test = x_test.reshape(x_test.shape[0],784) / 255
print(f"XTRAIN:{x_train.shape}, XTEST:{x_test.shape}")

with tf.compat.v1.Session() as sess:
  y_train = sess.run(tf.one_hot(y_train, 10))
  y_test = sess.run(tf.one_hot(y_test, 10))

learning_rate = 0.01
epochs = 50
batch_size = 200
batches = int(x_train.shape[0] / batch_size)

X = tf.compat.v1.placeholder(tf.float32, [None, 784])
Y = tf.compat.v1.placeholder(tf.float32, [None, 10])

#print(type(0.1 * np.random.randn(784,10).astype('float32')))
W = tf.Variable(0.1 * np.random.randn(784,10).astype('float32'), name = "weights")
B = tf.Variable(0.1 * np.random.randn(10).astype('float32'), name = "bias")

pred = tf.nn.softmax(tf.add(tf.matmul(X, W), B))
cost = tf.reduce_mean(-tf.reduce_sum(Y* tf.compat.v1.log(pred), axis = 1))
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate).minimize(cost)

with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())
    for epoch in range(epochs):
        for i in range(batches):
          offset = i * epoch
          x = x_train[offset: offset + batch_size]
          y = y_train[offset: offset + batch_size]
          sess.run(optimizer, feed_dict={X: x, Y:y})
          sess.run(cost, feed_dict={X:x,Y:y})

        if not epoch % 10:
            w = sess.run(W)
            b= sess.run(B)
            print(f'epoch:{epoch}, cost:{cost}, weight:{w}, bias:{b}')

    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    acc = accuracy.eval({X:x_test,Y:y_test})
    print(acc)

    fig, axes = plt.subplots(1, 25, figsize=(8, 4))
    for img, ax in zip(x_test, axes):
        guess = np.argmax(sess.run(pred, feed_dict={X: [img]}))
        ax.set_title(guess)
        ax.imshow(img.reshape((28, 28)))
        ax.axis('off')
plt.show()
