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
import gtk
from glob import glob

from Globals import Globals
from Parser import Parser

class Utils():
	def ViewConfig(self):
		myColor = Parser().read("text_color")

		def btn(obj):
			Globals().CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		dialog = gtk.Dialog("Cmcompiler", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(800, 400)
		color = gtk.gdk.color_parse(Parser().read('background_color'))
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.set_resizable(False)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.show()
		table = gtk.Table(1, 1, False)
		table.show()
		view = gtk.Viewport()
		view.modify_bg(gtk.STATE_NORMAL, color)
		view.add(table)
		view.show()
		sw.add(view)
		frame = gtk.Frame()
		frame.add(sw)
		frame_label = gtk.Label()
		frame_label.set_markup("<span color=\"%s\">Configuration</span>" % myColor)
		frame_label.show()
		frame.set_label_widget(frame_label)
		frame.set_border_width(15)
		frame.show()
		dialog.vbox.pack_start(frame, True, True, 0)

		try:
			f = open(Globals.myCONF)
			count = 0
			for line in f:
				if "Cmc" in line:
					pass
				elif line == '\n':
					pass
				else:
					count += 1
					i = line.split("=")
					x = i[0]
					y = i[1]
					label = gtk.Label()
					label.set_markup("<span color=\"%s\"><b>%s:</b> <small>%s</small></span>" % (myColor, x, y))
					label.show()
					table.attach(label, 0, 1, count-1, count, xpadding=10, ypadding=10)
		except IOError:
			Globals().CDial(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

		dialog.run()
		dialog.destroy()

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

	def CDial(self, dialog_type, title, message):
		myColor = Parser().read("text_color")
		color = gtk.gdk.color_parse(Parser().read('background_color'))
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=dialog_type, buttons=gtk.BUTTONS_OK)
		dialog.set_markup("<span color=\"%s\"><b>%s</b></span>" % (myColor, title))
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.format_secondary_markup("<span color=\"%s\">%s</span>" % (myColor, message))
		dialog.run()
		dialog.destroy()
		return True

	def QDial(self, title, message):
		myColor = Parser().read("text_color")
		color = gtk.gdk.color_parse(Parser().read('background_color'))
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
		dialog.set_markup("<span color=\"%s\"><b>%s</b></span>" % (myColor, title))
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.format_secondary_markup("<span color=\"%s\">%s</span>" % (myColor, message))
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			return True
		else:
			return False
