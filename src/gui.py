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
        return f'Square: x={self.x}, y={self.y}, kind={self.kind}, taken={self.occupied}'

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

        self.modeVar = tk.IntVar()
        self.modeLabel = tk.Label(self, text="Mode:")
        self.modeLabel.grid(row=3, column=9, sticky=tk.W)
        self.modeRadio1 = tk.Radiobutton(self, text="PvsP", variable=self.modeVar, value=0)
        self.modeRadio2 = tk.Radiobutton(self, text="PvsAI", variable=self.modeVar, value=1)
        self.modeRadio3 = tk.Radiobutton(self, text="AIvsAI", variable=self.modeVar, value=2)
        self.modeVar.set(0)
        self.modeRadio1.grid(row=3, column=10)
        self.modeRadio2.grid(row=3, column=11)
        self.modeRadio3.grid(row=3, column=12)

        self.depthLabel = tk.Label(self, text="Depth:")
        self.depthLabel.grid(row=5, column=9, sticky=tk.W)
        self.depthVar = tk.StringVar()
        self.depthInput = tk.Entry(self, width=6, textvariable=self.depthVar)
        self.depthVar.set('5')
        self.depthInput.grid(row=5, column=10, sticky=tk.W)

        self.heurVarP1 = tk.IntVar()
        self.heurLabelP1 = tk.Label(self, text="Heuristic\nAI 1:")
        self.heurLabelP1.grid(row=6, column=9)
        self.heuristicRadio1P1 = tk.Radiobutton(self, text="Naive", variable=self.heurVarP1, value=0)
        self.heuristicRadio2P1 = tk.Radiobutton(self, text="Advanced", variable=self.heurVarP1, value=1)
        self.heuristicRadio1P1.grid(row=6, column=10)
        self.heuristicRadio2P1.grid(row=6, column=11)
        self.heurVarP1.set(0)

        self.heurVarP2 = tk.IntVar()
        self.heurLabelP2 = tk.Label(self, text="Heuristic\nAI 2:")
        self.heurLabelP2.grid(row=7, column=9)
        self.heuristicRadio1P2 = tk.Radiobutton(self, text="Naive", variable=self.heurVarP2, value=0)
        self.heuristicRadio2P2 = tk.Radiobutton(self, text="Advanced", variable=self.heurVarP2, value=1)
        self.heuristicRadio1P2.grid(row=7, column=10)
        self.heuristicRadio2P2.grid(row=7, column=11)
        self.heurVarP2.set(0)

        return self.modeVar, self.depthVar, self.heurVarP1, self.heurVarP2

    def run(self):
        self.mainloop()


