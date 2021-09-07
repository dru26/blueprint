# global imports
from dataclasses import dataclass, field
from random import randint, shuffle

# local imports
from room import Room
from wall import Wall
from point import Point
from door import Door, DWIDTH
from direction import HORIZONTAL, VERTICAL, NORTH, SOUTH, EAST, WEST

@dataclass(frozen = False, order = False)
class Layout:
	points: list[Point] = field()
	scale: float = field(default = 1)
	def make(self, scale = None):
		if scale == None: scale = self.scale
		walls = []
		for i in range(len(self.points) - 1):
			walls.append(Wall((self.points[i] * scale).round(), (self.points[i + 1] * scale).round()))
		walls.append(Wall((self.points[-1] * scale).round(), (self.points[0] * scale).round()))
		shuffle(walls)
		room = Room(walls)
		print(room)
		print(walls[0].p1.x == walls[0].p2.x)
		if walls[0].p1.x == walls[0].p2.x:
			p = Point(walls[0].p1.x, randint(min(walls[0].p1.y, walls[0].p2.y) + 1 + DWIDTH, max(walls[0].p1.y, walls[0].p2.y) - 1 - DWIDTH))
			if (room.contains(p + (0.5, 0), VERTICAL)):
				walls[0].doors.append(Door(p, EAST))
			else:
				walls[0].doors.append(Door(p, WEST))
		else:
			p = Point(randint(min(walls[0].p1.x, walls[0].p2.x) + 1 + DWIDTH, max(walls[0].p1.x, walls[0].p2.x) - 1 - DWIDTH), walls[0].p1.y)
			if (room.contains(p + (0, 0.5), HORIZONTAL)):
				walls[0].doors.append(Door(p, SOUTH))
			else:
				walls[0].doors.append(Door(p, NORTH))
		return room

# Starting layouts
SQUARE = [Point(0, 0), Point(1,0), Point(1,1), Point(0,1)]
RECT = [Point(0, 0), Point(1.5,0), Point(1.5,1), Point(0,1)]
TSHAPE = [Point(1, 0), Point(2,0), Point(2,3), Point(1,3), Point(1,2),
	Point(0,2), Point(0,1), Point(1,1)]
