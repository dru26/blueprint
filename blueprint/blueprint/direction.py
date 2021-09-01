# global imports
from enum import Enum

# local imports
from point import Point

NORTH = 1
SOUTH = -1
EAST = 2
WEST = -2
VERTICAL = 3
HORIZONTAL = -3
X = HORIZONTAL
Y = VERTICAL


def push(point, direction, distance):
	if direction is SOUTH:
		return Point(point.x, point.y + distance)
	if direction is EAST:
		return Point(point.x + distance, point.y)
	if direction is NORTH:
		return Point(point.x, point.y - distance)
	if direction is WEST:
		return Point(point.x - distance, point.y)
	if direction is X:
		return [Point(point.x - distance, point.y), Point(point.x + distance, point.y)]
	if direction is Y:
		return [Point(point.x, point.y - distance), Point(point.x, point.y + distance)]
