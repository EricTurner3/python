import rng
import math

class Character:
    def __init__(self,name,hp, maxHP, mana,gold,inventory,exp,level):
        self.name=name
        self.hp=hp
        self.maxHP = maxHP
        self.mana=mana
        self.gold=gold
        self.inventory=inventory
        self.exp=exp
        self.percent = 0.00 # the playerLevel will update this for the player. enemies dont level up
        self.level=level

# show a stats bar on the screen
def statsBar(player):
    print("[" +player.name+ " - Level " + str(player.level)+ " - HP " + str(player.hp)+ "/" + str(player.maxHP) + " - Gold " + str(player.gold)+ " - EXP " + str(player.exp)+"]")

def expBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# update player level based on XP
def playerLevel(player):
    constant = 0.46 # coefficient for level calculation
    player.level = math.floor(constant * math.sqrt(player.exp))
    player.percent = float(str(round(constant * math.sqrt(player.exp),2))[1:])
        

# create a random enemy, based on the player's current stats
class Enemy(Character):
    def __init__(self, Player):
        hp = rng.randomCharStats(Player.hp)
        super().__init__(
            name        =   rng.randomEnemyName(),
            hp          =   hp,
            maxHP       =   hp,
            mana        =   rng.randomCharStats(Player.mana),
            gold        =   rng.randomLoot(Player.level),
            inventory   =   {'main': 'unarmed'},
            exp         =   rng.randomLoot(Player.level), 
            level       =   rng.randomLevel(Player.level)
        )
