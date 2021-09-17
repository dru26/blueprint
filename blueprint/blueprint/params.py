# global imports
from dataclasses import dataclass, field
import numpy as np
from enum import Enum, auto
from copy import deepcopy

class RoomType(Enum):
	ANY = auto()
	SOCIAL = auto()
	PRIVATE = auto()
	ENTRY = auto()
	LIMITED = auto()

class Policy(Enum):
	ALLOW_DUPS = auto()
	LIMIT_DUPS = auto()

SOCIAL = RoomType.SOCIAL
PRIVATE = RoomType.PRIVATE
ENTRY = RoomType.ENTRY

@dataclass(frozen = False, order = False)
class RoomParams:
	weight: int = field(default = 1)
	label: str = field(default = None)
	type: RoomType = field(default = RoomType.ANY)
	scale: tuple = field(default = None)
	scaleable: tuple = field(default = None)
	max: tuple = field(default = None)
	min: tuple = field(default = None)
	discard: bool = field(default = False)
	policy: Policy = field(default = Policy.ALLOW_DUPS)

	def __post_init__(self):
		if self.scale == None:
			self.scale = (1, 1)
		if self.scaleable == None:
			self.scaleable = (True, True)
		if len(self.scale) != 2 or len(self.scaleable) != 2:
			raise ValueError("Arguments scale and scaleable must have a length of 2")
		if (not isinstance(self.scale[0], (int, float))) or (not isinstance(self.scale[1], (int, float))):
				raise ValueError("scale must be a tuple of floats")
		if (not isinstance(self.scaleable[0], (bool))) or (not isinstance(self.scaleable[1], (bool))):
				raise ValueError("scaleable must be a tuple of bools")
		if self.min != None:
			if len(self.min) != 2 or len(self.min) != 2:
				raise ValueError("Argument min must have a length of 2")
			if (not isinstance(self.min[0], (int, float))) or (not isinstance(self.min[1], (int, float))):
					raise ValueError("min must be a tuple of floats")
		if self.max != None:
			if len(self.max) != 2 or len(self.max) != 2:
				raise ValueError("Argument max must have a length of 2")
			if (not isinstance(self.max[0], (int, float))) or (not isinstance(self.max[1], (int, float))):
					raise ValueError("max must be a tuple of floats")

@dataclass(frozen = False, order = False)
class Params:
	rooms: list[RoomParams] = field(default = None)
	private: float = field(default = 0.5)
	social: float = field(default = 0.4)
	other: float = field(default = 0.1)
	force_private: bool = field(default = True)
	door_size: float = field(default = 3)
	min_gap: float = field(default = 3)
	_social_rooms: list[RoomParams] = field(init = False, default_factory = list)
	_private_rooms: list[RoomParams] = field(init = False, default_factory = list)
	_entry_rooms: list[RoomParams] = field(init = False, default_factory = list)
	_social_p_lst: list[float] = field(init = False, default_factory = list)
	_private_p_lst: list[float] = field(init = False, default_factory = list)
	_entry_p_lst: list[float] = field(init = False, default_factory = list)

	def __post_init__(self):
		# Make the room param lists
		for param in self.rooms:
			if param.type == RoomType.ANY:
				self._private_rooms.append(param)
				self._entry_rooms.append(param)
				self._social_rooms.append(param)
			elif param.type == RoomType.LIMITED:
				self._private_rooms.append(param)
				self._social_rooms.append(param)
			elif param.type == RoomType.SOCIAL:
				self._social_rooms.append(param)
			elif param.type == RoomType.PRIVATE:
				self._private_rooms.append(param)
			elif param.type == RoomType.ENTRY:
				self._entry_rooms.append(param)
		# Make the probability lists
		sum = 0
		for param in self._social_rooms:
			self._social_p_lst.append(float(param.weight))
			sum += float(param.weight)
		for i in range(len(self._social_p_lst)):
			self._social_p_lst[i] /= sum
		sum = 0
		for param in self._private_rooms:
			self._private_p_lst.append(float(param.weight))
			sum += float(param.weight)
		for i in range(len(self._private_p_lst)):
			self._private_p_lst[i] /= sum
		sum = 0
		for param in self._entry_rooms:
			self._entry_p_lst.append(float(param.weight))
			sum += float(param.weight)
		for i in range(len(self._entry_p_lst)):
			self._entry_p_lst[i] /= sum

	def next(self, lst: list[RoomParams]):
		'''Returns the next item in the list and reorders the list based on this
			parameter policy.'''
		param = lst.pop(0)
		if param.discard:
			return param
		lst.append(param)
		if param.policy == Policy.LIMIT_DUPS:
			return param
		p_lst = []
		sum = 0
		for p in lst:
			p_lst.append(float(p.weight))
			sum += float(p.weight)
		lst = np.random.choice(lst, size = len(lst), replace = False, p = p_lst)
		return param

	def get(self, type):
		if type == RoomType.SOCIAL:
			return np.random.choice(self._social_rooms, size = len(self._social_rooms), replace = False, p = self._social_p_lst).tolist()
		if type == RoomType.ENTRY:
			return np.random.choice(self._entry_rooms, size = len(self._entry_rooms), replace = False, p = self._entry_p_lst).tolist()
		if type == RoomType.PRIVATE:
			return np.random.choice(self._private_rooms, size = len(self._private_rooms), replace = False, p = self._private_p_lst).tolist()

GENERIC = Params(rooms = [RoomParams(label = 'generic')])
