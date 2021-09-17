# global imports
from PIL import Image, ImageDraw
from dataclasses import dataclass, field
from random import randint

# local imports
from room import Room
from wall import Wall
from point import Point
from layout import Layout, TSHAPE, SQUARE, RECT
from params import Params, GENERIC, RoomType, RoomParams, SOCIAL, PRIVATE, ENTRY
from direction import NORTH, SOUTH, EAST, WEST, HORIZONTAL, VERTICAL, generalize
# testing
import os

# ft/in
SCALE = 12

@dataclass(frozen = False, order = False)
class Blueprint:
	_layout: Layout = field()
	_params: Params = field(default = GENERIC)
	_outline: Room = field(init = False)
	_subrooms: list[Room] = field(init = False)
	_size: tuple = field(init = False)
	_social: list[RoomParams] = field(init = False)
	_entry: list[RoomParams] = field(init = False)
	_private: list[RoomParams] = field(init = False)

	def __post_init__(self):
		self._outline = self._layout.make(self._params)
		self._size = (self._outline.bounds[2], self._outline.bounds[3])
		self._subrooms = []
		self._social = self._params.get(SOCIAL)
		self._entry = self._params.get(ENTRY)
		self._private = self._params.get(PRIVATE)

		self._generate()

	def _next(self, type):
		if type == SOCIAL:
			return self._params.next(self._social)
		if type == PRIVATE:
			return self._params.next(self._private)
		if type == ENTRY:
			return self._params.next(self._entry)

	def _create(self, start: Wall, type: RoomType):
		# Create the largest possible room given door location and blueprint size
		bounds = [0, 0, self._size[0], self._size[1]]
		direction = start.interior
		center = start.doors[-1].center
		if start.interior == NORTH:
			bounds[3] = start.p1.y
			start = start.extend(bounds, HORIZONTAL)
		elif start.interior == SOUTH:
			bounds[1] = start.p1.y
			start = start.extend(bounds, HORIZONTAL)
		elif start.interior == EAST:
			bounds[0] = start.p1.x
			start = start.extend(bounds, VERTICAL)
		elif start.interior == WEST:
			bounds[2] = start.p1.x
			start = start.extend(bounds, VERTICAL)
		room = Room([start.copy(), start.extend(bounds, direction = direction)])
		params = self._next(type)
		# Reduce
		direction = generalize(direction)
		# TODO: Add a limit to how small a room can get with reduce
		# 	Use parameter to figure this out. NO matter what, it must be
		# 	at least the width of the door.
		if params.scale[0] > params.scale[1]:
			room.reduce(self._outline, self._subrooms, -direction, center)
		else:
			room.reduce(self._outline, self._subrooms, direction, center)
		# TODO: Add the door back into the room

		# TODO: Shrink the room down to its ideal size

		# TODO: Expand room to close up small gaps between walls after shrinkage

		# Room is finished
		self._subrooms.append(room)
		# Continue recursion
		for wall in room.walls:
			continue
			self._create(wall, None)

	def _generate(self):
		for wall in self._outline.walls:
			if len(wall.doors) == 0: continue
			# Starting point for recursion
			self._create(wall, ENTRY)

	def isOverlap(self, room1, room2):
		pass

	def draw(self):
		size = self._size
		size = (size[0] + 2, size[1] + 2)
		img = Image.new('RGB', (size[0] * SCALE, size[1] * SCALE), (40, 44, 52)) # GOLD (226, 192, 141) [E2C08D], BLUE (91, 161, 219) [5BA1B5], GREY (156, 165, 181) (9CA5B5)
		canvas = ImageDraw.Draw(img)
		for i in range(size[0] - 1):
			canvas.line(((i + 1) * SCALE, 0, (i + 1) * SCALE, size[1] * SCALE), fill = "#3B4048", width = 0)
		for i in range(size[1] - 1):
			canvas.line((0, (i + 1) * SCALE, size[0] * SCALE, (i + 1) * SCALE), fill = "#3B4048", width = 1)
		for room in self._subrooms:
			room.draw(canvas, (1,1), SCALE)
		self._outline.draw(canvas, (1,1), SCALE)

		for i in range(size[0] - 1):
			for j in range(size[1] - 1):
				#x = (randint(0, size[0] - 2) + 1) * SCALE
				x = (i + 1) * SCALE
				#y = (randint(0, size[1] - 2) + 1) * SCALE
				y = (j + 1) * SCALE
				if self._outline.contains(Point((x / SCALE) - 1, (y / SCALE) - 1)):
					canvas.ellipse((x-1,y-1,x+1,y+1), fill='green')
				else:
					canvas.ellipse((x-1,y-1,x+1,y+1), fill='red')

		img.show()
		img.save('img.png')
		# TEMP
		#os.system('atom -a img.png')

b = Blueprint(Layout(TSHAPE, 20))
b.draw()
