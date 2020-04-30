import tkinter as tk
from abc import ABC, abstractmethod


class Figure(ABC):
    def __init__(self, canvas, x, y, width, height, content=None, color=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = content
        self.color = color

    @abstractmethod
    def draw(self):
        pass

    def __repr__(self):
        return f'x={self.x},y={self.y},width={self.width},height={self.height},color={self.color},content={self.content}'


class Square(Figure):
    def __init__(self, canvas, x, y, size, content=None, color=None):
        super(Square, self).__init__(canvas, x, y, size, size, content, color)
        self.size = size

    def __repr__(self):
        return f'Square: x={self.x},y={self.y}, size={self.size}, color={self.color}'

    def draw(self):
        self.canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.color, width=1)



class Board(ABC):
    def __init__(self, canvas, width, height, squares, squareSize):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.squareSize = squareSize
        self.squares = []
        colors = ('black', 'white')
        colorIdx = 0
        for x in range(int(squares ** 0.5)):
            row = []
            colorIdx = int(not colorIdx)
            for y in range(int(squares ** 0.5)):
                row.append(Square(self.canvas, y * self.squareSize, x * self.squareSize, self.squareSize,
                                  color=colors[(colorIdx := (colorIdx + 1) % len(colors))]))
                row[-1].draw()
            self.squares.append(row)

    # @abstractmethod
    # def updateSquare(self, ):
    #     pass


class Window(tk.Tk):
    def __init__(self, width, height, title):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.place(x=50, y=50)
        self.title(title)
        self.geometry(f'{width}x{height}')

        self.board = Board(self.canvas, width, height, 64, 70)

    def run(self):
        self.mainloop()

    def build(self):
        pass
