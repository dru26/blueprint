# global imports
from dataclasses import dataclass, field
import math

# local imports
from point import Point
from door import Door
from direction import push


@dataclass(frozen=True, order=False)
class Wall:
	'''A line drawn between two points with other features like doors and splitting.'''
	p1: Point = field()
	p2: Point = field()
	doors: list[Door] = field(default_factory=list)

	def offset(self, distance, direction = None):
		'''Returns a copy of this Wall offset in a direction and distance without doors.'''
		if direction == None and len(self.doors) != 0:
			direction = self.doors[0].direction
		return Wall(push(self.p1, direction, distance), push(self.p2, direction, distance))

	def draw(self, canvas, offset, scale):
		canvas.line([(self.p1 + offset) * scale, (self.p2 + offset) * scale], fill = "#5BA1B5", width = 2)
		for door in self.doors:
			door.draw(canvas, offset, scale)

	@staticmethod
	def getIntersection(wall1, wall2):
		'''Returns None if there is no intersection between the walls. Otherwise it
			returns the intersection point. If the walls are the same,
			None is also returned.'''
		# Get the slope
		try: m1 = (wall1.p2.y - wall1.p1.y) / (wall1.p2.x - wall1.p1.x)
		except ZeroDivisionError: m1 = float('inf')
		try: m2 = (wall2.p2.y - wall2.p1.y) / (wall2.p2.x - wall2.p1.x)
		except ZeroDivisionError: m2 = float('inf')

		# Special case: walls can never intersect
		if m1 == m2:
			return None
		# General case: lines will intersect but might not in the wall's range
		x = (b2 - b1) / (m1 - m2)
		y = (m1 * x) + b1
		i = Point(x, y)
		if i.inRange(wall1.p1, wall1.p2) and i.inRange(wall2.p1, wall2.p2):
			return i
		return None
