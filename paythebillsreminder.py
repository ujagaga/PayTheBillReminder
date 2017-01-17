#!/usr/bin/python3

from os import path, rename, system, getenv, makedirs
import sys
from datetime import date
from tkinter import Tk, Frame, LEFT, RIGHT, BOTTOM, TOP, Label, Button, Checkbutton, X, IntVar, RIDGE, PhotoImage
from webbrowser import open as sys_file_open

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    current_path = path.dirname(sys.executable)
elif __file__:
    current_path = path.dirname(path.realpath(__file__))

configFileLocation = path.expanduser("~") + '/.paythebillsreminder'
makedirs(configFileLocation, exist_ok=True)

configFileName = configFileLocation + '/bill_list.txt'
icon_path = current_path + '/icon.gif'
app_title = 'Pay the bills'
unpaid_bills_label_text = 'Unpaid bills:'
paid_bills_label_text = 'Paid bills:'
add_bill_label_text = 'Add new bill:'
bill_list_label_text = 'List of monthly paid bills:'
checkbox_text = 'Payed'
paid_dict = {}
unpaid_dict = {}
current_date = date.today()
alert_date = 0


def check_bills_file():
    global configFileName
    global paid_dict
    global unpaid_dict
    global alert_date

    paid_dict = {}
    unpaid_dict = {}

    # reading the contents of the config file
    bills_file = open(configFileName, 'r', encoding="utf-8")
    content = bills_file.read().splitlines()
    bills_file.close()

    for row in range(0, len(content)):
        line = content[row]
    # for line in content:
        if line.startswith('#') or len(line) < 2:
            continue

        if alert_date == 0:
            if len(line) < 3:
                temp = int(line, 10)
                if (temp > 1) and (temp < 28):
                    alert_date = temp
                    continue

        data = line.split("|")

        bill_name = data[0]

        if len(data) > 1:
            date_paid = data[1]
            month_paid = int(date_paid.split('.')[0], 10)

            if month_paid == current_date.month:
                paid_dict[str(row) + '|' + line] = 0
            else:
                # this was paid some other month so archive
                return False
        else:
            unpaid_dict[str(row) + '|' + bill_name] = 0

    if alert_date == 0:
        alert_date = 19

        config_file = open(configFileName, 'w', encoding="utf-8")
        config_file.write('%d\n' % alert_date)

        for new_lines in content:
            config_file.write(new_lines + '\n')
        config_file.close()

    return True


def mark_as_payed(bill_name):
    global current_date

    # reading the contents of the config file
    bills_file = open(configFileName, 'r', encoding="utf-8")
    content = bills_file.read().splitlines()
    bills_file.close()

    config_file = open(configFileName, 'w', encoding="utf-8")

    for i in range(0, len(content)):
        if content[i] == bill_name:
            content[i] += '|' + '%d' % current_date.month + '.%d' % current_date.day

        config_file.write(content[i] + '\n')

    config_file.close()


def mark_as_unpayed(bill_name):
    # reading the contents of the config file
    bills_file = open(configFileName, 'r', encoding="utf-8")
    content = bills_file.read().splitlines()
    bills_file.close()

    config_file = open(configFileName, 'w', encoding="utf-8")

    for i in range(0, len(content)):
        if content[i] == bill_name:
            content[i] = content[i].split('|')[0]

        config_file.write(content[i] + '\n')

    config_file.close()


class InfoBox(Tk):
    global app_title
    global icon_path

    def __init__(self, box_text):

        Tk.__init__(self)

        self.wm_iconphoto(True, PhotoImage(file=icon_path))
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


class BillList(Tk):
    global app_title
    global paid_dict
    global unpaid_dict
    global configFileName
    global current_date
    global icon_path

    def __init__(self):
        global app_title

        Tk.__init__(self)

        self.wm_iconphoto(True, PhotoImage(file=icon_path))
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
            c = Checkbutton(local_frame, text=checkbox_text, variable=unpaid_dict[bill_string], command=self.chk)
            c.pack(side=RIGHT)

        Label(self.frame_paid, text=paid_bills_label_text).pack(side=TOP, padx=5, pady=10)

        paid_dict = sorted(paid_dict)
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
            c = Checkbutton(local_frame, text=checkbox_text, variable=paid_dict[data], command=self.unchk)
            c.pack(side=RIGHT)
            c.select()

        Button(self.frame_dialog, text='CONFIGURE', command=self.setup, width=9).pack(side=RIGHT, padx=5, pady=5)

        Button(self.frame_dialog, text='DISMISS', command=self.dismiss, width=9).pack(side=LEFT, padx=5, pady=5)

    def setup(self, event=None):
        editor = getenv('EDITOR')
        if editor:
            system(editor + ' ' + configFileName)
        else:
            sys_file_open(configFileName)
        self.wm_withdraw()
        self.quit()

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

    eng_string = "# English:\n"
    eng_string += "# The first non comment line is the day of the month when this app will display notification.\n"
    eng_string += "# Each new line after this comment represents a new bill to be paid each month.\n"
    eng_string += "# Paid bills will have a date next to it.\n"

    rs_string = "# Srpski:\n"
    rs_string += "# Prva nekomentarisana linija pretstavlja datum kad će ova aplikacija da prikaže obaveštenje.\n"
    rs_string += "# Svaka nova linija posle ovog komentara pretstavlja nov račun koji treba da se plati svakog meseca.\n"
    rs_string += "# Plaćeni računi imaju pored sebe datum.\n"

    try:
        # write config file
        config_file = open(configFileName, 'w', encoding="utf-8")
        config_file.write("19\n")
        config_file.write(eng_string)
        config_file.write(rs_string)
        config_file.write("bill_1\n")
        config_file.write("bill_2\n")
        config_file.close()
    except EnvironmentError as e:
        InfoBox("Error: " + e)
        sys.exit()


def archive_current_list():
    global configFileName
    global alert_date

    # reading the contents of the config file
    bills_file = open(configFileName, 'r', encoding="utf-8")
    content = bills_file.read().splitlines()
    bills_file.close()

    first_paid_month = 12

    for line in content:
        if line.startswith('#'):
            continue

        if alert_date == 0:
            if len(line) < 3:
                temp = int(line, 10)
                if (temp > 1) and (temp < 28):
                    alert_date = temp
                    continue

        data = line.split("|")

        if len(data) > 1:
            date_paid = data[1]
            month_paid = int(date_paid.split('.')[0], 10)

            if month_paid < first_paid_month:
                first_paid_month = month_paid

    try:
        rename(configFileName, configFileLocation + "/archive_%d.txt" % first_paid_month)
        # write config file
        config_file = open(configFileName, 'w', encoding="utf-8")

        if alert_date == 0:
            alert_date = 19
            config_file.write('%d\n' % alert_date)

        for new_lines in content:
            config_file.write(new_lines.split('|')[0] + '\n')
        config_file.close()

    except EnvironmentError as e:
        InfoBox("Error: " + e)
        sys.exit()


def show_dialog():
    global current_path
    global icon_path

    box = BillList()
    box.mainloop()


# read config
if not path.exists(configFileName):
    setup()


if not check_bills_file():
    archive_current_list()
    if not check_bills_file():
        info = InfoBox('An unknown error has occurred while parsing the bills list file. ' +
                       'Please remove it and reconfigure.')
        info.mainloop()
        sys.exit()

if alert_date == 0:
    alert_date = 19

if len(sys.argv) > 1:
    if current_date.day < alert_date:
        sys.exit()
    else:
        if len(unpaid_dict) > 0:
            show_dialog()
else:
    show_dialog()


