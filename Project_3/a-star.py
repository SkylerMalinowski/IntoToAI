# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import math
import heapq
import operator
import numpy as np


# class  ***********************************************************************
class cell:
	
	def __init__( self, row, col, parent=None ):
		self.parent = parent
		self.where = (row,col)
		self.f = 0.
		self.g = 0.
		self.h = 0.


class aStar:
	
	def __init__( self, world ):
		self.world = world
		self.goal = None
		self.length = [len(world),len(world[0])]
		self.openList = []
		self.closedList = []
		while( len(self.openList) == 0 and self.goal == None ):
			for row in range(self.length[0]):
				for col in range(self.length[1]):
					if( world[row][col] == 's' ):
						self.openList.append(cell(row,col))
					elif(  world[row][col] == 'g' ):
						self.goal = (row,col)
	
	def search( self ):
		
		def heapsort( cellList ):
			h = []
			for cell in cellList:
				heapq.heappush(h, cell.f)
			return [heapq.heappop(h) for i in range(len(h))]
		
		def g( p, c ):
			# diagonal movement or not
			if( c.where[0]-p.where[0] == 0 and c.where[1]-p.where[1] != 0 or
			c.where[0]-p.where[0] != 0 and c.where[1]-p.where[1] == 0):
				m = 1
			else:
				m = math.sqrt(2)
			# movement cost given terrain
			if( self.world[p.where[0]][p.where[1]] in ['1','s'] ):
				if( self.world[c.where[0]][c.where[1]] in ['1','a','s','g'] ):
					c.g = p.g + ( m*1 )
				elif( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*1.5 )
			
			elif( self.world[p.where[0]][p.where[1]] == '2' ):
				if( self.world[c.where[0]][c.where[1]] in ['1','a','s','g'] ):
					c.g = p.g + ( m*1.5 )
				elif( self.world[c.where[0]][c.where[1]] in ['2','b'] ):
					c.g = p.g + ( m*2 )
			
			elif( self.world[p.where[0]][p.where[1]] == 'a' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*(1/4) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] in ['1','s','g'] ):
					c.g = p.g + ( m*1 )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
			
			elif( self.world[p.where[0]][p.where[1]] == 'b' ):
				if( self.world[c.where[0]][c.where[1]] == 'a' ):
					c.g = p.g + ( m*(3/8) )
				elif( self.world[c.where[0]][c.where[1]] == 'b' ):
					c.g = p.g + ( m*(1/2) )
				elif( self.world[c.where[0]][c.where[1]] in ['1','s','g'] ):
					c.g = p.g + ( m*1 )
				elif( self.world[c.where[0]][c.where[1]] == '2' ):
					c.g = p.g + ( m*1.5 )
		
		def h( p, c ):
			c.h = math.sqrt((p.where[0]-c.where[0])**2 + (p.where[1]-c.where[1])**2)
		
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
				h(parent,child)
				# calculate f
				child.f = child.g + child.h
				
				if(self.world[child.where[0]][child.where[1]] == 'g'):
					# Trace Back
					print(child.g)
					return
				
				# populate openList with new valid cells
				good = True
				for listCell in self.openList:
					if( child.where == listCell.where and child.f > listCell.f ):
						good = False
				for listCell in self.closedList:
					if( child.where == listCell.where ):
						good = False
				if( good == True ):
					self.openList.append(child)
		
		# main()
		while( len(self.openList) != 0 ):
			# find smallest 'f' in openList
			heapsort(self.openList)
			# pop the smallest 'f'
			q = self.openList.pop(0)
			# generate successors
			successors(q)
			self.closedList.append(q)


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
		['1','1','2','1','1'],
		['1','0','0','0','1'],
		['s','0','g','1','1'],
		['1','0','0','0','1'],
		['1','1','1','1','1'],
	]
	
	aStar(world).search()


# Self Run  ********************************************************************
if( __name__ == "__main__" ):
	main()
