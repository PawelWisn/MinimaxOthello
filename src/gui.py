import tkinter as tk
from abc import ABC, abstractmethod
from PIL import Image, ImageTk
from src.minimax import Move


class Figure(ABC):
    def __init__(self, root, x, y, width, height, content=None, color=None, img=None):
        self.root = root
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = content
        self.color = color
        self.img = img

    @abstractmethod
    def draw(self)->None:
        pass

    def __repr__(self):
        return f'x={self.x},y={self.y},width={self.width},height={self.height},color={self.color},content={self.content}'


class Square(Figure):
    def __init__(self, root, x, y, size, squareImg):
        super(Square, self).__init__(root, x, y, size, size, img=squareImg)
        self.size = size
        self.kind = squareImg

    def __repr__(self):
        return f'Square: x={self.x},y={self.y}, size={self.size}, kind={self.kind}, img={self.img}'

    def draw(self)->None:
        self.button = tk.Button(self.root, command=self.handler)
        self.update('')
        self.button.grid(row=self.x, column=self.y)

    def update(self, player:str)->None:
        if player: player = player[0].upper()+player[1:]
        self.photo = Image.open(f'pictures/{self.kind}{player}.png')
        self.photo = self.photo.resize((self.size, self.size), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.button.config(image=self.photo, width=self.size, height=self.size)

    @abstractmethod
    def handler(self):
        pass


class Board(ABC):
    def __init__(self, root, square, width, height, squares, squareSize):
        self.root = root
        self.width = width
        self.height = height
        self.squareSize = squareSize
        self.squares = []
        squareImgs= ('darkgreen', 'lightgreen')
        imgIdx = 0
        for x in range(int(squares ** 0.5)):
            row = []
            imgIdx = int(not imgIdx)
            for y in range(int(squares ** 0.5)):
                row.append(square(self.root, y, x, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))]))
                row[-1].draw()
            self.squares.append(row)

    @abstractmethod
    def updateSquare(self, move:Move)->None:
        pass


class Window(tk.Tk):
    def __init__(self, width, height, title):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.place(x=50, y=50)
        self.title(title)
        self.geometry(f'{width}x{height}')

    def run(self):
        self.mainloop()

    def build(self, board, square, squaresNum, squareSize):
        self.board = board(self, square, self.width, self.height, squaresNum, squareSize)
