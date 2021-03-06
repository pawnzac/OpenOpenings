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


import tkinter as tk
from tkinter import ttk
import chess

class ImportWindow(object):
    def __init__(self, after):
        self.win = tk.Toplevel(class_="OpenOpenings")
        self.win.wm_title("Import")

        self.frame = ttk.Frame(self.win, padding=10)
        self.frame.grid()

        self.color_var = tk.IntVar()

        self.color_label = tk.Label(self.frame,
                                    text="Color to Play")
        self.color_label.grid(row=0, column=0, columnspan=2)
        
        self.white_button = tk.Radiobutton(self.frame,
                                           text="White",
                                           variable=self.color_var,
                                           value=chess.WHITE)
        self.white_button.grid(row=1, column=0)

        self.black_button = tk.Radiobutton(self.frame,
                                           text="Black",
                                           variable=self.color_var,
                                           value=chess.BLACK)
        self.black_button.grid(row=1, column=1)


        self.book_label = tk.Label(self.frame, text="Book")
        self.book_label.grid(row=2, column=0, columnspan=2)

        self.book = tk.StringVar()
        self.book_entry = tk.Entry(self.frame, textvariable=self.book)
        self.book_entry.grid(row=3, column=0, columnspan=2)

        self.tag_label = tk.Label(self.frame, text="Tag to Use for Chapter Titles")
        self.tag_label.grid(row=4, column=0, columnspan=2)

        self.tag = tk.StringVar()
        self.tag_entry = tk.Entry(self.frame, textvariable=self.tag)
        self.tag_entry.grid(row=5, column=0, columnspan=2)

        self.tag.set("Event")

        self.ok_button = tk.Button(self.frame, text="OK", command=self.ok_command)
        self.ok_button.grid(row=6, column=0, sticky="nsew")

        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.cancel_command)
        self.cancel_button.grid(row=6, column=1, sticky="nsew")
        
        self.after = after
    
    def ok_command(self):
        color = "white" if self.color_var.get()==chess.WHITE else "black"
        self.after(color, self.book.get(), self.tag.get())
        self.win.destroy()
        
        
    def cancel_command(self):
        self.win.destroy()
        
