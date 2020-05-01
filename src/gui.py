import tkinter as tk
from abc import ABC, abstractmethod
from PIL import Image, ImageTk


class Square:
    def __init__(self, root, x, y, size, squareImg, action):
        self.root = root
        self.x = x
        self.y = y
        self.size = size
        self.kind = squareImg
        self.photo = None
        self.occupied = False
        self.action = action

    def __repr__(self):
        return f'Square: x={self.x}, y={self.y}, size={self.size}, kind={self.kind}, img={self.photo}'

    def draw(self) -> None:
        self.button = tk.Button(self.root, command=self.handle)
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

    def handle(self):
        self.action(self)


class Window(tk.Tk):
    def __init__(self, width, height, title):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.title(title)
        self.geometry(f'{width}x{height}')

    def build(self):
        self.startButton = tk.Button(self, text='Start')
        self.startButton.grid(row=1, column=9, sticky=tk.W)
        self.restartButton = tk.Button(self, text='Restart')
        self.restartButton.grid(row=2, column=9, sticky=tk.W)

        self.aiVar = tk.IntVar()
        self.aiLabel = tk.Label(self, text="Mode:")
        self.aiLabel.grid(row=3, column=9, sticky=tk.W)
        self.aiRadio1 = tk.Radiobutton(self, text="PvsP", variable=self.aiVar, value=1)
        self.aiRadio2 = tk.Radiobutton(self, text="PvsAI", variable=self.aiVar, value=2)
        self.aiRadio3 = tk.Radiobutton(self, text="AIvsAI", variable=self.aiVar, value=3)
        self.aiRadio1.grid(row=3, column=10)
        self.aiRadio2.grid(row=3, column=11)
        self.aiRadio3.grid(row=3, column=12)

        self.depthLabel = tk.Label(self, text="Depth:")
        self.depthLabel.grid(row=5, column=9, sticky=tk.W)
        self.depthVar = tk.StringVar()
        self.depthInput = tk.Entry(self, width=6, textvariable=self.depthVar)
        self.depthVar.set('5')
        self.depthInput.grid(row=5, column=10, sticky=tk.W)

        self.heurVar = tk.IntVar()
        self.heurLabel = tk.Label(self, text="Heuristic:")
        self.heurLabel.grid(row=7, column=9)
        self.heuristicRadio1 = tk.Radiobutton(self, text="Naive", variable=self.heurVar, value=1)
        self.heuristicRadio2 = tk.Radiobutton(self, text="Advanced", variable=self.heurVar, value=2)
        self.heuristicRadio1.grid(row=7, column=10)
        self.heuristicRadio2.grid(row=7, column=11)
        self.heurVar.set(1)

        return self.heurVar, self.depthVar, self.aiVar

    def run(self):
        self.mainloop()
