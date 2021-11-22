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
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import os
from os.path import expanduser, exists
from score_window import ScoreWindow
import time
import chess
import chess.pgn
import json
from gui import UserInterface
from utility import *
class OpenOpenings(object):
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()

        self.internal_queue = queue.Queue()
        self.gui = UserInterface(master, self.queue, self.end_application)
        self.running = True
        self.node = None
        self.board = None
        self.need_to_update_board = True
        self.player = None
        self.done = True
        self.tries = 0
        self.moves = 0
        
        self.var_num = 0
        self.var_node = None
        self.backup_board = None
        
        self.current = None
        self.hint_level = 0
        self.variation = None
        self.modifying = False
        self.score_file = expanduser("~") + "/.pracchess.json"
        self.set_command()
        self.set_hint()
        self.set_open()
        self.set_cancel()
        self.set_score()
        self.move_list = []
        self.awaiting_move = False
        self.thread1 = threading.Thread(target=self.worker_thread1)
        self.thread1.start()
        self.periodic_call()

    def cancel_moves(self, event):
        for sq in self.move_list:
            self.move_list.remove(sq)
            self.queue.put(["DeselectSquare", sq])

    def make_command(self, square):
        def com():
            if (self.awaiting_move):
                self.move_list.append(square)
                if (len(self.move_list)==1):
                    self.queue.put(["SelectSquare", square])
                if (len(self.move_list)==2):
                    try:
                        mv = self.board.find_move(self.move_list[0],
                                                  self.move_list[1])
                        self.tries = self.tries + 1
                        self.queue.put(["Try", self.tries])
                        if (self.board.san(mv)==self.node.san()):
                            self.queue.put(["Status", "Correct!"])

                            self.send_make_move(mv)
                            self.board.push(mv)
                            self.awaiting_move = False
                            self.need_to_update_board = True
                            self.hint_level = 0
                            
                            if (len(self.node.variations)>1):
                                self.backup_board = self.board.copy()
                                self.var_node = self.node
                                if (self.var_num==0):
                                    self.var_num = 1
                                self.node = self.node.variations[self.var_num]
                            elif ((self.var_num != 0) & (self.node.next() is None)):
                                if (len(self.var_node.variations) <= (self.var_num+1)):
                                    self.var_num = 0
                                    self.node = self.var_node.variations[0]
                                else:
                                    self.var_num += 1
                                    self.node = self.var_node.variations[self.var_num]
                                self.board = self.backup_board.copy()
                                self.queue.put(["Board",self.board])
                            else:
                                self.node = self.node.next()

                            if ((self.node is None) & (self.var_num==0)):
                                self.queue.put(["Status", "Done!"])
                                self.write_score()
                        else:
                            self.queue.put(["Status", "Incorrect."])

                    except ValueError as e:
                        self.queue.put(["Status", "Invalid Move."])

                    self.queue.put(["DeselectSquare", self.move_list[0]])
                    self.move_list = []
                    self.internal_queue.put("Continue")

        return com

    def make_hint(self):
        def com():
            if self.node is None:
                return
            p = self.board.piece_at(self.node.move.from_square)
            fsq = chess.SQUARE_NAMES[self.node.move.from_square]
            tsq = chess.SQUARE_NAMES[self.node.move.to_square]
            if self.hint_level==0:
                self.queue.put(["Status", "Hint: " + p.symbol()])
                self.hint_level = self.hint_level+1
            elif self.hint_level==1:
                self.queue.put(["Status", "Hint: " + fsq])
                self.hint_level = self.hint_level+1
            elif self.hint_level==2:
                self.queue.put(["Status", "Hint: " + fsq + "->" + tsq])

            self.tries += 5
            self.queue.put(["Try", self.tries])
        return com

    def make_open(self):
        def com():
            f = tk.filedialog.askopenfilename(title="Open")
            if (f==""):
                return
            color = "no"
            while ((color != "white") & (color != "black") & (color != "")):
                color = tk.simpledialog.askstring("Color to play", "What color will you play? (white/black)")

            if (color==""):
                return

            self.queue.put(["Flip", color])
            self.player = chess.WHITE if color=="white" else chess.BLACK
            self.awaiting_move = color=="white" 
            pgn = open(f)
            game = chess.pgn.read_game(pgn)
            self.current = f
            self.board = game.board()
            self.node = game.next()
            self.queue.put(["Board", self.board])
            self.done = False
            self.internal_queue.put("Continue")
        return com
            
    def set_command(self):
        for row in range(0,8):
            for col in range(0,8):
                self.queue.put(["Command", col+row*8,
                                self.make_command(col+row*8)])

    def set_cancel(self):
        for row in range(0,8):
            for col in range(0,8):
                self.queue.put(["Cancel", col+row*8,
                                self.cancel_moves])
    def set_hint(self):
        self.queue.put(["SetupHint", self.make_hint()])

    def set_open(self):
        self.queue.put(["SetupOpen", self.make_open()])

    def set_score(self):
        self.queue.put(["SetupScore", self.display_scores])
    
    def display_scores(self):
        output = {}
        with open(self.score_file, 'r') as f:
            scores = json.load(f)
            for key, value in scores.items():
                output[key] = compute_stats(value)

        ScoreWindow(["Last Practice","All Time", "Last 30 Days", "Last Week"], output)

    def send_make_move(self, move):
        x0 = move.from_square
        x1 = move.to_square
        p = self.board.piece_at(move.from_square)

        san = self.board.san(move)
        if (san=="O-O"):
            self.queue.put(["MakeMove", p.symbol(), x0, x1])
            if (p.symbol()=="K"):
                self.queue.put(["MakeMove", "R", x0+3, x1-1])
            if (p.symbol()=="k"):
                self.queue.put(["MakeMove", "r", x0+3, x1-1])
        elif (san=="O-O-O"):
            self.queue.put(["MakeMove", p.symbol(), x0, x1])
            if (p.symbol()=="K"):
                self.queue.put(["MakeMove", "R", x0-4, x1+1])
            if (p.symbol()=="k"):
                self.queue.put(["MakeMove", "r", x0-4, x1+1])
        else:
            self.queue.put(["MakeMove", p.symbol(), x0, x1])

    def write_score(self):
        if (exists(self.score_file) & os.stat(self.score_file).st_size > 0):
            with open(self.score_file, 'r') as infile:
                toadd = json.load(infile)

        else:
            toadd = {}

        if (self.current in toadd):
            toadd[self.current].append({'tries': self.tries,
                                        'moves': self.moves,
                                        'time': time.time()})
        else:
            toadd[self.current] = [{'tries': self.tries,
                                    'moves': self.moves,
                                    'time': time.time()}]
        
        with open(self.score_file, 'w') as outfile:
            json.dump(toadd, outfile)
    
    def periodic_call(self):
        self.master.after(50, self.periodic_call)
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)

    def worker_thread1(self):
        while self.running:
            if (not self.done):
                msg = self.internal_queue.get()
                if (self.board.turn != self.player):
                    if (self.node is not None):
                        self.send_make_move(self.node.move)
                        self.board.push(self.node.move)
                        self.awaiting_move = True
                        self.node = self.node.next()
                        self.moves = self.moves + 1
                        self.queue.put(["Move", self.moves])
                    elif (self.var_num == 0):
                        self.done = True
                        self.queue.put(["Move", self.moves+1])


                
    def end_application(self):
        self.running = False
        self.internal_queue.put("Continue")
        self.master.destroy()


