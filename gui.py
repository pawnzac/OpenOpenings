import tkinter as tk, time, threading, random, queue
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

        self.scores_button = tk.Button(self.frm, text="Scores")
        self.scores_button.grid(column=8, row=4)

        self.init_board_draw()
        self.draw_board(chess.Board())

        self.hint_button = tk.Button(self.frm, text = "Hint")
        self.hint_button.grid(column=8, row=5)

        self.open_button = tk.Button(self.frm, text = "Open")
        self.open_button.grid(column=8, row=6)


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
                if (msg[0]=="SetupOpen"):
                    self.open_button.config(command=msg[1])
                if (msg[0]=="SetupScore"):
                    self.scores_button.config(command=msg[1])
                if (msg[0]=="Try"):
                    self.tries_label.configure(text="Tries: " + str(msg[1]))
                if (msg[0]=="Move"):
                    self.moves_label.configure(text="Moves: " + str(msg[1]-1))
                if (msg[0]=="MakeMove"):
                    self.draw_move(msg[1], msg[2], msg[3])

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
                self.buttons[col+row*8] = tk.Button(self.frm, relief='flat', bg=color, bd=0, activebackground='#ecd9BA')
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
