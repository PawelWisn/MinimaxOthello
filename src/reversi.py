from src.gui import abcSquare
from src.game import abcMove, abcHeuristic, abcGame,abcBoard

class Square(abcSquare):
    def handler(self):
        print('handling')
        self.update('white')


class Board(abcBoard):
    def updateSquare(self, move:abcMove)->None:
        self.squares[move.dest[0]][move.dest[1]].update(move.player)


class Move(abcMove):
    @staticmethod
    def isLegal(board:abcBoard, dest, player, src=None) -> bool:
        return board.getSquare(dest[0],dest[1])