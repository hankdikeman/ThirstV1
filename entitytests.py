from entity import entity
from enemy import enemy
from enemyex import enemyex

if __name__ == "__main__":
    en1 = enemyex(x=0, y=0, id=0, weap=None)
    en2 = enemyex(x=0, y=0, id=0, weap=None)

    print(en1.max_health)
    print(en1.health)
    print(en1.get_speech())

    en1.attack(en2, -101)

    print(en2.health)
