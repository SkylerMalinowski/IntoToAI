# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import xlsxwriter

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
	
	def __init__( self, master, rowNumber, columnNumber, cellSize, theMap ):
		Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber)
		self.pack()
		self.cellSize = cellSize
		self.grid = []
		for row in range(rowNumber):
			line = []
			for column in range(columnNumber):
				line.append(Cell(self, column, row, cellSize, theMap[row][column]))
			self.grid.append(line)
		
		self.draw()
	
	def draw(self):
		for row in self.grid:
			for cell in row:
				cell.draw()


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
def display( fileName, world, pathData ):
	
	colors = { 
		'0':"black",	# blocked cell
		'1':"white",	# regular unblocked cell
		'2':"grey",		# hard to traverse cell
		'a':"blue",		# regular unblocked cell with a highway
		'b':"navy",		# hard to traverse cell with a highway
		's':"green",	# start cell
		'g':"red"		# finish cell
	}
	
	world,length,kCells,centers = readFile(fileName)
	
	'''
	root = Tk()
	root.title( fileName )
	GUI = CellGrid(root,length[0],length[1],40,world)
	root.mainloop()
	'''
	
	with xlsxwriter.Workbook(fileName[:-4]+'.xlsx', {'constant_memory': True}) as workbook:
	
		worksheet1 = workbook.add_worksheet("Raw")
		worksheet2 = workbook.add_worksheet("Colored")
		
		format1 = workbook.add_format()
		format1.set_center_across()
		
		for row in range(length[0]):
			for col in range(length[1]):
				worksheet1.write(row, col, world[row][col], format1)
				format2 = workbook.add_format({'bg_color':str(colors[world[row][col]])})
				worksheet2.write_blank(row, col, ''+str(pathData[row][col])+'\n'+str(), format2)
	
	print("File Created")
