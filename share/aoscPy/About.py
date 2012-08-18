#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

from Globals import Globals

######################################################################
# About
######################################################################
class About():

        def main(self):
                dialog = gtk.AboutDialog()
                dialog.set_name("CMC")
                dialog.set_version("0.5 Beta")
                dialog.set_comments(Globals.about_info)
                dialog.set_copyright("CMC - 2012")
                dialog.set_website_label("Donate")
                dialog.set_website(Globals.myDONATE)
                dialog.run()
                dialog.destroy()
