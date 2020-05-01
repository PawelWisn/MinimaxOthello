from src.gui import Window
from src.reversi import Square, Board

window = Window(1000, 750, 'Reversi')
board = Board(window, Square, 64, 75)
window.run()
