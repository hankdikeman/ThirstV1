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


class Player(GameObject):
    MOTION = {'left': [-1, 0],
              'right': [1, 0],
              'up': [0, -1],
              'down': [0, 1]
              }

    def __init__(self, canvas, x, y):
        self.radius = 20
        self.direction = [1, 0]
        item = canvas.create_oval(x - self.radius * 0.5, y - self.radius * 1.5,
                                  x + self.radius * 0.5, y + self.radius * 1.5,
                                  fill='green')
        super(Player, self).__init__(canvas, item)

    # direction is a tuple of x and y direction of movement
    def move(self, offset, angle):
        print('player movement ' + angle)
        # parse direction from keyword
        direction = self.MOTION[angle]
        # get coordinates and window info
        coords = self.get_position()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        motion = [0, 0]
        # calculate if x move is possible
        if coords[0] + offset >= 0 and \
                coords[2] + offset <= width:
            motion[0] = offset * direction[0]
            self.direction[0] = direction[0]
        # calculate if y move is possible
        if coords[1] + offset >= 0 and \
                coords[3] + offset <= height:
            motion[1] = offset * direction[1]
            self.direction[1] = direction[1]
        # move in allowed direction by offset
        super(Player, self).move(motion[0], motion[1])
