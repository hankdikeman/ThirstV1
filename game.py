import tkinter as tk
import pygame
from os import path
from gamemobs import Player, Beetle, Enemy, Lizard
from gamestructures import Oasis
from mathutils import coords_to_area
from secrets import choice


# game baseclass, inherits from tkinter frame
class Game(tk.Frame):
    PAUSED = False
    MOVE_DIR = ['left', 'right', 'up', 'down']
    MOVEMENT_STEP = 30
    NUM_OASES = 5
    TIMESTEP = 300
    MOB_TIMESTEP = 300
    AGRO_DISTANCE = 150
    BACKGROUND_MUSIC = path.join('music', 'jazzy.wav')

    def __init__(self, master):
        super(Game, self).__init__(master)
        # define sound mixer
        pygame.mixer.init()
        # play background music
        pygame.mixer.music.load(self.BACKGROUND_MUSIC)
        pygame.mixer.music.play(-1)
        # set window width and height and create canvas object
        self.width = 1400
        self.height = 800
        self.canvas = tk.Canvas(self, bg='#E1C699',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()
        self.init_structs_and_entities()
        self.set_bindings()

    def init_structs_and_entities(self):
        # entity and structure dictionaries
        self.entities = {}
        self.structures = {}
        # generate new player object and store
        self.player = Player(self.canvas, int(
            self.width / 2), int(self.height / 2), self)
        self.entities[self.player.item] = self.player
        # generate oasis structure and store
        for i in range(self.NUM_OASES):
            # generate new randomized oasis position and check overlaps
            new_oasis_position = self.random_canvas_position()
            while(self.canvas.find_overlapping(*Oasis.generate_oasis_boundaries(*new_oasis_position))):
                new_oasis_position = self.random_canvas_position()
            # generate new oasis
            oasis = Oasis(self.canvas, self, *new_oasis_position)
            # merge oasis and game entity list
            self.entities = {**self.entities, **oasis.get_enemylist()}
            # store oasis in structure list
            self.structures[oasis.item] = oasis

    def set_bindings(self):
        # key bindings for movement
        self.canvas.focus_set()
        # up
        self.canvas.bind('<w>',
                         lambda _: self.shift_game('up'))
        # left
        self.canvas.bind('<a>',
                         lambda _: self.shift_game('left'))
        # down
        self.canvas.bind('<s>',
                         lambda _: self.shift_game('down'))
        # right
        self.canvas.bind('<d>',
                         lambda _: self.shift_game('right'))
        self.canvas.bind('<space>',
                         lambda _: self.player.attack_enemy())
        self.canvas.bind('p', lambda _: self.pause_game())

    def pause_game(self):
        if not self.PAUSED:
            self.PAUSED = not self.PAUSED
            self.PAUSED_MSG = self.canvas.create_text(
                self.width / 2,
                self.height / 2,
                fill="black",
                font="Times 100 bold",
                text="GAME PAUSED")
        else:
            self.canvas.delete(self.PAUSED_MSG)
            self.PAUSED = not self.PAUSED

    # get random canvas position (for structure generation)
    def random_canvas_position(self):
        return [choice(range(0, self.width)), choice(range(0, self.height))]

    # shifts all objects but player one step in given direction on game grid
    def shift_game(self, angle):
        if not self.PAUSED:
            # set new player direction
            self.player.set_direction(angle)
            # get new canvas coordinates of player after shift
            new_position = self.player.get_position_after_move(
                self.MOVEMENT_STEP, angle)
            # some BS needed to convert (x,y) point to (x1, y1, x2, y2) area
            # not useful enough to justify a dedicated function yet
            new_position_area = coords_to_area(new_position)
            # check to make sure no entities are overlapping new position
            if not self.player.check_movement_collision(new_position_area):
                for _, item in {**self.entities, **self.structures}.items():
                    if not isinstance(item, Player):
                        item.shift(self.MOVEMENT_STEP, angle)

    ###############################
    # ENTITY/STRUCTURE MANAGEMENT #
    ###############################

    # remove a structure using
    def remove_structure(self, item):
        print('removing struct ' + str(self.structures[item]))
        del self.structures[item]

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

    # checks whether item is a structure
    def item_is_structure(self, item):
        return item in self.structures.keys()

    # checks whether item is an enemy
    def item_is_enemy(self, item):
        if item in self.entities.keys():
            return isinstance(self.entities[item], Enemy)
        else:
            return False

    # checks whether item is the player
    def item_is_player(self, item):
        if item in self.entities.keys():
            return isinstance(self.entities[item], Player)
        else:
            return False

    # returns grid position nearest to x and y on coordinate grid
    def nearest_grid_node(self, x, y):
        player_x, player_y = self.player.get_object_xy()
        node_x = x - ((x - player_x) % self.MOVEMENT_STEP)
        node_y = y - ((y - player_y) % self.MOVEMENT_STEP)
        return node_x, node_y

    ##############
    # GAME LOOPS #
    ##############

    # game intro sequence to be
    def game_intro(self):
        intro_header = self.canvas.create_text(
            self.width / 2,
            self.height / 4,
            fill="black",
            font="Times 80 bold",
            text="THIRST")
        self.canvas.after(4000, lambda: self.canvas.delete(intro_header))

    # start game sequence
    def start_game(self):
        # create intro title and schedule removal after period of time
        self.game_intro()
        # run game loop
        self.game_loop()
        self.mob_movement_loop()

    # game loop event
    def game_loop(self):
        # add gameloop event to event queue
        self.canvas.after(self.TIMESTEP, lambda: self.game_loop())

    # mob movement timesteps
    def mob_movement_loop(self):
        if not self.PAUSED:
            # iterate through entities in entity list
            # list is necessary because dictionary may change size during loop
            for item in list(self.entities.values()):
                # move if instance of NPC
                if isinstance(item, Enemy):
                    # get next move direction
                    move_direction = item.get_next_move(self.player)
                    # attempt to move in that direction
                    item.move(self.MOVEMENT_STEP, move_direction)
                    # check distance to player
                    if(item.check_enemy_agro(self.player, self.AGRO_DISTANCE)):
                        # print('agro worked')
                        item.attack_player(self.player)

        self.canvas.after(self.MOB_TIMESTEP, lambda: self.mob_movement_loop())
