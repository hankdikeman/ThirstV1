from gameobject import GameObject


# game structure baseclass
class GameStructure(GameObject):
    def __init__(self, canvas, item, game):
        super(GameStructure, self).__init__(canvas, item, game)


# oasis placeholder class
class Oasis(GameStructure):
    pass


# baseclass for RNG objects
class BackgroundObject(GameStructure):
    pass
