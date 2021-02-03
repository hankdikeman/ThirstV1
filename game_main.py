import tkinter as tk
from game import Game
from gameobject import Player

if __name__ == '__main__':
    # generate root tkinter window
    root = tk.Tk()
    root.title('Thirst')
    # initialize tkinter frame and begin main loop
    game = Game(root)
    game.after(1000, game.start_game())
    game.mainloop()
    # game.start_game()
