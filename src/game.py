from abc import ABC, abstractmethod


class abcHeuristic(ABC):
    @abstractmethod
    def eval(self, state: list) -> int:
        pass


class Settings:
    def __init__(self, modeVar, depthInputP1, depthInputP2, abVarP1, abVarP2, heurVarP1, heurVarP2):
        self.modeVar = modeVar
        self.depthP1 = depthInputP1
        self.depthP2 = depthInputP2
        self.abVarP1 = abVarP1
        self.abVarP2 = abVarP2
        self.heurVarP1 = heurVarP1
        self.heurVarP2 = heurVarP2

    def getMode(self): return self.modeVar.get()

    def getDepthP1(self): return self.depthP1.get()

    def getDepthP2(self): return self.depthP2.get()

    def isAlphaBetaP1(self): return self.abVarP1.get() == 1

    def isAlphaBetaP2(self): return self.abVarP2.get() == 1

    def getHeurP1(self): return self.heurVarP1.get()

    def getHeurP2(self): return self.heurVarP2.get()

    def __repr__(self):
        return f"Settings: m={self.getMode()},dP1={self.getDepthP1()},dP2={self.getDepthP2()},abP1={self.isAlphaBetaP1()},abP2={self.isAlphaBetaP2()},hP1={self.getHeurP1()},hP2={self.getHeurP2()}"


class Player:
    def __init__(self, type: str):
        self.type = type[0].upper() + type[1:]
        print(self.type)

    def __str__(self):
        return f"Player: type={self.type}"


class Move:
    def __init__(self, dest, player: Player = None, src=None):
        self.dest = dest
        self.src = src
        self.player = player

    @property
    def x(self):
        return self.dest[0]

    @property
    def y(self):
        return self.dest[1]

    def __repr__(self):
        return f"Move: dest={self.dest}, player={self.player.type}"


class abcBoard(ABC):
    def __init__(self, root, game, square, squaresNum: int, squareSize: int):
        self.game = game
        self.root = root
        self.squareSize = squareSize
        self.squaresNum = squaresNum
        self.squares = []
        squareImgs = ('darkgreen', 'lightgreen')
        imgIdx = 0
        for x in range(int(squaresNum ** 0.5)):
            row = []
            imgIdx = int(not imgIdx)
            for y in range(int(squaresNum ** 0.5)):
                row.append(square(self.root, x, y, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))],
                                  action=game.action))
                row[-1].draw()
            self.squares.append(row)

    def getSquare(self, x, y):
        return self.squares[x][y]

    @abstractmethod
    def updateSquare(self, move: Move, display: bool = True) -> None:
        pass

    @abstractmethod
    def __deepcopy__(self, memodict={}):
        pass


class abcGame(ABC):
    def __init__(self, window, board, square, squaresNum: int, squareSize: int, firstPlayer: str, secondPlayer: str,
                 settings: Settings):
        self.window = window
        self.board = board(window, self, square, squaresNum, squareSize)
        self.player1 = Player(firstPlayer)
        self.player2 = Player(secondPlayer)
        self.currPlayer = self.player1
        self.squaresNum = squaresNum
        self.settings = settings

    @abstractmethod
    def __deepcopy__(self, memodict={}):
        pass

    @abstractmethod
    def getPossibleMoves(self) -> list:
        pass

    @abstractmethod
    def commitMove(self, move: Move, display: bool = True) -> None:
        pass

    @abstractmethod
    def gameOver(self) -> str:
        pass

    @abstractmethod
    def evaluate(self) -> float:
        pass

    @abstractmethod
    def isLegalMove(self, move: Move) -> bool:
        pass

    @abstractmethod
    def updateState(self, move: Move = None, display: bool = True) -> None:
        pass

    @abstractmethod
    def action(self, square) -> None:
        pass

    @abstractmethod
    def switchPlayers(self) -> None:
        pass

    @abstractmethod
    def getHeuristic(self) -> abcHeuristic:
        pass
