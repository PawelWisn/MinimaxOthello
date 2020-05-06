from src.game import Move, abcHeuristic, abcGame, abcBoard
from src.minimax import Minimax


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.freeSquares = self.squaresNum
        self.size = int(self.squaresNum ** 0.5)

    def updateSquare(self, move: Move) -> None:
        self.squares[move.x][move.y].update(move.player)


class Game(abcGame):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.passCounter = 0
        self.freeSquares = self.squaresNum
        self.coinParityHeur = CoinParity()
        self.weightsHeur = Weights()

    def action(self, square):
        move = Move((square.x, square.y), self.currPlayer)
        if flippables := self.isLegalMove(move):
            print("click legal")
            self.commitMove(move, flippables)
            print('evaluation:', self.evaluate())
            if self.gameOver():
                raise ValueError('GAME OVER', self.coinParityHeur.eval(self.board.squares))

            print(self.getPossibleMoves())
            if True:  # if next player has move
                self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2
            else:
                self.passCounter += 1
                print('PLAYER HAS NO MOVE - SKIPPING')
        else:
            print("click illegal")
        print("next player:", self.currPlayer.type, '\n')

    def getPossibleMoves(self) -> list:
        legalMoves = []
        for x in range(self.board.size):
            for y in range(self.board.size):
                if not self.board.getSquare(x, y).occupied:
                    move = Move((x, y), self.currPlayer)
                    if self.isLegalMove(move):
                        legalMoves.append(move)
        return legalMoves

    def commitMove(self, move: Move, toUpdate: list) -> None:
        self.updateState(toUpdate + [move])
        self.passCounter = 0
        self.freeSquares -= 1

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

    def _getFlippablesHorVer(self, row, col, src, init, dst, step=1):
        candidates = []
        for var in range(src + init, dst, step):
            r = row if row is not None else var
            c = col if col is not None else var
            if (owner := self.board.getSquare(r, c).getPlayer()):
                if owner is not self.currPlayer:
                    candidates.append(Move((r, c), self.currPlayer))
                else:
                    return candidates
            else:
                break
        return []

    def _getFlippablesDiagonal(self, row, col, row_sign, col_sign, condL, condR):
        offset = 1
        candidates = []
        while condL(row, row_sign, offset) and condR(col, col_sign, offset):
            if (owner := self.board.getSquare(row + row_sign * offset, col + col_sign * offset).getPlayer()):
                if owner is not self.currPlayer:
                    candidates.append(Move((row + row_sign * offset, col + col_sign * offset), self.currPlayer))
                else:
                    return candidates
            else:
                break
            offset += 1
        return []

    def _getFlippables(self, move: Move):
        '''This method returns a list of taken squares that should change color after the move.'''
        candsE = self._getFlippablesHorVer(move.x, None, move.y, 1, self.board.size, 1)
        candsW = self._getFlippablesHorVer(move.x, None, move.y, -1, -1, -1)
        candsN = self._getFlippablesHorVer(None, move.y, move.x, -1, -1, -1)
        candsS = self._getFlippablesHorVer(None, move.y, move.x, 1, self.board.size, 1)
        candsNE = self._getFlippablesDiagonal(move.x, move.y, -1, 1, lambda a, b, c: a + b * c >= 0,
                                              lambda a, b, c: a + b * c < self.board.size)
        candsSE = self._getFlippablesDiagonal(move.x, move.y, 1, 1, lambda a, b, c: a + b * c < self.board.size,
                                              lambda a, b, c: a + b * c < self.board.size)
        candsSW = self._getFlippablesDiagonal(move.x, move.y, 1, -1, lambda a, b, c: a + b * c < self.board.size,
                                              lambda a, b, c: a + b * c >= 0)
        candsNW = self._getFlippablesDiagonal(move.x, move.y, -1, -1, lambda a, b, c: a + b * c >= 0,
                                              lambda a, b, c: a + b * c >= 0)
        return candsE + candsW + candsN + candsS + candsNE + candsSE + candsSW + candsNW

    def updateState(self, toUpdate: list) -> None:
        for f in toUpdate: self.board.updateSquare(f)

    def isLegalMove(self, move: Move) -> list:
        if self.board.getSquare(move.x, move.y).occupied: return []
        return self._getFlippables(move)


class CoinParity(abcHeuristic):  # optimize by map
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
        return black - white


class Weights(abcHeuristic):  # optimize by map
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
        black = white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player is not None:
                    if player.type == 'White':
                        white += self.weights[(square.x, square.y)]
                    else:
                        black += self.weights[(square.x, square.y)]
        return black - white
