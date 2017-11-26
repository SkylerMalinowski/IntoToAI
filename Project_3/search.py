from heapq import *
import numpy as np
#import world


class astar(object):

	@staticmethod
	def distance(a, b):
		return float(((b[0] - a[0])**2) + ((b[1] - a[1])**2))

	@staticmethod
	def heuristic(a, ter_a, b, ter_b):
		distance = float()
		if(ter_a not in ['a','b'] and ter_b not in ['a','b']):
			if(ter_a is 'a'):
				ter_a = 1
			if(ter_b is 'a'):
				ter_b = 1
			if(ter_a is 'b'):
				ter_a = 2
			if(ter_b is 'b'):
				ter_b = 2
			distance = (float(ter_a+ter_b)/2)*astar.distance(a,b)
		else:
			if(ter_a is 'a' and ter_b is 'a'):
				distance = (.25)*astar.distance(a,b)
			if(ter_a is 'b' and ter_b is 'b'):
				distance = (.50)*astar.distance(a,b)
			else:
				distance = (.375)*astar.distance(a,b)
		return distance

	@staticmethod
	def pathfind(array, start, goal):
		#terrain = {(0,):(),(1,):(),(2,):(),('a',):(),('b',):(),(0,):(),(1,):(),(2,):(),('a',):(),('b',):(),(0,):(),(1,):(),(2,):(),('a',):(),('b',):()}
		neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

		close_set = set()
		came_from = {}
		gscore = {start:array[start[0]][start[1]]}
		#array[]	#need a current terrain variable?
		fscore = {start:astar.distance(start, goal)} #something like this not sure??
		oheap = []

		heappush(oheap, (fscore[start], start))

		while oheap:

			current = heappop(oheap)[1]

			if current == goal:
				data = []
				while current in came_from:
					data.append(current)
					current = came_from[current]
					return data

			print(current)
			close_set.add(current)
			for i, j in neighbors:
				neighbor = current[0] + i, current[1] + j
				if 0 <= neighbor[0] < array.shape[0]:
					if 0 <= neighbor[1] < array.shape[1]:
						if array[neighbor[0]][neighbor[1]] == 0:
							continue
					else:
						# array bound y walls
						continue
				else:
					# array bound x walls
					continue
				tentative_g_score = gscore[current] + astar.heuristic(current,array[current[0]][current[1]],neighbor, array[neighbor[0]][neighbor[1]])
				if neighbor in close_set and tentative_g_score <= gscore.get(neighbor, 0):
					continue

				if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
					came_from[neighbor] = current
					gscore[neighbor] = tentative_g_score
					fscore[neighbor] = tentative_g_score + astar.distance(neighbor, goal)
					heappush(oheap, (fscore[neighbor], neighbor))

		return False


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

def main():

	#as per this example the above algorithm reverses 0 and 1 in compared to the use the project expects
	#flipping those two will hopefully point to how to implement different terrain types

	nmap = np.array([
	[1,1,'b',1,0,0,0,0,2,2,2,2,2,0],
	[1,1,'b',2,2,2,2,1,1,1,1,1,2,1],
	[1,1,'a',1,0,0,2,0,0,0,0,1,1,0],
	[1,0,'a',1,1,1,2,1,1,1,1,1,1,1],
	[0,0,'b',0,0,0,2,0,0,1,1,0,0,0],
	[1,'a','a','a','a','a',2,1,1,1,1,1,0,1],
	[0,0,0,0,0,0,0,0,'b',0,2,1,0,0],
	[1,0,1,2,2,2,2,2,2,'b',2,2,2,2],
	[0,1,1,1,2,2,2,1,1,0,0,0,0,'a'],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0]],dtype=object)
	print(astar.pathfind(nmap, (0,0), (9,4)))


if( __name__ == "__main__" ):
	#fileName = parseCommand(sys.argv)
	main()
