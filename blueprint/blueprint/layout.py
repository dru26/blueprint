# global imports
from dataclasses import dataclass, field
from random import randint, shuffle

# local imports
from room import Room
from wall import Wall
from point import Point
from door import Door, DWIDTH
from direction import HORIZONTAL, VERTICAL

@dataclass(frozen = False, order = False)
class Layout:
	points: list[Point] = field()
	scale: float = field(default = 1)
	def make(self, scale = None):
		if scale == None: scale = self.scale
		walls = []
		for i in range(len(self.points) - 1):
			walls.append(Wall(self.points[i] * scale, self.points[i + 1] * scale))
		walls.append(Wall((self.points[-1] * scale), self.points[0] * scale))
		shuffle(walls)
		if walls[0].p1.x == walls[0].p2.x:
			p = Point(walls[0].p1.x, randint(min(walls[0].p1.y, walls[0].p2.y) + 1 + DWIDTH, max(walls[0].p1.y, walls[0].p2.y) - 1 - DWIDTH))
			walls[0].doors.append(Door(p, VERTICAL))
		else:
			p = Point(randint(min(walls[0].p1.x, walls[0].p2.x) + 1 + DWIDTH, max(walls[0].p1.x, walls[0].p2.x) - 1 - DWIDTH), walls[0].p1.y)
			walls[0].doors.append(Door(p, HORIZONTAL))
		return Room(walls)


# Starting layouts
SQUARE = Layout([Point(0, 0), Point(1,0), Point(1,1), Point(0,1)], 20)
RECT = Layout([Point(0, 0), Point(1.5,0), Point(1.5,1), Point(0,1)], 20)
TSHAPE = Layout([Point(1, 0), Point(2,0), Point(2,3), Point(1,3), Point(1,2),
	Point(0,2), Point(0,1), Point(1,1)], 20)
