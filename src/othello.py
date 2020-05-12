from src.game import Move, abcHeuristic, abcGame, abcBoard
from src.minimax import Minimax
from copy import deepcopy, copy
from src.gui import Square
import threading
from time import time
import matplotlib.pyplot as plt


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        if args[0]:
            super(Board, self).__init__(*args, **kwargs)
            self.freeSquares = []
            for row in self.squares:
                for square in row: self.freeSquares.append(square)
            self.size = int(self.squaresNum ** 0.5)

    def updateSquare(self, move: Move, display: bool = True) -> None:
        if move.player and (square := self.getSquare(move.x, move.y)) in self.freeSquares:
            self.freeSquares.remove(square)
        elif not move.player:
            self.freeSquares.append(self.getSquare(move.x, move.y))
        self.squares[move.x][move.y].update(move.player, display)

    def __deepcopy__(self, memodict={}):
        new = self.__class__(None, None, None, None, None)
        new.__dict__.update(self.__dict__)
        new.__dict__['squares'] = deepcopy(self.__dict__['squares'])
        return new


class Game(abcGame):
    def __init__(self, *args, **kwargs):
        if args[0]:
            super(Game, self).__init__(*args, **kwargs)
            self.passCounter = 0
            self.coinParityHeur = CoinParity()
            self.weightsHeur = Weights()
            self.mobility = Mobility()

    def action(self, square):
        move = Move((square.x, square.y), self.currPlayer)
        if self.isLegalMove(move):
            self.commitMove(move)
            if (winner := self.gameOver()):
                print("GAME OVER - The winner is:", winner)
                self.window.showWinnerPopup(winner)
            elif self.settings.getMode() == 1:
                self.start()
        else:
            print("click was illegal")
        print("next player:", self.currPlayer.type, '\n')

    def _start(self):
        statistics = []
        print('start')
        mode = self.settings.getMode()
        if mode == 0:
            pass
        elif mode == 1:
            move = Minimax(self).getBestMove()
            if move is None:
                self.handlePass()
            else:
                self.commitMove(move)
            if (winner := self.gameOver()):
                print("GAME OVER - The winner is:", winner)
                self.window.showWinnerPopup(winner)
            else:
                if not self.getPossibleMoves():
                    self.handlePass()
                    self.start()
        elif mode == 2:
            if self.settings.getMode() == 2:
                while True:
                    start = time()
                    move = Minimax(self).getBestMove()
                    if self.currPlayer is self.player1:
                        statistics.append(time() - start)
                    print('time=', statistics[-1])
                    if move is None:
                        self.handlePass()
                    else:
                        self.commitMove(move)
                    if (winner := self.gameOver()):
                        print("GAME OVER - The winner is:", winner)
                        break
                plt.plot([x for x in range(len(statistics))], statistics)
                plt.show()

    def start(self):
        thread = threading.Thread(None, target=self._start)
        thread.start()

    def restart(self):  # todo restart
        self.currPlayer = self.player1
        self.passCounter = 0
        self.board = Board(self.window, self, Square, self.squaresNum, self.squareSize)
        self.commitMove(Move((3, 4), self.player1))
        self.commitMove(Move((3, 3), self.player2))
        self.commitMove(Move((4, 3), self.player1))
        self.commitMove(Move((4, 4), self.player2))

    def switchPlayers(self) -> None:
        self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2

    def getPossibleMoves(self) -> list:  ##
        legalMoves = []
        for freeSquare in self.board.freeSquares:
            move = Move((freeSquare.x, freeSquare.y), self.currPlayer)
            if self.isLegalMove(move):
                legalMoves.append(move)
        return legalMoves

    def commitMove(self, move: Move, display: bool = True) -> None:
        self.passCounter = 0
        self.updateState(move, display)
        self.board.updateSquare(move, display)
        self.switchPlayers()

    def handlePass(self) -> None:
        print("Pass")
        self.passCounter += 1
        self.switchPlayers()

    def gameOver(self) -> str:
        '''Checks if the game is over. If it is, it returns a winner'''
        if not self.board.freeSquares or self.passCounter == 2:
            print('Game over!')
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
                value = self.coinParityHeur.eval(self.board.squares)
            elif self.settings.getHeurP1() == 1:
                value = self.weightsHeur.eval(self.board.squares)
            else:
                value = self.mobility.eval(self)
        else:
            if self.settings.getHeurP2() == 0:
                value = self.coinParityHeur.eval(self.board.squares)
            elif self.settings.getHeurP2() == 1:
                value = self.weightsHeur.eval(self.board.squares)
            else:
                value = self.mobility.eval(self)
        return value

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
        out = candsE + candsW + candsN + candsS + candsNE + candsSE + candsSW + candsNW
        return out

    def updateState(self, move: Move = None, display: bool = True) -> None:
        for square in self._getFlippables(move): self.board.updateSquare(square, display)

    def isLegalMove(self, move: Move) -> bool:
        if self.board.getSquare(move.x, move.y).occupied:
            return False
        return len(self._getFlippables(move)) != 0

    def __deepcopy__(self, memodict={}):
        new = self.__class__(None, None, None, None, None, None, None, None)
        new.__dict__.update(self.__dict__)
        new.__dict__['board'] = deepcopy(self.__dict__['board'])
        return new


class CoinParity(abcHeuristic):  # optimize by map
    def eval(self, *args) -> int:
        state = args[0]
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
        vals = '5 -3 2 2 2 2 -3 5 -3 -4 -1 -1 -1 -1 -4 -3 2 -1 1 0 0 1 -1 2 2 -1 0 1 1 0 -1 2 2 -1 0 1 1 0 -1 2 2 -1 1 0 0 1 -1 2 -3 -4 -1 -1 -1 -1 -4 -3 5 -3 2 2 2 2 -3 5'.split(
            ' ')[::-1]
        size = int(len(vals) ** 0.5)
        for x in range(size):
            for y in range(size):
                self.weights[(x, y)] = int(vals.pop())

    def eval(self, *args) -> int:
        state = args[0]
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

class Mobility(abcHeuristic):  # optimize by map
    def eval(self, *args) -> int:
        game = args[0]
        temp = game.currPlayer
        game.currPlayer=game.player1
        black = len(game.getPossibleMoves())
        game.currPlayer = game.player2
        white = len(game.getPossibleMoves())
        game.currPlayer = temp
        return black-white