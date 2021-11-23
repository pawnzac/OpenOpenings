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
import json

class LibraryWindow(object):
    def __init__(self, library_file, queue):
        self.library = None
        self.queue = queue
        if library_file is not None:
            self.load_library(library_file)
        else:
            self.library = {}

        self.select_book = -1
        self.win = None
        self.current_pgn = None
        self.current_color = None
        self.current_chapter = None
        self.current_book = None
        
    def load_library(self, file_name):
        with open(file_name, 'r') as f:
            self.library = json.load(f)

    def add_to_library(self, name, pgn, book, color):

        if (book not in self.library):
            self.library[book] = {}
            
        self.library[book][name] =  { "pgn" : pgn,
                                      "color" : color,
                                      "sessions" : []
                                     }

    def get_current_pgn(self):
        return self.current_pgn

    def get_color(self):
        return self.current_color
    
    def get_pgn(self, book, name):
        return self.library[book][name]

    def make_select_book(self, var):
        def com():
            self.book_select = var.get()
            self.win.destroy()
            self.win = tk.Toplevel()
            self.win.wm_title("Library")
            sel = tk.StringVar(self.win, "0")
            for key in self.library[self.book_select].keys():
                tk.Radiobutton(self.win, text=key, variable=sel, value=key).pack(side=tk.TOP, ipady=5)
            tk.Button(self.win, text="Next", command=self.make_select_final(sel)).pack(side=tk.TOP, ipady=5)
            self.current_book = self.book_select
        return com

    def make_select_final(self, var):
        def com():
            chapter = var.get()
            self.win.destroy()
            self.current_pgn = self.library[self.book_select][chapter]["pgn"]
            self.current_color = self.library[self.book_select][chapter]["color"]
            self.current_chapter = chapter
            self.queue.put("Library")
        return com
    
    def open_window(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Library")

        sel = tk.StringVar(self.win, "0")

        for (key, value) in self.library.items():
            tk.Radiobutton(self.win, text=key, variable=sel,
                           value=key).pack(side=tk.TOP, ipady=5)


        tk.Button(self.win, text="Next", command=self.make_select_book(sel)).pack(side=tk.TOP, ipady=5)
        

    def write(self, lib_file):
        with open(lib_file,'w') as f:
            json.dump(self.library, f)

    def get_sessions(self):
        return self.library[self.current_book][self.current_chapter]["sessions"]
    
    def add_session(self, tries, moves, time):
        toadd = {"tries" : tries,
                 "moves" : moves,
                 "time" : time}
        if ("sessions" in self.library[self.current_book][self.current_chapter]):
            self.library[self.current_book][self.current_chapter]["sessions"].append(toadd)
        else:
            self.library[self.current_book][self.current_chapter]["sessions"] = [toadd]
