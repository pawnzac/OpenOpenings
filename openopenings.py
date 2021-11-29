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
from library_window import LibraryWindow
import time
import chess
import chess.pgn
import json
from gui import UserInterface
from utility import *
import io
from import_window import ImportWindow
class OpenOpenings(object):
    def __init__(self, master):
        self.master = master
        self.master.winfo_toplevel().title("OpenOpenings")
        self.queue = queue.Queue()

        self.internal_queue = queue.Queue()
        
        self.lib_file = expanduser("~") + "/.openopenings.json"
        if (exists(self.lib_file) and (os.stat(self.lib_file).st_size > 0)):
            self.library = LibraryWindow(self.lib_file, self.internal_queue, self.make_open())
        else:
            self.library = LibraryWindow(None, self.internal_queue, self.make_open())
        

        self.gui = UserInterface(master, self.queue, self.end_application)
        self.running = True
        self.node = None
        self.board = None
        self.need_to_update_board = True
        self.player = None
        self.done = True
        self.awaiting_continue = False
        self.tries = 0
        self.moves = 0
        self.master.bind("<Key>", self.continue_text)
        
        self.var_num = [0]
        self.var_node = []
        self.backup_board = []
        
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
        self.set_library()
        self.set_start()
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
                                self.backup_board.append(self.board.copy())
                                self.var_node.append(self.node)
                                self.var_num.append(0)
                                if (self.var_num[-1]==0):
                                    self.var_num[-1] = 1
                                
                                self.node = self.node.variations[self.var_num[-1]]
                            elif ((self.var_num[-1] != 0) & ((self.node.next() is None) or (self.node.next().next() is None))):
                                if (len(self.var_node[-1].variations) <= (self.var_num[-1]+1)):
                                    self.var_num.pop()
                                    self.node = self.var_node[-1].variations[0]
                                    self.board = self.backup_board.pop().copy()
                                    self.var_node.pop()
                                else:
                                    self.var_num[-1] += 1
                                    self.node = self.var_node[-1].variations[self.var_num[-1]]
                                    self.board = self.backup_board[-1].copy()
                                self.queue.put(["Board",self.board])
                            elif self.node is not None:
                                self.queue.put(["SetReadText", self.node.comment])
                                self.node = self.node.next()


                            if ((self.node is None) & (self.var_num[-1]==0)):
                                self.queue.put(["Status", "Done!"])
                                if (self.gui.read_mode.get()==0):
                                    self.write_score()
                                    self.library.write(self.lib_file)

                                self.queue.put(["CheckBoxState", tk.NORMAL])
                        else:
                            self.queue.put(["Status", "Incorrect."])

                    except ValueError as e:
                        self.queue.put(["Status", "Invalid Move."])

                    self.queue.put(["DeselectSquare", self.move_list[0]])
                    self.move_list = []
                    self.internal_queue.put("Continue")

        return com

    def make_full_move_hint(self):
        def com(event):
            self.tries += 5*(2-self.hint_level)
            self.hint_level = 2
            do = self.make_hint()
            do()

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
            fs = tk.filedialog.askopenfilenames(title="Open")
            if (len(fs)==0):
                return

            def after(color, book, tag):
                for f in fs:
                    if (f==""):
                        return

                    fh = open(f,mode='r',encoding="utf-8")

                    game = chess.pgn.read_game(fh)
                    while (game is not None):
                        exporter = chess.pgn.StringExporter(headers=True,
                                                            variations=True,
                                                            comments=True)
                
                        pgn = game.accept(exporter)

                        self.library.add_to_library(game.headers[tag],
                                                    pgn, book, color)
                    
                        game = chess.pgn.read_game(fh)
                    fh.close()
                
                self.library.write(self.lib_file)
                self.library.open_window()
                self.internal_queue.put("Continue")
                
            ImportWindow(after)

        return com

    def make_start(self):
        def com():
            pgn = self.library.get_current_pgn()
            color = self.library.get_color()

            self.moves = 0
            self.tries = 0


            self.queue.put(["Move", self.moves])
            self.queue.put(["Try", self.tries])
            self.queue.put(["Flip", color])
            self.player = chess.WHITE if color=="white" else chess.BLACK
            self.awaiting_move = color=="white"
            pgn_io = io.StringIO(pgn)
            game = chess.pgn.read_game(pgn_io)
        
            self.current = self.library.current_book + "/" + self.library.current_chapter
            self.board = game.board()
            self.node = game.next()
            if self.node is not None:
                self.queue.put(["SetReadText", self.node.comment])
            self.queue.put(["Board", self.board])
            self.queue.put(["CheckBoxState",tk.DISABLED])
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
        self.queue.put(["SetRightClickHint", self.make_full_move_hint()])

    def set_open(self):
        self.queue.put(["SetupOpen", self.make_open()])

    def set_score(self):
        self.queue.put(["SetupScore", self.make_scores()])

    def set_library(self):
        self.queue.put(["SetupLibrary", self.display_library])

    def set_start(self):
        self.queue.put(["SetupStart", self.make_start()])

    def make_scores(self):
        def com():
            self.display_scores()
        return com
    def display_library(self):
        self.library.open_window()

    def display_comments(self):
        return self.node.comment
        
        
    def display_scores(self):
        output = {}
        bookname = self.library.current_book
        if bookname is not None:
            for (chaptername, chapter) in self.library.library[bookname].items():
                output[bookname + "/" + chaptername] = compute_stats(
                    self.library.library[bookname][chaptername]["sessions"])

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
        self.library.add_session(self.tries, self.moves, time.time())
    
    def periodic_call(self):
        self.master.after(50, self.periodic_call)
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)

    def format_title(self, x):
        n = 38
        return '\n'.join([x[idx:idx+n] for idx in range(0, len(x), n)])
        
        
    def worker_thread1(self):
        while self.running:
            msg = self.internal_queue.get()
            if (msg=="Library"):
                self.queue.put(["ChangeChapter",
                                self.library.current_book +
                                " / " + self.library.current_chapter])
            if (not self.done):

                if (self.board.turn != self.player):
                    if (self.node is not None):
                        if (self.node.next() is None):
                            if (len(self.var_num) > 0):
                                self.var_num.pop()
                                self.node = self.var_node[-1].variations[0]
                                self.board = self.backup_board.pop().copy()
                                self.var_node.pop()

                        self.send_make_move(self.node.move)
                        self.board.push(self.node.move)
                        self.awaiting_move = True
                        comment = "Press Space to see comment on next ply...\n\n" + self.node.comment
                        self.queue.put(["SetReadText", comment])
                        self.awaiting_continue = True
                        self.node = self.node.next()
                            
                        self.moves = self.moves + 1
                        self.queue.put(["Move", self.moves])
                    elif (len(self.var_num) == 0):
                        self.done = True
                        self.queue.put(["Move", self.moves+1])

    def continue_text(self, event):
        if self.awaiting_continue and event.char == ' ':
            if (self.node is not None):
                self.queue.put(["SetReadText", self.node.comment])
                self.awaiting_continue = False
                
    def end_application(self):
        self.running = False
        self.internal_queue.put("Continue")
        self.master.destroy()


