# mlp.py
# -------------

# mlp implementation


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random
import util
import math
import numpy as np


import argparse
import sys

#from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

PRINT = True

class MLPClassifier:
	"""
	mlp classifier
	"""
	def __init__(self, legalLabels, max_iterations):
		self.legalLabels = legalLabels
		self.type = "mlp"
		self.max_iterations = max_iterations
		self.x = tf.placeholder(tf.float32, [None, 784])
		self.W = tf.Variable(tf.zeros([784, 10]))
		self.b = tf.Variable(tf.zeros([10]))
		#self.y = tf.matmul(self.x, self.W) + self.b
		self.y_ = tf.placeholder(tf.float32, [None, 10])

		self.W_conv1 = self.weight_variable([5, 5, 1, 32])
		self.b_conv1 = self.bias_variable([32])
		self.x_image = tf.reshape(self.x, [-1, 28, 28, 1])
		self.h_conv1 = tf.nn.relu(self.conv2d(self.x_image, self.W_conv1) + self.b_conv1)
		self.h_pool1 = self.max_pool_2x2(self.h_conv1)

		self.W_conv2 = self.weight_variable([5, 5, 32, 64])
		self.b_conv2 = self.bias_variable([64])
		self.h_conv2 = tf.nn.relu(self.conv2d(self.h_pool1, self.W_conv2) + self.b_conv2)
		self.h_pool2 = self.max_pool_2x2(self.h_conv2)

		self.W_fc1 = self.weight_variable([7 * 7 * 64, 1024])
		self.b_fc1 = self.bias_variable([1024])

		self.h_pool2_flat = tf.reshape(self.h_pool2, [-1, 7*7*64])
		self.h_fc1 = tf.nn.relu(tf.matmul(self.h_pool2_flat, self.W_fc1) + self.b_fc1)

		self.keep_prob = tf.placeholder(tf.float32)
		self.h_fc1_drop = tf.nn.dropout(self.h_fc1, self.keep_prob)

		self.W_fc2 = self.weight_variable([1024, 10])
		self.b_fc2 = self.bias_variable([10])

		self.y_conv = tf.matmul(self.h_fc1_drop, self.W_fc2) + self.b_fc2

		self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y_conv))
		self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
		#self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(self.cross_entropy)
		self.correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.y_, 1))
		self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))

		self.sess = tf.InteractiveSession()
		self.sess.run(tf.global_variables_initializer())
		#self.sess = tf.InteractiveSession()

	def train(self, trainingData, trainingLabels, validationData, validationLabels):
		input_set = self.convertInputs(trainingData)
		output_set = self.convertOutputs(trainingLabels)
		validationData_set = self.convertInputs(validationData)
		validationLabels_set = self.convertOutputs(validationLabels)
		for iteration in range(self.max_iterations):
			print("Starting iteration", iteration, "...")
			self.sess.run(self.train_step, feed_dict={self.x: input_set, self.y_: output_set, self.keep_prob: 0.5})
		correct_prediction = tf.equal(tf.argmax(self.y_conv, 1), tf.argmax(self.y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
		#print('test accuracy', self.sess.run(accuracy, feed_dict={self.x:validationData_set, self.y_:validationLabels_set, self.keep_prob: 1.0}))

	def convertInputs(self, input_data):
		input_set = []
		for i in range(len(input_data)):
			input_list = np.array(input_data[i].values())
			input_set.append(list(input_list))
		return input_set

	def convertOutputs(self, output_data):
		output_set = []
		for i in range(len(output_data)):
			output = np.zeros(10)
			output[output_data[i]] = 1.
			output_set.append(output)
		return output_set

	def classify(self, data):
		input_set = self.convertInputs(data)
		guesses = []
		prediction = tf.argmax(self.y_conv, 1)
		guess = tf.Print(prediction, [prediction])
		#print(self.sess.run(guess,feed_dict={self.x:input_set}))
		return self.sess.run(guess,feed_dict={self.x:input_set, self.keep_prob: 1.0})

	def weight_variable(self, shape):
		initial = tf.truncated_normal(shape, stddev=0.1)
		return tf.Variable(initial)

	def bias_variable(self, shape):
		initial = tf.constant(0.1, shape=shape)
		return tf.Variable(initial)

	def conv2d(self, x, W):
		return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

	def max_pool_2x2(self, x):
		return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1], padding='SAME')
