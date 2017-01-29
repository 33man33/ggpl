
from pyplasm import *
from numpy import array
import patch
import colors
import random

def punto_medio(a,b):
    x = min(a[0],b[0])+((abs(a[0]-b[0]))/2)
    y = min(a[1],b[1])+((abs(a[1]-b[1]))/2)
    z = min(a[2],b[2])+((abs(a[2]-b[2]))/2)
    e = [ x, y, z ]
    return e

def foglia3():
    one = R([1,3])(PI/4)(MKPOL([[[0,0,0],[0,-0.01,0.02],[-0.005,0,0.04],[0,0.01,0.02]],[[1,2,4],[2,3,4]],False]))
    three = STRUCT([R([1,2])(4*PI/3)(one),R([1,2])(-4*PI/3)(one), \
            R([1,3])(PI/4)(MKPOL([[[0,0,0],[0,-0.01,0.02],[0.01,0,0.04],[0,0.01,0.02]],[[1,2,4],[2,3,4]],False]))])
    return COLOR(colors.BID_GREEN)(STRUCT([T(3)(0.015)(three),T([1,2])([-0.001,-0.001])(CUBOID([0.002,0.002,0.015]))]))

def sphere(R):
    def sphere0 (point):
        u,v = point
        fx = R*COS(u)*COS(v)
        fy = R*COS(u)*SIN(v)
        fz = -R*SIN(u)
        return fx, fy, fz
    return sphere0

def sfera(r):
    dom = PROD([T(1)(-PI/2)(INTERVALS(PI)(15)),INTERVALS(2*PI)(25)])
    return T(3)(r)(MAP(sphere(r))(dom))

def chiomaelement():
    return S(3)(2)(COLOR(colors.BID_GREEN)(sfera(0.3)))

def tronco0():
    dom = Plasm.power(INTERVALS(1)(10),INTERVALS(2*PI)(10))
    profile = BEZIER(S1)([[0.3,0,3.5],[0.15,0,3.5],[0.15,0,0],[0.4,0,0]])
    dom = Plasm.power(INTERVALS(1)(2),INTERVALS(2*PI)(10))
    profile = BEZIER(S1)([[0,0,3.7],[0.3,0,3.7],[0.3,0,3.5]])
    return COLOR(colors.BROWN)(CYLINDER([.28, (10./12)*4.2])(30))

tronco = tronco0()

def srami0():
    celement = T(3)(0.2)(R([1,2])(PI)(chiomaelement()))
    sramo = COLOR(colors.BROWN)(CYLINDER([0.1,0.8])(15))
    sram = STRUCT([sramo,S([1,2,3])([2.9,2.9,2.3])(celement)])
    sramo = T(1)(0.15)(R([1,3])(-1*PI/4)(sramo))
    sramo = STRUCT([sramo,T(1)(0.7)(S([1,2,3])([3,3,2])(celement))])
    for i in range(5):
	el = R([1,2])(i*2*PI/5)(sramo)
        sram = STRUCT([sram,el])
    sram = T(3)(3.5)(sram)
    return sram

srami = srami0()

def ramoElement0(n=10,raggio_base=0.2,altezza_base=0.4):
    foglia = T([1,3])([raggio_base-(raggio_base*0.033),altezza_base/3])(R([1,3])(-3*PI/8)(S([1,2,3])([8,8,6])(foglia3())))
    element = COLOR(colors.BROWN)(TRUNCONE([raggio_base,raggio_base*0.95,altezza_base])(n))
    list=[element]
    for i in range(n):
        random.seed()
	alpha = random.randint(0,n)
	if((alpha%2)==1):
            list += [R([1,2])(i*4*PI/n)(foglia)]
    return STRUCT(list)

ramoElement = ramoElement0()

def ramoLastElement(n=10,raggio=0.2,altezza=0.4,s=1):
    foglia = T([1,3])([raggio-(raggio*0.033),altezza/3])(R([1,3])(-3*PI/8)(S([1,2,3])([8,8,6])(S([1,2,3])([s,s,s])(foglia3()))))
    element = COLOR(colors.BROWN)(CONE([raggio,altezza])(n))
    list=[element]
    for i in range(n):
        random.seed()
	alpha = random.randint(0,n)
	if((alpha%2)==1):
            list += [R([1,2])(i*4*PI/n)(foglia)]
    return STRUCT(list)

def ramo0(n=10,base_h=0.4,base_r=0.2):
    re = ramoElement
    h = base_h
    s = 1
    angle = PI/40
    ramo_1 = T(3)(-0.9*h)(re)
    for i in range(1,20):
	alpha = random.randint(0,n)
        re = R([1,2])(alpha*2*PI/n)(S([1,2,3])([0.95,0.95,0.9])(re))
	h = h*0.9
	s = s*0.95
	ramo_1 = T(3)(-0.9*h)(STRUCT([R([2,3])(angle)(ramo_1),re]))
    ramo_1 = T(3)(-1.0*h)(STRUCT([ramo_1, ramoLastElement(n,s*base_r,3*h,0.9*s)]))
    return T([2,3])([1.6,2.45])(R([2,3])(-PI/2)(ramo_1))

ramo = ramo0()

def multiramo0():
    mult = ramo
    ramo2 = S([1,2,3])([0.5,0.5,0.6])(ramo)
    ramo3 = S([1,2,3])([0.7,0.7,0.7])(ramo)
    mult = STRUCT([mult,
           T([1,2,3])([-0.03,0.1,0.6])(R([1,2])(PI/8)(R([2,3])(-PI/8)(ramo2))),
           T([1,2,3])([-0.03,0.4,1.6])(R([1,2])(-PI/4)(R([2,3])(-PI/8)(ramo2))),
           T([1,3])([0,0.4])(R([1,2])(-PI/3)(R([2,3])(-PI/8)(ramo3)))
	   ])
    return mult

multiramo = multiramo0()

def multirami0():
    mult = T([2,3])([0.07,3.5])(R([2,3])(-PI/8)(multiramo))
    chioma = mult
    for i in range(1,4):
        chioma = STRUCT([chioma,R([1,2])(i*PI/2)(mult)])
    return STRUCT([chioma,
           R([1,2])(PI/3)(T(3)(3.6)(R([2,3])(PI/8)(S(3)(0.6)(multiramo)))),
           R([1,2])(-PI/6)(T(3)(3.6)(R([2,3])(PI/8)(S(3)(0.6)(multiramo))))])

def base0():
    return STRUCT([ COLOR(colors.LIGHT_GREEN)(PROD([T([1,2])([-1,-1])(CUBOID([2,2])),Q(0.05)])),
           T([1,2])([-1.05,-1.05])(COLOR(colors.DIRTY)(DIFF([CUBOID([2.1,2.1,0.1]),T([1,2])([0.05,0.05])(CUBOID([2,2,2]))])))  
	   ])

def base1():
    return STRUCT([ COLOR(colors.LIGHT_GREEN)(PROD([CIRCLE(0.95)([30,1]),Q(0.02)])),
           T(3)(0.03)(COLOR(colors.DIRTY)(TORUS([0.9,1.0])([30,3])))
	   ])

base = base1()

multirami = multirami0()
albero = STRUCT([multirami,tronco])
albero_stilizzato = STRUCT([tronco,srami])
albero_stilizzato_b = STRUCT([base,T(3)(0.05)(albero_stilizzato)])

if __name__ == "__main__":
    VIEW(albero_stilizzato_b)
