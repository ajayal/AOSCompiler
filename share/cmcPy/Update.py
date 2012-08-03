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

import gtk
from Globals import Globals
from Parser import Parser
import urllib

class Update():
	def GET_COLOR(self):
		myColor = None
		colord = gtk.ColorSelectionDialog("Choose color")
		selector = colord.get_color_selection()
		response = colord.run()
		if response == gtk.RESPONSE_OK:
			myColor = str(selector.get_current_color())
		colord.destroy()
		return myColor

	def BACKGROUND_COLOR(self):
		d = Update().GET_COLOR()

		if d is not None:
			Parser().write("background_color", d)
			color = gtk.gdk.color_parse(d)
			Globals.MAIN_WIN.modify_bg(gtk.STATE_NORMAL, color)

	def TEXT_COLOR(self):
		myColor = Parser().read("text_color")
		b = Parser().read("branch")
		d = Parser().read("device")
		r = Parser().read("repo_path")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		Globals.branchLab.set_markup("<span color=\"%s\">Branch</span>" % myColor)
		Globals.deviceLab.set_markup("<span color=\"%s\">Device</span>" % myColor)
		Globals.syncjobsLab.set_markup("<span color=\"%s\">Sync jobs</span>" % myColor)
		Globals.makeLab.set_markup("<span color=\"%s\">Make jobs</span>" % myColor)
		Globals.compileLab.set_markup("<span color=\"%s\">Compile</span>" % myColor)
		Globals.syncLab.set_markup("<span color=\"%s\">Sync</span>" % myColor)
		Globals.toolsLab.set_markup("<span color=\"%s\">Tools</span>" % myColor)
		Globals.build_appLab.set_markup("<span color=\"%s\"><small>Build specific <b>app/binary</b> here.</small></span>" % myColor)
		Globals.KEY_BIND_INFO.set_markup("<small><small><span color=\"%s\">[CTL-L + (<b>v</b> = View config, <b>a</b> = Start adb, <b>m</b> = Main start/stop, <b>s</b> = Sync, <b>b</b> = build/compile, <b>r</b> = Repo path) <b>esc</b> = Quit]</span></small></small>" % myColor)
		Globals.MAIN_INFO.set_markup("<span color=\"%s\"><small>Device: <b>%s</b> <big>|</big> Branch: <b>%s</b> <big>|</big> Repo path: <b>%s</b></small></span>" % (myColor, d,b,r))

	def TEXT_COLOR_DIALOG(self):
		d = Update().GET_COLOR()
		if d is not None:
			Parser().write("text_color", d)
			Update().TEXT_COLOR()

	def DEVICES(self):
		LIST = []
		Globals.DEV_COMBO.get_model().clear()
		try:
			del LIST[:]
		except:
			print "Meh"

		b = Parser().read("branch")
		if "Default" in b:
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

			try:
				filehandle = urllib.urlopen(useBranch)
			except IOError:
				print "fuck you"

			for lines in filehandle.readlines():

				if "combo" in lines and not "#" in lines:
					x = lines.split(" ")
					x = x[1]
					x = x.split("_")
					x = x[1]
					x = x.split("-")
					x = x[0]
				
					LIST.extend([x])

			filehandle.close()
			for i in LIST:
				Globals.DEV_COMBO.append_text("%s" % i)

