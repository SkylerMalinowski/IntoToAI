# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import operator

import numpy as np

from tkinter import *


# readFile()  ******************************************************************
def readFile( fileName ):
	kCells = []
	centers = []
	world = []
	
	with open(fileName,'r') as out:
		
		for i in range(2):
			line = out.readline().rstrip()
			kCells.append([int(line.split('[')[1].split(',')[0]),int(line.split(',')[1].split(']')[0])])
		
		for i in range(8):
			line = out.readline().rstrip()
			centers.append([int(line.split('[')[1].split(',')[0]),int(line.split(',')[1].split(']')[0])])
		
		for line in out:
			cell = line.split()
			world.append(cell)
	
	world[kCells[0][0]][kCells[0][1]] = 's'
	world[kCells[1][0]][kCells[1][1]] = 'g'
	
	return np.array(world), [len(world[0:]),len(world[0])], kCells, centers


# saveFile()  ******************************************************************
def saveFile( world, length, fileName, kCells, centers ):
	
	with open(fileName,'w') as out:
		
		out.write(str(kCells[0])+'\n')
		out.write(str(kCells[1])+'\n')
		
		for i in range(8):
			out.write(str(centers[i])+'\n')
		
		for x in range(length[0]):
			
			for y in range(length[1]):
				
				out.write(str(world[x][y]))
				out.write(str(' '))
			
			out.write('\n')


# Class  ***********************************************************************
class CellGrid(Canvas):
	
	def __init__( self, master, theMap, theData, rowNumber, columnNumber, cellSize ):
		Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber)
		self.pack()
		self.cellSize = cellSize
		self.grid = []
		self.theData = theData
		for row in range(rowNumber):
			line = []
			for col in range(columnNumber):
				line.append(Cell(self, col, row, cellSize, theMap[row][col]))
			self.grid.append(line)
		
		#bind click action
		self.bind("<Button-1>", self.handleMouseClick)  
		#bind moving while clicking
		self.bind("<B1-Motion>", self.handleMouseMotion)
		#bind release button action - clear the memory of midified cells.
		self.bind("<ButtonRelease-1>", lambda event: print("--> Click"))

		self.draw()
	
	def draw(self):
		for row in self.grid:
			for cell in row:
				cell.draw()
	
	def _eventCoords(self, event):
		row = int(event.y / self.cellSize)
		col = int(event.x / self.cellSize)
		return row, col

	def handleMouseClick(self, event):
		row, col = self._eventCoords(event)
		cell = self.grid[row][col]
		print(self.theData[row][col])
	
	def handleMouseMotion(self, event):
		row, col = self._eventCoords(event)
		cell = self.grid[row][col]


class Cell():
	
	colors = { 
		'0':"black",		# blocked cell
		'1':"white",		# regular unblocked cell
		'2':"grey",			# hard to traverse cell
		'a':"light blue",	# regular unblocked cell with a highway
		'b':"blue",			# hard to traverse cell with a highway
		's':"green",		# start cell
		'g':"red"			# finish cell
	}
	
	def __init__(self, master, x, y, size, value):
		self.master = master
		self.abs = x
		self.ord = y
		self.size = size
		self.fill = "white"
		self.value = value
	
	def setValue(self, value):
		self.value = value
	
	def draw(self):
		""" order to the cell to draw its representation on the canvas """
		if self.master != None :
			xmin = self.abs * self.size
			xmax = xmin + self.size
			ymin = self.ord * self.size
			ymax = ymin + self.size
			
			self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=self.colors[self.value], outline = "black")


# display()  *******************************************************************
def display( fileName, world, pathData, pathList ):
	
	colors = { 
		'0':"black",	# blocked cell
		'1':"white",	# regular unblocked cell
		'2':"grey",		# hard to traverse cell
		'a':"blue",		# regular unblocked cell with a highway
		'b':"navy",		# hard to traverse cell with a highway
		's':"green",	# start cell
		'g':"red"		# finish cell
	}
	
	#world,length,kCells,centers = readFile(fileName)
	
	print("Display World")
	
	size = 10
	root = Tk()
	root.title( fileName )
	GUI = CellGrid(root,world,pathData,len(world),len(world[0]),size)
	pathList = [tu[::-1] for tu in pathList]
	for i in range(len(pathList)):
		pathList[i] = tuple(map(size.__mul__,pathList[i]))
		pathList[i] = tuple(map(operator.add,pathList[i],[(size/2),(size/2)]))
	GUI.create_line(pathList,fill="orange",width=size/5)
	root.mainloop()
	
