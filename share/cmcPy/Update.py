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
	def TEXT_COLOR(self):
		myColor = Globals.myTextColor
		b = Parser().read("branch")
		d = Parser().read("device")
		r = Parser().read("repo_path")
		if r == "Default":
			r = Globals.myDEF_REPO_PATH
		Globals.branchLab.set_markup("<span color=\"%s\"><small>Branch</small></span>" % myColor)
		Globals.LinkContact.set_markup("<span color=\"%s\">Contact</span>" % myColor)
		Globals.deviceLab.set_markup("<span color=\"%s\"><small>Device</small></span>" % myColor)
		Globals.syncjobsLab.set_markup("<span color=\"%s\"><small>Sync jobs</small></span>" % myColor)
		Globals.makeLab.set_markup("<span color=\"%s\"><small>Make jobs</small></span>" % myColor)
		Globals.compileLab.set_markup("<span color=\"%s\"><small>Compile</small></span>" % myColor)
		Globals.syncLab.set_markup("<span color=\"%s\"><small>Sync</small></span>" % myColor)
		Globals.clobberLab.set_markup("<span color=\"%s\"><small>Clobber</small></span>" % myColor)
		Globals.build_appLab.set_markup("<span color=\"%s\"><small><small>Build specific <b>app/binary</b> here. :: <b>enter</b> ::</small></small></span>" % myColor)
		Globals.KEY_BIND_INFO.set_markup("<small><small><span color=\"%s\">[CTL-L + (<b>v</b> = View config, <b>a</b> = Start adb, <b>m</b> = Main start/stop, <b>s</b> = Sync, <b>b</b> = build/compile, <b>r</b> = Repo path) <b>esc</b> = Quit]</span></small></small>" % myColor)
		Globals.MAIN_INFO.set_markup("<span color=\"%s\"><small>Device: <b>%s</b> <big>|</big> Branch: <b>%s</b> <big>|</big> Repo path: <b>%s</b></small></span>" % (myColor, d,b,r))

	def DEVICES(self):
		def callback_device(widget, data=None):
			Parser().write("device", data)

		b = Parser().read("branch")
		if "Default" in b:
			Utils().CDial(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
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
			dialog = gtk.Dialog("Choose device", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
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
				filehandle = urllib.urlopen(useBranch)
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

