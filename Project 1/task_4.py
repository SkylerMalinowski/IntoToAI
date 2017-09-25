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
	best_matrix = []

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

	#print(RenderTree(best_root, style=AsciiStyle()).by_attr())
	RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(n)+'_k'+str(best_k)+'.png')
	T2.dumpFile(best_matrix,fileName+'_n'+str(n)+'_k'+str(best_k))

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
	plt.savefig(fileName+'_fig_n'+str(n)+'.png')
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
