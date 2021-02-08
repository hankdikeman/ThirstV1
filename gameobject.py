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

    # delete item
    def delete(self):
        # delete off canvas
        self.canvas.delete(self.item)
        # delete from item list in game object
        self.game.remove_object(self.item)
