# OpenOpenings
# Copyright 2021 pawnzac <pawnzac90@gmail.com>

# This file is part of OpenOpenings.

# OpenOpenings is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# OpenOpenings is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with OpenOpenings.  If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk, time, threading, random, queue
import os
from os.path import expanduser, exists

class ScoreWindow(object):
    def __init__(self, stats, data):
        win = tk.Toplevel()
        win.wm_title("Scores")
        self.current_rows = 0
        tk.Label(win, text="Moves Per Try [0-100%]").grid(row=0, columnspan=len(stats)+1, sticky='nsew')
        tk.Label(win, text="Chapter",borderwidth=2, relief='ridge').grid(row=1, column=0, sticky='nsew')
        for i in range(0, len(stats)):
            tk.Label(win, text=stats[i], borderwidth=2, relief='ridge').grid(row=1, column=i+1, sticky='nsew')

        i = 2
        for key, value in data.items():
            tk.Label(win, text=key, borderwidth=2, relief='ridge').grid(row=i, column=0, sticky='nsew')
            j = 1
            for s in stats:
                tk.Label(win, text=str(value[s]), borderwidth=2, relief='ridge').grid(row=i, column=j, sticky='nsew')
                j += 1
            i += 1

        tk.Button(win, text="Close", command=win.destroy).grid(row=1, column=len(stats)+2)
