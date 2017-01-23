from pyplasm import *

def circle(r):
	def circle0(p):
		alpha = p[0]
		return [r*COS(alpha), r*SIN(alpha)]
	return circle0

B = COLOR(Color4f([193/255., 154/255., 107/255., 1]))

def remodular(X, Y, occurrency, dx, dz):
	"""
	remodular is a function that scale the empty space of a window base on dx and dz.
	@param X: Float list of asix X of the windows cells
	@param Y: Float list of asix Y of the windows cells
	@param occurrency: Bool matrix that represent the full cell and empty cell.
	@param dx: represent a X coordinate of the box
	@param dz: represent a Z coordinate of the box	
	"""
	sy = sum(Y) 
	sx = sum(X)
	vY = [False]*len(Y)
	for y in range(len(Y)):
		update = True
		for x in range(len(X)):
			if(occurrency[x][y] == False):
				update = False 
		if(update):
			sy = sy - Y[y]
			sx = sx - X[y]
			dx = dx - X[y]
			dz = dz - Y[y]

	for x in range(len(X)):
		modifyX = False
		for y in range(len(Y)):
			if(occurrency[x][y] == False and vY[y] == False):
				Y[y] = (dz * Y[y])/sy
				vY[y] = True
				modifyX = True
			if(occurrency[x][y] == False and vY[y] == True and not modifyX):
				modifyX = True
		if(modifyX):
			X[x] = (dx * X[x])/sx


def ggpl_window(X,Y,occurrency):
    def window(dx,dy,dz):
        arc = MAP(circle(dx/2.))(INTERVALS(1*PI)(30))
        arc = OFFSET([0,0,.06])(PROD([Q(dy),arc]))
        arc = T([1,3])([dx/2.,dz])(R([1,2])(PI/2)(arc))
        arc = BROWN(arc)
        
        glass = R([2,3])(PI/2)(semiCircle(dx/2.))
        glass = TRASPARENT( T([1,2,3])([dx/2.,dy/2,dz])(glass))
        
        glass_tot = TRASPARENT(T(2)(dy/2)(CUBOID([dx-0.04,(dy/4),dz-0.02])))
        
        handle = COLOR(BLACK)(CUBOID([.03,.03,.02]))
        handle2 = T(3)([-.1])(handle)
        handles = STRUCT([handle,handle2])
        handle = T([1,2,3])([dx/2.- .1, dy/2 + .05, dz/2. + .04])(handles)
        handle2 = T([1,2,3])([dx/2.+ .1, dy/2+ .05, dz/2. + .04])(handles)
        
        beam = BROWN(CUBOID([.04,.08,.3]))
        beam3 = T([1,2,3])([(dx/2)-.03,dy/2 -.03,dz])(beam)
        beam1 = T([1,2,3])([(dx/2)-.03,dy/2-.03,dz])(R([1,3])(PI/4)(beam))
        beam2 = BROWN(T([1,2,3])([(dx/2)-.038,dy/2-.03,dz])(R([1,3])(-PI/4)(CUBOID([.04,.08,.36]))))
        
        ggpl_final(X,Y,occurrency, dx,dy,dz)
        final = support_function(X,Y,occurrency)
        final.append(BOX([dx,dz,dy]))
        final_tot = STRUCT(final)
        final_tot = BROWN(MAP([S1,S3,S2])(PROD([final_tot, Q(dy)])))
        
        #VIEW(STRUCT([final_tot,arc,beam3,beam2,beam1]))
        return STRUCT([final_tot,arc,glass,handle,handle2,beam3,beam1,beam2,glass_tot])
    return window


def ggpl_door(X,Y,occurrency):
    def door(dx,dy,dz):
        
        circ = JOIN(MAP(circle(dx/6.))(INTERVALS(2*PI)(30)))
        circ = MAP([S1,S3,S2])(PROD([circ, Q(dy/4.)]))
        circ = BROWN(T([1,2,3])([dx/2.,dy-dy/4.+0.01,dz/2.])(circ))
        
        handle = COLOR(BLACK)(CUBOID([.06,.06,.04]))
        handle2 = COLOR(BLACK)(CUBOID([.06,.15,.04]))
        handle = T([1,2,3])([dx/2, dy, dz/2. ])(handle)
        handle2 = T([1,2,3])([dx/2+.06, dy+.06, dz/2.])(R([1,2])(PI/2)(handle2))
        handles = STRUCT([handle,handle2])
        
        
        beam = BROWN(CUBOID([dx/30,dy,dz+.2]))
        beam1 = T(3)(.1)(R([1,3])(-PI/5.8)(beam))
        beam2 = BROWN(T([1,3])([dx-.06,.04])(R([1,3])(PI/5.9)(beam)))
        beam3 = BROWN(CUBOID([dz/35.,dy,dx]))
        beam3 = T([1,3])([dx,dz/2.])(R([1,3])(PI/2)(beam3))

        final = support_function(X,Y,occurrency)
    
        final.append(BOX([dx,dz,dy]))
        final_tot = STRUCT(final)
        final_tot = PROD([final_tot, Q(dy)])
        final_tot = MAP([S2,S3,S1])(final_tot)
        final_tot = S([1,2,3])([dx/SIZE([1])(final_tot)[0], dy/SIZE([2])(final_tot)[0], dz/SIZE([3])(final_tot)[0]]) (final_tot)
        final_tot = BROWN(final_tot)
        
        glass = CUBOID([dx-0.1, dy/4., dz-0.2])
        glass = T([1,2,3])([dx*0.04,dy/8., dz*0.04])(glass)
        glass = TRASPARENT(glass)
        
        return STRUCT([final_tot, circ, glass,handles,beam1,beam2,beam3])
    return door

def window_creator(X,Y,occurrency):
	"""
	window_creator is a function that generate HPC Model represent the window, parametric by dx, dy and dz.
	@param X: Float list of asix X of the window cells
	@param Y: Float list of asix Y of the window cells
	@param occurency: Bool matrix that represent the full cell and empty cell.
	@return windows_aux: function that return a HPC Model.
	"""
	def window_aux(dx,dy,dz):
		"""
		window_aux is the second level function of window_creator.
		@param dx: represent the X value of the box that contain the window
		@param dy: represent the Y value of the box that contain the window
		@param dz: represent the Z value of the box that contain the window
		@return HPC Model: represent the window.
		"""
		remodular(X,Y,occurrency, dx, dz)
		result = []
		for x in range(len(X)):
			y_quotes = []
			x_sum = sum(X[:x])
			for y in range(len(Y)):
				if(occurrency[x][y] == False):
					y_quotes.append(-Y[y])
				else:
					y_quotes.append(Y[y])
			result.append(PROD([ QUOTE([-x_sum, X[x]]), QUOTE(y_quotes)]))
		result.append(BOX([dx,dz,dy]))
		res = PROD([STRUCT(result), Q(dy)])
		res = B(STRUCT([MAP([S1,S3,S2])(res)]))
		return STRUCT([res])
	return window_aux



def door_creator(XDoor,YDoor,occurrency):
	"""
	door_main is a function that generate the HPC Model represent the door, parametric by dx,dy and dz.
	@param XDoor: Float list of asix X of the door cells.
	@param YDoor: Float list of asix Y of the door cells.
	@param occurency: Bool matrix that represent the full cells and empty cells.
	@return door_aux: function that return a HPC Model.
	"""
	def door_aux(dx,dy,dz):
		"""
		door_aux is the second level function of door_main. 
		@param dx: represent the X value of the box that contain the door
		@param dy: represent the Y value of the box that contain the door
		@param dz: represent the Z value of the box that contain the door
		@return HPC Model: represent the door.
		"""
		result = []
		door1 = JOIN(MAP(circle(sum(YDoor[4:9])/2.*.6))(INTERVALS(2*PI)(50)))
		door1 = PROD([door1, Q(dy/4.)])
		door1 = MAP([S1,S3,S2])(door1)
		door1 = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(T([1,2,3])([dx/2., dy-dy/4.+0.01, dz/2.])(door1))
		for x in range(len(XDoor)):
			y_quotes = []
			x_sum = sum(XDoor[:x])
			for y in range(len(YDoor)):
				if(occurrency[x][y] == False):
					y_quotes.append(-YDoor[y])
				else:
					y_quotes.append(YDoor[y])
			result.append(PROD([ QUOTE([-x_sum, XDoor[x]]), QUOTE(y_quotes)]))
		result.append(BOX([dx,dz,dy])) 
		res = MAP([S2,S3,S1])(PROD([STRUCT(result), Q(dy)]))
		res = COLOR(Color4f([93/255., 94/255., 107/255., 1]))(S([1,2,3])([dx/SIZE([1])(res)[0], dy/SIZE([2])(res)[0], dz/SIZE([3])(res)[0]]) (res))
		glass = CUBOID([SIZE([1])(res)[0]*0.9, dy/4.*0.9, SIZE([3])(res)[0]*0.9])
		glass = T([1,2,3])([dx*0.05, dy/8. + dy*0.05, dz*0.05])(glass)
		glass = COLOR(Color4f([38/255.,226/255.,189/255.,1]))(glass)
		return STRUCT([res, door1, glass])
	return door_aux





