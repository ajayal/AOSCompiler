#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

import pygtk
pygtk.require('2.0')
import threading
import random, time, datetime
import gtk
import gobject
import appindicator
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

# Path variables
u_home = os.environ['HOME']
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

# URL
cmcUrl = "http://forum.xda-developers.com/showthread.php?t=1415661"
donateUrl = "http://forum.xda-developers.com/donatetome.php?u=2709018"
urlCmIcs = "https://raw.github.com/CyanogenMod/android_vendor_cm/ics/vendorsetup.sh"
urlCmGb = "https://raw.github.com/CyanogenMod/android_vendor_cyanogen/gingerbread/vendorsetup.sh"
cmGit = "https://github.com/CyanogenMod/android.git"
repoToolUrl = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"

# Config file definitions
configDeviceName = "config_device_name:"
configCustomRepoPath = "config_custom_repo_path:"
configBranch = "config_branch:"

placeIcon = gtk.gdk.pixbuf_new_from_file(cmcIcon)

