from src.gui import Window
from src.reversi import Square, Board

window = Window(1150, 800, 'Reversi')
window.build(Board, Square, 64, 100)
window.run()
