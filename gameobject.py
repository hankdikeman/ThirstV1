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

    # move object on canvas
    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    # delete item
    def delete(self):
        self.canvas.delete(self.item)
        self.game.remove_item(self.item)
