# global imports
from PIL import Image, ImageDraw
from dataclasses import dataclass, field

# local imports
from room import Room
from layout import Layout, TSHAPE

# testing
import os

# ft/in
SCALE = 12

@dataclass(frozen = False, order = False)
class Blueprint:
	_layout: Layout = field()
	_params: str = field(default="params.csv")
	_outline: Room = field(init=False)

	def __post_init__(self):
		self._outline = self._layout.make()
		self._generate()

	def draw(self):
		img = Image.new('RGB', (70 * SCALE, 70 * SCALE), (255, 255, 255))
		canvas = ImageDraw.Draw(img)
		self._outline.draw(canvas, (0,0), SCALE)
		img.show()
		img.save('img.png')
		# TEMP
		#os.system('atom -a img.png')

	def _generate(self):
		for wall in self._outline.walls:
			if len(wall.doors) == 0: continue
			print("door", wall.doors)

b = Blueprint(TSHAPE)
b.draw()
