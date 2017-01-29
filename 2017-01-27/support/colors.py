
from pyplasm import *

def intRGBColor(values):
	return Color4f([ values[0]/255.0,
                         values[1]/255.0,
                         values[2]/255.0,
                         1.0])

PURPLE = Color4f([0.41, 0.112, 0.77, 1.0])
GRAY = Color4f([0.7, 0.7, 0.7, 1.0])
RED= Color4f([0.6, 0, 0, 1.0])
WHITE= Color4f([1.0, 1.0, 1.0, 1.0])

BLUE_WIND = Color4f([0.275, 0.509, 0.706, 1.0])
NEW_YELLOW = intRGBColor([ 255, 250, 193 ])
DARK_GREEN = intRGBColor([ 80, 113, 103 ])
LIGHT_GREEN = intRGBColor([ 116, 164, 150 ])
BRICK = intRGBColor([211,153,127])
SIDEWALKS_GRAY = intRGBColor([90,89,89])

BID_GREEN = Color4f([0.0, 0.4, 0.3, 1.0])
DIRTY = Color4f([1, 0.9, 0.9, 1.0])
SILVER = Color4f([9.5, 9.5, 9.5, 1.0])
BLACK = Color4f([0.2, 0.2, 0.2, 1.0])
BROWN = Color4f([0.5, 0.2, 0, 1.0])
LIGHT_BROWN = Color4f([0.6, 0.5, 0, 1.0])
GROUND = Color4f([0.5, 0.05, 0.03, 1.0])
BLUE = Color4f([0, 0, 0.45, 1.0])
ORANGE = Color4f([1.0,0.5,0.16,1.0])

if __name__ == "__main__":
    VIEW(COLOR(LIGHT_BROWN)(CUBOID([1,1,1])))
