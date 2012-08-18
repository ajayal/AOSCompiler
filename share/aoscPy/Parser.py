#!/usr/bin/env python

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
			getRomDist = config.get(title, 'rom_dist')
			getRomAbrv = config.get(title, 'rom_abrv')
			getDevice = config.get(title, 'device')
			getBranch = config.get(title, 'branch')
			getRepoPath = config.get(title, 'repo_path')
			getSyncJobs = config.get(title, 'sync_jobs')
			getMakeJobs = config.get(title, 'make_jobs')
			getManuf = config.get(title, 'manuf')

		except ConfigParser.NoSectionError:
			getRomDist = None
			getRomAbrv = None
			getDevice = None
			getBranch = None
			getRepoPath = None
			getSyncJobs = None
			getMakeJobs = None
			getManuf = None

		config = ConfigParser.RawConfigParser()
		config.add_section(title)

		if arg == "rom_dist":
			config.set(title, 'rom_dist', value)
		elif getRomDist:
			config.set(title, 'rom_dist', getRomDist)
		else:
			config.set(title, 'rom_dist', default)

		if arg == "rom_abrv":
			config.set(title, 'rom_abrv', value)
		elif getRomAbrv:
			config.set(title, 'rom_abrv', getRomAbrv)
		else:
			config.set(title, 'rom_abrv', default)

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

		with open(Globals.myCONF, 'wb') as configfile:
    			config.write(configfile)
    			
