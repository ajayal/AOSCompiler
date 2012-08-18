#!/usr/bin/env python

import gtk
from Globals import Globals
from Parser import Parser
import urllib

class Update():
	def TEXT(self):
		b = Parser().read("branch")
		d = Parser().read("device")
		p = Parser().read("repo_path")
		r = Parser().read("rom_dist")
		a = Parser().read("rom_abrv")
		Globals.branchLab.set_markup("<small>Branch: <b>%s</b></small>" % b)
		Globals.LinkContact.set_markup("<small>Contact</small>")
		Globals.runLab.set_markup("<small>Run</small>")
		Globals.romLab.set_markup("<small>Rom: <b>%s</b></small>" % a)
		Globals.aboutRomLab.set_markup("<small>About rom</small>")
		Globals.toolsLab.set_markup("<small>Options</small>")
		Globals.deviceLab.set_markup("<small>Device: <b>%s</b></small>" % d)
		Globals.aoscTitleLab.set_markup("<span font=\"18\">%s</span>" % r)
		Globals.syncjobsLab.set_markup("<small>Sync jobs</small>")
		Globals.makeLab.set_markup("<small>Make jobs</small>")
		Globals.compileLab.set_markup("<small>Compile</small>")
		Globals.runFrameLab.set_markup("<small>Run options</small>")
		Globals.buildFrameLab.set_markup("<small>Build options</small>")
		Globals.syncLab.set_markup("<small>Sync</small>")
		Globals.clobberLab.set_markup("<small>Clobber</small>")
		Globals.build_appLab.set_markup("<small><small>Build specific <b>app/binary</b> here. :: <b>enter</b> ::</small></small>")
		Globals.KEY_BIND_INFO.set_markup("<small><small>[CTL-L + (<b>v</b> = View config, <b>a</b> = Start adb, <b>m</b> = Main start/stop, <b>s</b> = Sync, <b>b</b> = build/compile, <b>r</b> = Repo path) <b>esc</b> = Quit]</small></small>")
		Globals.MAIN_INFO.set_markup("<small>Repo path: <b>%s</b></small>" % p)

