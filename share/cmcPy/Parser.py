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

from Globals import Globals
import ConfigParser

class Parser():

	def read(self, arg):
		title = "Cmc"
		default = "Default"
		try:
			config = ConfigParser.RawConfigParser()
			config.read(Globals.myCONF)
			c = config.get(title, arg)
		except ConfigParser.NoSectionError:
			c = "%s" % (default)

		return c

	def write(self, arg, value):
		title = "Cmc"
		default = "Default"
		try:
			config = ConfigParser.RawConfigParser()
			config.read(Globals.myCONF)
			getDevice = config.get(title, 'device')
			getBranch = config.get(title, 'branch')
			getRepoPath = config.get(title, 'repo_path')
			getSyncJobs = config.get(title, 'sync_jobs')
			getMakeJobs = config.get(title, 'make_jobs')
			getManuf = config.get(title, 'manuf')
			getBackColor = config.get(title, 'background_color')
			getTextColor = config.get(title, 'text_color')

		except ConfigParser.NoSectionError:
			getDevice = None
			getBranch = None
			getRepoPath = None
			getSyncJobs = None
			getMakeJobs = None
			getManuf = None
			getBackColor = None
			getTextColor = None

		config = ConfigParser.RawConfigParser()
		config.add_section(title)

		if arg == "device":
			config.set(title, 'device', value)
		elif getDevice:
			config.set(title, 'device', getDevice)
		else:
			config.set(title, 'device', default)

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
			config.set(title, 'repo_path', Globals.myDEF_REPO_PATH)
		
		if arg == "sync_jobs":
			config.set(title, 'sync_jobs', value)
		elif getSyncJobs:
			config.set(title, 'sync_jobs', getSyncJobs)
		else:
			config.set(title, 'sync_jobs', "4")
		
		if arg == "make_jobs":
			config.set(title, 'make_jobs', value)
		elif getMakeJobs:
			config.set(title, 'make_jobs', getMakeJobs)
		else:
			config.set(title, 'make_jobs', Globals.numprocs)
		
		if arg == "manuf":
			config.set(title, 'manuf', value)
		elif getManuf:
			config.set(title, 'manuf', getManuf)
		else:
			config.set(title, 'manuf', default)

		if arg == "background_color":
			config.set(title, 'background_color', value)
		elif getManuf:
			config.set(title, 'background_color', getBackColor)
		else:
			config.set(title, 'background_color', '#000')

		if arg == "text_color":
			config.set(title, 'text_color', value)
		elif getManuf:
			config.set(title, 'text_color', getTextColor)
		else:
			config.set(title, 'text_color', '#3294ae')

		with open(Globals.myCONF, 'wb') as configfile:
    			config.write(configfile)
    			
