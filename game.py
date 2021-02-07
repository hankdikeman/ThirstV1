import tkinter as tk
from gamemobs import Player, Beetle, Enemy
from gamestructures import Oasis
import secrets


# game baseclass, inherits from tkinter frame
class Game(tk.Frame):
    MOVE_DIR = ['left', 'right', 'up', 'down']
    MOB_MOVEMENT = 30
    TIMESTEP = 80

    def __init__(self, master):
        super(Game, self).__init__(master)
        # set window width and height and create canvas object
        self.width = 1400
        self.height = 800
        self.canvas = tk.Canvas(self, bg='#E1C699',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()
        # entity and structure dictionaries
        self.entities = {}
        self.structures = {}
        # generate new player object and store
        self.player = Player(self.canvas, int(
            self.width / 2), int(self.height / 2), self)
        self.entities[self.player.item] = self.player

        # generate oasis structure and store
        oasis = Oasis(self.canvas, self, self.width / 4, self.height / 4)
        self.entities = {**self.entities, **oasis.get_enemylist()}

        self.structures[oasis.item] = oasis
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
        print(self.entities)

    # remove object method, subcontracts to *_entity or *_structure
    def remove_object(self, item):
        if item in self.entities.keys():
            self.remove_entity(item)
        elif item in self.structures.keys():
            self.remove_structure(item)

    # remove item from item list after deletion
    def remove_entity(self, item):
        print('removing entity ' + str(self.entities[item]))
        del self.entities[item]

    def remove_structure(self, item):
        print('removing struct ' + str(self.structures[item]))
        del self.structures[item]

    # generic method to return pointer to game_object, less optimal
    def get_item_ptr(self, item):
        if item in self.entities.keys():
            return self.entities[item]
        elif item in self.structures.keys():
            return self.structures[item]
        return None

    # method to return pointer to entity
    def get_entity_ptr(self, item):
        return self.entities[item]

    # method to return pointer to structure
    def get_structure_ptr(self, item):
        return self.structures[item]

    # returns true if item is an entity
    def item_is_entity(self, item):
        return item in self.entities.keys()

    # game intro sequence to be
    def game_intro(self):
        return self.canvas.create_text(self.width / 2, self.height / 4, fill="black", font="Times 80 bold",
                                       text="THIRST")

    # start game sequence
    def start_game(self):
        # create intro title and schedule removal after period of time
        intro_header = self.game_intro()
        self.canvas.after(4000, lambda: self.canvas.delete(intro_header))
        # run game loop
        self.game_loop()

    # game loop event
    def game_loop(self):
        # iterate through entities in entity list
        # list is necessary because dictionary may change size during loop
        for item in list(self.entities.values()):
            # move if instance of NPC
            if isinstance(item, Enemy):
                item.move(self.MOB_MOVEMENT, secrets.choice(self.MOVE_DIR))
                # item.increment_health(-1)
        # add gameloop event to event queue
        self.canvas.after(self.TIMESTEP, lambda: self.game_loop())
