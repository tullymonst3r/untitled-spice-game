init -9 python in itemslib: 
    from enum import Enum
    import json

    items = {}

    def findItem (tag: str):
        global selectedItem
        selectedItem = items[tag]


    class Item(object):
        def __init__(self, name: str, price: int, imageName: str, *args, **kwargs):
            self.name = name
            self.price = price
            self.imageName = imageName
            self.weaponData = kwargs.get('weaponData', None)
        def __str__(self):
            return self.name

    class WeaponType(Enum):
        MELEE = 'melee'
        RANGE = 'range'

    items['gay_sword'] = Item('Gay Sword', 100, 'gay_sword', weaponData={"damage": 10, "weight": 2, "type": "melee"})
    items['gay_stick'] = Item('Gay Stick', 100, 'gay_stick', weaponData={"damage": 10, "weight": 1, "type": "magic", "mana": 15})
    items['root_hammer'] = Item('Root Hammer', 100, 'root_hammer', weaponData={"damage": 15, "weight": 4, "type": "melee"})
    items['mg42'] = Item('MG42', 100, 'mg42', weaponData={"damage": 100, "weight": 5, "type": "range", "precision": 3})
    items['jannyWeapon'] = Item('Janny\'s Ban Axe', 100, 'mg42', weaponData={"damage": 7, "weight": 2, "type": "melee"})

    # Example of weapon data
    # itemData = {
    #     "name": "Name displayed. (str)",
    #     "price": "Selling / buying price. (int)",
    #     "imageName": "Image displayed on inspection. (str)",
    #     "weaponData": {
    #         "damage": "Damage added to the base attack. (int)",
    #         "weight": "Speed penalization. (int)",
    #         "type": "Type of weapon. (WeaponType)",
    #         "precision": "Chances of hitting. Only range weapons. (int)",
    #         "mana": "Mana saved from each attack. Only magic weapons. (int)",
    #         "user_effects": "List of status effects it activates on the user upon entering combat (list of tuples. [...(effect_tag, level, duration(optional))])",
    #         "attack_effects": "List of status effects it activates on the attacked enemies (list of tuples. [...(effect_tag, level, duration(optional))])"
    #     }
    # }

    # Initializing stored items
    # f = open(renpy.loader.transfn("./items.json"), "r")
    # loaded_items = json.load(f)
    # for item in loaded_items['list']:
    #     items.append(Item(item.tag, item.name, item.price, item.imageName, item.weaponData))
    # f.close()
