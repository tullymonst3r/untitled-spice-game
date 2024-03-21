init -6 python in playerLib:
    import copy
    import math
    import store.combatLib as combatLib
    import store.itemslib as itemslib
    import store.spellslib as spellslib
    import store.charsLib as charsLib

    # gold = 0
    inventory = {
        'smallHealPot': 100,
        'medHealPot': 50,
        'largeHealPot': 20,
        'smallManPot': 100,
        'medManPot': 50,
        'largeManPot': 20,
        'giantTranPot': 1,
    }
    selected_guardian = None
    selected_slot = None
    unsaved_upgrades = {
        'base_hp': 0,
        'base_mp': 0,
        'base_strength': 0,
        'base_speed': 0,
        'base_defense': 0,
        'base_mag_defense': 0,
        'base_reflexes': 0,
        'base_accuracy': 0,
        'base_finesse': 0
    }
    upgradeable_stats = {
        'base_hp': {'label': 'HP', 'jump': 20, 'max': 1000, 'color': "#ce1937ff"},
        'base_mp': {'label': 'MP', 'jump': 5, 'max': 250, 'color': "#1e8cdbff"},
        'base_defense': {'label': 'Defense', 'jump': 1, 'max': 100, 'color': "#b68b09"},
        'base_mag_defense': {'label': 'Defense', 'jump': 1, 'max': 100, 'color': "#b68b09"},
        'base_reflexes': {'label': 'Reflexes', 'jump': 1, 'max': 100, 'color': "#b68b09"},
        'base_speed': {'label': 'Speed', 'jump': 1, 'max': 100, 'color': "#b68b09"},
        'base_strength': {'label': 'Strength', 'jump': 2, 'max': 100, 'color': "#b68b09"},
        'base_accuracy': {'label': 'Accuracy', 'jump': 1, 'max': 100, 'color': "#b68b09"},
        'base_finesse': {'label': 'Fin', 'jump': 1, 'max': 50, 'color': "#b68b09"}
    }

    sp_available = 0

    
    unlocked_skills=["mg42", "gay_stick", "summonDemon", "hex", "curse", "fireball", "thunderbolt", "summonDemon", "fists", "kick", "meditation"]
    level=1
    xp=0
    sp=0

    def gainXp(gained_xp):
        global xp, level, sp
        has_leveled_up = False
        can_level_up = True
        xp += gained_xp
        while can_level_up:
            req_exp = 100
            if level > 1: req_exp =  int(pow(100, 1 + (((level + 1)/10) - 0.1)))
            if xp >= req_exp:
                level += 1
                sp += int(( 0.8 * math.sqrt(level) ) + 0.5)
                has_leveled_up = True
                xp = xp - req_exp
            else:
                can_level_up = False
        return has_leveled_up



    def selectGuardianToInspect(charTag):
        global selected_guardian
        # combatLib.combatChars[charTag].calcTerrasphereStats()
        selected_guardian = charTag
    def selectSlot(index):
        global selected_slot
        selected_slot = index
    def unassignSlot():
        if (selected_guardian is not None) and (selected_slot is not None):
            char = combatLib.combatChars[selected_guardian]
            char.assignSlot(selected_slot, None)
    def assignSlot(equipment):
        if (selected_guardian is not None) and (selected_slot is not None):
            char = combatLib.combatChars[selected_guardian]
            char.assignSlot(selected_slot, equipment)
    def selectAssignEquipment(equipment):
        global selectedEquipmentType
        selectedEquipmentType = equipment


    def availableSkills():
        return []

    def resetUnsavedUpgrades(upgrades):
        global sp_available, upgradeable_stats, unsaved_upgrades
        sp_available = upgrades
        for stat in upgradeable_stats.keys():
            unsaved_upgrades[stat] = 0
    def saveUpgrades():
        global selected_guardian, unsaved_upgrades, sp_available
        char = combatLib.combatChars[selected_guardian]
        char.upgrades = char.upgrades - (char.upgrades - sp_available)
        for upgrade in unsaved_upgrades.items():
            if upgrade[1] > 0:
                setattr(char, upgrade[0], getattr(char, upgrade[0]) + upgrade[1])
        resetUnsavedUpgrades(0)

    selected_guardian = 'garlic'
    # Load Garlic:
    if 'garlic' not in charsLib.chars: charsLib.addPlayableChar("garlic")
    
