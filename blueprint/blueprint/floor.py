# global imports
from dataclasses import dataclass

# local imports
from .point import Point
from .rooms import isValid
from .plotter import NORMAL, FAST

@dataclass(frozen = False, order = False)
class Floor:
	def __init__(self, width, height, level = 0, mode = NORMAL):
		self.rooms = [] # List of rooms added. Sorted by insertion time
		self._grid = [[0 for i in range(width)] for j in range(height)]
		self._spaces = dict() # dictionary mapping space ids to their matching rooms
		# TODO: impliment _doors
		self._doors = dict() # adjacency matrix showing connections
		self._count = 0
		self._level = level
		self._mode = mode

	def insert(self, point, room_space):
		'''Attempts to insert a new room's space into the floor at the given point.
		   The parent Room must contain only one room space and cannot already be
		   a part of the floor. Returns True if the room was inserted and False
		   if insertion failed.'''
		# Remove insertion if there is no room to add (attempting to
		# insert at wall)
		space = self.getSpaceAt(point)
		if space == None: return False

		# If the self is too small to insert a room, extend and existing room
		# and remove the insertion
		if not isValid(space):
			if space[0] > space[1]: self.extend(point - Point(0, 1), 'y', space[1])
			else: self.extend(point - Point(1, 0), 'x', space[0])
			return False

		# This space can theoretically fit some valid room
		# Check to see if the room fits
		fit = self.fits(point, room_space.size())
		if fit != 0:
			# Flip the room if needed to fit
			if fit == -1: room_space.flip()
			# Update variables
			room_space.setPos(point)
			self.rooms.append(room_space.parent)
			self._count += 1
			self._spaces[self._count] = room_space
			# Fill the space
			self.fill(point, room_space.size(), self._count)
			return True

		# Room was not able to be inserted
		# TODO: Trim the room down and allow it to be inserted at a smaller scale
		#       The room should have a max ratio, which, if exceeded, creates multiple
		#       rooms instead as close to ideal ratio. Have option to disable this
		#       behavior and allow floors to be non-rectangular
		return False

	def draw(self, canvas, scale):
		'''Tells each child room to draw itself on the canvas at a given scale'''
		for room in self.rooms:
			room.draw(canvas, scale)

	def assign(self, x, y, value):
		'''Sets a certain postion on the floor to the given value. All varibales
			must be ints or floats. This function is not safe, so all coordinates must
			first be manually checked with self.inBounds()'''
		self._grid[int(y)][int(x)] = value

	def get(self, point):
		'''Gets a certain postion on the floor. This function is not safe,
			so all coordinates must first be manually checked with self.inBounds()'''
		return self._grid[int(point.y)][int(point.x)]

	def fill(self, point, size, room_id):
		'''Fills an area at a point given its size and a label. This function is
			not safe, and bounds must be checked with self.inBounds()'''
		# Add horizontal top and bottom lines
		for x in range(size[0]):
			# Attempt to erase if a room is being extended and FAST is enabled
			if self.get(Point(point.x + x, point.y - 1)) != room_id:
				self.assign(point.x + x, point.y, room_id)
			elif self._mode == FAST and x != 0 and x != size[0] - 1:
				self.assign(point.x + x, point.y - 1, 0)
			# Add bottom line no matter what
			self.assign(point.x + x, point.y + size[1] - 1, room_id)
			# Add to adjacency matrix
			# TODO: Impliment adjacency matrix (doors)

		# Add vertical left and right lines
		for y in range(size[1]):
			# Attempt to erase if a room is being extended and FAST is enabled
			if self.get(Point(point.x - 1, point.y + y)) != room_id:
				self.assign(point.x, point.y + y, room_id)
			elif self._mode == FAST and y != 0 and y != size[1] - 1:
				self.assign(point.x - 1, point.y + y, 0)
			# Add right line no matter what
			self.assign(point.x + size[0] - 1, point.y + y, room_id)
			# Add to adjacency matrix
			# TODO: Impliment adjacency matrix (doors)

		# Fill in the entire block if NORMAL is enabled
		if self._mode == NORMAL:
			for x in range(int(point.x), int(point.x + size[0])):
				for y in range(int(point.y), int(point.y + size[1])):
					self.assign(x, y, room_id)

	def extend(self, point, direction, distance):
		'''Finds the space at a given point and extends it in the given direction.
			Also updates the floor's visuals'''
		# Extend the room's space
		char = self.get(point)
		space = self._spaces[char]
		# Update visuals
		x1, x2, y1, y2  = space.extend(direction, distance)
		self.fill(Point(x1, y1), (int(x2 - x1), int(y2 - y1)), char)

	def getSpaceAt(self, point):
		'''Returns a point relative to the given point of the theoretical maximum size
			a room could be if inserted at this point, only considering'''
		if not self.inBounds(point): return None
		endx, endy = 0, 0
		while endx + point.x < self.width() and self.get(point + (endx, 0)) == 0:
			endx += 1
		while endy + point.y < self.height() and self.get(point + (0, endy)) == 0:
			endy += 1
		if endx == 0 or endy == 0: return None
		return (endx, endy)

	def fits(self, point, size, checkFlip = True):
		'''Returns 1 if the given space fits at the point, -1 if it fits when
			rotated, or 0 if it does not fit.'''
		if not self.inBounds(point + Point(size[0] - 1, size[1] - 1)): return 0
		for x in range(size[0]):
			if self.get(Point(point.x + x, point.y)) != 0:
				if checkFlip: return self.fits(point, (size[1], size[0]), False)
				return False
		for y in range(size[1]):
			if self.get(Point(point.x, point.y + y)) != 0:
				if checkFlip: return self.fits(point, (size[1], size[0]), False)
				return False
		return 1 if checkFlip else -1

	def width(self):
		'''Returns the width of the floor.'''
		return len(self._grid)

	def height(self):
		'''Returns the height of the floor.'''
		return len(self._grid[0])

	def inBounds(self, point):
		'''Checks if a point is within the boundaries of the 2D floor space.'''
		return 0 <= point[0] < self.width() and 0 <= point[1] < self.height()

	def print(self, prefix = ''):
		spacing = len(str(self._count)) + len(str(self._level).lstrip('0')) + 1
		border = prefix + ('#' * len(self._grid) * spacing) + '###'
		print(border)
		for row in self._grid:
			line = prefix + '#'
			for item in row:
				item = str(self._level) + str(item)
				line += ('{0:>' + str(spacing) + 's}').format(item.lstrip('0'))
			line += ' #'
			print(line)
		print(border)