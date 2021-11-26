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
from tkinter import ttk

class LibraryWindow(object):
    def __init__(self, library_file, queue, add_func):
        self.library = None
        self.queue = queue
        self.add_func = add_func
        if library_file is not None:
            self.load_library(library_file)
        else:
            self.library = {}

        self.lib_file = library_file

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

    def select_window(self, commands, elements):
        if (self.win is not None):
            self.win.destroy()

        self.win = tk.Toplevel()
        self.win.wm_title("Library")
        self.frame = ttk.Frame(self.win, padding=10)
        self.frame.grid()

        i = 0
        for (name, cmd) in commands.items():
            tk.Button(self.frame, text=name, command=cmd).grid(row=0, column=i, sticky="nsew")
            i += 1

        scrollbar = tk.Scrollbar(self.frame)
        scrollbar.grid(row=1, column=i, stick="nsew")

        self.listbox = tk.Listbox(self.frame, yscrollcommand=scrollbar.set, width=65, height=20)
        self.listbox.grid(row=1, column=0, columnspan=i, sticky="nsew")

        scrollbar.config(command=self.listbox.yview)
        minw = 65
        for (key, value) in elements.items():
            minw = len(key) if len(key) > minw else minw
            self.listbox.insert(tk.END, key)

        self.listbox.config(width=minw)
        
        

    def make_select_book(self):
        def com():
            self.book_select = self.listbox.get(self.listbox.curselection())
            self.current_book = self.book_select

            self.select_window({
                "Select" : self.make_select_final(),
                "Rename" : self.make_rename()
            }, self.library[self.book_select])
            

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

        self.select_window({
            "Select" : self.make_select_book(),
            "Add to Library" : self.add_func,
            "Rename" : self.make_rename_book()
        }, self.library)
        

    def make_rename(self):
        def com():
            chapter = self.listbox.get(self.listbox.curselection())
            newname = ""
            while (newname==""):
                newname = tk.simpledialog.askstring("New name", "Rename " + chapter + " to what?")
            
            self.library[self.current_book][newname] = self.library[self.current_book].pop(chapter)
            self.write(self, self.lib_file)
            self.select_window({
                "Select" : self.make_select_final(),
                "Rename" : self.make_rename()
            }, self.library[self.book_select])

        return com

    def make_rename_book(self):
        def com():
            book = self.listbox.get(self.listbox.curselection())
            newname = ""
            while (newname==""):
                newname = tk.simpledialog.askstring("New name", "Rename " + book + " to what?")
            
            self.library[newname] = self.library.pop(book)
            self.write(self.lib_file)
            self.open_window()

        return com
    


    def rename(self, book0, chapter0, book1, chapter1):
        if (book1 not in self.library):
            self.library[book1] = {}
        
        self.library[book1][chapter1] = self.library[book0].pop(chapter0)

        
        
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
