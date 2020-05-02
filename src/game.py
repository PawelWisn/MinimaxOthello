from abc import ABC, abstractmethod


class abcHeuristic(ABC):
    @abstractmethod
    def eval(self, state:list) -> int:
        pass


class abcMove(ABC):
    def __init__(self, dest, player:str=None, src=None):
        self.dest = dest
        self.src = src
        self.player = player

    @staticmethod
    @abstractmethod
    def isLegal(board, dest, player=None, src=None) -> bool:
        pass


class abcBoard(ABC):
    def __init__(self, root, game, square, squaresNum, squareSize):
        self.game = game
        self.root = root
        self.squareSize = squareSize
        self.squares = []
        squareImgs = ('darkgreen', 'lightgreen')
        imgIdx = 0
        for x in range(int(squaresNum ** 0.5)):
            row = []
            imgIdx = int(not imgIdx)
            for y in range(int(squaresNum ** 0.5)):
                row.append(square(self.root, y, x, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))],
                                  action=self.game.action))
                row[-1].draw()
            self.squares.append(row)

    def getSquare(self, x, y):
        return self.squares[x][y]

    @abstractmethod
    def updateSquare(self, move: abcMove) -> None:
        pass


class abcGame(ABC):
    def __init__(self, window, board, square, squaresNum, squareSize, firstPlayer, secondPlayer, modeVar, depthVar, heurVarP1,
                 heurVarP2):
        self.window = window
        self.board = board(window, self, square, squaresNum, squareSize)
        self.player1 = Player(firstPlayer)
        self.player2 = Player(secondPlayer)
        self.currPlayer = self.player1
        self.modeVar = modeVar
        self.depthVar = depthVar
        self.heurVarP1 = heurVarP1
        self.heurVarP2 = heurVarP2

    @abstractmethod
    def makeMove(self, move: abcMove) -> None:
        pass

    # @abstractmethod
    # def getMoves(self) -> list:
    #     pass
    #
    @abstractmethod
    def gameOver(self) -> bool:
        pass

    #
    # @abstractmethod
    # def evaluate(self, heuristic: abcHeuristic) -> float:
    #     pass
    #
    # @abstractmethod
    # def updateState(self, state, move: abcMove):
    #     pass

    @abstractmethod
    def action(self, square):
        pass


class Player:
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return "Player: " + self.type
