from src.game import abcMove, abcHeuristic, abcGame,abcBoard

class Board(abcBoard):
    def updateSquare(self, move:abcMove)->None:
        self.squares[move.dest[0]][move.dest[1]].update(move.player)


    def action(self, square):
        print('action')
        print(self.ai.get())
        self.ai.set(self.ai.get()+1)
        print(self.hvar.get())
        print(self.entry.get())


class Move(abcMove):
    @staticmethod
    def isLegal(board:abcBoard, dest, player, src=None) -> bool:
        return not board.getSquare(dest[0],dest[1]).occupied

class Game(abcGame):
    pass