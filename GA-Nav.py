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

	#Edit these values to manipulate the map
	start = (0,0) #coordinates of the start
	goal = (3,3) #coordinates of the end
	obs1 = (2,0) #coordinates of an obstacle
	obs2 = (1,3) #coordinates of an obstacle
	minMoves = 6 #minimum number of moves to reach goal

	#Constructor
	def __init__(self):
		#Initialize an empty map
		for x in range(0, 4):
			for y in range(0,4):
				self.grid[x][y] = ' '

		#Fill in the map with points of interest		
		self.grid[self.start[0]][self.start[1]] = 'S'
		self.grid[self.goal[0]][self.goal[1]] = 'G'
		self.grid[self.obs1[0]][self.obs1[1]] = '%'
		self.grid[self.obs2[0]][self.obs2[1]] = '%'

	#Draw the map
	def draw(self):
		sys.stdout.write('+-+-+-+-+\n')
		for y in range(3,-1,-1):
			sys.stdout.write('|')
			for x in range(0, 4):
				sys.stdout.write(self.grid[x][y] + '|')
			sys.stdout.write('\n+-+-+-+-+\n')

#Generate random movement strings with a certain number of moves
def generate(moves):
	member = ["00"] * moves
	for x in range(0, moves):
		member[x] = random.choice("01") + random.choice("01")
	return member

#Check the fitness of a moveset
def fitCalc(member, enviro):
	position = enviro.start
	for x in range(0, len(member)):
		#Test out moves for the robot
		temp = member.pop(0)
		if temp == "00":
			postion[1]++
		elif temp == "01":
			position[1]--
		elif temp == "10":
			position[0]++
		elif temp == "11":
			position[0]--

		#Make sure it's a valid move, the fitness of the member is 0 if it results in passing through an obstacle or going out of bounds
		if position == enviro.obs1 or position == enviro.obs2 or position[0] > 3 or position[0] < 0 or position[1] > 3 or position[1] < 0:
			return 0

	#Calculate the Manhattan distance from the final location to the goal
	distance = abs(enviro.goal[0] - position[0]) + abs(enviro.goal[1] - position [1])

	return enviro.minMoves - distance

enviro = Map()
enviro.draw()
print (enviro.start)
