# global imports
from dataclasses import dataclass, field
from random import shuffle

# local imports
from wall import Wall
from point import Point
from direction import HORIZONTAL, VERTICAL

@dataclass(frozen=False, order=False)
class Room:
	'''A list of walls.'''
	walls: list[Wall] = field()
	offset: Point = field(default = Point())
	bounds: tuple = field(init = False)

	def __post_init__(self):
		# If only two walls are passed in, assume rectangular room and make
		# the missing walls
		if len(self.walls) == 2:
			wall1 = Wall(self.walls[0].p1, self.walls[1].p1)
			wall2 = Wall(self.walls[0].p2, self.walls[1].p2)
			if Wall.getIntersection(wall1, wall2):
				self.walls.append(Wall(self.walls[0].p1, self.walls[1].p2))
				self.walls.append(Wall(self.walls[0].p2, self.walls[1].p1))
			else:
				self.walls.append(wall1)
				self.walls.append(wall2)
		self._sort()
		x, y = 0, 0
		for wall in self.walls:
			x = max(x, wall.p1.x)
			y = max(y, wall.p1.y)
		self.bounds = (x, y)

	def _sort(self):
		'''Orders the walls for proper traversal using bubble sort.'''
		for i in range(len(self.walls) - 1):
			next = self.walls[i].p2
			for j in range(len(self.walls) - i - 1):
				if self.walls[j + 1].p1 == next:
					temp = self.walls[i + 1]
					self.walls[i + 1] = self.walls[j + 1]
					self.walls[j + 1] = temp

	def draw(self, canvas, offset, scale):
		for wall in self.walls:
			wall.draw(canvas, offset, scale)

	def contains(self, point, direction, offset = Point(0,0)):
		'''Checks if the room contains the given point using raycasting.'''
		count = 0
		n = 0
		m = 0
		target = -1
		step = -1
		if direction == HORIZONTAL:
			n = point.x - offset.x
			m = point.y - offset.y
			if n > self.bounds[0] / 2:
				target = self.bounds[0] + 1
				step = 1
		else:
			n = point.y - offset.y
			m = point.x - offset.x
			if n > self.bounds[1] / 2:
				target = self.bounds[1] + 1
				step = 1

		while n != target:
			if direction == HORIZONTAL: p = Point(n, m)
			else: p = Point(m, n)
			for wall in self.walls:
				if p.isOnPerpendicular(wall.p1, wall.p2):
					count += 1
			n += step
		return count % 2
