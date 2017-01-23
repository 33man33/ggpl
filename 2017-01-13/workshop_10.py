from pyplasm import *
import csv
import src.workshop_08 as create_walls
import src.workshop_07 as create_door_window
import src.workshop_03 as create_stairs
import src.workshop_09 as create_roof

windowx = [2,3,2,3,2]
windowy = [2,3,2,3,2]
p = 15
t = .1
m = 1.09
occurrencwindowy = [[1, 1, 1, 1, 1],
			  [1, 0, 1, 0, 1],
			  [1, 1, 1, 1, 1],
			  [1, 0, 1, 0, 1],
			  [1, 1, 1, 1, 1]]

doorx = [.2, .2, .05, .2, .05, .2, .3, .2, .05, .2 ,.05, .2, .2]
doory = [.2, .2, .05, .2, .05, 1, .05, .2, .05, .2, .2]
occurencdoory = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
				[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 
				[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
				[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
				[1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
				[1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
				[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
				[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

external_walls = STRUCT(create_walls.create_walls('first_model_muri_esterni_1.lines'))
x = (p)/SIZE([1])(external_walls)[0]
y = (p+t)/SIZE([2])(external_walls)[0]
z = x

external_walls2 = create_walls.create_walls('second_model_muri_esterni_1.lines')
externalWalls2 = STRUCT(external_walls2)
x2 = p/SIZE([1])(externalWalls2)[0]
y2 = p+t/SIZE([2])(externalWalls2)[0]
z2 = x2

def create_house(floornum, bases, x, y, z):
	"""
	create_house is a function that return the function that calculate the HPC Model represent the house.
	@param nFloor: represent the number of floors.
	@param bases: String represent the prefix of the .lines files.
	@param x: Float represent the factor to scale and calculate h.
	@param y: Float represent the factor to scale and calculate h.
	@param z: Float represent the factor to scale and calculate h.
	@return create_windows: Function that calculate the HPC Model.
	"""
	def create_windows(windowx, windowy, occurrencwindowy):
		"""
		create_windows is a function that return the function that calculate the HPC Model represent the house.
		@param windowx: Float list of asix X of the window cells
		@param windowy: Float list of asix Y of the window cells
		@param occurrencwindowy: Bool matrix that represent the full cell and empty cell.
		@return create_doors: Function that calculate the HPC Model.
		"""
		def create_doors(doorx, doory, occurencdoory):
			"""
			create_doors is a function that return the function that calculate the HPC Model represent the house.
			@param doorx: Float list of asix X of the door cells.
			@param doory: Float list of asix Y of the door cells.
			@param occurencdoory: Bool matrix that represent the full cells and empty cells.
			@return create_floors: Function that calculate the HPC Model.
			"""
			def create_floors(v, angle, h):
				"""
				create_floors is a function that return the HPC Model represent the house.
				@param v: list of list of integer represent the v that define the shape of roof bottom.
				@param angle: integer represent the angle used to rotate the planes.
				@param h: integer represent the h of the roof.
				@return house: HPC Model represent the house.
				"""
				floors = []
				#building roof model
				with open(v) as file:
					reader = csv.reader(file, delimiter=",")
					new_v = []
					for row in reader:
						new_v.append([float(row[0]), float(row[1])])
					roof = T([3])([floornum*3/z])(create_roof.buildRoof(new_v, angle, h))
					roof = S([1,2,3])([x*m, y*m, z])(roof)
					roof = T([1,2])([-SIZE([1])(roof)[0]*(t-.05), -SIZE([2])(roof)[0]*(t-.05)])(roof)

				for i in range(floornum):
					floor_lines = [bases + '_muri_esterni_'+str(i+1)+'.lines', bases + '_muri_interni_'+str(i+1)+'.lines', bases + '_porte_'+str(i+1)+'.lines', bases + '_finestre_'+str(i+1)+'.lines', bases + '_scale_'+str(i)+'.lines', bases + '_scale_'+str(i+1)+'.lines']
					floor = create_walls.ggpl_building_house(floor_lines, 
						create_door_window.window_creator(windowx,windowy,occurrencwindowy), 
						create_door_window.door_creator(doory, doorx, occurencdoory), 
						create_stairs, i, floornum-1)
					floors.append(floor)
				
				floors = STRUCT(floors)
				return STRUCT([floors, roof])
			return create_floors
		return create_doors
	return create_windows

VIEW(create_house(2, 'first_model', x, y, z)(windowx, windowy, occurrencwindowy)(doorx, doory, occurencdoory)('first_model_muri_esterni_1.lines', PI/5., 3/z))

VIEW(create_house(2, 'second_model', x2, y2, z2)(windowx, windowy, occurrencwindowy)(doorx, doory, occurencdoory)('second_model_muri_esterni_1.lines', PI/5., 3/z2))






