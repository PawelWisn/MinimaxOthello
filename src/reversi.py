from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.freeSquares = len(self.squares) ** 2
        self.size = int(len(self.squares) ** 0.5)

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
            move = Move(dest, self.currPlayer)
            self.makeMove(move)
        print(self.evaluate())

    def makeMove(self, move: abcMove) -> None:
        print(repr(self.settings))
        self.passCounter = 0
        self.board.updateSquare(move)
        if self.gameOver():
            raise ValueError('GAME OVER', self.coinParityHeur.eval(self.board.squares))

        if True:  # if next player has move
            self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2
        else:
            print('PLAYER HAS NO MOVE - SKIPPING')
            pass  # display  player has no move

    def gameOver(self) -> bool:
        return not self.board.freeSquares or self.passCounter == 2

    def evaluate(self) -> float:
        if self.currPlayer is self.player1:  # Player1's turn
            if self.settings.getHeurP1() == 0:  # First heuristic
                return self.coinParityHeur.eval(self.board.squares)
            else:  # Second heuristic
                return self.weightsHeur.eval(self.board.squares)
        else:  # Player2's turn
            if self.settings.getHeurP2() == 0:  # First heuristic
                return self.coinParityHeur.eval(self.board.squares)
            else:  # Second heuristic
                return self.weightsHeur.eval(self.board.squares)

    def updateState(self, state, move: abcMove):
        toFlip = []
        candidates = []
        # row right
        for column in range(move.dest[1] + 1, self.board.size):
            if self.board.getSquare(move.dest[0], column).getPlayer():
                pass


class CoinParity(abcHeuristic):
    def eval(self, state: list) -> int:
        black = white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player is not None:
                    if player.type == 'White':
                        white += 1
                    else:
                        black += 1
        return white - black


class Weights(abcHeuristic):
    def __init__(self, *args, **kwargs):
        super(Weights, self).__init__(*args, **kwargs)
        self.weights = {}
        vals = '4 -3 2 2 2 2 -3 4 -3 -4 -1 -1 -1 -1 -4 -3 2 -1 1 0 0 1 -1 2 2 -1 0 1 1 0 -1 2 2 -1 0 1 1 0 -1 2 2 -1 1 0 0 1 -1 2 -3 -4 -1 -1 -1 -1 -4 -3 4 -3 2 2 2 2 -3 4'.split(
            ' ')[::-1]
        size = int(len(vals) ** 0.5)
        for x in range(size):
            for y in range(size):
                self.weights[(x, y)] = int(vals.pop())

    def eval(self, state: list) -> int:
        print('Weights')
        black = white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player is not None:
                    if player.type == 'White':
                        white += self.weights[(square.x, square.y)]
                    else:
                        black += self.weights[(square.x, square.y)]
        return white - black
