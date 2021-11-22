import tkinter as tk

root = tk.Tk()

from openopenings import OpenOpenings

root.title("OpenOpenings")

client = OpenOpenings(root)

root.protocol("WM_DELETE_WINDOW", client.end_application)
root.mainloop()
