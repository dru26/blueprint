# global imports
from dataclasses import dataclass, field
from random import shuffle

# local imports
from wall import Wall
from point import Point
from direction import HORIZONTAL, VERTICAL, EAST, SOUTH, NORTH, WEST

@dataclass(frozen=False, order=False)
class Room:
	'''A list of walls.'''
	walls: list[Wall] = field()
	offset: Point = field(default = Point())
	bounds: tuple = field(init = None)

	def __post_init__(self):
		self._make()

	def _make(self):
		# If only two walls are passed in, assume rectangular room and make
		# the missing walls
		if len(self.walls) == 2:
			wall1 = Wall(self.walls[0].p1, self.walls[1].p1)
			wall2 = Wall(self.walls[0].p2, self.walls[1].p2)
			if Wall.getIntersection(wall1, wall2):
				self.walls.append(Wall(self.walls[0].p1, self.walls[1].p2))
				self.walls.append(Wall(self.walls[0].p2, self.walls[1].p1))
			else:
				self.walls.append(wall1)
				self.walls.append(wall2)
		self._sort()
		xmax, xmin, ymax, ymin = 0, float('inf'), 0, float('inf')
		for wall in self.walls:
			xmax = max(xmax, wall.p1.x, wall.p2.x)
			ymax = max(ymax, wall.p1.y, wall.p2.y)
			xmin = min(xmin, wall.p1.x, wall.p2.x)
			ymin = min(ymin, wall.p1.y, wall.p2.y)
		self.bounds = (xmin, ymin, xmax, ymax)

		self._mark()

	def _mark(self):
		'''Marks the walls in a room to tell which direction is interior.'''
		for wall in self.walls:
			if wall.p1.x == wall.p2.x:
				p = Point(wall.p1.x, (wall.p1.y + wall.p2.y) / 2)
				if (self.contains(p + (1, 0))):
					wall.interior = EAST
				else:
					wall.interior = WEST
			else:
				p = Point((wall.p1.x + wall.p2.x) / 2, wall.p1.y)
				if (self.contains(p + (0, 1))):
					wall.interior = SOUTH
				else:
					wall.interior = NORTH
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

	def contains(self, point):
		'''Checks if the room contains the given point using raycasting.'''
		# Corner case
		for wall in self.walls:
			# Always return true if the point given is on a *corner*
			if point == wall.p1 or point == wall.p2:
				return 1
		west = abs(point.x - self.bounds[0])
		east = abs(point.x - self.bounds[2])
		north = abs(point.y - self.bounds[1])
		south = abs(point.y - self.bounds[3])
		count, n, m, c = 0, 0, 0, 0
		target, step = 0, -1
		direction = VERTICAL
		min_ = min(east, west, north, south)
		if east == min_ or west == min_:
			n = point.x
			m = point.y
			direction = HORIZONTAL
			target = west
			if east == min_:
				step = 1
				target = east + 1
		elif north == min_ or south == min_:
			n = point.y
			m = point.x
			target = north
			if south == min_:
				step = 1
				target = south + 1
		while c <= target:
			if direction == HORIZONTAL: p = Point(n, m)
			else: p = Point(m, n)
			for wall in self.walls:
				if p.isOnPerpendicular(wall.p1, wall.p2, direction):
					count += 1
					break
			n += step
			c += 1
		return count % 2

	def _updateBounds(self, x, y, outline, rooms, bounds, direction):
		point = Point(x, y)
		flag = False
		if not outline.contains(point): flag = True
		for room in rooms:
			if room.contains(point):
				flag = True
				break
		if flag:
			if direction == WEST: bounds[0] = x + 1
			elif direction == NORTH: bounds[1] = y + 1
			elif direction == EAST: bounds[2] = x - 1
			elif direction == SOUTH: bounds[3] = y - 1
			return True
		if direction == WEST and x < bounds[0]: return True
		if direction == NORTH and y < bounds[1]: return True
		if direction == EAST and x > bounds[2]: return True
		if direction == SOUTH and y > bounds[3]: return True
		return False

	def _tree(self, x, y, outline, rooms, bounds, direction):
		#print('tree')
		if self._updateBounds(x, y, outline, rooms, bounds, direction): return
		if direction == NORTH or direction == SOUTH:
			self._branch(x + 1, y, outline, rooms, bounds, EAST)
			self._branch(x - 1, y, outline, rooms, bounds, WEST)
			self._tree(x, y + direction.step(), outline, rooms, bounds, direction)
		else:
			self._branch(x, y + 1, outline, rooms, bounds, SOUTH)
			self._branch(x, y - 1, outline, rooms, bounds, NORTH)
			self._tree(x + direction.step(), y, outline, rooms, bounds, direction)

	def _branch(self, x, y, outline, rooms, bounds, direction):
		#print('branch')
		if self._updateBounds(x, y, outline, rooms, bounds, direction): return
		if direction == NORTH or direction == SOUTH:
			self._branch(x, y + direction.step(), outline, rooms, bounds, direction)
		else:
			self._branch(x + direction.step(), y, outline, rooms, bounds, direction)

	def reduce(self, outline, rooms, direction, point):
		'''Reduces the room around a given point with a certain directional bias.'''
		if len(self.walls) != 4:
			return False
		bounds = list(self.bounds)

		if direction == VERTICAL:
			self._tree(point.x, point.y, outline, rooms, bounds, EAST)
			self._tree(point.x, point.y, outline, rooms, bounds, WEST)
		else:
			self._tree(point.x, point.y, outline, rooms, bounds, NORTH)
			self._tree(point.x, point.y, outline, rooms, bounds, SOUTH)

		self.walls = [Wall(Point(bounds[0], bounds[1]), Point(bounds[0], bounds[3])),
			Wall(Point(bounds[2], bounds[1]), Point(bounds[2], bounds[3]))]

		self._make()
		return True









'''
		x, y = self.bounds[0], self.bounds[1]

		if direction == VERTICAL:
			# Reduce y to make the room fit
			x = self.bounds[0]
			max_ = self.bounds[3]
			while x < self.bounds[2]:
				y = self.bounds[1]
				while y < max_:
					if not room.contains(Point(x, y)):
						max_ = y - 1
					y += 1
				x += 1
		else:
			# Reduce x to make the room fit
			y = self.bounds[1]
			max_ = self.bounds[2]
			while y < self.bounds[3]:
				x = self.bounds[0]
				while x < max_:
					if not room.contains(Point(x, y)):
						max_ = x - 1
					x += 1
				y += 1

		w1 = Wall()
		w2 =


		return True
'''
