# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import sys
import math
import random
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
'''' # No not need unless tkinter is being used
class CellGrid(Canvas):
	
	def __init__(self,master, rowNumber, columnNumber, cellSize, theMap):
		Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber)
		self.pack()
		self.cellSize = cellSize
		
		scrollbar = Scrollbar(master)
		scrollbar.pack(side=RIGHT, fill=Y)
		
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
'''

# display()  *******************************************************************
def display( fileName ):
	
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
	
	'''' # No Scrollbars
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
				worksheet2.write_blank(row, col, '', format2)


# selectLeyLocation()  *********************************************************
def selectKeyLocation( cell ):
	r = random.randint(0,3)
		
	# Top Margin
	if( r == 0 ):
		cell[0] = random.randint(0,int(0.2*(length[1]-1)))
		cell[1] = random.randint(0,length[1]-1)
	
	# Bottom Margin
	elif( r == 1 ):
		cell[0] = random.randint(int(0.2*(length[0]-1)),length[0]-1)
		cell[1] = random.randint(0,length[1]-1)
	
	# Left Margin
	elif( r == 2 ):
		cell[0] = random.randint(0,length[0]-1)
		cell[1] = random.randint(0,int(0.2*(length[1]-1)))
	
	# Right Margin
	elif( r == 3 ):
		cell[0] = random.randint(0,length[0]-1)
		cell[1] = random.randint(int(0.2*(length[1]-1)),length[1]-1)
	
	# Failure
	else:
		print("Error: Location cannot be determined");
	
	return cell

# keyCells()  ******************************************************************
def keyCells( world, length, kCells ):
	done = False
	
	while( not done ):
		
		kCells[0] = selectKeyLocation(kCells[0])
		kCells[1] = selectKeyLocation(kCells[1])
		
		if( (math.sqrt(math.pow(kCells[0][0]-kCells[1][0],2)+math.pow(kCells[0][1]-kCells[1][1],2)) >= 100) 
		and (world[kCells[0][0],kCells[0][1]] is not '0') 
		and (world[kCells[1][0],kCells[1][1]] is not '0') ):
			done = True
	
	world[kCells[0][0],kCells[0][1]] = 's'
	world[kCells[1][0],kCells[1][1]] = 'g'


# blockedCells()  **************************************************************
def blockedCells( world, length ):
	
	for num in range(int(0.2*length[0]*length[1])):
		cell = [random.randint(0,length[0]-1),random.randint(0,length[1]-1)]
		
		while( (world[cell[0],cell[1]] == 'a') or (world[cell[0],cell[1]] == 'b')
		or (world[cell[0],cell[1]] == '0') ):
			cell = [random.randint(0,length[0]-1),random.randint(0,length[1]-1)]
		
		world[cell[0],cell[1]] = '0'


# layHighway()  ****************************************************************
def layHighway( world, length, edge, highway_length, direction ):
	strip = 20
	valid = True
	
	if( direction == 'up' ):
		for offset in range(strip):
			if( edge[0]-1 >= 0 and edge[0]-1 < length[0] ):
				edge = [edge[0]-1,edge[1]]
				highway_length += 1
				if( world[edge[0],edge[1]] == '1' ):
					world[edge[0],edge[1]] = 'a'
				elif( world[edge[0],edge[1]] == '2' ):
					world[edge[0],edge[1]] = 'b'
				else:
					valid = False
			else:
				break
	
	elif( direction == 'down' ):
		for offset in range(strip):
			if( edge[0]+1 >= 0 and edge[0]+1 < length[0] ):
				edge = [edge[0]+1,edge[1]]
				highway_length += 1
				if( world[edge[0],edge[1]] == '1' ):
					world[edge[0],edge[1]] = 'a'
				elif( world[edge[0],edge[1]] == '2' ):
					world[edge[0],edge[1]] = 'b'
				else:
					valid = False
			else:
				break
	
	elif( direction == 'left' ):
		for offset in range(strip):
			if( edge[1]-1 >= 0 and edge[1]-1 < length[1] ):
				edge = [edge[0],edge[1]-1]
				highway_length += 1
				if( world[edge[0],edge[1]] == '1' ):
					world[edge[0],edge[1]] = 'a'
				elif( world[edge[0],edge[1]] == '2' ):
					world[edge[0],edge[1]] = 'b'
				else:
					valid = False
			else:
				break
	
	elif( direction == 'right' ):
		for offset in range(strip):
			if( edge[1]+1 >= 0 and edge[1]+1 < length[1] ):
				edge = [edge[0],edge[1]+1]
				highway_length += 1
				if( world[edge[0],edge[1]] == '1' ):
					world[edge[0],edge[1]] = 'a'
				elif( world[edge[0],edge[1]] == '2' ):
					world[edge[0],edge[1]] = 'b'
				else:
					valid = False
			else:
				break
	
	else:
		print("Error: not a direction!")
		sys.exit(1)
	
	return world, edge, highway_length, valid


# highwayCells()  **************************************************************
def highwayCells( world, length ):
	
	for highway_num in range(4):
		world_backup = np.copy(world)  # make backup
		done = False
		
		while( not done ):
			world = np.copy(world_backup)  # restore backup
			r = random.randint(0,3)
			edge = [0,0]
			highway_length = 0
			valid = True
			
			# Top
			if( r == 0 ):
				edge[0] = 0
				edge[1] = random.randint(0,length[1]-1)
				direction = 'down'
			
			# Bottom
			elif( r == 1 ):
				edge[0] = length[0]-1
				edge[1] = random.randint(0,length[1]-1)
				direction = 'up'
			
			# Left Side
			elif( r == 2 ):
				edge[0] = random.randint(0,length[0]-1)
				edge[1] = 0
				direction = 'right'
			
			# Right Side
			elif( r == 3 ):
				edge[0] = random.randint(0,length[0]-1)
				edge[1] = length[1]-1
				direction = 'left'
			
			# Failure
			else:
				print("Error: start not determined!")
				sys.exit(1)
			
			if( world[edge[0],edge[1]] == '1' ):
				world[edge[0],edge[1]] = 'a'
			elif( world[edge[0],edge[1]] == '2' ):
				world[edge[0],edge[1]] = 'b'
			
			world,edge,highway_length,valid = layHighway(world,length,edge,highway_length,direction)
			
			while( (edge[0] is not 0) and (edge[0] is not length[0]-1)
			and (edge[1] is not 0) and (edge[1] is not length[1]-1) and (valid is True) ):
				
				world,edge,highway_length,valid = layHighway(world,length,edge,highway_length,direction)
				
				r = random.randint(0,100)
				
				# Left
				if( r < 20 ):
					if( direction == 'up' ):
						direction = 'left'
					elif( direction == 'down' ):
						direction = 'right'
					elif( direction == 'left' ):
						direction = 'down'
					elif( direction == 'right' ):
						direction = 'up'
					else:
						sys.exit(1)
				
				# Ahead
				elif( r <= 80 ):
					pass
				
				# Right
				elif( r <= 100 ):
					if( direction == 'up' ):
						direction = 'right'
					elif( direction == 'down' ):
						direction = 'left'
					elif( direction == 'left' ):
						direction = 'up'
					elif( direction == 'right' ):
						direction = 'down'
					else:
						sys.exit(1)
				
				# Failure
				else:
					print("Error: highway bend failed!")
					sys.exit(1)
				
			if( highway_length >= 100 and valid == True ):
				done = True
	
	return world


# hardCells()  *****************************************************************
def hardCells( world, length, centers ):
	radii = 15
	
	for hardCell_num in range(8):
		centers.append([random.randint(0,length[0]-1),random.randint(0,length[0]-1)])
		# Need: Reroll duplicates
	
	for row,col in centers:
		top = max(0,row-radii)
		bottom = min(length[0]-1,row+radii)
		left = max(0,col-radii)
		right = min(length[1]-1,col+radii)
		
		for x in range(top,bottom+1):  # row
			for y in range(left,right+1):  # col
				if( random.randint(0,100) < 50 ):
					world[x][y] = '2'


# generate()  ******************************************************************
def generate( length, fileName ):
	''''
	'0' = blocked cell
	'1' = regular unblocked cell
	'2' = hard to traverse cell
	'a' = regular unblocked cell with a highway
	'b' = hard to traverse cell with a highway
	'''
	
	random.seed()
	length[0] = int(length[0])
	length[1] = int(length[1])
	world = np.ones(shape=(length[0],length[1]),dtype=str)
	kCells = [[0,0],[0,0]]
	centers = []
	
	# Procedurally generate World
	hardCells(world,length,centers)
	world = highwayCells(world,length)
	blockedCells(world,length)
	
	for i in range(10):
		keyCells(world,length,kCells)
		
		# Save the World for I/O
		saveFile(world,length,fileName[:-4]+str(i+1)+'.txt',kCells,centers)


# main()  **********************************************************************
def main( length, fileName ):
	
	if( length is None ):
		display(fileName)
	
	else:
		generate(length,fileName)


# parseCommand()  **************************************************************
def parseCommand( argv ):
	# Allow user to enter one or two numbers and a filename or just a file name
	
	if( len(argv) == 1 ):
		print("Too few arguments. Needs at least 1 arguments.")
		sys.exit(1)
	
	if( len(argv) == 2 ):
		
		if( argv[1].lower().endswith('.txt') ):
			return None, argv[1]
		
		else:
			print("Argument is not correct. Enter a text file name.")
			sys.exit(1)
	
	elif( len(argv) == 3 ):
		
		if( argv[1].isdigit() and argv[2].lower().endswith('.txt') ):
			return [argv[1],argv[1]], argv[2]
		
		elif( argv[1].lower().endswith('.txt') and argv[2].isdigit() ):
			return [argv[2],argv[2]], argv[1]
		
		else:
			print("Arguments are not correct. Both enter a number and a text file name.")
			sys.exit(1)
	
	elif( len(argv) == 4 ):
		
		if( argv[1].isdigit() and argv[2].isdigit() and argv[3].lower().endswith('.txt') ):
			return [argv[1],argv[2]], argv[3]
		
		elif( argv[1].lower().endswith('.txt') and argv[2].isdigit() and argv[3].isdigit() ):
			return [argv[2],argv[3]], argv[1]
		
		else:
			print("Arguments are not correct. Enter two consecutive numbers and a text file name.")
			sys.exit(1)
	
	else:
		print("Too many arguments. Needs at most 3 arguments.")
		sys.exit(1)


# Run Module If Not Imported  **************************************************
if( __name__ == "__main__" ):
	length,fileName = parseCommand(sys.argv)
	main(length,fileName)
