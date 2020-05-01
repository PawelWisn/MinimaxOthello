from src.gui import Window, Square
from src.reversi import Board, Game, Move

window = Window(1000, 750, 'Reversi')
modeVar, depthVar, heurVarP1, heurVarP2 = window.build()
game = Game(window, Board, Square, 64, 75, 'black', 'white', modeVar, depthVar, heurVarP1, heurVarP2)
game.makeMove(Move((3,3),'white'))
game.makeMove(Move((3,4),'black'))
game.makeMove(Move((4,3),'black'))
game.makeMove(Move((4,4),'white'))

window.run()
