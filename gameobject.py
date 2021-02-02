class GameObject(object):
    # initialize item and place within canvas
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    # get position (boundaries) of item on canvas
    def get_position(self):
        return self.canvas.coords(self.item)

    # move object on canvas
    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    # delete item
    def delete(self):
        self.canvas.delete(self.item)


class Entity(GameObject):
    MOTION = {'left': [-1, 0],
              'right': [1, 0],
              'up': [0, -1],
              'down': [0, 1]
              }

    # direction is a tuple of x and y direction of movement
    def move(self, distance, angle):
        print('object movement ' + angle)
        # parse direction from keyword
        x_dir, y_dir = self.MOTION[angle]
        # get coordinates and window info
        print(self.get_position())
        l_obj, t_obj, r_obj, b_obj = self.get_position()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        motion = [0, 0]
        # calculate if left-right move is possible
        if angle == 'left':
            if l_obj - distance >= 0:
                motion[0] = distance * x_dir
        if angle == 'right':
            if r_obj + distance <= width:
                motion[0] = distance * x_dir
        # calculate if up-down move is possible
        if angle == 'up':
            if t_obj - distance >= 0:
                motion[1] = distance * y_dir
        if angle == 'down':
            if b_obj + distance <= height:
                motion[1] = distance * y_dir
        # set new direction
        self.direction = self.MOTION[angle]
        print(self.direction)
        # move in allowed direction by distance
        super(Entity, self).move(*motion)


# generic enemy class
class Enemy(Entity):
    pass


# example enemy class for beetle
class Beetle(Enemy):
    def __init__(self, canvas, x, y):
        # set size of player
        self.radius = 20
        # set initial direction
        self.direction = [1, 0]
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 1, y - self.radius * 1,
                                  x + self.radius * 1, y + self.radius * 1,
                                  fill='red')
        super(Player, self).__init__(canvas, item)


# core player-character class
class Player(Entity):
    def __init__(self, canvas, x, y):
        # set size of player
        self.radius = 20
        # set initial direction
        self.direction = [1, 0]
        # generate new player and store on canvas
        item = canvas.create_oval(x - self.radius * 0.5, y - self.radius * 1.5,
                                  x + self.radius * 0.5, y + self.radius * 1.5,
                                  fill='green')
        super(Player, self).__init__(canvas, item)
