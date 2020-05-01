from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def updateSquare(self, move: abcMove) -> None:
        self.squares[move.dest[0]][move.dest[1]].update(move.player)

class Move(abcMove):
    @staticmethod
    def isLegal(board: abcBoard, dest, player, src=None) -> bool:
        return not board.getSquare(dest[0], dest[1]).occupied


class Game(abcGame):
    def action(self, square):
        print('action')



