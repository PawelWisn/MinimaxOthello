from src.gui import Window, Square
from src.reversi import Board, Game

window = Window(1000, 750, 'Reversi')
modeVar, depthVar, heurVarP1, heurVarP2 = window.build()
game = Game(window, Board, Square, 64, 75, modeVar, depthVar, heurVarP1, heurVarP2)


window.run()
