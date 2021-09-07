# global imports
from dataclasses import dataclass, field
import math

# local imports
from point import Point
from direction import push, HORIZONTAL, VERTICAL, NORTH, SOUTH, EAST, WEST

DWIDTH = 3

@dataclass(frozen=True, order=False)
class Door:
	'''A passage through a wall.'''
	center: Point = field()
	direction: int = field()
	width: int = field(default=DWIDTH)

	def draw(self, canvas, offset, scale):
		if self.direction == NORTH or self.direction == SOUTH:
			dir = VERTICAL
		if self.direction == EAST or self.direction == WEST:
			dir = HORIZONTAL
		pts = push((self.center + offset) * scale, -dir, self.width * scale / 2)
		canvas.line(pts, fill = "#282C34", width = 3)
		canvas.line(pts, fill = "#3B4048", width = 0)
		canvas.line(push(pts[0], dir, scale / 2), fill = "#5BA1B5", width = 4)
		canvas.line(push(pts[1], dir, scale / 2), fill = "#5BA1B5", width = 4)
		canvas.line((pts[0], push(pts[1], self.direction, self.width * scale * 0.5)), fill = "#5BA1B5", width = 3)
