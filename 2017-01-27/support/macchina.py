from pyplasm import *
from numpy import array
import random
import colors

colori = [ colors.PURPLE, colors.BLUE, colors.RED ]

def telaio(larghezza=1.3):
    points =  [[0.2,0],[2.8,0],[3,0.1],[3,0.4],[2.9,0.5],[2.4,0.7],
              [1.85,1.2],[0.6,1.2],[0.3,0.7],[0.1,0.6],[0,0.4],[0,0.1],[0.2,0],
              [2.25,0.75],[1.20,0.75],[1.15,0.75],[0.45,0.75],
              [1.80,1.15],[1.20,1.15],[1.15,1.15],[0.65,1.15]]
    fiancata= MKPOL([(points),[[13,12,11,10,9,6,5,4,3,2,1],[6,14,18,7],
	            [7,18,19,20,21,8],[21,17,9,8],[9,17,16,15,14,6],[15,16,20,19]],False])
    telaio = S(3)(-1)(R([2,3])(-PI/2)(PROD([fiancata,Q(larghezza)])))
    telaio = DIFF([telaio,T([2,3])([0.05,0.75])(CUBOID([3,larghezza-0.1,0.4]))])
    ruota_rdx = T(1)(0.7)(R([2,3])(-PI/2)(PROD([CIRCLE(0.35)([8,1]),Q(0.3)])))
    telaio = DIFF([telaio,ruota_rdx,T(1)(1.60)(ruota_rdx),
             T(2)(larghezza-0.3)(ruota_rdx),T([1,2])([1.60,larghezza-0.3])(ruota_rdx)])
    return telaio

telaio_base = telaio()
telai = []
for i in range(len(colori)):
    telai += [ COLOR(colori[i])(telaio_base) ]


def elementi(larghezza=1.3):
    fari = T([1,2,3])([3,0.05,0.2])(COLOR(YELLOW)(CUBOID([0.02,0.3,0.15])))
    fari = STRUCT([fari,T(2)(larghezza-0.4)(fari)])
    fari_posteriori = STRUCT([T([1,2,3])([-0.02,0.1,0.2])(COLOR(YELLOW)(CUBOID([0.02,0.1,0.1]))),
                              T([1,2,3])([-0.02,0.1,0.3])(COLOR(RED)(CUBOID([0.02,0.1,0.1])))])
    fari_posteriori = STRUCT([fari_posteriori,T(2)(larghezza-0.3)(fari_posteriori)])
    targhe = T([1,2,3])([-0.02,((larghezza/2)-0.2),0.15])(COLOR(colors.DIRTY)(CUBOID([0.02,0.4,0.15])))
    targhe = STRUCT([targhe,T(1)(3.02)(targhe)])
    vetri = COLOR(CYAN)(T(2)(0.05)(S(3)(-1)(R([2,3])(-PI/2)(PROD([
            MKPOL([[[0.45,0.75],[2.25,0.75],[1.80,1.15],[0.65,1.15]],[[1,2,3,4]],FALSE]),
	    Q(larghezza-0.1)])))))
    return STRUCT([fari,fari_posteriori,targhe,vetri])
    
fari_targhe_vetri = elementi()

def ruota0():
    return T([1,3])([0.7,0.05])(R([2,3])(-PI/2)(STRUCT([
           COLOR(colors.BLACK)(DIFF([PROD([CIRCLE(0.25)([16,1]),Q(0.3)]),PROD([CIRCLE(0.15)([16,1]),Q(0.3)])])),
           COLOR(colors.SILVER)(T(3)(-0.02)(PROD([CIRCLE(0.15)([16,1]),Q(0.34)]))) ])))

ruota = ruota0()

def ruote0(larghezza=1.3):
    return STRUCT([ruota,T(1)(1.60)(ruota),T(2)(larghezza-0.3)(ruota),T([1,2])([1.60,larghezza-0.3])(ruota)])

ruote = ruote0()

def antenna0():
    return T([1,2,3])([0.7,0.65,1.2])(COLOR(colors.BLACK)(TOP([T([1,2])([-0.04,-0.04])(CUBOID([0.06,0.06,0.03])),
           T([1,2])([-0.004,-0.004])(CUBOID([0.006,0.006,0.2]))])))

antenna = antenna0()

anyth = STRUCT([fari_targhe_vetri,ruote,antenna])

macchine = []
for i in range(len(telai)):
    macchine += [ T([1,2,3])([0.3,-0.65,0.2])(STRUCT([telai[i],anyth])) ]

def random_car():
    random.seed()
    return macchine[random.randint(0,len(macchine)-1)]

def park0():
    return T([2,3])([-1,0.005])(SOLIDIFY(STRUCT([POLYLINE([[0,0],[0,2],[3.5,2],[3.5,0]]), \
                                                 POLYLINE([[0.1,0.1],[0.1,1.9],[3.4,1.9],[3.4,0.1]])])))

park = park0()

def fullpark(color=0):
    return STRUCT([park,macchine[color]])

fullparks = []
for i in range(len(colori)):
    fullparks += [fullpark(i)]

def parkchance(chance=0):
    random.seed()
    i = random.randint(0,chance+1)
    if (i<len(macchine)):
        result = fullparks[i]
    else:
        result = park
    return result
    
def parkline(num=20,chance=5):
    obj = T(2)(2)(parkchance(chance))
    for i in range(num-1):
        obj = T(2)(2)(STRUCT([obj,parkchance(chance)]))
    return T(2)(-1)(obj)

def parkline2(num=6,chance=5):
    obj = T([1,2])([-2,+2])(parkchance(chance))
    for i in range(num-1):
        obj = T([1,2])([-2,+2])(STRUCT([obj,parkchance(chance)]))
    return R([1,2])(-PI/4)(obj)

if __name__ == "__main__":
    VIEW(parkline(6,4))
    VIEW(parkline2(6,4))
