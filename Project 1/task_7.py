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
import task_8 as T8
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
def genetic_step(population,s,fileName='T7_GA',row=0,col=0):
	#for y in population:
		#print(y)
	p = len(population)
	n = len(population[0])
	k = np.zeros(p)
	root = [None]*p
	best_k = 0
	best_pop = None
	best_root = None
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i],fileName)
		# if(k[i] < 0):
		# 	#print("shit puzzle detected ********************")
		# 	k[i] = k[i]
		while(k[i]< 0):
			print("")
			population[i] = T1.makeMatrix(n)
			k[i],root[i] = T3.evaluate(population[i],fileName)
		if(k[i] >= best_k):
			best_k = k[i]
			best_pop = population[i]
	t = int(sum(k))
	reproductive_strength = []
	for l in range(p):
			for z in range(int(k[l])):
				reproductive_strength.append(l)
	print("k map", k)
	print("population schema", reproductive_strength)
	#print("t",t)
	survivor_values = random.sample(range(0, t), 2)
	#print(survivor_values)
	survivor = [None,None]
	#print(survivor)
	survivor[0] = population[reproductive_strength[survivor_values[0]]]
	survivor[1] = population[reproductive_strength[survivor_values[1]]]
	print("survivors", survivor)
	swapping_rows = [[0,0]]*s
	print(swapping_rows)
	for iter in range(s):
		swapping_rows_1 = random.sample(range(0, n), 2)
		while(swapping_rows_1[0] in swapping_rows[iter] or swapping_rows_1[1] in swapping_rows[iter]):
			swapping_rows_1 = random.sample(range(0, n), 2)
		swapping_rows[iter] = swapping_rows_1
	for x in range(s):
		side_of_swap = [random.randint(0,1),random.randint(0,1)]
		print("swapping rows ", swapping_rows)
		print("on sides", side_of_swap)
		i = int((float(n)/2 - .5))
		print(i)
		if n-1 in swapping_rows[x]:
			if side_of_swap[0] == side_of_swap[1] == 1:
				#worry about goal
				survivor[0][swapping_rows[x][0]][i+1:n-1],survivor[1][swapping_rows[x][1]][i+1:n-1] = survivor[1][swapping_rows[x][1]][i+1:n-1],survivor[0][swapping_rows[x][0]][i+1:n-1]
			elif side_of_swap[0] == side_of_swap[1] == 0:
				#dont worry about goal
				survivor[0][0:i],survivor[1][0:i] = survivor[1][0:i],survivor[0][0:i]
			else:
				rev1,rev2 = survivor[1][swapping_rows[x][1]][::-1],survivor[0][swapping_rows[x][0]][::-1]
				if(swapping_rows[1]==n-1):
					survivor[0][swapping_rows[x][0]][0:i],survivor[1][swapping_rows[x][1]][i+1:n-1] = rev1[i+1:n],rev2[1:i]
				else:
					survivor[1][swapping_rows[x][1]][0:i],survivor[0][swapping_rows[x][0]][i+1:n-1] = rev2[i+1:n],rev1[1:i]
		else:
			if side_of_swap[0] == side_of_swap[1] == 1:
				survivor[0][swapping_rows[x][0]][i+1:n],survivor[1][swapping_rows[x][1]][i+1:n] = survivor[1][swapping_rows[x][1]][i+1:n],survivor[0][swapping_rows[x][0]][i+1:n]
			elif side_of_swap[0] == side_of_swap[1] == 0:
				survivor[0][0:i],survivor[1][0:i] = survivor[1][0:i],survivor[0][0:i]
			else:
				rev1,rev2 = survivor[1][swapping_rows[x][1]][::-1],survivor[0][swapping_rows[x][0]][::-1]
				#print(rev1,rev2)
				survivor[0][swapping_rows[x][0]][0:i],survivor[1][swapping_rows[x][1]][i+1:n] = rev1[i+1:n],rev2[0:i]
		survivor[0][i],survivor[1][i] = survivor[1][i],survivor[0][i]
	#print("survivors offspring",survivor)
	population[0] = survivor[0]
	population[1] = survivor[1]
	population[2] = best_pop
	for i in range(p):
		population[i],k[i],root[i] = T5.hillClimb_random_walk(population[i],1)
		population[i],k[i],root[i] = T5.hillClimb_random_walk(population[i],1)
		print(population[i])
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i])
		# while(k[i]< 0):
		# 	print(population[i],"died at birth")
		# 	population[i] = T1.makeMatrix(n)
		# 	k[i],root[i] = T3.evaluate(population[i],fileName)

	# goal_row = n-1
	# goal_col = n-1
	return population,k,root

def collectData(population,argv1,argv2,fileName='T7_GA'):
	n = len(population[0])
	p = len(population)
	N = int(argv1)
	s = int(argv2)

	t = [0,0]
	k = np.zeros(p)

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

	#print(RenderTree(best_root,style=AsciiStyle()).by_attr())
	T8.saveBest(best_matrix,best_k,best_root)
	#T8.saveBest(best_matrix,best_k,best_root,fileName)

	print('Population Based Approach - Final',str(n),'by',str(n),"Matrix:")
	print(best_matrix)
	print("Evaluation Function =",best_k)
	print("Elapsed Computational Time =",t[1]-t[0],"sec")
	print('')

	plt.title(str(n)+' by '+str(n))
	plt.legend(['Population Based Approach'])
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
		collectData(population,argv[1],argv[2])


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
