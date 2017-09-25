# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# CS 440
# **************************************************************************** #


# Import other Tasks
import task_1 as T1
import task_2 as T2
# Sys and Opt for CLI arguments and flags
import sys, getopt, os
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


# Task 2  **********************************************************************
# BFS algorithm
def evaluate(matrix,fileName='tree',row=0,col=0):
	n = len(matrix)

	visitMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat.fill(-1)
	Q = T2.Queue()

	root = Node(T2.encodeName(row,col))  # root tree node
	Q.enqueue(root)

	while( Q.isEmpty() == False ):
		node = Q.dequeue()

		row,col = T2.decodeName(node)
		visitMat[row,col] = 1
		evalMat[row,col] = node.depth
		valid_moves = T2.validMoves(matrix,visitMat,row,col)

		for child in valid_moves:
			new_node = Node(T2.encodeName(child[0],child[1]),parent=node)
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
def hillClimb(matrix,fileName='task_3',row=0,col=0):
	n = len(matrix)
	new_matrix = np.copy(matrix)

	goal_row = n-1
	goal_col = n-1

	rand_row = random.randint(0,n-1)
	rand_col = random.randint(0,n-1)

	while(rand_row == goal_row and rand_col == goal_col):
		rand_row = random.randint(0,n-1)
		rand_col = random.randint(0,n-1)

	Max = max(abs(n-1-rand_row),abs(rand_row-n-1),abs(n-1-rand_col),abs(rand_col-n-1))

	old_val = matrix[rand_row,rand_col]
	while( new_matrix[rand_row,rand_col] == old_val):
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
	if k1 >= k2:
		#RenderTreeGraph(root1).to_picture(fileName)
		return new_matrix,k1,root1
	else:
		#RenderTreeGraph(root2).to_picture(fileName)
		return matrix,k2,root2


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of iterations of hill climbing

	fileName = 'T3_HC'
	N = int(argv[1])

	t = [0,0]
	k = 0

	best_k = 0
	best_root = Node('None')
	best_matrix = []

	x = np.arange(N)
	y = np.zeros(N,dtype=np.int)

	for arg in [5,7,9,11]:
		matrix = T1.makeMatrix(arg)
		t[0] = time.time()
		for i in range(N):
			matrix,k,root = hillClimb(matrix,fileName+'_S'+str(arg))
			if i == 0 or k > best_k:
				best_k = k
				best_root = root
				best_matrix = matrix
			y[i] = k
		t[1] = time.time()

		plt.plot(x,y)

		#print(RenderTree(best_root, style=AsciiStyle()).by_attr())
		sum = 0
		fileRoot = fileName+'_n'+str(arg)+'_k'
		for file in os.listdir():
			if file.find(fileRoot) is not -1:
				sum += 1
		if sum > 0:
			for file in os.listdir():
				if file.find(fileRoot) is not -1:
					file_k = file.split('_k',1)
					file_k = file_k[1]
					file_k = int(file_k[:-4])
					if k > file_k:
						os.remove(file)
						RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(arg)+'_k'+str(best_k)+'.png')
						T2.dumpFile(best_matrix,fileName+'_n'+str(arg)+'_k'+str(best_k))
		else:
			RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(arg)+'_k'+str(best_k)+'.png')
			T2.dumpFile(best_matrix,fileName+'_n'+str(arg)+'_k'+str(best_k))

		# debug
		print('Final',arg,'by',arg,"Matrix:")
		print(matrix)
		print("Evaluation Function =",k)
		print("Elapsed Computational Time =",t[1]-t[0],"sec")

	# debug
	plt.legend(['5-by-5','7-by-7','9-by-9','11-by-11'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	plt.savefig(fileName+'_fig'+'.png')
	plt.show()


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
