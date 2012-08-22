#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

from ..Globals import Globals
from ..Parser import Parser

######################################################################
# About
######################################################################
class AOSP():

	INIT_URL = "https://android.googlesource.com/platform/manifest"
	RAW_URL = "https://raw.github.com/lithid"
	JELLYBEAN_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-JB" % RAW_URL
	ICS_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-ICS" % RAW_URL
	GINGERBREAD_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-GB" % RAW_URL

	BranchList = ["gingerbread", "ics-mr1", "android-4.1.1_r4", "master"]

	AboutDesc = "<small><b>Type</b> some things here about the rom and about it's design! <b>Type</b> some things here about the rom and about it's design!</small>"

	# GeekRom Images
	Images = ["screeny1.jpg", "screeny2.jpg", "screeny3.jpg"]
	ScreenList = []
	for i in Images:
		ScreenList.append("%s/aosp/%s" % (Globals.myScreenURL, i))

	def getBranch(self, arg):
		b = Parser().read("branch").strip()
		BR = None
		if arg == "init":
			BR = AOSP.INIT_URL
		else:
			if b == "gingerbread":
				BR = AOSP.GINGERBREAD_URL
			elif b == "ics-mr1":
				BR = AOSP.ICS_URL
			elif b == "android-4.1.1_r4":
				BR = AOSP.JELLYBEAN_URL
			elif b == "master":
				BR = AOSP.JELLYBEAN_URL
			else:
				pass

		return BR

	def Compile(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		m = Utils().getManu(d)
		if m == None:
			Utils().CDial(gtk.MESSAGE_INFO, "Couldn't find device manufacturer", "Please try again.\n\nReturned: %s" % m)
			return

		Parser().write("manuf", m)
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
		Globals.TERM.feed_child("lunch full_%s-userdebug\n" % d)
		Globals.TERM.feed_child("time make -j%s otapackage\n" % Globals.numprocs)
