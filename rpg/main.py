# REQUIRES PYTHON 3

import characters
import gamelogic
#import gui
import json
import os.path


# check and see if there is a save file, and if so, load it up
def checkForSave():
    # check if there is an existing save and load it
    if os.path.exists('player.json'):
        print('Found existing save! Loading save file...')
        file = open("player.json", "r")
        j = json.loads(file.read())
        print(j)
        player = characters.Character(j['name'], j['hp'], j['maxHP'], j['mana'], j['gold'], j['inventory'], j['exp'], j['level'])
    # else create a new character
    else:
        print("Enter your character's name... ")
        i = input()
        player = characters.Character(i, 100, 100, 100, 0, {'main': 'wooden_sword'}, 0, 1)
    return player

        
# the main game loop
def main():
    #gui
    gamelogic.clearScreen()
    
    player = checkForSave()

    # Game Loop
    while(True):
        gamelogic.clearScreen()
        characters.statsBar(player)
        characters.expBar(player.percent, 1, prefix = 'Progress:', suffix = 'til Level ' + str(player.level + 1), length = 50)
        print("\n")
        print('Pick an action: [fight] [inventory] [doctor] [exit] \n')
        action = input()


        if action == 'fight':
            gamelogic.fight(player)
        if action == 'inventory':
            gamelogic.showInventory(player)
        if action =='doctor':
            gamelogic.doctor(player)
        if action == 'exit':
            with open('player.json', 'w') as save:
                # dump the status to file
                json.dump(vars(player), save)
            gamelogic.clearScreen()
            
            exit()


# start the game when called 
main()