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


# Task 1  **********************************************************************
def makeMatrix(size):
	n = int(size)
	matrix = np.zeros( shape=(n,n),dtype=np.int )

	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)

	return matrix


# Main  ************************************************************************
def main(argv):
	# argv[1] = n, matrix side dimension

	matrix = makeMatrix(argv[1])
	print('matrix:')
	print(matrix)


# run main module if not imported
if __name__ == "__main__":
	main(sys.argv)
