import urllib.request, urllib.parse, urllib.error
import json
import ssl
from shutil import move
import move_files
from move_files import source_folder
import tkinter as tk
from functools import partial


def daf_yomi():
    '''
    gets daf yomi from Sefaria
    :return: str: today's daf yomi
    '''
    url = 'http://www.sefaria.org/api/calendars'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    try:
        js = json.loads(data)
    except:
        js = None

    page = js['calendar_items'][2]['ref'][:-1]

    return page


class Entry_Box(tk.Frame):
    '''
    GUI object.
    includes 2 parts:
    1) confirmation: shows today's daf yomi and asks if it is wanted file name
    has 2 buttons: yes closes GUI, no goes to second part

    2) change: has entry box and ok button.
    '''
    string = ''

    def __init__(self, master=None):
        Entry_Box.string = daf_yomi()
        self.root = master
        self.root.title("Confirmation")
        self.root.minsize(150, 50)
        tk.Frame.__init__(self, self.root)
        self.pack(side="bottom")
        # self.master = master


    def confirmation(self):
        self.label = tk.Label(self, text = Entry_Box.string +". Confirm?")
        self.label.pack(side="top")
        self.yes_button = tk.Button(self, text='Yes', command=partial(self.yes, None))
        self.no_button = tk.Button(self, text='No', command=partial(self.no, None))
        self.yes_button.pack(side = "left")
        self.no_button.pack(side = "right")
        self.root.bind('<Return>', self.yes)
        self.root.mainloop()


    def yes(self,event):
        self.destroy()
        self.root.destroy()

    def no(self,event):
        self.label.destroy()
        self.yes_button.destroy()
        self.no_button.destroy()
        self.change()

    def change(self):
        self.text = tk.Entry(self)
        self.ok_button = tk.Button(self, text='OK', command=partial(self.ok, None))
        self.text.pack(side="left")
        self.ok_button.pack(side="left")
        self.root.bind('<Return>', self.ok)

    def ok(self, event):
        Entry_Box.string = self.text.get()
        self.destroy()
        self.root.destroy()


def elis_sivug(func, GUI):  # decorator for sivug function
    '''

    :param func: sivug function (move_files.py)
    :param GUI: tkinter frame. needed to be here so we can run GUI functions.
    might not need to be here. maybe functions should be static, not needing Entry_Box object.

    :return: str: destinanion folder, or in case of WhatsApp audio - destinaion filename (whole path).
    '''
    def wrapper(*args, **kwargs):
        dest_file = func(*args, **kwargs)
        if args[0].endswith('.ogg') and args[0].startswith('WhatsApp'):
            GUI.confirmation()
            GUI.root.mainloop()
            daf = Entry_Box.string  # getting todays page from sefaria
            return  dest_file + '\\' + daf + '.ogg'  # renaming file. should add confirmation GUI
        else:
            return dest_file
    GUI.root.quit()
    return wrapper



def move_file(src, filename): # new function to use decorated sivug
    root = tk.Tk()
    root.title("Confirmation")
    root.minsize(150, 50)
    a = Entry_Box(root)
    sivug = elis_sivug(move_files.sivug, a)  # decorating the sivug function
    dest = sivug(filename)
    if dest != source_folder:
        move(src + '\\' + filename, dest)





