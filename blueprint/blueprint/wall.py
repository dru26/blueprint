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

	def offset(self, direction, distance):
		'''Returns a copy of this Wall offset in a direction and distance without doors.'''
		return Wall(push(p1, direction, distance), push(p2, direction, distance))

	def draw(self, canvas, offset, scale):
		canvas.line([self.p1 * scale, self.p2 * scale], fill = 128)
		for door in self.doors:
			door.draw(canvas, offset, scale)
