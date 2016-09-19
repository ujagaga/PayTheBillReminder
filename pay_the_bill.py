#!/usr/bin/python3

from os import path, remove, system
import sys
from time import sleep, time
from tkinter import Tk, Frame, Entry, LEFT, RIGHT, BOTTOM, TOP, Label, Button, Checkbutton, PhotoImage, X


# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    current_path = path.dirname(sys.executable)
elif __file__:
    current_path = path.dirname(path.realpath(__file__))

configFileName = current_path + "/bill_list.txt"
app_title = "Pay the bills"


class BillList(Tk):
    global app_title

    def __init__(self, box_text):
        global app_title

        Tk.__init__(self)

        self.title(app_title)
        self.wm_title(app_title)
        self.minsize(300, 100)

        self.frame1 = Frame(self)
        self.frame1.pack(pady=0, padx=0, fill=X)

        Label(self.frame1, text=box_text).pack(side=TOP, padx=5)

        self.passBox = Entry(self.frame1, name="passBox", show="*")
        self.passBox.bind("<Return>", self.confirmed)
        self.passBox.pack(padx=5)
        self.passBox.focus_set()

        self.chkBoxState = False
        self.chkBox = Checkbutton(self.frame1, text="Show password", command=self.chk)
        self.chkBox.pack()

        Button(self.frame1, text="OK", command=self.ok, width=4).pack(side=RIGHT, padx=5, pady=5)
        Button(self.frame1, text="Cancel", command=self.cancel, width=4).pack(side=LEFT, padx=5, pady=5)

        self.password = ""

    def ok(self, event=None):
        self.password = self.passBox.get()
        self.wm_withdraw()
        self.quit()

    def confirmed(self, event):
        self.password = self.passBox.get()
        self.wm_withdraw()
        self.quit()

    def cancel(self, event=None):
        self.password = ""
        self.wm_withdraw()
        self.quit()

    def chk(self, event=None):
        self.chkBoxState = not self.chkBoxState

        if self.chkBoxState:
            self.chkBox.select()
            self.passBox.config(show="")
        else:
            self.chkBox.deselect()
            self.passBox.config(show="*")


class InfoBox(Tk):
    global app_title

    def __init__(self, box_text):
        global app_title
        Tk.__init__(self)

        self.title(app_title)
        self.wm_title(app_title)
        self.minsize(300, 50)

        self.frame1 = Frame(self)
        self.frame1.pack(pady=0, padx=0, fill=X)

        Label(self.frame1, text=box_text, justify=LEFT).pack(padx=5)

        Button(self.frame1, text="Dismiss", command=self.dismiss, width=10).pack(side=BOTTOM, padx=5, pady=5)

    def dismiss(self, event=None):
        self.wm_withdraw()
        self.quit()


def setup():
    print("Setup")
    try:
        # write config file
        config_file = open(configFileName, 'w')
        config_file.write("# List the names of your bills here.\n")
        config_file.write("# Each new line after this comment represents a new bill to be paid each month.\n")
        config_file.close()
    except EnvironmentError as e:
        InfoBox("Error: " + e)
        sys.exit()


# read config
if not path.exists(configFileName):
    setup()


# reading the contents of the config file
f = open(configFileName, 'r')
content = f.read().splitlines()
f.close()

for lineIdx in range(0, len(content)):
    if content[lineIdx].startswith('#'):
        continue

    # line = content[lineIdx].split('=')
    # if line[0] == "hostName":
    #     if len(line) > 1:
    #         host = line[1].split('#')[0].strip()
    #     else:
    #         host = gethostname()
    #
    # if line[0] == "hostPassword":
    #     if len(line) > 1:
    #         password = line[1].split('#')[0].strip()
    #     else:
    #         password = ""