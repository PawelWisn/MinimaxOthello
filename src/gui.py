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
    def __init__(self, root, x, y, size, content=None, squareImg=None):
        super(Square, self).__init__(root, x, y, size, size, content, img=squareImg)
        self.size = size

    def __repr__(self):
        return f'Square: x={self.x},y={self.y}, size={self.size}, img={self.img}'

    def draw(self)->None:
        self.button = tk.Button(self.root)
        self.photo = Image.open(f'pictures/{self.img}.png')
        self.photo = self.photo.resize((self.size,self.size),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.button.config(image=self.photo, width=self.size, height=self.size)
        self.button.grid(row=self.x, column=self.y)

    # @abstractmethod
    # def update(self, imgName:str)->None:
    #     pass

class Board(ABC):
    def __init__(self, root, width, height, squares, squareSize):
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
                row.append(Square(self.root, y, x, self.squareSize,
                                  squareImg=squareImgs[(imgIdx := (imgIdx + 1) % len(squareImgs))]))
                row[-1].draw()
            self.squares.append(row)

    # @abstractmethod
    # def updateSquare(self, move:Move)->None:
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

        self.board = Board(self, width, height, 64, 100)

    def run(self):
        self.mainloop()

    def build(self):
        pass
