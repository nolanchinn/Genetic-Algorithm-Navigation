# Nolan Chinn
# CPTR 445
# Homework 5
# 19 Feb. 2016
# A genetic algorithm approach to a robotic navigation problem.

import random 
import sys
import os

#A map of fixed size 4x4 with a starting point, an ending point, and 2 obstacles
class Map:
	grid = [[0 for x in range(4)] for x in range(4)] #the container for the map
	start = () #coordinates of the start
	goal = () #coordinates of the end
	obs1 = () #coordinates of an obstacle
	obs2 = () #coordinates of an obstacle

	#Constructor
	def __init__(self):
		#Initialize an empty map
		for x in range(0, 4):
			for y in range(0,4):
				self.grid[x][y] = ' '

		#Choose a starting location
		x = random.randrange(0,4)
		y = random.randrange(0,4)
		self.start = (x, y)
		self.grid[x][y] = 'S'

		#Choose a ending location
		while True:
			x = random.randrange(0,4)
			y = random.randrange(0,4)
			self.goal = (x, y)
			if self.start != self.goal:
				self.grid[x][y] = 'G'
				break

		#Choose the first obstacle's location
		while True:
			x = random.randrange(0,4)
			y = random.randrange(0,4)
			self.obs1 = (x, y)
			if self.start != self.obs1:
				if self.goal != self.obs1:
					self.grid[x][y] = '%'
					break

		#Choose the second obstacle's location
		while True:
			x = random.randrange(0,4)
			y = random.randrange(0,4)
			self.obs2 = (x, y)
			if self.start != self.obs2:
				if self.goal != self.obs2:
					if self.obs1 != self.obs2:
						self.grid[x][y] = '%'
						break

	#Draw the map
	def draw(self):
		sys.stdout.write('+-+-+-+-+\n')
		for y in range(3,-1,-1):
			sys.stdout.write('|')
			for x in range(0, 4):

				sys.stdout.write(self.grid[x][y] + '|')
			sys.stdout.write('\n+-+-+-+-+\n')
	
enviro = Map()
enviro.draw()
print (enviro.start)
