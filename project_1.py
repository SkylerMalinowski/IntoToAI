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

# Task 1  **********************************************************************

def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	
	return False


def makeMatrix(size):
	
	n = int(size)
	
	# makes n by n matrix
	matrix = np.zeros( shape=(n,n) )
	visitMat = np.zeros( shape=(n,n) )
	
	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)
	
	# debug
	print(matrix)
	
	return matrix, visitMat


# Task 2  **********************************************************************

# Tree
class Node(object):
	def __init__(self,row,col,data):
		self.name = "(" + str(row) + "," + str(col) + ")"
		self.row = row
		self.col = col
		self.data = data
		self.items = []
	
	def __repr__(self):
		return self.name
	
	def add_child(self,obj):
		self.items.append(obj)
	
	def get_name(self):
		return self.name
	
	def get_children(self):
		return self.items


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


def printTree(root,lv=0):
	print( lv * '  ', root.get_name() )
	
	children = root.get_children()
	lv += 1
	
	for child in children:
		printTree(child,lv)


def validMoves(matrix,visitMat,curr):
	valid_list = []
	
	test = int(curr[1] + curr[2])
	if test < len(matrix) and visitMat[curr[0],test] == 0:  # Right
		valid_list.append([ curr[0],test,matrix[curr[0],test] ])
	
	test = int(curr[0] + curr[2])
	if test < len(matrix) and visitMat[test,curr[1]] == 0:  # Down
		valid_list.append([ test,curr[1],matrix[test,curr[1]] ])
	
	test = int(curr[1] - curr[2])
	if test >= 0 and visitMat[test,curr[0]] == 0:  # Left
		valid_list.append([ curr[0],test,matrix[curr[0],test] ])
	
	test = int(curr[0] - curr[2])
	if test >= 0 and visitMat[test,curr[1]] == 0:  # Up
		valid_list.append([ test,curr[1],matrix[test,curr[1]] ])
	
	# debug
	#print(valid_list)
	
	return valid_list


def buildTree(matrix,visitMat,size,row,col):
	n = int(size)
	Q = Queue()
	
	root = Node(row,col,matrix[row,col])  # root tree node
	Q.enqueue([row,col,matrix[row,col]])  # row,col,jump
	visitMat[row,col] = 1
	
	curr_data = None  # current node data
	curr_node = root
	while( Q.isEmpty() == False ):
		prev_data = curr_data  # previous node data
		prev_node = curr_node
		curr_data = Q.dequeue()
		
		# check valid for children (move,visit)
		valid_moves = validMoves(matrix,visitMat,curr_data)
		
		# tree,queue,visit
		for child in valid_moves:
			curr_node = Node(child[0],child[1],child[2])
			prev_node.add_child(curr_node)
			Q.enqueue(child)
			visitMat[child[0],child[1]] = 1
	
	# debug
	#printTree(root)
	#print(visitMat)
	
	return root


def evalMatrix(matrix,visitMat):
	pass # code


# Main  ************************************************************************
def main(argv):
	# Task 1
	matrix,visitMat = makeMatrix(argv[1])
	
	# Task 2
	tree = buildTree(matrix,visitMat,argv[1],0,0)
	evalMatrix(matrix,visitMat)


# run main module if not imported
if __name__ == "__main__":
	if checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11]")
	
	else:
		main(sys.argv)
