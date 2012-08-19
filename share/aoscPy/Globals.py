#!/usr/bin/env python

import os
import gtk
import vte

class Globals():

	# Resources
	myMainTitle = "Android Open Source Compiler"
	myIMGS = "/usr/share/aoscompiler/images"
	myICON = "%s/aosc-icon.png" % myIMGS
	myTermWall = "%s/termwall.jpg" % myIMGS
	myTermWall_CM = "%s/termwall_cm.jpg" % myIMGS
	myTermWall_CNA = "%s/termwall_cna.jpg" % myIMGS
	myTermWall_AOKP = "%s/termwall_aokp.jpg" % myIMGS
	myTermWall_AOSP = "%s/termwall_aosp.jpg" % myIMGS
	myTHEME = "%s/theme/" % myIMGS
	SyncImg = "%s/sync.png" % myIMGS
	CompileImg = "%s/compile.png" % myIMGS
	DeviceImg = "%s/device.png" % myIMGS
	ClobImg = "%s/clobber.png" % myIMGS
	myBASH = "/usr/share/cmcompiler/cmcBash"

	#####
	# Remote Images per rom type
	#####
	# Aosp
	aospScreenyList = []
	aospScreeny1 = "https://raw.github.com/lithid/AOSCompiler/master/extras/rom/aosp/screeny1.jpg"
	aospScreeny2 = "https://raw.github.com/lithid/AOSCompiler/master/extras/rom/aosp/screeny2.jpg"
	aospScreeny3 = "https://raw.github.com/lithid/AOSCompiler/master/extras/rom/aosp/screeny3.jpg"
	aospScreenyList.append(aospScreeny1)
	aospScreenyList.append(aospScreeny2)
	aospScreenyList.append(aospScreeny3)

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
	myREPO_TOOL_URL = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"
	myGETCM = "http://get.cm"
	myCMWIKI = "http://wiki.cyanogenmod.com"
	myAOSP_SITE = "http://source.android.com"

	#####
	# Device URLs
	#####
	# Cyanogenmod
	myCM_URL = "https://github.com/CyanogenMod"
	myCM_RAW_URL = "https://raw.github.com/CyanogenMod"
	myCM_INIT_URL = "https://github.com/CyanogenMod/android.git"
	myCM_JB_URL = "%s/android_vendor_cm/jellybean/jenkins-build-targets" % myCM_RAW_URL
	myCM_ICS_URL = "%s/android_vendor_cm/ics/jenkins-build-targets" % myCM_RAW_URL
	myCM_GB_URL = "%s/android_vendor_cyanogen/gingerbread/vendorsetup.sh" % myCM_RAW_URL
	# Codename Android
	myCNA_URL = "https://github.com/CNA"
	myCNA_RAW_URL = "https://raw.github.com/CNA"
	myCNA_INIT_URL = "https://github.com/CNA/android_manifest.git"
	myCNA_JB_URL = "%s/proprietary_vendor_cna/jellybean/vendorsetup.sh" % myCNA_RAW_URL
	# Android Open Kang Project
	myAOKP_URL = "https://github.com/AOKP"
	myAOKP_RAW_URL = "https://raw.github.com/AOKP"
	myAOKP_INIT_URL = "https://github.com/AOKP/platform_manifest.git"
	myAOKP_ICS_URL = "%s/vendor_aokp/ics/vendorsetup.sh" % myAOKP_RAW_URL
	myAOKP_JB_URL = "%s/vendor_aokp/jb/vendorsetup.sh" % myAOKP_RAW_URL
	# Android Open Source Project
	myGR_INIT_URL = "https://github.com/GeekRom/android_manifest.git"
	myGR_RAW_URL = "https://raw.github.com/GeekRom"
	myGR_JB_URL = "%s/android_vendor_geek/master/vendorsetup.sh" % myGR_RAW_URL
	# Android Open Source Project
	myAOSP_INIT_URL = "https://android.googlesource.com/platform/manifest"
	myRAW_URL = "https://raw.github.com/lithid"
	myAOSP_JB_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-JB" % myRAW_URL
	myAOSP_ICS_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-ICS" % myRAW_URL
	myAOSP_GB_URL = "%s/AOSCompiler/master/extras/rom/aosp/DeviceList-GB" % myRAW_URL

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
	
	numprocs = [ int(line.strip()[-1]) for line in open('/proc/cpuinfo', 'r') if line.startswith('processor') ][-1] + 1

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

