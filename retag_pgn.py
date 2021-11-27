## Sets Event Tag to some other tag in PGN file.
## Syntax:
## python retag_pgn.py path/to/pgn/file.pgn $TAG path/to/output/output.pgn
## Where $TAG will be assigned to the Event tag.


import sys
import chess
import chess.pgn

fn = sys.argv[1]
tag = sys.argv[2]
out = sys.argv[3]

fh = open(fn, mode='r')
game = chess.pgn.read_game(fh)
exporter = chess.pgn.StringExporter(headers=True,
                                    variations=True,
                                    comments=True)

pgn_out = ""

while (game is not None):
    game.headers["Event"] = game.headers[tag]
    pgn = game.accept(exporter)
    pgn_out = pgn_out + "\n\n" + pgn
    game = chess.pgn.read_game(fh)

fh.close()

fh = open(out, mode='w')
print(pgn_out, file=fh, end="\n\n")
fh.close()

