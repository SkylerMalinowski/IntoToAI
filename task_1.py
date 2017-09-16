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


# ******************************************************************************
def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	
	return False


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
	#matrix = np.matrix([ [2,2,2,4,3], [2,2,3,3,3], [3,3,2,3,3], [4,3,2,2,2], [1,2,1,4,0] ])
	#matrix = np.matrix([ [3,3,2,4,3], [2,2,2,1,1], [4,3,1,3,4], [2,3,1,1,3], [1,1,3,2,0] ])
	print('matrix:')
	print(matrix)
	
	return matrix


# Main  ************************************************************************
def main(argv):
	matrix = makeMatrix(argv[1])


# run main module if not imported
if __name__ == "__main__":
	if checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11]")
	else:
		main(sys.argv)
