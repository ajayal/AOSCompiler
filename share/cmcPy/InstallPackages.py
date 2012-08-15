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
import sys
import platform
import commands

from Globals import Globals
from Utils import Utils
#from Parser import Parser
#from Update import Update

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

def getLinux(arg):
	# ('Ubuntu', '12.04', 'precise')
	plat_list = platform.dist()
	if arg == "Distro":
		return plat_list[0]
	elif arg == "Version":
		return plat_list[1]
	elif arg == "Name":
		return plat_list[2]
	else:
		return None 

class InstallPackages():
	def repo(self):
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command("bash")
		Globals.TERM.feed_child("clear\n")
		Globals.TERM.feed_child("curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > repo\n")
		Globals.TERM.feed_child("chmod a+x repo\n")
		Globals.TERM.feed_child("gksudo mv repo /usr/local/bin/repo\n")
		

	def Ubuntu(self, version):

		L = []

		if version == "12.10":
			pak = "libwxgtk2.8-dev"
		else:
			pak = "libwxgtk2.6-dev"
		P = ["git-core", "gnupg", "flex", "bison", "gperf", "libsdl1.2-dev", "libesd0-dev", "squashfs-tools", "build-essential", "zip", "curl", "libncurses5-dev", "zlib1g-dev", "openjdk-6-jdk", "pngcrush", "libxml2-utils", "schedtool", "xsltproc", pak]
		for x in P:
			i = chkInstalled(x)
			if i == False:
				L.extend([x])

		check = (sys.maxsize > 2**32)
		if check is True:
			if version == "10.04":
				P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline5-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
				for x in P:
					i = chkInstalled(x)
					if i == False:
						L.extend([x])
			elif version == "11.04":
				P = ["g++-multilib" "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev", "gcc-4.3-multilib", "g++-4.3-multilib"]
				for x in P:
					i = chkInstalled(x)
					if i == False:
						L.extend([x])
			elif version == "12.10" or version == "12.04" or version == "11.10":
				P = ["g++-multilib", "lib32z1-dev", "lib32ncurses5-dev", "lib32readline-gplv2-dev"]
				for x in P:
					i = chkInstalled(x)
					if i == False:
						L.extend([x])
		print len(L)
		if len(L) == 0:
			Utils().CDial(gtk.MESSAGE_INFO, "Empty package list", "You already have the packages you need installed!")
		else:
			packages = ",".join(L).replace(",", " ")
			q = Utils().QDial("Are you sure??", "We are going to install this list of packages\n\n%s\n\n Are you sure we should proceed?" % packages)
			if q == True:
				Globals.TERM.set_background_saturation(0.3)
				Globals.TERM.fork_command("bash")
				Globals.TERM.feed_child("clear\n")
				Globals.TERM.feed_child("gksudo \"apt-get install -y %s\"\n" % packages)
			else:
				return

	def runInstall(self):
		D = getLinux("Distro")
		if D == "Ubuntu":
			V = getLinux("Version")
			InstallPackages().Ubuntu(V)
		else:
			Utils().CDial(gtk.MESSAGE_WARNING, "Linux Distro", "Sorry, we couldn't detect your linux distro. File a bug report with this info:\n\n<b>Distro: </b>%s\n<b>Version: </b>%s\n<b>Name: </b>%s\n" % (plat_d, plat_v, plat_n))

