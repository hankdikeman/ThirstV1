from gameobject import GameObject


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
        # get coordinates and window info
        l_obj, t_obj, r_obj, b_obj = self.get_position()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        motion = [0, 0]
        # calculate if left-right move is possible
        if angle == 'left':
            if l_obj - distance >= 0:
                motion[0] = distance * x_dir
        elif angle == 'right':
            if r_obj + distance <= width:
                motion[0] = distance * x_dir
        # calculate if up-down move is possible
        elif angle == 'up':
            if t_obj - distance >= 0:
                motion[1] = distance * y_dir
        elif angle == 'down':
            if b_obj + distance <= height:
                motion[1] = distance * y_dir
        # set new direction
        self.direction = self.MOTION[angle]
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
                print("collision")
                return True
        return False


# enemy baseclass, stores reference to oasis
class Enemy(Entity):
    def __init__(self, canvas, item, game, oasis, max_health):
        self.oasis = oasis
        super(Enemy, self).__init__(canvas, item, game, self.MAX_HEALTH)


# example enemy class for beetle
class Beetle(Enemy):
    MAX_HEALTH = 50

    def __init__(self, canvas, x, y, game, oasis):
        # set size of player
        self.radius = 10
        # set initial direction
        self.direction = [1, 0]
        # set max health
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 1, y - self.radius * 1,
                                  x + self.radius * 1, y + self.radius * 1,
                                  fill='red')
        super(Beetle, self).__init__(
            canvas, item, game, oasis, self.MAX_HEALTH)


# additional enemy class
class Lizard(Enemy):
    MAX_HEALTH = 50

    def __init__(self, canvas, x, y, game, oasis):
        # set size of player
        self.radius = 10
        # set initial direction
        self.direction = [1, 0]
        # set max health
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 1, y - self.radius * 1,
                                  x + self.radius * 1, y + self.radius * 1,
                                  fill='brown')
        super(Lizard, self).__init__(
            canvas, item, game, oasis, self.MAX_HEALTH)


# player-character class
class Player(Entity):
    MAX_HEALTH = 100

    def __init__(self, canvas, x, y, game):
        # set size of player
        self.radius = 15
        # set initial direction
        self.direction = [1, 0]
        # set direction indicator
        #** implement direction indicator here **#
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 0.5, y - self.radius * 1.5,
                                  x + self.radius * 0.5, y + self.radius * 1.5,
                                  fill='green')
        super(Player, self).__init__(canvas, item, game, self.MAX_HEALTH)
