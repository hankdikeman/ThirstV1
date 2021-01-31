from abc import ABC, abstractmethod


class entity(ABC):
    # initialize entity
    def __init__(self, x, y, id, weap):
        self.x = x
        self.y = y
        self.id = id
        self.weapon = weap
        self.orient = 'S'
        self.set_health()

    # return speech line for given entity
    @abstractmethod
    def get_speech(self):
        pass

    @abstractmethod
    def set_health(self):
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

    def health_change(self, delta):
        self.health += delta
        if self.health <= 0:
            del self
        else:
            self.health -= self.health % self.max_health
