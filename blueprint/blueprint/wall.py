# global imports
from dataclasses import dataclass, field
from PIL import ImageDraw
import math

# local imports
from point import Point
from door import Door
from direction import Direction, push, HORIZONTAL, VERTICAL, SOUTH, NORTH, EAST, WEST


@dataclass(frozen=False, order=False)
class Wall:
	'''A horizontal or vertical line drawn between two points with other features
		like doors and splitting.'''
	p1: Point = field()
	p2: Point = field()
	doors: list[Door] = field(default_factory=list)
	interior: Direction = None
	direction: Direction = field(init=False)
	length: float = field(init = False)

	def __post_init__(self):
		if self.p1.x == self.p2.x:
			self.direction = VERTICAL
		if self.p1.y == self.p2.y:
			self.direction = HORIZONTAL
		if self.p1.x != self.p2.x and self.p1.y != self.p2.y:
			raise ValueError("Wall must be horizontal or vertical.")
		self.length = Point.distance(self.p1, self.p2)

	def copy(self):
		return Wall(self.p1, self.p2, self.doors, interior = self.interior)

	def offset(self, distance: float, direction: Direction = None):
		'''Returns a copy of this Wall offset in a direction and distance without doors.'''
		if direction == None:
			direction = self.interior
		return Wall(push(self.p1, direction, distance), push(self.p2, direction, distance))

	def extend(self, bounds, direction, doors = []):
		'''Returns a copy of this Wall offset in a direction as far as possible while
			within the bounds.'''
		if direction == None:
			direction = self.interior
		if direction == SOUTH:
			return Wall(Point(self.p1.x, bounds[3]), Point(self.p2.x, bounds[3]), doors = doors)
		if direction == NORTH:
			return Wall(Point(self.p1.x, bounds[1]), Point(self.p2.x, bounds[1]), doors = doors)
		if direction == EAST:
			return Wall(Point(bounds[2], self.p1.y), Point(bounds[2], self.p2.y), doors = doors)
		if direction == WEST:
			return Wall(Point(bounds[0], self.p1.y), Point(bounds[0], self.p2.y), doors = doors)
		if direction == HORIZONTAL:
			return Wall(Point(bounds[0], self.p1.y), Point(bounds[2], self.p2.y), doors = doors)
		if direction == VERTICAL:
			return Wall(Point(self.p1.x, bounds[1]), Point(self.p2.x, bounds[3]), doors = doors)

	def draw(self, canvas: ImageDraw, offset: float, scale: float):
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
