import tkinter as tk
from game import Game
from gameobject import Player

# main game function
if __name__ == '__main__':
    # generate root tkinter window
    root = tk.Tk()
    root.title('Thirst')
    # initialize tkinter frame and begin main loop
    game = Game(root)
    # add game start sequence to event queue
    game.after(1000, game.start_game())
    # begin main event loop
    game.mainloop()
