#!/usr/bin/env python
import sys
import gtk
import appindicator

import subprocess
import time
import thread
import os

#available resolutions, set to standard xrandr resolutions by default
AVAIL_RES = ["1920x1200", "1920x1080", "1600x1200", "1680x1050", "1400x1050", "1440x900", "1280x960", "1360x768", "1152x864", "800x600", "640x480"]

#SETTINGS are loaded at runtime from prefs.ini, currently two: RESOLUTION and SIDE
#RESOLUTION: currently set resolution for the external monitor
#SIDE: the side on which your external monitor is, relative to the thinkpad display
SETTINGS = { }

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

        self.prefs_item = gtk.MenuItem("Set Display Preferences")
        self.prefs_item.connect("activate", self.prefs)
        self.prefs_item.show()
        self.menu.append(self.prefs_item)

        self.about_item = gtk.MenuItem("About ThinkDisp")
        self.about_item.connect("activate", self.about_popup)
        self.about_item.show()
        self.menu.append(self.about_item)
        
        self.quit_item = gtk.MenuItem("Quit Indicator")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def main(self):
        self.load_defaults() #import settings from prefs.ini
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def status_check(self, widget):
        a = subprocess.check_output(["cat", "/proc/acpi/bbswitch"])
        if "ON" in a:
            print("card is on")
            #self.popup_test("The Card is On", "Card Status")
            subprocess.call(["notify-send", 'thinkdisp', 'The Nvidia card is on'])
        elif "OFF" in a:
            print("card is off")
            #self.popup_test("The Card is Off", "Card Status")
            subprocess.call(["notify-send", 'thinkdisp', 'The Nvidia card is off'])

    def card_on(self, widget):
        p = subprocess.Popen(["sudo", "tee", "/proc/acpi/bbswitch"], stdin=subprocess.PIPE)
        p.communicate(input="ON")
        self.status_check(0)

    def card_off(self, widget):	
        p = subprocess.Popen(["sudo", "tee", "/proc/acpi/bbswitch"], stdin=subprocess.PIPE)
        p.communicate(input="OFF")
        self.status_check(0)

    def prefs(self, widget):
        self.prefs_popup()

    def popup_test(self, message_text, dialog_title):
        label = gtk.Label(message_text)
        dialog = gtk.Dialog(dialog_title,
                    None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        response = dialog.run()
        dialog.destroy()

    def prefs_popup(self):
        global SETTINGS
        label = gtk.Label("Set Preferences:                                                        ")
        dialog = gtk.Dialog("Display Preferences",
                    None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()

        label2 = gtk.Label("External Monitor Resolution")
        dialog.vbox.pack_start(label2)
        label2.show()

        #RESOLUTION combobox
        combo = gtk.combo_box_new_text()
        for res in AVAIL_RES:
            combo.append_text(res)
        try:
            combo.set_active(AVAIL_RES.index(SETTINGS["RESOLUTION"]))
        except: # in case of value_error
            combo.set_active(0)
        dialog.vbox.pack_start(combo)
        combo.show()

        label3 = gtk.Label("My external monitor is to the ________ of the thinkpad display")
        dialog.vbox.pack_start(label3)
        label3.show()

        #SIDE combobox
        sidecombo = gtk.combo_box_new_text()
        sidecombo.append_text("left")
        sidecombo.append_text("right")
        if SETTINGS["SIDE"]=="left":
            sidecombo.set_active(0)
        else:
            sidecombo.set_active(1)
        dialog.vbox.pack_start(sidecombo)
        sidecombo.show()

        #run the dialog, get user input
        response = dialog.run()
        comboresp = combo.get_active_text()
        sidecomboresp = sidecombo.get_active_text()
        SETTINGS["RESOLUTION"] = comboresp
        SETTINGS["SIDE"] = sidecomboresp
        dialog.destroy()

        #terminal output
        print("External Monitor Resolution set to: " + SETTINGS["RESOLUTION"])
        print("External Monitor is to the " + SETTINGS["SIDE"] + " of the thinkpad display")
    
    def about_popup(self, widget):
        self.about()


    def about(self):
        label = gtk.Label("Developed by Sagar Karandikar \n http://sagark.org \n http://github.com/sagark/thinkdisp")
        dialog = gtk.Dialog("About ThinkDisp:",
                    None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        response = dialog.run()
        dialog.destroy()

    
    #runs the commands to start the display using RESOLUTION and SIDE
    def start_disp(self, widget):
        subprocess.Popen(["optirun", "true"])
        time.sleep(1)
        subprocess.Popen(["xrandr", "--output", "LVDS1", "--auto", "--output", "VIRTUAL", "--mode", str(SETTINGS["RESOLUTION"]), "--"+str(SETTINGS["SIDE"])+"-of", "LVDS1"])
		#YOU MUST HAVE screenclone in /usr/bin/
        time.sleep(1)
        subprocess.Popen(["screenclone", "-d", ":8", "-x", "1"])
        self.status_check(0)

    def kill_disp(self, widget):
        subprocess.call(["gksudo", "killdisp1"])
        self.status_check(0)
        #time.sleep(3)
        #subprocess.call(["gksudo", "killdisp2"])

    def load_defaults(self):
        global SETTINGS
        beg_path = os.path.expanduser("~")
        prefs_file = file(beg_path + "/Documents/thinkdisp/prefs.ini")
        prefs_file.readline()
        defaults = eval(prefs_file.readline())
        SETTINGS = defaults

#    def save_defaults(self):


def switch_batt():
    counter = 0
    while True:
        counter += 1
        print(counter)
        print("switch")
        a = file("/proc/acpi/battery/BAT0/state")
        a.readline()
        a.readline()
        battstat = a.readline()
        if "charging" in battstat:
            print("not switching")
            #pass
        else:
            print("switching")
            ThinkDisp.kill_disp(0, 1)
        time.sleep(5)

"""def switch_batt_runner():
    counter = 0
    while True:
        counter+= 1
        print(counter)
        switch_batt()
        time.sleep(5)"""


if __name__ == "__main__":
	#ensures that bbswitch dkms module is inserted and usable
    time.sleep(5) #prevents the weird gksudo lockup
    print("the thinkdisp icon should now be in your top panel")
    print("there are currently some bugs - for example if thinkdisp crashes \n so does the xserver running the second monitor")
    #subprocess.call(["gksudo", "modprobe", "bbswitch"])
    subprocess.call(["gksudo", "start_thinkdisp"])
    #thread.start_new_thread(switch_batt, ())
    indicator = ThinkDisp()
    indicator.main()
