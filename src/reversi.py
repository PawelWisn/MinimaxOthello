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
        self.coinParityHeur = CoinParity()
        self.weightsHeur = Weights()

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


class CoinParity(abcHeuristic):
    def eval(self, state: list) -> int:
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


class Weights(abcHeuristic):
    def __init__(self, *args, **kwargs):
        super(Weights, self).__init__(*args, **kwargs)
        self.weights = {}
        vals = '4 -3 2 2 2 2 -3 4 -3 -4 -1 -1 -1 -1 -4 -3 2 -1 1 0 0 1 -1 2 2 -1 0 1 1 0 -1 2 2 -1 0 1 1 0 -1 2 2 -1 1 0 0 1 -1 2 -3 -4 -1 -1 -1 -1 -4 -3 4 -3 2 2 2 2 -3 4'.split(' ')[::-1]
        for x in range(8):
            for y in range(8):
                self.weights[(x,y)] = int(vals.pop())


    def eval(self, state: list) -> int:
        black = 0
        white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player == 'White':
                    white += self.weights[(square.x, square.y)]
                elif player == 'Black':
                    black += self.weights[(square.x, square.y)]
        return white - black
