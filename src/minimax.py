from src.game import abcGame
from copy import deepcopy
from random import choice


class Minimax:
    def __init__(self, game):
        self.game = deepcopy(game)
        self.depth = game.settings.getDepthP1() if game.currPlayer is game.player1 else game.settings.getDepthP2()
        self.inf = int(1e50)
        alphaBeta = game.settings.isAlphaBetaP1() if game.currPlayer is game.player1 else game.settings.isAlphaBetaP2()
        self.alpha = -self.inf if alphaBeta else None
        self.beta = self.inf if alphaBeta else None

    def getBestMove(self):
        maximizing = self.game.currPlayer is self.game.player1
        bestScore = -self.inf if maximizing else self.inf
        bestMovesArr = []
        for move in self.game.getPossibleMoves():
            score = self.search(self.game, self.depth, maximizing, self.alpha, self.beta)
            if (maximizing and score > bestScore) or (not maximizing and score < bestScore):
                bestScore = score
                bestMovesArr = [move]
            elif score == bestScore:
                bestMovesArr.append(move)
        return choice(bestMovesArr) if bestMovesArr else None

    def getWinnerValue(self, game, winner):
        if game.player1.type == winner: return self.inf
        if game.player2.type == winner: return -self.inf
        return 0

    def search(self, game: abcGame, depth: int, maximizing: bool = True, alpha=None, beta=None):
        if (winner := game.gameOver()):
            return self.getWinnerValue(game, winner)
        if depth == 0:
            return game.evaluate()
        moves = game.getPossibleMoves()
        if maximizing:
            if moves:
                value = -self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    newValue = self.search(copy, depth - 1, False, alpha, beta)
                    if alpha is not None:  # alpha-beta
                        alpha = max(alpha, newValue)
                        if alpha >= beta:
                            return alpha
                    else:  # minimax
                        value = max(value, newValue)
                return alpha if alpha is not None else value
            else:
                game.handlePass()
                return self.search(game, depth - 1, False, alpha, beta)
        else:
            if moves:
                value = self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    newValue = self.search(copy, depth - 1, True, alpha, beta)
                    if alpha is not None:  # alpha-beta
                        beta = min(beta, newValue)
                        if alpha >= beta:
                            return beta
                    else:  # minimax
                        value = min(value, newValue)
                return beta if alpha is not None else value
            else:
                game.handlePass()
                return self.search(game, depth - 1, True, alpha, beta)
