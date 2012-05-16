#!/usr/bin/env python
from helper import *

class WalkThroughThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet():
			gtk.threads_enter()
			WalkThrough()
			main()
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

class WalkThrough():

    def delete(self, widget, event=None):
        gtk.main_quit()
        return False

    def __init__(self):
        window = gtk.Window()
	window.set_title("CMC Walkthrough")
	window.set_icon(placeIcon)
        window.connect("delete_event", self.delete)
        window.set_border_width(10)

        table = gtk.Table(3,6,False)
        window.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        table.attach(notebook, 0,6,0,1)
        notebook.show()
        notebook.set_show_border(False)
	notebook.set_show_tabs(False)

        # Let's append a bunch of pages to the notebook
        for i in range(5):
            bufferf = "Append Frame %d" % (i+1)
            bufferl = "Page %d" % (i+1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(700, 400)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            notebook.append_page(frame, label)
    
        # Set what page to start at (page 4)
        notebook.set_current_page(0)

        button = gtk.Button("prev page")
        button.connect("clicked", lambda w: notebook.prev_page())
        table.attach(button, 1,2,1,2)
        button.show()

        button = gtk.Button("next page")
        button.connect("clicked", lambda w: notebook.next_page())
        table.attach(button, 2,3,1,2)
        button.show()

        table.show()
        window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    WalkThroughThread().start()

