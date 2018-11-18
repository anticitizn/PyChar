import time
from pychar import Terminal

SCREEN_HEIGHT = 30
SCREEN_WIDTH = 30
BACKGROUND_CHAR = "."

MAP_WIDTH = 100
MAP_HEIGHT = 100
gameMap = Terminal("map", MAP_WIDTH, MAP_HEIGHT, BACKGROUND_CHAR)
screen = Terminal("screen", SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_CHAR)


def makeMap():
	gameMap.drawRect(0, 34, 59, 39, "#", filled=True)

def renderObjects():
	for object in objects:
		screen.putChar(object.x, object.y, object.char)

def performPhysics():
	for object in objects:
		if object.physics:
			object.move(object.physics.mx, object.physics.my)
			if not is_blocked(object.x, object.y + 1):
				object.physics.accelerate(0, 1)


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
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
		else:
			print("Collision detected and averted!")

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
Rocket = Entity(30, 33, "O", physics=physMod)
objects.append(Rocket)


makeMap()
while True:
	screen.blit(gameMap)
	performPhysics()
	try:
		renderObjects()
	except IndexError:
		print("list assignment out of range!")
	screen.flush()
	print(Rocket.x)
	print(Rocket.y)
	playerInput()