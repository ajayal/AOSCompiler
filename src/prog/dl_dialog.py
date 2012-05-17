#!/usr/bin/env python

#   CMCompiler is free software. It comes without any warranty, to
#   the extent permitted by applicable law. You can redistribute it
#   and/or modify it under the terms of the Do What The Fuck You Want
#   To Public License, Version 2, as published by Sam Hocevar. See
#   http://sam.zoy.org/wtfpl/COPYING for more details.

from helper import *

repo_path = read_parser("repo_path")
repo_branch = read_parser("branch")
build_device = read_parser("device")

dl_version = None
dl_url = None
dl_device = None
mylist = []

class DownloadDialog():

	def main(self):

		def get_download_urls(device, version):
			RURL = "http://download.cyanogenmod.com"
			URL = "http://download.cyanogenmod.com/?device=%s&type=%s" % (device, version)
			htmlpage = urllib2.urlopen(URL).read()
			alllinks = re.findall('<a href=\".*?\">.*?zip</a>',htmlpage)

			count=1
			global mylist
			for links in alllinks:
				x = "%s%s" % (RURL, links)
				x = x.split("\"")
				x = x[1]
				y = x.split("/")

				if y[2] == "artifacts":
					y = y[6]
				elif y[2] == "RC":
					y = y[3]
				else:
					y = y[4]

				s = "%s%s" % (RURL, x)
				mylist.append(s)

				if count == 10:
					break
				else:
					count += 1

			return

		def downloadList(obj):
			def callback_url(widget, data=None):
				print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
				global dl_url
				dl_url = data

			dl_list.hide()
			device_scroll.hide()
			version_tbl.hide()

			table3 = gtk.Table(5, 1, False)
			table3.set_row_spacings(15)
			table3.set_col_spacings(15)
			table3.show()
			dialog.vbox.pack_start(table3, True, True, 0)

			url = gtk.RadioButton(None, None)

			button_count = 0
			get_download_urls(dl_device, dl_version)
			print mylist
			for lines in mylist:

				button_count += 1
				button = "button%s" % (button_count)
				x = lines.split("/")
				x = x[-1]

				print x

				button = gtk.RadioButton(group=url, label="%s" % (x))
				button.connect("toggled", callback_url, "%s" % (lines))
				table3.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK, xpadding=50, ypadding=7)
				button.show()

		def callback_device(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			global dl_device
			dl_device = data
			if not dl_version == None and not dl_device == None:
				dl_list.show()
		

		def callback_version(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			global dl_version
			dl_version = data
			if not dl_version == None and not dl_device == None:
				dl_list.show()

		dialog = gtk.Dialog("Download Cyanogenmod", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_resizable(False)

		device_scroll = gtk.ScrolledWindow()
		device_scroll.set_border_width(10)
		device_scroll.set_size_request(200, 180)
		device_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		device_scroll.show()
		dialog.vbox.pack_start(device_scroll, True, True, 0)

		try:
			filehandle = urllib2.urlopen("http://download.cyanogenmod.com").read()
			alldevices = re.findall('.*?navigate_device.*?</a></li>', filehandle)
			print alldevices
		except IOError:
			alldevices = None
			custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")
			exit()

		count = 0
		for lines in alldevices:
			print lines
			count += 1

		device_tbl = gtk.Table(count, 1, False)
		device_tbl.set_row_spacings(5)

		device_scroll.add_with_viewport(device_tbl)
		device_tbl.show()

		device = gtk.RadioButton(None, None)

		button_count = 0
		for lines in alldevices:
			button_count += 1
			if "device_all" in lines:
				print "skipping first line all"
				button_count = 0
			else:

				button_count += 1
				button = "button%s" % (button_count)

				s = lines.split(">")
				s = s[2]
				s = s.split("<")
				s = s[0]
				print s

				button = gtk.RadioButton(group=device, label="%s" % (s))
				button.connect("toggled", callback_device, "%s" % (s))
				device_tbl.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

		version_tbl = gtk.Table(1, 4, False)
		version_tbl.set_row_spacings(15)
		version_tbl.set_row_spacings(15)
		version_tbl.show()
		dialog.vbox.pack_start(version_tbl, True, True, 0)

		version = gtk.RadioButton(None, None)

		button_count = 0
		for lines in list(["all", "nightly", "RC", "stable"]):

			button_count += 1
			button = "button%s" % (button_count)

			button = gtk.RadioButton(group=version, label="%s" % (lines))
			if lines == "all":
				button.connect("toggled", callback_version, "")
			else:
				button.connect("toggled", callback_version, "%s" % (lines))
			version_tbl.attach(button, button_count-1, button_count, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

		dl_list = gtk.Button("Download List")
		dl_list.set_size_request(140, 28)
		dl_list.connect("clicked", downloadList)
		dl_list.hide()
		dialog.vbox.pack_start(dl_list, True, True, 15)

		dialog.run()
		dialog.destroy()
		if not dl_url == None:
			cmd = "python download.py %s &" % (dl_url)
			os.system(cmd)
		else:
			custom_dialog(gtk.MESSAGE_WARNING, "No Download Choosen", "You didn't select a download, can't download anything for you!")

if __name__ == "__main__":
	DownloadDialog().main()

