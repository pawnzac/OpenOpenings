# OpenOpenings

## Screenshots

![Screenshot](screenshot1.png?raw=true)


In Read Mode:

![Screenshot](screenshot2.png?raw=true)

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

## Documentation

To add PGNs to the Library, click Library->Add to Library. Can select groups of PGN and import them all as separate chapters in the same book. If a PGN contains multiple games, they will also all be added to the same book. The chapters are automatically named after the Event tag in the PGN. Lichess studies have their chapter titles in the Event tag. Chapters can be renamed with Library->(Select Book Name)->Select->Rename. PGN files do _not_ need to be retained or kept in the same location after, the PGNs are saved in the directory itself.

"Read Mode" disables scoring and displays any comments in the PGN below the board. Useful for browsing a lesson before practicing it.

Data is saved in the Home directory in file ".openopenings.json". 

