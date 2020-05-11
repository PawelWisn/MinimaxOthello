from src.game import Player, abcBoard, Move, abcGame
from copy import deepcopy


class Minimax:
    def __init__(self, game, alphaBeta=False):
        self.game = deepcopy(game)
        self.alphaBeta = alphaBeta
        self.depth = game.settings.getDepthP1() if game.currPlayer is game.player1 else game.settings.getDepthP2()
        self.inf = int(1e50)
        self.moveDict = {}

    def getBestMove(self):
        out = self.search(self.game, self.depth, self.game.currPlayer is self.game.player1)
        print('bestmove=',out)
        return out

    def getWinnerValue(self,game, winner):
        if game.player1.type==winner: return self.inf
        if game.player2.type==winner: return -self.inf
        return 0

    def search(self, game: abcGame, depth: int, maximizing: bool = True):
        if (winner:=game.gameOver()):
            return self.getWinnerValue(game,winner)

        if depth == 0:
            return game.getHeuristic().eval(game.board.squares)

        moves = game.getPossibleMoves()
        if maximizing:
            if moves:
                value = -self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    value = max(value, self.search(copy, depth - 1, False))
                    if depth == self.depth: self.moveDict[move] = value
            else:
                value = self.search(game, depth - 1, False)
        else:
            if moves:
                value = self.inf
                for move in moves:
                    copy = deepcopy(game)
                    copy.commitMove(move, display=False)
                    value = min(value, self.search(copy, depth - 1, True))
                    if depth == self.depth: self.moveDict[move] = value
            else:
                value = self.search(game, depth - 1, True)

        if depth==self.depth:
            if maximizing: return max(self.moveDict.items(),key=lambda x:x[1])[0]
            else: return min(self.moveDict.items(),key=lambda x:x[1])[0]
        else:
            return value
