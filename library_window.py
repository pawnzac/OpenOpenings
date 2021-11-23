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

    def make_select_book(self):
        def com():
            self.book_select = self.listbox.get(self.listbox.curselection())
            self.current_book = self.book_select
            self.win.destroy()
            self.win = tk.Toplevel()
            self.win.wm_title("Library")

            tk.Button(self.win, text="Next", command=self.make_select_final()).pack(side=tk.TOP)

            scrollbar = tk.Scrollbar(self.win)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.listbox = tk.Listbox(self.win, yscrollcommand=scrollbar.set)
            self.listbox.pack(side=tk.LEFT)

            scrollbar.config(command=self.listbox.yview)
        
            for (key, value) in self.library[self.book_select].items():
                self.listbox.insert(tk.END, key)

        return com

    def make_select_final(self):
        def com():
            chapter = self.listbox.get(self.listbox.curselection())
            self.win.destroy()
            self.current_pgn = self.library[self.book_select][chapter]["pgn"]
            self.current_color = self.library[self.book_select][chapter]["color"]
            self.current_chapter = chapter
            self.queue.put("Library")
        return com
    
    def open_window(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Library")

        tk.Button(self.win, text="Next", command=self.make_select_book()).pack(side=tk.TOP)

        scrollbar = tk.Scrollbar(self.win)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.win, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT)

        scrollbar.config(command=self.listbox.yview)
        
        for (key, value) in self.library.items():
            self.listbox.insert(tk.END, key)
        

        

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
