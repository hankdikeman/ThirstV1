import tkinter as tk
from game import Game
from gameobject import Player

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Thirst')
    game = Game(root)
    game.mainloop()
