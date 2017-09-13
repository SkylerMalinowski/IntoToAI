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

# Task 1
def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	
	return False
			
# Task 1
def makeMatrix(size):
	
	n = int(size)
	
	# makes n by n matrix
	matrix = np.zeros( shape=(n,n) )
	
	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			matrix[row,col] = random.randint(1,n-1)
	
	matrix[n-1,n-1] = 0  # goal
	
	# display n by n matrix
	print matrix

# Task 2
def validMove():
	pass

# Task 2
def evalMatrix():
	pass # code

# main
def main(argv):
	# Task 1
	makeMatrix(argv[1])
	
	# Task 2
	evalMatrix()
	
# run main module if not imported
if __name__ == "__main__":
	if checkArgv(sys.argv) == False:
		print "arguement error: not in domain [5,7,9,11]"
	
	else:
		main(sys.argv)
