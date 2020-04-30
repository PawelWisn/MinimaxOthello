from src.gui import Window
from src.reversi import ReversiSquare, ReversiBoard

window = Window(1150,800,'Reversi')
window.build(ReversiBoard,ReversiSquare,64,100)
window.run()