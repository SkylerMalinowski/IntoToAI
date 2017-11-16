# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import colors


# fileRead()  ******************************************************************
def fileRead( fileName ):
	world = []
	
	with open(fileName,'r') as out:
		
		for line in out:
			cell = line.split()
			world.append(cell)
	
	return np.array(world), [len(world[0:]),len(world[0])]


# saveFile()  ******************************************************************
def saveFile( world, length, fileName ):
	
	with open(fileName,'w') as out:
		
		for x in range(length[0]):
			
			for y in range(length[1]):
				
				out.write(str(world[x][y]))
				out.write(str(' '))
			
			out.write('\n')


# display()  *******************************************************************
def display( fileName ):
	world,length = fileRead(fileName)
	color = { '0':[0,0,0], '1':[255,255,255], '2':[224,224,224],
		'a':[80,208,255], 'b':[0,32,255], 's':[255,255,0], 'g':[255,0,0] }
	'''
	'0' 	= Black 		= [0,0,0]
	'1' 	= White 		= [255,255,255]
	'2' 	= Grey 			= [128,128,128]
	'a' 	= Light Blue 	= [80,208,255]
	'b' 	= Blue 			= [0,32,225]
	's' 	= Yellow 		= [255,255,0]
	'g' 	= Red 			= [255,0,0]
	'''
	color_world = np.ones([length[0],length[1],3],dtype=np.uint8)
	
	for row in range(length[0]):
		
		for col in range(length[1]):
			
			color_world[row,col,:] = color[world[row,col]]
	
	img = Image.fromarray(color_world)
	img.save(fileName[:-4]+'.png')
	
	''''  Sample Code
	data = np.random.rand(10, 10) * 20
	
	# create discrete colormap
	cmap = colors.ListedColormap(['red', 'blue'])
	bounds = [0,10,20]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	
	fig, ax = plt.subplots()
	ax.imshow(data, cmap=cmap, norm=norm)
	
	# draw gridlines
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
	ax.set_xticks(np.arange(-.5, 10, 1));
	ax.set_yticks(np.arange(-.5, 10, 1));
	
	plt.show()
	Modify Below For Our Data  '''
	
	data = np.random.rand(10, 10) * 20
	
	# create discrete colormap
	cmap = colors.ListedColormap(['red', 'blue'])
	bounds = [0,10,20]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	
	fig, ax = plt.subplots()
	ax.imshow(data, cmap=cmap, norm=norm)
	
	# draw gridlines
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
	ax.set_xticks(np.arange(-.5, 10, 1));
	ax.set_yticks(np.arange(-.5, 10, 1));
	
	plt.show()


# keyCells()  ******************************************************************
def keyCells( world, length ):
	start_cell = [0,0]
	goal_cell = [0,0]
	done = False
	
	while( not done ):
		
		r = random.uniform(0,1)
		
		# Top Margin
		if( r > 0.5 ):
			start_cell[0] = random.randint(0,int(0.2*(length[1]-1)))
			start_cell[1] = random.randint(0,length[1]-1)
		
		# Bottom Margin
		else:
			start_cell[0] = random.randint(int(0.2*(length[0]-1)),length[0]-1)
			start_cell[1] = random.randint(0,length[1]-1)
		
		r = random.uniform(0,1)
		
		# Left Margin
		if( r > 0.5 ):
			goal_cell[0] = random.randint(0,length[0]-1)
			goal_cell[1] = random.randint(0,int(0.2*(length[1]-1)))
		
		# Right Margin
		else:
			goal_cell[0] = random.randint(0,length[0]-1)
			goal_cell[1] = random.randint(int(0.2*(length[1]-1)),length[1]-1)
		
		if( (math.sqrt(math.pow(start_cell[0]-goal_cell[0],2)+math.pow(start_cell[1]-goal_cell[1],2)) >= 100) 
		and (world[start_cell[0],start_cell[1]] is not '1') 
		and (world[goal_cell[0],goal_cell[1]] is not '1') ):
			done = True
	
	world[start_cell[0],start_cell[1]] = 's'
	world[goal_cell[0],goal_cell[1]] = 'g'


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
def hardCells( world, length ):
	hardCell_centers = []
	radii = 15
	
	for hardCell_num in range(8):
		hardCell_centers.append([random.randint(0,length[0]-1),random.randint(0,length[0]-1)])
		# Need: Reroll duplicates
	
	for row,col in hardCell_centers:
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
	
	hardCells(world,length)
	world = highwayCells(world,length)
	blockedCells(world,length)
	keyCells(world,length)
	
	saveFile(world,length,fileName)


# main()  **********************************************************************
def main( length, fileName ):
	
	if( length is not None and fileName is not None ):
		generate(length,fileName)
	
	display(fileName)


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
