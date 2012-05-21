#!/usr/bin/env python
import sys
import gtk
import appindicator

import subprocess
import time

RESOLUTION = "1440x900"
SIDE = "right"

"""Future Features:
	switching out the xorg.conf.nvidia so that optirun can actually be used properly
"""

class ThinkDisp:
    def __init__(self):
        self.ind = appindicator.Indicator("think-disp-indicator",
                                           "indicator-think",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon("gsd-xrandr") #this is located in /usr/share/icons/ubuntu-mono-light/apps/24/

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.status_item = gtk.MenuItem("Check Status")
        self.status_item.connect("activate", self.status_check)
        self.status_item.show()
        self.menu.append(self.status_item)

        self.dispon_item = gtk.MenuItem("Turn Disp On")
        self.dispon_item.connect("activate", self.start_disp)
        self.dispon_item.show()
        self.menu.append(self.dispon_item)

        self.dispoff_item = gtk.MenuItem("Turn Disp Off")
        self.dispoff_item.connect("activate", self.kill_disp)
        self.dispoff_item.show()
        self.menu.append(self.dispoff_item)

        self.cardon_item = gtk.MenuItem("Turn Card On")
        self.cardon_item.connect("activate", self.card_on)
        self.cardon_item.show()
        self.menu.append(self.cardon_item)

        self.cardoff_item = gtk.MenuItem("Turn Card Off")
        self.cardoff_item.connect("activate", self.card_off)
        self.cardoff_item.show()
        self.menu.append(self.cardoff_item)

        self.quit_item = gtk.MenuItem("Quit Indicator")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def status_check(self, widget):
        a = subprocess.check_output(["cat", "/proc/acpi/bbswitch"])
        if "ON" in a:
            print("card is on")
            self.popup_test("The Card is On", "Card Status")
        elif "OFF" in a:
            print("card is off")
            self.popup_test("The Card is Off", "Card Status")

    def card_on(self, widget):
        p = subprocess.Popen(["sudo", "tee", "/proc/acpi/bbswitch"], stdin=subprocess.PIPE)
        p.communicate(input="ON")

    def card_off(self, widget):	
        p = subprocess.Popen(["sudo", "tee", "/proc/acpi/bbswitch"], stdin=subprocess.PIPE)
        p.communicate(input="OFF")


    def popup_test(self, message_text, dialog_title):
        label = gtk.Label(message_text)
        dialog = gtk.Dialog(dialog_title,
                    None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        #checkbox = gtk.CheckButton("Useless checkbox")
        #dialog.action_area.pack_end(checkbox)
        #checkbox.show()
        response = dialog.run()
        dialog.destroy()
    
    #runs the commands to start the display using RESOLUTION and SIDE
    def start_disp(self, widget):
        subprocess.Popen(["optirun", "true"])
        subprocess.Popen(["xrandr", "--output", "LVDS1", "--auto", "--output", "VIRTUAL", "--mode", str(RESOLUTION), "--"+str(SIDE)+"-of", "LVDS1"])
		#YOU MUST HAVE screenclone in /usr/bin/
        subprocess.Popen(["screenclone", "-d", ":8", "-x", "1"])

    def kill_disp(self, widget):
        subprocess.call(["thinkdispk1"])
        subprocess.call(["thinkdispk2"])

if __name__ == "__main__":
	#ensures that bbswitch dkms module is inserted and usable
    print("the thinkdisp icon should now be in your top panel")
    print("there are currently some bugs - for example if thinkdisp crashes \n so does the xserver running the second monitor")
    subprocess.call(["sudo", "modprobe", "bbswitch"])
    indicator = ThinkDisp()
    indicator.main()
