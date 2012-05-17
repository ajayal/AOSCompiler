#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

from helper import *

gtk.threads_init()

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

class UpdateThread(threading.Thread):
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

class InstallThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			#time.sleep(15)
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
		global ut
		ut.stop()
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
		print check
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

if __name__ == "__main__":

	packages = chkInstalledPackages().main()

    	def quit(self):
		global it
		it._Thread__stop()
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

		it = InstallThread()
		ut = UpdateThread()
		it.start()
		ut.start()

		window.show()
		gtk.main()
	else:
		print "Move along, nothing really going on that concerns you!"

