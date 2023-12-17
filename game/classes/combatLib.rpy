init -10 python in combatlib: 
    from enum import Enum
    import math
    import random
    import store.itemslib as itemslib
    import store.spellslib as spellslib

    combatChars = {}

    # Variables for combat
    # allies = []
    # enemies = []

    class CombatCharacter(object):
        exp: int = 0
        level: int = 1
        x: int = 0
        y: int = 0
        inventory = [ ]
        def __init__(self, name: str, spriteName: str, baseHealth: int, *args, **kwargs):
            self.name = name
            self.baseHealth = baseHealth
            self.health = baseHealth
            self.spriteName = spriteName
            self.baseStrength = kwargs.get('baseStrength', 10)
            self.baseDefense = kwargs.get('baseDefense', 0)
            self.baseSpeed = kwargs.get('baseSpeed', 5)
            self.baseFinesse = kwargs.get('baseFinesse', 1)
            self.baseMana = kwargs.get('baseMana', 0)
            self.mana = self.baseMana
            self.level = kwargs.get('level', 1)
            self.hand = kwargs.get("hand", None)
            self.spells = kwargs.get("spells", (None, None))
            self.fightClass = kwargs.get('fightClass', FightClass.NPC)
        def levelup(self):
            reqExp = 100
            if self.level > 1:
                reqExp = 100 * pow(1 + (((self.level + 1)/10) - 0.1))
            if self.exp >= reqExp:
                self.level * self.level + 1
                self.exp = self.exp - reqExp
        def addItem(self, item: str):
            self.inventory.append(item)

    class FightClass(Enum):
        WAR = 'warrior'
        OM = 'old_magic'
        NM = 'new_magic'
        BSM = 'blacksmith'
        RNG = 'ranger'
        NPC = 'npc'

    def resetChars(chars):
        for tag in chars:
            combatChars[tag].health = combatChars[tag].baseHealth
    
    def weaponAttack(attacker, target):
        if combatChars[attacker].hand is not None:
            weapon = itemslib.items[combatChars[attacker].hand]
            if weapon.weaponData['type'] == 'melee':
                return attackMelee(attacker, target)
            elif weapon.weaponData['type'] == 'range':
                return attackRange(attacker, target)
            elif weapon.weaponData['type'] == 'magic':
                return attackMagicWeapon(attacker, target) 
        else:
            return attackFists(attacker, target)
        return (0, 0)

    def attackFists(attacker, target):
        # At same speed chances if hit are 50%
        attackPrecision = 50
        # TODO: use current speed incase buffs or debuffs
        # Each point of speed difference adds or removes 10% or hit TODO: Maybe 10% is too much?
        # Weapon weight affects attacker speed
        speedDif = combatChars[attacker].baseSpeed - combatChars[target].baseSpeed
        attackPrecision += speedDif * 10
        # caps between 0 and 100
        if attackPrecision < 0:
            attackPrecision = 0
        if attackPrecision > 100:
            attackPrecision = 100
        attackChance = random.randrange(attackPrecision, 101)
        if random.randrange(100) < attackChance:
            # successfull hit
            # attacker strength and weapon damage combined
            maxAttackDamage = combatChars[attacker].baseStrength
            # target defense has random chance of reducing incomming damage
            minAttackDamage = maxAttackDamage - combatChars[target].baseDefense
            if minAttackDamage < 0:
                minAttackDamage = 0
            damage = random.randrange(minAttackDamage, maxAttackDamage+1)
            # 5% chance of crit for each point of finesse
            critChance = combatChars[attacker].baseFinesse * 5
            if random.randrange(100) < critChance:
                # crit hit. doubles the damage
                damage = damage * 2
                combatChars[target].health -= damage
                if combatChars[target].health < 0:
                    combatChars[target].health = 0
                return (2, damage)
            else:
                #normal hit
                combatChars[target].health -= damage
                if combatChars[target].health < 0:
                    combatChars[target].health = 0
                return (1, damage)
        else:
            return (0, 0)
    
    def attackMelee(attacker, target):
        # At same speed chances if hit are 50%
        attackPrecision = 50
        # TODO: use current speed incase buffs or debuffs
        # Each point of speed difference adds or removes 10% or hit
        # Weapon weight affects attacker speed
        weapon = itemslib.items[combatChars[attacker].hand]
        speedDif = (combatChars[attacker].baseSpeed - weapon.weaponData['weight']) - combatChars[target].baseSpeed
        attackPrecision += speedDif * 10
        # caps between 0 and 100
        if attackPrecision < 0:
            attackPrecision = 0
        if attackPrecision > 100:
            attackPrecision = 100
        attackChance = random.randrange(attackPrecision, 101)
        if random.randrange(100) < attackChance:
            # successfull hit
            # attacker strength and weapon damage combined
            maxAttackDamage = combatChars[attacker].baseStrength + weapon.weaponData['damage']
            # target defense has random chance of reducing incomming damage
            minAttackDamage = maxAttackDamage - combatChars[target].baseDefense
            if minAttackDamage < 0:
                minAttackDamage = 0
            damage = random.randrange(minAttackDamage, maxAttackDamage+1)
            # 5% chance of crit for each point of finesse
            critChance = combatChars[attacker].baseFinesse * 5
            if random.randrange(100) < critChance:
                # crit hit. doubles the damage
                damage = damage * 2
                combatChars[target].health -= damage
                if combatChars[target].health < 0:
                    combatChars[target].health = 0
                return (2, damage)
            else:
                #normal hit
                combatChars[target].health -= damage
                if combatChars[target].health < 0:
                    combatChars[target].health = 0
                return (1, damage)
        else:
            return (0, 0)

    def attackRange(attacker, target):
        # TODO: use current speed incase buffs or debuffs
        # Weapon precision and attackers finesse add up to total precision
        weapon = itemslib.items[combatChars[attacker].hand]
        attackPrecision = (combatChars[attacker].baseFinesse + weapon.weaponData['precision']) * 4
        # caps precision at 100%
        if attackPrecision > 100:
            attackPrecision = 100
        hitChance = random.randrange(attackPrecision, 101)
        if random.randrange(100) < hitChance:
            # successfull hit
            # attacker strength has no effect
            maxAttackDamage = itemslib.items[combatChars[attacker].hand].weaponData['damage']
            # target defense has random chance of reducing incomming damage
            damage = random.randrange(maxAttackDamage - combatChars[target].baseDefense, maxAttackDamage+1)
            combatChars[target].health -= damage
            if combatChars[target].health < 0:
                combatChars[target].health = 0
            return (1, damage)
        else:
            return (0, 0)

    def attackMagicWeapon(attacker, target):
        # 100% chance of hit
        # attacker strength has no effect
        # attack ignores defenses
        weapon = itemslib.items[combatChars[attacker].hand]
        maxAttackDamage = weapon.weaponData['damage']
        combatChars[target].health -= maxAttackDamage
        if combatChars[target].health < 0:
            combatChars[target].health = 0
        return (1, maxAttackDamage)
    
    def castSpell(attackerTag, targetTag, spellIndex):
        # 100% chance of hit
        # attack ignores defenses
        attacker = combatChars[attackerTag]
        attackerSpell = combatChars[attackerTag].spells[spellIndex]
        if attackerSpell is not None:
            spell = spellslib.spells[attackerSpell['tag']]
            if spell.damage > 0:
                damage = 0
                weapon = None
                if (attacker.hand is not None) and (itemslib.items[attacker.hand].weaponData['type'] == 'magic'):
                    weapon = itemslib.items[attacker.hand]
                if spell.magicType == 'old':
                    damage = int(spell.damage * math.sqrt(attackerSpell['lvl']))
                    attackerSpell['cd'] = spell.cooldown
                else:
                    if weapon is not None:
                        damage = spell.damage + weapon.weaponData['damage']
                combatChars[targetTag].health -= damage
                if combatChars[targetTag].health < 0:
                    combatChars[targetTag].health = 0
                if weapon is not None:
                    manaCost = spell.cost - weapon.weaponData['mana']
                    if manaCost > 0:
                        attacker.mana -= manaCost
                else:
                    attacker.mana -= spell.cost
                return (1, damage)
            else:
                # apply status effects
                return (1, 0)
        else:
            return (0, 0)

    def castMultiSpell(attackerTag, targetsTags, spellIndex):
        # 100% chance of hit
        # attack ignores defenses
        attacker = combatChars[attackerTag]
        attackerSpell = combatChars[attackerTag].spells[spellIndex]
        if attackerSpell is not None:
            spell = spellslib.spells[attackerSpell['tag']]
            if spell.damage > 0:
                damage = 0
                weapon = None
                if (attacker.hand is not None) and (itemslib.items[attacker.hand].weaponData['type'] == 'magic'):
                    weapon = itemslib.items[attacker.hand]
                if spell.magicType == 'old':
                    damage = int(spell.damage * math.sqrt(attackerSpell['lvl']))
                    attackerSpell['cd'] = spell.cooldown
                else:
                    if weapon is not None:
                        damage = spell.damage + weapon.weaponData['damage']
                totalDamage = 0
                for targetTag in targetsTags:
                    combatChars[targetTag].health -= damage
                    totalDamage += damage
                    if combatChars[targetTag].health < 0:
                        combatChars[targetTag].health = 0
                if weapon is not None:
                    manaCost = spell.cost - weapon.weaponData['mana']
                    if manaCost > 0:
                        attacker.mana -= manaCost
                else:
                    attacker.mana -= spell.cost
                return (1, totalDamage)
            else:
                # apply status effects
                return (1, 0)
        else:
            return (0, 0)

    def reduceCooldown(tag, ammount = 1):
        char = combatChars[tag]
        if (char.spells[0] is not None) and (char.spells[0]['cd'] > 0):
            char.spells[0]['cd'] -= ammount
        if (char.spells[1] is not None) and (char.spells[1]['cd'] > 0):
            char.spells[1]['cd'] -= ammount

        