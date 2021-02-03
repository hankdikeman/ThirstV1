import tkinter as tk
from gamemobs import Player, Beetle, Enemy
import secrets


# game baseclass, inherits from tkinter frame
class Game(tk.Frame):
    MOVE_DIR = ['left', 'right', 'up', 'down']
    NUM_ENEMIES = 10
    MOB_MOVEMENT = 30
    TIMESTEP = 80

    def __init__(self, master):
        super(Game, self).__init__(master)
        self.width = 1400
        self.height = 800
        self.canvas = tk.Canvas(self, bg='#E1C699',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()
        # item list
        self.items = {}
        # generate new player object and store
        self.player = Player(self.canvas, int(
            self.width / 2), int(self.height / 2))
        self.items[self.player.item] = self.player
        # generate "beetle" mob and store
        for beetle_num in range(self.NUM_ENEMIES):
            beetle = Beetle(self.canvas, int(
                self.width / 2), int(self.height / 2))
            self.items[beetle.item] = beetle
        # key bindings for movement
        self.canvas.focus_set()
        # up
        self.canvas.bind('<w>',
                         lambda _: self.player.move(30, 'up'))
        # left
        self.canvas.bind('<a>',
                         lambda _: self.player.move(30, 'left'))
        # down
        self.canvas.bind('<s>',
                         lambda _: self.player.move(30, 'down'))
        # right
        self.canvas.bind('<d>',
                         lambda _: self.player.move(30, 'right'))
        print('screen initialized')

    # game intro sequence to be
    def game_intro(self):
        pass

    # start game sequence
    def start_game(self):
        self.game_intro()
        self.game_loop()

    # game loop event
    def game_loop(self):
        # iterate through entities in entity list
        for item in self.items.values():
            # move if instance of NPC
            if isinstance(item, Enemy):
                item.move(self.MOB_MOVEMENT, secrets.choice(self.MOVE_DIR))
        # add gameloop event to event queue
        self.canvas.after(self.TIMESTEP, lambda: self.game_loop())
