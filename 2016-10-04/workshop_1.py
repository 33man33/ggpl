from pyplasm import *

#(bx,bz) (given dimensions of beam section)
#(px,py) (given dimensions of pillar section)
#[dy1,dy2,...] (distances between axes of the pillars)
#[hz1,hz2,...] (interstory heights)

#x = [.1,-.05,.001, -0.5]
#a = QUOTE(x*5)
#aa = PROD([a,a])
#aaa = PROD([aa,a])
#VIEW(a)
#VIEW(aa)
#VIEW(aaa)


bx = by = .6	
bz = .2

px = py = .2			

dy = 3.4
dy2 = 2.4		#distanza dei pilastri
hz = 2.8
hz1 = 2.0

"""acquisizione dati tramite opportuni cicli for ed istanziati in queste 2 tuple e liste"""
dim_beam = (bx,bz)
dim_pillar=(px,py)
dis_pillars = [dy,dy2]
heights_interstory = [hz,hz1]


def struttura(dim_beam,dim_pillar,dis_pillars,heights_interstory):
	
	x_base = QUOTE([px*3, - dis_pillars[0]] * 6)   
	y_base = QUOTE([py*3, - dis_pillars[0]] * 4)  

	""" prodotto cartesiano"""
	base = INSR(PROD)([x_base,y_base,Q(.2)])  #base complete, alta 0.2
	
	""" costruzione dei pilastri traslati opportunamente tramite lista delle distanze di pilastri """
	x_pilastri = QUOTE([-dim_pillar[0], dim_pillar[0], -dim_pillar[0], - dis_pillars[0] ] * 6)	#dim. x del pilastro(ne creo 6) 
	y_pilastri = QUOTE([-dim_pillar[0], dim_pillar[0], -dim_pillar[0], - dis_pillars[0] ] * 4)	#dim. y del pilastro(ne creo 4)	
	pilastri = INSR(PROD)([x_pilastri,y_pilastri,QUOTE([-.2,heights_interstory[0]]*5 )])#inserisco 5 piani, con altezza = quella dei pili   
	
	x_travi_assey = QUOTE([dim_beam[0], -(dis_pillars[0])] *6)
	y_travi_assey = QUOTE([4*(dis_pillars[0]) -dim_beam[0]])
	travi_assey = INSR(PROD)([x_travi_assey,y_travi_assey,QUOTE([-dim_beam[1] ,.2 - heights_interstory[0], dim_beam[1]] * 5)])

	x_travi_assex = QUOTE([dis_pillars[0]*6])
	y_travi_assex = QUOTE([dim_beam[0],-dis_pillars[0]] * 4)
	travi_assex = INSR(PROD)([x_travi_assex,y_travi_assex,QUOTE([-dim_beam[1] ,.2 - heights_interstory[0], dim_beam[1]] * 5)])
	
	return (base,pilastri,travi_assey,travi_assex)


test_base = struttura(dim_beam,dim_pillar,dis_pillars,heights_interstory)
VIEW(test_base[0])

VIEW(STRUCT([test_base[0],test_base[1]]))

VIEW(STRUCT([test_base[0],test_base[1],test_base[2]]))

VIEW(STRUCT([test_base[0],test_base[1],test_base[2],test_base[3]]))


""" prova di travi piene """
x_travi = QUOTE([bx,(bx*6) + ( dy*5)])
y_travi = QUOTE([by,(by*4) + ( dy*3) - 0.2])

travi = INSR(PROD)([x_travi,y_travi,QUOTE([bz ,.2 - hz, bz] * 5)])

VIEW(STRUCT([test_base[0],test_base[1],travi]))




