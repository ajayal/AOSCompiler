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
