from enemy import enemy


class enemyex(enemy):
    def get_speech(self):
        return 'YOLO'

    def set_health(self, max_health=100):
        self.max_health = 100
        self.health = 100

    def attack(self, ent, damage):
        ent.health_change(damage)
