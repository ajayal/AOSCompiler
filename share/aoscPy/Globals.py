#!/usr/bin/env python

import os
import gtk
import vte

from Tools import Tools

class Globals():

	# Resources
	myMainTitle = "Android Open Source Compiler"
	myIMGS = "/usr/share/aoscompiler/images"
	myICON = "%s/aosc-icon.png" % myIMGS
	myTermWall = "%s/termwall.jpg" % myIMGS
	myTHEME = "%s/theme/" % myIMGS
	SyncImg = "%s/sync.png" % myIMGS
	CompileImg = "%s/compile.png" % myIMGS
	DeviceImg = "%s/device.png" % myIMGS
	ClobImg = "%s/clobber.png" % myIMGS
	myBASH = "/usr/share/aoscompiler/cmcBash"
	myScreenURL = "https://raw.github.com/lithid/AOSCompiler/master/extras/rom"

	# Local config junk
	myHOME = os.environ['HOME']
	myGIT_CONF = "%s/.gitconfig" % (myHOME)
	myCONF_DIR = "%s/.aoscompiler" % (myHOME)
	myCONF = "%s/aoscompiler.conf" % (myCONF_DIR)
	myCONFIRM = "%s/ask.confim" % (myCONF_DIR)
	myREPO_CONF = "%s/repo_list" % (myCONF_DIR)
	myDEF_REPO_PATH = "%s/build" % (myCONF_DIR)
	askConfirm = "%s/ask.confim" % (myCONF_DIR)

	# Needed web urls
	myFORUM_URL = "http://forum.xda-developers.com/showthread.php?t=1415661"
	myDONATE = "http://forum.xda-developers.com/donatetome.php?u=2709018"
	myREPO_TOOL_URL = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"

	PROCESSORS = Tools().processor()

	# Device lists
	dl_version = None
	dl_url = None
	dl_device = None
	mylist = []

	# Info stuff
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

	MAIN_WIN = gtk.Window(gtk.WINDOW_TOPLEVEL)
	DEV_BTN = gtk.Button()
	runBtn = gtk.Button()
	branchBtn = gtk.Button()
	aboutRomBtn = gtk.Button()
	KEY_BIND_INFO = gtk.Label()
	MAIN_INFO = gtk.Label()
	runLab = gtk.Label()
	romLab = gtk.Label()
	LinkContact = gtk.Label()
	aboutRomLab = gtk.Label()
	branchLab = gtk.Label()
	toolsLab = gtk.Label()
	clobberLab = gtk.Label()
	deviceLab = gtk.Label()
	syncjobsLab = gtk.Label()
	makeLab = gtk.Label()
	compileLab = gtk.Label()
	syncLab = gtk.Label()
	build_appLab = gtk.Label()
	buildFrameLab = gtk.Label()
	runFrameLab = gtk.Label()
	aoscTitleLab = gtk.Label()
	checkCompile = gtk.CheckButton()
	checkSync = gtk.CheckButton()
	checkClobber = gtk.CheckButton()
	TERM = vte.Terminal()
	TERM.set_font_from_string("Ubuntu Mono 9")
	TERM.set_background_image_file(myTermWall)
	TERM.set_background_saturation(1.0)

