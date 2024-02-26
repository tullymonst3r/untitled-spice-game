init -9 python in itemslib: 
    from enum import Enum
    import store.combatlib as combatlib
    import json

    items = {}

    def addItem(tag: str, item: Item):
        global items
        item.tag = tag
        items[tag] = item
        items = items

    class Item(object):
        def __init__(self, name: str, price: int, imageName: str, *args, **kwargs):
            self.name = name
            self.price = price
            self.imageName = imageName
            self.tag = kwargs.get('tag', None)
            self.equipped = kwargs.get('equipped', False) # Whether someone has this item equipped
            self.description = kwargs.get('description', '')
            self.weaponType = kwargs.get('weaponType', None) # melee | range | magic | consumable | None (story item)
            self.manaReduction = kwargs.get('manaReduction', 0) # discounted mana cost from every equipped spell. Only magic type weappns
            self.cd = kwargs.get('cd', 0) # cooldown
            self.attackData = kwargs.get('attackData', None)
            self.exclusiveTo = kwargs.get('exclusiveTo', None) # list of chars that can use this item. Set to None to allow any 
        def __str__(self):
            return self.name
    
    addItem('smallHealPot', Item('Small healing Potion', 100, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", sfx="02_Heal_02.mp3", heal=20)))
    addItem('medHealPot', Item('Medium healing Potion', 200, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", sfx="02_Heal_02.mp3", heal=50)))
    addItem('largeHealPot', Item('Large healing Potion', 400, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", sfx="02_Heal_02.mp3", heal=100)))
    addItem('smallManPot', Item('Small mana Potion', 100, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", mana=20)))
    addItem('medManPot', Item('Medium mana Potion', 200, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", mana=50)))
    addItem('largeManPot', Item('Large mana Potion', 400, 'mg42', weaponType='consumable', attackData=combatlib.AttackData(target="ally", mana=100)))
    addItem('giantTranPot', Item('Trans Potion: Giant', 2000, 'mg42', weaponType='consumable', description="Transform into a powerful giant for 4 rounds.", attackData=combatlib.AttackData(target="self", animation="magicHit", sfx="16_Atk_buff_04.mp3", specialAction="transformTo", specialVal="titan")))

    # Initializing stored items
    # f = open(renpy.loader.transfn("./items.json"), "r")
    # loaded_items = json.load(f)
    # for item in loaded_items['list']:
    #     items.append(Item(item.tag, item.name, item.price, item.imageName, item.weaponData))
    # f.close()
