from src.gui import Window, Square
from src.reversi import Board

window = Window(1000, 750, 'Reversi')
hvar, entry, ai = window.build()
board = Board(window, Square, 64, 75 , hvar, entry, ai)

window.run()
