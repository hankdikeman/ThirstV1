class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Player(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, 0]
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='green')
        super(Player, self).__init__(canvas, item)

    def move(self, offset, direction):
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
