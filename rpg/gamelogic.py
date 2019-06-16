import characters
import items
from pprint import pprint
from random import randint
import os
import time


def clearScreen():
    os.system("clear")


# calculate character damage
def damage(character):
    # grab the current weapon from the characters main hand
    weapon = items.retrieveItem(character.inventory['main'])
    #pprint(weapon)
    damage = randint(weapon['minDamage'], weapon['maxDamage'])
    return damage

# remaining fight loop based on who won the first hit
def fightLoop(nextChar, Player, enemy):
    alive = True
    enemyAlive = True
    turn = nextChar

    while (alive) and (enemyAlive):
        if(turn == 'player'):
            clearScreen()
            characters.statsBar(Player)
            characters.statsBar(enemy)
            playerDamage = damage(Player)
            enemy.hp -= playerDamage
            print("\nYou deal " + str(playerDamage) + " to " + enemy.name + ". Enemy HP: " + str(enemy.hp))
            turn = 'enemy'
            if enemy.hp <=0: enemyAlive = False
        else:
            clearScreen()
            characters.statsBar(Player)
            characters.statsBar(enemy)
            enemyDamage = damage(enemy)
            print("\nYou were hit for " + str(enemyDamage) + " damage!" + " Your HP: " + str(Player.hp))
            turn = 'player'
            Player.hp -= enemyDamage
            if Player.hp <=0:  alive= False
        time.sleep(1) # sleep for one second between iterations so we aren't just flying through this loop

    if enemyAlive == False:
        print("You won " + str(enemy.gold) + " gold and " + str(enemy.exp) + " experience!")
        Player.exp += enemy.exp
        Player.gold += enemy.gold


# the fight action
def fight(Player):
    # spawn a new enemy, relative to the player's stats
    enemy = characters.Enemy(Player)
    # clear screen so it does not become cluttered
    clearScreen()

    # print to the console what we have
    print('A level ' + str(enemy.level) + ' ' + enemy.name + ' appears with '+ str(enemy.hp)+ 'HP!')
    pprint(vars(enemy))

    if(randint(0,1) == 1):
        playerDamage = damage(Player)
        clearScreen()
        characters.statsBar(Player)
        characters.statsBar(enemy)
        print("\nYou strike first! You deal " + str(playerDamage) + " to " + enemy.name + ". Enemy HP: " + str(enemy.hp))
        fightLoop('enemy', Player, enemy)
    else:
        enemyDamage = damage(enemy)
        clearScreen()
        characters.statsBar(Player)
        characters.statsBar(enemy)
        print("\n" + enemy.name + " strikes first! You get dealt " + str(enemyDamage) + " damage!" + " Your HP: " + str(enemy.hp))
        fightLoop('player', Player, enemy)
        
    # calc if player has leveled up
    characters.playerLevel(Player)
    print("Fight Over! Press enter to return to main menu... ")
    input()

# the doctor (heal) action

def doctor(Player):
    # clear the screen and show the stats bar on the top
    clearScreen()
    characters.statsBar(Player)

    # cost of the services, can be changed to an incremental value later
    doctorCost = 1

    print("\nWelcome to the apothecary! I can fully heal you for " + str(doctorCost) + " gold! Would you like to be healed? [y] or [n]")
    choice = input()

    if choice == 'y':
        Player.gold -= doctorCost
        Player.hp = Player.maxHP
        print("You're all patched up!")
    else:
        print("I'll be here if you ever change you mind!")


    print("\nPress enter to return to the main menu...")
    input()

def showInventory(character):
    for index in character.inventory:
        print("Slot [%s]: %s" % (index, character.inventory[index]))

    print("\nEnter a slot name / number or type exit to leave ")
    choice = input()

    while choice != 'exit':
        print("\n What do you want to do with the item? [equip] [toss]")
        itemChoice = input()
        if itemChoice == "equip":
            item = items.retrieveItem(character.inventory[choice])
            if item.equippable:
                character.inventory['main'], character.inventory[choice] = character.inventory[choice], character.inventory['main']
        if itemChoice == 'toss':
                del character.inventory[choice]

        # at the end ask for next option
        print("\nEnter a slot name / number or type exit to leave ")
        choice = input()



