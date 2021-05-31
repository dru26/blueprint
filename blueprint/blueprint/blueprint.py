# global imports
from PIL import Image, ImageDraw
from dataclasses import dataclass

# local imports
from .point import Point
from .plotter import Plotter, FAST



@dataclass(frozen = False, order = False, init = False)
class Blueprint:
	'''TODO: Class docstr'''

	def __init__(self, width, height, name = 'Blueprint'):
		self.name = name
		self._width, self._height = width, height
		self._pen = Plotter(width, height)
		self.clear()

	def inspect(self, x, y, floor = 1):
		'''Returns None if the location does not exist, "Blank" if there is no room
		   at that location, or the room's label as a string if a room exists'''
		if not self._inBounds(Point(x, y)): return None
		if floor >= self._floor_count[0] or floor < self._floor_count[1]: return None
		print(x, y, self._floor_count, floor)
		return self._floors[floor].get(x, y)

	def clear(self):
		'''Removes all annotations from the blueprint.'''
		self._floors = []
		self._floor_count = [0, 0]

	def print(self):
		'''Prints the blueprint to the console along with a dictionary of rooms'''
		print(self.name + ':')
		for f in range(len(self._floors)):
			print('\tFloor', f)
			self._floors[f].print(prefix = '\t')

	def show(self, scale = 100):
		self._image(scale).show()

	def save(self, filename, scale = 100):
		self._image(scale).save(filename + '.jpeg')

	def plot(self, mode):
		self._floor_count = self._pen.makePlan(mode, self._floors)

	def _wireframe(self):
		# TODO: impliment the Line class and use it to make a wireframe model
		# the blueprint so that walls can be generated
		pass

	def _enableOptimizations(self):
		'''Enables certain optimizations for the blueprint. If enabled, inspect
		   may not function properly, but might run faster for larger blueprints.'''
		self._pen._optimize = FAST

	def _image(self, scale):
		img = Image.new('RGB', (scale * self._width, scale * self._height), (255, 255, 255))
		canvas = ImageDraw.Draw(img)
		for floor in self._floors: floor.draw(canvas, scale)
		return img

	def _inBounds(self, point):
		return 0 <= point.x < self._width and 0 <= point.y < self._height