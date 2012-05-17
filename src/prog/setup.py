#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

from helper import *

class Setup():
 
	def main_quit(self, obj):
		gtk.main_quit()
 
	# Main program
	def main(self):

		def callback_device(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("device", data)

		def callback_branch(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("branch", data)

		def choose_branch(obj):

			dialog = gtk.Dialog("Choose branch", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(260, 200)
			dialog.set_resizable(False)

			scroll = gtk.ScrolledWindow()
			scroll.set_border_width(10)
			scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
			dialog.vbox.pack_start(scroll, True, True, 0)
			scroll.show()

			table = gtk.Table(2, 1, False)
			table.set_row_spacings(45)

			scroll.add_with_viewport(table)
			table.show()

			device = gtk.RadioButton(None, None)

			button_count = 0
			for radio in list(["ics", "gingerbread"]):

				button_count += 1
				button = "button%s" % (button_count)

				button = gtk.RadioButton(group=device, label="%s" % (radio))
				button.connect("toggled", callback_branch, "%s" % (radio))
				table.attach(button, 0, 1, 0, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

			dialog.run()
			dialog.destroy()

		def choose_repo_path(obj):
			direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			r = direct.run()
			repo_dir = direct.get_filename()
			direct.destroy()
			if r == gtk.RESPONSE_ACCEPT:
				try:
					parser("repo_path", repo_dir)
				except NameError:
					pass

		def remove_config(obj):
			q = question_dialog("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
			if q == True:
				os.remove(cmcconfig)
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		def view_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)
			dialog.set_resizable(False)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(cmcconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def viewgit_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc git configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)
			dialog.set_resizable(False)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(gitconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def device_list(obj):

			b = read_parser("branch")
			if "Default" in b:
				custom_dialog(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
				chk_config = 0
			elif "gingerbread" in b:
				useBranch = urlCmGb
				chk_config = 1
			elif "ics" in b:
				useBranch = urlCmIcs
				chk_config = 1
			else:
				useBranch = "null"
				chk_config = 0

			if chk_config == True:
				try:
					filehandle = urllib.urlopen(useBranch)
				except IOError:
					custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

				count = 0
				for lines in filehandle.readlines():
					count += 1

				filehandle.close()

				dialog = gtk.Dialog("Choose device", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
				dialog.set_size_request(260, 400)
				dialog.set_resizable(False)

				scroll = gtk.ScrolledWindow()
				scroll.set_border_width(10)
				scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
				dialog.vbox.pack_start(scroll, True, True, 0)
				scroll.show()

				table = gtk.Table(count, 1, False)
				table.set_row_spacings(5)

				scroll.add_with_viewport(table)
				table.show()

				device = gtk.RadioButton(None, None)

				try:
					filehandle = urllib.urlopen(useBranch)
				except IOError:
					custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

				button_count = 0
				for lines in filehandle.readlines():

					if "combo" in lines:
						button_count += 1
						button = "button%s" % (button_count)

						x = lines.split(" ")
						radio = x[1]
						x = radio.split("_")
						radio = x[1]
						x = radio.split("-")
						radio = x[0]

						button = gtk.RadioButton(group=device, label="%s" % (radio))
						button.connect("toggled", callback_device, "%s" % (radio))
						table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
						button.show()

				filehandle.close()

				dialog.run()
				dialog.destroy()

		def ThemeClicked(widget, event, data):
			if data == "a-default.png":
				data = "Default"
				icon = "%s/a-default.png" % (cmcThemeSmall)
				sendNoti("Cmc theme", "Default theme has been set", icon)
			else:
				icon = "%s/%s" % (cmcThemeSmall, data)
				sendNoti("Cmc theme", "Theme has been set", icon)
			parser("theme", data)

		dialog = gtk.Dialog("CMC Setup", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_position(gtk.WIN_POS_CENTER)
		dialog.set_resizable(False)

		settings_lab = gtk.Label("Configure your settings here")
		settings_lab.show()
		dialog.vbox.pack_start(settings_lab, False, False, 10)

		table = gtk.Table(6, 2, False)
		table.set_row_spacings(5)
		table.show()

		dialog.vbox.pack_start(table, True, True, 15)

		device_btn = gtk.Button("Choose device")
		device_btn.set_size_request(140, 28)
		device_btn.connect("clicked", device_list)
		device_btn.show()

		branch_btn = gtk.Button("Choose branch")
		branch_btn.set_size_request(140, 28)
		branch_btn.connect("clicked", choose_branch)
		branch_btn.show()

		repo_path_btn = gtk.Button("Choose repo path")
		repo_path_btn.set_size_request(140, 28)
		repo_path_btn.connect("clicked", choose_repo_path)
		repo_path_btn.show()

		viewgit_btn = gtk.Button("View git config")
		viewgit_btn.set_size_request(140, 28)
		viewgit_btn.connect("clicked", viewgit_config)
		viewgit_btn.show()

		view_btn = gtk.Button("View config")
		view_btn.set_size_request(140, 28)
		view_btn.connect("clicked", view_config)
		view_btn.show()

		config_btn = gtk.Button("Remove config")
		config_btn.set_size_request(140, 28)
		config_btn.connect("clicked", remove_config)
		config_btn.show()

		table.attach(device_btn, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(branch_btn, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(repo_path_btn, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(viewgit_btn, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(view_btn, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(config_btn, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)


		theme_label = gtk.Label()
		theme_label.set_markup("<small>To change the theme, please select your preference from <b>below</b></small>")
		theme_label.show()
		dialog.vbox.pack_start(theme_label, False, False, 0)

		scroll = gtk.ScrolledWindow()
		scroll.set_size_request(400, 180)
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		tab = gtk.Table(1, 8, True)
		tab.set_col_spacings(10)
		scroll.add_with_viewport(tab)
		tab.show()

		dirList = custom_listdir(cmcThemeSmall)
		count = 0
		for x in dirList:
			count+=1

			event = "event%s" % (count)
			image = "image%s" % (count)

			tooltips = gtk.Tooltips()
			event = gtk.EventBox()
			image = gtk.Image()
			path = "%s/%s" % (cmcThemeSmall, x)
			image.set_from_file(path)
			event.connect("button_press_event", ThemeClicked, x)
			tooltips.set_tip(event, x)
			event.add(image)
			tab.attach(event, count-1, count, 0, 1)
			image.show()
			event.show()

		b = read_parser("branch")
		d = read_parser("device")
		r = read_parser("repo_path")
		if r == "Default":
			r = default_repo_path
		settings_info = gtk.Label()
		settings_info.set_alignment(0, 0)
		settings_info.set_markup("<small><small>Device: <b>%s</b>\nBranch: <b>%s</b>.\nRepo path: <b>%s</b></small></small>" % (d,b,r))
		settings_info.show()
		dialog.vbox.pack_start(settings_info, False, False, 10)

		dialog.run()
		dialog.destroy()
 
if __name__ == '__main__':
	go = Setup()
	go.main()
