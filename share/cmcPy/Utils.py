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
import urllib
import urllib2
import re
import commands

from Globals import Globals
from Parser import Parser
from Update import Update

class Utils():
	def is_adb_running(self):
		running = False
		cmd = commands.getoutput("adb devices")
		x = cmd.split(" ")
		x = x[4]
		if "device" in x:
			running = True

		return running

	def ViewConfig(self):
		def btn(obj):
			Globals().CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		dialog = gtk.Dialog("Cmcompiler", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(600, 400)
		dialog.set_resizable(False)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.show()
		table = gtk.Table(1, 1, False)
		table.show()
		sw.add_with_viewport(table)
		frame = gtk.Frame()
		frame.add(sw)
		frame_label = gtk.Label()
		frame_label.set_markup("Configuration:")
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
					label.set_markup("<b>%s:</b> <small>%s</small>" % (x, y))
					label.show()
					label.set_alignment(xalign=0, yalign=0)
					label.set_padding(5, 5)
					table.attach(label, 0, 1, count-1, count)
		except IOError:
			Globals().CDial(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

		dialog.run()
		dialog.destroy()

	def Compile(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		os.chdir(r)
		m = Utils().getManu(d, b)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')
		if m == None:
			print "Here"
			os.chdir(p)
			Globals.TERM.feed_child('clear\n')
			Globals.TERM.feed_child('python build/tools/roomservice.py cm_%s\n' % d)
			Utils().CDial(gtk.MESSAGE_INFO, "<small>Running roomservice", "Roomservice is running right now, you will have to run, \"<b>Compile</b>\" again after this is done downloading your kernel and device dependancies.</small>")
		else:
			Parser().write("manuf", m)
			Globals.TERM.feed_child('clear\n')
			if not os.path.exists("%s/vendor/%s" % (r, m)) and b is not "jellybean":
				if Utils().is_abd_running() == True:
					os.chdir("%s/devices/%s/%s/" % (r, m, d))
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

	def which(self, program):
		def is_exe(fpath):
			return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

		fpath, fname = os.path.split(program)
		if fpath:
			if is_exe(program):
				return program
		else:
			for path in os.environ["PATH"].split(os.pathsep):
				exe_file = os.path.join(path, program)
				if is_exe(exe_file):
					return exe_file

		return None

	def choose_branch(self, obj):
		branchList = []
		rom = Parser().read("rom_abrv")
		if rom == "CM":
			for x in ["gingerbread", "ics", "jellybean"]:
				branchList.append(x)
		elif rom == "AOKP":
			for x in ["ics", "jb"]:
				branchList.append(x)
		elif rom == "AOSP":
			for x in ["gingerbread", "gingerbread-release", "ics-mr1", "jb-dev", "android-4.1.1_r4", "master"]:
				branchList.append(x)
		elif rom == "CNA":
			for x in ["jellybean"]:
				branchList.append(x)
		elif rom == "GR":
			for x in ["master"]:
				branchList.append(x)
		else:
			return

		def callback_branch(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			Parser().write("branch", data)

		dialog = gtk.Dialog("Choose branch", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(260, 200)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(0)

		scroll.add_with_viewport(table)
		table.show()

		device = gtk.RadioButton(None, None)

		button_count = 0
		for radio in branchList:

			button_count += 1
			button = gtk.RadioButton(group=device, label="%s" % (radio))
			button.connect("toggled", callback_branch, radio)
			table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.FILL)
			button.show()

		dialog.run()
		dialog.destroy()
		Update().TEXT()

	def aboutRom(self, obj):
		r = Parser().read("rom_dist")
		a = Parser().read("rom_abrv")
		if a == "AOSP":
			ImageList = Globals.aospScreenyList
		else:
			ImageList = None
			return
		dialog = gtk.Dialog("About: %s" % r, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_resizable(False)

		label = gtk.Label(a)
		label.show()
		dialog.vbox.pack_start(label, True, True, 0)

		table = gtk.Table(2, 1, False)
		table.show()

		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scroll.add_with_viewport(table)
		scroll.set_size_request(700, 475)
		scroll.show()
		frame = gtk.Frame()
		frame.add(scroll)
		frame.show()
		dialog.vbox.pack_start(frame, True, True, 0)

		count = 0
		for i in ImageList:
			count+=1
			image = gtk.Image()
			image.show()
			imgurl = urllib2.urlopen(i)
			loader = gtk.gdk.PixbufLoader()
			loader.write(imgurl.read())
			loader.close()
			image.set_from_pixbuf(loader.get_pixbuf())
			table.attach(image, count-1, count, 0, 1, xpadding=20, ypadding=10)

		dialog.run()
		dialog.destroy()

	def Devices(self):
		def callback_device(widget, data=None):
			Parser().write("device", data)

		BR = Utils().getBranchUrl("raw")
		if BR == None:
			return

		a = Parser().read("rom_abrv")
		dialog = gtk.Dialog("Choose device for %s" % a, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(260, 400)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(5)

		scroll.add_with_viewport(table)
		table.show()

		device = gtk.RadioButton(None, None)

		try:
			filehandle = urllib.urlopen(BR)
		except IOError:
			Utils().CDial(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

		button_count = 0
		for lines in filehandle.readlines():

			if "combo" in lines and not "#" in lines:
				button_count += 1
				button = "button%s" % (button_count)

				x = lines.split(" ")
				radio = x[1]
				x = radio.split("_")
				radio = x[1]
				x = radio.split("-")
				radio = x[0]

				button = gtk.RadioButton(group=device, label="%s" % (radio))
				button.connect("toggled", callback_device, "%s" % (radio))
				table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

		filehandle.close()

		dialog.run()
		dialog.destroy()

	def getBranchUrl(self, arg):
		BR = None
		b = Parser().read("branch")
		b = b.strip()
		a = Parser().read("rom_abrv")
		a = a.strip()
		if b == "Default":
			Utils().CDial(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
			return None

		if a == "CM":
			if arg == "init":
				BR = Globals.myCM_INIT_URL
			else:
				if b == "gingerbread":
					BR = Globals.myCM_GB_URL
				elif b == "ics":
					BR = Globals.myCM_ICS_URL
				elif b == "jellybean":
					BR = Globals.myCM_JB_URL
				else:
					pass
		elif a == "CNA":
			if arg == "init":
				BR = Globals.myCNA_INIT_URL
			else:
				if b == "jellybean":
					BR = Globals.myCNA_JB_URL
				else:
					pass
		elif a == "GR":
			if arg == "init":
				BR = Globals.myGR_INIT_URL
			else:
				if b == "master":
					BR = Globals.myGR_JB_URL
				else:
					pass
		elif a == "AOSP":
			print b
			if arg == "init":
				BR = Globals.myAOSP_INIT_URL
			else:
				if b == "gingerbread" or b == "gingerbread-release":
					BR = Globals.myAOSP_GB_URL
				elif b == "ics-mr1":
					BR = Globals.myAOSP_ICS_URL
				elif b == "android-4.1.1_r4" or b == "jb-dev":
					BR = Globals.myAOSP_JB_URL
				else:
					pass
		elif a == "AOKP":
			if arg == "init":
				BR = Globals.myAOKP_INIT_URL
			else:
				if b == "ics":
					BR = Globals.myAOKP_ICS_URL
				elif b == "jb":
					BR = Globals.myAOKP_JB_URL
				else:
					pass
		else:
			pass

		return BR

	def CDial(self, dialog_type, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=dialog_type, buttons=gtk.BUTTONS_OK)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		dialog.run()
		dialog.destroy()
		return True

	def QDial(self, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			return True
		else:
			return False

