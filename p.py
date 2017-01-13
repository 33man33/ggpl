from larlib import *
from pyplasm import *
import csv

dimp = 8
dimf = 14
dimb = 4
dm= 2
b1= 100
b2= 50
n = .0015
h = 1./9
H = INTERVALS(h)(1)

def createStruct(file_name):
	lines = lines2lines(file_name)
	vert,eve = lines2lar(lines)
	level = STRUCT(MKPOLS((vert,eve)))
	level = OFFSET([n,n])(level)
	level = PROD([level,H])
	return level

def create_wall(f,dim):
	with open(f, "rb") as file:
		br = csv.reader(file, delimiter=",")
		w = []
		for r in br:
			w.append(POLYLINE([[float(r[0]), float(r[1])],[float(r[2]), float(r[3])]]))
	w = STRUCT(w)
	w = OFFSET([dim,dim])(w)
	return w

def create_floor(f, dim):
	i = 0
	verts = []
	cells = []
	pols = None
	with open(f, 'rb') as file:
        	br = csv.reader(file,delimiter=",")
        	for r in br:
            		verts.append([float(r[0]), float(r[1])])
                    j = i+1
            		verts.append([float(r[2]), float(r[3])])
            		i = i+1
            		cells.extend([j, i])
    	tot = OFFSET([dim, dim])(MKPOL([verts,[cells],pols]))
	return tot

exwall = create_wall("lines/perimetro.lines", dimp)
intwall = create_wall("lines/muri.lines", dimp)
windows = create_wall("lines/finestre.lines", dimf)
doors = create_wall("lines/porte.lines", dimb)
bal = create_wall("lines/balc.lines", dimb)


floor1 = STRUCT([create_floor("lines/pav1.lines", dm),create_floor("lines/pav2.lines", dm),create_floor("lines/pav3.lines", dm)])

floor2 = STRUCT([create_floor("lines/pav4.lines", dm),create_floor("lines/pav5.lines", dm),create_floor("lines/pav6.lines", dm), create_floor("lines/pav7.lines", dm), create_floor("lines/pav8.lines", dm), create_floor("lines/pav9.lines", dm), create_floor("lines/pav10.lines",dm)])

ex = PROD([DIFF([exwall,windows]),QUOTE([b1])])
inter = PROD([DIFF([intwall,doors]),QUOTE([b1])])
bal = PROD([bal,QUOTE([b2])])

floor1 = TEXTURE(["11.jpg"])(floor1)
floor2 = TEXTURE(["t1.jpg"])(floor2)
ex = TEXTURE(["12.jpeg"])(ex)
inter = TEXTURE(["12.jpeg"])(inter)
bal = TEXTURE(["t.jpg"])(bal)

VIEW(STRUCT([ex,inter,bal,floor1,floor2]))

