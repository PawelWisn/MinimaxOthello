from game import Player, abcBoard, Move, abcGame
from copy import deepcopy
from random import choice


class Minimax:
    def __init__(self, game):
        self.game = deepcopy(game)
        self.depth = game.settings.getDepthP1() if game.currPlayer is game.player1 else game.settings.getDepthP2()
        self.inf = int(1e50)
        self.moveDict = {}
        alphaBeta = game.settings.isAlphaBetaP1() if game.currPlayer is game.player1 else game.settings.isAlphaBetaP2()
        self.alpha = -self.inf if alphaBeta else None
        self.beta = self.inf if alphaBeta else None

    def getBestMove(self):
        return self.search(self.game, self.depth, self.game.currPlayer is self.game.player1, self.alpha, self.beta)


    def getWinnerValue(self, game, winner):
        if game.player1.type == winner: return int(1e45)
        if game.player2.type == winner: return -int(1e45)
        return 0

    def search(self, game: abcGame, depth: int, maximizing: bool = True, alpha=None, beta=None):
        if (winner := game.gameOver()):
            return self.getWinnerValue(game, winner)
        if depth == 0:
            return game.evaluate()
        moves = game.getPossibleMoves()
        if maximizing:
            if moves:
                if alpha is not None:
                    for move in moves:
                        copy = deepcopy(game)
                        copy.commitMove(move, display=False)
                        value = self.search(copy, depth - 1, False, alpha, beta)
                        alpha = max(alpha, value)
                        if alpha>=beta: return alpha
                        value = alpha
                        if depth == self.depth: self.moveDict[move] = value
                else:
                    value = -self.inf
                    for move in moves:
                        copy = deepcopy(game)
                        copy.commitMove(move, display=False)
                        value = max(value, self.search(copy, depth - 1, False))
                        if depth == self.depth: self.moveDict[move] = value
            else:
                game.handlePass()
                value = self.search(game, depth - 1, False, alpha, beta)
        else:
            if moves:
                if alpha is not None:
                    for move in moves:
                        copy = deepcopy(game)
                        copy.commitMove(move, display=False)
                        value = self.search(copy, depth - 1, True, alpha, beta)
                        beta = min(beta, value)
                        if alpha>=beta: return alpha
                        value = beta
                        if depth == self.depth: self.moveDict[move] = value
                else:
                    value = self.inf
                    for move in moves:
                        copy = deepcopy(game)
                        copy.commitMove(move, display=False)
                        value = min(value, self.search(copy, depth - 1, True))
                        if depth == self.depth: self.moveDict[move] = value
            else:
                game.handlePass()
                value = self.search(game, depth - 1, True, alpha, beta)

        if depth == self.depth:
            if len(self.moveDict) == 0: return None
            if maximizing:
                best = max(self.moveDict.items(), key=lambda x: x[1])[1]
            else:
                best = min(self.moveDict.items(), key=lambda x: x[1])[1]
            candidateMoves = list(filter(lambda x: x[1] == best, self.moveDict.items()))
            return choice(candidateMoves)[0]
        else:
            return value
