#!/usr/bin/env python
from vars import *


def sendNoti(title, summary, icon):
	pynotify.init(title)
	n = pynotify.Notification(title, summary, icon)
	n.show()

def custom_listdir(path):
    dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
    dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))

    return dirs

def checkAdb():
	cmd = "adb devices |wc -l"
	c = commands.getoutput(cmd)
	if not c == "3":
		return False
	else:
		return True

def extractFiles(parg, marg, darg):
	os.chdir(repo_path)
	d = "%s/device/%s/%s" % (parg, marg, darg)
	if os.path.exists(d):
		os.chdir(d)
	if os.path.exists("extract-files.sh"):
		d = "%s/vendor/%s/%s/proprietary" % (parg, marg, darg)
		if not os.path.exists(d):
			cmd = "sh extract-files.sh"
			os.system(cmd)
			d = "%s/vendor/%s/%s/proprietary" % (parg, marg, darg)
			time.sleep(0.5)
			if os.path.exists(d):
				return True
			else:
				return False
		else:
			return True
	else:
		return False

def install_repo():
	cmd1 = "curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > %s/repo" % (configdir)
	cmd2 = "chmod a+x %s/repo" % (configdir)
	cmd3 = "gksudo mv %s/repo /usr/local/sbin/" % (configdir)
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

def custom_dialog(dialog_type, title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=dialog_type,
                               buttons=gtk.BUTTONS_OK)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    dialog.run()
    dialog.destroy()
    return True

def question_dialog(title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=gtk.MESSAGE_QUESTION,
                               buttons=gtk.BUTTONS_YES_NO)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.RESPONSE_YES:
       return True
    else:
       return False

def chk_config():
	if not os.path.exists(configdir):
		os.makedirs(configdir)

def getManu(arg):
	s = None
	paths = glob("device/*/*/cm.mk")
	for x in paths:
		if arg in x:
			s = x.split("/")
			s = s[1]
	if s:
		return s
	else:
		return None

def common_chk():
	r = "%s/NeedRepoScript" % (configdir)
	if os.path.exists(r):
		os.remove(r)

	d = "%s/NoDeviceC" % (configdir)
	if os.path.exists(d):
		os.remove(d)

	g = "%s/GenError" % (configdir)
	if os.path.exists(g):
		os.remove(g)

	chk_repo = 0
	global repo_path
	global repo_branch
	p = read_parser("repo_path")
	if not p == "Default":
		repo_path = read_parser("repo_path")
	else:
		repo_path = default_repo_path

	repo_branch = read_parser("branch")
	chk_dev = read_parser("device")
	if not chk_dev == "Default":
		if not os.path.exists(repo_path):
			os.makedirs(repo_path)
		os.chdir(repo_path)
		p = which("repo")
		if p == None:
			chk_repo = 0
		else:
			chk_repo = 1
	else:
		chk_repo = 2

	return chk_repo


def get_askConfirm():
	def askedClicked():
		if not os.path.exists(askConfirm):
			file(askConfirm, 'w').close()

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("**** User Confirmation ****")
	dialog.set_markup("<small>This is what <b>YOU</b> do to <b>YOUR</b> phone.</small>")
	dialog.format_secondary_markup("<small>By no means what so ever is this software or cyanogenmod responsible for what you do to your phone. \
You are taking the risks, you are choosing to this to your phone. By proceeding you are aware, you are warned. No crying or moaning. This software \
was tested by human beings, not cybogs from your mothers closet. Please keep this in mind when something breaks, or hangs.  If you have an issue \
with this software, please let me know.\n\nBy clicking this ok button, you have given me your soul.\n\nPlay safe.\n\n</small>\
<small><small><b>Note:\n- </b><i>This will not proceed unless you agree.</i></small>\n\
<small><b>-</b><i> Cyanogenmod doesn't consider source builds offical, please keep this in mind if you plan on bug reporting.</i></small></small>")
	dialog.set_resizable(False)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		askedClicked()
	else:
		exit()
	dialog.destroy()

def set_git_Text():

	def loginClicked(name, email):
		if not os.path.exists(gitconfig):
			file(gitconfig, 'w').close()
			f = open(gitconfig, 'w')
			f.write("[color]\n")
			f.write("	ui = auto\n")
			f.write("[user]\n")
			f.write("	name = %s\n" % name)
			f.write("	email = %s\n" % email)
			f.write("[review \"review.cyanogenmod.com\"]\n")
			f.write("	username = %s\n" % name)
			f.close()

	def loginChecked(name, email):
		if "ex" in name:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad username", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		elif "ex" in email:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad email", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		else:
			loginClicked(name, email)

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("User settings for repo config..")
	dialog.set_markup("<small>This will be used for <i>identification</i> purposes only</small>")
	dialog.format_secondary_markup("<small>This will be used to create a config file used by the repo script. This script is used to sync the repo locally. This information is not being used in any other way. You can look at the git config here:\n\n<b>%s/.gitconfig</b>\n\n<small><b>Note:</b> <i>This will be needed before we can start using cyanogenmod compiler.</i></small></small>" % u_home)
	dialog.set_resizable(False)

	table = gtk.Table(4, 1, True)
	table.set_row_spacings(5)
	table.show()

	dialog.vbox.pack_start(table, True, True, 0)

	user_entry = gtk.Entry()
	user_entry.set_text("ex. lithid")
	user_lab = gtk.Label("User:")
	user_entry.show()
	user_lab.show()
	email_entry = gtk.Entry()
	email_entry.set_text("ex. mrlithid@gmail.com")
	email_lab = gtk.Label("Email:")
	email_entry.show()
	email_lab.show()

	table.attach(user_lab, 0, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(user_entry, 0, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)
	table.attach(email_lab, 0, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(email_entry, 0, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		name = user_entry.get_text()
		email = email_entry.get_text()
		loginChecked(name, email)
	else:
		exit()
	dialog.destroy()

def read_parser(arg):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		c = config.get(title, arg)

	except ConfigParser.NoSectionError:
		c = "%s" % (default)

	return c

def parser(arg, value):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		getTheme = config.get(title, 'theme')
		getDevice = config.get(title, 'device')
		getBranch = config.get(title, 'branch')
		getRepoPath = config.get(title, 'repo_path')
	except ConfigParser.NoSectionError:
		getTheme = None
		getDevice = None
		getBranch = None
		getRepoPath = None

	config = ConfigParser.RawConfigParser()
	config.add_section(title)

	if arg == "device":
		config.set(title, 'device', value)
	elif getDevice:
		config.set(title, 'device', getDevice)
	else:
		config.set(title, 'device', default)

	if arg == "theme":
		config.set(title, 'theme', value)
	elif getTheme:
		config.set(title, 'theme', getTheme)
	else:
		config.set(title, 'theme', default)

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
		config.set(title, 'repo_path', default)

	with open(cmcconfig, 'wb') as configfile:
    		config.write(configfile)

