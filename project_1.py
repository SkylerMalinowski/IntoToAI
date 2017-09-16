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
# MatPlotLib for graphibg
import matplotlib.pyplot as plt
# Math for math functions
import math
# Random for random numbers
import random
# AnyTree to make and display Trees
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
# RE for string parsing
import re

import collections


# Task 1  **********************************************************************
def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	
	return False


def makeMatrix(size):
	
	n = int(size)
	
	# makes n by n matrix
	matrix = np.zeros( shape=(n,n),dtype=np.int )
	visitMat = np.zeros( shape=(n,n),dtype=np.int )
	
	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)
	
	# debug
	#matrix = np.matrix([ [2,2,2,4,3], [2,2,3,3,3], [3,3,2,3,3], [4,3,2,2,2], [1,2,1,4,0] ])
	#matrix = np.matrix([ [3,3,2,4,3], [2,2,2,1,1], [4,3,1,3,4], [2,3,1,1,3], [1,1,3,2,0] ])
	print('Matrix:')
	print(matrix)
	
	return matrix, visitMat


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
def evaluate(matrix,visitMat,size,row,col):
	n = int(size)
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
	if evalMat[n-1,n-1] is not -1:
		k = evalMat[n-1,n-1]
	else:
		k = - (evalMat == -1).sum()
	
	
	#debug
	#print('visitMat:')
	#print(visitMat)
	print('evalMat:')
	print(evalMat)
	#print(RenderTree(tree, style=AsciiStyle()).by_attr())
	RenderTreeGraph(root).to_picture("tree.png")
	print('Value Function =',k)
	
	return root,evalMat,k


# Main  ************************************************************************
def main(argv):
	# Task 1
	matrix,visitMat = makeMatrix(argv[1])
	
	# Task 2
	tree,evalMat,k = evaluate(matrix,visitMat,argv[1],0,0)
	
	# Task 3
	pass # code


# run main module if not imported
if __name__ == "__main__":
	
	if checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11]")
	
	else:
		main(sys.argv)
