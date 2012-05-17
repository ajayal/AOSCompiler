#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

from helper import *

repo_path = read_parser("repo_path")
if repo_path == "Default":
	repo_path = default_repo_path
repo_branch = read_parser("branch")
build_device = read_parser("device")

gtk.threads_init()


class UpdateLabel(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		global ct
		
		while not ct.stopthread.isSet() :
			gtk.threads_enter()
			finish = datetime.datetime.now()
			delta = finish - start
			t = "Compiling %s" % (delta)
			menu_items.set_label(t)
			gtk.threads_leave()
			
			time.sleep(0.1)

		if ct.stopthread.isSet() :
			a = "%s/NeedSync" % (configdir)
			b = "%s/NoDevice" % (configdir)
			c = "%s/NoAdbRunning" % (configdir)
			d = "%s/ExtractFiles" % (configdir)
			e = "%s/build.failed" % (configdir)
			f = "%s/NeedRepoScript" % (configdir)
			g = "%s/NoDeviceC" % (configdir)
			h= "%s/GenError" % (configdir)

			if os.path.exists(a):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Error: Need to sync first!")
			elif os.path.exists(b):
				ind.set_icon(cmcIntE)
				b = read_parser("device")
				d = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
				menu_items.set_label("Error: %s not found:\nReturned:\n%s" % (b, d))
			elif os.path.exists(c):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Error: Adb isn't running")
			elif os.path.exists(d):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Error: Extract-files came back False")
			elif os.path.exists(e):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Error: Compile error please check")
			elif os.path.exists(f):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Repo Script needs setup")
			elif os.path.exists(g):
				ind.set_icon(cmcIntE)
				menu_items.set_label("No device configured!")
			elif os.path.exists(h):
				ind.set_icon(cmcIntE)
				menu_items.set_label("General sync error. Run in terminal")
			else:
				menu_items.set_label("Complete!")
				sendNoti("Compiling Complete", "Your cyanogenmod build has finished", cmcIcon)
			
	def stop(self):
		self.stopthread.set()

class CompileThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			repo_build_go()
			menu_items1.set_sensitive(True)
			menu_items2.set_sensitive(True)
			ind.set_icon(cmcIntD)
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

def main_quit(obj):
	global ct
	global ul
	cmd = "/usr/share/cmcompiler/prog/scripts/kill-cm.sh build"
	os.system(cmd)
	ct._Thread__stop()
	ul._Thread__stop()
	sys.exit()

def openFolder(obj):
	t = "%s/out/target/product/%s" % (repo_path, build_device)
	cmd = "nautilus %s" % (t)
	os.system(cmd)
	sys.exit()

# Compile dialog
def repo_build_go():
	def build_gb():
		e = "%s/NoAdbRunning" % (configdir)
		if os.path.exists(e):
			os.remove(e)
		CHECKS = 0
		build_manu = getManu(build_device, "gb")
		d = "%s/.repo" % (repo_path)
		if not os.path.exists(d):
			CHECKS+=1
			e = "%s/NeedSync" % (configdir)
			file(e, 'w').close()

		if CHECKS == 0:
			e = "%s/NoDevice" % (configdir)
			if os.path.exists(e):
				os.remove(e)
			d = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
			if not os.path.exists(d):
				e = "%s/NoDevice" % (configdir)
				file(e, 'w').close()

			if CHECKS == 0:
				e = "%s/NoAdbRunning" % (configdir)
				if os.path.exists(e):
					os.remove(e)
				d = "%s/vendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
				if not os.path.exists(d):
					c = checkAdb()
					if c == False:
						CHECKS+=1
						e = "%s/NoAdbRunning" % (configdir)
						file(e, 'w').close()

				if CHECKS == 0:
					e = "%s/ExtractFiles" % (configdir)
					if os.path.exists(e):
						os.remove(e)
					c = extractFiles(repo_path, build_manu, build_device)
					if c == False:
						CHECKS+=1
						e = "%s/ExtractFiles" % (configdir)
						file(e, 'w').close()

					if CHECKS == 0:
						os.chdir(repo_path)
						cacheran = "%s/cacheran" % configdir
						if not os.path.exists(cacheran):
							cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
							os.system(cmd)
							file(cacheran, 'w').close()
						cmd = "/bin/bash %s/vendor/cyanogen/get-rommanager" % (repo_path)
						os.system(cmd)
						cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
						os.system(cmd)

	def build_ics():
		e = "%s/NeedSync" % (configdir)
		if os.path.exists(e):
			os.remove(e)
		CHECKS = 0
		build_manu = getManu(build_device, "ics")

		d = "%s/.repo" % (repo_path)
		print d
		if not os.path.exists(d):
			CHECKS+=1
			e = "%s/NeedSync" % (configdir)
			file(e, 'w').close()

		if CHECKS == 0:
			e = "%s/NoDevice" % (configdir)
			if os.path.exists(e):
				os.remove(e)
			d = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
			if not os.path.exists(d):
				os.chdir(repo_path)
				cmd = "python build/tools/roomservice.py cm_" + build_device
				os.system(cmd)
				time.sleep(2)
				build_manu = getManu(build_device)
				nd = "%s/device/%s/%s" % (repo_path, build_manu, build_device)
				if not os.path.exists(nd):
					CHECKS+=1
					e = "%s/NoDevice" % (configdir)
					file(e, 'w').close()

			if CHECKS == 0:
				print "Here now"
				e = "%s/NoAdbRunning" % (configdir)
				if os.path.exists(e):
					os.remove(e)
				d = "%s/vendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
				print d
				if not os.path.exists(d):
					c = checkAdb()
					print c
					if not c == True:
						CHECKS+=1
						e = "%s/NoAdbRunning" % (configdir)
						file(e, 'w').close()

				if CHECKS == 0:
					e = "%s/ExtractFiles" % (configdir)
					if os.path.exists(e):
						os.system(e)
					c = extractFiles(repo_path, build_manu, build_device)
					if not c == True:
						CHECKS+=1
						e = "%s/ExtractFiles" % (configdir)
						file(e, 'w').close()

					if CHECKS == 0:
						os.chdir(repo_path)
						cacheran = "%s/cacheran" % configdir
						if not os.path.exists(cacheran):
							cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
							os.system(cmd)
							file(cacheran, 'w').close()
						cmd = "/bin/bash %s/vendor/cm/get-prebuilts" % (repo_path)
						os.system(cmd)
						cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
						os.system(cmd)

	def start_build():
		chk_repo = common_chk()
		if chk_repo == 1:
			if repo_branch == "ics":
				build_ics()
			elif repo_branch == "gingerbread":
				build_gb()
			else:	
				print "Default"

		elif chk_repo == 0:
			r = "%s/NeedRepoScript" % (configdir)
			file(r, 'w').close()

		elif chk_repo == 2:
			d = "%s/NoDeviceC" % (configdir)
			file(d, 'w').close()

		else:
			g = "%s/GenError" % (configdir)
			file(g, 'w').close()

	start_build()

if __name__ == "__main__":
	sendNoti("Compiling Cyanogenmod", "Your cyanogenmod build is starting", cmcIcon)
	ind = appindicator.Indicator("cmcompiler-compile-indicator", cmcInt, appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status(appindicator.STATUS_ACTIVE)
	ind.set_attention_icon(cmcInt)

	# create a menu
	menu = gtk.Menu()

	menu_items = gtk.MenuItem()
	menu_items.set_label("Compiling...")
	menu_items.set_sensitive(False)
	menu.append(menu_items)
	menu_items.show()

	menu_items2 = gtk.MenuItem("Open")
	menu_items2.set_sensitive(False)
	menu.append(menu_items2)
	menu_items2.connect("activate", openFolder)
	menu_items2.show()

	menu_items1 = gtk.MenuItem("Quit")
	menu_items1.set_sensitive(True)
	menu.append(menu_items1)
	menu_items1.connect("activate" ,  main_quit)
	menu_items1.show()

	ind.set_menu(menu)

	start = datetime.datetime.now()
	ul = UpdateLabel()
	ct = CompileThread()
	ul.start()
	ct.start()

	gtk.main()

