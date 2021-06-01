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
	mode: int = field(default = NORMAL)

	def makePlan(self, mode, floors, maxFloors = 1):
		'''Uses the mode to construct floors, storing them in the floors input,
			then returns a tuple of how many basement floors were created and how
			many non-basement floors were created.'''
		# Get the number of floors to make
		# TODO: Allow multiple floors to be made
		floors.append(Floor(self.width, self.height, level = 0, mode = self.mode))
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