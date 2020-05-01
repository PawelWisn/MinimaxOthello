from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def __init__(self, root, game, square, squaresNum, squareSize):
        super(Board, self).__init__(root, game, square, squaresNum, squareSize)
        self.freeSquares = squaresNum

    def updateSquare(self, move: abcMove) -> None:
        self.squares[move.dest[1]][move.dest[0]].update(move.player)
        self.freeSquares -= 1


class Move(abcMove):
    @staticmethod
    def isLegal(board: abcBoard, dest, player=None, src=None) -> bool:
        if board.getSquare(dest[1], dest[0]).occupied:
            return False
        # if not change -> False
        return True


class Game(abcGame):
    def action(self, square):
        dest = square.x, square.y
        if Move.isLegal(self.board, dest):
            move = Move(dest, self.currentPlayer.type)
            self.makeMove(move)

    def makeMove(self, move: abcMove) -> None:
        self.board.updateSquare(move)
        if self.currentPlayer is self.firstPlayer:
            self.currentPlayer = self.secondPlayer
        else:
            self.currentPlayer = self.firstPlayer

    def gameOver(self) -> int:
        if not self.board.freeSquares:
            return True
        # if two passes in a row -> True
        return False
