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
import os

from Globals import Globals
from Parser import Parser
from Utils import Utils
#from Update import Update

class Compile():
	def run(self):
		r = Parser().read("rom_abrv")
		C = Compile()
		if r == "CM":
			C.CM()
		elif r == "GR":
			C.GR()
		else:
			n = Parser().read("rom_dist")
			Utils().CDial(gtk.MESSAGE_INFO, "Rom %s not supported" % n, "Sorry but at this time,\n\n%s\n\nis not supported, please contact us for more info" % n)

	def CM(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		os.chdir(r)
		m = Utils().getManu(d)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')
		if m == None:
			os.chdir(p)
			Globals.TERM.feed_child('clear\n')
			Globals.TERM.feed_child('python build/tools/roomservice.py cm_%s\n' % d)
			Utils().CDial(gtk.MESSAGE_INFO, "<small>Running roomservice", "Roomservice is running right now, you will have to run, \"<b>Compile</b>\" again after this is done downloading your kernel and device dependancies.</small>")
		else:
			Parser().write("manuf", m)
			Globals.TERM.feed_child('clear\n')
			if not os.path.exists("%s/vendor/%s" % (r, m)) and b is not "jellybean":
				if Utils().is_adb_running() == True:
					os.chdir("%s/device/%s/%s/" % (r, m, d))
					Globals.TERM.feed_child('clear\n')
					Globals.TERM.feed_child('./extract-files.sh\n')
				else:
					Globals().CDial(gtk.MESSAGE_ERROR, "Adb isn't running", "Need adb to setup vendor files.\n\nIs this something you are going to do yourself?\n\nPlease try again.")
					Globals.TERM.set_background_saturation(1.0)
					Globals.TERM.feed_child('clear\n')

			if not os.path.exists("%s/cacheran" % Globals.myCONF_DIR) and b is not "gingerbread":
				os.chdir(r)
				file("%s/cacheran" % myCONF_DIR, 'w').close()
				Globals.TERM.feed_child('bash prebuilt/linux-x86/ccache/ccache -M 50G\n')

			if b is not "gingerbread":
				Globals.TERM.feed_child('bash vendor/cm/get-prebuilts\n')
			else:
				Globals.TERM.feed_child('bash vendor/cyanogen/get-rommanager\n')

			Globals.TERM.feed_child('source build/envsetup.sh\n')
			Globals.TERM.feed_child("brunch %s\n" % d)

	def GR(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		os.chdir(r)
		m = Utils().getManu(d)
		if m == None:
			Utils().CDial(gtk.MESSAGE_INFO, "Couldn't find device manufacturer", "Please try again.\n\nReturned: %s" % m)
			return

		Parser().write("manuf", m)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')
		Globals.TERM.feed_child('clear\n')
		if not os.path.exists("%s/vendor/%s" % (r, m)):
			Globals.TERM.feed_child("cd %s/device/%s/%s/\n" % (r, m, d))
			Globals.TERM.feed_child('clear\n')
			Globals.TERM.feed_child('./extract-files.sh\n')
			Globals.TERM.feed_child("cd %s\n" % r)

		if not os.path.exists("%s/cacheran" % Globals.myCONF_DIR):
			file("%s/cacheran" % Globals.myCONF_DIR, 'w').close()
			Globals.TERM.feed_child('bash prebuilt/linux-x86/ccache/ccache -M 50G\n')

		Globals.TERM.feed_child('source build/envsetup.sh\n')
		Globals.TERM.feed_child("geek %s\n" % d)
