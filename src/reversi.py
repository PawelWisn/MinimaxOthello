from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def updateSquare(self, move: abcMove) -> None:
        self.squares[move.dest[1]][move.dest[0]].update(move.player)

class Move(abcMove):
    @staticmethod
    def isLegal(board: abcBoard, dest, player=None, src=None) -> bool:
        return not board.getSquare(dest[1], dest[0]).occupied


class Game(abcGame):
    def action(self, square):
        dest = square.x, square.y
        if Move.isLegal(self.board,dest):
            move = Move(dest, self.nextPlayer)
            self.makeMove(move)

    def makeMove(self, move: abcMove) -> None:
        self.board.updateSquare(move)
