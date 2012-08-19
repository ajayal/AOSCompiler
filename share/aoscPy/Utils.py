#!/usr/bin/env python

import os
import gtk
from glob import glob
import urllib
import urllib2
import re
import shutil
import commands

from Globals import Globals
from Parser import Parser

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

	def deviceFile(self):
		FILE = None
		a = Parser().read("rom_abrv")
		b = Parser().read("branch")
		if a == "CM":
			if b == "gb":
				FILE = "device.mk"
			if b == "ics" or b == "jellybean":
				FILE = "cm.mk"

		if a == "GR":
			if b == "master":
				FILE = "geek.mk"

		return FILE

	def getManu(self, device):
		s = None
		FILE = Utils().deviceFile()
		if FILE is not None:
			paths = glob("device/*/*/%s" % FILE)
		else:
			paths = None

		if paths is not None:
			for x in paths:
				if device in x:
					i = x.split("/")
					i = i[1]
					s = i

		return s

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
			#print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
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
		Utils().update()

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

			if not "#" in lines:
				line = lines.strip()
				button_count += 1
				button = "button%s" % (button_count)

				try:
					if line:
						x = line.split(" ")
						radio = x[1]
					else:
						break
				except:
					radio = line.strip()
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
			#print b
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

	def ResetTerm(self):
		Globals.TERM.set_background_saturation(1.0)
		Globals.TERM.fork_command('clear')

	def choose_repo_path(self):
		direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		r = direct.run()
		repo_dir = direct.get_filename()
		direct.destroy()
		if r == gtk.RESPONSE_ACCEPT:
			try:
				Parser().write("repo_path", repo_dir)
				Utils().update()
			except NameError:
				pass

	def update(self):
		b = Parser().read("branch")
		d = Parser().read("device")
		p = Parser().read("repo_path")
		r = Parser().read("rom_dist")
		a = Parser().read("rom_abrv")
		Globals.branchLab.set_markup("<small>Branch: <b>%s</b></small>" % b)
		Globals.LinkContact.set_markup("<small>Contact</small>")
		Globals.runLab.set_markup("<small>Run</small>")
		Globals.romLab.set_markup("<small>Rom: <b>%s</b></small>" % a)
		Globals.aboutRomLab.set_markup("<small>About rom</small>")
		Globals.toolsLab.set_markup("<small>Options</small>")
		Globals.deviceLab.set_markup("<small>Device: <b>%s</b></small>" % d)
		Globals.aoscTitleLab.set_markup("<span font=\"18\">%s</span>" % r)
		Globals.syncjobsLab.set_markup("<small>Sync jobs</small>")
		Globals.makeLab.set_markup("<small>Make jobs</small>")
		Globals.compileLab.set_markup("<small>Compile</small>")
		Globals.runFrameLab.set_markup("<small>Run options</small>")
		Globals.buildFrameLab.set_markup("<small>Build options</small>")
		Globals.syncLab.set_markup("<small>Sync</small>")
		Globals.clobberLab.set_markup("<small>Clobber</small>")
		Globals.build_appLab.set_markup("<small><small>Build specific <b>app/binary</b> here. :: <b>enter</b> ::</small></small>")
		Globals.KEY_BIND_INFO.set_markup("<small><small>[CTL-L + (<b>v</b> = View config, <b>a</b> = Start adb, <b>m</b> = Main start/stop, <b>s</b> = Sync, <b>b</b> = build/compile, <b>r</b> = Repo path) <b>esc</b> = Quit]</small></small>")
		Globals.MAIN_INFO.set_markup("<small>Repo path: <b>%s</b></small>" % p)
		if not os.path.exists(p):
			Utils().CDial(gtk.MESSAGE_ERROR, "No Folder Found!", "Path: %s\n\nDoes not exist and it needs to to continue." % p)
			Utils().choose_repo_path()

	def run_custom_device(self):
		title = "Setup custom device"
		message = "Please setup your device here:"
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		table = gtk.Table(8, 1, False)
		dialog.vbox.pack_start(table)
		label = gtk.Label()
		label.set_markup("Device name:")
		label.show()
		entry = gtk.Entry()
		entry.show()
		label1 = gtk.Label()
		label1.set_markup("Device manufacturer:")
		label1.show()
		entry1 = gtk.Entry()
		entry1.show()
		label2 = gtk.Label()
		label2.set_markup("Device tree url:")
		label2.show()
		entry2 = gtk.Entry()
		entry2.show()
		label3 = gtk.Label()
		label3.set_markup("Device tree branch:")
		label3.show()
		entry3 = gtk.Entry()
		entry3.show()
		table.attach(label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label1, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry1, 0, 1, 3, 4, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label2, 0, 1, 4, 5, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry2, 0, 1, 5, 6, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label3, 0, 1, 6, 7, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry3, 0, 1, 7, 8, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.show()
		q = dialog.run()
		if q == gtk.RESPONSE_OK:
			n = entry.get_text()
			m = entry1.get_text()
			u = entry2.get_text()
			b = entry3.get_text()
			r = Parser().read("repo_path")
			os.chdir(r)
			manu_path = "%s/device/%s" % (r,m)
			if not os.path.exists(manu_path):
				os.mkdir(manu_path)
			if os.path.exists("%s/%s" % (manu_path, n)):
				shutil.rmtree("%s/%s" % (manu_path, n))
			os.chdir(manu_path)
			Globals.TERM.set_background_saturation(0.3)
			Globals.TERM.fork_command('bash')
			Globals.TERM.feed_child('git clone %s -b %s %s\n' % (u,b,n))
		else:
			Utils().CDial(gtk.MESSAGE_INFO, "Skipping this", "No changes have been made!")
		dialog.destroy()

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

