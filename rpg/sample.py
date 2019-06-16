# https://codereview.stackexchange.com/questions/91069/simple-text-rpg-in-python
from random import randint
class Die:
    """Represents a single die."""
    def __init__(self, sides=6):
        """Set the number of sides (defaults to six)."""
        self.sides = sides

    def roll(self):
        """Roll the die."""
        return randint(1, self.sides)

class Character:
    def __init__(self,name,hp,thaco,ac,inventory,exp):
        self.name=name
        self.hp=hp
        self.thaco=thaco
        self.ac=ac
        self.inventory=inventory
        self.exp=exp



class Fighter(Character):
    def __init__(self):
        super().__init__(name=input("What is your characters name?"),thaco=20,ac=10,
                         hp=10,inventory={},exp=10)
    prof = "fighter"
    maxhp=10
    level=1
    hd=10
    level2=20

class Cleric(Character):
    def __init__(self):
        super().__init__(name=input("What is your characters name?"),thaco=20,ac=10,
                         hp=8,inventory={},exp=8)
    prof= "cleric"
    maxhp=8
    level=1
    hd=8
    level2=15
class Mage(Character):
    def __init__(self):
        super().__init__(name=input("What is your characters name?"),thaco=20,ac=10,
                         hp=4,inventory={},exp=4)
    prof= "mage"
    mana=1
    maxmana=1
    maxhp=4
    level=1
    hd=4
    level2=10
class Goblin(Character):
    def __init__(self):
        super().__init__(name="goblin",
                         hp=7,thaco=20,
                         ac=6,inventory={},
                         exp=7)


class Orc(Character):
    def __init__(self):
        super().__init__(name="orc",
                         hp=8,thaco=18,
                         ac=6,inventory={},
                         exp=8)

def profession():
    print("What is your class?",'\n',
          " press f for Fighter",'\n',
          " press c for Cleric",'\n',
          " press m for Mage")
    pclass=input(">>>")
    if pclass =="f":
        Prof = Fighter()
    elif pclass=="c":
        Prof = Cleric()
    elif pclass == "m":
        Prof = Mage()
    else:
        Prof=Fighter()
        #profession()
    return Prof
def ranmob():
    mob = Goblin() if Die(2).roll()<2 else Orc()
    return mob


def playerAttack():
    roll=Die(20).roll()   
    if roll>=hero.thaco-mob.ac:
        print("You hit")
        if hero.prof=="fighter":
            rollD=Die(10).roll()

        if hero.prof=="cleric":
            rollD=Die(6).roll()

        if hero.prof=="mage":
            rollD=Die(4).roll()
        print("for",rollD,"damage")
        mob.hp-=rollD
        print("the",mob.name,"has",mob.hp,"hp left")
    else:
        print("You miss")

def monsterAttack():
    roll=Die(20).roll()   
    if roll>=mob.thaco-hero.ac:
        print("Monster hit")
        if mob.name=="goblin":                    
            rollD=Die(4).roll()
        elif mob.name=="orc":
            rollD=Die(6).roll()
        print("for",rollD,"damage")
        hero.hp-=rollD
        print(hero.name,"has",hero.hp,"hp left")
    else:
        print("Monster misses")

def levelUp():


    while hero.exp>=hero.level2:
        levelGain=False
        hero.level+=1
        levelGain=True
        hero.level2=hero.level2*2
        if levelGain==True:
            hero.maxhp+=Die(hero.hd).roll()
            hero.hp=hero.maxhp
            if hero.prof=="mage":
                hero.maxmana+=1
                hero.mana=hero.maxmana

            print("You Gained a level","\n",'hp:',hero.hp,"\n",'level:',hero.level)
            levelGain=False
    while hero.level>=3:
        hero.level-=3
        hero.thaco-=1
        print("thaco:",hero.thaco)


def commands():
    if hero.prof=="fighter":
        print (" press f to fight",'\n',
               "press enter to pass")
        command=input("~~~~~~~~~Press a key to Continue.~~~~~~~")
        if command=="f":            
            playerAttack()
        if command=="":
            pass

    if hero.prof=="cleric":
        print (" press f to fight",'\n',
               "press h to heal",'\n',
               "press enter to pass")
        command=input("~~~~~~~~~Press a key to Continue.~~~~~~~")
        if command=="f":            
            playerAttack()
        elif command =="h":
            if hero.hp<hero.maxhp:
                hero.hp+=Die(8).roll()               
                if hero.hp>hero.maxhp:
                    hero.hp=hero.hp-(hero.hp-hero.maxhp)                    
                print("You now have:",hero.hp,"hp")
            else:
                print("Your hit points are full")
                commands()
        elif command=="":
            pass
    if hero.prof=="mage":
        print (" press f to fight",'\n',
               "press s for spells",'\n',
               "press m to generate mana",'\n',
               "press enter to pass")
        command=input("~~~~~~~~~Press a key to Continue.~~~~~~~")
        if command=="f":            
            playerAttack()
        elif command =="s":
            print("You have",hero.mana,"mana")
            if hero.mana>=1 and hero.mana<3:
                print("press s for sleep",'\n',
                      "press m for magic missile")
                command=input(">>>")
                if command =="s":
                    print("You put the monster to sleep it is easy to kill now")
                    mob.hp-=mob.hp
                    hero.mana-=1
                if command=="m":
                    if hero.mana<hero.maxmana:
                        hero.mana+=Die(4).roll()            
                        if hero.mana>hero.maxmana:
                            hero.mana-=(hero.mana-hero.maxmana)
                    dam =Die(4).roll()*hero.mana
                    mob.hp-=dam
                    print("You use all your mana! and do",dam,"damage!")
                    hero.mana-=hero.mana
            elif hero.mana>=3:
                print("press s for sleep",'\n',
                      "press m for magic missile",'\n',
                      "press f for fireball")
                command=input(">>>")
                if command =="s":
                    print("You put the monster to sleep it is easy to kill now")
                    mob.hp-=mob.hp
                    hero.mana-=1
                if command=="m":
                    dam=Die(4).roll()*hero.mana
                    mob.hp-=dam
                    print("You use all your mana! and do",dam,"damage!")
                    hero.mana-=hero.mana
                if command=="f":
                    print("You are temporarily blinded by a feiry flash of light.")
                    dam=0
                    dam+=Die(6).roll()
                    dam+=Die(6).roll()
                    dam+=Die(6).roll()
                    mob.hp-=dam
                    print("You did",dam,"points of damage")

                    hero.mana-=3
            else:
                print("Your mana is empty")
                commands()
        elif command =="m":
            if hero.mana<hero.maxmana:
                hero.mana+=1
                print("You have",hero.mana,"mana")
            elif hero.mana>=hero.maxmana:
                print("Your mana is full.")
                print("You have",hero.mana,"mana")
                commands()

        elif command=="":
            pass

mob=ranmob()
hero=profession()
print("name hp thaco ac inventory xp",'\n',
      hero.name,hero.hp,hero.thaco,hero.ac,hero.inventory,hero.exp)
while True:

    if mob.hp<=0:
        print('The',mob.name,'is dead!')        
        hero.exp+=mob.exp        
        print('hero xp',hero.exp)
        mob=ranmob()
    if hero.hp<=0:
        mob.exp+=hero.exp
        print("mob xp:",mob.exp)
        print(hero.name,'died!')
        #name=input("What is your characters name?")                
        hero=profession()
        print("name hp thaco ac inventory xp",'\n',
              hero.name,hero.hp,hero.thaco,hero.ac,hero.inventory,hero.exp)

    levelUp()

    print("You see",mob.name+",",mob.name,"has",mob.hp,"hp.")
    if hero.hp>0:
        commands()
    if mob.hp>0:                
        monsterAttack()