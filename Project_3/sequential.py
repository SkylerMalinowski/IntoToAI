# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import sys, glob, os
import math
import time
import heapq
import operator
import xlsxwriter

import numpy as np

import IO


# class  ***********************************************************************
class cell:

	def __init__( self, row, col, parent=None ):
		self.parent = parent
		self.where = (row,col)
		self.f = 0.
		self.g = 0.
		self.h = 0.


class sequential:
	
	def __init__( self, world, weight=[1.,1.] ):
		self.world = world
		self.length = [len(world),len(world[0])]
		self.goal = None
		self.nodes_expanded = []
		self.nodes_considered = []
		self.pathList = []
		self.openList = []
		self.closedList = []
		self.found = []
		self.g = 0
		for i in range(5):
			self.nodes_expanded.append(0)
			self.nodes_considered.append(0)
			self.openList.append([])
			self.closedList.append([])
			self.found.append(False)
		self.w = weight
		while( len(self.openList) == 5 and self.goal == None ):
			for row in range(self.length[0]):
				for col in range(self.length[1]):
					if( world[row][col] == 's' ):
						for i in range(len(self.openList)):
							self.openList[i].append(cell(row,col))
					elif( world[row][col] == 'g' ):
						self.goal = (row,col)
		for i in range(len(self.openList)):
			# calculate h
			self.openList[i][0].h = 0.25 * math.sqrt(math.pow(self.openList[i][0].where[0]-self.goal[0],2)
									+ math.pow(self.openList[i][0].where[1]-self.goal[1],2))
			# calculate f
			self.openList[i][0].f = self.openList[i][0].h


	def search( self ):
		
		def heapsort( cellList ):
			heap = []
			for cell in cellList:
				heap.append((cell.f,cell))
			heap.sort(key=operator.itemgetter(0))
			for i in range(len(heap)):
				heap[i] = heap[i][1]
			return heap

		def g( p, c ):
			# diagonal movement or not
			m = 2
			if( c.where[0]-p.where[0] == 0 and c.where[1]-p.where[1] != 0 or
			c.where[0]-p.where[0] != 0 and c.where[1]-p.where[1] == 0):
				m = 1
			else:
				m = math.sqrt(2)

			# movement cost given terrain
			if( self.world[p.where[0]][p.where[1]] == '2' ):
				if( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*2 )
				else:
					c.g = p.g + ( m*1.5 )

			elif( self.world[p.where[0]][p.where[1]] == 'a' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*0.25 )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*0.375 )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			elif( self.world[p.where[0]][p.where[1]] == 'b' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*0.375 )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*0.5 )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			else:
				if( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

		def h( c, i ):
			if( i == 1 ):  # Raw Manhattan Distance -- Inadmissable
				c.h = math.fabs(c.where[0]-self.goal[0]) + math.fabs(c.where[1]-self.goal[1])
			elif( i == 2 ):  # Raw Chebyshev Distance -- Inadmissable
				c.h = max(math.fabs(c.where[0]-self.goal[0]), math.fabs(c.where[1]-self.goal[1]))
			elif( i == 3 ):  # Custom Manhattan Distance -- Inadmissable
				c.h = 0.25 * math.fabs(c.where[0]-self.goal[0]) + math.fabs(c.where[1]-self.goal[1])
			elif( i == 4 ):  # Custom Chebyshev Distance -- Admissable
				c.h = 0.25 * max(math.fabs(c.where[0]-self.goal[0]), math.fabs(c.where[1]-self.goal[1]))
			else:  # Custom Euclidean Distance -- Admissable
				c.h = 0.25 * math.sqrt(math.pow(c.where[0]-self.goal[0],2)+math.pow(c.where[1]-self.goal[1],2))

		def tracePath( c, i ):
			print("Shortest Movement Path Cost with weights {} =".format(self.w),c.g)
			curr = c
			self.g = curr.g
			#print("Shortest Path Trace")
			while( curr.parent != None ):
				#print(curr.where,curr.f,curr.g,curr.h)
				self.pathList.append(curr.where)
				curr = curr.parent
			#print(curr.where,curr.f,curr.g,curr.h)
			self.pathList.append(curr.where)
			'''
			for i in range(5):
				print(i,"Nodes Expanded =",self.nodes_expanded[i])
				print(i,"Nodes Considered =",self.nodes_considered[i])
			'''

		def successors( parent, index ):
			s = []

			# Top Left
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[1]
			and self.world[parent.where[0]+1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]-1,parent))
			# Top Center
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1],parent))
			# Top Right
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[1]
			and self.world[parent.where[0]+1][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]+1,parent))

			# Center Left
			if(parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[1]
			and self.world[parent.where[0]][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]-1,parent))
			# Center Right
			if(parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[1]
			and self.world[parent.where[0]][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]+1,parent))

			# Bottom Left
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]-1
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[1]
			and self.world[parent.where[0]-1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1]-1,parent))
			# Bottom Center
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1],parent))
			# Bottom Right
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[1]
			and self.world[parent.where[0]-1][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1]+1,parent))

			for child in s:
				# calculate g
				g(parent,child)
				# calculate h
				h(child,index)
				# calculate f
				child.f = child.g + self.w[0] * child.h
				# populate openList with new valid cells
				good = True
				for listCell in self.openList[index]:
					if( child.where == listCell.where and child.f >= listCell.f ):
						good = False
				for listCell in self.closedList[index]:
					if( child.where == listCell.where and child.f >= listCell.f ):
						good = False
				if( good == True ):
					self.nodes_considered[index] += 1
					self.openList[index].append(child)
		
		# main()
		while( len(self.openList[0]) != 0 ):
			for i in range(1,len(self.openList)):
				self.openList[0] = heapsort(self.openList[0])
				self.openList[i] = heapsort(self.openList[i])
				if( self.openList[i][0].f <= self.w[1]*self.openList[0][0].f ):
					if( self.openList[i][0].where == self.goal ):
						tracePath(self.openList[i][0],i)
						return self.pathList,i,self.nodes_expanded,self.nodes_considered,self.g
					else:
						s = self.openList[i].pop(0)
						successors(s,i)
						self.nodes_expanded[i] += 1
						self.closedList[i].append(s)
				else:
					if( self.openList[0][0].where == self.goal ):
						tracePath(self.openList[0][0],0)
						return self.pathList,0,self.nodes_expanded,self.nodes_considered,self.g
					else:
						s = self.openList[0].pop(0)
						successors(s,0)
						self.nodes_expanded[0] += 1
						self.closedList[0].append(s)


# main()  **********************************************************************
def main():

	world = [
		['s','1','1','1','1','1'],
		['0','1','0','0','0','1'],
		['0','1','0','0','0','1'],
		['1','1','0','1','1','1'],
		['1','0','0','1','0','1'],
		['1','1','1','1','0','1'],
		['0','0','0','0','0','g']
	]
	'''
	tic = []
	toc = []
	
	fileName = sys.argv[1]
	world,length,kCells,Centers = IO.readFile(fileName)
	
	w = [1.5,1.5]
	tic = time.clock()
	pathList,index,nodes_expanded,nodes_considered = sequential(world,w).search()
	toc = time.clock()
	print( index, "Elapsed Time = " + str(toc - tic) + " sec" )
	'''
	workbook = xlsxwriter.Workbook('Output.xlsx')
	worksheet = workbook.add_worksheet()
	
	results = []
	fileName = sys.argv[1]
	os.chdir("maps")
	row = 0
	for fileName in glob.glob("*.txt"):
		line = []
		line.append(fileName)  # 0
		print(fileName)
		world,length,kCells,Centers = IO.readFile(fileName)
		
		weights = [2,1.25]
		tic = time.clock()
		pathData,index,opened,considered,pathcost = sequential(world,weights).search()
		line.append(index)  # 1
		line.append(pathcost)  # 2
		line.append(weights[0])  # 3
		line.append(weights[1])  # 4
		for i in range(len(opened)):
			line.append(opened[i])  # 5-9
		for i in range(len(considered)):
			line.append(considered[i])  # 10-14
		#IO.display(fileName,world,pathData,pathList)
		toc = time.clock()
		print( index, "Elapsed Time = " + str(toc - tic) + " sec" )
		line.append(toc - tic)  # 15

		for col in range(len(line)):
			worksheet.write(row, col, line[col])
		row += 1
		
	# Start from the first cell. Rows and columns are zero indexed.
	# Iterate over the data and write it out row by row.

	# Write a total using a formula.
	
	workbook.close()


# Self Run  ********************************************************************
if( __name__ == "__main__" ):
	main()
