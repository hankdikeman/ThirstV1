import tkinter as tk
from gameobject import Player


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
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
        # key bindings for movement
        self.canvas.bind('<W>',
                         lambda _: self.player.move(10, [-1, 0]))
        self.canvas.bind('<A>',
                         lambda _: self.player.move(10, [1, 0]))
        self.canvas.bind('<S>',
                         lambda _: self.player.move(10, [0, -1]))
        self.canvas.bind('<D>',
                         lambda _: self.player.move(10, [0, 1]))
        print('screen initialized')

    def game_intro(self):
        pass

    def start_game(self):
        self.game_intro()
