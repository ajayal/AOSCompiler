#!/usr/bin/env python

import gtk
import os

from Globals import Globals
from Parser import Parser
from Utils import Utils

class Sync():
	def run(self):
		repo = Utils().which("repo")
		if repo == None:
			Utils().CDial(gtk.MESSAGE_INFO, "Repo is not installed", "You need to install repo to continue.")
			main_cmc_cmd()
			return
		r = Parser().read("repo_path")
		url = Utils().getBranchUrl("init")
		b = Parser().read("branch")
		j = Parser().read("sync_jobs")
		if not os.path.exists(r):
			os.mkdir(r)
		Globals.TERM.feed_child("cd %s\n" % r)
		if not os.path.exists("%s/.repo" % r):
			Globals.TERM.feed_child("repo init -u %s -b %s\n" % (url, b))
			Utils().CDial(gtk.MESSAGE_INFO, "Running repo init!", "You needed to init the repo, doing that now.")
		Globals.TERM.feed_child("repo sync -j%s\n" % j)
		Globals.TERM.feed_child("echo \"Complete!!!\"\n")

