from entity import entity
from enemy import enemy
from enemyex import enemyex

if __name__ == "__main__":
    en = enemyex(x=0, y=0, id=0, weap=None)

    print(en.get_speech())
