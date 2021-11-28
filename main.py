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
import sys
import os

root = tk.Tk(className="OpenOpenings")

from openopenings import OpenOpenings

root.title("OpenOpenings")
root.wm_title("OpenOpenings")

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")


root.iconphoto(True, tk.PhotoImage(file=os.path.join(base_path,"img/icon.png")))
client = OpenOpenings(root)

root.protocol("WM_DELETE_WINDOW", client.end_application)
root.mainloop()
