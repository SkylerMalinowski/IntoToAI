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
import sys, getopt
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
def genetic_step(population,s,fileName='task_7',row=0,col=0):
	#for y in population:
		#print(y)
	p = len(population)
	n = len(population[0])
	k = np.zeros(p)
	root = [None]*p
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i],fileName)
		if(k[i] < 0):
			while(k[i]< 0):
				population[i] = T1.makeMatrix(n)
				k[i],root[i] = T3.evaluate(population[i],fileName)
	t=int(sum(k))
	reproductive_strength = []
	for l in range(p):
		for z in range(int(k[l])):
			reproductive_strength.append(l)

	#print("population schema", reproductive_strength)
	#print("t",t)
	survivor_values = random.sample(range(0, abs(t)), 2)
	#print(survivor_values)
	survivor = [None,None]
	#print(survivor)
	survivor[0] = population[reproductive_strength[survivor_values[0]]]
	survivor[1] = population[reproductive_strength[survivor_values[1]]]
	#print("survivors", survivor)
	for x in range(s):
		swapping_rows = random.sample(range(0, n), 2)
		if n-1 in swapping_rows:
			for h in range(1,n-1):
				survivor[0][swapping_rows[0]][h],survivor[1][swapping_rows[1]][h] = survivor[1][swapping_rows[1]][h],survivor[0][swapping_rows[0]][h]
		else:
			survivor[0][swapping_rows[0]],survivor[1][swapping_rows[1]] = survivor[1][swapping_rows[1]],survivor[0][swapping_rows[0]]
	#print("survivors offspring",survivor)
	population[0] = survivor[0]
	population[1] = survivor[1]
	population[2] = T1.makeMatrix(n)
	for mut in population:
		T5.hillClimb_random_walk(mut,1)
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i])


	# goal_row = n-1
	# goal_col = n-1
	return population,k,root

def collectData(population,argv1,argv2,fileName='task_7'):
	n = len(population[0])
	p = len(population)
	N = int(argv1)
	s = int(argv2)

	t = [0,0]

	k = np.zeros(p)
	#matrix = np.copy(matrix)

	best_k = 0
	best_root = Node('None')
	best_matrix = []

	x = np.arange(N)
	y = np.zeros(N)

	t[0] = time.time()
	#print("initial T")
	#print(T)
	for i in range(N):
		population,k,root = genetic_step(population,s,fileName+'_'+str(n))
		for j in range(p):
			if i == 0:
				best_k = k[j]
				best_root = root[j]
				best_matrix = population[j]
			if k[j] > best_k:
				best_k = k[j]
				best_root = root[j]
				best_matrix = population[j]
			y[i] = k[j]
	plt.plot(x,y)
	t[1] = time.time()

	#print(RenderTree(best_root, style=AsciiStyle()).by_attr())
	RenderTreeGraph(best_root).to_picture(fileName+'_n'+str(n)+'_k'+str(best_k)+'.png')
	T2.dumpFile(best_matrix,fileName+'_n'+str(n)+'_k'+str(best_k))

	# debug
	print('Hill Climb with population based approach - Final',str(n),'by',str(n),"Matrix:")
	print(best_matrix)
	print("Evaluation Function =",best_k)
	print("Elapsed Computational Time =",t[1]-t[0],"sec")
	print('')

	# debug
	plt.title(str(n)+' by '+str(n))
	plt.legend(['Hill Climb with population based approach'])
	plt.xlabel('Iteration (i)')
	plt.ylabel('Evaluation Function Value (k)')
	plt.savefig(fileName+'_fig_n'+str(n)+'.png')
	plt.show()


# Main  ************************************************************************
def main(argv):
	# argv[1] = number of iterations
	# argv[2] = number of chromesomes swapped per genetic step
    # argv[3] = population size

	for arg in [5,7,9,11]:
		population = []
		for p in range(int(argv[3])):
			matrix = T1.makeMatrix(arg)
			population.append(matrix)
		collectData(population,argv[1],argv[2],'T7_PA')

# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
