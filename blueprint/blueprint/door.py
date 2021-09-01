# global imports
from dataclasses import dataclass, field
import math

# local imports
from point import Point
from direction import push

DWIDTH = 3

@dataclass(frozen=True, order=False)
class Door:
	'''A passage through a wall.'''
	center: Point = field()
	direction: int = field()
	width: int = field(default=DWIDTH)

	def draw(self, canvas, offset, scale):
		pts = push(self.center * scale, self.direction, self.width * scale / 2)
		canvas.line(push(pts[0], -self.direction, scale), fill = 50, width = math.ceil(scale / 2))
		canvas.line(push(pts[1], -self.direction, scale), fill = 50, width = math.ceil(scale / 2))
		canvas.line(pts, fill = 50, width = math.ceil(scale / 2))
