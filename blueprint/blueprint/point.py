# global imports
from dataclasses import dataclass, field
import math

@dataclass(frozen = True, order = False)
class Point(tuple):
	'''A special tuple with only two values: x and y.'''
	x: float = field(default = 0)
	y: float = field(default = 0)

	def __new__(self, x = 0, y = 0):
		return tuple.__new__(Point, (x, y))

	def __add__(self, obj):
		'''Adds any tuple with a length of 2 to a Point and returns a new
		   Point.'''
		if not isinstance(obj, tuple): return None
		if len(obj) != 2: return None
		return Point(self.x + float(obj[0]), self.y + float(obj[1]))

	def __sub__(self, obj):
		'''Subtracts any tuple with a length of 2 from a Point and returns a new
		   Point.'''
		if not isinstance(obj, tuple): return None
		if len(obj) != 2: return None
		return Point(self.x - float(obj[0]), self.y - float(obj[1]))

	def __mul__(self, num):
		'''Subtracts any tuple with a length of 2 from a Point and returns a new
		   Point.'''
		if (isinstance(num, int) or isinstance(num, float) or isinstance(num, double)):
			return Point(self.x * num, self.y * num)
		return None

	@staticmethod
	def distance(p1, p2):
		'''Returns the Eucladian distance between two points'''
		return math.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))

	def rng(self, p1, p2):
		'''Checks if the point is in the range bounded by two unordered points'''
		x, y = False, False
		if p1.x <= self.x <= p2.x: x = True
		if p2.x <= self.x <= p1.x: x = True
		if p1.y <= self.y <= p2.y: y = True
		if p2.y <= self.y <= p1.y: y = True
		return x and y

	def on(self, p1, p2):
		'''Checks if the point is on a line bounded by two unordered points'''
		v, h = False, False
		if p1.x == self.x == p2.x: h = True
		if h and p1.y <= self.y <= p2.y: v = True
		if p1.y == self.y == p2.y: v = True
		if v and p1.x <= self.x <= p2.x: h = True
		return h and v
