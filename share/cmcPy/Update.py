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

from cmcPy.Globals import Globals
from cmcPy.Parser import Parser
import urllib

class Update():

	def MAIN_INFO(self):
		b = Parser().read("branch")
		d = Parser().read("device")
		r = Parser().read("repo_path")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		info = "<span color=\"%s\"><small>Device: <b>%s</b> <big>|</big> Branch: <b>%s</b> <big>|</big> Repo path: <b>%s</b></small></span>" % (Globals.myColor, d,b,r)
		Globals.MAIN_INFO.set_markup(info)

	def DEVICES(self):
		LIST = []
		Globals.DEV_COMBO.get_model().clear()
		try:
			del LIST[:]
		except:
			print "Meh"

		b = Parser().read("branch")
		if "Default" in b:
			print "Meh you too"
			chk_config = 0
		elif "gingerbread" in b:
			useBranch = Globals.myCM_GB_URL
			chk_config = 1
		elif "ics" in b:
			useBranch = Globals.myCM_ICS_URL
			chk_config = 1
		elif "jellybean" in b:
			useBranch = Globals.myCM_JB_URL
			chk_config = 1
		else:
			useBranch = "null"
			chk_config = 0

		if chk_config == 1:

			print useBranch
			try:
				filehandle = urllib.urlopen(useBranch)
			except IOError:
				print "fuck you"

			for lines in filehandle.readlines():

				if "combo" in lines and not "#" in lines:

					print lines

					x = lines.split(" ")
					x = x[1]
					x = x.split("_")
					x = x[1]
					x = x.split("-")
					x = x[0]
				
					LIST.extend([x])

			filehandle.close()
			print "Here"
			for i in LIST:
				Globals.DEV_COMBO.append_text("%s" % i)

