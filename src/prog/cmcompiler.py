#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

from helper import *

from chkPackages import chkInstalledPackages

gtk.threads_init()

def call_setup(obj):
	from setup import Setup
	Setup().main()

def call_about(obj):
	from about import About
	About().main()

class AppMainThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet():
			gtk.threads_enter()
			cmcStartClass().main()
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

class WalkThroughThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet():
			gtk.threads_enter()
			from walkthrough import WalkThroughThread
			WalkThroughThread().start()
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

class cmcStartClass():

	def syncClicked(self, obj):
		cmd = "/usr/bin/cmcompiler --sync &"
		os.system(cmd)
		gtk.main_quit()

	def buildClicked(self, obj):
		cmd = "/usr/bin/cmcompiler --compile &"
		os.system(cmd)
		gtk.main_quit()

	def downloadClicked(self, obj):
		from dl_dialog import DownloadDialog
		DownloadDialog().main()

	def startWalkthrough(self, obj):
		WalkThroughThread().start()
 
	def main_quit(self, obj):
		gtk.main_quit()
		exit()
 
	# Main program
	def main(self):

		if not os.path.exists(askConfirm):
			get_askConfirm()

		if not os.path.exists(gitconfig):
			set_git_Text()

		cmd = "python /usr/share/cmcompiler/prog/chkPackages.py"
		i = os.system(cmd)
		if i == 256:
			exit()

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

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("CMC")
		window.set_icon(placeIcon)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)

		vbox = gtk.VBox(False, 0)
		hbox = gtk.HBox(True, 3)
		h1box = gtk.HBox(True, 3)

		menu_bar_file = gtk.Menu()

		menu_setup = gtk.MenuItem("Setup")
		menu_bar_file.append(menu_setup)
		menu_setup.connect("activate", call_setup)
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
		menu_about.connect("activate", call_about)
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
		vbox.pack_start(h1align, False, False, 10)

		author_lab = gtk.Label()
		author_lab.set_markup("<small><small>Built by <b><i>lithid</i></b> open and free!</small></small>")
		vbox.pack_start(author_lab, False, False, 2)

        	window.add(vbox)

		image.show()
		event.show()
        	window.connect('destroy', self.main_quit)
       		window.show_all()
 
		gtk.main()
 
if __name__ == '__main__':

	chk_config()

	try:
		pro = sys.argv[1]
	except:
		pro = "Default"

	if pro == "-c" or pro == "--compiling":
		print "Compiling happily"
	elif pro == "-s" or pro == "--syncing":
		print "Syncing happily"
	elif pro == "-d" or pro == "--download":
		from dl_dialog import DownloadDialog
		DownloadDialog().main()
	else:
		AppMainThread().start()


