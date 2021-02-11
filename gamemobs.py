from gameobject import GameObject
from mathutils import direction_weighting, move_direction_to_target, coords_to_area
from statistics import mean
from math import sqrt


# entity baseclass (NPC and PC)
class Entity(GameObject):
    MOTION = {'left': [-1, 0],
              'right': [1, 0],
              'up': [0, -1],
              'down': [0, 1]
              }

    def __init__(self, canvas, item, game, max_health):
        self.max_health = max_health
        self.health = max_health
        self.direction = 'left'
        super(Entity, self).__init__(canvas, item, game)

    # getter function for health
    def get_current_health(self):
        return self.health

    # getter function for max health
    def get_max_health(self):
        return self.max_health

    # setter function for current health
    def set_current_health(self, new_health):
        self.health = new_health

    # setter function for max health
    def set_max_health(self, new_max_health):
        self.max_health = new_max_health

    # setter function for current health
    def increment_health(self, delta):
        self.health += delta
        if self.health <= 0:
            self.delete()
        elif self.health > self.max_health:
            self.health = self.max_health

    # direction is a tuple of x and y direction of movement
    def move(self, distance, angle):
        # parse direction from keyword
        x_dir, y_dir = self.MOTION[angle]
        # set new direction in Entity class
        self.direction = angle
        # get coordinates and window info
        l_obj, t_obj, r_obj, b_obj = self.get_position()
        motion = [0, 0]
        # calculate left right move
        if angle == 'left':
            motion[0] = distance * x_dir
        elif angle == 'right':
            motion[0] = distance * x_dir
        # calculate up down move
        elif angle == 'up':
            motion[1] = distance * y_dir
        elif angle == 'down':
            motion[1] = distance * y_dir
        # calculate new center of object
        new_x, new_y = [(l_obj + r_obj) / 2, (t_obj + b_obj) / 2]
        # calculate new position with buffer zone
        new_position = [new_x + motion[0], new_y + motion[1],
                        new_x + motion[0], new_y + motion[1]]
        # check collision over new center of object
        if not self.check_movement_collision(new_position):
            # move in allowed direction by distance
            super(Entity, self).move(*motion)

    # collision checker, true if collision with entity and false if not
    def check_movement_collision(self, new_position):
        # get tuple of overlapping items
        overlapping_items = self.canvas.find_overlapping(*new_position)
        # determine if any of the items are entities
        for item in overlapping_items:
            if self.game.item_is_entity(item):
                return True
        return False


# enemy baseclass, stores reference to oasis
class Enemy(Entity):
    # debug code, must be removed later
    AGRO_ACTIVE = True
    ATTACK_ACTIVE = True

    def __init__(self, canvas, item, game, oasis, max_health):
        self.oasis = oasis
        self.agro = False
        super(Enemy, self).__init__(canvas, item, game, self.MAX_HEALTH)

    def get_next_move(self, player):
        if(self.agro and self.AGRO_ACTIVE):
            return self.targeting_move(player)
        else:
            return self.idle_move()

    def targeting_move(self, player):
        # get distance from player
        dist = [x - y for x, y
                in zip(self.get_position(), player.get_position())]
        # average x distance and y distance
        x_dist, y_dist = (mean([dist[0], dist[2]]), mean([dist[1], dist[3]]))
        # calculate next move and return
        new_direction = move_direction_to_target(x_dist, y_dist)
        return new_direction

    def idle_move(self):
        # get distance from home oasis
        dist = [x - y for x, y
                in zip(self.get_position(), self.oasis.get_position())]
        # average x distance and y distance
        x_dist, y_dist = (mean([dist[0], dist[2]]), mean([dist[1], dist[3]]))
        # calculate next move and return
        new_direction = direction_weighting(x_dist, y_dist)
        return new_direction

    # calculate distance between enemy and player
    def get_distance_to_player(self, player):
        # get one x position and one y position of each object
        enemy_loc = self.get_object_xy()[0:2:1]
        player_loc = player.get_object_xy()[0:2:1]
        # calculate distance with geometric mean and return
        return sqrt(sum([(e - p)**2 for e, p in zip(enemy_loc, player_loc)]))

    # use get_distance_to_player function to determine whether agro
    def check_enemy_agro(self, player, agro_distance):
        self.agro = (self.get_distance_to_player(player) <= agro_distance)
        if(self.agro):
            self.canvas.itemconfig(self.item, fill='blue')
            return True
        else:
            self.canvas.itemconfig(self.item, fill='red')
            return False

    def attack_player(self, player):
        # get current position
        attack_coord = self.get_position_after_move(
            self.game.MOVEMENT_STEP, self.direction)
        # get overlapping area for collision detection
        collision_box = coords_to_area(attack_coord)
        # check if player is overlapping one tile over
        attacked_entities = self.canvas.find_overlapping(*collision_box)
        # loop through bordering entities and attack if player
        for item in attacked_entities:
            if self.game.item_is_player(item) and self.ATTACK_ACTIVE:
                player.increment_health(self.ATTACK_POWER)
                print('player health: ', player.get_current_health())

    # return the current agro status of the enemy mob
    def get_agro_status(self):
        return self.agro


# example enemy class for beetle
class Beetle(Enemy):
    MAX_HEALTH = 50
    ATTACK_POWER = -1
    COLOR = 'red'

    def __init__(self, canvas, x, y, game, oasis):
        # set size of player
        self.radius = 10
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 1, y - self.radius * 1,
                                  x + self.radius * 1, y + self.radius * 1,
                                  fill=self.COLOR)
        super(Beetle, self).__init__(
            canvas, item, game, oasis, self.MAX_HEALTH)


# additional enemy class
class Lizard(Enemy):
    MAX_HEALTH = 50
    ATTACK_POWER = -10
    COLOR = 'brown'

    def __init__(self, canvas, x, y, game, oasis):
        # set size of player
        self.radius = 10
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 1, y - self.radius * 1,
                                  x + self.radius * 1, y + self.radius * 1,
                                  fill=self.COLOR)
        super(Lizard, self).__init__(
            canvas, item, game, oasis, self.MAX_HEALTH)


# player-character class
class Player(Entity):
    MAX_HEALTH = 100
    ATTACK_POWER = -50
    ATTACK_ACTIVE = True
    COLOR = 'green'

    def __init__(self, canvas, x, y, game):
        # set size of player
        self.radius = 15
        #** implement direction indicator here **#
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 0.5, y - self.radius * 1.5,
                                  x + self.radius * 0.5, y + self.radius * 1.5,
                                  fill=self.COLOR)
        super(Player, self).__init__(canvas, item, game, self.MAX_HEALTH)

    def attack_enemy(self):
        # get current position
        attack_coord = self.get_position_after_move(
            self.game.MOVEMENT_STEP, self.direction)
        # get overlapping area for collision detection
        collision_box = coords_to_area(attack_coord)
        # check if player is overlapping one tile over
        attacked_entities = self.canvas.find_overlapping(*collision_box)
        # loop through bordering entities and attack if player
        for item in attacked_entities:
            if self.game.item_is_enemy(item) and self.ATTACK_ACTIVE:
                targeted_enemy = self.game.get_entity_ptr(item)
                targeted_enemy.increment_health(self.ATTACK_POWER)

    def set_direction(self, new_direction):
        self.direction = new_direction
