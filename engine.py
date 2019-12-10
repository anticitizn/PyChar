import os
import time
from pychar import Terminal
from bresenham import bresenham

SCREEN_WIDTH = 20
SCREEN_HEIGHT = 10
SCREEN_X = 0
SCREEN_Y = 0
SCREEN_X2 = SCREEN_X + SCREEN_WIDTH
SCREEN_Y2 = SCREEN_Y + SCREEN_HEIGHT
BACKGROUND_CHAR = "."

MAP_WIDTH = 20
MAP_HEIGHT = 10
gameMap = Terminal("map", MAP_WIDTH, MAP_HEIGHT, BACKGROUND_CHAR)
screen = Terminal("screen", SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_CHAR)

def mergeTerminals():
	screen.blit(gameMap, 0, 0, SCREEN_X, SCREEN_X2 - 1, SCREEN_Y, SCREEN_Y2 - 1)

def makeMap():
	gameMap.drawRect(0, 19, 9, 8, "#", filled=True)

def renderObjects():
	for object in objects:
		if is_inside(SCREEN_X, SCREEN_Y, SCREEN_X2, SCREEN_Y2, object.x, object.y):
			screen.putChar(object.x - SCREEN_X, object.y - SCREEN_Y, object.char)

def performPhysics():
	for object in objects:
		if object.physics:
			object.move(object.physics.mx, object.physics.my)
			if not is_blocked(object.x, object.y + 1):
				object.physics.accelerate(0, 1)
			else:
				object.physics.my = 0

def playerInput():
	print("Input x acceleration")
	xacc = input()
	print("Input y acceleration")
	yacc = input()
	Rocket.physics.accelerate(int(xacc), int(yacc))



def is_blocked(x, y):
	#testing the map tile first
	if gameMap.getChar(x, y) == "#":
		return True

	for object in objects: 
		if object.x == x and object.y == y:
			return True

	return False

def is_inside(x1, y1, x2, y2, x, y):
	if (x > x1 and x < x2 and 
		y > y1 and y < y2): 
		return True
	else: 
		return False


class Entity:
	#A generic object

	def __init__(self, x, y, char, physics=None):
		self.x = x
		self.y = y
		self.char = char
		self.physics = physics
		if self.physics:
			self.physics.owner = self

	def move(self, dx, dy):
		path = list(bresenham(self.x, self.y, self.x + dx, self.y + dy))
		print(path)
		print(self.x)
		print(self.y)
		for point in path[1:]:
			if not is_blocked(point[0], point[1]):  #<----------- THE PROBLEM IS HERE!
				self.x = point[0] #Tiles shouldn't be added, adding them results in absurd and incorrect values
				self.y = point[1]
				print(str(self.x) + " " + str(self.y))
				print(str(point[0]) + " " + str(point[1]))
				print("is_blocked check ran successfuly!")
			else:
				print("is_blocked check failed")
				break

	def returnCoords(self):
		print(str(self.x) + ' ' + str(self.y))

class genericPhysics:
	def __init__(self, mx=0, my=0):
		self.mx = mx
		self.my = my

	def accelerate(self, nx, dy):
		self.mx += nx
		self.my += dy

objects = []

physMod = genericPhysics()
Rocket = Entity(10, 5, "O", physics=physMod)
objects.append(Rocket)


makeMap()

if __name__ == '__main__':
	while True:
		delay = 0.2
		print("Frames:")
		frames = input()
		playerInput()
		frames = int(frames)
		while frames >= 0:
			os.system('cls' if os.name == 'nt' else 'clear')
			mergeTerminals()
			performPhysics()
			try:
				renderObjects()
			except IndexError:
				print("list assignment out of range!")
			screen.flush()
			frames -= 1
			time.sleep(delay)