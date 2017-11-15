# **************************************************************************** #
# Skyler Malinowski [ som12 ]
# Andrew Dos Reis [ ad1005 ]
# Project 3
# CS 440
# **************************************************************************** #

import sys, os;
import random;
import numpy as np;
import tkinter as tk;
#from tkinter import *;

# display()  *******************************************************************
def display( fileName ):
	root = tk.Tk()
	root.title("Grid World");
	
	# Need: Display world as a grid with colors
	for r in range(10):
		for c in range(10):
			i = random.randint(0,10);
			tk.Label(root,text='%s'%(i),borderwidth=10,relief='groove').grid(row=r,column=c);
	
	root.mainloop();


# blockedCells()  **************************************************************
def blockedCells( world, length ):
	cell = [0,0];
	
	for num in range(int(0.2*length[0]*length[1])):
		cell[0] = random.randint(0,length[0]-1);
		cell[1] = random.randint(0,length[1]-1);
		
		while( (world[cell[0],cell[1]] == 'a') or (world[cell[0],cell[1]] == 'b')
		or (world[cell[0],cell[1]] == 0) ):
			cell[0] = random.randint(0,length[0]-1);
			cell[1] = random.randint(0,length[1]-1);
		
		world[cell[0],cell[1]] = 0;


# layHighway()  ****************************************************************
def layHighway( world, length, edge, highway_length, direction ):
	stretch = 20;
	
	if( direction == 'up' ):
		for offset in range(stretch):
			if( edge[0]-1 >= 0 and edge[0]-1 < length[0] ):
				edge = [edge[0]-1,edge[1]];
				if( world[edge[0],edge[1]] == 1 ):
					world[edge[0],edge[1]] = 'a';
				elif( world[edge[0],edge[1]] == 2 ):
					world[edge[0],edge[1]] = 'b';
			else:
				break;
	
	elif( direction == 'down' ):
		for offset in range(stretch):
			if( edge[0]+1 >= 0 and edge[0]+1 < length[0] ):
				edge = [edge[0]+1,edge[1]];
				if( world[edge[0],edge[1]] == 1 ):
					world[edge[0],edge[1]] = 'a';
				elif( world[edge[0],edge[1]] == 2 ):
					world[edge[0],edge[1]] = 'b';
			else:
				break;
	
	elif( direction == 'left' ):
		for offset in range(stretch):
			if( edge[1]-1 >= 0 and edge[1]-1 < length[1] ):
				edge = [edge[0],edge[1]-1];
				if( world[edge[0],edge[1]] == 1 ):
					world[edge[0],edge[1]] = 'a';
				elif( world[edge[0],edge[1]] == 2 ):
					world[edge[0],edge[1]] = 'b';
			else:
				break;
	
	elif( direction == 'right' ):
		for offset in range(stretch):
			if( edge[1]+1 >= 0 and edge[1]+1 < length[1] ):
				edge = [edge[0],edge[1]+1];
				if( world[edge[0],edge[1]] == 1 ):
					world[edge[0],edge[1]] = 'a';
				elif( world[edge[0],edge[1]] == 2 ):
					world[edge[0],edge[1]] = 'b';
			else:
				break;
	
	else:
		print("Error: not a direction!");
		sys.exit(1);
	
	return edge, highway_length+stretch;


# highwayCells()  **************************************************************
def highwayCells( world, length ):
	
	for highway_num in range(4):
		world_backup = world;
		done = False
		
		while( not done ):
			world = world_backup;
			r = random.randint(0,3);
			edge = ['?','?'];
			highway_length = 0;
			
			# Top
			if( r == 0 ):
				edge[0] = 0;
				edge[1] = random.randint(0,length[1]-1);
				direction = 'down';
			
			# Bottom
			elif( r == 1 ):
				edge[0] = length[0]-1;
				edge[1] = random.randint(0,length[1]-1);
				direction = 'up';
			
			# Left Side
			elif( r == 2 ):
				edge[1] = 0;
				edge[0] = random.randint(0,length[0]-1);
				direction = 'right';
			
			# Right Side
			elif( r == 3 ):
				edge[1] = length[1]-1;
				edge[0] = random.randint(0,length[0]-1);
				direction = 'left';
			
			# Failure
			else:
				print("Error: start not determined!");
				sys.exit(1);
			
			edge,highway_length = layHighway(world,length,edge,highway_length,direction);
			
			while( (edge[0] is not 0) and (edge[0] is not length[0]-1)
			and (edge[1] is not 0) and (edge[1] is not length[1]-1) ):
				
				edge,highway_length = layHighway(world,length,edge,highway_length,direction);
				
				# Left
				if( random.randint(0,100) < 20 ):
					if( direction == 'up' ):
						direction = 'left';
					elif( direction == 'down' ):
						direction = 'right';
					elif( direction == 'left' ):
						direction = 'down';
					elif( direction == 'right' ):
						direction = 'up';
					else:
						sys.exit(1);
				
				# Ahead
				elif( random.randint(0,100) <= 80 ):
					direction = direction;
				
				# Right
				elif( random.randint(0,100) <= 100 ):
					if( direction == 'up' ):
						direction = 'right';
					elif( direction == 'down' ):
						direction = 'left';
					elif( direction == 'left' ):
						direction = 'up';
					elif( direction == 'right' ):
						direction = 'down';
					else:
						sys.exit(1);
				
				# Failure
				else:
					print("Error: highway bend failed!");
					sys.exit(1);
				
			if( highway_length >= 100 ):
				done = True;


# hardCells()  *****************************************************************
def hardCells( world, length ):
	radii = 15;
	hardCell_centers = [];
	
	for hardCell_num in range(8):
		hardCell_centers.append([random.randint(0,length[0]-1),random.randint(0,length[0]-1)]);
		# Need: Reroll duplicates
	
	for row,col in hardCell_centers:
		top = max(0,row-radii);
		bottom = min(length[0]-1,row+radii);
		left = max(0,col-radii);
		right = min(length[1]-1,col+radii);
		
		for x in range(top,bottom+1):  # row
			for y in range(left,right+1):  # col
				if( random.randint(0,100) < 50 ):
					world[x][y] = 2;


# generate()  ******************************************************************
def generate( length, fileName ):
	''''
	'0' = blocked cell
	'1' = regular unblocked cell
	'2' = hard to traverse cell
	'a' = regular unblocked cell with a highway
	'b' = hard to traverse cell with a highway
	'''
	
	random.seed();
	length[0] = int(length[0]);
	length[1] = int(length[1]);
	world = np.ones(shape=(length[0],length[1]),dtype=object);
	
	hardCells(world,length);
	highwayCells(world,length);
	blockedCells(world,length);
	
	# top 20 rows or bottom 20 rows
	# left-most 20 columns or right-most 20 columns
	#S_start = [0,0];
	#S_end = [length[0]-1,length[1]-1];
	
	''''
	with open(fileName,'w') as out:
		pass;
	'''


# main()  **********************************************************************
def main( length, fileName ):
	
	if( length is not None and fileName is not None ):
		generate(length,fileName);
	
	display(fileName);


# parseCommand()  **************************************************************
def parseCommand( argv ):
	# Allow user to enter one or two numbers and a filename or just a file name
	
	if( len(argv) == 1 ):
		print("Too few arguments. Needs at least 1 arguments.");
		sys.exit(1);
	
	if( len(argv) == 2 ):
		
		if( argv[1].lower().endswith('.txt') ):
			return None, argv[1];
		
		else:
			print("Argument is not correct. Enter a text file name.");
			sys.exit(1);
	
	elif( len(argv) == 3 ):
		
		if( argv[1].isdigit() and argv[2].lower().endswith('.txt') ):
			return [argv[1],argv[1]], argv[2];
		
		elif( argv[1].lower().endswith('.txt') and argv[2].isdigit() ):
			return [argv[2],argv[2]], argv[1];
		
		else:
			print("Arguments are not correct. Both enter a number and a text file name.");
			sys.exit(1);
	
	elif( len(argv) == 4 ):
		
		if( argv[1].isdigit() and argv[2].isdigit() and argv[3].lower().endswith('.txt') ):
			return [argv[1],argv[2]], argv[3];
		
		elif( argv[1].lower().endswith('.txt') and argv[2].isdigit() and argv[3].isdigit() ):
			return [argv[2],argv[3]], argv[1];
		
		else:
			print("Arguments are not correct. Enter two consecutive numbers and a text file name.");
			sys.exit(1);
	
	else:
		print("Too many arguments. Needs at most 3 arguments.");
		sys.exit(1);


# Run Module If Not Imported  **************************************************
if( __name__ == "__main__" ):
	length,fileName = parseCommand(sys.argv);
	main(length,fileName);
