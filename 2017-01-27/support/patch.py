
from pyplasm import *

def PATCHEDSOLIDIFY(pol):

	box=Plasm.limits(pol)
	xmin=box.p1[1]
	xmax=box.p2[1]
	ymin=box.p1[2]
	ymax=box.p2[2]
	xsize=xmax-xmin
	ysize=ymax-ymin

	pol = T([1,2])([-xmin,-ymin])(pol)
	pol = S([1,2])([1./xsize, 1./ysize])(pol)
	far_point=2

	def InftyProject(pol):
		verts,cells,pols=UKPOL(pol)
		verts=[[far_point] + v[1:] for v in verts]
		return MKPOL([verts,cells,pols])

	def IsFull(pol):
		return DIM(pol)==RN(pol)

	ret=SPLITCELLS(pol)
	ret=[JOIN([pol,InftyProject(pol)]) for pol in ret]
	ret = XOR(FILTER(IsFull)(ret))

	ret = S([1,2])([xsize, ysize])(ret)
	ret = T([1,2])([xmin,ymin])(ret)
	return ret
