#!/usr/bin/env python

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

from aoscPy.About import About
from aoscPy.Globals import Globals
from aoscPy.Parser import Parser
from aoscPy.Update import Update
from aoscPy.Utils import Utils
from aoscPy.Compile import Compile
from aoscPy.Sync import Sync
from aoscPy.InstallPackages import InstallPackages

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
for i in ["Options", "Start adb", "View config", "Repo path", "Remove config", "Run bash", "Add device", "Stop/reset", "Open rom folder", "Install packages", "Install repo"]:
	toolsCombo.append_text(i)

romCombo = gtk.combo_box_new_text()
for i in ["Choose", "AOSP", "CM", "AOKP", "CNA", "GR"]:
	romCombo.append_text(i)

makeCombo = gtk.combo_box_new_text()
for i in range(1,Globals.numprocs+1):
	makeCombo.append_text(str(i))

syncCombo = gtk.combo_box_new_text()
for i in range(1,17):
	syncCombo.append_text(str(i))

entryBox = gtk.Entry()

######################################################################
# Global Settings
######################################################################
def run_vt_command(event):
	Globals.TERM.set_background_saturation(0.3)
	i = entryBox.get_text()
	r = Parser().read('repo_path')
	d = Parser().read('device')
	a = Parser().read('rom_abrv')
	os.chdir(r)
	Globals.TERM.fork_command('bash')
	Globals.TERM.feed_child('clear\n')
	Globals.TERM.feed_child('. build/envsetup.sh\n')
	if a == "CM":
		Globals.TERM.feed_child('lunch cm_%s-userdebug\n' % d)
	elif a == "GR":
		Globals.TERM.feed_child('lunch geek_%s-userdebug\n' % d)
	else:
		return
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

def tools_combo_change(event):
	value = int(toolsCombo.get_active())
	if value == 1:
		start_adb()
	elif value == 2:
		Utils().ViewConfig()
	elif value == 3:
		choose_repo_path()
	elif value == 4:
		remove_config()
	elif value == 5:
		run_local_shell()
	elif value == 6:
		run_custom_device()
	elif value == 7:
		Utils().ResetTerm()
	elif value == 8:
		openBuildFolder()
	elif value == 9:
		InstallPackages().runInstall()
	elif value == 10:
		InstallPackages().repo()
	else:
		pass

	toolsCombo.set_active(0)

def compile_combo_change(event):
	value = str(makeCombo.get_active_text())
	Parser().write("make_jobs", value)

def sync_combo_change(event):
	value = str(syncCombo.get_active_text())
	Parser().write("sync_jobs", value)

def rom_combo_change(event):
	value = str(romCombo.get_active_text())
	if value == "Choose":
		pass
	else:
		if value == "AOSP":
			value2 = "Android Open Source Project"
		elif value == "AOKP":
			value2 = "Android Open Kang Project"
		elif value == "CM":
			value2 = "CyanogenMod"
		elif value == "CNA":
			value2 = "Codename Android"
		elif value == "GR":
			value2 = "GeekRom"
		else:
			Value2 = "Android Open Source Compiler"
		Parser().write("rom_dist", value2)
		Parser().write("rom_abrv", value)
		Parser().write("branch", "Default")
		Parser().write("device", "Default")
		Parser().write("manuf", "Default")
		Update().TEXT()
	romCombo.set_active(0)

def device_button(event):
	Utils().Devices()
	Update().TEXT()

def run_button(event):
	isit = None
	r = Parser().read("repo_path")
	os.chdir(r)
	Globals.TERM.set_background_saturation(0.3)
	Globals.TERM.fork_command('clear')
	Globals.TERM.fork_command('bash')
	if 	Globals.checkClobber.get_active() == True:
		isit = True
		Globals.TERM.feed_child('make clobber\n')

	if Globals.checkSync.get_active() == True:
		Sync().run()

	if Globals.checkCompile.get_active() == True:
		isit = True
		Compile().run()

	if isit == None:
		Utils().ResetTerm()

def choose_repo_path():
	direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	r = direct.run()
	repo_dir = direct.get_filename()
	direct.destroy()
	if r == gtk.RESPONSE_ACCEPT:
		try:
			Parser().write("repo_path", repo_dir)
			Update().TEXT()
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

def hit_event_btn(obj, event, arg):
	print "Pressed event button: %s" % arg

######################################################################
# Advanced
######################################################################
class advanced():
 
	def main_quit(self, widget, event=None):
		gtk.main_quit()

	def on_key_press(self, widget, data=None):
		i = gtk.gdk.keyval_name(data.keyval)

		if i == "v" and data.state & gtk.gdk.CONTROL_MASK:
			Utils().ViewConfig()
		elif i == "a" and data.state & gtk.gdk.CONTROL_MASK:
			start_adb()
		elif i == "m" and data.state & gtk.gdk.CONTROL_MASK:
			Utils().ResetTerm()
		elif i == "s" and data.state & gtk.gdk.CONTROL_MASK:
			Sync().run()
		elif i == "b" and data.state & gtk.gdk.CONTROL_MASK:
			Compile().run()
		elif i == "r" and data.state & gtk.gdk.CONTROL_MASK:
			choose_repo_path()
		elif i == "x" and data.state & gtk.gdk.CONTROL_MASK or i == "Escape":
			gtk.main_quit()
		else:
			pass
 
	# Main program
	def main(self):
		Globals.MAIN_WIN.set_title(Globals.myMainTitle)
		Globals.MAIN_WIN.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		Globals.MAIN_WIN.set_icon(myMAIN_ICON)
		Globals.MAIN_WIN.connect("delete_event", self.main_quit)
		Globals.MAIN_WIN.connect("key_press_event", self.on_key_press)
		Globals.MAIN_WIN.set_events(gtk.gdk.KEY_PRESS_MASK)
		Globals.MAIN_WIN.set_events(gtk.gdk.CONTROL_MASK)
		Globals.MAIN_WIN.set_size_request(1024, 638)
		Globals.MAIN_WIN.set_resizable(False)

		MAIN_VBOX = gtk.VBox(False, 0)

		TERM_FRAME = gtk.Frame()
		TERM_FRAME.show()
		Globals.TERM.show()
		TERM_FRAME.add(Globals.TERM)

		table = gtk.Table(1, 3, False)
		table.show()

		Globals.MAIN_INFO.show()
		Globals.KEY_BIND_INFO.show()
		Globals.aoscTitleLab.show()

		# Build options
		toolsCombo.show()
		toolsCombo.set_wrap_width(2)
		toolsCombo.set_active(0)
		toolsCombo.connect("changed", tools_combo_change)

		Globals.toolsLab.show()

		romCombo.show()
		romCombo.set_wrap_width(2)
		romCombo.set_active(0)
		romCombo.connect("changed", rom_combo_change)

		Globals.romLab.show()

		aboutRomImg = gtk.Image()
		aboutRomImg.set_from_file(Globals.ClobImg)
		Globals.aboutRomBtn.set_image(aboutRomImg)
		Globals.aboutRomBtn.connect("clicked", Utils().aboutRom)
		Globals.aboutRomBtn.show()

		Globals.aboutRomLab.show()

		branchImg = gtk.Image()
		branchImg.set_from_file(Globals.ClobImg)
		Globals.branchBtn.set_image(branchImg)
		Globals.branchBtn.connect("clicked", Utils().choose_branch)
		Globals.branchBtn.show()

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

		optTable = gtk.Table(2, 1, False)
		optTable.show()
		optTable.attach(romCombo, 0, 1, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.romLab, 0, 1, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.aboutRomBtn, 1, 2, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.aboutRomLab, 1, 2, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.branchBtn, 2, 3, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.branchLab, 2, 3, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.DEV_BTN, 3, 4, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.deviceLab, 3, 4, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(syncCombo, 4, 5, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.syncjobsLab, 4, 5, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(makeCombo, 5, 6, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.makeLab, 5, 6, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(toolsCombo, 6, 7, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.attach(Globals.toolsLab, 6, 7, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		optTable.set_border_width(5)
		optFrame = gtk.Frame()
		optFrame.add(optTable)
		Globals.buildFrameLab.show()
		optFrame.set_label_widget(Globals.buildFrameLab)
		optFrame.set_border_width(5)
		optFrame.show()

		# Build Frame
		Globals.checkCompile.set_active(False)
		Globals.checkCompile.show()

		Globals.compileLab.show()

		Globals.checkSync.set_active(False)
		Globals.checkSync.show()

		Globals.syncLab.show()

		Globals.checkClobber.set_active(False)
		Globals.checkClobber.show()

		Globals.clobberLab.show()

		runImg = gtk.Image()
		runImg.set_from_file(Globals.ClobImg)
		Globals.runBtn.set_image(runImg)
		Globals.runBtn.connect("clicked", run_button)
		Globals.runBtn.show()

		Globals.runLab.show()

		buildTable = gtk.Table(2, 1, False)
		buildTable.show()
		buildTable.attach(Globals.checkCompile, 0, 1, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.compileLab, 0, 1, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.checkSync, 1, 2, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.syncLab, 1, 2, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.checkClobber, 2, 3, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.clobberLab, 2, 3, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.runBtn, 3, 4, 0, 1, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.attach(Globals.runLab, 3, 4, 1, 2, xpadding=15, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		buildTable.set_border_width(5)
		buildFrame = gtk.Frame()
		buildFrame.add(buildTable)
		Globals.runFrameLab.show()
		buildFrame.set_label_widget(Globals.runFrameLab)
		buildFrame.show()

		# Entrybox stuff
		tableEntry = gtk.Table(1, 2, False)
		tableEntry.show()

		entryBox.show()
		entryBox.connect("activate", run_vt_command)

		Globals.build_appLab.show()

		tableEntry.attach(entryBox, 0, 1, 0, 1, ypadding=5, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(Globals.build_appLab, 0, 1, 1, 2, xoptions=gtk.EXPAND)
		tableEntry.set_border_width(5)

		Globals.LinkContact.show()

		# Link footer stuff
		LinksTable = gtk.Table(2, 1, False)
		LinksTable.show()

		SpacerLinkR = gtk.Label()
		SpacerLinkR.show()

		SpacerLinkL = gtk.Label()
		SpacerLinkL.show()

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
			event.set_size_request(26, 26)
			event.show()
			tooltip = gtk.Tooltips()
			tooltip.set_tip(event, i)
			LinksTable.attach(event, count-1, count, 0, 1,)

		linksFrame = gtk.Frame()
		linksFrame.add(LinksTable)
		linksFrame.set_size_request(300, 75)
		linksFrame.set_label("Contact")
		linksFrame.show()

		# Main button table
		tableB = gtk.Table(1, 2, False)
		tableB.show()

		MAIN_VBOX.pack_start(Globals.aoscTitleLab, False, False, 0)
		MAIN_VBOX.pack_start(Globals.MAIN_INFO, False, False, 0)
		MAIN_VBOX.pack_start(table, True, True, 0)
		MAIN_VBOX.pack_start(Globals.KEY_BIND_INFO, False, False, 0)
		MAIN_VBOX.pack_start(optFrame, True, True, 0)
		MAIN_VBOX.pack_start(tableB, True, True, 0)

		table.attach(TERM_FRAME, 0, 1, 0, 1, xpadding=10)

		tableB.attach(buildFrame, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(tableEntry, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(linksFrame, 2, 3, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)

		Update().TEXT()

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

