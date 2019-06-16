


def retrieveItem(item_name):
    items = {
        'unarmed': {'type': 'hands', 'minDamage': 0, 'maxDamage': 2, 'cost': None, 'equippable': True},
        'wooden_sword' : {'type': 'sword', 'minDamage': 0, 'maxDamage': 5, 'cost': 10,  'equippable': True}
        }
    return items[item_name]
    