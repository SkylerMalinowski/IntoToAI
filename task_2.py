# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 1
# CS 440
# **************************************************************************** #


# task_1.py modules
import task_1

# Sys and Opt for CLI arguments and flags
import sys, getopt
# NumPy for math functions and data structures
import numpy as np
# Random for random numbers
import random
# AnyTree to make and display Trees
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
# RE for string parsing
import re


# ******************************************************************************
class Queue():
	def __init__(self):
		self.items = []
	
	def isEmpty(self):
		return self.items == []
	
	def enqueue(self, item):
		self.items.insert(0,item)
	
	def dequeue(self):
		return self.items.pop()
	
	def size(self):
		return len(self.items)


def encodeName(row,col):
	name = '(' + str(row) + ',' + str(col) + ')'
	return name


def decodeName(node):
	name = node.name
	digits = re.findall('\d+',name)
	return int(digits[0]),int(digits[1])


def validMoves(matrix,visitMat,row,col):
	valid_list = []
	jump = int(matrix[row,col])
	
	test = int(col + jump)
	if test < len(matrix) and visitMat[row,test] == 0:  # Right
		valid_list.append( [row,test] )
	
	test = row + jump
	if test < len(matrix) and visitMat[test,col] == 0:  # Down
		valid_list.append( [test,col] )
	
	test = col - jump
	if test >= 0 and visitMat[row,test] == 0:  # Left
		valid_list.append( [row,test] )
	
	test = row - jump
	if test >= 0 and visitMat[test,col] == 0:  # Up
		valid_list.append( [test,col] )
	
	# debug
	#print(valid_list)
	
	return valid_list


# BFS algorithm
def evaluate(matrix,fileName='tree',row=0,col=0):
	fileName = fileName + '.png'
	n = len(matrix)
	
	visitMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat = np.zeros( shape=(n,n),dtype=np.int )
	evalMat.fill(-1)
	Q = Queue()
	
	root = Node(encodeName(row,col))  # root tree node
	Q.enqueue(root)
	
	while( Q.isEmpty() == False ):
		node = Q.dequeue()
		
		row,col = decodeName(node)
		visitMat[row,col] = 1
		evalMat[row,col] = node.depth
		valid_moves = validMoves(matrix,visitMat,row,col)
		
		for child in valid_moves:
			new_node = Node(encodeName(child[0],child[1]),parent=node)
			Q.enqueue( new_node )
			visitMat[child[0],child[1]] = 1
			evalMat[child[0],child[1]] = new_node.depth
	
	k = 0
	if evalMat[n-1,n-1] is not -1:
		k = evalMat[n-1,n-1]
	else:
		k = - (evalMat == -1).sum()
	
	#debug
	#print('visitMat:')
	#print(visitMat)
	print('evalMat:')
	print(evalMat)
	#print(RenderTree(tree, style=AsciiStyle()).by_attr())
	RenderTreeGraph(root).to_picture(fileName)
	print('Value Function =',k)
	
	return k


# Main  ************************************************************************
def main(argv):
	matrix = task_1.makeMatrix(argv[1])
	k = evaluate(matrix,'task_2')


# run main module if not imported
if __name__ == "__main__":
	if task_1.checkArgv(sys.argv) == False:
		print("arguement error: not in domain [5,7,9,11]")
	else:
		main(sys.argv)
