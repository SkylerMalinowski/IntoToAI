# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# CS 440
# **************************************************************************** #


# Sys and Opt for CLI arguments and flags
import sys, getopt
# NumPy for math functions and data structures
import numpy as np
# Random for random numbers
import random
# AnyTree to make and display Trees
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
# RE for string parsing
import re


# Task 1  **********************************************************************
def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	if '.txt' in argv[1]:
		return True
	return False

def fileParse(fileName):
	file = open(fileName,'r')
	data = file.readline()
	data = data.split()
	matrix = []

	if len(data) > 1:
		data = [int(i) for i in line.split()]
		matrix.append(data)

	for line in file:
		data = [int(i) for i in line.split()]
		matrix.append(data)
	file.close()

	npMatrix = np.array(matrix)

	#debug
	print('matrix:')
	print(npMatrix)

	return npMatrix


def makeMatrix(size):

	n = int(size)

	# makes n by n matrix
	matrix = np.zeros( shape=(n,n),dtype=np.int )

	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)

	# debug
	print('matrix:')
	print(matrix)

	return matrix


# Task 2  **********************************************************************
class Queue():
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def enqueue(self, item):
		self.items.insert(0,item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)


def encodeName(row,col):
	name = '(' + str(row) + ',' + str(col) + ')'
	return name


def decodeName(node):
	name = node.name
	digits = re.findall('\d+',name)
	return int(digits[0]),int(digits[1])


def validMoves(matrix,visitMat,row,col):
	valid_list = []
	jump = int(matrix[row,col])

	test = int(col + jump)
	if test < len(matrix) and visitMat[row,test] == 0:  # Right
		valid_list.append( [row,test] )

	test = row + jump
	if test < len(matrix) and visitMat[test,col] == 0:  # Down
		valid_list.append( [test,col] )

	test = col - jump
	if test >= 0 and visitMat[row,test] == 0:  # Left
		valid_list.append( [row,test] )

	test = row - jump
	if test >= 0 and visitMat[test,col] == 0:  # Up
		valid_list.append( [test,col] )

	# debug
	#print(valid_list)

	return valid_list


# BFS algorithm
def evaluate(matrix,fileName='tree',row=0,col=0):
	fileName = fileName + '.png'
	n = len(matrix)

	visitMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat.fill(-1)
	Q = Queue()

	root = Node(encodeName(row,col))  # root tree node
	Q.enqueue(root)

	while( Q.isEmpty() == False ):
		node = Q.dequeue()

		row,col = decodeName(node)
		visitMat[row,col] = 1
		evalMat[row,col] = node.depth
		valid_moves = validMoves(matrix,visitMat,row,col)

		for child in valid_moves:
			new_node = Node(encodeName(child[0],child[1]),parent=node)
			Q.enqueue( new_node )
			visitMat[child[0],child[1]] = 1
			evalMat[child[0],child[1]] = new_node.depth

	k = 0
	if evalMat[n-1,n-1] == -1:
		k = - (evalMat == -1).sum()
	else:
		k = evalMat[n-1,n-1]

	# debug
	#print('visitMat:')
	#print(visitMat)
	print('evalMat:')
	print(evalMat)
	print('Value Function =',k)

	#print(RenderTree(root, style=AsciiStyle()).by_attr())
	RenderTreeGraph(root).to_picture(fileName)

	return k


# Main  ************************************************************************
def main(argv):
	# argv[1] = n, matrix side dimension || inout file name

	if '.txt' in argv[1]:
		matrix = fileParse(argv[1])
	else:
		matrix = makeMatrix(argv[1])
	k = evaluate(matrix,'task_2')


# run main module if not imported
if __name__ == "__main__":
	if checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11] or a file")
	else:
		main(sys.argv)
