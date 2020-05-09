from src.game import Move, abcHeuristic, abcGame, abcBoard
# from src.minimax import Minimax
from copy import deepcopy, copy
from src.gui import Square


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        if args[0]:
            super(Board, self).__init__(*args, **kwargs)
            print(self.squares)
            self.freeSquares = []
            for row in self.squares:
                for square in row: self.freeSquares.append(square)
            print(self.freeSquares)
            self.size = int(self.squaresNum ** 0.5)

    def updateSquare(self, move: Move, display: bool = True) -> None:
        if move.player and (square := self.getSquare(move.x, move.y)) in self.freeSquares:
            self.freeSquares.remove(square)
        elif not move.player:
            self.freeSquares.append(self.getSquare(move.x, move.y))
        self.squares[move.x][move.y].update(move.player, display)

    def __deepcopy__(self, memodict={}):
        new = self.__class__(None, None, None, None, None)
        d = copy(self.__dict__)
        print(d)
        d.pop('game', None)
        d.pop('root', None)
        print(d)
        new.__dict__.update(deepcopy(d))
        return new


class Game(abcGame):
    def __init__(self, *args, **kwargs):
        if args[0]:
            super(Game, self).__init__(*args, **kwargs)
            self.passCounter = 0
            self.coinParityHeur = CoinParity()
            self.weightsHeur = Weights()

    def action(self, square):
        move = Move((square.x, square.y), self.currPlayer)
        if self.isLegalMove(move):
            print("click was legal")
            self.commitMove(move)
            print('evaluation:', self.evaluate())
            if self.gameOver():
                raise ValueError('GAME OVER',
                                 self.coinParityHeur.eval(self.board.squares))  # todo change gameover signal
        else:
            print("click was illegal")
        print("next player:", self.currPlayer.type, '\n')

    def switchPlayers(self) -> None:
        self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2

    def getPossibleMoves(self) -> list:
        legalMoves = []
        for x in range(self.board.size):
            for y in range(self.board.size):
                move = Move((x, y), self.currPlayer)
                if self.isLegalMove(move):
                    legalMoves.append(move)
        return legalMoves

    def commitMove(self, move: Move, display: bool = True) -> None:
        self.updateState(move, display)
        self.switchPlayers()

    def gameOver(self) -> str:
        '''Checks if the game is over. If it is, it returns a winner'''
        if not self.board.freeSquares:
            evaluate = self.coinParityHeur.eval(self.board.squares)
            if evaluate > 0:
                return self.player1.type
            elif evaluate < 0:
                return self.player2.type
            else:
                return "Draw"
        if len(self.getPossibleMoves()) == 0:  # if next player has no moves
            self.switchPlayers()
            if len(self.getPossibleMoves()) == 0:  # if both players have no moves
                evaluate = self.coinParityHeur.eval(self.board.squares)
                if evaluate > 0:
                    return self.player1.type
                elif evaluate < 0:
                    return self.player2.type
                else:
                    return "Draw"
        return ''

    def evaluate(self) -> float:
        if self.currPlayer is self.player1:
            if self.settings.getHeurP1() == 0:
                return self.coinParityHeur.eval(self.board.squares)
            else:
                return self.weightsHeur.eval(self.board.squares)
        else:
            if self.settings.getHeurP2() == 0:
                return self.coinParityHeur.eval(self.board.squares)
            else:
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

    def updateState(self, move: Move = None, display: bool = True) -> None:
        for square in self._getFlippables(move) + [move]: self.board.updateSquare(square, display)

    def isLegalMove(self, move: Move) -> bool:
        if self.board.getSquare(move.x, move.y).occupied: return False
        return len(self._getFlippables(move)) != 0

    def getHeuristic(self) -> abcHeuristic:
        if self.currPlayer is self.player1:
            return self.coinParityHeur if self.settings.getHeurP1() == 0 else self.weightsHeur
        else:
            return self.coinParityHeur if self.settings.getHeurP2() == 0 else self.weightsHeur

    def __deepcopy__(self, memodict={}):
        print(self.__dict__.keys())
        new = self.__class__(None, None, None, None, None, None, None, None)
        d = copy(self.__dict__)
        print(d)
        d.pop('window', None)
        d.pop('settings', None)
        print(d)
        new.__dict__.update(deepcopy(d))
        print(self.__dict__.keys())
        new.__dict__['settings'] = self.__dict__['settings']
        print(new.__dict__.keys())
        return new


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
        print('weights')
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
