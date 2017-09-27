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
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i],fileName)
		# if(k[i] < 0):
		# 	#print("shit puzzle detected ********************")
		# 	k[i] = k[i]
		while(k[i]< 0):
			population[i] = T1.makeMatrix(n)
			k[i],root[i] = T3.evaluate(population[i],fileName)
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

	for x in range(s):
		swapping_row = random.randint(0,n-1)
		side_of_swap = random.randint(0,1)
		i = int((float(n)/2 - .5))
		print(i)
		if n-1 == swapping_row:
			if side_of_swap == 1:
				#worry about goal
				survivor[0][swapping_row][i+1:n-1],survivor[1][swapping_row][i+1:n-1] = survivor[1][swapping_row][i+1:n-1],survivor[0][swapping_row][i+1:n-1]
			else:
				#dont worry about goal
				survivor[0][swapping_row][0:i],survivor[1][swapping_row][0:i] = survivor[1][swapping_row][0:i],survivor[0][swapping_row][0:i]
		else:
			if side_of_swap == 1:
				survivor[0][swapping_row][i+1:n],survivor[1][swapping_row][i+1:n] = survivor[1][swapping_row][i+1:n],survivor[0][swapping_row][i+1:n]
			else:
				survivor[0][swapping_row][0:i],survivor[1][swapping_row][0:i] = survivor[1][swapping_row][0:i],survivor[0][swapping_row][0:i]

		survivor[0][swapping_row][i],survivor[1][swapping_row][i] = survivor[1][swapping_row][i],survivor[0][swapping_row][i]
	#
	population[0] = survivor[0]
	population[1] = survivor[1]
	population[2] = T1.makeMatrix(n)
	for i in range(p):
		population[i],k[i],root[i] = T5.hillClimb_random_walk(population[i],1)
		population[i],k[i],root[i] = T5.hillClimb_random_walk(population[i],1)
	for i in range(p):
		k[i],root[i] = T3.evaluate(population[i])

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

	T8.saveBest(best_matrix,best_k,best_root)
	T8.saveBest(best_matrix,best_k,best_root,fileName)

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

	for arg in [5,7,9,11]:
		population = []
		for p in range(3):
			matrix = T1.makeMatrix(arg)
			population.append(matrix)
		collectData(population,argv[1],argv[2])


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
