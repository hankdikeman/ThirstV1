from gameobject import GameObject


# game structure baseclass
class GameStructure(GameObject):
    def __init__(self, canvas, item, game):
        super(GameStructure, self).__init__(canvas, item, game)


# early implemented oasis class
class Oasis(GameStructure):
    def __init__(self, canvas, game, x, y):
        # store oasis radius
        self.radius = 40

        # generate enemies that belong to oasis

        # generate oasis object and store tag
        item = canvas.create_oval(x - self.radius * 1.5, y - self.radius * 1,
                                  x + self.radius * 1.5, y + self.radius * 1,
                                  fill='dodger blue')
        # move to lowest z level
        canvas.tag_lower(item, 'all')
        super(Oasis, self).__init__(canvas, item, game)

    def generate_oasis_enemies(self, num_enemies):
        self.enemy_list = {}


# baseclass for RNG objects
class BackgroundObject(GameStructure):
    pass
