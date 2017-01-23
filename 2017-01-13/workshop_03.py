from pyplasm import *
import math

B = COLOR(Color4f([193/255., 154/255., 107/255., 1]))

def creatorStep(tread_prov,widt_prov,riser_prov,height_axis):
    step = CUBOID([tread_prov,widt_prov,riser_prov])
    step = STRUCT([T(3)(height_axis),step])
    base = CUBOID([tread_prov-tread_prov/8,riser_prov,height_axis])
    base = STRUCT([T(1)(tread_prov/8),T(2)(widt_prov/2-riser_prov/2),base])
    axis = CUBOID([riser_prov,riser_prov,height_axis+riser_prov])
    axis = STRUCT([T(1)(tread_prov),T(2)(widt_prov/2-riser_prov/2),axis])
    step = STRUCT([step,base,axis])
    return step

def creator_stepSimple(stepNumber, tread, riser, stepWidth):
    steps = []
    verts =[[tread,0],[tread,riser*2],[tread*2,riser*2],[tread*2,riser] ]
    cells =[[1,2,3,4] ]
    step2d = MKPOL([verts,cells,None])
    firstStep = CUBOID([tread,riser,stepWidth])
    steps.append(firstStep)
    for i in range(int(stepNumber-1)):
        steps.append(T([1,2])([(tread*i),riser*i])(PROD([step2d,Q(stepWidth)])))
    return steps

def ggpl_stairCase(dx, dy, dz):
    riser = 0.17
    tread = 0.35
    number_step = (int)(dz/(riser*3))
    platformX = dx/3.
    platformY = dy-tread*(number_step)
    stairs = creator_stepSimple(number_step,tread,riser,platformX)
    platform = CUBOID([platformY,riser,platformX+.01])
    stairs.append(T([1,2])([tread*number_step,riser*(number_step-1)])(platform))
    stair_two = creator_stepSimple(number_step,tread,riser,platformY)
    stair_two = R([1,3])(PI/2)(STRUCT(stair_two))
    stair_two = T([1,2,3])([dy, riser*(number_step-1),platformX-tread])(stair_two)
    stairs.append(stair_two)
    stairs.append(T([1,2,3])([tread*number_step,2*riser*(number_step-1),tread*(-1+number_step+platformX/tread)])(platform))
    stair_three = creator_stepSimple(number_step,tread,riser,platformX)
    stair_three = R([1,3])(PI)(STRUCT(stair_three))
    stair_three = T([1,2,3])([tread*number_step,2*riser*(number_step-1),((platformX*2)+tread*(number_step-1))])(stair_three)
    stairs.append(stair_three)
    final_stairs = MAP([S1,S3,S2])(STRUCT(stairs))
    return final_stairs


def generate_steps(stepNumber, tread, riser, stepWidth):
	
	step2d = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])
	steps = []
	firstStep = CUBOID([tread, riser, stepWidth])
	steps.append(firstStep)

	for i in range(int(stepNumber-1)):
		steps.append(T([1,2])([(tread*i), riser*i])(PROD([step2d, Q(stepWidth)])))

	return steps

def ggpl_single_stair(dx, dy, dz):
	riser = dz/20.
	stepNumber = 20

	if(dx>dy):
		tread1 = dx/(stepNumber)
		stepWidth = dy
	else:
		tread1 = dy / (stepNumber)
		stepWidth = dx

	stairs = generate_steps(stepNumber, tread1, riser, stepWidth)

	stairs = B(MAP([S1,S3,S2])(STRUCT(stairs)))

	return stairs
