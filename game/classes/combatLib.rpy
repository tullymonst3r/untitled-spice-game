init -10 python in combatlib: 
    from enum import Enum
    import math
    import copy
    import random
    import store.itemslib as itemslib
    import store.spellslib as spellslib
    import store.effectsLib as effectsLib
    import store.playerLib as playerLib

    # GLOBALS CONSTANTS
    critMultiplier = 2 # percentage each finesse point is equals to
    meleeMinChance = 50 # minimum chance of hit when no speed diff
    speedMultiplier = 10 # percentage each speed diff point is equals to
    accuMultiplier = 2 # percentage each speed diff point is equals to

    attacks = {}
    combatChars = {} # Dict of every different 
    wonLastCombat = False
    hideSpritesAfterBattle = True
    gauntlet = False # While true battles won't reset health and mana
    arenaChars = {} # Dict of characters in combat (copies)
    arenaTags = [] # tags of chars in combat (order of turns)
    allies = []
    alliesAlive = []
    enemies = []
    enemiesAlive = []

    def addCharacter(tag: str, combatChar: CombatCharacter):
        global combatChars
        combatChar.tag = tag
        combatChar.ogTag = tag
        combatChars[tag] = combatChar
        combatChars = combatChars
    def addAttack(tag: str, attack: Attack):
        global attacks
        attack.tag = tag
        attacks[tag] = attack
        attacks = attacks

    def updateCharsDict():
        global combatChars
        combatChars = combatChars
    def resetArena():
        global arenaChars
        arenaChars = {}
    def addCharacterToArena(tag, newTag):
        global arenaChars, combatChars
        charCopy = copy.deepcopy(combatChars[tag])
        charCopy.tag = newTag
        arenaChars[newTag] = charCopy
        arenaChars = arenaChars



    class CombatCharacter(object):
        xp: int = 0
        upgrades: int = 0
        x: int = 0
        y: int = 0
        zorder: int = 0
        tsTotalMana = 0 # Mana cost reduction from all equiped TerraSpeheres combined
        tsTotalDamage = 0 # Damage increase on new magic spells from all equiped TerraSpeheres combined
        damageDone = 0
        healDone = 0
        summonedBy = None # Tag of the character that summoned it.
        transFrom = None # Tag of the character that transformed into this char.
        def __init__(self, name: str, *args, **kwargs):
            self.name = name
            self.tag = kwargs.get('tag', None)
            self.ogTag = self.tag
            self.spriteName = kwargs.get('spriteName', 'garlic_chives')
            self.baseHealth = kwargs.get('baseHealth', 100)
            self.health = self.baseHealth
            self.baseMana = kwargs.get('baseMana', 0)
            self.mana = self.baseMana
            self.baseTurns = kwargs.get('baseTurns', 1)
            self.turns = self.baseTurns

            # Stats
            self.baseStrength = kwargs.get('baseStrength', 10) # Damage added to melee attacks
            self.strength = self.baseStrength
            self.baseDefense = kwargs.get('baseDefense', 0) # % of non magic damage mitigated (Minimum damage possible)
            self.defense = self.baseDefense
            self.baseSpeed = kwargs.get('baseSpeed', 5) # Affect chances of hitting or avoiding melee attacks (based on speed difference between attacker and target)
            self.speed = self.baseSpeed
            self.baseFinesse = kwargs.get('baseFinesse', 1) # Chances of crit damage in non magic attacks (1 = 5%)
            self.finesse = self.baseFinesse
            self.baseAccuracy = kwargs.get('baseAccuracy', 1) # Chances of hitting range and magic attacks
            self.accuracy = self.baseAccuracy
            self.baseMagicDef = kwargs.get('baseMagicDef', 0) # % of magic damage mitigated (Minimum damage possible)
            self.magicDef = self.baseMagicDef


            # Special stats. Ignore randomness. Too OP. Watch out
            self.baseNimbleness = kwargs.get('baseNimbleness', 0) # Increases chances of avoiding all attacks (1 = +1% chance of dodging)
            self.nimbleness = self.baseNimbleness # Avoid setting default too high or the battle becomes too annoying
            self.baseFocus = kwargs.get('baseFocus', 0) # Increases chances of hitting all attacks (1 = +1% chance of dodging)
            self.focus = self.baseFocus # Beats nimbleness
            # #######################
            
            self.level = kwargs.get('level', 1)
            self.isPlayable = kwargs.get('isPlayable', False)

            self.effects = kwargs.get('effects', {})
            self.equipmentLevels = kwargs.get('equipmentLevels', {})
            self.unlockedSpells = kwargs.get('unlockedSpells', {})
            self.unlockedAttacks = kwargs.get('unlockedAttacks', {})
            self.lockedAttacks = kwargs.get('lockedAttacks', [])
            self.equipment = [None, None, None, None]
            innitialEquipments = kwargs.get('equipment', None)
            if innitialEquipments is not None:
                for (index, equipment) in enumerate(innitialEquipments):
                    if isinstance(equipment, tuple):
                        self.assignSlot(index, equipment[0])
                        self.equipmentLevels[equipment[0].tag] = equipment[1]
                    else:
                        self.assignSlot(index, equipment)
            else:
                self.equipment[0] = Attack()
            
            self.loot = kwargs.get('loot', [])
            self.gold = kwargs.get('gold', 0)
        def __str__(self):
            return self.name
        def gainXp(self, xp):
            hasLeveledUp = False
            canLevelUp = True
            self.xp += xp
            while canLevelUp:
                reqExp = 100
                if self.level > 1:
                    reqExp =  int(pow(100, 1 + (((self.level + 1)/10) - 0.1)))
                if self.xp >= reqExp:
                    self.level += 1
                    self.upgrades += int(( 0.8 * math.sqrt(self.level) ) + 0.5)
                    hasLeveledUp = True
                    self.xp = self.xp - reqExp
                else:
                    canLevelUp = False
            return hasLeveledUp
        def assignSlot(self, index: int, equipment):
            if (index <= len(self.equipment)-1) and (self.equipment[index] is not None) and (self.equipment[index].tag is not None):
                className = self.equipment[index].__class__.__name__
                if className == 'Item':
                    itemslib.items[self.equipment[index].tag].equipped = False
                if className == 'Spell':
                    self.unlockedSpells[self.equipment[index].tag] = False
                if className == 'Attack':
                    self.unlockedAttacks[self.equipment[index].tag] = False
            if (equipment is not None) and (equipment.tag is not None):
                className = equipment.__class__.__name__
                if className == 'Item':
                    equipment.equipped = True
                elif className == 'Spell':
                    self.unlockedSpells[equipment.tag] = True
                elif className == 'Attack':
                    self.unlockedAttacks[equipment.tag] = True
            if (index <= len(self.equipment)-1):
                # Replaces equipment at index
                self.equipment[index] = copy.deepcopy(equipment)
            else:
                # Pushes equipment at the end of list
                self.equipment.append(copy.deepcopy(equipment))
            self.calcTerrasphereStats()
        def calcTerrasphereStats(self):
            self.tsTotalMana = 0
            self.tsTotalDamage = 0
            for equipment in self.equipment:
                if (equipment is not None) and (equipment.__class__.__name__ == 'Item'):
                    if equipment.weaponType == 'magic':
                        self.tsTotalMana += equipment.manaReduction
                        self.tsTotalDamage += equipment.attackData.damage

    class AttackData(object): # Attack modifiers
        def __init__(self, *args, **kwargs):
            self.target = kwargs.get('target', 'enemy') # enemy | enemies | ally | allies | self | all | any
            self.hits = kwargs.get('hits', 1) # number of hits per attack
            self.baseCooldown = kwargs.get('baseCooldown', 0) # Cooldown applied after use

            self.damage = kwargs.get('damage', 0) # Damage modifier.
            self.noDamage = kwargs.get('noDamage', False) # Whether the attack ignores damage on melee attacks.
            self.forceHitChance = kwargs.get('forceHitChance', False) # Whether checks hit chance even when no damage.
            self.heal = kwargs.get('heal', 0) # Heal modifier. Negatives are ignored.
            self.mana = kwargs.get('mana', 0) # Steal | regen mana to target
            self.weight = kwargs.get('weight', 0) # Weapon weight, speed modifier
            self.accuracy = kwargs.get('accuracy', 0) # Range and magic attacks accuracy
            self.finesse = kwargs.get('finesse', 0) # Normal attacks precision

            self.active_effects = kwargs.get('active_effects', []) # effects applied to target on use
            self.passive_effects = kwargs.get('passive_effects', []) # effects applied to users on equipping
            self.animation = kwargs.get('animation', 'impact') # Animation played on the target on use
            self.sfx = kwargs.get('sfx', '22_Slash_04.mp3') # Sound effect played on use
            self.verb = kwargs.get('verb', 'uses') # Verb (third person) that goes along with the name of the equipment (character "USES" punch)
            self.specialAction = kwargs.get('specialAction', None) # Name of function called when effect activates. (str)
            self.specialVal = kwargs.get('specialVal', None) # Value passed to the special action function. (str)
        def __str__(self):
            return self.damage
    class Attack(object): # Attack modifiers
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'Punch') # Displayed Name (optional. Required for normal type)
            self.description = kwargs.get('description', '') # Displayed Name (optional. Required for normal type)
            self.attackType = kwargs.get('attackType', 'melee') # melee | range | magic
            self.tag = kwargs.get('tag', None)
            self.cd = kwargs.get('cd', 0) # cooldown
            self.xpPrice = kwargs.get('xpPrice', 0) # Cost to unlock attack
            self.attackData = kwargs.get('attackData', AttackData()) # AttackData

    
    def resetChars(chars):
        global gauntlet
        for tag in chars:
            if tag is not None:
                if gauntlet == False:
                    combatChars[tag].health = combatChars[tag].baseHealth
                    combatChars[tag].mana = combatChars[tag].baseMana
                combatChars[tag].strength = combatChars[tag].baseStrength
                combatChars[tag].defense = combatChars[tag].baseDefense
                combatChars[tag].speed = combatChars[tag].baseSpeed
                combatChars[tag].finesse = combatChars[tag].baseFinesse
                combatChars[tag].turns = combatChars[tag].baseTurns
                combatChars[tag].effects = {}
    
    def actionAttack(attacker: CombatCharacter, targetTags, equipment):
        if equipment.__class__.__name__ == 'Item':
            weaponAttack(attacker, targetTags, equipment)
        elif equipment.__class__.__name__ == 'Spell':
            spellAttack(attacker, targetTags, equipment)
        elif equipment.__class__.__name__ == 'Attack':
            normalAttack(attacker, targetTags, equipment)
        # Set cooldown if applied
        if equipment.attackData.baseCooldown > 0: equipment.cd = equipment.attackData.baseCooldown
    
    def normalAttack(attacker: CombatCharacter, targetTags, equipment):
        if equipment.attackType == 'melee':
            meleeAttack(attacker, targetTags, equipment.attackData)
        elif equipment.attackType == 'range':
            rangeAttack(attacker, targetTags, equipment.attackData)
        elif equipment.attackType == 'magic':
            magicAttack(attacker, targetTags, equipment.attackData)

    def weaponAttack(attacker: CombatCharacter, targetTags, equipment):
        if equipment.weaponType == 'melee':
            meleeAttack(attacker, targetTags, equipment.attackData)
        elif equipment.weaponType == 'range':
            rangeAttack(attacker, targetTags, equipment.attackData)
        elif equipment.weaponType == 'magic':
            magicAttack(attacker, targetTags, equipment.attackData)
        elif equipment.weaponType == 'consumable':
            itemAttack(attacker, targetTags, equipment.attackData)
            playerLib.itemsInventory[equipment.tag] -= 1
    
    def meleeAttack(attacker: CombatCharacter, targetTags, attackData: AttackData):
        global critMultiplier, speedMultiplier, meleeMinChance
        totalDamage = 0
        totalHeal = 0
        maxAttackDamage = attacker.strength + attackData.damage
        critChance = (attacker.finesse + attackData.finesse) * critMultiplier
        for i in range(attackData.hits):
            for targetTag in targetTags:
                target = arenaChars[targetTag]
                minimumChanceOfHit = meleeMinChance
                speedDif = (attacker.speed - attackData.weight) - target.speed
                minimumChanceOfHit += speedDif * speedMultiplier
                # caps between 0 and 100
                if minimumChanceOfHit < 0:
                    minimumChanceOfHit = 0
                if minimumChanceOfHit > 100:
                    minimumChanceOfHit = 100
                attackChance = random.randrange(minimumChanceOfHit, 101)
                (damageDone, healDone) = attack(target, attackData, attackChance, maxAttackDamage, critChance, 'normal', attacker.focus, i == attackData.hits - 1)
                totalDamage += damageDone
                totalHeal += healDone
            if attackData.hits > 1:
                renpy.pause(0.25)
        attacker.damageDone += totalDamage
        attacker.healDone += totalHeal
        return totalDamage

    def rangeAttack(attacker: CombatCharacter, targetTags, attackData: AttackData):
        global critMultiplier, accuMultiplier
        totalDamage = 0
        totalHeal = 0
        maxAttackDamage = attackData.damage
        minimumChanceOfHit = (attacker.accuracy + attackData.accuracy) * accuMultiplier
        critChance = (attacker.finesse + attackData.finesse) * critMultiplier
        # caps precision at 100%
        if minimumChanceOfHit > 100:
            minimumChanceOfHit = 100
        for i in range(attackData.hits):
            for targetTag in targetTags:
                target = arenaChars[targetTag]
                attackChance = random.randrange(minimumChanceOfHit, 101)
                (damageDone, healDone) = attack(target, attackData, attackChance, maxAttackDamage, critChance, 'normal', attacker.focus, i == attackData.hits - 1) # No crits
                totalDamage += damageDone
                totalHeal += healDone
            if attackData.hits > 1:
                renpy.pause(0.25)
        attacker.damageDone += totalDamage
        attacker.healDone += totalHeal
        return totalDamage
    
    def magicAttack(attacker: CombatCharacter, targetTags, attackData: AttackData):
        global accuMultiplier
        totalDamage = 0
        totalHeal = 0
        maxAttackDamage = attackData.damage
        minimumChanceOfHit = (attacker.accuracy + attackData.accuracy) * accuMultiplier
        if minimumChanceOfHit > 100:
            minimumChanceOfHit = 100
        for i in range(attackData.hits):
            for targetTag in targetTags:
                target = arenaChars[targetTag]
                (damageDone, healDone) = attack(target, attackData, minimumChanceOfHit, maxAttackDamage, 0, 'magic', attacker.focus, i == attackData.hits - 1) # 100% attack chance | No crit chance | Ignore defense
                totalDamage += damageDone
                totalHeal += healDone
            if attackData.hits > 1:
                renpy.pause(0.25)
        if attackData.specialAction is not None:
            method = getattr(spellslib, attackData.specialAction)
            method(attacker, attackData.specialVal)
        attacker.damageDone += totalDamage
        attacker.healDone += totalHeal
        return totalDamage

    def itemAttack(attacker: CombatCharacter, targetTags, attackData: AttackData):
        maxAttackDamage = attackData.damage
        for i in range(attackData.hits):
            for targetTag in targetTags:
                target = arenaChars[targetTag]
                attack(target, attackData, 100, maxAttackDamage, 0, None, 0, i == attackData.hits - 1) # 100% attack chance | No crit chance | Ignore defense
            if attackData.hits > 1:
                renpy.pause(0.25)
        if attackData.specialAction is not None:
            method = getattr(spellslib, attackData.specialAction)
            method(attacker, attackData.specialVal)

    def spellAttack(attacker: CombatCharacter, targetTags, equipment):
        global accuMultiplier
        totalDamage = 0
        totalHeal = 0
        # Calculate mana cost
        manaCost = equipment.cost - attacker.tsTotalMana if equipment.cost - attacker.tsTotalMana > 0 else 0
        attacker.mana -= manaCost
        attackData = equipment.attackData
        minimumChanceOfHit = (attacker.accuracy + attackData.accuracy) * accuMultiplier
        if minimumChanceOfHit > 100:
            minimumChanceOfHit = 100
        maxAttackDamage = 0
        if attackData.damage > 0:
            # Calculate spell's damage
            if equipment.magicType == 'old':
                # spellLvl = attacker.equipmentLevels.get(equipment.tag, 1) I think this is replaces the next 3 lines
                spellLvl = 1
                if equipment.tag in attacker.equipmentLevels:
                    spellLvl = attacker.equipmentLevels[equipment.tag]
                # maxAttackDamage = int(attackData.damage * math.sqrt(attackerSpell.lvl + attacker.level))
                maxAttackDamage = int(attackData.damage * math.sqrt(spellLvl))
            else:
                maxAttackDamage = attackData.damage + attacker.tsTotalDamage
        for i in range(attackData.hits):
            for targetTag in targetTags:
                target = arenaChars[targetTag]
                (damageDone, healDone) = attack(target, attackData, minimumChanceOfHit, maxAttackDamage, 0, 'magic', attacker.focus, i == attackData.hits - 1) # 100% attack chance | No crit chance | Ignore defense
                totalDamage += damageDone
                totalHeal += healDone
            if attackData.hits > 1:
                renpy.pause(0.25)
        if attackData.specialAction is not None:
            method = getattr(spellslib, attackData.specialAction)
            method(attacker, attackData.specialVal)
        # Set cooldown if applied
        # equipment.cd = equipment.attackData.baseCooldown if equipment.magicType == 'old' else 0
        attacker.damageDone += totalDamage
        attacker.healDone += totalHeal
        return totalDamage

    def attack(target, attackData: AttackData, attackChance, maxAttackDamage, critChance = 0, attackType = None, focus = 0, lastHit = True):
        # attackType = 'normal' - uses target's normal defense | 'magic' - Uses target's magic defense | None - Ignores defenses
        hitType = 1 # 0 - miss | 1 - hit(at least one) | 2 - crit(at least one)
        totalDamage = 0
        totalHeal = 0
        if target.nimbleness != 0:
            attackChance -= target.nimbleness
        if focus != 0:
            attackChance += focus
        if (attackData.noDamage == False) and (maxAttackDamage > 0):
            damageResult = damageTarget(target, attackChance, maxAttackDamage, critChance, attackType)
            totalDamage += damageResult[1]
            hitType = damageResult[0]
        elif attackData.forceHitChance == True:
            if random.randrange(100) >= attackChance:
                hitType = 0
        if hitType > 0:
            # No miss if attack has damage
            if attackData.mana != 0:
                manaEffectTarget(target, attackData.mana)
            if attackData.heal > 0:
                totalHeal = healTarget(target, attackData.heal)
            # Apply negative effects
            if lastHit == True:
                applyActiveEffects(target, attackData.active_effects)
            renpy.play("audio/sfx/{}".format(attackData.sfx), channel='audio')
            if hitType == 1:
                # Standard animation
                renpy.show_screen(attackData.animation, positions=[(target.x, target.y)], _tag='an_'+str(target.x)+str(target.y),_transient=True)
            if hitType == 2:
                # Crit animation
                renpy.show_screen("crit", positions=[(target.x, target.y)], _tag='an_'+str(target.x)+str(target.y),_transient=True)
        else:
            renpy.show_screen("msg_effect", x=target.x, y=target.y, text="MISS", _tag='msg_'+str(target.x)+str(target.y), _transient=True)
            renpy.play("audio/sfx/35_Miss_Evade_02.mp3", channel='audio')
            renpy.show_screen("missedHit", positions=[(target.x, target.y)], _tag='an_'+str(target.x)+str(target.y),_transient=True)
        return (totalDamage, totalHeal)

    def damageTarget(target, attackChance, maxAttackDamage, critChance = 0, attackType = None):
        hitType = 0 # 0 - miss | 1 - hit(at least one) | 2 - crit(at least one)
        if random.randrange(100) < attackChance:
            minAttackDamage = maxAttackDamage
            if attackType == 'normal':
                if target.defense > 0:
                    minAttackDamage = int(maxAttackDamage - (maxAttackDamage * (target.defense / 100)))
            if attackType == 'magic':
                if target.magicDef > 0:
                    minAttackDamage = int(maxAttackDamage - (maxAttackDamage * (target.magicDef / 100)))
            damage = random.randrange(minAttackDamage, maxAttackDamage + 1)
            if random.randrange(100) < critChance:
                # crit hit. doubles the damage
                damage = damage * 2
                realDamage = damage if target.health > damage else target.health
                target.health -= realDamage
                renpy.show_screen("number_effect", x=target.x, y=target.y, val=realDamage, textColor="#ff1d1d", _tag='dam_'+str(target.x)+str(target.y), _transient=True)
                return (2, damage)
            else:
                realDamage = damage if target.health > damage else target.health
                target.health -= realDamage
                renpy.show_screen("number_effect", x=target.x, y=target.y, val=realDamage, textColor="#ff1d1d", _tag='dam_'+str(target.x)+str(target.y), _transient=True)
                return (1, damage)
        return (0, 0)
    
    def manaEffectTarget(target, mana):
        if mana > 0:
            missingMana = (target.baseMana - mana)
            manaModifier = mana if mana < missingMana else missingMana
            target.mana += manaModifier
            renpy.show_screen("number_effect", x=target.x, y=target.y, val=manaModifier, textColor="#3bd5ff", _tag='man_'+str(target.x)+str(target.y), _transient=True)
        elif mana < 0:
            if (target.baseMana > 0) and (target.mana > 0):
                absMana = abs(mana)
                manaModifier = absMana if absMana < target.mana else target.mana
                target.mana -= manaModifier
                renpy.show_screen("number_effect", x=target.x, y=target.y, val=manaModifier, textColor="#803bff", _tag='men_'+str(target.x)+str(target.y), _transient=True)

    def healTarget(target, heal):
        targetMissingHealth = target.baseHealth - target.health
        # Cap healing at target's max missing health
        realHealing = heal if targetMissingHealth > heal else targetMissingHealth
        target.health += realHealing
        renpy.show_screen("number_effect", x=target.x, y=target.y, val=realHealing, textColor="#1dff25", _tag='heal_'+str(target.x)+str(target.y), _transient=True)
        return realHealing

    def applyActiveEffects(target, active_effects):
        for effectTag in active_effects:
            # Add status effect to target or reset duration if already applied.
            effect = effectsLib.effects[effectTag]
            if (effectTag not in target.effects) or ((effectTag in target.effects) and (target.effects[effectTag] > -1)):
                target.effects[effectTag] = effect.duration
                if effect.instant_effect:
                    effectsLib.triggerInstantEffect(target, effect)
    
    def reduceCooldown(tag, amount = 1):
        char = arenaChars[tag]
        for equipment in char.equipment:
            if equipment is not None:
                if (equipment.cd > 0):
                    equipment.cd -= amount

        