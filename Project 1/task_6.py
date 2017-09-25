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
import task_5 as T5
# Sys and Opt for CLI arguments and flags
import sys, getopt, os
# NumPy for math functions and data structures
import numpy as np
# Random for random numbers
import math
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


# Task 6 ***********************************************************************
def hillClimb_simulated_annealing(matrix,T,fileName='task_6',row=0,col=0):
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

	x = float(random.random())

	try:
		y = math.exp((k1-k2)/T)
	except (OverflowError):
		y = 0

	if k1 >= k2:  # Hill Climb
		return new_matrix,k1,root1,T
	elif(x <= y):  # Random Walk
		return new_matrix,k1,root1,T
	else:
		return matrix,k2,root2,T


def collectData(matrix,argv1,argv2,argv3,fileName='task_6'):
	n = len(matrix)
	N = int(argv1)
	T = int(argv2)
	d = float(argv3)

	t = [0,0]

	k = 0
	matrix = np.copy(matrix)

	best_k = 0
	best_root = Node('None')
	best_matrix = []

	x = np.arange(N)
	y = np.zeros(N)

	t[0] = time.time()

	for i in range(N):
		matrix,k,root,T = hillClimb_simulated_annealing(matrix,T,fileName+'_'+str(n))
		if i == 0 or k > best_k:
			best_k = k
			best_root = root
			best_matrix = matrix
		T = d*T
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

	print('Hill Climb with Simulated Annealing - Final',str(n),'by',str(n),"Matrix:")
	print(best_matrix)
	print("Evaluation Function =",best_k)
	print("Elapsed Computational Time =",t[1]-t[0],"sec")
	print('')

	plt.title(str(n)+' by '+str(n))
	plt.legend(['Hill Climb with Simulated Annealing'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	plt.savefig(fileName+'_fig_n'+str(n)+'.png')
	plt.show()


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of iterations
	# argv[2] = initial Temperature
    # argv[3] = temp decay on [0,1]

	for arg in [5,7,9,11]:
		matrix = T1.makeMatrix(arg)
		collectData(matrix,argv[1],argv[2],argv[3],'T6_SA')

# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
