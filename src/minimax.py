from src.game import Player, abcBoard, Move, abcGame
from copy import deepcopy


class Minimax:
    def __init__(self, game, alphaBeta=False):
        self.game = deepcopy(game)
        self.gameCopy = game
        self.alphaBeta = alphaBeta
        self.heuristic = game.getHeuristic()
        self.depth = game.settings.getDepthP1() if game.currPlayer is game.player1 else game.settings.getDepthP2()
        self.inf = int(1e50)

    def getBestMove(self):
        out = self.search(self.game, self.depth, self.game.currPlayer is self.game.player1)
        self.game = self.gameCopy
        return out

    def search(self, game: abcGame, depth: int, maximizing: bool = True) -> Move:
        print('depth',depth)
        print(game.getPossibleMoves())
        if depth == 0 or game.gameOver():
            return self.heuristic.eval(game.board.squares)
        moves = game.getPossibleMoves()
        if maximizing:
            if moves:
                value = -self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    value = max(value, self.search(copy, depth - 1, False))
            else:
                value = self.search(game, depth - 1, False)
        else:
            if moves:
                value = self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    value = min(value, self.search(copy, depth - 1, True))
            else:
                value = self.search(game, depth - 1, True)
        return value
