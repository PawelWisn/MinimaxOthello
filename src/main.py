from src.gui import Window, Square
from src.othello import Board, Game, Move
from src.minimax import Minimax

if __name__=="__main__":
    window = Window(1000, 750, 'Othello')
    settings = window.build()
    game = Game(window, Board, Square, 64, 75, 'Black', 'White', settings)
    game.commitMove(Move((3, 3), game.player2))
    game.commitMove(Move((3, 4), game.player1))
    game.commitMove(Move((4, 3), game.player1))
    game.commitMove(Move((4, 4), game.player2))

    window.run()