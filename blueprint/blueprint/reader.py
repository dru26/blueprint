# global imports
import csv
from pathlib import Path

def readCSVtoLst(filename, headers = False):
	'''Reads a .csv filt to a list.'''
	lst = []
	with open(Path(__file__).with_name(filename + '.csv')) as file:
		reader = csv.reader(file)
		for row in reader:
			if headers:
				headers = False
				continue
			line = []
			for item in row:
				if item.replace('.','').isdigit(): line.append(float(item))
				else:
					if ';' in item:
						subline = []
						for subitem in item.split(';'):
							if subitem != '':
								if subitem.replace('.','').isdigit(): subline.append(float(subitem))
								else: subline.append(subitem)
						line.append(subline)
					else: line.append(item)
			lst.append(line)
	return lst

def readCSVtoDict(filename):
	'''Reads a .csv filt to a dictionary.'''
	lst = []
	dct = dict()
	# Store indoor connections to a dictionary
	with open(Path(__file__).with_name(filename + '.csv')) as file:
		first = True
		reader = csv.reader(file)
		i = -2
		for row in reader:
			i += 1
			if first:
				lst = row[1:].copy()
				first = False
				continue
			dct[row[0]] = dict()
			for j in range(1, len(row) - 1):
				if row[j] != '':
					if row[j].replace('.','').isdigit():
						dct[row[0]][lst[j]] = float(row[j])
					else:
						dct[row[0]][lst[j]] = row[j]
	return dct