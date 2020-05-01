import tkinter as tk
from abc import ABC, abstractmethod
from PIL import Image, ImageTk


class abcSquare(ABC):
    def __init__(self, root, x, y, size, squareImg):
        self.root = root
        self.x = x
        self.y = y
        self.size = size
        self.kind = squareImg
        self.photo=None
        self.occupied = False

    def __repr__(self):
        return f'Square: x={self.x}, y={self.y}, size={self.size}, kind={self.kind}, img={self.photo}'

    def draw(self) -> None:
        self.button = tk.Button(self.root, command=self.handler)
        self.update('')
        self.button.grid(row=self.x, column=self.y)

    def update(self, player: str) -> None:
        if player:
            player = player[0].upper() + player[1:]
            self.occupied = True
        self.photo = Image.open(f'pictures/{self.kind}{player}.png')
        self.photo = self.photo.resize((self.size, self.size), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.button.config(image=self.photo, width=self.size, height=self.size)

    @abstractmethod
    def handler(self):
        pass


class Window(tk.Tk):
    def __init__(self, width, height, title):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.title(title)
        self.geometry(f'{width}x{height}')

    def run(self):
        self.mainloop()
