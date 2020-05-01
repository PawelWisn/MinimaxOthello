from src.game import abcMove, abcHeuristic, abcGame, abcBoard


class Board(abcBoard):
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.freeSquares = len(self.squares) ** 2

    def updateSquare(self, move: abcMove) -> None:
        self.squares[move.dest[1]][move.dest[0]].update(move.player)
        self.freeSquares -= 1


class Move(abcMove):
    @staticmethod
    def isLegal(board: abcBoard, dest, player=None, src=None) -> bool:
        if board.getSquare(dest[1], dest[0]).occupied:
            return False
        # if not change -> False
        return True


class Game(abcGame):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.passCounter = 0

    def action(self, square):
        print(repr(square))
        dest = square.x, square.y
        if Move.isLegal(self.board, dest):
            move = Move(dest, self.currPlayer.type)
            self.makeMove(move)

    def makeMove(self, move: abcMove) -> None:
        self.passCounter = 0
        self.board.updateSquare(move)

        if True:  # if next player has move
            self.currPlayer = self.player1 if self.currPlayer is self.player2 else self.player2
        else:
            pass  # display  player has no move

    def gameOver(self) -> int:
        if not self.board.freeSquares:
            return True
        # if two passes in a row -> True
        return False


class CoinParity(abcHeuristic):
    def eval(self, state: list) -> float:
        black = 0
        white = 0
        for row in state:
            for square in row:
                player = square.getPlayer()
                if player == 'White':
                    white += 1
                elif player == 'Black':
                    black += 1
        return white - black

class Weights(abcHeuristic):
    def __init__(self, *args, **kwargs):
        super(Weights, self).__init__(*args,**kwargs)
        self. weights = {(0,0):4, (0,7):4, (7,0):4,(7,7):4,(0,1):-3,(0,6):-3,(1,0):-3,(1,7):-3,(6,0):-3,(6,7):-3,(7,1):-3,(7,6):-3,(1,1):-4,(1,6):-4,(6,1):-4,(6,6):-4,(0,2):2,(0,3):2,(0,4):2,(0,5):2,(7,2):2,(7,3):2,(7,4):2,(7,5):2,(2,0):2,(3,0):2,(4,0):2,(5,0):2,(2,7):2,(3,7):2,(4,7):2,(5,7):2,(1,2):-1,(1,3):-1,(1,4):-1,(1,5):-1,(6,2):-1,(6,3):-1,(6,4):-1,(6,5):-1,(2,1):1,(3,1):-1,(4,1):-1,(5,1):-1,(2,6):-1,(3,6):-1,(4,6):-1,(5,6):-1,(2,2):1,(2,3):0,(2,4):0,(2,5):1,(5,2):1,(5,3):0,(5,4):0,(5,5):1,(3,2):0,(4,2):0,(3,5):0,(4,5):0,(3,3):1,(3,4):1,(4,3):1,(4,4):1}
        print(len(self.weights.keys()))



    def eval(self, state: list) -> float:
        pass