# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# CS 440
#
# **************************************************************************** #

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
# Node and RenderTree for making and displaying trees
#from anytree import Node, RenderTree, AsciiStyle
#from anytree.dotexport import RenderTreeGraph


# Task 1  **********************************************************************

def checkArgv(argv):
	for validArgv in ['5','7','9','11']:
		if argv[1] == validArgv:
			return True
	
	return False


def makeMatrix(size):
	
	n = int(size)
	
	# makes n by n matrix
	matrix = np.zeros( shape=(n,n) )
	visitMat = np.zeros( shape=(n,n) )
	
	# populates n by n matrix
	for row in range(n):
		for col in range(n):
			Max = max(n-1-row,row-n-1,n-1-col,col-n-1)
			if Max == 0:
				matrix[row,col] = 0
			else:
				matrix[row,col] = random.randint(1,Max)
	
	# display n by n matrix
	print(matrix)
	return matrix, visitMat


# Task 2  **********************************************************************

class Node(object):
	def __init__(self,row,col,data):
		self.row = row
		self.col = col
		self.data = data
		self.children = []
	
	def add_child(self,obj):
		self.children.append(obj)


def buildTree(matrix,visitMat,size):
	n = int(size)
	
	curr_row = 0
	curr_col = 0
	root = Node(curr_row,curr_col,matrix[curr_row,curr_col])
	visitMat[curr_row,curr_col] = 1
	
	#while(True):
		# check if legal move and has not been visited
	
	#print("\n",RenderTree(root, style=AsciiStyle()))
	#RenderTreeGraph(root).to_dotfile("tree.dot")
	# run to convert .dot to .pdf
	# $ dot -Tpdf tree.dot -o tree.pdf


def evalMatrix(matrix,visitMat):
	pass # code


# Main  ************************************************************************
def main(argv):
	# Task 1
	matrix,visitMat = makeMatrix(argv[1])
	
	# Task 2
	Tree = buildTree(matrix,visitMat,argv[1])
	evalMatrix(matrix,visitMat)


# run main module if not imported
if __name__ == "__main__":
	if checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11]")
	
	else:
		main(sys.argv)
