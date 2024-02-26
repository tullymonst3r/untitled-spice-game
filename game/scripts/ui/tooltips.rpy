init python:
    import store.playerLib as playerLib
    import store.combatlib as combatlib

    def updateTooltipPos(tf,st,at):
        mx,my=renpy.get_mouse_pos()
        tf.pos=(mx,my)
        return 0
    def updateCharTooltipPos(tf,st,at):
        mx,my=renpy.get_mouse_pos()
        if mx > 1620:
            mx = 1620
        tf.pos=(mx,my)
        return 0
    def updateEffectTooltipPos(tf,st,at):
        mx,my=renpy.get_mouse_pos()
        if mx > 1695:
            mx = 1695
        tf.pos=(mx,my)
        return 0

transform followMouse:
    function updateTooltipPos
transform followMouseChar:
    function updateCharTooltipPos
transform followMouseEffect:
    function updateEffectTooltipPos

screen equipmentTooltip(equipment):
    zorder 100
    frame:
        xfill False
        yfill False
        anchor (-0.05, 1.05)
        xsize 400
        use equipmentDetailBox(equipment)
        at followMouse
screen equipmentDetailBox(equipment):
    python:
        className = equipment.__class__.__name__
        attackType = None
        weaponType = ''
        if hasattr(equipment, 'weaponType'): weaponType = ": {}".format(equipment.weaponType)
        char = None
        if playerLib.selectedGuardian is not None:
            if playerLib.selectedGuardian in combatlib.combatChars:
                char = combatlib.combatChars[playerLib.selectedGuardian]
            elif playerLib.selectedGuardian in combatlib.arenaChars:
                char = combatlib.arenaChars[playerLib.selectedGuardian]
        damage = equipment.attackData.damage
        accu = (equipment.attackData.accuracy + char.baseAccuracy) * combatlib.accuMultiplier
        crit = (equipment.attackData.finesse + char.baseFinesse) * combatlib.critMultiplier
        mpCost = 0
        magicType = None
        if (className == 'Item'):
            attackType = equipment.weaponType
        elif (className == 'Attack'):
            attackType = equipment.attackType
        elif (className == 'Spell'):
            attackType = 'magic'
            mpCost = equipment.cost - char.tsTotalMana if equipment.cost > char.tsTotalMana else 0
            if (equipment.magicType == 'new') and (equipment.attackData.damage > 0):
                damage += char.tsTotalDamage
        if attackType == 'melee':
            damage += char.baseStrength
            accu = 0
        elif attackType == 'magic':
            crit = 0
            magicType = 'new'
            if hasattr(equipment, 'magicType'):
                magicType = equipment.magicType
        elif attackType == 'consumable':
            crit = 0
        if damage == 0:
            accu = 0
        if (hasattr(equipment.attackData, 'noDamage')) and (equipment.attackData.noDamage):
            damage = 0
            crit = 0
        if accu > 100:
            accu = 100
        if crit > 100:
            crit = 100
    vbox:
        spacing 10
        text "{}".format(equipment.name)
        text "{}{}".format("{} ".format(magicType) if magicType is not None else '', attackType) style "sublabel"
        if className == 'Spell':
            text "MP Cost: {}".format(mpCost) style "label"
        text " •Target: {}".format(equipment.attackData.target) style "label"
        if damage > 0:
            text " •Dmg: {}".format(damage) style "label"
        if accu > 0:
            text " •Acu: {}%".format(accu) style "label"
        if crit > 0:
            text " •Crit: {}%".format(crit) style "label"
        if equipment.attackData.hits > 1:
            text " •Hits: {}".format(equipment.attackData.hits) style "label"
        if equipment.attackData.heal > 0:
            text " •HP: +{}".format(equipment.attackData.heal) style "label"
        if equipment.attackData.mana != 0:
            text " •MP: {}{}".format('+' if equipment.attackData.mana > 0 else '', equipment.attackData.mana) style "label"
        if equipment.attackData.weight != 0:
            text " •Spd: {}{}".format('-' if equipment.attackData.weight > 0 else '+', abs(equipment.attackData.weight)) style "label"
        if hasattr(equipment, 'manaReduction') and (equipment.manaReduction > 0):
            text " •TS MP: {}".format(equipment.manaReduction) style "label"
        if equipment.attackData.baseCooldown > 0:
            text " •CD: {} rounds".format(equipment.attackData.baseCooldown) style "label"
        if len(equipment.attackData.active_effects) > 0:
            text " Effects:" style "sublabel"
            for effectTag in equipment.attackData.active_effects:
                text "  ○ {}".format(effectsLib.effects[effectTag].name) style "sublabel"
        text "{}".format(equipment.description) style "sublabel"


screen charTooltip(char):
    zorder 100
    frame:
        xfill False
        yfill False
        anchor (-0.05, 1.05)
        xsize 300
        use charDetailBox(char)
        at followMouseChar
screen charDetailBox(char):
    python:
        reducedStr = (char.baseStrength - char.strength)*-1
        reducedDef = (char.baseDefense - char.defense)*-1
        reducedMagDef = (char.baseMagicDef - char.magicDef)*-1
        reducedSpd = (char.baseSpeed - char.speed)*-1
        reducedAcu = (char.baseAccuracy - char.accuracy)*-1
        reducedFin = (char.baseFinesse - char.finesse)*-1
    vbox:
        text "{}".format(char.name) style "label"
        text "HP: {}/{}".format(char.health, char.baseHealth) style "sublabel"
        text "MP: {}/{}".format(char.mana, char.baseMana) style "sublabel"
        hbox:
            text "Str: {}".format(char.baseStrength) style "sublabel"
            if reducedStr != 0:
                text " {0:+}".format(reducedStr) color ("#ff0000ff" if reducedStr < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Def: {}".format(char.baseDefense) style "sublabel"
            if reducedDef != 0:
                text " {0:+}".format(reducedDef) color ("#ff0000ff" if reducedDef < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Mag Def: {}".format(char.magicDef) style "sublabel"
            if reducedMagDef != 0:
                text " {0:+}".format(reducedMagDef) color ("#ff0000ff" if reducedMagDef < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Spd: {}".format(char.speed) style "sublabel"
            if reducedSpd != 0:
                text " {0:+}".format(reducedSpd) color ("#ff0000ff" if reducedSpd < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Acu: {}".format(char.accuracy) style "sublabel"
            if reducedAcu != 0:
                text " {0:+}".format(reducedAcu) color ("#ff0000ff" if reducedAcu < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Fin: {}".format(char.finesse) style "sublabel"
            if reducedFin != 0:
                text " {0:+}".format(reducedFin) color ("#ff0000ff" if reducedFin < 0 else "#11ff00ff") style "sublabel"
        # text "TS MP: {}".format(char.tsTotalMana) style "sublabel"

screen effectTooltip(effect):
    zorder 100
    frame:
        xfill False
        yfill False
        anchor (-0.05, 1.05)
        xsize 225
        use effectDetailBox(effect)
        at followMouseEffect
screen effectDetailBox(effect):
    vbox:
        text "{}".format(effect.name) style "label"
        text "Duration: {} rounds".format(effect.duration) style "sublabel"
        if effect.hp != 0:
            text "• HP: {0:+}".format(effect.hp) color ("#ff0000ff" if effect.hp < 0 else "#11ff00ff") style "sublabel"
        if effect.mana != 0:
            text "• MP: {0:+}".format(effect.mana) color ("#ff0000ff" if effect.mana < 0 else "#11ff00ff") style "sublabel"
        if effect.defense != 0:
            text "• Def: {0:+}%".format(effect.defense) color ("#ff0000ff" if effect.defense < 0 else "#11ff00ff") style "sublabel"
        if effect.magicDef != 0:
            text "• Mag Def: {0:+}%".format(effect.magicDef) color ("#ff0000ff" if effect.magicDef < 0 else "#11ff00ff") style "sublabel"
        if effect.strength != 0:
            text "• Str: {0:+}%".format(effect.strength) color ("#ff0000ff" if effect.strength < 0 else "#11ff00ff") style "sublabel"
        if effect.speed != 0:
            text "• Spd: {0:+}%".format(effect.speed) color ("#ff0000ff" if effect.speed < 0 else "#11ff00ff") style "sublabel"
        if effect.accuracy != 0:
            text "• Acu: {0:+}%".format(effect.accuracy) color ("#ff0000ff" if effect.accuracy < 0 else "#11ff00ff") style "sublabel"
        if effect.finesse != 0:
            text "• Fin: {0:+}%".format(effect.finesse) color ("#ff0000ff" if effect.finesse < 0 else "#11ff00ff") style "sublabel"
        if effect.nimbleness != 0:
            text "• Nim: {0:+}%".format(effect.nimbleness) color ("#ff0000ff" if effect.nimbleness < 0 else "#11ff00ff") style "sublabel"
        if effect.focus != 0:
            text "• Foc: {0:+}%".format(effect.focus) color ("#ff0000ff" if effect.focus < 0 else "#11ff00ff") style "sublabel"
        if effect.description:
            text "• {}".format(effect.description) style "sublabel"