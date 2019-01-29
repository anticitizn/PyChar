import time
from pychar import Terminal

SCREEN_HEIGHT = 30
SCREEN_WIDTH = 50
SCREEN_X = 25
SCREEN_Y = 30
SCREEN_X2 = SCREEN_X + SCREEN_WIDTH
SCREEN_Y2 = SCREEN_Y + SCREEN_HEIGHT
BACKGROUND_CHAR = "."

MAP_WIDTH = 100
MAP_HEIGHT = 100
gameMap = Terminal("map", MAP_WIDTH, MAP_HEIGHT, BACKGROUND_CHAR)
screen = Terminal("screen", SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_CHAR)


def makeMap():
	gameMap.drawRect(0, 34, 59, 39, "#", filled=True)

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
	screen.blit(gameMap, 0, 0, SCREEN_X, SCREEN_X2 - 1, SCREEN_Y, SCREEN_Y2 - 1)
	performPhysics()
	try:
		renderObjects()
	except IndexError:
		print("list assignment out of range!")
	screen.flush()
	print(Rocket.x)
	print(Rocket.y)
	playerInput()