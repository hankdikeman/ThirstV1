from gameobject import GameObject
from gamemobs import Enemy, Beetle, Lizard


# game structure baseclass
class GameStructure(GameObject):
    def __init__(self, canvas, item, game):
        super(GameStructure, self).__init__(canvas, item, game)


# early implemented oasis class
class Oasis(GameStructure):
    NUM_ENEMIES = 5

    def __init__(self, canvas, game, x, y):
        # store oasis radius
        self.radius = 40
        self.x = x
        self.y = y

        # generate oasis object and store tag
        item = canvas.create_oval(x - self.radius * 1.5, y - self.radius * 1,
                                  x + self.radius * 1.5, y + self.radius * 1,
                                  fill='dodger blue')
        # move to lowest z level
        canvas.tag_lower(item, 'all')
        super(Oasis, self).__init__(canvas, item, game)

        # generate enemies that belong to oasis
        self.generate_oasis_enemies(self.NUM_ENEMIES)

    def generate_oasis_enemies(self, num_enemies):
        self.enemy_list = {}
        for i in range(num_enemies):
            beetle = Beetle(self.canvas, self.x, self.y, self.game, self)
            self.enemy_list[beetle.item] = beetle

    def get_enemylist(self):
        return self.enemy_list


# baseclass for RNG objects
class BackgroundObject(GameStructure):
    pass
