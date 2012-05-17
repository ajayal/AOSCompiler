#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

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
