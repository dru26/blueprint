# global imports
from dataclasses import dataclass, field
import random

# local imports
from .point import Point
from .reader import readCSVtoLst, readCSVtoDict

# builtin room modes
HOUSE = 'House'

# Read global data from provided files
ROOMS = readCSVtoLst('rooms', headers = True) # List of rooms
modes = readCSVtoLst('modes', headers = True) # Temp list of mode data
CONNECT = readCSVtoDict('connections') # Rooms mapped to which rooms they can connect to

# Setup other global data to be filled in later
ROOM_TYPES = dict()
ROOM_SPECS = dict()
MODES = dict()

# Setup global limit on how small a room can be
MIN_LENGTH = 3

@dataclass(frozen = False, order = False)
class Room:
	'''A Room holds multiple rectangular RoomSpaces that occupy floor space.
	   In abstract terms, a Room is just a collection of rectangles that make up
	   its area along with a labeling term.'''
	label: str = field(default_factory = str)
	children: str = field(default_factory = list)

	def addSpace(self, space):
		'''Adds a RoomSpace to the Room. The RoomSpace cannot already be a
		   child of this Room'''
		self.children.append(space)

	def area(self):
		'''Returns the total square footage of the room'''
		area = 0
		for child in self.children: area += child.area()
		return area

	# draws the room onto a canvas at a certain scale
	def draw(self, canvas, scale):
		'''Tells each child space to draw itself on the canvas at a given scale
		   with a radomly chosen color'''
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		for child in self.children:
			child.draw(canvas, scale, color)



@dataclass(frozen = False, order = False, init = False)
class RoomSpace:
	def __init__(self, parent, width, height, offset = Point(0, 0)):
		self.parent = parent
		self.parent.addSpace(self)
		self.width = width
		self.height = height
		self._offset = offset

	def draw(self, canvas, scale, color):
		'''Draws a rectangle representing the space on a canvas at a given scale
		   using a given color.'''
		x, y = self._offset.x * scale, self._offset.y * scale
		w, h = self.width * scale, self.height * scale
		canvas.rectangle((x, y, x + w, y + h), fill = color, outline = (255, 255, 255))

	def area(self):
		'''Returns the total area of the space.'''
		return self.width * self.height

	def flip(self):
		'''Rotates the space 90 degrees, effectively swapping the width and height.'''
		self.width, self.height = self.height, self.width

	def setPos(self, point):
		'''Sets the initial upper-left position of the room in 2D space'''
		self._offset = point

	def getLabel(self):
		'''Returns the label that this space belongs to'''
		return self.parent.label

	def extend(self, direction, distance):
		'''Extends the space in a single direction by a certain distance.'''
		if direction == 'x':
			old_width = self.width
			self.width += distance
			return (self.x() + old_width, self.x() + self.width, self.y(), self.y() + self.height)
		elif direction == 'y':
			old_height = self.height
			self.height += distance
			return (self.x(), self.x() + self.width, self.y() + old_height, self.y() + self.height)

	def x(self):
		'''Returns the x position of the space in 2D space.'''
		return self._offset.x

	def y(self):
		'''Returns the y position of the space in 2D space.'''
		return self._offset.y

	def size(self):
		'''Returns the size of the size of the space as a tuple.'''
		return (int(self.width), int(self.height))

# Construct the ROOM_TYPES and ROOM_SPECS dictionaries from the ROOMS list
for room in ROOMS:
	if ROOM_TYPES.get(room[0]) == None:
		ROOM_TYPES[room[0]] = [room[1]]
	else:
		ROOM_TYPES[room[0]] += [room[1]]
	ROOM_SPECS[room[1]] = room[2:]

# Construct the MODES dictionary from the modes list
for mode in modes:
	MODES[mode[0]] = mode[1:]
del modes

def getRooms(mode):
	'''Returns a list of rooms that have been randomized from the given mode.'''
	global MODES, ROOM_SPECS, ROOM_TYPES, FAILS
	rooms = []
	for room in MODES[mode][0]:
		name = random.choice(ROOM_TYPES[room])
		specs = ROOM_SPECS[name]
		r = Room(name)
		rs = RoomSpace(r, specs[1] + random.randint(-specs[2], specs[2]), specs[3] + random.randint(-specs[4], specs[4]))
		rooms.append(rs)
	random.shuffle(rooms)
	return rooms

def getRandomRoom():
	'''Returns a random room.'''
	global MODES, ROOM_SPECS, ROOM_TYPES
	name = random.choice(list(ROOM_SPECS.keys()))
	specs = ROOM_SPECS[name]
	r = Room(name)
	rs = RoomSpace(r, specs[1] + random.randint(-specs[2], specs[2]), specs[3] + random.randint(-specs[4], specs[4]))
	return rs

def isValid(size):
	'''Checks if the given size tuple is large enough for any room to fit inside.'''
	if size[0] < MIN_LENGTH: return False
	if size[1] < MIN_LENGTH: return False
	return True