#!/usr/bin/python3

from os import path, rename, remove, system
import sys
from datetime import date
from tkinter import Tk, Frame, Entry, LEFT, RIGHT, BOTTOM, TOP, Label, Button, Checkbutton, X, IntVar, RIDGE, scrolledtext, WORD, INSERT, END, Toplevel


# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    current_path = path.dirname(sys.executable)
elif __file__:
    current_path = path.dirname(path.realpath(__file__))

configFileName = current_path + '/bill_list.txt'
app_title = 'Pay the bills'
unpaid_bills_label_text = 'Unpaid bills:'
paid_bills_label_text = 'Paid bills:'
add_bill_label_text = 'Add new bill:'
bill_list_label_text = 'List of monthly paid bills:'
paid_dict = {}
unpaid_dict = {}
current_date = date.today()


def check_bills_file():
    global configFileName
    global paid_dict
    global unpaid_dict

    paid_dict = {}
    unpaid_dict = {}

    # reading the contents of the config file
    bills_file = open(configFileName, 'r')
    content = bills_file.read().splitlines()
    bills_file.close()

    for line in content:
        if line.startswith('#') or len(line) < 2:
            continue

        data = line.split("|")

        bill_name = data[0]

        if len(data) > 1:
            date_paid = data[1]
            month_paid = int(date_paid.split('.')[0], 10)

            if month_paid == current_date.month:
                paid_dict[line] = 0
            else:
                # this was paid some other month so archive
                return False
        else:
            unpaid_dict[bill_name] = 0

    return True


def mark_as_payed(bill_name):
    global current_date

    # reading the contents of the config file
    bills_file = open(configFileName, 'r')
    content = bills_file.read().splitlines()
    bills_file.close()

    config_file = open(configFileName, 'w')

    for i in range(0, len(content)):
        if content[i] == bill_name:
            content[i] += '|' + '%d' % current_date.month + '.%d' % current_date.day

        config_file.write(content[i] + '\n')

    config_file.close()


def mark_as_unpayed(bill_name):
    # reading the contents of the config file
    bills_file = open(configFileName, 'r')
    content = bills_file.read().splitlines()
    bills_file.close()

    config_file = open(configFileName, 'w')

    for i in range(0, len(content)):
        if content[i] == bill_name:
            content[i] = content[i].split('|')[0]

        config_file.write(content[i] + '\n')

    config_file.close()


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


class SetupDialog(Tk):
    global app_title
    global paid_dict
    global unpaid_dict
    global configFileName
    global current_date

    def __init__(self):
        global app_title

        Tk.__init__(self)

        self.grab_set()

        self.title(app_title)
        self.wm_title(app_title)
        self.minsize(300, 100)

        self.frame_bill_list = None
        self.frame_add = None
        self.frame_dialog = None
        self.addBillBox = None
        self.billListBox = None

        self.content = []

        # reading the contents of the config file
        bills_file = open(configFileName, 'r')
        self.content = bills_file.read().splitlines()
        bills_file.close()

        self.populate()

    def populate(self):
        if self.frame_bill_list is not None:
            self.frame_bill_list.destroy()

        if self.frame_add is not None:
            self.frame_add.destroy()

        if self.frame_dialog is not None:
            self.frame_dialog.destroy()

        self.frame_bill_list = Frame(self)
        self.frame_bill_list.pack(pady=0, padx=0, fill=X)
        self.frame_add = Frame(self)
        self.frame_add.pack(pady=0, padx=0, fill=X)
        self.frame_dialog = Frame(self)
        self.frame_dialog.pack(pady=0, padx=0, fill=X)

        Label(self.frame_bill_list, text=bill_list_label_text).pack(side=TOP, padx=5, pady=10)

        self.billListBox = scrolledtext.ScrolledText(master=self.frame_bill_list, wrap=WORD, height=10)
        self.billListBox.pack(pady=0, padx=0, fill=X)

        for j in range(0, len(self.content)):
            data = self.content[j]

            bill_string = data.split('|')[0]
            self.billListBox.insert(INSERT, bill_string + '\n')

        Button(self.frame_dialog, text='SAVE', command=self.save, width=4).pack(side=LEFT, padx=5, pady=5)
        Button(self.frame_dialog, text='CANCEL', command=self.cancel, width=4).pack(side=RIGHT, padx=5, pady=5)

    def save(self, event=None):
        # write config file
        config_file = open(configFileName, 'w')
        current_text = self.billListBox.get(0.0, END).splitlines()

        # Write data which has not changed
        for original_idx in range(0, len(self.content)):
            for edited_idx in range(len(current_text)-1, -1, -1):
                if self.content[original_idx].split('|')[0] == current_text[edited_idx]:
                    config_file.write(self.content[original_idx] + '\n')
                    current_text.pop(edited_idx)
                    break
        # write data that is added (now leftover)
        for edited_idx in range(0, len(current_text)):
            config_file.write(current_text[edited_idx] + '\n')

        config_file.close()

        check_bills_file()
        self.wm_withdraw()

    def cancel(self, event=None):
        self.wm_withdraw()


class BillList(Tk):
    global app_title
    global paid_dict
    global unpaid_dict
    global configFileName
    global current_date

    def __init__(self):
        global app_title

        Tk.__init__(self)

        self.title(app_title)
        self.wm_title(app_title)
        self.minsize(300, 100)

        self.frame_unpaid = None
        self.frame_paid = None
        self.frame_add = None
        self.frame_dialog = None
        self.addBillBox = None
        self.populate()

    def populate(self):
        print("populating")
        if self.frame_unpaid is not None:
            self.frame_unpaid.destroy()

        if self.frame_paid is not None:
            self.frame_paid.destroy()

        if self.frame_add is not None:
            self.frame_add.destroy()

        if self.frame_dialog is not None:
            self.frame_dialog.destroy()

        if self.addBillBox is not None:
            self.addBillBox.destroy()

        self.frame_unpaid = Frame(self, relief=RIDGE, borderwidth=2)
        self.frame_unpaid.pack(pady=0, padx=0, fill=X)
        self.frame_paid = Frame(self, relief=RIDGE, borderwidth=2)
        self.frame_paid.pack(pady=0, padx=0, fill=X)
        self.frame_dialog = Frame(self)
        self.frame_dialog.pack(pady=0, padx=0, fill=X)

        Label(self.frame_unpaid, text=unpaid_bills_label_text).pack(side=TOP, padx=5, pady=10)

        for bill_string in unpaid_dict:
            local_frame = Frame(self.frame_unpaid)
            local_frame.pack(pady=0, padx=0, fill=X)
            unpaid_dict[bill_string] = IntVar()
            Label(local_frame, text=bill_string).pack(side=LEFT, padx=5)
            c = Checkbutton(local_frame, text='', variable=unpaid_dict[bill_string], command=self.chk)
            c.pack(side=RIGHT)

        Label(self.frame_paid, text=paid_bills_label_text).pack(side=TOP, padx=5, pady=10)

        for data in paid_dict:
            bill_data = data.split('|')
            bill_string = bill_data[0]
            if len(bill_data) > 1:
                bill_date = bill_data[1].split('.')
                if len(bill_date) > 1:
                    bill_string += '(' + bill_date[1] + '.' + bill_date[0] + ')'
                else:
                    bill_string += '(xx.' + bill_date[0] + ')'

            local_frame = Frame(self.frame_paid)
            local_frame.pack(pady=0, padx=0, fill=X)
            paid_dict[data] = IntVar()
            Label(local_frame, text=bill_string).pack(side=LEFT, padx=5)
            c = Checkbutton(local_frame, text='', variable=paid_dict[data], command=self.unchk)
            c.pack(side=RIGHT)
            c.select()

        Button(self.frame_dialog, text='SETUP', command=self.setup, width=4).pack(side=RIGHT, padx=5, pady=5)

        Button(self.frame_dialog, text='DISMISS', command=self.dismiss, width=4).pack(side=LEFT, padx=5, pady=5)

    def setup(self, event=None):
        setup_box = SetupDialog()
        self.populate()

    def dismiss(self, event=None):
        self.wm_withdraw()
        self.quit()

    def chk(self, event=None):
        for data in unpaid_dict:
            if unpaid_dict[data].get() == 1:
                # move to paid dict
                key = data + '|' + '%d' % current_date.month + '.%d' % current_date.day
                paid_dict[key] = 0
                unpaid_dict.pop(data)
                mark_as_payed(data)
                break

        self.populate()

    def unchk(self, event=None):
        for data in paid_dict:
            if paid_dict[data].get() == 0:
                # move to unpaid dict
                unpaid_dict[data.split('|')[0]] = 0
                paid_dict.pop(data)
                mark_as_unpayed(data)
                break

        self.populate()


def setup():
    global configFileName
    try:
        # write config file
        config_file = open(configFileName, 'w')
        config_file.write("# List the names of your bills here.\n")
        config_file.write("# Each new line after this comment represents a new bill to be paid each month.\n")
        config_file.close()
    except EnvironmentError as e:
        InfoBox("Error: " + e)
        sys.exit()


def archive_current_list():
    global configFileName

    # reading the contents of the config file
    bills_file = open(configFileName, 'r')
    content = bills_file.read().splitlines()
    bills_file.close()

    first_paid_month = 12

    for line in content:
        if line.startswith('#'):
            continue

        data = line.split("|")

        if len(data) > 1:
            date_paid = data[1]
            month_paid = int(date_paid.split('.')[0], 10)

            if month_paid < first_paid_month:
                first_paid_month = month_paid

    try:
        rename(configFileName, "archive_%d.txt" % first_paid_month)
        # write config file
        config_file = open(configFileName, 'w')
        for new_lines in content:
            config_file.write(new_lines.split('|')[0] + '\n')
        config_file.close()

    except EnvironmentError as e:
        InfoBox("Error: " + e)
        sys.exit()


# read config
if not path.exists(configFileName):
    setup()

if check_bills_file():
    box = BillList()
    box.mainloop()
else:
    archive_current_list()
    if check_bills_file():
        box = BillList()
        box.mainloop()
    else:
        InfoBox('An unknown error has occurred while parsing the bills list file. Please remove it and reconfigure.')
