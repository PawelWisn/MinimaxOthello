import tkinter as tk
from PIL import Image, ImageTk
from src.game import Player, Settings
from copy import deepcopy, copy


class Square:
    def __init__(self, root, x, y, size, squareImg, action):
        if root:
            self.root = root
            self.x = x
            self.y = y
            self.size = size
            self.kind = squareImg
            self.photo = None
            self.action = action
            self.player = None

    def __repr__(self):
        return f'Square: x={self.x}, y={self.y}, kind={self.kind}, player={self.player}'

    def draw(self) -> None:
        self.button = tk.Button(self.root, command=self.handle)
        self.update()
        self.button.grid(row=self.x, column=self.y)

    def update(self, player: Player = None, display: bool = True) -> None:
        if player:
            self.player = player
        if display:
            self.display()

    def display(self):
        self.photo = Image.open(f'pictures/{self.kind}{self.player.type if self.player else ""}.png')
        self.photo = self.photo.resize((self.size, self.size), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.photo)
        self.button.config(image=self.photo, width=self.size, height=self.size)

    def getPlayer(self):
        return self.player

    def handle(self):
        self.action(self)

    def occupied(self):
        return self.player is not None

    def __deepcopy__(self, memodict={}):
        new = self.__class__(None, None, None, None, None, None)
        new.__dict__.update(self.__dict__)
        return new


class Window(tk.Tk):
    def __init__(self, width, height, title):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.title(title)
        self.geometry(f'{width}x{height}')

    def onClickStart(self, method):
        self.startButton.configure(command=method)

    def onClickRestart(self, method):
        self.restartButton.configure(command=method)

    def showWinnerPopup(self, winner):
        win = tk.Toplevel()
        win.wm_title("Game Over")
        l = tk.Label(win, text='The winner is: ' + winner)
        l.grid(row=0,column=0)
        b = tk.Button(win,text="OK",command=win.destroy)
        b.grid(row=1,column=0)

    def build(self):  # to optimize
        self.startButton = tk.Button(self, text='Start')
        self.startButton.grid(row=0, column=9, sticky=tk.W)
        self.restartButton = tk.Button(self, text='Restart')
        self.restartButton.grid(row=0, column=10, sticky=tk.W)

        self.modeVar = tk.IntVar()
        self.modeLabel = tk.Label(self, text="Mode:")
        self.modeLabel.grid(row=1, column=9, sticky=tk.W)
        self.modeRadio1 = tk.Radiobutton(self, text="PvsP", variable=self.modeVar, value=0)
        self.modeRadio2 = tk.Radiobutton(self, text="PvsAI", variable=self.modeVar, value=1)
        self.modeRadio3 = tk.Radiobutton(self, text="AIvsAI", variable=self.modeVar, value=2)
        self.modeVar.set(2)
        self.modeRadio1.grid(row=1, column=10)
        self.modeRadio2.grid(row=1, column=11)
        self.modeRadio3.grid(row=1, column=12)

        self.depthLabelP1 = tk.Label(self, text="Depth AI 1:")
        self.depthLabelP1.grid(row=2, column=9, sticky=tk.W)
        self.depthVarP1 = tk.StringVar()
        self.depthInputP1 = tk.Entry(self, width=6, textvariable=self.depthVarP1)
        self.depthVarP1.set('3')
        self.depthInputP1.grid(row=2, column=10, sticky=tk.W)

        self.depthLabelP2 = tk.Label(self, text="Depth AI 2:")
        self.depthLabelP2.grid(row=3, column=9, sticky=tk.W)
        self.depthVarP2 = tk.StringVar()
        self.depthInputP2 = tk.Entry(self, width=6, textvariable=self.depthVarP2)
        self.depthVarP2.set('3')
        self.depthInputP2.grid(row=3, column=10, sticky=tk.W)

        self.abVarP1 = tk.IntVar()
        self.abLabelP1 = tk.Label(self, text="Alpha-Beta\nAI 1:")
        self.abLabelP1.grid(row=4, column=9)
        self.abRadio1P1 = tk.Radiobutton(self, text="Off", variable=self.abVarP1, value=0)
        self.abRadio2P1 = tk.Radiobutton(self, text="On", variable=self.abVarP1, value=1)
        self.abRadio1P1.grid(row=4, column=10)
        self.abRadio2P1.grid(row=4, column=11)
        self.abVarP1.set(1)

        self.abVarP2 = tk.IntVar()
        self.abLabelP2 = tk.Label(self, text="Alpha-Beta\nAI 2:")
        self.abLabelP2.grid(row=5, column=9)
        self.abRadio1P2 = tk.Radiobutton(self, text="Off", variable=self.abVarP2, value=0)
        self.abRadio2P2 = tk.Radiobutton(self, text="On", variable=self.abVarP2, value=1)
        self.abRadio1P2.grid(row=5, column=10)
        self.abRadio2P2.grid(row=5, column=11)
        self.abVarP2.set(1)

        self.heurVarP1 = tk.IntVar()
        self.heurLabelP1 = tk.Label(self, text="Heuristic\nAI 1:")
        self.heurLabelP1.grid(row=6, column=9)
        self.heuristicRadio1P1 = tk.Radiobutton(self, text="CoinParity", variable=self.heurVarP1, value=0)
        self.heuristicRadio2P1 = tk.Radiobutton(self, text="Weights", variable=self.heurVarP1, value=1)
        self.heuristicRadio3P1 = tk.Radiobutton(self, text="Mobility", variable=self.heurVarP1, value=2)
        self.heuristicRadio1P1.grid(row=6, column=10)
        self.heuristicRadio2P1.grid(row=6, column=11)
        self.heuristicRadio3P1.grid(row=6, column=12)
        self.heurVarP1.set(0)

        self.heurVarP2 = tk.IntVar()
        self.heurLabelP2 = tk.Label(self, text="Heuristic\nAI 2:")
        self.heurLabelP2.grid(row=7, column=9)
        self.heuristicRadio1P2 = tk.Radiobutton(self, text="CoinParity", variable=self.heurVarP2, value=0)
        self.heuristicRadio2P2 = tk.Radiobutton(self, text="Weights", variable=self.heurVarP2, value=1)
        self.heuristicRadio3P2 = tk.Radiobutton(self, text="Mobility", variable=self.heurVarP2, value=2)
        self.heuristicRadio1P2.grid(row=7, column=10)
        self.heuristicRadio2P2.grid(row=7, column=11)
        self.heuristicRadio3P2.grid(row=7, column=12)
        self.heurVarP2.set(0)

        self.nextPlayerLabel = tk.Label(self, text="player:")
        self.nextPlayerInfo = tk.Label(self, text="todo")
        self.nextPlayerLabel.grid(row=7, column=0)
        self.nextPlayerInfo.grid(row=7, column=1)

        return Settings(self.modeVar, self.depthInputP1, self.depthInputP2, self.abVarP1, self.abVarP2, self.heurVarP1,
                        self.heurVarP2)

    def run(self):
        self.mainloop()
