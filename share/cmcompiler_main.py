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

######################################################################
# Python imports
######################################################################
import pygtk
pygtk.require('2.0')
import gtk
import os
import platform
import sys
import time
import webbrowser
import shutil
import subprocess

from cmcPy.About import About
from cmcPy.Globals import Globals
from cmcPy.Parser import Parser
from cmcPy.Update import Update
from cmcPy.Utils import Utils

######################################################################
# Helper functions
######################################################################

def openBuildFolder():
	r = Parser().read("repo_path")
	d = Parser().read("device")
	t = "%s/out/target/product/%s" % (r, d)
	if os.path.exists(t):
		subprocess.call(('xdg-open', t))
	else:
		Utils().CDial(gtk.MESSAGE_ERROR, "No out folder", "Need to compile before you can do this silly!")

def custom_listdir(path):
	dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
	dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))

	return dirs

def install_repo():
	cmd1 = "curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > %s/repo" % (configdir)
	cmd2 = "chmod a+x %s/repo" % (configdir)
	cmd3 = "gksudo mv %s/repo /usr/local/bin/" % (configdir)
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)

def which(program):
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

def chk_config():
	if not os.path.exists(Globals.myCONF_DIR):
		os.makedirs(Globals.myCONF_DIR)

def get_askConfirm():
	def askedClicked():
		if not os.path.exists(Globals.askConfirm):
			file(Globals.askConfirm, 'w').close()

	q = Utils().QDial("**** User Confirmation ****", Globals.ask_confirm_info)
	if q == True:
		askedClicked()
	else:
		exit()

def download_clicked(obj):
	webbrowser.open_new_tab(Globals.myGETCM)

def cm_wiki_clicked(obj):
	webbrowser.open_new_tab(Globals.myCMWIKI)

def aosp_site_clicked(obj):
	webbrowser.open_new_tab(Globals.myAOSP_SITE)

def main_about(obj):
	About().main()

def sync_button_clicked(obj):
	vteterminal("Syncing")

def compile_button_clicked(obj):
	vteterminal("Compiling")

######################################################################
# Some GTK globals
######################################################################
myMAIN_ICON = gtk.gdk.pixbuf_new_from_file(Globals.myICON)

toolsCombo = gtk.combo_box_new_text()
for i in ["Options", "Start adb", "View config", "Repo path", "Remove config", "Run bash", "Add device", "Stop/reset", "Open rom folder"]:
	toolsCombo.append_text("%s" % i)

branchCombo = gtk.combo_box_new_text()
for i in ["gingerbread", "ics", "jellybean"]:
	branchCombo.append_text("%s" % i)

makeCombo = gtk.combo_box_new_text()
for i in range(1,Globals.numprocs+1):
	makeCombo.append_text("%s" % i)

syncCombo = gtk.combo_box_new_text()
for i in range(1,17):
	syncCombo.append_text("%s" % i)

entryBox = gtk.Entry()

######################################################################
# Global Settings
######################################################################
def run_vt_command(event):
	Globals.TERM.set_background_saturation(0.3)
	i = entryBox.get_text()
	r = Parser().read('repo_path')
	d = Parser().read('device')
	os.chdir(r)
	Globals.TERM.fork_command('bash')
	Globals.TERM.feed_child('clear\n')
	Globals.TERM.feed_child('. build/envsetup.sh\n')
	Globals.TERM.feed_child('lunch cm_%s-userdebug\n' % d)
	Globals.TERM.feed_child('make -j%s %s\n' % (Globals.numprocs, i))

def run_local_shell():
	Globals.TERM.set_background_saturation(0.3)
	Globals.TERM.fork_command('bash')

def run_custom_device():
	title = "Setup custom device"
	message = "Please setup your device here:"
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_markup(title)
	dialog.format_secondary_markup(message)
	table = gtk.Table(8, 1, False)
	dialog.vbox.pack_start(table)
	label = gtk.Label()
	label.set_markup("Device name:")
	label.show()
	entry = gtk.Entry()
	entry.show()
	label1 = gtk.Label()
	label1.set_markup("Device manufacturer:")
	label1.show()
	entry1 = gtk.Entry()
	entry1.show()
	label2 = gtk.Label()
	label2.set_markup("Device tree url:")
	label2.show()
	entry2 = gtk.Entry()
	entry2.show()
	label3 = gtk.Label()
	label3.set_markup("Device tree branch:")
	label3.show()
	entry3 = gtk.Entry()
	entry3.show()
	table.attach(label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(entry, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(label1, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(entry1, 0, 1, 3, 4, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(label2, 0, 1, 4, 5, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(entry2, 0, 1, 5, 6, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(label3, 0, 1, 6, 7, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.attach(entry3, 0, 1, 7, 8, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
	table.show()
	q = dialog.run()
	if q == gtk.RESPONSE_OK:
		n = entry.get_text()
		m = entry1.get_text()
		u = entry2.get_text()
		b = entry3.get_text()
		r = Parser().read("repo_path")
		os.chdir(r)
		manu_path = "%s/device/%s" % (r,m)
		if not os.path.exists(manu_path):
			os.mkdir(manu_path)
		if os.path.exists("%s/%s" % (manu_path, n)):
			shutil.rmtree("%s/%s" % (manu_path, n))
		os.chdir(manu_path)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')
		Globals.TERM.feed_child('git clone %s -b %s %s\n' % (u,b,n))
	else:
		Utils().CDial(gtk.MESSAGE_INFO, "Skipping this", "No changes have been made!")
	dialog.destroy()

def get_branch_combo():
	r = Parser().read("branch")
	if r == "gingerbread":
		return 0
	elif r == "ics":
		return 1
	elif r == "jellybean":
		return 2

def tools_combo_change(event):
	value = int(toolsCombo.get_active())
	if value == 1:
		start_adb()
	elif value == 2:
		view_config()
	elif value == 3:
		choose_repo_path()
	elif value == 4:
		remove_config()
	elif value == 5:
		run_local_shell()
	elif value == 6:
		run_custom_device()
	elif value == 7:
		main_cmc_cmd()
	elif value == 8:
		openBuildFolder()
	else:
		pass

	toolsCombo.set_active(0)

def compile_combo_change(event):
	value = str(makeCombo.get_active_text())
	Parser().write("make_jobs", value)

def sync_combo_change(event):
	value = str(syncCombo.get_active_text())
	Parser().write("sync_jobs", value)

def branch_combo_change(event):
	value = str(branchCombo.get_active_text())
	Parser().write("branch", value)
	Parser().write("device", "None")
	Update().TEXT_COLOR()

def device_button(event):
	Update().DEVICES()
	Update().TEXT_COLOR()

def clobber_button(event):
	print "clobbering it now"

def choose_repo_path():
	direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	r = direct.run()
	repo_dir = direct.get_filename()
	direct.destroy()
	if r == gtk.RESPONSE_ACCEPT:
		try:
			Parser().write("repo_path", repo_dir)
			Update().TEXT_COLOR()
		except NameError:
			pass

def remove_config():
	q = Utils().QDial("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
	if q == True:
		os.remove(cmcconfig)
		Utils().CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

def start_adb():
	Globals.TERM.set_background_saturation(0.3)
	Globals.TERM.fork_command(Globals.myA_ADB_START)

def view_config():
	Utils().ViewConfig()

def main_cmc_cmd():
	Globals.TERM.set_background_saturation(1.0)
	Globals.TERM.fork_command('clear')

def compile_or_sync(arg):
	if arg == "Syncing":
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command(Globals.mySYNC_SCRIPT)
	elif arg == "Compiling":
		i = str(Utils().Compile())

		i = i.split("-")
		RUN = i[0]
		PID = i[1]

		if RUN == "ROOM":
			Utils().CDial(gtk.MESSAGE_INFO, "<small>Running roomservice", "Roomservice is running right now, you will have to run, \"<b>Compile</b>\" again after this is done downloading your kernel and device dependancies.</small>")

def hit_event_btn(obj, event, arg):
	print "Pressed event button: %s" % arg

def main_sync_compile_btn(obj, arg):
	compile_or_sync(arg)

######################################################################
# Advanced
######################################################################
class advanced():
 
	def main_quit(self, widget, event=None):
		gtk.main_quit()

	def on_key_press(self, widget, data=None):
		i = gtk.gdk.keyval_name(data.keyval)

		if i == "v" and data.state & gtk.gdk.CONTROL_MASK:
			view_config()
		elif i == "a" and data.state & gtk.gdk.CONTROL_MASK:
			start_adb()
		elif i == "m" and data.state & gtk.gdk.CONTROL_MASK:
			main_cmc_cmd()
		elif i == "s" and data.state & gtk.gdk.CONTROL_MASK:
			compile_or_sync("Syncing")
		elif i == "b" and data.state & gtk.gdk.CONTROL_MASK:
			compile_or_sync("Compiling")
		elif i == "r" and data.state & gtk.gdk.CONTROL_MASK:
			choose_repo_path()
		elif i == "x" and data.state & gtk.gdk.CONTROL_MASK or i == "Escape":
			gtk.main_quit()
		else:
			pass
 
	# Main program
	def main(self):
		Globals.MAIN_WIN.set_title("Cyanogenmod Compiler")
		Globals.MAIN_WIN.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		Globals.MAIN_WIN.set_icon(myMAIN_ICON)
		Globals.MAIN_WIN.connect("delete_event", self.main_quit)
		Globals.MAIN_WIN.connect("key_press_event", self.on_key_press)
		Globals.MAIN_WIN.set_events(gtk.gdk.KEY_PRESS_MASK)
		Globals.MAIN_WIN.set_events(gtk.gdk.CONTROL_MASK)
		color = gtk.gdk.color_parse(Globals.myBackgroundColor)
		Globals.MAIN_WIN.modify_bg(gtk.STATE_NORMAL, color)
		Globals.MAIN_WIN.set_size_request(1080, 638)
		Globals.MAIN_WIN.set_resizable(False)

		MAIN_VBOX = gtk.VBox(False, 0)

		TERM_FRAME = gtk.Frame()
		TERM_FRAME.show()
		Globals.TERM.show()
		TERM_FRAME.add(Globals.TERM)

		table = gtk.Table(1, 3, False)
		table.show()

		Globals.MAIN_INFO.show()

		tableB = gtk.Table(1, 2, False)
		tableB.show()

		toolsCombo.show()
		toolsCombo.set_wrap_width(2)
		toolsCombo.set_active(0)
		toolsCombo.set_size_request(90, 28)
		toolsCombo.connect("changed", tools_combo_change)

		frameB = gtk.Frame()
		frameB.add(tableB)
		frameB.set_label_widget(toolsCombo)
		frameB.set_border_width(1)
		frameB.set_shadow_type(gtk.SHADOW_NONE)
		frameB.show()

		tableEntry = gtk.Table(1, 2, False)
		tableEntry.show()

		Globals.KEY_BIND_INFO.show()

		branchCombo.show()
		i = get_branch_combo()
		branchCombo.set_active(i)
		branchCombo.set_wrap_width(4)
		branchCombo.connect("changed", branch_combo_change)

		Globals.branchLab.show()

		DevImg = gtk.Image()
		DevImg.set_from_file(Globals.DeviceImg)
		Globals.DEV_BTN.set_image(DevImg)
		Globals.DEV_BTN.connect("clicked", device_button)
		Globals.DEV_BTN.show()

		Globals.deviceLab.show()

		syncCombo.show()
		syncCombo.set_active(int(Parser().read("sync_jobs"))-1)
		syncCombo.set_wrap_width(4)
		syncCombo.connect("changed", sync_combo_change)

		Globals.syncjobsLab.show()

		makeCombo.show()
		makeCombo.set_active(int(Parser().read("make_jobs"))-1)
		makeCombo.set_wrap_width(4)
		makeCombo.connect("changed", compile_combo_change)

		Globals.makeLab.show()

		CompImg = gtk.Image()
		CompImg.set_from_file(Globals.CompileImg)
		compile_btn = gtk.Button()
		compile_btn.set_image(CompImg)
		compile_btn.connect("clicked", main_sync_compile_btn, "Compiling")
		compile_btn.show()

		Globals.compileLab.show()

		SyImg = gtk.Image()
		SyImg.set_from_file(Globals.SyncImg)
		sync_btn = gtk.Button()
		sync_btn.set_image(SyImg)
		sync_btn.connect("clicked", main_sync_compile_btn, "Syncing")
		sync_btn.show()

		Globals.syncLab.show()

		entryBox.show()
		entryBox.connect("activate", run_vt_command)

		Globals.build_appLab.show()

		ClobberImg = gtk.Image()
		ClobberImg.set_from_file(Globals.ClobImg)
		Globals.clobberBtn.set_image(ClobberImg)
		Globals.clobberBtn.connect("clicked", clobber_button)
		Globals.clobberBtn.show()

		Globals.clobberLab.show()

		LinksTable = gtk.Table(2, 1, False)
		LinksTable.show()
		LinkFrame = gtk.Frame()
		LinkFrame.set_label_widget(Globals.LinkContact)
		LinkFrame.set_shadow_type(gtk.SHADOW_NONE)
		LinkFrame.set_border_width(5)
		LinkFrame.add(LinksTable)

		count = 0
		LinkList = ["Gmail", "Twitter", "GooglePlus", "Xda", "Youtube", "Gallery"]
		for i in LinkList:
			count+=1
			name = "%s/%s.png" % (Globals.myIMGS, i)
			image = gtk.Image()
			image.set_from_file(name)
			image.show()
			event = gtk.EventBox()
			event.connect("button_press_event", hit_event_btn, i)
			event.add(image)
			event.set_size_request(32, 32)
			event.show()
			tooltip = gtk.Tooltips()
			tooltip.set_tip(event, i)
			LinksTable.attach(event, count-1, count, 0, 1, xpadding=1, ypadding=1, xoptions=gtk.FILL, yoptions=gtk.FILL)

		MAIN_VBOX.pack_start(Globals.MAIN_INFO, False, False, 0)
		MAIN_VBOX.pack_start(Globals.KEY_BIND_INFO, False, False, 0)
		MAIN_VBOX.pack_start(table, True, True, 0)
		MAIN_VBOX.pack_start(frameB, True, True, 0)
		MAIN_VBOX.pack_start(LinkFrame, True, True, 0)

		SpacerRT = gtk.Label()
		SpacerRT .show()
		SpacerLT  = gtk.Label()
		SpacerLT .show()

		SpacerRB = gtk.Label()
		SpacerRB .show()
		SpacerLB  = gtk.Label()
		SpacerLB .show()

		table.attach(TERM_FRAME, 0, 1, 0, 1, xpadding=10, ypadding=10)

		tableB.attach(SpacerRT, 0, 1, 0, 1, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerRB, 0, 1, 1, 2, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(syncCombo, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.syncjobsLab, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(makeCombo, 2, 3, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.makeLab, 2, 3, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(branchCombo, 3, 4, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.branchLab, 3, 4, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.DEV_BTN, 4, 5, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.deviceLab, 4, 5, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(compile_btn, 5, 6, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.compileLab, 5, 6, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(sync_btn, 6, 7, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.syncLab, 6, 7, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(entryBox, 7, 8, 0, 1, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.build_appLab, 7, 8, 1, 2, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.clobberBtn, 8, 9, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.clobberLab, 8, 9, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerLT, 9, 10, 0, 1, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerLB, 9, 10, 1, 2, xpadding=50, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)

		Update().TEXT_COLOR()

		Globals.MAIN_WIN.add(MAIN_VBOX)
		Globals.MAIN_WIN.show_all()
		gtk.main()

def main():
	gtk.main()
	return 0

if __name__ == "__main__":

	chk_config()
	
	if not os.path.exists(Globals.myCONF):
		Parser().write("branch", "ics")
	
	if not os.path.exists(Globals.askConfirm):
		get_askConfirm()
	advanced().main()

