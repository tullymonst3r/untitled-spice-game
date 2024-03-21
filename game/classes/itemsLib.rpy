init -5 python in itemslib: 
    from enum import Enum
    import store.combatLib as combatLib
    import store.skillsLib as skillsLib
    import store.playerLib as playerLib
    import json
    import copy

    items = {}

    def gainItem(tag: str, quantity: int):
        if tag not in playerLib.inventory:
            playerLib.inventory[tag] = 0
        playerLib.inventory[tag] += quantity


    def getItem(tag):
        items_json = open(renpy.config.gamedir + "/db/items.json", "r")
        loaded_items = json.load(items_json)
        item = loaded_items[tag]
        items_json.close()
        return copy.deepcopy(Item(tag=tag, **item))

    class Item(object):
        def __init__(self, tag: str, name: str, *args, **kwargs):
            self.tag = tag
            self.name = name
            self.price = kwargs.get('pricec', 0)
            self.description = kwargs.get('description', '')
            self.image_name = kwargs.get('image_name', 'mg42')
            self.max_stock = kwargs.get('max_stock', 100)
            self.reusable = kwargs.get('reusable', False)
            if ('skill_data' in kwargs):
                self.skill_data = skillsLib.SkillData(**kwargs.get('skill_data'))
            else:
                self.skill_data = None 
        def __str__(self):
            return self.name
