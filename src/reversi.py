from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.freeSquares = self.squaresNum ** 2
        self.size = int(self.squaresNum ** 0.5)

    def updateSquare(self, move: abcMove) -> None:
        print('\nupdating player', move.dest, move.player)
        self.squares[move.x][move.y].update(move.player)
        self.freeSquares -= 1


class Move(abcMove):
    @property
    def x(self):
        return self.dest[0]

    @property
    def y(self):
        return self.dest[1]

    @staticmethod
    def isLegal(board: abcBoard, dest, player=None, src=None) -> bool:
        if board.getSquare(dest[0], dest[1]).occupied:
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
        # print(repr(square))
        dest = square.x, square.y
        if Move.isLegal(self.board, dest):
            move = Move(dest, self.currPlayer)
            self.makeMove(move)
        print('evaluation:', self.evaluate())

    def makeMove(self, move: abcMove) -> None:
        # print(repr(self.settings))
        self.passCounter = 0
        self.board.updateSquare(move)
        self.updateState(move)
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

    def getFlippablesHorVer(self, row, col, src, init, dst, step=1):
        candidates = []
        for var in range(src + init, dst, step):
            print(var, end=' ')
            r = row if row else var
            c = col if col else var
            if (owner := self.board.getSquare(r, c).getPlayer()):
                if owner is not self.currPlayer:
                    candidates.append(Move((r, c), self.currPlayer))
                else:
                    return candidates
            else:
                break
        return []

    def getFlippablesDiagonal(self, row, col, row_sign, col_sign, condL, condR):
        offset = 1
        candidates = []
        while condL(row, row_sign, offset) and condR(col, col_sign, offset):
            print((row + row_sign * offset, col + col_sign * offset), end=' ')
            if (owner := self.board.getSquare(row + row_sign * offset, col + col_sign * offset).getPlayer()):
                if owner is not self.currPlayer:
                    candidates.append(Move((row + row_sign * offset, col + col_sign * offset), self.currPlayer))
                else:
                    return candidates
            else:
                break
            offset += 1
        return []

    def getFlippables(self, move: abcMove):
        candsE = self.getFlippablesHorVer(move.x, None, move.y, 1, self.board.size, 1)
        candsW = self.getFlippablesHorVer(move.x, None, move.y, -1, -1, -1)
        candsN = self.getFlippablesHorVer(None, move.y, move.x, -1, -1, -1)
        candsS = self.getFlippablesHorVer(None, move.y, move.x, 1, self.board.size, 1)
        candsNE = self.getFlippablesDiagonal(move.x, move.y, -1, 1, lambda a, b, c: a + b * c >= 0,
                                             lambda a, b, c: a + b * c < self.board.size)
        candsSE = self.getFlippablesDiagonal(move.x, move.y, 1, 1, lambda a, b, c: a + b * c < self.board.size,
                                             lambda a, b, c: a + b * c < self.board.size)
        candsSW = self.getFlippablesDiagonal(move.x, move.y, 1, -1, lambda a, b, c: a + b * c < self.board.size,
                                             lambda a, b, c: a + b * c >= 0)
        candsNW = self.getFlippablesDiagonal(move.x, move.y, -1, -1, lambda a, b, c: a + b * c >= 0,
                                             lambda a, b, c: a + b * c >= 0)
        return candsE + candsW + candsN + candsS + candsNE + candsSE + candsSW + candsNW


    def updateState(self, move: abcMove):
        for c in self.getFlippables(move): self.board.updateSquare(c)

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
