from pyplasm import *
from sympy import *
import numpy as np

A = [3.0,3.0,0.0]
B = [3.0,16.0,0.0]
C = [10.0,16.0,0.0]
D = [10.0,3.0,0.0]

A1 = [10.0,8.0,0.0]
B1 = [10.0,16.0,0.0]
C1 = [20.0,16.0,0.0]
D1 = [20.0,8.0,0.0]

A = [5.0,5.0,0.0]
B = [5.0,20.0,0.0]
C = [20.0,20.0,0.0]
D = [20.0,5.0,0.0]
E = [15.0,5.0,0.0]
F = [15.0,15.0,0.0]
G = [10.0,15.0,0.0]
H = [10.0,5.0,0.0]

A = [4.0,4.0,0.0]
B = [4.0,20.0,0.0]
C = [20.0,20.0,0.0]
D = [20.0,4.0,0.0]
E = [13.0,4.0,0.0]
F = [13.0,8.0,0.0]
G = [16.0,8.0,0.0]
H = [16.0,15.0,0.0]
I = [8.0,15.0,0.0]
L = [8.0,8.0,0.0]
M = [11.0,8.0,0.0]
N = [11.0,4.0,0.0]

mg = 2

def mF(pL):
    upx = pL[0][0]
    upy = pL[0][1]
    for p in pL:
        if p[0]> upx : upx = p[0]
        if p[1]> upy : upy = p[1]
    return (upx,upy)

def iP(p1, p2, p3):
    A = numpy.array([p1[:3], p2[:3], p3[:3]])
    B = -1*numpy.array([p1[-1], p2[-1], p3[-1]])
    return p(list(numpy.linalg.solve(A,B)))

def pE(A,B,C):
    x1,y1,z1 = p(A)
    x2,y2,z2 = p(B)
    x3,y3,z3 = p(C) 
    v1 = [x2 - x1, y2 - y1, z2 - z1]
    v2 = [x3 - x1, y3 - y1, z3 - z1]
    vProduct = [v1[1] * v2[2] - v1[2] * v2[1], -1 * (v1[0] * v2[2] - v1[2] * v2[0]), v1[0] * v2[1] - v1[1] * v2[0]]
    a = vProduct[0]
    b = vProduct[1]
    c = vProduct[2]
    d = - (vProduct[0] * x1 + vProduct[1] * y1 + vProduct[2] * z1)
    return [a,b,c,d]


def generatePol(pL):
	segm = []
	segmL = []
	for i in range(0,len(pL)) :
        	if i == len(pL)-1 : 
            		segm.append(points2s(pL[i],pL[0]))
            		segmL.append([pL[i],pL[0]])
        	else: 
            		segm.append(points2s(pL[i],pL[i+1]))
            		segmL.append([pL[i],pL[i+1]])
	return (segm,segmL)


def generateRoof (pointsList,height,angle):
    mg = 2
  
    xm = mF(pointsList)[0]
    ym = mF(pointsList)[1]

    ss = generatePol(pointsList)[0]
    ssList = generatePol(pointsList)[1]
    
    VIEW(COLOR(BLACK)(STRUCT(ss)))
    
    p = []
    for s in ssList :
        p.append(s2plane(s[0],s[1],angle))     
    p.append(COLOR(BLUE)(CUBOID([xm,ym,0])))  
    fsList = []
    for i in range(0,len(p)-1):
	if i != len(p)-mg : fsList.append(INTERSECTION([p[i],p[i+mg-1]]))
        else : fsList.append(INTERSECTION([p[i],p[0]]))


    fsL2 = []
    for f in fsList :
        fsL2.append(DIFFERENCE([f,STRUCT([T(3)(height),CUBOID([xm,ym,height*5])])]))
    
    p2 = []
    for i in range (0,len(fsL2)) :
        if i == len(fsL2)-1 : p2.append(TEXTURE("tetto.jpg")(JOIN([fsL2[i],fsL2[0]])))
        else : p2.append(TEXTURE("tetto.jpg")(JOIN([fsL2[i],fsL2[i+1]])))
        
    
    roof = STRUCT(p2)
    roofUk = UKPOL(roof)

    pterrace = getPointsTerrace(pointsList,height,roofUk)

    terrace = STRUCT([T(3)(height),fillPolygon(pterrace)])  
    terrace = TEXTURE("terrazzo.jpg")(terrace)
    #VIEW(terrace)  
    
    roof = STRUCT([roof,terrace])
    return roof



def getPointsTerrace(pointsList,height,rk):
    maxps = []
    for p in rk[0] :
        if p[2] < height+0.1 and p[2] > height-0.1 :
            ins = False
            for eP in maxps :
                xf = p[0] > eP[0] + 0.1 or p[0] < eP[0] - 0.1 
                yf = p[1] > eP[1] + 0.1 or p[1] < eP[1] - 0.1
                if not xf and not yf : 
                    ins = True
            if not ins : 
                p[2] = 0.0
                maxps.append(p)

    maxps_orderer = []
    for point in pointsList :
        point2 = maxps[0]
        point2X = math.fabs(maxps[0][0]-point[0])
        point2Y = math.fabs(maxps[0][1]-point[1])
        distance = math.sqrt(point2X*point2X+point2Y*point2Y)
        for i in range (1,len(maxps)):
            p2roximityX = math.fabs(maxps[i][0]-point[0])
            p2roximityY = math.fabs(maxps[i][1]-point[1])
            newDistance = math.sqrt(p2roximityX*p2roximityX+p2roximityY*p2roximityY)
            if newDistance < distance :
                point2 = maxps[i]
                point2X = p2roximityX
                distance = newDistance
                
        maxps_orderer.append(point2)
        
    maxps = maxps_orderer
    return maxps

def transflist(initList):
	"""
	transflist is a function that return a list containing, for every element in the initList, a couple (python tuple)
	made by the original element and its successor.
	Example : [1,2,3] -> [[1,2], [2,3], [3,1]]
	@param initList: integer list represent the initial list.
	@return coupleList: list of list of integer, represent the couple list.
	"""
	result = []
	for element in range(len(initList)-1):
		result.append([initList[element], initList[element+1]])
	result.append([initList[-1], initList[0]])
	return result

def support_plane(angle, line):
	"""
	support_plane is a function that from angle and line, return a list containing the 4 coefficients that describe 
	a plane passing through the line.
	@param angle: integer represent the angle used to rotate the planes.
	@param line: couple represent the verts of the line.
	@return planesParam: list that contain the 4 coefficients. 
	"""
	plane1 = PROD([POLYLINE(line), QUOTE([2])])
	plane1 = T([1,2])([-line[0][0], -line[0][1]])(plane1)
	plane1 = ROTN([-angle, [line[1][0] - line[0][0], line[1][1] - line[0][1], 0]])(plane1)
	plane1 = T([1,2])([+line[0][0], +line[0][1]])(plane1)
	#obtain 3 points 
	points = []
	points.append(UKPOL(plane1)[0][0])
	points.append(UKPOL(plane1)[0][1])
	points.append(UKPOL(plane1)[0][2])

	x1 = points[0][0]
	x2 = points[1][0]
	x3 = points[2][0]
	y1 = points[0][1]
	y2 = points[1][1]
	y3 = points[2][1]
	z1 = points[0][2]
	z2 = points[1][2]
	z3 = points[2][2]

	#calculate the vectors
	p1 = np.array([x1, y1, z1])
	p2 = np.array([x2, y2, z2])
	p3 = np.array([x3, y3, z3])

	v1 = p3 - p1
	v2 = p2 - p1 
	# this is a vector normal to the plane
	cp = np.cross(v1, v2)
	a, b, c = cp 

	# This evaluates a * x3 + b * y3 + c * z3 which equals d
	d = np.dot(cp, p3)

	return [a,b,c,d]


def buildRoof(verts, angle, height):
	"""
	buildRoof is a function that return a HPC Model represent the roof from the verts, angle and height.
	@param verts: list of list of integer represent the verts that define the shape of roof bottom.
	@param angle: integer represent the angle used to rotate the planes.
	@param height: integer represent the height of the roof.
	@return roof: HPC Model represent the roof.
	"""
	lines = transflist(verts)

	base = SOLIDIFY(POLYLINE(verts + [verts[0]]))

	planes = []

	for line in lines:
		planes.append(support_plane(angle, line))

	couplePlanes = transflist(planes)

	roofTop = []
	linesEquations = []

	# calculating equations with planes intersection
	for couple in couplePlanes:
		x, y, z = symbols('x y z')
		solved = solve([Eq(couple[0][0]*x+couple[0][1]*y+couple[0][2]*z, couple[0][3]), 
						Eq(couple[1][0]*x+couple[1][1]*y+couple[1][2]*z, couple[1][3])])
		linesEquations.append(solved)
		roofTop.append([round(float(solved[x].subs(z,height)),2), round(float(solved[y].subs(z,height)),2)])

	roofTop.append(roofTop[0])
	terrace = T([3])([height])(SOLIDIFY(POLYLINE(roofTop)))

	coupleLines = transflist(linesEquations)
	roofPitch = []

	#building roof pitches
	for couple in coupleLines:
		base1 = [round(float((couple[0])[x].subs(z,0)),2),round(float((couple[0])[y].subs(z,0)),2),0]
		base2 = [round(float((couple[1])[x].subs(z,0)),2),round(float((couple[1])[y].subs(z,0)),2),0]
		top1 = [round(float((couple[0])[x].subs(z,height)),2),round(float((couple[0])[y].subs(z,height)),2),height]
		top2 = [round(float((couple[1])[x].subs(z,height)),2),round(float((couple[1])[y].subs(z,height)),2),height]
		points = [base1, base2, top2, top1, base1]
		faces = [[1,2,3,4]]
		roofPitch.append(TEXTURE("texture/tetto.jpg")(MKPOL([points, faces, 1])))

	roofPitch = STRUCT(roofPitch)

	return STRUCT([TEXTURE("texture/terrazzo.jpg")(terrace), base, roofPitch])

