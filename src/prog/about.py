#!/usr/bin/env python
from helper import *

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
   		dialog.run()
    		dialog.destroy()
 
if __name__ == '__main__':
	go = About()
	go.main()
