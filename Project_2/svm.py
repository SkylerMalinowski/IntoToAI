# svm.py
# -------------

from sklearn import svm
import numpy as np
import math
# svm implementation
import util
PRINT = True

class SVMClassifier:
	"""
	svm classifier
	"""
	def __init__(self, legalLabels):
		self.legalLabels = legalLabels
		self.type = "svm"

	def train(self, trainingData, trainingLabels, validationData, validationLabels):
		self.features = svm.SVC()
		data = self.convert(trainingData)
		self.features.fit(data,trainingLabels)
		self.features.score(data,trainingLabels)

	def classify(self, data):
		guesses = []
		data = self.convert(data)
		predicted = self.features.predict(data)
		for prediction in predicted:
			guesses.append(prediction)
		return guesses

	def convert(self, data):
		total_matrix = []
		for picture in data:
			keys = np.array(picture.keys())
			vals = np.array(picture.values())
			n = int(math.sqrt(len(keys)))
			vals = np.reshape(vals,(n,n))
			matrix = np.zeros(shape=(n,n),dtype=np.int)
			for x,y in keys:
				matrix[x][y] = vals[x][y]
			total_matrix.append(np.reshape(matrix,len(keys)))
		return total_matrix
