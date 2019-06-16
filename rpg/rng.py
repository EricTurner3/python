from random import randint
from random import random
from random import choice


# grab a random enemy name
def randomEnemyName():
    enemies = ['orc', 'goblin', 'wolf', 'zombie', 'skeleton']
    return choice(enemies)

# random level for enemy
def randomLevel(level):
    return randint(1, level+1)

# create random stats based on player's values
def randomCharStats(PlayerStat):
    return round(PlayerStat * random())


def randomLoot(level):
    return randint(1, 10*level)