#!/usr/bin/env python

import pygtk
import gtk
pygtk.require('2.0')
import os

from ..Globals import Globals
from ..Parser import Parser
from ..Utils import Utils

######################################################################
# About
######################################################################
class CyanogenMod():

	URL = "https://github.com/CyanogenMod"
	RAW_URL = "https://raw.github.com/CyanogenMod"
	INIT_URL = "https://github.com/CyanogenMod/android.git"
	JELLYBEAN_URL = "%s/android_vendor_cm/jellybean/jenkins-build-targets" % RAW_URL
	ICS_URL = "%s/android_vendor_cm/ics/jenkins-build-targets" % RAW_URL
	GINGERBREAD_URL = "%s/android_vendor_cyanogen/gingerbread/vendorsetup.sh" % RAW_URL

	BranchList = ["gingerbread", "ics", "jellybean"]

	AboutDesc = "Type some things here about the rom and about it's design!"

	# GeekRom Images
	Images = ["screeny1.jpg", "screeny2.jpg", "screeny3.jpg"]
	ScreenList = []
	for i in Images:
		ScreenList.append("%s/aosp/%s" % (Globals.myScreenURL, i))

	def getBranch(self, arg):
		CM = CyanogenMod()
		b = Parser().read("branch").strip()
		BR = None
		if arg == "init":
			BR = CM.INIT_URL
		else:
			if b == "gingerbread":
				BR = CM.GINGERBREAD_URL
			elif b == "ics":
				BR = CM.ICS_URL
			elif b == "jellybean":
				BR = CM.JELLYBEAN_URL
			else:
				pass

		return BR

	def Compile(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		m = Utils().getManu(d)
		Globals.TERM.feed_child('clear\n')
		if m == None:
			Globals.TERM.feed_child('python build/tools/roomservice.py cm_%s\n' % d)
			Utils().CDial(gtk.MESSAGE_INFO, "<small>Running roomservice", "Roomservice is running right now, you will have to run, \"<b>Compile</b>\" again after this is done downloading your kernel and device dependancies.</small>")
		else:
			Parser().write("manuf", m)
			Globals.TERM.feed_child('clear\n')
			if not os.path.exists("%s/vendor/%s" % (r, m)) and b is not "jellybean":
				if Utils().is_adb_running() == True:
					Globals.TERM.feed_child("cd %s/device/%s/%s/\n" % (r, m, d))
					Globals.TERM.feed_child('clear\n')
					Globals.TERM.feed_child('./extract-files.sh\n')
					Globals.TERM.feed_child("cd %s\n" % r)
				else:
					Utils().CDial(gtk.MESSAGE_ERROR, "Adb isn't running", "Need adb to setup vendor files.\n\nIs this something you are going to do yourself?\n\nPlease try again.")
					Globals.TERM.set_background_saturation(1.0)
					Globals.TERM.feed_child('clear\n')

			if not os.path.exists("%s/cacheran" % Globals.myCONF_DIR) and b is not "gingerbread":
				os.chdir(r)
				file("%s/cacheran" % Globals.myCONF_DIR, 'w').close()
				Globals.TERM.feed_child('bash prebuilt/linux-x86/ccache/ccache -M 50G\n')

			if b is not "gingerbread":
				Globals.TERM.feed_child('bash vendor/cm/get-prebuilts\n')
			else:
				Globals.TERM.feed_child('bash vendor/cyanogen/get-rommanager\n')

			Globals.TERM.feed_child('source build/envsetup.sh\n')

		if d is "gingerbread":
			Globals.TERM.feed_child("lunch cyanogen_%s-eng\n" % d)
		else:
			Globals.TERM.feed_child("lunch cm_%s-userdebug\n" % d)
		Globals.TERM.feed_child("lunch cm_%s-userdebug\n" % d)
		Globals.TERM.feed_child("time make -j%s otapackage\n" % Globals.PROCESSORS)
