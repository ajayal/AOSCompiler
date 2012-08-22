#!/usr/bin/env python

class Tools():

	def processor(self):
		count = 0
		for line in open('/proc/cpuinfo', 'r'):
			if line.startswith('processor'):
				count += 1
		return count
