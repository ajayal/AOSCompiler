#!/usr/bin/env python

import gtk
import pygtk
import os

from Globals import Globals
from Parser import Parser
from Utils import Utils

class Compile():
	def run(self):
		r = Parser().read("rom_abrv")
		C = Compile()
		if r == "CM":
			C.CM()
		elif r == "GR":
			from projects.GeekRom import GeekRom as G
			G.Compile()
		else:
			n = Parser().read("rom_dist")
			Utils().CDial(gtk.MESSAGE_INFO, "Rom %s not supported" % n, "Sorry but at this time,\n\n%s\n\nis not supported, please contact us for more info" % n)
