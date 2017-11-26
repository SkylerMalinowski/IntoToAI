# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import sys
import math
import heapq
import operator

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

	def __str__(self):
		return str(self.where)

class aStar:

	def __init__( self, world ):
		self.world = world
		self.pathData = []
		self.goal = None
		self.length = [len(world),len(world[0])]
		self.openList = []
		self.closedList = []
		self.found = False
		while( len(self.openList) == 0 and self.goal == None ):
			for row in range(self.length[0]):
				for col in range(self.length[1]):
					if( world[row][col] == 's' ):
						self.openList.append(cell(row,col))
					elif(  world[row][col] == 'g' ):
						self.goal = (row,col)

	def search( self ):

		def heapsort( cellList ):
			heap = []
			sortedHeap = []
			for cell in cellList:
				heapq.heappush(heap,(cell.f,cell))
			for tup in range(len(heap)):
				x = heapq.heappop(heap)
				print(x[0],x[1])
				sortedHeap.append(x[1])
			return sortedHeap

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
					c.g = p.g + ( m*(1/4) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			elif( self.world[p.where[0]][p.where[1]] == 'b' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(1/2) )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			else:
				if( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

		def h( c ):
			c.h = math.sqrt(math.pow(c.where[0]-self.goal[0],2) + math.pow(c.where[1]-self.goal[1],2))

		def tracePath( c ):
			print("Shortest Movement Path Cost =",c.g)
			curr = c
			print("Shortest Path Trace")
			while( curr.parent != None ):
				print(curr.where)
				curr = curr.parent
			print(curr.where)

		def successors( parent ):
			s = []

			# Top Left
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]-1,parent))
			# Top Center
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1],parent))
			# Top Right
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]+1,parent))

			# Center Left
			if(parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]-1,parent))
			# Center Right
			if(parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]+1,parent))

			# Bottom Left
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1]-1,parent))
			# Bottom Center
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1],parent))
			# Bottom Right
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]+1] != '0'):
				s.append(cell(q.where[0]-1,parent.where[1]+1,parent))

			for child in s:
				# calculate g
				g(parent,child)
				# calculate h
				h(child)
				# calculate f
				child.f = child.g + child.h

				# Goal Found
				if(self.world[child.where[0]][child.where[1]] == 'g'):
					print("Path Found")
					#tracePath(child)
					self.found = True
					return

				# populate openList with new valid cells
				good = True
				for listCell in self.openList:
					if( child.where == listCell.where and child.f > listCell.f ):
						good = False
				for listCell in self.closedList:
					if( child.where == listCell.where and child.f > listCell.f ):
						good = False
				if( good == True ):
					self.openList.append(child)
					#print(child.where,child.f,child.g,child.h)

				'''
				# populate openList with new valid cells
				good = True
				for listCell in self.closedList:
					if( child.where == listCell.where and child.f < listCell.f ):
						good = False
				for listCell in self.openList:
					if( child.where == listCell.where and good == True ):
						if( child.f < listCell.f):
							listCell = child
						good = False
				if( good == True ):
					self.openList.append(child)
				'''

		# main()
		while( len(self.openList) != 0 ):
			# find smallest 'f' in openList
			self.openList = heapsort(self.openList)
			input()
			# pop the smallest 'f'
			q = self.openList.pop(0)
			# generate successors
			if( self.found == False ):
				successors(q)
			self.closedList.append(q)

		if( self.found == False ):
			print("Path Not Found")
		return self.pathData


class aStarWeighted(aStar):

	def __init__( self, world, weight):
		aStar.__init__(self,world)
		self.w = weight

	def search( self ):
		def heapsort( cellList ):
			h = []
			for cell in cellList:
				heapq.heappush(h, cell.f)
			return [heapq.heappop(h) for i in range(len(h))]

		def g( p, c ):
			# diagonal movement or not
			m = 1
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
					c.g = p.g + ( m*(1/4) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			elif( self.world[p.where[0]][p.where[1]] == 'b' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(1/2) )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

			else:
				if( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*1.5 )
				else:
					c.g = p.g + ( m*1 )

		def h( c ):
			c.h = math.sqrt(math.pow(c.where[0]-self.goal[0],2) + math.pow(c.where[1]-self.goal[1],2))

		def tracePath( c ):
			print("Shortest Movement Path Cost =",c.g)
			curr = c
			print("Shortest Path Trace")
			while( curr.parent != None ):
				print(curr.where)
				curr = curr.parent
			print(curr.where)

		def successors( parent ):
			s = []

			# Top Left
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]-1,parent))
			# Top Center
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1],parent))
			# Top Right
			if(parent.where[0]+1 >= 0 and parent.where[0]+1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]+1][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0]+1,parent.where[1]+1,parent))

			# Center Left
			if(parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]-1,parent))
			# Center Right
			if(parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]][parent.where[1]+1] != '0'):
				s.append(cell(parent.where[0],parent.where[1]+1,parent))

			# Bottom Left
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and parent.where[1]-1 >= 0 and parent.where[1]-1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]-1] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1]-1,parent))
			# Bottom Center
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]] != '0'):
				s.append(cell(parent.where[0]-1,parent.where[1],parent))
			# Bottom Right
			if(parent.where[0]-1 >= 0 and parent.where[0]-1 < self.length[0]
			and parent.where[1]+1 >= 0 and parent.where[1]+1 < self.length[0]
			and self.world[parent.where[0]-1][parent.where[1]+1] != '0'):
				s.append(cell(q.where[0]-1,parent.where[1]+1,parent))

			for child in s:
				# calculate g
				g(parent,child)
				# calculate h
				h(child)
				# calculate f
				#print("hi from weighted land!")
				child.f = child.g + (self.w)*child.h

				# Goal Found
				if(self.world[child.where[0]][child.where[1]] == 'g'):
					print("Path Found")
					tracePath(child)
					self.found = True
					return

				''''
				# populate openList with new valid cells
				good = True
				for listCell in self.openList:
					if( child.where == listCell.where and child.f > listCell.f ):
						good = False
				for listCell in self.closedList:
					if( child.where == listCell.where and child.f > listCell.f ):
						good = False
				if( good == True ):
					self.openList.append(child)
					print(child.where,child.f,child.g,child.h)
					input()
				'''

				# populate openList with new valid cells
				good = True
				for listCell in self.closedList:
					if( child.where == listCell.where and child.f < listCell.f ):
						good = False
				for listCell in self.openList:
					if( child.where == listCell.where and good == True ):
						if( child.f < listCell.f):
							listCell = child
						good = False
				if( good == True ):
					self.openList.append(child)

		# main()
		while( len(self.openList) != 0 ):
			# find smallest 'f' in openList
			heapsort(self.openList)
			# pop the smallest 'f'
			q = self.openList.pop(0)
			#print(q.where, q.f, q.g, q.h)
			# generate successors
			if( self.found == False ):
				successors(q)
			self.closedList.append(q)

		if( self.found == False ):
			print("Path Not Found")
		return self.pathData


# class  ***********************************************************************
class heuristic_algorithm:

	def __init__( self, w1, w2,  ):
		self.start = start
		self.goal = goal
		self.w = [w1,w2]  # w1,w2 >= 1.0
		self.openList = []
		self.closedList = []


# main()  **********************************************************************
def main():
	world = [
		['s','1','1','1','1','1','0'],
		['0','1','0','0','0','1','0'],
		['0','1','0','0','0','1','0'],
		['1','1','0','1','1','1','0'],
		['1','0','0','1','0','1','0'],
		['1','1','1','1','0','1','0'],
		['0','0','0','0','0','g','0']
	]

	#fileName = sys.argv[1]

	#world,length,kCells,Centers = IO.readFile(sys.argv[1])

	pathData = aStar(world).search()
	#pathData = aStarWeighted(world,5.5).search()
	#IO.display(fileName,world,pathData)


# Self Run  ********************************************************************
if( __name__ == "__main__" ):
	main()
