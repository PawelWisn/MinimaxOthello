from src.gui import Square, Board
from src.minimax import Move

class ReversiSquare(Square):
    def handler(self):
        print('handling')


class ReversiBoard(Board):
    def updateSquare(self, move:Move)->None:
        self.squares[move.dest[0]][move.dest[1]].update(move.player)