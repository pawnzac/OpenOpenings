import tkinter as tk, time, threading, random, queue
import os
from os.path import expanduser, exists

class ScoreWindow(object):
    def __init__(self, stats, data):
        win = tk.Toplevel()
        win.wm_title("Scores")
        self.current_rows = 0
        tk.Label(win, text="Tries per Move").grid(row=0, columnspan=len(stats)+1, sticky='nsew')
        tk.Label(win, text="File",borderwidth=2, relief='ridge').grid(row=1, column=0, sticky='nsew')
        for i in range(0, len(stats)):
            tk.Label(win, text=stats[i], borderwidth=2, relief='ridge').grid(row=1, column=i+1, sticky='nsew')

        i = 2
        for key, value in data.items():
            tk.Label(win, text=os.path.basename(os.path.dirname(key)) + "/" + os.path.basename(key), borderwidth=2, relief='ridge').grid(row=i, column=0, sticky='nsew')
            j = 1
            for s in stats:
                tk.Label(win, text=str(value[s]), borderwidth=2, relief='ridge').grid(row=i, column=j, sticky='nsew')
                j += 1
            i += 1

        tk.Button(win, text="Close", command=win.destroy).grid(row=1, column=len(stats)+2)
