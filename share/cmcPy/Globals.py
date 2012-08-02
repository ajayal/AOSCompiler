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

class Globals():

	# Resources
	myIMGS = "/usr/share/cmcompiler/images"
	myICON = "%s/cmc-icon.png" % myIMGS
	myWallMain = "%s/CM_WALL_MAIN.jpg" % myIMGS
	myTHEME = "%s/theme/" % myIMGS
	myBASH = "/usr/share/cmcompiler/cmcBash"
	myColor = "Black"

	# VTE Commands
	mySYNC_SCRIPT = "%s/sync_script.sh" % myBASH
	myCOMPILE_SCRIPT = "%s/compile_script.sh" % myBASH
	myROOMSERVICE_SCRIPT = "%s/roomservice_script.sh" % myBASH
	myCMC_VT_TITLE = "%s/cm_vt_title.sh" % myBASH
	myA_VIEW_CONFIG = "%s/A_view_config.sh" % myBASH
	myA_VIEW_GIT_CONFIG = "%s/A_view_git_config.sh" % myBASH
	myA_ADB_START = "%s/A_adb_start.sh" % myBASH

	# Local config junk
	myHOME = os.environ['HOME']
	myGIT_CONF = "%s/.gitconfig" % (myHOME)
	myCONF_DIR = "%s/.cmcompiler" % (myHOME)
	myCONF = "%s/cmcompiler.cfg" % (myCONF_DIR)
	myCONFIRM = "%s/ask.confim" % (myCONF_DIR)
	myREPO_CONF = "%s/repo_list" % (myCONF_DIR)
	myDEF_REPO_PATH = "%s/build" % (myCONF_DIR)
	askConfirm = "%s/ask.confim" % (myCONF_DIR)

	# Needed web urls
	myFORUM_URL = "http://forum.xda-developers.com/showthread.php?t=1415661"
	myDONATE = "http://forum.xda-developers.com/donatetome.php?u=2709018"
	myCM_URL = "https://github.com/CyanogenMod"
	myCM_RAW_URL = "https://raw.github.com/CyanogenMod"
	myCM_JB_URL = "%s/android_vendor_cm/jellybean/vendorsetup.sh" % myCM_RAW_URL
	myCM_ICS_URL = "%s/android_vendor_cm/ics/vendorsetup.sh" % myCM_RAW_URL
	myCM_GB_URL = "%s/android_vendor_cyanogen/gingerbread/vendorsetup.sh" % myCM_RAW_URL
	myINIT_URL = "https://github.com/CyanogenMod/android.git"
	myREPO_TOOL_URL = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"
	myGETCM = "http://get.cm"
	myCMWIKI = "http://wiki.cyanogenmod.com"
	myAOSP_SITE = "http://source.android.com"

	# Meh
	myDEF_BRANCH = "ics"
	dl_version = None
	dl_url = None
	dl_device = None
	mylist = []

	ask_confirm_info = "<small>By no means what so ever is this software or cyanogenmod responsible for what you do to your phone. \
You are taking the risks, you are choosing to this to your phone. By proceeding you are aware, you are warned. No crying or moaning. This software \
was tested by human beings, not cybogs from your mothers closet. Please keep this in mind when something breaks, or hangs.  If you have an issue \
with this software, please let me know.\n\nBy clicking this ok button, you have given me your soul.\n\nPlay safe.\n\n</small>\
<small><small><b>Note:\n- </b><i>This will not proceed unless you agree.</i></small>\n\
<small><b>-</b><i> Cyanogenmod doesn't consider source builds offical, please keep this in mind if you plan on bug reporting.</i></small></small>\n\n\
Any bugs? Please report them <a href=\"https://github.com/lithid/Cmcompiler/issues\">here</a>.\n"

	about_info = "The cyanogenmod compiler was written, not to dismiss the need\
to learn the android system, but to release the need consistly remember menial tasks.\n\n\
Please intend to learn the system, contribute back to any upstream.\n\n\
Happy compiling,\n\nCode: Jeremie Long\nGraphics: SavocaFTW\n\n\
Any bugs? Please report them <a href=\"mailto:https://github.com/lithid/Cmcompiler/issues\">here</a>.\n"

	key_bindings = "<small><small><span color=\"%s\">[CTL-L + (<b>v</b> = View config, <b>a</b> = Start adb, <b>m</b> = Main start/stop, <b>s</b> = Sync, <b>b</b> = build/compile, <b>d</b> = Background color, <b>r</b> = Repo path, <b>esc</b> = Quit)]</span></small></small>" % myColor
	
	numprocs = [ int(line.strip()[-1]) for line in open('/proc/cpuinfo', 'r') if line.startswith('processor') ][-1] + 1

	MAIN_WIN = gtk.Window(gtk.WINDOW_TOPLEVEL)
	DEV_COMBO = gtk.combo_box_new_text()
	KEY_BIND_INFO = gtk.Label()
	MAIN_INFO = gtk.Label()

	def CDial(self, dialog_type, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=dialog_type, buttons=gtk.BUTTONS_OK)
		dialog.set_markup("<b>%s</b>" % title)
		dialog.format_secondary_markup(message)
		dialog.run()
		dialog.destroy()
		return True

	def QDial(self, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
		dialog.set_markup("<b>%s</b>" % title)
		dialog.format_secondary_markup(message)
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			return True
		else:
			return False

