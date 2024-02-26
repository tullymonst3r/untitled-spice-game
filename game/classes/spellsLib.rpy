init -8 python in spellslib:
    import copy
    import random
    import store.combatlib as combatlib
    import store.effectsLib as effectsLib
    spells = {}

    def addSpell(tag: str, spell: Spell):
        global spells
        spell.tag = tag
        spells[tag] = spell
        spells = spells

    class Spell(object):
        def __init__(self, name: str, magicType: str, cost: int, *args, **kwargs):
            self.name = name
            self.magicType = magicType # old | new
            self.cost = cost
            self.tag = kwargs.get('tag', None)
            self.cd = kwargs.get('cd', 0) # cooldown
            self.description = kwargs.get('description', '')
            self.cooldown = kwargs.get('cooldown', 0)
            self.icon = kwargs.get('icon', '')
            self.attackData = kwargs.get('attackData', combatlib.AttackData())
            self.xpPrice = kwargs.get('xpPrice', 250) # Cost to unlock spell
        def __str__(self):
            return self.name

    def summonDemon(attacker: combatlib.CombatCharacter, summonTag):
        combatDemon = combatlib.combatChars['demon']
        # Create copy of demon
        demonCopy = copy.deepcopy(combatDemon)
        demonCopyTag = 'demon' + str(len(combatlib.arenaTags))
        demonCopy.tag=demonCopyTag
        demonCopy.isPlayable=False
        demonCopy.effects['summon']=5 # Maybe extract this from effects lib?

        # Insert demon into combat after attacker's turn
        index = combatlib.arenaTags.index(attacker.tag)
        combatlib.arenaTags.insert(index+1, demonCopyTag)
        x = attacker.x
        y = attacker.y
        zorder = attacker.zorder - 1
        if attacker.tag in combatlib.allies:
            index = combatlib.allies.index(attacker.tag)
            combatlib.allies.insert(index+1, demonCopyTag)
            index = combatlib.alliesAlive.index(attacker.tag)
            combatlib.alliesAlive.insert(index+1, demonCopyTag)
            # random.uniform(200, -200)
            x += 150
            y -= 150
        if attacker.tag in combatlib.enemies:
            index = combatlib.enemies.index(attacker.tag)
            combatlib.enemies.insert(index+1, demonCopyTag)
            index = combatlib.enemiesAlive.index(attacker.tag)
            combatlib.enemiesAlive.insert(index+1, demonCopyTag)
            x -= 150
            y -= 150
        renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=demonCopy, _zorder=zorder)
        renpy.show_screen("charStatus", _tag="status_"+str(x)+str(y), char=demonCopy)
        demonCopy.x = x
        demonCopy.y = y
        demonCopy.zorder = zorder
        combatlib.arenaChars[demonCopyTag] = demonCopy

    def transformTo(attacker: combatlib.CombatCharacter, transformTag):
        ogCombatChar = combatlib.combatChars[transformTag]
        # Create copy of demon
        tranCharCopy = copy.deepcopy(ogCombatChar)
        tranCharCopyTag = transformTag + str(len(combatlib.arenaTags))
        tranCharCopy.transFrom=attacker.tag
        tranCharCopy.tag=tranCharCopyTag
        tranCharCopy.name="{} ({})".format(attacker.name, ogCombatChar.name)
        tranCharCopy.baseTurns=attacker.baseTurns
        tranCharCopy.turns=attacker.turns
        tranCharCopy.x=attacker.x
        tranCharCopy.y=attacker.y
        tranCharCopy.zorder=attacker.zorder
        tranCharCopy.effects = copy.deepcopy(attacker.effects)
        tranCharCopy.effects['trans']=3 # Maybe extract this from effects lib?
        attackerHpPercent = (attacker.health/attacker.baseHealth) * 100
        tranCharCopy.health = int((tranCharCopy.baseHealth/100) * attackerHpPercent)
        effectsLib.triggerStatModifiers(tranCharCopy)
        combatlib.arenaChars[tranCharCopyTag] = tranCharCopy
        renpy.show_screen("char_sprite", _tag=str(tranCharCopy.x) + str(tranCharCopy.y), char=tranCharCopy, _zorder=tranCharCopy.zorder)
        renpy.show_screen("charStatus", _tag="status_"+str(tranCharCopy.x)+str(tranCharCopy.y), char=tranCharCopy)

        # Insert transform char into the attacker's turn
        index = combatlib.arenaTags.index(attacker.tag)
        combatlib.arenaTags[index] = tranCharCopyTag
        if attacker.tag in combatlib.allies:
            index = combatlib.allies.index(attacker.tag)
            combatlib.allies[index] = tranCharCopyTag
            index = combatlib.alliesAlive.index(attacker.tag)
            combatlib.alliesAlive[index] = tranCharCopyTag
        if attacker.tag in combatlib.enemies:
            index = combatlib.enemies.index(attacker.tag)
            combatlib.enemies[index] = tranCharCopyTag
            index = combatlib.enemiesAlive.index(attacker.tag)
            combatlib.enemiesAlive[index] = tranCharCopyTag