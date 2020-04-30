from abc import ABC, abstractmethod


class Heuristic(ABC):
    @abstractmethod
    def eval(self, state) -> float:
        pass


class Move:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


class Game(ABC):
    def __init__(self, state):
        self.state = state

    @abstractmethod
    def makeMove(self, move: Move) -> None:
        pass

    @abstractmethod
    def getMoves(self) -> list:
        pass

    @abstractmethod
    def gameOver(self) -> int:
        pass

    @abstractmethod
    def evaluate(self, heuristic: Heuristic) -> float:
        pass
