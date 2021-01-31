from abc import abstractmethod
from entity import entity


class enemy(entity):
    # define initialization for enemy with agro status
    def __init__(self, x, y, id, weap):
        self.agro = False
        super(enemy, self).__init__(x, y, id, weap)

    # define attack method for enemy
    @ abstractmethod
    def attack(self, ent):
        pass
