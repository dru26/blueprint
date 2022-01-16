# global imports
from dataclasses import dataclass, field
import math

NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4

@dataclass(frozen = True, order = False)
class Point(tuple):
	'''A special tuple with only two values: x and y.'''
	x: int = field(default = 0)
	y: int = field(default = 0)

	def __new__(self, x = 0, y = 0):
		return tuple.__new__(Point, (x, y))

	def __add__(self, obj):
		'''Adds any tuple with a length of 2 to a Point and returns a new
		   Point.'''
		if not isinstance(obj, tuple): return None
		if len(obj) != 2: return None
		return Point(self.x + int(obj[0]), self.y + int(obj[1]))

	def __sub__(self, obj):
		'''Subtracts any tuple with a length of 2 from a Point and returns a new
		   Point.'''
		if not isinstance(obj, tuple): return None
		if len(obj) != 2: return None
		return Point(self.x - int(obj[0]), self.y - int(obj[1]))

	def inRange(self, p1, p2):
		'''Checks if the point is in the range bounded by two other unordered
		   points'''
		x, y = False, False
		if p1.x < self.x < p2.x: x = True
		if p2.x < self.x < p1.x: x = True
		if p1.y < self.y < p2.y: y = True
		if p2.y < self.y < p1.y: y = True
		return x and y

	@staticmethod
	def distance(p1, p2):
		'''Returns the Eucladian distance between two points'''
		return math.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))
