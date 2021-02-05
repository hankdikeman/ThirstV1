import tkinter as tk
from game import Game

# main game function
if __name__ == '__main__':
    # generate root tkinter window
    root = tk.Tk()
    root.title('Thirst')
    # initialize tkinter frame and begin main loop
    game = Game(root)
    # add game start sequence to event queue
    game.after(500, lambda: game.start_game())
    # begin main event loop
    game.mainloop()
