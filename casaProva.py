from pyplasm import *

base = CUBOID([1.05,1.05,0.01])

p1 = CUBOID([0.05,0.05,1]) #pilastro primo della casa

p2 = p3 = p4 = p1 #gli altri pilastri della casa

pt2 = T([1,0,0])([1,0,0])(p2) #traslazione sull'asse x del pilastro numero 2
pt3 = T([0,2,0])([0,1,0])(p3) #traslazione sull'asse y del pilastro numero 3
pt4 = T([1,2,0])([1,1,0])(p4) #traslazione sull'asse y del pilastro numero 4

t1 = CUBOID([1.05,0.05,0.05]) #pilastro "verticale" (sull'asse x)
t2 = CUBOID([0.05,1.05,0.05]) #pilastro "orizzontale" (sull'asse y)

t3 = t1
t4 = t2

#travi di altezza z = 1(quindi alla fine dei pilastri)
tt1 = T([0,0,3])([0,0,1])(t1)
tt3 = T([0,2,3])([0,1,1])(t3)
tt2 = T([0,0,3])([0,0,1])(t2)
tt4 = T([1,0,3])([1,0,1])(t4)

tetto = SIMPLEX(2) #triangolo
tr= R([1,2])(PI/2)(tetto)  #tetto ruotato

te=EXTRUSION(1)(2)(tr) #da triangolo a tetto

casa=STRUCT([base,p1,pt2,pt3,pt4,tt1,tt3,tt2,tt4,te])
VIEW(casa)

