from src.gui import Window, Square
from src.reversi import Board, Game, Move, Weights
from src.game import Player

window = Window(1000, 750, 'Reversi')
modeVar, depthVar, heurVarP1, heurVarP2 = window.build()
game = Game(window, Board, Square, 64, 75, 'Black', 'White', modeVar, depthVar, heurVarP1, heurVarP2)
game.makeMove(Move((3,3),game.player2))
game.makeMove(Move((3,4),game.player1))
game.makeMove(Move((4,3),game.player1))
game.makeMove(Move((4,4),game.player2))

window.run()
