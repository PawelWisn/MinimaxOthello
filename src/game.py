from abc import ABC, abstractmethod


class abcHeuristic(ABC):
    @abstractmethod
    def eval(self, state) -> float:
        pass


class abcMove(ABC):
    def __init__(self, dest, player, src=None):
        self.dest = dest
        self.src = src
        self.player = 'Black'

    @staticmethod
    @abstractmethod
    def isLegal(board, dest, player, src=None) -> bool:
        pass


class abcBoard(ABC):
    def __init__(self, root, square, squares, squareSize):
        self.root = root
        self.squareSize = squareSize
        self.squares = []
        squareImgs = ('darkgreen', 'lightgreen')
        imgIdx = 0
        for x in range(int(squares ** 0.5)):
            row = []
            imgIdx = int(not imgIdx)
            for y in range(int(squares ** 0.5)):
                row.append(square(self.root, y, x, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))]))
                row[-1].draw()
            self.squares.append(row)

    def getSquare(self, x, y):
        return self.squares[x][y]

    @abstractmethod
    def updateSquare(self, move: abcMove) -> None:
        pass


class abcGame(ABC):
    def __init__(self, state):
        self.state = state

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
