init -7 python in effectsLib:
    import store.combatlib as combatlib
    import math
    import copy

    effects = {}

    def addEffect(tag: str, effect: Effect):
        global effects
        effect.tag = tag
        effects[tag] = effect
        effects = effects

    class Effect(object):
        def __init__(self, name: str, icon: str, duration: int, *args, **kwargs):
            self.name = name # Name display. (str)
            self.icon = icon # effect icon displayed on sprite. (str)
            self.duration = duration # Time it takes to wear off. set to -1 for perpetual effect (int)
            self.description = kwargs.get('description', '')
            self.tag = kwargs.get('tag', None)
            self.sfx = kwargs.get('sfx', None)
            # self.effectType = kwargs.get('effectType', 0) # -1 negative | 0 neutral | 1 positive
            self.instant_effect = kwargs.get('instant_effect', False) # Whether the effect will have instant effect. (boolean)
            self.hp = kwargs.get('hp', 0) # Healing applied each round. Set to negative for damage. (int)
            self.mana = kwargs.get('mana', 0) # Mana regenerated each round. Set to negative to reduce. (int)
            self.defense = kwargs.get('defense', 0) # % of base defense increased. Set to negatives to reduce. (int)
            self.strength = kwargs.get('strength', 0) # % of base strength increased. Set to negatives to reduce. (int)
            self.finesse = kwargs.get('finesse', 0) # % of base finesse increased. Set to negatives to reduce. (int)
            self.speed = kwargs.get('speed', 0) # % of base speed increased. Set to negatives to reduce. (int)
            self.accuracy = kwargs.get('accuracy', 0) # % of base speed increased. Set to negatives to reduce. (int)
            self.magicDef = kwargs.get('magicDef', 0) # % of base speed increased. Set to negatives to reduce. (int)
            self.nimbleness = kwargs.get('nimbleness', 0) # % of base speed increased. Set to negatives to reduce. (int)
            self.focus = kwargs.get('focus', 0) # % of base speed increased. Set to negatives to reduce. (int)
            
            self.applyAction = kwargs.get('applyAction', None) # Name of function called when effect activates. (str)
            self.removeAction = kwargs.get('removeAction', None) # Name of function called when effect is removed. (str)
            self.specialVal = kwargs.get('specialVal', None) # Special value used when effect activates
        def __str__(self):
            return self.name

    addEffect('cursed', Effect('Cursed', 'cursed', 2, hp=-5, mana=-5, sfx="22_Slash_04.mp3"))
    addEffect('exposed1', Effect('Exposed 1', 'exposed', 3, defense=-30, instant_effect=True))
    addEffect('toughen1', Effect('Toughen 1', 'toughen', 3, defense=30, instant_effect=True))
    addEffect('regen1', Effect('Regeneration 1', 'regen', 2, hp=10, sfx="02_Heal_02.mp3"))
    addEffect('regen2', Effect('Regeneration 2', 'regen', 2, hp=25, sfx="02_Heal_02.mp3"))
    addEffect('haste1', Effect('Haste 1', 'haste', 3, speed=40, instant_effect=True))
    addEffect('power1', Effect('Power 1', 'power', 3, strength=40, instant_effect=True))
    addEffect('slow1', Effect('Slowness 1', 'slow', 3, speed=-40, instant_effect=True))
    addEffect('accu1', Effect('Accuracy 1', 'accu', 3, accuracy=15, instant_effect=True))
    addEffect('overclock1', Effect('Overclock 1', 'overclock', 0, instant_effect=True, applyAction="overclockApply", removeAction="overclockRemove", specialVal=2))
    addEffect('stunned', Effect('Stunned', 'stunned', 1, applyAction="stunApply", removeAction="stunRemove"))
    addEffect('summon', Effect('Summon', 'summon', 5, description="Entity dies after the effect is over.", removeAction="killSummon"))
    addEffect('trans', Effect('Transformation', 'transformation', 3, description="Char returns to it's original form after the effect is over", removeAction="detransform"))

    addEffect('drunk', Effect('Drunk', 'drunk', 3, instant_effect=True, finesse=-100, nimbleness=50, accuracy=-50, strength=-10, speed=-10))

    def triggerStatModifiers(char: combatlib.CombatCharacter):
        char.defense = char.baseDefense
        char.strength = char.baseStrength
        char.finesse = char.baseFinesse
        char.speed = char.baseSpeed
        char.accuracy = char.baseAccuracy
        char.magicDef = char.baseMagicDef
        char.nimbleness = char.baseNimbleness
        char.focus = char.baseFocus
        for effectTuple in char.effects.items():
            effectTag = effectTuple[0]
            effect = effects[effectTag]
            if effect.defense != 0:
                defenseModifier = (char.baseDefense * (abs(effect.defense / 100))) * math.copysign(1, effect.defense)
                char.defense += int(defenseModifier)
            if effect.strength != 0:
                strengthModifier = (char.baseStrength * (abs(effect.strength / 100))) * math.copysign(1, effect.strength)
                char.strength += int(strengthModifier)
            if effect.finesse != 0:
                finesseModifier = (char.baseFinesse * (abs(effect.finesse / 100))) * math.copysign(1, effect.finesse)
                char.finesse += int(finesseModifier)
            if effect.speed != 0:
                speedModifier = (char.baseSpeed * (abs(effect.speed / 100))) * math.copysign(1, effect.speed)
                char.speed += int(speedModifier)
            if effect.accuracy != 0:
                accuracyModifier = (char.baseAccuracy * (abs(effect.accuracy / 100))) * math.copysign(1, effect.accuracy)
                char.accuracy += int(accuracyModifier)
            if effect.magicDef != 0:
                magicDefModifier = (char.baseMagicDef * (abs(effect.magicDef / 100))) * math.copysign(1, effect.magicDef)
                char.magicDef += int(magicDefModifier)
            if effect.nimbleness != 0:
                nimblenessModifier = (char.baseNimbleness * (abs(effect.nimbleness / 100))) * math.copysign(1, effect.nimbleness)
                char.nimbleness += int(nimblenessModifier)
            if effect.focus != 0:
                focusModifier = (char.baseFocus * (abs(effect.focus / 100))) * math.copysign(1, effect.focus)
                char.focus += int(focusModifier)


    def triggerInstantEffect(char: combatlib.CombatCharacter, effect: Effect):
        if effect.hp > 0:
            # heal
            missingHealth = (char.baseHealth - char.health)
            realHealing = effect.hp if effect.hp < missingHealth else missingHealth
            char.health += realHealing
            renpy.show_screen("number_effect", x=char.x, y=char.y, val=realHealing, textColor="#1dff25", _tag='heal_'+str(char.x)+str(char.y), _transient=True)
        elif effect.hp < 0:
            # damage
            realDamage = effect.hp if effect.hp < char.health else char.health
            char.health += realDamage
            renpy.show_screen("number_effect", x=char.x, y=char.y, val=realDamage, textColor="#ff1d1d", _tag='dam_'+str(char.x)+str(char.y), _transient=True)
        if effect.mana > 0:
            missingMana = (char.baseMana - char.mana)
            manaModifier = effect.mana if effect.mana < missingMana else missingMana
            char.mana += manaModifier
            renpy.show_screen("number_effect", x=char.x, y=char.y, val=manaModifier, textColor="#3bd5ff", _tag='man_'+str(char.x)+str(char.y), _transient=True)
        elif effect.mana < 0:
            absMana = abs(effect.mana)
            manaModifier = absMana if absMana < char.mana else char.mana
            char.mana -= manaModifier
            renpy.show_screen("number_effect", x=char.x, y=char.y, val=manaModifier, textColor="#803bff", _tag='men_'+str(char.x)+str(char.y), _transient=True)
        if (effect.defense != 0) or (effect.strength != 0) or (effect.finesse != 0) or (effect.speed != 0) or (effect.accuracy != 0) or (effect.magicDef != 0) or (effect.nimbleness != 0) or (effect.focus != 0):
            triggerStatModifiers(char)
        if effect.applyAction is not None:
            possibles = globals().copy()
            possibles.update(locals())
            method = possibles.get(effect.applyAction)
            method(char, effect, effect.tag)
        if effect.sfx is not None:
            renpy.play("audio/sfx/{}".format(effect.sfx), channel='audio')

    def triggerRoundEffects(char: combatlib.CombatCharacter):
        char.defense = char.baseDefense
        char.strength = char.baseStrength
        char.finesse = char.baseFinesse
        char.speed = char.baseSpeed
        char.accuracy = char.baseAccuracy
        char.magicDef = char.baseMagicDef
        char.nimbleness = char.baseNimbleness
        char.focus = char.baseFocus
        removedEffects = []
        for effectTuple in char.effects.items():
            effectTag = effectTuple[0]
            duration = effectTuple[1]
            effect = effects[effectTag]
            if effect.hp > 0:
                # heal
                missingHealth = (char.baseHealth - char.health)
                realHealing = effect.hp if effect.hp < missingHealth else missingHealth
                char.health += realHealing
                renpy.show_screen("number_effect", x=char.x, y=char.y, val=realHealing, textColor="#1dff25", _tag='heal_'+str(char.x)+str(char.y), _transient=True)
            elif effect.hp < 0:
                # damage
                realDamage = effect.hp if effect.hp < char.health else char.health
                char.health += realDamage
                renpy.show_screen("number_effect", x=char.x, y=char.y, val=realDamage, textColor="#ff1d1d", _tag='dam_'+str(char.x)+str(char.y), _transient=True)
            if effect.mana > 0:
                missingMana = (char.baseMana - char.mana)
                manaModifier = effect.mana if effect.mana < missingMana else missingMana
                char.mana += manaModifier
                renpy.show_screen("number_effect", x=char.x, y=char.y, val=manaModifier, textColor="#3bd5ff", _tag='man_'+str(char.x)+str(char.y), _transient=True)
            elif effect.mana < 0:
                absMana = abs(effect.mana)
                manaModifier = absMana if absMana < char.mana else char.mana
                char.mana -= manaModifier
                renpy.show_screen("number_effect", x=char.x, y=char.y, val=manaModifier, textColor="#803bff", _tag='men_'+str(char.x)+str(char.y), _transient=True)
            if duration > 1:
                if effect.defense != 0:
                    defenseModifier = (char.baseDefense * (abs(effect.defense / 100))) * math.copysign(1, effect.defense)
                    char.defense += int(defenseModifier)
                if effect.strength != 0:
                    strengthModifier = (char.baseStrength * (abs(effect.strength / 100))) * math.copysign(1, effect.strength)
                    char.strength += int(strengthModifier)
                if effect.finesse != 0:
                    finesseModifier = (char.baseFinesse * (abs(effect.finesse / 100))) * math.copysign(1, effect.finesse)
                    char.finesse += int(finesseModifier)
                if effect.speed != 0:
                    speedModifier = (char.baseSpeed * (abs(effect.speed / 100))) * math.copysign(1, effect.speed)
                    char.speed += int(speedModifier)
                if effect.accuracy != 0:
                    accuracyModifier = (char.baseAccuracy * (abs(effect.accuracy / 100))) * math.copysign(1, effect.accuracy)
                    char.accuracy += int(accuracyModifier)
                if effect.magicDef != 0:
                    magicDefModifier = (char.baseMagicDef * (abs(effect.magicDef / 100))) * math.copysign(1, effect.magicDef)
                    char.magicDef += int(magicDefModifier)
                if effect.nimbleness != 0:
                    nimblenessModifier = (char.baseNimbleness * (abs(effect.nimbleness / 100))) * math.copysign(1, effect.nimbleness)
                    char.nimbleness += int(nimblenessModifier)
                if effect.focus != 0:
                    focusModifier = (char.baseFocus * (abs(effect.focus / 100))) * math.copysign(1, effect.focus)
                    char.focus += int(focusModifier)
            if effect.applyAction is not None:
                possibles = globals().copy()
                possibles.update(locals())
                method = possibles.get(effect.applyAction)
                method(char, effect, effect.tag)
            if effect.sfx is not None:
                renpy.play("audio/sfx/{}".format(effect.sfx), channel='audio')
            # Reduce duration each round
            if char.effects[effectTag] > 0:
                char.effects[effectTag] -= 1
            if char.effects[effectTag] == 0:
                if effect.removeAction is None:
                    removedEffects.append(effectTag)
        for tag in removedEffects:
            char.effects.pop(tag)
    
    def triggerRemoveActions(char: combatlib.CombatCharacter):
        removedEffects = []
        addedEffects = []
        for effectTuple in char.effects.items():
            effectTag = effectTuple[0]
            effect = effects[effectTag]
            if char.effects[effectTag] == 0:
                if effect.removeAction is not None:
                    possibles = globals().copy()
                    possibles.update(locals())
                    method = possibles.get(effect.removeAction)
                    newEffects = method(char, effect, effect.tag)
                    addedEffects = addedEffects + newEffects
                removedEffects.append(effectTag)
        for tag in removedEffects:
            char.effects.pop(tag)
        for tag in addedEffects:
            effect = effects[tag]
            char.effects[tag] = effect.duration
            if effect.instant_effect:
                triggerInstantEffect(char, effect)
            
    def overclockApply(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        if effect.specialVal is not None:
            char.turns = char.baseTurns + effect.specialVal
    def overclockRemove(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        renpy.pause(1.0)
        char.turns = char.baseTurns
        renpy.play("audio/sfx/21_Debuff_01.mp3", channel='audio')
        renpy.show_screen("hex", positions=[(char.x, char.y)], _tag='an_'+str(char.x)+str(char.y),_transient=True)
        return ['slow1']
    def stunApply(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        char.turns = char.baseTurns - 1 # 1 turn or all turns?
        renpy.show_screen("msg_effect", x=char.x, y=char.y, text="STUNNED", _tag='msg_'+str(char.x)+str(char.y), _transient=True)
        if char.turns > 0:
            renpy.pause(1.0)
    def stunRemove(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        char.turns = char.baseTurns
        return []
    def killSummon(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        char.health = 0
        return []
    def detransform(char: combatlib.CombatCharacter, effect: Effect, effectTag):
        renpy.pause(1.0)
        # Give the original char the proportional health
        transChar = combatlib.arenaChars[char.transFrom]
        hpPercent = (char.health/char.baseHealth) * 100
        transChar.health = int((transChar.baseHealth/100) * hpPercent)
        transChar.damageDone += char.damageDone
        transChar.healDone += char.healDone
        transChar.effects = copy.deepcopy(char.effects)
        transChar.effects['drunk'] = effects['drunk'].duration
        if 'trans' in transChar.effects:
            transChar.effects.pop('trans')
        triggerStatModifiers(transChar)
        renpy.show_screen("char_sprite", _tag=str(transChar.x) + str(transChar.y), char=transChar, _zorder=transChar.zorder)
        renpy.show_screen("charStatus", _tag="status_"+str(transChar.x)+str(transChar.y), char=transChar)

        # Return original char to the list
        index = combatlib.arenaTags.index(char.tag)
        combatlib.arenaTags[index] = char.transFrom
        if char.tag in combatlib.allies:
            index = combatlib.allies.index(char.tag)
            combatlib.allies[index] = char.transFrom
            index = combatlib.alliesAlive.index(char.tag)
            combatlib.alliesAlive[index] = char.transFrom
        if char.tag in combatlib.enemies:
            index = combatlib.enemies.index(char.tag)
            combatlib.enemies[index] = char.transFrom
            index = combatlib.enemiesAlive.index(char.tag)
            combatlib.enemiesAlive[index] = char.transFrom
        renpy.play("audio/sfx/21_Debuff_01.mp3", channel='audio')
        renpy.show_screen("magicHit", positions=[(transChar.x, transChar.y)], _tag='an_'+str(transChar.x)+str(transChar.y),_transient=True)
        return []



            
