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
import tkinter.font as font
from tkinter import ttk
import chess
import math
from utility import *
import sys
import os
black_square_color = "#add8e6"

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

piece_pics = {
    "k" : tk.PhotoImage(file=os.path.join(base_path,"img/black_king.png")),
    "q" : tk.PhotoImage(file=os.path.join(base_path,"img/black_queen.png")),
    "r" : tk.PhotoImage(file=os.path.join(base_path,"img/black_rook.png")),
    "b" : tk.PhotoImage(file=os.path.join(base_path,"img/black_bishop.png")),
    "n" : tk.PhotoImage(file=os.path.join(base_path,"img/black_knight.png")),
    "p" : tk.PhotoImage(file=os.path.join(base_path,"img/black_pawn.png")),
    "K" : tk.PhotoImage(file=os.path.join(base_path,"img/white_king.png")),
    "Q" : tk.PhotoImage(file=os.path.join(base_path,"img/white_queen.png")),
    "R" : tk.PhotoImage(file=os.path.join(base_path,"img/white_rook.png")),
    "B" : tk.PhotoImage(file=os.path.join(base_path,"img/white_bishop.png")),
    "N" : tk.PhotoImage(file=os.path.join(base_path,"img/white_knight.png")),
    "P" : tk.PhotoImage(file=os.path.join(base_path,"img/white_pawn.png"))

}

blank_img = tk.PhotoImage(file=os.path.join(base_path,"img/black_square.png"))

class UserInterface(object):
    def __init__(self, master, queue, end_command):
        self.queue = queue
        self.selected_squares = []
        self.awaiting_move = False
        self.master = master
        self.buttons = [None]*64
        self.frm = ttk.Frame(master, padding=10)
        self.frm.grid()
        for i in range(0,8):
            self.frm.columnconfigure(i, weight=1,uniform="group")
            self.frm.rowconfigure(i, weight=1,uniform="group")

        self.tries_label = tk.Label(self.frm, text="Tries: 0", width=20)
        self.tries_label.grid(column=8, row=0)

        self.moves_label = tk.Label(self.frm, text="Moves: 0")
        self.moves_label.grid(column=8, row=1)
        
        self.output_label = tk.Label(self.frm, text="Get Ready!")
        self.output_label.grid(column=8, row=2)

        self.read_mode = tk.IntVar()
        self.read_mode_check = tk.Checkbutton(self.frm, text="Read Mode",
                                              variable=self.read_mode)
        self.read_mode_check.grid(row=3, column=8)

        self.start_button = tk.Button(self.frm, text="Start")
        self.start_button.grid(column=8, row=4, sticky='nsew', padx=20, pady=5)
        self.hint_button = tk.Button(self.frm, text = "Hint")
        self.hint_button.grid(column=8, row=5, sticky='nsew', padx=20, pady=5)

        self.library_button = tk.Button(self.frm, text="Library")
        self.library_button.grid(column=8, row=6, sticky='nsew', padx=20, pady=5)

        self.scores_button = tk.Button(self.frm, text="Scores")
        self.scores_button.grid(column=8, row=7, sticky='nsew', padx=20, pady=5)

        self.init_board_draw()
        self.draw_board(chess.Board())


        self.title_label = tk.Label(self.frm, text="No File Loaded.", width=45, padx=0, wraplength=350)
        self.title_label.grid(row=8, columnspan=8)

        self.read_label = tk.Text(self.frm, width=45, height=6, relief='ridge', font=font.nametofont("TkDefaultFont"), background=master.cget('bg'), wrap=tk.WORD,bd=1, state=tk.DISABLED)
        self.read_label.grid(row=9, column=0, columnspan=9, sticky='nsew')

        self.read_scroll = tk.Scrollbar(self.frm)
        self.read_scroll.grid(row=9, column=9, sticky='ns')

        self.read_scroll.config(command=self.read_label.yview)
        self.read_label.config(yscrollcommand=self.read_scroll.set)

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get_nowait()
                if (msg[0]=="Board"):
                    self.draw_board(msg[1])
                if (msg[0]=="Await"):
                    self.awaiting_move = msg[1]
                if (msg[0]=="Status"):
                    self.output_label.config(text=msg[1])
                if (msg[0]=="SetupHint"):
                    self.hint_button.config(command=msg[1])
                if (msg[0]=="SetupRead"):
                    self.read_button.config(command=msg[1])
                if (msg[0]=="SetupScore"):
                    self.scores_button.config(command=msg[1])
                if (msg[0]=="SetupLibrary"):
                    self.library_button.config(command=msg[1])
                if (msg[0]=="SetupStart"):
                    self.start_button.config(command=msg[1])
                if (msg[0]=="ChangeChapter"):
                    self.title_label.config(text=msg[1])
                if (msg[0]=="Try"):
                    self.tries_label.configure(text="Tries: " + str(msg[1]))
                if (msg[0]=="Move"):
                    self.moves_label.configure(text="Moves: " + str(msg[1]-1))
                if (msg[0]=="MakeMove"):
                    self.draw_move(msg[1], msg[2], msg[3])

                if (msg[0]=="SetReadText"):
                    if (self.read_mode.get()==1):
                        self.read_label.config(state=tk.NORMAL)
                        self.read_label.delete("1.0", tk.END)
                        self.read_label.insert(tk.END, msg[1])
                        self.read_label.config(state=tk.DISABLED)

                if (msg[0]=="CheckBoxState"):
                    self.read_mode_check.config(state=msg[1])
                if (msg[0]=="SelectSquare"):
                    self.buttons[msg[1]].configure(bg='#aaaa00')
                    self.selected_squares.append(msg[1])

                if (msg[0]=="DeselectSquare"):
                    row = math.floor(msg[1] / 8)
                    col = msg[1]-row*8
                    if (odd_or_even(row,col)):
                        self.buttons[msg[1]].configure(bg=black_square_color)
                    else:
                        self.buttons[msg[1]].configure(bg='#f5f5f5')
                    self.selected_squares.remove(msg[1])

                if (msg[0]=="Flip"):
                    self.flip_board(msg[1])
                    
                if (msg[0]=="Command"):
                    self.buttons[msg[1]].config(command=msg[2])
                if (msg[0]=="Cancel"):
                    self.buttons[msg[1]].bind("<Button-3>", msg[2])
            except queue.Empty:
                pass


    def init_board_draw(self):
        white = True
        for row in range(0,8):
            white = not white
            for col in range(0,8):
                if white:
                    color = '#f5f5f5'
                    white = False
                else:
                    color = black_square_color
                    white = True
                self.buttons[col+row*8] = tk.Button(self.frm, relief='flat',
                                                    bg=color, bd=0, activebackground='#ecd9BA')
                self.buttons[col+row*8].grid(column=7-col, row=row)

    def draw_board(self, board):
        for row in range(0, 8):
            for col in range(0,8):
                p = board.piece_at(col+row*8)
                
                if p is not None:
                    if (p.symbol() in piece_pics):
                        self.buttons[col+row*8].configure(image=piece_pics[p.symbol()])
                    else:
                        self.buttons[col+row*8].config(text=p.symbol())
                else:
                    self.buttons[col+row*8].configure(image=blank_img)

    def flip_board(self, player):
        if (player=="black"):
            for row in range(0,8):
                for col in range(0,8):
                    self.buttons[col+row*8].grid(column=7-col, row=row)
        if (player=="white"):
            for row in range(0,8):
                for col in range(0,8):
                    self.buttons[col+row*8].grid(column=col, row=7-row)

            

    def draw_move(self, piece, old_square, new_square):
        self.buttons[old_square].configure(image=blank_img)
        self.buttons[new_square].configure(image=piece_pics[piece])
