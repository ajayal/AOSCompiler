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

import pygtk
pygtk.require('2.0')
import random, time, datetime
import threading
import gtk
import gobject
import os
import sys
import array
import urllib
import shutil
import time
import pynotify
import commands
from glob import glob
import ConfigParser
import platform
import urllib2
import re
import subprocess

gtk.threads_init()

# Path variables
u_home = os.environ['HOME']
#u_term = os.environ['TERM']

gitconfig = "%s/.gitconfig" % (u_home)
configdir = "%s/.cmcompiler" % (u_home)
cmcconfig = "%s/.cmcompiler/cmcompiler.cfg" % (u_home)
build_script = "/usr/share/cmcompiler/prog/scripts/build-it.sh"
askConfirm = "%s/.cmcompiler/ask.confim" % (u_home)
repo_config = "%s/.cmcompiler/repo_list" % (u_home)
default_repo_path = "%s/.cmcompiler/build" % (u_home)
cmcMainImage = "/usr/share/cmcompiler/images/cmc-main.png"
cmcIcon = "/usr/share/cmcompiler/images/cmc-icon.png"
cmcInt = "/usr/share/cmcompiler/images/indicator/cmc-int.png"
cmcIntD = "/usr/share/cmcompiler/images/indicator/cmc-int-blue.png"
cmcIntE = "/usr/share/cmcompiler/images/indicator/cmc-int-red.png"
cmcTheme = "/usr/share/cmcompiler/images/theme/"
cmcThemeSmall = "/usr/share/cmcompiler/images/theme/small"
default_branch = "ics"
cmcUrl = "http://forum.xda-developers.com/showthread.php?t=1415661"
donateUrl = "http://forum.xda-developers.com/donatetome.php?u=2709018"
urlCmIcs = "https://raw.github.com/CyanogenMod/android_vendor_cm/ics/vendorsetup.sh"
urlCmGb = "https://raw.github.com/CyanogenMod/android_vendor_cyanogen/gingerbread/vendorsetup.sh"
cmGit = "https://github.com/CyanogenMod/android.git"
repoToolUrl = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"
configDeviceName = "config_device_name:"
configCustomRepoPath = "config_custom_repo_path:"
configBranch = "config_branch:"

placeIcon = gtk.gdk.pixbuf_new_from_file(cmcIcon)

dl_version = None
dl_url = None
dl_device = None
mylist = []

MainAppWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
GlobalProgressBar = gtk.ProgressBar()
GlobalProgressWindow = gtk.Window()
SplashW = gtk.Window(gtk.WINDOW_TOPLEVEL)

######################################################################
# Helper functions
#---------------------------------------------------------------------
def repo_sync_go():
	print "Here"
	repo_path = read_parser("repo_path")
	if repo_path == "Default":
		repo_path = default_repo_path

	print repo_path

	repo_branch = read_parser("branch")

	chk_repo = common_chk()

	os.chdir(repo_path)
	if chk_repo == 1:
		cmd1 = "%s -hold -e \"repo init -u %s -b %s\"" % (u_term, cmGit, repo_branch)
		cmd2 = "%s -hold -e \"repo sync -j1\"" % (u_term)
		d = "%s/.repo" % (repo_path)
		if not os.path.exists(d):
			print cmd1
			os.system(cmd1)
		print cmd2
		os.system(cmd2)

def repo_build_go():
	def build_gb():
		e = "%s/NoAdbRunning" % (configdir)
		if os.path.exists(e):
			os.remove(e)
		CHECKS = 0
		d = "%s/.repo" % (repo_path)
		if not os.path.exists(d):
			CHECKS+=1
			e = "%s/NeedSync" % (configdir)
			file(e, 'w').close()

		if CHECKS == 0:
			e = "%s/NoDevice" % (configdir)
			if os.path.exists(e):
				os.remove(e)
			d = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
			if not os.path.exists(d):
				e = "%s/NoDevice" % (configdir)
				file(e, 'w').close()

			if CHECKS == 0:
				e = "%s/NoAdbRunning" % (configdir)
				if os.path.exists(e):
					os.remove(e)
				d = "%s/vendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
				if not os.path.exists(d):
					c = checkAdb()
					if c == False:
						CHECKS+=1
						e = "%s/NoAdbRunning" % (configdir)
						file(e, 'w').close()

				if CHECKS == 0:
					e = "%s/ExtractFiles" % (configdir)
					if os.path.exists(e):
						os.remove(e)
					c = extractFiles(repo_path, build_manu, build_device)
					if c == False:
						CHECKS+=1
						e = "%s/ExtractFiles" % (configdir)
						file(e, 'w').close()

					if CHECKS == 0:
						os.chdir(repo_path)
						cacheran = "%s/cacheran" % configdir
						if not os.path.exists(cacheran):
							cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
							os.system(cmd)
							file(cacheran, 'w').close()
						cmd = "/bin/bash %s/vendor/cyanogen/get-rommanager" % (repo_path)
						os.system(cmd)
						cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
						os.system(cmd)

	def build_ics():
		e = "%s/NeedSync" % (configdir)
		if os.path.exists(e):
			os.remove(e)
		CHECKS = 0
		build_manu = getManu(build_device, "ics")

		d = "%s/.repo" % (repo_path)
		if not os.path.exists(d):
			CHECKS+=1
			e = "%s/NeedSync" % (configdir)
			file(e, 'w').close()

		if CHECKS == 0:
			e = "%s/NoDevice" % (configdir)
			if os.path.exists(e):
				os.remove(e)
			d = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
			if not os.path.exists(d):
				os.chdir(repo_path)
				cmd = "python build/tools/roomservice.py cm_" + build_device
				os.system(cmd)
				time.sleep(2)
				build_manu = getManu(build_device)
				nd = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
				if not os.path.exists(nd):
					CHECKS+=1
					e = "%s/NoDevice" % (configdir)
					file(e, 'w').close()

			if CHECKS == 0:
				print "Here now"
				e = "%s/NoAdbRunning" % (configdir)
				if os.path.exists(e):
					os.remove(e)
				d = "%s/vendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
				if not os.path.exists(d):
					c = checkAdb()
					if not c == True:
						CHECKS+=1
						e = "%s/NoAdbRunning" % (configdir)
						file(e, 'w').close()

				if CHECKS == 0:
					e = "%s/ExtractFiles" % (configdir)
					if os.path.exists(e):
						os.system(e)
					c = extractFiles(repo_path, build_manu, build_device)
					if not c == True:
						CHECKS+=1
						e = "%s/ExtractFiles" % (configdir)
						file(e, 'w').close()

					if CHECKS == 0:
						os.chdir(repo_path)
						cacheran = "%s/cacheran" % configdir
						if not os.path.exists(cacheran):
							cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
							os.system(cmd)
							file(cacheran, 'w').close()
						cmd = "/bin/bash %s/vendor/cm/get-prebuilts" % (repo_path)
						os.system(cmd)
						cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
						os.system(cmd)

	def start_build():
		chk_repo = common_chk()
		if chk_repo == 1:
			if repo_branch == "ics":
				build_ics()
			elif repo_branch == "gingerbread":
				build_gb()
			else:	
				print "Default"

		elif chk_repo == 0:
			r = "%s/NeedRepoScript" % (configdir)
			file(r, 'w').close()

		elif chk_repo == 2:
			d = "%s/NoDeviceC" % (configdir)
			file(d, 'w').close()

		else:
			g = "%s/GenError" % (configdir)
			file(g, 'w').close()

	start_build()

def openBuildFolder():
	t = "%s/out/target/product/%s" % (repo_path, build_device)
	cmd = "nautilus %s" % (t)
	os.system(cmd)
	sys.exit()

def chkInstalled(arg):

	p = False

	cmd = "dpkg --get-selections " + arg
	p = commands.getoutput(cmd)
	try:
		p = p.split("\t")
		p = p[-1]
		if p == "install":
			p = True
		else:
			p = False
	except:
		p = False

	return p

def openFolder(obj):
	t = "%s/Downloads" % (u_home)
	cmd = "nautilus %s" % (t)
	os.system(cmd)
	gtk.main_quit()

def sendNoti(title, summary, icon):
	pynotify.init(title)
	n = pynotify.Notification(title, summary, icon)
	n.show()

def custom_listdir(path):
    dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
    dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))

    return dirs

def checkAdb():
	cmd = "adb devices |wc -l"
	c = commands.getoutput(cmd)
	if not c == "3":
		return False
	else:
		return True

def extractFiles(parg, marg, darg):
	os.chdir(repo_path)
	d = "%s/device/%s/%s" % (parg, marg, darg)
	if os.path.exists(d):
		os.chdir(d)
	if os.path.exists("extract-files.sh"):
		d = "%s/vendor/%s/%s/proprietary" % (parg, marg, darg)
		if not os.path.exists(d):
			cmd = "sh extract-files.sh"
			os.system(cmd)
			d = "%s/vendor/%s/%s/proprietary" % (parg, marg, darg)
			time.sleep(0.5)
			if os.path.exists(d):
				return True
			else:
				return False
		else:
			return True
	else:
		return False

def install_repo():
	cmd1 = "curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > %s/repo" % (configdir)
	cmd2 = "chmod a+x %s/repo" % (configdir)
	cmd3 = "gksudo mv %s/repo /usr/local/sbin/" % (configdir)
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)

def which(program):
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

def custom_dialog(dialog_type, title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=dialog_type,
                               buttons=gtk.BUTTONS_OK)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    dialog.run()
    dialog.destroy()
    return True

def question_dialog(title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=gtk.MESSAGE_QUESTION,
                               buttons=gtk.BUTTONS_YES_NO)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.RESPONSE_YES:
       return True
    else:
       return False

def chk_config():
	if not os.path.exists(configdir):
		os.makedirs(configdir)

def getManu(arg, br):
	s = None
	if br == "gb":
		paths = glob("device/*/*/device.mk")
	elif br == "ics":
		paths = glob("device/*/*/cm.mk")
	else:
		paths = None

	for x in paths:
		if arg in x:
			s = x.split("/")
			s = s[1]
	if s:
		return s
	else:
		return None

def common_chk():
	r = "%s/NeedRepoScript" % (configdir)
	if os.path.exists(r):
		os.remove(r)

	d = "%s/NoDeviceC" % (configdir)
	if os.path.exists(d):
		os.remove(d)

	g = "%s/GenError" % (configdir)
	if os.path.exists(g):
		os.remove(g)

	chk_repo = 0
	global repo_path
	global repo_branch
	p = read_parser("repo_path")
	if not p == "Default":
		repo_path = read_parser("repo_path")
	else:
		repo_path = default_repo_path

	repo_branch = read_parser("branch")
	chk_dev = read_parser("device")
	if not chk_dev == "Default":
		if not os.path.exists(repo_path):
			os.makedirs(repo_path)
		os.chdir(repo_path)
		p = which("repo")
		if p == None:
			chk_repo = 0
		else:
			chk_repo = 1
	else:
		chk_repo = 2

	return chk_repo


def get_askConfirm():
	def askedClicked():
		if not os.path.exists(askConfirm):
			file(askConfirm, 'w').close()

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("**** User Confirmation ****")
	dialog.set_markup("<small>This is what <b>YOU</b> do to <b>YOUR</b> phone.</small>")
	dialog.format_secondary_markup("<small>By no means what so ever is this software or cyanogenmod responsible for what you do to your phone. \
You are taking the risks, you are choosing to this to your phone. By proceeding you are aware, you are warned. No crying or moaning. This software \
was tested by human beings, not cybogs from your mothers closet. Please keep this in mind when something breaks, or hangs.  If you have an issue \
with this software, please let me know.\n\nBy clicking this ok button, you have given me your soul.\n\nPlay safe.\n\n</small>\
<small><small><b>Note:\n- </b><i>This will not proceed unless you agree.</i></small>\n\
<small><b>-</b><i> Cyanogenmod doesn't consider source builds offical, please keep this in mind if you plan on bug reporting.</i></small></small>")
	dialog.set_resizable(False)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		askedClicked()
	else:
		exit()
	dialog.destroy()

def set_git_Text():

	def loginClicked(name, email):
		if not os.path.exists(gitconfig):
			file(gitconfig, 'w').close()
			f = open(gitconfig, 'w')
			f.write("[color]\n")
			f.write("	ui = auto\n")
			f.write("[user]\n")
			f.write("	name = %s\n" % name)
			f.write("	email = %s\n" % email)
			f.write("[review \"review.cyanogenmod.com\"]\n")
			f.write("	username = %s\n" % name)
			f.close()

	def loginChecked(name, email):
		if "ex" in name:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad username", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		elif "ex" in email:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad email", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		else:
			loginClicked(name, email)

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("User settings for repo config..")
	dialog.set_markup("<small>This will be used for <i>identification</i> purposes only</small>")
	dialog.format_secondary_markup("<small>This will be used to create a config file used by the repo script. This script is used to sync the repo locally. This information is not being used in any other way. You can look at the git config here:\n\n<b>%s/.gitconfig</b>\n\n<small><b>Note:</b> <i>This will be needed before we can start using cyanogenmod compiler.</i></small></small>" % u_home)
	dialog.set_resizable(False)

	table = gtk.Table(4, 1, True)
	table.set_row_spacings(5)
	table.show()

	dialog.vbox.pack_start(table, True, True, 0)

	user_entry = gtk.Entry()
	user_entry.set_text("ex. lithid")
	user_lab = gtk.Label("User:")
	user_entry.show()
	user_lab.show()
	email_entry = gtk.Entry()
	email_entry.set_text("ex. mrlithid@gmail.com")
	email_lab = gtk.Label("Email:")
	email_entry.show()
	email_lab.show()

	table.attach(user_lab, 0, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(user_entry, 0, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)
	table.attach(email_lab, 0, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(email_entry, 0, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		name = user_entry.get_text()
		email = email_entry.get_text()
		loginChecked(name, email)
	else:
		exit()
	dialog.destroy()

def read_parser(arg):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		c = config.get(title, arg)

	except ConfigParser.NoSectionError:
		c = "%s" % (default)

	return c

def parser(arg, value):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		getTheme = config.get(title, 'theme')
		getDevice = config.get(title, 'device')
		getBranch = config.get(title, 'branch')
		getRepoPath = config.get(title, 'repo_path')
	except ConfigParser.NoSectionError:
		getTheme = None
		getDevice = None
		getBranch = None
		getRepoPath = None

	config = ConfigParser.RawConfigParser()
	config.add_section(title)

	if arg == "device":
		config.set(title, 'device', value)
	elif getDevice:
		config.set(title, 'device', getDevice)
	else:
		config.set(title, 'device', default)

	if arg == "theme":
		config.set(title, 'theme', value)
	elif getTheme:
		config.set(title, 'theme', getTheme)
	else:
		config.set(title, 'theme', default)

	if arg == "branch":
		config.set(title, 'branch', value)
	elif getBranch:
		config.set(title, 'branch', getBranch)
	else:
		config.set(title, 'branch', default)

	if arg == "repo_path":
		config.set(title, 'repo_path', value)
	elif getRepoPath:
		config.set(title, 'repo_path', getRepoPath)
	else:
		config.set(title, 'repo_path', default)

	with open(cmcconfig, 'wb') as configfile:
    		config.write(configfile)
######################################################################

######################################################################
# Package checking
#---------------------------------------------------------------------

class InstallLabelThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			pbar.pulse()
			label.set_markup("Installing packages...")
			gtk.threads_leave()
			time.sleep(0.1)
			
	def stop(self):
		self.stopthread.set()

class InstallPackageThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			cmd = "gksudo -m \"Here is a list of packages needed to run cmcompiler:\n%s\n\nOnce this runs it can't be stopped, if you are sure, type in the sudo password.\" \"apt-get install -y %s\"" % (packages, packages)
			c = os.system(cmd)
			if not c == 0:
				label.set_markup("Package install not successful!")
				pbar.set_fraction(0)
			else:
				label.set_markup("Packages installed successfully!")
				pbar.set_fraction(1)
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		InstallPackageThread().stop()
		self.stopthread.set()

class chkInstalledPackages():

	def main(self):

		L = []
		pcount = 0

		# ('Ubuntu', '12.04', 'precise')
		plat_list = platform.dist()
		plat_d = plat_list[0]
		plat_v = plat_list[1]
		plat_n = plat_list[2]

		if plat_d == "Ubuntu":
			pcount += 1
			P = ["git-core", "gnupg", "flex", "bison", "gperf", "libsdl1.2-dev", "libesd0-dev", "libwxgtk2.6-dev", "squashfs-tools", "build-essential", "zip", "curl", "libncurses5-dev", "zlib1g-dev", "openjdk-6-jdk", "pngcrush", "schedtool"]
			for x in P:
				i = chkInstalled(x)
				if i == False:
					L.extend([x])
		else:
			custom_dialog(gtk.MESSAGE_WARNING, "Linux Distro", "Sorry, we couldn't detect your linux distro. File a bug report with this info:\n\n<b>Distro: </b>%s\n<b>Version: </b>%s\n<b>Name: </b>%s\n" % (plat_d, plat_v, plat_n))
			L = []

		check = (sys.maxsize > 2**32)
		if check is True:
			if plat_d == "Ubuntu":
				if plat_v == "10.04":
					P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline5-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
					for x in P:
						i = chkInstalled(x)
						if i == False:
							L.extend([x])
				elif plat_v == "11.04":
					P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
					for x in P:
						i = chkInstalled(x)
						if i == False:
							L.extend([x])
				elif plat_v == "12.04" or plat_v == "11.10":
					P = ["g++-multilib", "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev"]
					for x in P:
						i = chkInstalled(x)
						if i == False:
							L.extend([x])
				else:
					print "Nothing to extend, version not matched"

		if not L and pcount == 0:
			custom_dialog(gtk.MESSAGE_INFO, "Empty package list", "After looking at your packages the list is empty, maybe an unsupported distro or filesystem error. Either way I am not able to help without some information. You will not be able to use most features until you install the needed packages, be warned.\n\n Thanks.")
			exit(1)
		elif not L and pcount == 1:
			pass
			print "passing"
			return True
		else:
			packages = ",".join(L).replace(",", " ")
			return packages

class InstallingPackages():

	def main(self):

		packages = chkInstalledPackages().main()

    		def quit(self):
			InstallPackageThread()._Thread__stop()
       			gtk.main_quit()

		if not packages == True:
			window = gtk.Window(gtk.WINDOW_TOPLEVEL)
			window.set_title("Package Installation")
			window.connect("destroy", quit)
			window.set_resizable(False)

        		vbox = gtk.VBox(False, 5)
        		vbox.set_border_width(10)
        		window.add(vbox)
        		vbox.show()

        		align = gtk.Alignment(0.5, 0.5, 0, 0)
        		vbox.pack_start(align, False, False, 5)
        		align.show()

			label = gtk.Label()
			label.set_markup("Waiting to install packages...")
			label.show()

			pbar = gtk.ProgressBar()
			pbar.show()

			vbox.pack_start(label, True, True, 0)
			vbox.pack_start(pbar, True, True, 0)

			InstallPackageThread().start()
			InstallLabelThread().start()

			window.show()
			gtk.main()
		else:
			print "Move along, nothing really going on that concerns you!"
######################################################################

######################################################################
# Setup
#---------------------------------------------------------------------
class Setup():
 
	def main_quit(self, obj):
		gtk.main_quit()
 
	# Main program
	def main(self):

		def callback_device(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("device", data)

		def callback_branch(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("branch", data)

		def choose_branch(obj):

			dialog = gtk.Dialog("Choose branch", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(260, 200)
			dialog.set_resizable(False)

			scroll = gtk.ScrolledWindow()
			scroll.set_border_width(10)
			scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
			dialog.vbox.pack_start(scroll, True, True, 0)
			scroll.show()

			table = gtk.Table(2, 1, False)
			table.set_row_spacings(45)

			scroll.add_with_viewport(table)
			table.show()

			device = gtk.RadioButton(None, None)

			button_count = 0
			for radio in list(["ics", "gingerbread"]):

				button_count += 1
				button = "button%s" % (button_count)

				button = gtk.RadioButton(group=device, label="%s" % (radio))
				button.connect("toggled", callback_branch, "%s" % (radio))
				table.attach(button, 0, 1, 0, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

			dialog.run()
			dialog.destroy()

		def choose_repo_path(obj):
			direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			r = direct.run()
			repo_dir = direct.get_filename()
			direct.destroy()
			if r == gtk.RESPONSE_ACCEPT:
				try:
					parser("repo_path", repo_dir)
				except NameError:
					pass

		def remove_config(obj):
			q = question_dialog("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
			if q == True:
				os.remove(cmcconfig)
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		def view_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)
			dialog.set_resizable(False)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(cmcconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def viewgit_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc git configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)
			dialog.set_resizable(False)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(gitconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def device_list(obj):

			b = read_parser("branch")
			if "Default" in b:
				custom_dialog(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
				chk_config = 0
			elif "gingerbread" in b:
				useBranch = urlCmGb
				chk_config = 1
			elif "ics" in b:
				useBranch = urlCmIcs
				chk_config = 1
			else:
				useBranch = "null"
				chk_config = 0

			if chk_config == True:
				try:
					filehandle = urllib.urlopen(useBranch)
				except IOError:
					custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

				count = 0
				for lines in filehandle.readlines():
					count += 1

				filehandle.close()

				dialog = gtk.Dialog("Choose device", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
				dialog.set_size_request(260, 400)
				dialog.set_resizable(False)

				scroll = gtk.ScrolledWindow()
				scroll.set_border_width(10)
				scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
				dialog.vbox.pack_start(scroll, True, True, 0)
				scroll.show()

				table = gtk.Table(count, 1, False)
				table.set_row_spacings(5)

				scroll.add_with_viewport(table)
				table.show()

				device = gtk.RadioButton(None, None)

				try:
					filehandle = urllib.urlopen(useBranch)
				except IOError:
					custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

				button_count = 0
				for lines in filehandle.readlines():

					if "combo" in lines:
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

		def ThemeClicked(widget, event, data):
			if data == "a-default.png":
				data = "Default"
				icon = "%s/a-default.png" % (cmcThemeSmall)
				sendNoti("Cmc theme", "Default theme has been set", icon)
			else:
				icon = "%s/%s" % (cmcThemeSmall, data)
				sendNoti("Cmc theme", "Theme has been set", icon)
			parser("theme", data)

		dialog = gtk.Dialog("CMC Setup", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_position(gtk.WIN_POS_CENTER)
		dialog.set_resizable(False)

		settings_lab = gtk.Label("Configure your settings here")
		settings_lab.show()
		dialog.vbox.pack_start(settings_lab, False, False, 10)

		table = gtk.Table(6, 2, False)
		table.set_row_spacings(5)
		table.show()

		dialog.vbox.pack_start(table, True, True, 15)

		device_btn = gtk.Button("Choose device")
		device_btn.set_size_request(140, 28)
		device_btn.connect("clicked", device_list)
		device_btn.show()

		branch_btn = gtk.Button("Choose branch")
		branch_btn.set_size_request(140, 28)
		branch_btn.connect("clicked", choose_branch)
		branch_btn.show()

		repo_path_btn = gtk.Button("Choose repo path")
		repo_path_btn.set_size_request(140, 28)
		repo_path_btn.connect("clicked", choose_repo_path)
		repo_path_btn.show()

		viewgit_btn = gtk.Button("View git config")
		viewgit_btn.set_size_request(140, 28)
		viewgit_btn.connect("clicked", viewgit_config)
		viewgit_btn.show()

		view_btn = gtk.Button("View config")
		view_btn.set_size_request(140, 28)
		view_btn.connect("clicked", view_config)
		view_btn.show()

		config_btn = gtk.Button("Remove config")
		config_btn.set_size_request(140, 28)
		config_btn.connect("clicked", remove_config)
		config_btn.show()

		table.attach(device_btn, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(branch_btn, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(repo_path_btn, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(viewgit_btn, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(view_btn, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(config_btn, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)


		theme_label = gtk.Label()
		theme_label.set_markup("<small>To change the theme, please select your preference from <b>below</b></small>")
		theme_label.show()
		dialog.vbox.pack_start(theme_label, False, False, 0)

		scroll = gtk.ScrolledWindow()
		scroll.set_size_request(400, 180)
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		tab = gtk.Table(1, 8, True)
		tab.set_col_spacings(10)
		scroll.add_with_viewport(tab)
		tab.show()

		dirList = custom_listdir(cmcThemeSmall)
		count = 0
		for x in dirList:
			count+=1

			event = "event%s" % (count)
			image = "image%s" % (count)

			tooltips = gtk.Tooltips()
			event = gtk.EventBox()
			image = gtk.Image()
			path = "%s/%s" % (cmcThemeSmall, x)
			image.set_from_file(path)
			event.connect("button_press_event", ThemeClicked, x)
			tooltips.set_tip(event, x)
			event.add(image)
			tab.attach(event, count-1, count, 0, 1)
			image.show()
			event.show()

		b = read_parser("branch")
		d = read_parser("device")
		r = read_parser("repo_path")
		if r == "Default":
			r = default_repo_path
		settings_info = gtk.Label()
		settings_info.set_alignment(0, 0)
		settings_info.set_markup("<small><small>Device: <b>%s</b>\nBranch: <b>%s</b>.\nRepo path: <b>%s</b></small></small>" % (d,b,r))
		settings_info.show()
		dialog.vbox.pack_start(settings_info, False, False, 10)

		dialog.run()
		dialog.destroy()
######################################################################

######################################################################
# Downloads
#---------------------------------------------------------------------
class DownloadLabelThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		global dlt
		
		while not ct.stopthread.isSet() :
			gtk.threads_enter()
			f = "%s/Downloads/%s" % (u_home, file_name)
			if os.path.exists(f):
				statinfo = os.stat(f)
				delta = statinfo.st_size / 1024
				fs = file_size / 1024
				t = "Downloading MB: %s / %s" % (delta / 1024, fs / 1024)
			else:
				t = "Downloading..."
			menu_items.set_label(t)
			gtk.threads_leave()
			
			time.sleep(0.1)

		if ct.stopthread.isSet() :
			menu_items.set_label("Complete!")
			sendNoti("Compiling Complete", "Your cyanogenmod build has finished", cmcIcon)
			
	def stop(self):
		self.stopthread.set()

class DownloadThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			t = "%s/Downloads/%s" % (u_home, file_name)
			urllib.urlretrieve(url, t)
			menu_items1.set_sensitive(True)
			menu_items2.set_sensitive(True)
			ind.set_icon(cmcIntD)
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

class DownloadClass():

	def main_quit(self):
		global dlt
		global dt
		ul._Thread__stop()
		ct._Thread__stop()
		gtk.main_quit()

	def main(self):
		os.chdir("/tmp")
		url = sys.argv[1]
		file_name = url.split('/')[-1]
		sendNoti("Downloading Cyanogenmod", "Your cyanogenmod download is started\n\n%s" % file_name, cmcIcon,)
		u = urllib2.urlopen(url)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		if os.path.exists(file_name):
			os.remove(file_name)
		ind = appindicator.Indicator("cmcompiler-applicator", cmcInt, appindicator.CATEGORY_APPLICATION_STATUS)
		ind.set_status(appindicator.STATUS_ACTIVE)

		menu = gtk.Menu()

		menu_items = gtk.MenuItem()
		menu_items.set_label("Downloading...")
		menu_items.set_sensitive(False)
		menu_items.show()

		menu_items2 = gtk.MenuItem("Open")
		menu_items2.set_sensitive(False)
		menu_items2.connect("activate", openFolder)
		menu_items2.show()

		menu_items1 = gtk.MenuItem("Quit")
		menu_items1.set_sensitive(True)
		menu_items1.connect("activate" ,  main_quit)
		menu_items1.show()

		submenu = gtk.Menu()

		subitem = gtk.MenuItem("Filename")
		subitem.set_submenu(submenu)
		subitem.show()

		subFile = gtk.MenuItem(file_name)
		subFile.show()
		submenu.append(subFile)

		menu.append(menu_items)
		menu.append(subitem)
		menu.append(menu_items2)
		menu.append(menu_items1)

		ind.set_menu(menu)

		dlt = DownloadLabelThread()
		dt = DownloadThread()
		dlt.start()
		dt.start()

		gtk.main()
#---------------------------------------------------------------------

######################################################################
# About
#---------------------------------------------------------------------
class About():
 
	# About cmc dialog
	def main(self):
    		dialog = gtk.AboutDialog()
    		dialog.set_name("CMC")
		dialog.set_version("0.4 Beta")
		dialog.set_comments("The cyanogenmod compiler was written, not to dismiss the need to learn the android system, but to release the need consistly remember menial tasks.\n\nPlease intend to learn the system, contribute back to any upstream.\n\nHappy compiling,\n\nJeremie Long")
		dialog.set_copyright("CMC - 2012")
		dialog.set_website_label("Donate")
		dialog.set_website(donateUrl)
		MainAppWindow.hide()
   		dialog.run()
    		dialog.destroy()
		MainAppWindow.show()
#---------------------------------------------------------------------

######################################################################
# Download dialog
#---------------------------------------------------------------------
class DownloadDialog():

	def main(self):

		repo_path = read_parser("repo_path")
		repo_branch = read_parser("branch")
		build_device = read_parser("device")

		def get_download_urls(device, version):
			RURL = "http://download.cyanogenmod.com"
			URL = "http://download.cyanogenmod.com/?device=%s&type=%s" % (device, version)
			htmlpage = urllib2.urlopen(URL).read()
			alllinks = re.findall('<a href=\".*?\">.*?zip</a>',htmlpage)

			count=1
			global mylist
			for links in alllinks:
				x = "%s%s" % (RURL, links)
				x = x.split("\"")
				x = x[1]
				y = x.split("/")

				if y[2] == "artifacts":
					y = y[6]
				elif y[2] == "RC":
					y = y[3]
				else:
					y = y[4]

				s = "%s%s" % (RURL, x)
				mylist.append(s)

				if count == 10:
					break
				else:
					count += 1

			return

		def downloadList(obj):
			def callback_url(widget, data=None):
				print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
				global dl_url
				dl_url = data

			dl_list.hide()
			device_scroll.hide()
			version_tbl.hide()

			table3 = gtk.Table(5, 1, False)
			table3.set_row_spacings(15)
			table3.set_col_spacings(15)
			table3.show()
			dialog.vbox.pack_start(table3, True, True, 0)

			url = gtk.RadioButton(None, None)

			button_count = 0
			get_download_urls(dl_device, dl_version)
			for lines in mylist:

				button_count += 1
				button = "button%s" % (button_count)
				x = lines.split("/")
				x = x[-1]

				button = gtk.RadioButton(group=url, label="%s" % (x))
				button.connect("toggled", callback_url, "%s" % (lines))
				table3.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK, xpadding=50, ypadding=7)
				button.show()

		def callback_device(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			global dl_device
			dl_device = data
			print dl_device
			print dl_version
			if not dl_version == None and not dl_device == None:
				dl_list.show()
		

		def callback_version(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			global dl_version
			dl_version = data
			print dl_version
			print dl_device
			if not dl_version == None and not dl_device == None:
				dl_list.show()

		dialog = gtk.Dialog("Download Cyanogenmod", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_resizable(False)

		device_scroll = gtk.ScrolledWindow()
		device_scroll.set_border_width(10)
		device_scroll.set_size_request(200, 180)
		device_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		device_scroll.show()
		dialog.vbox.pack_start(device_scroll, True, True, 0)

		try:
			filehandle = urllib2.urlopen("http://download.cyanogenmod.com").read()
			alldevices = re.findall('.*?navigate_device.*?</a></li>', filehandle)
		except IOError:
			alldevices = None
			custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")
			exit()

		count = 0
		for lines in alldevices:
			count += 1

		device_tbl = gtk.Table(count, 1, False)
		device_tbl.set_row_spacings(5)

		device_scroll.add_with_viewport(device_tbl)
		device_tbl.show()

		device = gtk.RadioButton(None, None)

		button_count = 0
		for lines in alldevices:
			button_count += 1
			if "device_all" in lines:
				button_count = 0
			else:

				button_count += 1
				button = "button%s" % (button_count)

				s = lines.split(">")
				s = s[2]
				s = s.split("<")
				s = s[0]

				button = gtk.RadioButton(group=device, label="%s" % (s))
				button.connect("toggled", callback_device, "%s" % (s))
				device_tbl.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

		version_tbl = gtk.Table(1, 4, False)
		version_tbl.set_row_spacings(15)
		version_tbl.set_row_spacings(15)
		version_tbl.show()
		dialog.vbox.pack_start(version_tbl, True, True, 0)

		version = gtk.RadioButton(None, None)

		button_count = 0
		for lines in list(["all", "nightly", "RC", "stable"]):

			button_count += 1
			button = "button%s" % (button_count)

			button = gtk.RadioButton(group=version, label="%s" % (lines))
			if lines == "all":
				button.connect("toggled", callback_version, "")
			else:
				button.connect("toggled", callback_version, "%s" % (lines))
			version_tbl.attach(button, button_count-1, button_count, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

		dl_list = gtk.Button("Download List")
		dl_list.set_size_request(140, 28)
		dl_list.connect("clicked", downloadList)
		dl_list.hide()
		dialog.vbox.pack_start(dl_list, True, True, 15)

		dialog.run()
		dialog.destroy()
		if not dl_url == None:
			cmd = "python download.py %s &" % (dl_url)
			os.system(cmd)
		else:
			custom_dialog(gtk.MESSAGE_WARNING, "No Download Choosen", "You didn't select a download, can't download anything for you!")
#---------------------------------------------------------------------

######################################################################
# Main
#---------------------------------------------------------------------
class cmcStartClass():

	def call_setup(self, obj):
		Setup().main()

	def call_about(self, obj):
		About().main()

	def syncClicked(self, obj):
		repo_sync_go()

	def buildClicked(self, obj):
		repo_build_go()

	def downloadClicked(self, obj):
		DownloadDialog().main()

	def startWalkthrough(self, obj):
		WalkThroughThread().start()
 
	def main_quit(self, obj):
		gtk.main_quit()
		exit()
 
	# Main program
	def main(self):

		InstallingPackages().main()

		x = which("repo")
		if x == None:
			install_repo()

		if not os.path.exists(askConfirm):
			get_askConfirm()

		if not os.path.exists(gitconfig):
			set_git_Text()

   		def menuItem(parent, imageNam, num):
       			num = gtk.HBox(False, 0)
       			num.set_border_width(2)
       			image = gtk.Image()
       			image.set_from_file(imageNam)
      			num.pack_start(image, False, False, 3)
      			image.show()
       			return num

		def imageClicked(widget, event):
 	  		webbrowser.open_new_tab(cmcUrl)

		tooltips = gtk.Tooltips()

		MainAppWindow.set_title("CMC")
		MainAppWindow.set_icon(placeIcon)
		MainAppWindow.set_position(gtk.WIN_POS_CENTER)
		MainAppWindow.set_resizable(False)

		vbox = gtk.VBox(False, 0)
		hbox = gtk.HBox(True, 3)
		h1box = gtk.HBox(True, 3)

		menu_bar_file = gtk.Menu()

		menu_setup = gtk.MenuItem("Setup")
		menu_bar_file.append(menu_setup)
		menu_setup.connect("activate", self.call_setup)
		menu_setup.show()

		menu_dl = gtk.MenuItem("Download")
		menu_bar_file.append(menu_dl)
		menu_dl.connect("activate", self.downloadClicked)
		menu_dl.show()

		menu_close = gtk.MenuItem("Close")
		menu_bar_file.append(menu_close)
		menu_close.connect("activate",  self.main_quit)
		menu_close.show()

		file_menu = gtk.MenuItem("File")
		file_menu.set_submenu(menu_bar_file)

		menu_bar_help = gtk.Menu()

		help_menu = gtk.MenuItem("Help")
		help_menu.set_submenu(menu_bar_help)

		menu_walk = gtk.MenuItem("Walkthrough")
		menu_bar_help.append(menu_walk)
		menu_walk.connect("activate", self.startWalkthrough)
		menu_walk.show()

		menu_about = gtk.MenuItem("About")
		menu_bar_help.append(menu_about)
		menu_about.connect("activate", self.call_about)
		menu_about.show()

		menu_bar = gtk.MenuBar()
		vbox.pack_start(menu_bar, False, False, 0)
		menu_bar.show()

		menu_bar.append(file_menu)
		menu_bar.append(help_menu)

     		valign = gtk.Alignment(0, 1, 0, 0)
        	vbox.pack_start(valign)

		event = gtk.EventBox()
		image = gtk.Image()
		t = read_parser("theme")
		if t == "Default":
			image.set_from_file(cmcMainImage)
		else:
			themePath = "%s%s" % (cmcTheme, t)
			image.set_from_file(themePath)
		event.set_size_request(260, 358)
		event.connect("button_press_event", imageClicked)
		tooltips.set_tip(event, "Go to XDA thread!")
		event.add(image)

        	compile_btn = gtk.Button("Compile")
		compile_btn.connect("clicked", self.buildClicked)

        	sync_btn = gtk.Button("Sync")
		sync_btn.connect("clicked", self.syncClicked)

		vbox.add(event)
		h1box.add(compile_btn)
		h1box.add(sync_btn)

        	h1align = gtk.Alignment(.50, 0, .75, 0)
        	h1align.add(h1box)
		vbox.pack_start(h1align, False, False, 5)

		author_lab = gtk.Label()
		author_lab.set_markup("<small><small>Built by <b><i>lithid</i></b> open and free!</small></small>")
		vbox.pack_start(author_lab, False, False, 2)

        	MainAppWindow.add(vbox)

		image.show()
		event.show()
        	MainAppWindow.connect('destroy', self.main_quit)
		GlobalProgressWindow.hide()
       		MainAppWindow.show_all()
 
		gtk.main()
 
if __name__ == '__main__':

#	chk_config()

#	try:
#		pro = sys.argv[1]
#	except:
#		pro = "Default"

#	if pro == "-c" or pro == "--compiling":
#		print "Compiling happily"
#	elif pro == "-s" or pro == "--syncing":
#		print "Syncing happily"
#	elif pro == "-d" or pro == "--download":
#		DownloadDialog().main()
#	else:
	cmcStartClass().main()
#---------------------------------------------------------------------

