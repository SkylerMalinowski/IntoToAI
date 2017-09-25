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
import task_4 as T4
# Sys and Opt for CLI arguments and flags
import sys, getopt, os
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


# Task 5 ***********************************************************************
def hillClimb_random_walk(matrix,p,fileName='tree',row=0,col=0):
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

	k1,root1 = T3.evaluate(new_matrix,fileName,row,col)
	k2,root2 = T3.evaluate(matrix,fileName,row,col)

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
	else:  # Random Walk
		#RenderTreeGraph(root2).to_picture(fileName)
		if(random.random() <= p):  # Random Walk
			#RenderTreeGraph(root2).to_picture(fileName)
			return new_matrix,k1,root1
		else:
			return matrix,k2,root2


def collectData(matrix,argv1,argv2,fileName='task_5'):
	n = len(matrix)
	N = int(argv1)
	p = float(argv2)

	t = [0,0]
	k = 0

	best_k = 0
	best_root = Node('None')
	best_matrix = []

	x = np.arange(N)
	y = np.zeros(N)

	t[0] = time.time()
	for i in range(N):
		matrix,k,root = hillClimb_random_walk(matrix,p,fileName+'_S'+str(n))
		if i == 0 or k > best_k:
			best_k = k
			best_root = root
			best_matrix = matrix
		y[i] = k
	plt.plot(x,y)
	t[1] = time.time()

	#print(RenderTree(best_root, style=AsciiStyle()).by_attr())
	sum = 0
	fileRoot = fileName+'_n'+str(n)+'_k'
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
					RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(n)+'_k'+str(best_k)+'.png')
					T2.dumpFile(best_matrix,fileName+'_n'+str(n)+'_k'+str(best_k))
	else:
		RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(n)+'_k'+str(best_k)+'.png')
		T2.dumpFile(best_matrix,fileName+'_n'+str(n)+'_k'+str(best_k))

	# debug
	print('Hill Climb with Random Walk - Final',str(n),'by',str(n),"Matrix:")
	print(best_matrix)
	print("Evaluation Function =",best_k)
	print("Elapsed Computational Time =",t[1]-t[0],"sec")
	print('')

	# debug
	plt.title(str(n)+' by '+str(n))
	plt.legend(['Hill Climb with Random Walk'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	plt.savefig(fileName+'_fig_n'+str(n)+'.png')
	plt.show()


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of iterations
	# argv[2] = threshold probability on [0 -> hill climb, 1 -> with random walk]

	for arg in [5,7,9,11]:
		matrix = T1.makeMatrix(arg)
		collectData(matrix,argv[1],argv[2],'T5_RW')


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
