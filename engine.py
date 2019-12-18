import os
import time
import json
from pynput import keyboard
from pychar import Terminal
from bresenham import bresenham

DELAY = 0.2

scenarioName = input("Scenario name: ")

def loadSettings():
	with open(scenarioName) as json_file:

		#json_file is the dictionary containing the settings
		return json.load(json_file)

st = loadSettings()

SCREEN_WIDTH = int(st['screen-width'])
SCREEN_HEIGHT = int(st['screen-height'])
#camera pos
SCREEN_X = int(st['screen-x'])
SCREEN_Y = int(st['screen-y'])

SCREEN_X2 = SCREEN_X + SCREEN_WIDTH
SCREEN_Y2 = SCREEN_Y + SCREEN_HEIGHT

BACKGROUND_CHAR = st['background-char']

MAP_WIDTH = int(st['map-width'])
MAP_HEIGHT = int(st['map-height'])

#rocket position
START_X = int(st['start-x'])
START_Y = int(st['start-y'])
START_CHAR = st['start-char']

GROUND_X1 = int(st['ground-x1'])
GROUND_X2 = int(st['ground-x2'])
GROUND_Y1 = int(st['ground-y1'])
GROUND_Y2 = int(st['ground-y2'])

#some dark magic using kernel32 that refreshes the display without flickering
from ctypes import *

STD_OUTPUT_HANDLE = -11

class COORD(Structure):
	pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

class SMALL_RECT(Structure):
	pass

SMALL_RECT._fields_ = [("Left", c_short), ("Top", c_short), ("Right", c_short), ("Bottom", c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
	pass

CONSOLE_SCREEN_BUFFER_INFO._fields_ = [
	("dwSize", COORD),
	("dwCursorPosition", COORD),
	("wAttributes", c_ushort),
	("srWindow", SMALL_RECT),
	("dwMaximumWindowSize", COORD)
]

def clearScreen():
	h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
 
	csbi = CONSOLE_SCREEN_BUFFER_INFO()
	windll.kernel32.GetConsoleScreenBufferInfo(h, pointer(csbi))
	dwConSize = csbi.dwSize.X * csbi.dwSize.Y

	scr = COORD(0, 0)
	windll.kernel32.FillConsoleOutputCharacterA(h, c_char(b" "), dwConSize, scr, pointer(c_ulong()))
	windll.kernel32.FillConsoleOutputAttribute(h, csbi.wAttributes, dwConSize, scr, pointer(c_ulong()))
	windll.kernel32.SetConsoleCursorPosition(h, scr)

#def clearScreen():
#	os.system('cls')

def mergeTerminals():
	screen.blit(gameMap, 0, 0, SCREEN_X, SCREEN_X2 - 1, SCREEN_Y, SCREEN_Y2 - 1)

def makeMap():
	gameMap.drawRect(GROUND_X1, GROUND_X2, GROUND_Y1, GROUND_Y2, "#", filled=True)

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
		objects.append(self)

	def move(self, dx, dy):
		path = list(bresenham(self.x, self.y, self.x + dx, self.y + dy))
		for point in path[1:]:
			if not is_blocked(point[0], point[1]):
				self.x = point[0] 
				self.y = point[1]
			else:
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

def on_press(key):
	try:
		if key.char == "w":
			Rocket.physics.accelerate(0, -2)
		if key.char == "s":
			Rocket.physics.accelerate(0, 1)
		if key.char == "a":
			Rocket.physics.accelerate(-1, 0)
		if key.char == "d":
			Rocket.physics.accelerate(1, 0)
	except AttributeError:
		print('special key {0} pressed'.format(
			key))

def on_release(key):
	if key == keyboard.Key.esc:
		# Stop listener
		return False

listener = keyboard.Listener(
	on_press=on_press,
	on_release=on_release)

gameMap = Terminal("map", MAP_WIDTH, MAP_HEIGHT, BACKGROUND_CHAR)
screen = Terminal("screen", SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_CHAR)

objects = []

physMod = genericPhysics()
Rocket = Entity(START_X, START_Y, START_CHAR, physics=physMod)

makeMap()

if __name__ == '__main__':
	listener.start()
	while True:
		mergeTerminals()
		performPhysics()
		try:
			renderObjects()
		except IndexError:
			print("list assignment out of range!")
		clearScreen()
		screen.flush()
		time.sleep(DELAY)
