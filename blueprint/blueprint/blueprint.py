# global imports
from PIL import Image, ImageDraw
from dataclasses import dataclass, field

# local imports
from room import Room
from wall import Wall
from layout import Layout, TSHAPE, SQUARE, RECT
from params import Params, GENERIC
# testing
import os

# ft/in
SCALE = 12

@dataclass(frozen = False, order = False)
class Blueprint:
	_layout: Layout = field()
	_params: Params = field()
	_outline: Room = field(init = False)
	_subrooms: list[Room] = field(init = False)
	_size: tuple = field(init = False)

	def __post_init__(self):
		self._outline = self._layout.make()
		self._size = self._outline.bounds
		self._subrooms = []
		self._generate()

	def _create(self, wall, scale):
		# Create the optimal room
		self._subrooms.append(Room([wall, wall.offset(10)]))

	def _generate(self):
		for wall in self._outline.walls:
			if len(wall.doors) == 0: continue
			# Starting point for recursion
			self._create(Wall(wall.p1, wall.p2, wall.doors), 'ENTRY')

	def isOverlap(self, room):
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
			print(room)
		self._outline.draw(canvas, (1,1), SCALE)
		img.show()
		img.save('img.png')
		# TEMP
		#os.system('atom -a img.png')

b = Blueprint(Layout(TSHAPE, 20), GENERIC)
b.draw()
