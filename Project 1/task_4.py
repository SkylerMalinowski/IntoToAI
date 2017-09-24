# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# CS 440
# **************************************************************************** #

# Import other Tasks
import task_1 as T1
import task_2 as T2
import task_3 as T3
# Sys and Opt for CLI arguments and flags
import sys, getopt
# NumPy for math functions and data structures
import numpy as np
# Random for random numbers
import random
# AnyTree to make and display Trees
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
# Regular Expression for string parsing
import re
# MatPlotLib for graphibg
import matplotlib.pyplot as plt
# Time for stopwatch
import time

'''
# Task 1  **********************************************************************
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


# Generate Node name from location data
def encodeName(row,col):
	name = '(' + str(row) + ',' + str(col) + ')'
	return name


# Deconstruct Node name for location data
def decodeName(node):
	name = node.name
	digits = re.findall('\d+',name)
	return int(digits[0]),int(digits[1])


# Return a list of valid moves from given location
def validMoves(matrix,visitMat,row,col):
	valid_list = []
	jump = int(matrix[row,col])

	# Right
	test = int(col + jump)
	if test < len(matrix) and visitMat[row,test] == 0:
		valid_list.append( [row,test] )

	# Down
	test = row + jump
	if test < len(matrix) and visitMat[test,col] == 0:
		valid_list.append( [test,col] )

	# Left
	test = col - jump
	if test >= 0 and visitMat[row,test] == 0:
		valid_list.append( [row,test] )

	# Up
	test = row - jump
	if test >= 0 and visitMat[test,col] == 0:
		valid_list.append( [test,col] )

	# debug
	#print(valid_list)

	return valid_list


# BFS algorithm to generate a tree solution to the matrix
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

	#fileName += '.png'
	#print(RenderTree(root, style=AsciiStyle()).by_attr())
	#RenderTreeGraph(root).to_picture(fileName)

	return k,root


# Task 3  **********************************************************************
def hillClimb(matrix,fileName='tree',row=0,col=0):
	n = len(matrix)
	new_matrix = np.copy(matrix)

	rand_row = random.randint(0,n-1)
	rand_col = random.randint(0,n-1)

	while(rand_row is not 0 and rand_col is not 0 or rand_row is not n-1 and rand_col is not n-1):
		rand_row = random.randint(0,n-1)
		rand_col = random.randint(0,n-1)

	Max = max(n-1-rand_row,rand_row-n-1,n-1-rand_col,rand_col-n-1)
	new_matrix[rand_row,rand_col] = random.randint(1,Max)

	k1,root1 = evaluate(new_matrix,fileName,row,col)
	k2,root2 = evaluate(matrix,fileName,row,col)

	# debug
	#print('Matrix 1:')
	#print(mat)
	#print('Value Function 1 =',k1)
	#print('Matrix 2:')
	#print(new_mat)
	#print('Value Function 2 =',k2)

	#fileName += '.png'
	if k1 > k2:
		#RenderTreeGraph(root1).to_picture(fileName)
		return new_matrix,k1,root1
	else:
		#RenderTreeGraph(root2).to_picture(fileName)
		return matrix,k2,root2

'''

# Task 4  **********************************************************************
def collectData(matrix,argv1,argv2,fileName='task_4'):
	n = len(matrix)
	N = int(argv1) * int(argv2)
	restarts = int(argv1)
	sub_iterations = int(argv2)

	t = [0,0]
	k = 0

	best_k = 0
	best_root = Node('None')
	best_matrix = np.copy(matrix)

	x = np.arange(N)
	y = []

	t[0] = time.time()
	for re in range(restarts):
		row = random.randint(0,n-1)
		col = random.randint(0,n-1)
		for i in range(sub_iterations):
			matrix,k,root = T3.hillClimb(matrix,fileName+'_S'+str(n),row,col)
			if re == 0:
				best_k = k
				best_root = root
				best_matrix = matrix
			elif k > best_k:
				best_k = k
				best_root = root
				best_matrix = matrix
			y.append(best_k)
	plt.plot(x,y)
	t[1] = time.time()

	RenderTreeGraph(best_root).to_picture(fileName+'_S'+str(n)+'.png')
	T2.dumpFile(best_matrix,fileName+'_S'+str(n))

	# debug
	print('Hill Climb with Random Restarts - Final',str(n),'by',str(n),"Matrix:")
	print(best_matrix)
	print("Evaluation Function =",best_k)
	print("Elapsed Computational Time =",t[1]-t[0],"sec")
	print('')

	# debug
	plt.title(str(n)+' by '+str(n))
	plt.legend(['Hill Climb with Random Restarts'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	plt.show()


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of restarts
	# argv[2] = number of iterations per restart

	for arg in [5,7,9,11]:
		matrix = T1.makeMatrix(arg)
		collectData(matrix,argv[1],argv[2],'T4_RR')


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
