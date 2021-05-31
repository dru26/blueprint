# global variables
NORMAL = 0
FAST = 1

# global imports
from dataclasses import dataclass, field
from random import shuffle

# local imports
from .point import Point
from .rooms import getRooms, getRandomRoom
from .floor import Floor

@dataclass(frozen = True, order = False)
class Plotter:
	width: int = field()
	height: int = field()
	_optimize: int = field(default = NORMAL)

	def makePlan(self, mode, floors, maxFloors = 1):
		# Get the number of floors to make
		# TODO: Allow multiple floors to be made
		floors.append(Floor(self.width, self.height, 0))
		# Setup the room list and insertion points for the floor
		insertion_points = [Point(0, 0)]
		rooms = getRooms(mode)

		# Put rooms into the floor randomly
		# TODO: Allow multiple floors to be made
		cur_floor = floors[0]
		while len(insertion_points) > 0:
			#print(insertion_points)
			# Get room if we have inserted all the required ones
			if len(rooms) == 0: rooms.append(getRandomRoom())
			# Insert room and check if it was inserted
			if cur_floor.insert(insertion_points[0], rooms[0]):
				insertion_points.append(insertion_points[0] + Point(rooms[0].width, 0))
				insertion_points.append(insertion_points[0] + Point(0, rooms[0].height))
				del rooms[0]
			del insertion_points[0]
			shuffle(insertion_points)
		# return the number of floors on the basement and upper levels
		# TODO: Allow multiple floors to be made
		return (0, 1)

	def combineRooms(self, room1, room2):
		# Update visuals
		for x in range(set_room.offsetx(), set_room.offsetx() + set_room.x):
			for y in range(set_room.offsety(), set_room.offsety() + set_room.y):
				if not self.inBounds(Point(x, y)):
					continue
				self.grid[y][x] = copy_id

		# Update adjacency matrix

	def designRoom(self):
		pass

	def drawReplace(self, grid, width = None, height = None, offset = None):
		pass

	def drawOutline(self, grid):
		pass

	def insertRoom(floorplan, insert, floor, id_):
		floorplan.setFloor(insert[0], floor.width, floor.height, id_, floor)

		insert.append(Point(insert[0].x + floor.width, insert[0].y))
		insert.append(Point(insert[0].x, insert[0].y + floor.height))

		insert.pop(0)

		# shuffle insertion points for randomness
		shuffle(insert)

		return id_ + 1

	def doorify(floorplan):
		pass

	def fill(floorplan, mode):


		while len(insert) > 0:
			#print()
			space = floorplan.getSpaceAt(insert[0])
			# remove insertion if there is no room to add (attempting to insert at wall)
			if space == None:
				insert.pop(0)
				continue
			# if the floorplan is too small to insert a room, insert filler and remove the insertion
			if not isValid(space):
				if space.x > space.y:
					insert[0].y -= 1
					floorplan.extend(floorplan.get(insert[0]), 'y', space.y)
					insert.append(Point(insert[0].x + floorplan.getSpace(insert[0]).width, insert[0].y))
				else:
					insert[0].x -= 1
					floorplan.extend(floorplan.get(insert[0]), 'x', space.x)
					insert.append(Point(insert[0].x, insert[0].y + floorplan.getSpace(insert[0]).height))
				insert.pop(0)
				continue
			# there theoretically exists a room for this insertion: insert it
			room = getNext()
			if floorplan.fits(insert[0], room):
				id_ = insertRoom(floorplan, insert, room, id_)
				continue
			# try and flip the room
			room.flip()
			if floorplan.fits(insert[0], room):
				id_ = insertRoom(floorplan, insert, room, id_)
				continue
			if not isFail():
				floorplan = Blueprint(floorplan.width, floorplan.height)
				insert = [Point(0, 0)]
				prepare(mode)
				id_ = 1