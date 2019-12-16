import json

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 80

#camera pos
SCREEN_X = 0
SCREEN_Y = 0

BACKGROUND_CHAR = "."

MAP_WIDTH = 80
MAP_HEIGHT = 80

#rocket position
START_X = 40
START_Y = 74
START_CHAR = "O"

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
    }

with open('settings.txt', 'w') as outfile:
    json.dump(settings, outfile)
