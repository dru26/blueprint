# global imports
from dataclasses import dataclass, field
from random import shuffle

# local imports
from wall import Wall
from point import Point

@dataclass(frozen=False, order=False)
class Room:
	'''A list of walls.'''
	walls: list[Wall] = field()
	offset: Point = field(default=Point())

	def __post_init__(self):
		self._sort()

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
