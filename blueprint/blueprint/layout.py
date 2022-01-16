# global imports
from dataclasses import dataclass, field
from random import randint

# local imports
from room import Room
from wall import Wall
from point import Point
from door import Door
from direction import HORIZONTAL, VERTICAL, NORTH, SOUTH, EAST, WEST

@dataclass(frozen = False, order = False)
class Layout:
	points: list[Point] = field()
	scale: float = field(default = 1)

	def make(self, params, scale = None):
		if scale == None: scale = self.scale
		walls = []
		for i in range(len(self.points) - 1):
			walls.append(Wall((self.points[i] * scale).round(), (self.points[i + 1] * scale).round()))
		walls.append(Wall((self.points[-1] * scale).round(), (self.points[0] * scale).round()))
		room = Room(walls)
		i = randint(0, len(room.walls) - 1)
		if room.walls[i].direction == VERTICAL:
			y1 = min(room.walls[i].p1.y, room.walls[i].p2.y) + 1 + params.door_size
			y2 = max(room.walls[i].p1.y, room.walls[i].p2.y) - 1 - params.door_size
			p = Point(room.walls[i].p1.x, randint(y1, y2))
			room.walls[i].doors.append(Door(p, room.walls[i].interior, params.door_size))
		elif room.walls[i].direction == HORIZONTAL:
			x1 = min(room.walls[i].p1.x, room.walls[i].p2.x) + 1 + params.door_size
			x2 = max(room.walls[i].p1.x, room.walls[i].p2.x) - 1 - params.door_size
			p = Point(randint(x1, x2), room.walls[i].p1.y)
			room.walls[i].doors.append(Door(p, room.walls[i].interior, params.door_size))
		return room

# Starting layouts
SQUARE = [Point(0,0), Point(1,0), Point(1,1), Point(0,1)]
RECT = [Point(0,0), Point(1.5,0), Point(1.5,1), Point(0,1)]
TSHAPE = [Point(1,0), Point(2,0), Point(2,3), Point(1,3), Point(1,2),
	Point(0,2), Point(0,1), Point(1,1)]
