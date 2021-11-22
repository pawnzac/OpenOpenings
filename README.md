# OpenOpenings

![Screenshot](screenshot1.png?raw=true)

## What it does?

OpenOpenings is a program for practicing chess openings.

Essentially, what it does is allow you to open a PGN file and play one color of the moves contained in the PGN.  It iterates through all variations played by the opponent. The program scores you based on how accurate you are at choosing the moves and saves the results to disk so you can check how your scores improve over time.

It also gives you hints when you are stuck.

## Installation

If you have Python3 with the following packages installed:

- tkinter
- python-chess
- datetime
- json

Simply typing:

```
python3 main.py
```

From the project's directory should work.

If you prefer a standalone executable, typing:

```
make
```

from the project's directory will output `dist/openopenings`, a standalone executable. Bundling into a single file requires `pyinstaller`.

Once I've iterated a bit more on it, I'll add the single-file release to the page so that it's easy to just download the file for people that don't have Python.

## Current Limitations

Currently, it doesn't handle "nested" variations well. I don't really encounter that much in the Lichess studies I wanted to practice on so I didn't put much thought into it. To be clear, the program does handle variations well and fine. It just doesn't handle variations-within-variations. I will add this at some point.
