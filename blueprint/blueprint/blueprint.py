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

	def __post_init__(self):
		self._outline = self._layout.make()
		self._generate()

	def _create(self, wall, scale):
		# Create the optimal room
		#room = Room()
		pass

	def _generate(self):
		for wall in self._outline.walls:
			if len(wall.doors) == 0: continue
			# Starting point for recursion
			self._create(Wall(wall.p1, wall.p2, wall.doors), 'ENTRY')

	def isOverlap(self, room):
		pass

	def draw(self):
		img = Image.new('RGB', (70 * SCALE, 70 * SCALE), (255, 255, 255))
		canvas = ImageDraw.Draw(img)
		self._outline.draw(canvas, (0,0), SCALE)
		img.show()
		img.save('img.png')
		# TEMP
		#os.system('atom -a img.png')

b = Blueprint(Layout(TSHAPE, 20), GENERIC)
b.draw()
