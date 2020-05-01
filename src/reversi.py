from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.freeSquares = len(self.squares) ** 2

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
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.passCounter = 0

    def action(self, square):
        print(repr(square))
        dest = square.x, square.y
        if Move.isLegal(self.board, dest):
            move = Move(dest, self.currPlayer.type)
            self.makeMove(move)

    def makeMove(self, move: abcMove) -> None:
        self.passCounter = 0
        self.board.updateSquare(move)

        if True:  # if next player has move
            self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2
        else:
            pass  # display  player has no move

    def gameOver(self) -> int:
        if not self.board.freeSquares:
            return True
        # if two passes in a row -> True
        return False


class Naive(abcHeuristic):
    def eval(self, state: list) -> float:
        black = 0
        white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player == 'White':
                    white += 1
                elif player == 'Black':
                    black += 1
        return white - black
