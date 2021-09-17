# global imports
from enum import Enum

class Direction(Enum):
	NORTH = -1
	SOUTH = 1
	EAST = 2
	WEST = -2
	VERTICAL = 3
	HORIZONTAL = -3

	def step(self):
		return 1 if self.value > 0 else -1

	def __neg__(self):
		return Direction(value = -self.value)

NORTH = Direction.NORTH
SOUTH = Direction.SOUTH
EAST = Direction.EAST
WEST = Direction.WEST
VERTICAL = Direction.VERTICAL
HORIZONTAL = Direction.HORIZONTAL
X = HORIZONTAL
Y = VERTICAL

def generalize(direction):
	if direction == NORTH or direction == SOUTH:
		return VERTICAL
	if direction == EAST or direction == WEST:
		return HORIZONTAL

def push(point, direction, distance):
	if direction is SOUTH:
		return (point[0], point[1] + distance)
	if direction is EAST:
		return (point[0] + distance, point[1])
	if direction is NORTH:
		return (point[0], point[1] - distance)
	if direction is WEST:
		return (point[0] - distance, point[1])
	if direction is X:
		return [(point[0] - distance, point[1]), (point[0] + distance, point[1])]
	if direction is Y:
		return [(point[0], point[1] - distance), (point[0], point[1] + distance)]
