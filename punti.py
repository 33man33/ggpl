from random import random
from pyplasm import *

def randomPoints(m, sx=1, sy=1):
	def point():
		return [random() * sx, random() * sy]
	return [point() for k in range(m)]

verts = randomPoints(200, 2*PI, 2)
obj = MKPOL([verts, AA(LIST)(range(200)), None])
VIEW(obj)
