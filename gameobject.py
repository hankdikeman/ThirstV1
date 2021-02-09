from statistics import mean


# game object baseclass
class GameObject(object):
    # initialize item and place within canvas
    def __init__(self, canvas, item, game):
        self.canvas = canvas
        self.item = item
        self.game = game

    # get position (boundaries) of item on canvas
    def get_position(self):
        return self.canvas.coords(self.item)

    def get_object_xy(self):
        x1, y1, x2, y2 = self.canvas.coords(self.item)
        return mean([x1, x2]), mean([y1, y2])

    # move object on canvas
    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    # shift function for player movement
    def shift(self, delta, angle):
        move = self.get_movement_vector(delta, angle)
        self.canvas.move(self.item, *move)

    def get_position_after_move(self, delta, angle):
        position = list(self.get_object_xy())
        # change x y coordinates by given magnitude
        if angle == 'left':
            position[0] += -delta
        elif angle == 'right':
            position[0] += delta
        elif angle == 'up':
            position[1] += -delta
        elif angle == 'down':
            position[1] += delta
        return position

    def get_movement_vector(self, delta, angle):
        move = [0, 0]
        # change x y coordinates by given magnitude
        if angle == 'left':
            move[0] = delta
        elif angle == 'right':
            move[0] = -delta
        elif angle == 'up':
            move[1] = delta
        elif angle == 'down':
            move[1] = - delta
        return move

    # delete item
    def delete(self):
        # delete off canvas
        self.canvas.delete(self.item)
        # delete from item list in game object
        self.game.remove_object(self.item)
