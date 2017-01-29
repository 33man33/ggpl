from pyplasm import *
from numpy import array
import colors

def canestro0():
    tabellone = STRUCT([
                COLOR(colors.BLACK)(DIFF([CUBOID([1.05,1.80,0.05]),T([1,2])([0.05,0.05])(CUBOID([0.95,1.7,0.05]))])),
                COLOR(colors.DIRTY)(T([1,2,3])([0.05,0.05,-0.05])(CUBOID([0.95,1.7,0.05]))),
                (DIFF([T([1,2])([0.05,0.05])(CUBOID([0.95,1.7,0.05])),T([1,2])([0.15,0.55])(CUBOID([0.54,0.70,0.05]))])),
		COLOR(colors.BLACK)(DIFF([T([1,2])([0.15,0.55])(CUBOID([0.54,0.70,0.05])),T([1,2])([0.2,0.6])(CUBOID([0.44,0.60,0.05]))])),
		T([1,2])([0.2,0.6])(CUBOID([0.44,0.60,0.05]))
		])
    rete0 = CYLINDER([0.25,0.02])(30)
    rete = rete0
    for i in range(18):
        rete = TOP([rete,rete0])
    rete = COLOR(colors.WHITE)(SKELETON(1)(rete))
    cesto = COLOR(colors.ORANGE)(STRUCT([
                TORUS([0.22,0.28])([30,10]),
	        T([1,2,3])([-0.36,-0.075,-0.027])(CUBOID([0.1,0.15,0.1]))
	    ]))
    cesto = T([1,2,3]) ([0.1,0.9,0.37]) ( R([1,3])(PI/2) (STRUCT([ cesto, rete ])))
    c1 = T([1,2])([0.05,0.9])(R([1,2])(PI)(R([1,3])(PI/2)(STRUCT([tabellone,cesto]))))
    selem = COLOR(colors.BLUE)(CYLINDER([0.025,2.0])(20))
    ssemi = STRUCT([selem,T(3)(1.99)(R([1,3])(-1*PI/3)(selem)),
            T(3)(1.99)(R([1,3])(-1.5*PI/6)(S(3)(1.21)(selem))),
	    T(1)(0.8)(S(3)(1.395)(selem))])
    selem = T(2)(0.5)(R([2,3])(PI/2)(S(3)(0.5)(selem)))
    str = STRUCT([T(2)(-0.50)(ssemi),T(2)(0.50)(ssemi),T(3)(2)(selem),
          T(3)(1.9)(selem),T([1,3])([0.8,1.9])(selem),\
	  T([1,2,3])([0.4,0.5,1.9])(R([1,2])(PI/2)(S(2)(0.8)(selem))),T([1,2,3])([0.4,-0.5,1.9])(R([1,2])(PI/2)(S(2)(0.8)(selem))),
          T(3)(0.3)(selem),T([1,3])([0.8,0.3])(selem),\
	  T([1,2,3])([0.4,0.5,0.3])(R([1,2])(PI/2)(S(2)(0.8)(selem))),T([1,2,3])([0.4,-0.5,0.31])(R([1,2])(PI/2)(S(2)(0.8)(selem)))
	  ])
    return STRUCT([T([1,3])([1.7,2.8])(c1),str])

canestro = canestro0()

def campo_basket0(x=15,y=20):
    campo = TEXTURE('texture/basketball_field.png')(T(2)(-1*(x/2.0))(CUBOID([y,x,0.05])))
    campo = T(3)(-0.03)(STRUCT([COLOR(colors.GROUND)(T([1,2])([-2,-1*((x+4)/2.0)])\
            (DIFF([CUBOID([y+4,x+4,0.05]),T([1,2])([2,2])(CUBOID([y,x,0.05]))]))),campo]))
    return STRUCT([campo,T(1)(-1.2)(canestro),T(1)(y+1.2)(S(1)(-1)(canestro))])

campo_basket = campo_basket0()

def campo_calcio0():
    campo = T(3)(0.05)(S(3)(-1)(TEXTURE('texture/soccer_field_1.png')(T(2)(-1*(50/2.0))(CUBOID([30,25,0.05])))))
    porta = COLOR(colors.DIRTY)(STRUCT([
            T([2,3])([3.5,0.05])(CUBOID([0.1,0.1,2.44])),
            T([2,3])([-3.6,0.05])(CUBOID([0.1,0.1,2.44])),
            T([2,3])([-3.6,2.49])(R([2,3])(-1*PI/2)(CUBOID([0.1,0.1,7.2]))),
            T([1,2,3])([0.04,3.5,2.397])(R([1,3])(5*PI/8)(CUBOID([0.1,0.1,1.3]))),
            T([1,2])([-1.196,3.5])(CUBOID([0.05,0.05,1.99])),
            T([1,2,3])([0.04,-3.6,2.397])(R([1,3])(5*PI/8)(CUBOID([0.1,0.1,1.3]))),
            T([1,2])([-1.196,-3.6])(CUBOID([0.1,0.1,1.99])),
            T([1,2,3])([-1.196,-3.6,1.99])(R([2,3])(-1*PI/2)(CUBOID([0.1,0.1,7.2]))),
	    ]))
    return STRUCT([campo,
                   T([1,2,3])([2,-12,0.05])(porta),
                   T([1,2,3])([28,-12,0.05])(S(1)(-1)(porta))
		   ])

campo_calcio = campo_calcio0()
campo_calcio = S([1,2])([2.0/3.0,2.0/3,0])(campo_calcio)

def gradoni():
    gradone = COLOR(colors.DIRTY)(CUBOID([1.0,40.0,1.0]))
    gradone_sit = STRUCT([gradone,T([1,3])([0.1,1.0])(COLOR(colors.BROWN)(CUBOID([0.9,40.0,0.1])))])
    obj = STRUCT([
                 T(1)(1)(S(3)(3)(gradone)),
                 T(1)(2)(S(3)(2)(gradone)),
                 T(1)(3)(gradone),
		 T([1,3])([1,3])(gradone_sit),
		 T([1,3])([2,2])(gradone_sit),
		 T([1,3])([3,1])(gradone_sit),
		 T([1,3])([4,0])(gradone_sit),
                 ])
    obj = STRUCT([obj,T(1)(1)(S(1)(-1)(obj)),S(3)(4)(gradone)])
    return obj

spalti = gradoni()

if __name__ == "__main__":
    VIEW(campo_basket)
    VIEW(campo_calcio)
    VIEW(spalti)

