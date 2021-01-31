from abc import ABC, abstractmethod, staticmethod
import weapon


class entity(ABC):
    # initialize entity
    def __init__(self, x, y, id, weap, orient='S'):
        self.x = x
        self.y = y
        self.id = id
        self.weapon = weap
        self.orient = 'S'

    # return speech line for given entity
    @abstractmethod
    @staticmethod
    def get_speech():
        pass

    # return identifier id
    def get_id(self):
        return self.id

    # return position of entity
    def get_pos(self):
        return self.x, self.y

    # return orientation of entity
    def get_orientation(self):
        return self.orient

    def turn(self, dir):
        self.orient = dir
