#!/usr/bin/env python

######################################################################
#
#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.
#
######################################################################

import os
from glob import glob

from Globals import Globals
from Parser import Parser

class Utils():
	def Compile(self):
		RUN = None
		p = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		if p == "Default":
			p = Globals.myDEF_REPO_PATH
		os.chdir(p)
		m = Utils().getManu(d, b)
		if m == None:
			print "Here"
			os.chdir(p)
			PID = Globals.TERM.fork_command('bash')
			Globals.TERM.feed_child('clear\n')
			Globals.TERM.feed_child('python build/tools/roomservice.py cm_%s\n' % d)
			RUN = "ROOM"
		else:
			Parser().write("manuf", m)
			PID = Globals.TERM.fork_command(Globals.myCOMPILE_SCRIPT)
			RUN = "COMP"
			
		return "%s-%s" % (RUN, PID)
		
	def getManu(self, arg, br):
		s = None
		if br == "gb":
			paths = glob("device/*/*/device.mk")
		elif br == "ics" or br == "jellybean":
			paths = glob("device/*/*/cm.mk")
		else:
			paths = None

		if paths is not None:
			for x in paths:
				if arg in x:
					s = x.split("/")
					s = s[1]
		if s:
			return s
		else:
			return None
