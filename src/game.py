from abc import ABC, abstractmethod


class abcHeuristic(ABC):
    @abstractmethod
    def eval(self, state) -> float:
        pass


class abcMove(ABC):
    def __init__(self, dest, player, src=None):
        self.dest = dest
        self.src = src
        self.player = player

    @staticmethod
    @abstractmethod
    def isLegal(board, dest, player, src=None) -> bool:
        pass


class abcBoard(ABC):
    def __init__(self, root, square, squares, squareSize, hvar, entry, ai):
        self.root = root
        self.squareSize = squareSize
        self.squares = []
        self.hvar = hvar
        self.entry = entry
        self.ai = ai
        squareImgs = ('darkgreen', 'lightgreen')
        imgIdx = 0
        for x in range(int(squares ** 0.5)):
            row = []
            imgIdx = int(not imgIdx)
            for y in range(int(squares ** 0.5)):
                row.append(square(self.root, y, x, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))],
                                  action=self.action))
                row[-1].draw()
            self.squares.append(row)

    def getSquare(self, x, y):
        return self.squares[x][y]

    @abstractmethod
    def updateSquare(self, move: abcMove) -> None:
        pass

    @abstractmethod
    def action(self, square):
        pass

class abcGame(ABC):
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def makeMove(self, move: abcMove) -> None:
        pass

    @abstractmethod
    def getMoves(self) -> list:
        pass

    @abstractmethod
    def gameOver(self) -> int:
        pass

    @abstractmethod
    def evaluate(self, heuristic: abcHeuristic) -> float:
        pass

    @abstractmethod
    def updateState(self, state, move: abcMove):
        pass

class Player:
    def __init__(self, type):
        self.type=type

    def __str__(self):
        return "Player: " + self.type
