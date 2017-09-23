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
# MatPlotLib for graphibg
import matplotlib.pyplot as plt
# Time for stopwatch
import time


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
	
	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)
	
	# debug
	#print('matrix:')
	#print(matrix)
	
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
	
	#debug
	#print('visitMat:')
	#print(visitMat)
	#print('evalMat:')
	#print(evalMat)
	#print('Value Function =',k)
	
	#fileName = fileName + '.png'
	#print(RenderTree(root, style=AsciiStyle()).by_attr())
	#RenderTreeGraph(root).to_picture(fileName)
	
	return k,root


# Task 3  **********************************************************************
def perturbate(mat,fileName='tree'):
	n = len(mat)
	new_mat = np.copy(mat)
	
	row = random.randint(0,n-1)
	col = random.randint(0,n-1)
	
	while(row is not 0 and col is not 0 or row is not n-1 and col is not n-1):
		row = random.randint(0,n-1)
		col = random.randint(0,n-1)
	
	Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
	new_mat[row,col] = random.randint(1,Max)
	
	k1,root1 = evaluate(new_mat,fileName)
	k2,root2 = evaluate(mat,fileName)
	
	# debug
	#print('Matrix 1:')
	#print(mat)
	#print('Value Function 1 =',k1)
	#print('Matrix 2:')
	#print(new_mat)
	#print('Value Function 2 =',k2)
	
	fileName += '.png'
	if k1 > k2:
		RenderTreeGraph(root1).to_picture(fileName)
		return new_mat,k1
	else:
		RenderTreeGraph(root2).to_picture(fileName)
		return mat,k2


def collectData(size,fileName='tree'):
	n = int(size)
	
	t = [0,0]
	total_t = 0
	k = 0
	
	x = np.arange(n)
	y = np.zeros(n,dtype=np.int)
	
	for arg in [5,7,9,11]:
		matrix = makeMatrix(arg)
		t[0] = time.time()
		for i in range(int(n)):
			matrix,k = perturbate(matrix,fileName+'_'+str(arg))
			y[i] = k
		t[1] = time.time()
		total_t += t[1]-t[0]
		
		plt.plot(x,y)
		
		# debug
		print('Final',arg,'by',arg,"Matrix:")
		print(matrix)
		print("Evaluation Function =",k)
		print("Elapsed Computational Time =",t[1]-t[0],"sec")
	
	# debug
	plt.legend(['5-by-5','7-by-7','9-by-9','11-by-11'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	print("\n","Total Elapsed Computational Time =",total_t,"sec")
	plt.show()


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of iterations of hill climbing
	
	collectData(argv[1],'task_3')


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
