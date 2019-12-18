import json

FILE_NAME = input("FILE_NAME ")

SCREEN_WIDTH = input("SCREEN_WIDTH ")
SCREEN_HEIGHT = input("SCREEN_HEIGHT ")

#camera pos
SCREEN_X = input("SCREEN_X ")
SCREEN_Y = input("SCREEN_Y ")

BACKGROUND_CHAR = "."

MAP_WIDTH = input("MAP_WIDTH ")
MAP_HEIGHT = input("MAP_HEIGHT ")

#rocket position
START_X = input("START_X ")
START_Y = input("START_Y ")
START_CHAR = "O"

GROUND_X1 = input("GROUND_X1 ")
GROUND_X2 = input("GROUND_X2 ")
GROUND_Y1 = input("GROUND_Y1 ")
GROUND_Y2 = input("GROUND_Y2 ")

settings = {
    "screen-width" : SCREEN_WIDTH,
    "screen-height" : SCREEN_HEIGHT,
    "screen-x" : SCREEN_X,
    "screen-y" : SCREEN_Y,
    "background-char" : BACKGROUND_CHAR,
    "map-width" : MAP_WIDTH,
    "map-height" : MAP_HEIGHT,
    "start-x" : START_X,
    "start-y" : START_Y,
    "start-char" : START_CHAR,
    "map-width" : MAP_HEIGHT,
    "map-height" : MAP_WIDTH,
    "ground-x1" : GROUND_X1,
    "ground-x2" : GROUND_X2,
    "ground-y1" : GROUND_Y1,
    "ground-y2" : GROUND_Y2
    }

with open(FILE_NAME, 'w') as outfile:
    json.dump(settings, outfile)

print("Json file dumped successfuly")
input()