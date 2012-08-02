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
import vte
import webbrowser
from glob import glob

from cmcPy.About import About
from cmcPy.Globals import Globals
from cmcPy.Parser import Parser
from cmcPy.Update import Update

######################################################################
# Helper functions
######################################################################

def openBuildFolder():
     t = "%s/out/target/product/%s" % (repo_path, build_device)
     cmd = "nautilus %s" % (t)
     os.system(cmd)
     sys.exit()

def openFolder(obj):
	t = "%s/Downloads" % (u_home)
	cmd = "nautilus %s" % (t)
	os.system(cmd)
	gtk.main_quit()

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

def getManu(arg, br):
	s = None
	if br == "gb":
		paths = glob("device/*/*/device.mk")
	elif br == "ics" or br == "jellybean":
		paths = glob("device/*/*/cm.mk")
	else:
		paths = None

	if paths is not None:
		for x in paths:
			if arg in x:
				s = x.split("/")
				s = s[1]
	if s:
		return s
	else:
		return None

def get_askConfirm():
	def askedClicked():
		if not os.path.exists(Globals.askConfirm):
			file(Globals.askConfirm, 'w').close()

	q = Globals().QDial("**** User Confirmation ****", Globals.ask_confirm_info)
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
for i in ["Start adb", "View config", "Repo path", "Remove config", "Run bash", "Add device", "Stop/reset"]:
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

TERM = vte.Terminal()
entryBox = gtk.Entry()

######################################################################
# Global Settings
######################################################################
def run_vt_command(event):
	i = entryBox.get_text()
	print i
	
def run_local_shell():
	TERM.fork_command('bash')

def run_custom_device():
    title = "Setup custom device"
    message = "Please setup your device here:"
    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    table = gtk.Table(8, 1, False)
    dialog.vbox.pack_start(table)
    label = gtk.Label("Device name")
    label.show()
    entry = gtk.Entry()
    entry.show()
    label1 = gtk.Label("Device manufacturer")
    label1.show()
    entry1 = gtk.Entry()
    entry1.show()
    label2 = gtk.Label("Device tree url")
    label2.show()
    entry2 = gtk.Entry()
    entry2.show()
    label3 = gtk.Label("Device tree branch")
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
        os.chdir(manu_path)
        TERM.fork_command('bash')
        TERM.feed_child('git clone %s -b %s %s\n' % (u,b,n))
    else:
        Globals().CDial(gtk.MESSAGE_INFO, "Skipping this", "No changes have been made!")
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
        if value == 0:
        	start_adb()
        elif value == 1:
        	view_config()
        elif value == 2:
        	choose_repo_path()
        elif value == 3:
        	remove_config()
        elif value == 4:
        	run_local_shell()
        elif value == 5:
            run_custom_device()
        elif value == 5:
            main_cmc_cmd()
        else:
            pass

        i = toolsCombo.set_active(-1)

def compile_combo_change(event):
        value = str(makeCombo.get_active_text())
        Parser().write("make_jobs", value)
        
def sync_combo_change(event):
        value = str(syncCombo.get_active_text())
        Parser().write("sync_jobs", value)

def branch_combo_change(event):
        value = str(branchCombo.get_active_text())
        Parser().write("branch", value)
        Update().MAIN_INFO_LABEL()
        Update().DEVICES()
        
def device_combo_change(event):
        value = str(Globals.DEV_COMBO.get_active_text())
        Parser().write("device", value)
        Update().MAIN_INFO_LABEL()

def choose_repo_path():
	direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	r = direct.run()
	repo_dir = direct.get_filename()
	direct.destroy()
	if r == gtk.RESPONSE_ACCEPT:
		try:
			Parser().write("repo_path", repo_dir)
			Update().MAIN_INFO_LABEL()
		except NameError:
			pass

def remove_config():
	q = Globals.QDial("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
	if q == True:
		os.remove(cmcconfig)
		CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

def start_adb():
	TERM.fork_command(Globals.myA_ADB_START)

def view_config():
	TERM.fork_command(Globals.myA_VIEW_CONFIG)
	
def main_cmc_cmd():
	TERM.fork_command(Globals.myCMC_VT_TITLE)
	
def compile_or_sync(arg):
	if arg == "Syncing":
		TERM.fork_command(Globals.mySYNC_SCRIPT)
	elif arg == "Compiling":
		p = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		if p == "Default":
			p = Globals.myDEF_REPO_PATH
		os.chdir(p)
		m = getManu(d, b)
		if m == None:
			TERM.fork_command(Globals.myROOMSERVICE_SCRIPT)
		m = getManu(d, b)
		Parser().write("manuf", m)
		TERM.fork_command(Globals.myCOMPILE_SCRIPT)
	else:
		TERM.fork_command(Globals.myNONE_SCRIPT)

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
		elif i == "d" and data.state & gtk.gdk.CONTROL_MASK:
			Update().BACKGROUND_COLOR()
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
		color = gtk.gdk.color_parse(Parser().read('background_color'))
		Globals.MAIN_WIN.modify_bg(gtk.STATE_NORMAL, color)
		Globals.MAIN_WIN.resize(1080, 600)
		Globals.MAIN_WIN.realize()

		MAIN_VBOX = gtk.VBox(False, 0)
		
		TERM_FRAME = gtk.Frame()
		TERM_FRAME.show()
		TERM.show()
		TERM_FRAME.add(TERM)
		
		table = gtk.Table(1, 3, False)
		table.show()
		
		Update().MAIN_INFO_LABEL()
		Globals.MAIN_INFO.show()
		MAIN_VBOX.pack_start(Globals.MAIN_INFO, False, False, 5)

		MAIN_VBOX.pack_start(table, True, True, 0)

		tableB = gtk.Table(1, 2, False)
		tableB.show()

		MAIN_VBOX.pack_start(tableB, True, True, 0)

		tableEntry = gtk.Table(1, 2, False)
		tableEntry.show()

		MAIN_VBOX.pack_start(tableEntry, True, True, 5)

		Globals.KEY_BIND_INFO.set_markup(Globals.key_bindings)
		Globals.KEY_BIND_INFO.show()
		MAIN_VBOX.pack_start(Globals.KEY_BIND_INFO, False, False, 5)

		branchCombo.show()
		i = get_branch_combo()
		branchCombo.set_active(i)
		branchCombo.set_wrap_width(4)
		branchCombo.connect("changed", branch_combo_change)
		
		branchLab = gtk.Label()
		branchLab.set_markup("<span color=\"%s\">Branch</span>" % Globals.myColor)
		branchLab.show()
		
		Globals.DEV_COMBO.show()
		#i = read_parser("device")
		#Globals.DEV_COMBO.set_active(i)
		Globals.DEV_COMBO.set_wrap_width(4)
		Globals.DEV_COMBO.connect("changed", device_combo_change)
		Update().DEVICES()
		
		deviceLab = gtk.Label()
		deviceLab.set_markup("<span color=\"%s\">Device</span>" % Globals.myColor)
		deviceLab.show()
		
		syncCombo.show()
		syncCombo.set_active(int(Parser().read("sync_jobs"))-1)
		syncCombo.set_wrap_width(4)
		syncCombo.connect("changed", sync_combo_change)
		
		syncjobsLab = gtk.Label()
		syncjobsLab.set_markup("<span color=\"%s\">Sync jobs</span>" %Globals. myColor)
		syncjobsLab.show()
		
		makeCombo.show()
		makeCombo.set_active(int(Parser().read("make_jobs"))-1)
		makeCombo.set_wrap_width(4)
		makeCombo.connect("changed", compile_combo_change)
		
		makeLab = gtk.Label()
		makeLab.set_markup("<span color=\"%s\">Make jobs</span>" % Globals.myColor)
		makeLab.show()
		
		compile_btn = gtk.Button("Compile")
		compile_btn.set_size_request(140, 28)
		compile_btn.connect("clicked", main_sync_compile_btn, "Compiling")
		compile_btn.show()

		compileLab = gtk.Label()
		compileLab.set_markup("<span color=\"%s\">Compile</span>" % Globals.myColor)
		compileLab.show()
		
		sync_btn = gtk.Button("Sync")
		sync_btn.set_size_request(140, 28)
		sync_btn.connect("clicked", main_sync_compile_btn, "Syncing")
		sync_btn.show()
		
		syncLab = gtk.Label()
		syncLab.set_markup("<span color=\"%s\">Sync</span>" % Globals.myColor)
		syncLab.show()
		
		toolsCombo.show()
		toolsCombo.set_wrap_width(2)
		toolsCombo.set_size_request(40, 28)
		toolsCombo.connect("changed", tools_combo_change)
		
		toolsLab = gtk.Label()
		toolsLab.set_markup("<span color=\"%s\">Tools</span>" % Globals.myColor)
		toolsLab.show()

		entryBox.show()
		entryBox.connect("activate", run_vt_command)
		
		build_appLab = gtk.Label()
		build_appLab.set_markup("<span color=\"%s\"><small>Build specific <b>app/binary</b> here.</small></span>" % Globals.myColor)
		build_appLab.show()
		
		SpacerRT = gtk.Label()
		SpacerRT .show()
		SpacerLT  = gtk.Label()
		SpacerLT .show()

		SpacerRB = gtk.Label()
		SpacerRB .show()
		SpacerLB  = gtk.Label()
		SpacerLB .show()
		
		SpacerERT = gtk.Label()
		SpacerERT .show()
		SpacerELT  = gtk.Label()
		SpacerELT .show()

		SpacerERB = gtk.Label()
		SpacerERB .show()
		SpacerELB  = gtk.Label()
		SpacerELB .show()
		
		table.attach(TERM_FRAME, 1, 2, 0, 1, xpadding=10, ypadding=10)
		
		tableB.attach(SpacerRT, 0, 1, 0, 1, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerRB, 0, 1, 1, 2, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(branchLab, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(branchCombo, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(deviceLab, 2, 3, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(Globals.DEV_COMBO, 2, 3, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(syncjobsLab, 3, 4, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(syncCombo, 3, 4, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(makeLab, 4, 5, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(makeCombo, 4, 5, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(compileLab, 5, 6, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(compile_btn, 5, 6, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(syncLab, 6, 7, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(sync_btn, 6, 7, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(toolsLab, 7, 8, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(toolsCombo, 7, 8, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerLT, 8, 9, 0, 1, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableB.attach(SpacerLB, 8, 9, 1, 2, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)

		tableEntry.attach(SpacerERT, 0, 1, 0, 1, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(SpacerERB, 0, 1, 1, 2, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(build_appLab, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(entryBox, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(SpacerELT, 2, 3, 0, 1, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		tableEntry.attach(SpacerELB, 2, 3, 1, 2, xpadding=25, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		main_cmc_cmd()

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

