from src.game import abcMove, abcHeuristic, abcGame, abcBoard
from src.minimax import Minimax
from copy import deepcopy
from src.gui import Square
import threading


class Move(abcMove):
    @property
    def x(self):
        return self.dest[0]

    @property
    def y(self):
        return self.dest[1]


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
        newFreeSquares = []
        for oldFreeSquare in self.freeSquares:
            newFreeSquares.append(new.getSquare(oldFreeSquare.x, oldFreeSquare.y))
        new.__dict__['freeSquares'] = newFreeSquares
        return new


class Game(abcGame):
    def __init__(self, *args, **kwargs):
        if args[0]:
            super(Game, self).__init__(*args, **kwargs)
            self.passCounter = 0
            self.coinParityHeur = CoinParity()
            self.weightsHeur = Weights()
            self.mobility = Mobility()
            self.commitMove(Move((3, 4), self.player1))
            self.commitMove(Move((3, 3), self.player2))
            self.commitMove(Move((4, 3), self.player1))
            self.commitMove(Move((4, 4), self.player2))

    def action(self, square):
        '''Is invoked when a square is pressed'''
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
        mode = self.settings.getMode()
        if mode == 0:  # PvsP
            pass
        elif mode == 1:  # PvsAI
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
        elif mode == 2:  # AIvsAI
            if self.settings.getMode() == 2:
                while True:
                    move = Minimax(self).getBestMove()
                    if move is None:
                        self.handlePass()
                    else:
                        self.commitMove(move)
                    if (winner := self.gameOver()):
                        print("GAME OVER - The winner is:", winner)
                        self.window.showWinnerPopup(winner)
                        break

    def start(self):
        '''Runs another thread so that progress is visible on gui'''
        thread = threading.Thread(None, target=self._start)
        thread.start()

    def restart(self):
        self.currPlayer = self.player1
        self.passCounter = 0
        self.board = Board(self.window, self, Square, self.squaresNum, self.squareSize)
        self.commitMove(Move((3, 4), self.player1))
        self.commitMove(Move((3, 3), self.player2))
        self.commitMove(Move((4, 3), self.player1))
        self.commitMove(Move((4, 4), self.player2))

    def switchPlayers(self) -> None:
        self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2

    def getPossibleMoves(self) -> list:
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
        self.passCounter += 1
        self.switchPlayers()

    def gameOver(self) -> str:
        if not self.board.freeSquares or self.passCounter == 2:
            evaluate = self.coinParityHeur.eval(self.board.squares)
            if evaluate > 0:
                return self.player1.type
            elif evaluate < 0:
                return self.player2.type
            else:
                return "Draw"
        return ''

    def evaluate(self) -> int:
        if self.currPlayer is self.player1:
            if self.settings.getHeurP1() == 0:
                return self.coinParityHeur.eval(self.board.squares)
            elif self.settings.getHeurP1() == 1:
                return self.weightsHeur.eval(self.board.squares)
            else:
                return self.mobility.eval(self)
        else:
            if self.settings.getHeurP2() == 0:
                return self.coinParityHeur.eval(self.board.squares)
            elif self.settings.getHeurP2() == 1:
                return self.weightsHeur.eval(self.board.squares)
            else:
                return self.mobility.eval(self)

    def _getFlipsHorVer(self, row, col, src, init, dst, step=1):
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

    def _getFlipsDiag(self, row, col, row_sign, col_sign, condL, condR):
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

    def _getFlips(self, move: Move, booleanOutput=False):
        '''This method returns a list of taken squares that should change color after the move.'''
        candsE = self._getFlipsHorVer(move.x, None, move.y, 1, self.board.size, 1)
        if booleanOutput and candsE: return True
        candsW = self._getFlipsHorVer(move.x, None, move.y, -1, -1, -1)
        if booleanOutput and candsW: return True
        candsN = self._getFlipsHorVer(None, move.y, move.x, -1, -1, -1)
        if booleanOutput and candsN: return True
        candsS = self._getFlipsHorVer(None, move.y, move.x, 1, self.board.size, 1)
        if booleanOutput and candsS: return True
        candsNE = self._getFlipsDiag(move.x, move.y, -1, 1, lambda a, b, c: a + b * c >= 0,
                                     lambda a, b, c: a + b * c < self.board.size)
        if booleanOutput and candsNE: return True
        candsSE = self._getFlipsDiag(move.x, move.y, 1, 1, lambda a, b, c: a + b * c < self.board.size,
                                     lambda a, b, c: a + b * c < self.board.size)
        if booleanOutput and candsSE: return True
        candsSW = self._getFlipsDiag(move.x, move.y, 1, -1, lambda a, b, c: a + b * c < self.board.size,
                                     lambda a, b, c: a + b * c >= 0)
        if booleanOutput and candsSW: return True
        candsNW = self._getFlipsDiag(move.x, move.y, -1, -1, lambda a, b, c: a + b * c >= 0,
                                     lambda a, b, c: a + b * c >= 0)
        if booleanOutput: return len(candsNW) != 0

        return candsE + candsW + candsN + candsS + candsNE + candsSE + candsSW + candsNW

    def updateState(self, move: Move = None, display: bool = True) -> None:
        for square in self._getFlips(move): self.board.updateSquare(square, display)

    def isLegalMove(self, move: Move) -> bool:
        if self.board.getSquare(move.x, move.y).occupied(): return False
        return self._getFlips(move, booleanOutput=True)

    def __deepcopy__(self, memodict={}):
        new = self.__class__(None, None, None, None, None, None, None, None)
        new.__dict__.update(self.__dict__)
        new.__dict__['board'] = deepcopy(self.__dict__['board'])
        return new


class CoinParity(abcHeuristic):
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


class Weights(abcHeuristic):
    def __init__(self):
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


class Mobility(abcHeuristic):
    def eval(self, *args) -> int:
        game = args[0]
        temp = game.currPlayer
        game.currPlayer = game.player1
        black = len(game.getPossibleMoves())
        game.currPlayer = game.player2
        white = len(game.getPossibleMoves())
        game.currPlayer = temp
        return black - white
