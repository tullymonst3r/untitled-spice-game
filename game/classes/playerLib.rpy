init -6 python in playerLib:
    import copy
    import store.combatlib as combatlib
    import store.itemslib as itemslib
    import store.spellslib as spellslib
    party = ['garlic', None, None, None]
    guardians = {
        "garlic": True,
        "rosemary": False,
        "sage": False,
        "thyme": False,
        "parsley": False
    }
    gold = 0
    inventory = ['mg42', 'gay_sword', 'gay_stick', 'root_hammer', 'floweringThorn', 'sageTs', 'forestBow', 'stormBow', 'parsleyHammer']
    itemsInventory = {
        'smallHealPot': 100,
        'medHealPot': 50,
        'largeHealPot': 20,
        'smallManPot': 100,
        'medManPot': 50,
        'largeManPot': 20,
        'giantTranPot': 1,
    }
    selectedGuardian = None
    selectedSlot = None
    selectedEquipmentType = None
    unsavedUpgrades = {
        'baseHealth': 0,
        'baseMana': 0,
        'baseStrength': 0,
        'baseDefense': 0,
        'baseMagicDef': 0,
        'baseSpeed': 0,
        'baseAccuracy': 0,
        'baseFinesse': 0
    }
    upgradeableStats = {
        'baseHealth': {'label': 'HP', 'jump': 20, 'max': 1000, 'color': "#b010a8"},
        'baseMana': {'label': 'MP', 'jump': 5, 'max': 250, 'color': "#0fa0c1"},
        'baseStrength': {'label': 'Str', 'jump': 3, 'max': 150, 'color': "#b68b09"},
        'baseDefense': {'label': 'Def', 'jump': 2, 'max': 100, 'color': "#b68b09"},
        'baseMagicDef': {'label': 'Mag Def', 'jump': 2, 'max': 100, 'color': "#b68b09"},
        'baseSpeed': {'label': 'Spd', 'jump': 1, 'max': 50, 'color': "#b68b09"},
        'baseAccuracy': {'label': 'Acu', 'jump': 1, 'max': 50, 'color': "#b68b09"},
        'baseFinesse': {'label': 'Fin', 'jump': 1, 'max': 50, 'color': "#b68b09"}
    }
    upgradesAvailable = 0

    def removePartyMember(index):
        global party, guardians
        charTag = party[index]
        if charTag in guardians:
            guardians[charTag] = False
        party[index] = None
        party = party

    def addPartyMember(charTag):
        global party, guardians
        for (index, slot) in enumerate(party):
            if slot is None:
                party[index] = charTag
                break
        guardians[charTag] = True
        guardians = guardians

    def isPartySlotAvailable():
        available = False
        for slot in party:
            if slot is None:
                available = True
                break
        return available

    def selectGuardianToInspect(charTag):
        global selectedGuardian
        # combatlib.combatChars[charTag].calcTerrasphereStats()
        selectedGuardian = charTag
    def selectSlot(index):
        global selectedEquipmentType, selectedSlot
        selectedEquipmentType = None
        selectedSlot = index
    def unassignSlot():
        if (selectedGuardian is not None) and (selectedSlot is not None):
            char = combatlib.combatChars[selectedGuardian]
            char.assignSlot(selectedSlot, None)
    def assignSlot(equipment):
        if (selectedGuardian is not None) and (selectedSlot is not None):
            char = combatlib.combatChars[selectedGuardian]
            char.assignSlot(selectedSlot, equipment)
    def selectAssignEquipment(equipment):
        global selectedEquipmentType
        selectedEquipmentType = equipment

    def availableWeapons():
        global inventory
        availableItems = []
        weaponTypes = ['melee','range','magic']
        for itemTag in inventory:
            item = itemslib.items[itemTag]
            if (item.equipped == False) and (item.weaponType in weaponTypes):
                availableItems.append(item)
        return availableItems
    def availableSpells(charSpells):
        availableSpells = []
        for spellTuple in charSpells.items():
            if spellTuple[1] == False:
                availableSpells.append(spellslib.spells[spellTuple[0]])
        return availableSpells
    def availableAttacks(charAttacks):
        availableAttacks = []
        for attackTuple in charAttacks.items():
            if attackTuple[1] == False:
                availableAttacks.append(combatlib.attacks[attackTuple[0]])
        return availableAttacks

    def resetUnsavedUpgrades(upgrades):
        global upgradesAvailable, upgradeableStats, unsavedUpgrades
        upgradesAvailable = upgrades
        for stat in upgradeableStats.keys():
            unsavedUpgrades[stat] = 0
    def saveUpgrades():
        global selectedGuardian, unsavedUpgrades, upgradesAvailable
        char = combatlib.combatChars[selectedGuardian]
        char.upgrades = char.upgrades - (char.upgrades - upgradesAvailable)
        for upgrade in unsavedUpgrades.items():
            if upgrade[1] > 0:
                setattr(char, upgrade[0], getattr(char, upgrade[0]) + upgrade[1])
        resetUnsavedUpgrades(0)

    selectedGuardian = 'garlic'
