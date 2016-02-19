# Nolan Chinn
# CPTR 445
# Homework 5
# 19 Feb. 2016
# A genetic algorithm approach to a robotic navigation problem.

import random 
import sys
import copy
import operator
import os 

#A map of fixed size 4x4 with a starting point, an ending point, and 2 obstacles
class Map:
	grid = [[0 for x in range(4)] for x in range(4)] #the container for the map

	#Edit these values to manipulate the map
	start = [0,0] #coordinates of the start
	goal = [3,3] #coordinates of the end
	obs1 = [2,0] #coordinates of an obstacle
	obs2 = [1,3] #coordinates of an obstacle
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
	position = list(enviro.start)
	memCop = list(member) #copy the member so that we don't destroy it in the process
	for x in range(0, len(memCop)):
		#Test out moves for the robot
		temp = memCop.pop(0)
		if temp == "00": 
			position[1] += 1 #move up
		elif temp == "01":
			position[1] -= 1 #move down
		elif temp == "10":
			position[0] -= 1 #move left
		elif temp == "11":
			position[0] += 1 #move right

		#Make sure it's a valid move, the fitness of the member is 0 if it results in passing through an obstacle or going out of bounds
		if position == enviro.obs1 or position == enviro.obs2 or position[0] > 3 or position[0] < 0 or position[1] > 3 or position[1] < 0:
			return 0

	#Calculate the Manhattan distance from the final location to the goal
	distance = abs(enviro.goal[0] - position[0]) + abs(enviro.goal[1] - position [1])

	return enviro.minMoves - distance

#Print member
def printMem(member):
	for x in range(0, len(member)):
		sys.stdout.write(member[x])

#Draw the map with a path on top of it
def drawPath(enviro, member):
	newGrid = copy.deepcopy(enviro.grid)

	position = list(enviro.start)
	memCop = list(member)
	for x in range(0, len(memCop)):
		#Test out moves for the robot
		temp = memCop.pop(0)
		if temp == "00": 
			position[1] += 1 #move up
		elif temp == "01":
			position[1] -= 1 #move down
		elif temp == "10":
			position[0] -= 1 #move left
		elif temp == "11":
			position[0] += 1 #move right

		newGrid[position[0]][position[1]] = 'o'
	newGrid[enviro.goal[0]][enviro.goal[1]] = 'G'
	sys.stdout.write('+-+-+-+-+\n')
	for y in range(3,-1,-1):
		sys.stdout.write('|')
		for x in range(0, 4):
			sys.stdout.write(newGrid[x][y] + '|')
		sys.stdout.write('\n+-+-+-+-+\n')

#Create pairs ready for crossover
def select(pop):
	popCopy = copy.deepcopy(pop)
	totalFit = 0
	for x in range(0, len(popCopy)):
		totalFit += popCopy[x][1]
	if totalFit > 0:
		popCopy = sorted(popCopy, key=operator.itemgetter(1), reverse=True)
	pairs = []
	for x in range(0, len(popCopy), 2):
		pairs.append([popCopy[x], popCopy[x+1]])

	return pairs

#Change a random bit in a specific member
def mutate(member):
	moveSel = random.randrange(0,6) #select which "movement" to change
	bitSel = random.randrange(0,2) #select which bit in the "movement" to change

	#Logic for flipping bits (kinda hacky, probably a better way to do this)
	if bitSel == 0:
		if member[moveSel] == "00":
			member[moveSel] = "10"
		elif member[moveSel] == "01":
			member[moveSel] = "11"
		elif member[moveSel] == "10":
			member[moveSel] = "00"
		elif member[moveSel] == "11":
			member[moveSel] = "01"
	else:
		if member[moveSel] == "00":
			member[moveSel] = "01"
		elif member[moveSel] == "01":
			member[moveSel] = "00"
		elif member[moveSel] == "10":
			member[moveSel] = "11"
		elif member[moveSel] == "11":
			member[moveSel] = "10"
	return member

#Create a brand new population
def crossover(pairs, enviro):
	newPop = []
	for x in range(0, len(pairs)):
		a1 = [] #1st part of 1st in pair
		a2 = [] #2nd part of 1st in pair
		b1 = [] #1st part of 2nd in pair
		b2 = [] #2nd part of 2nd in pair
		new1 = []
		new2 = []
		crossPoint = random.randrange(0,6)
		for y in range(0, 6):
			if y < crossPoint:
				a1.append(pairs[x][0][0][y]) #build the 1st part from the 1st list
				b1.append(pairs[x][1][0][y]) #build the 1st part from the 2nd list
			else:
				a2.append(pairs[x][0][0][y]) #build the 2nd part from the 1st list
				b2.append(pairs[x][1][0][y]) #build the 2nd part from the 2nd list
		#form the new members of the population (perform the actual crossover)
		new1 = a1 + b2
		new2 = b1 + a2

		#both "children" have a 1/1000 chance to mutate
		if random.randrange(0, 1000) == 999:
			new1 = mutate(new1)
		if random.randrange(0, 1000) == 999:
			new2 = mutate(new2)
		#add the children to the newly created population
		newPop.append([new1, fitCalc(new1, enviro)])
		newPop.append([new2, fitCalc(new2, enviro)])
	return newPop



#Draw out the map
#+-+-+-+-+
#| |%| |G|	This is what the map looks like
#+-+-+-+-+  S represents the starting position
#| | | | |  G represents the goal position
#+-+-+-+-+  % represents an obstacle
#| | | | |  o represents a square visited by the path (none are visited at first)
#+-+-+-+-+
#|S| |%| |
#+-+-+-+-+

enviro = Map()
enviro.draw()

best = [[],1] #an empty best attempt, with 1 as the fitness since we don't want to display invalid solutions
population = [] 

#Generate the initial population
for x in range(0,6):
	temp = generate(6)
	tempFit = fitCalc(temp, enviro)
	population.append([temp, tempFit]) #member and member's fitness paired together

#Start the iterative process
for x in range(0,10000):
	population = crossover(select(population), enviro)
	if population[0][1] >= best[1]: #if a member of the new population is better than the previous best
		best = population[0] 		#make it then new best solution

		#Update the display with the new information
		os.system('cls')
		drawPath(enviro, best[0])
		sys.stdout.write("\nBest Path: ")
		printMem(best[0])
		sys.stdout.write("\nFitness: ")
		print(best[1])
