init python:
    import store.playerLib as playerLib
    import store.combatLib as combatLib

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

screen skillTooltip(skill):
    zorder 100
    frame:
        xfill False
        yfill False
        anchor (-0.05, 1.05)
        xsize 400
        use skillDetailBox(skill)
        at followMouse
screen skillDetailBox(skill):
    python:
        char = None
        if playerLib.selected_guardian is not None:
            if playerLib.selected_guardian in combatLib.arena:
                char = combatLib.arena[playerLib.selected_guardian]
        damage = skill.skill_data.damage
        accu = skill.skill_data.accuracy
        crit = (skill.skill_data.finesse + char.finesse) * combatLib.crit_multiplier
        if skill.skill_data.skill_type == 'melee':
            damage += char.strength
        if skill.skill_data.skill_type == 'range':
            accu += char.accuracy
            crit += (skill.skill_data.accuracy + char.accuracy) * combatLib.range_crit_multiplier
        accu = accu * combatLib.accu_multiplier
    vbox:
        spacing 10
        text "{}".format(skill.name)
        hbox:
            text "{}".format(skill.skill_data.skill_type) style "sublabel"
            if skill.skill_data.magic_type is not None:
                text "| {} magic".format(skill.skill_data.magic_type) style "sublabel"
        if skill.skill_data.mp_cost > 0:
            text "MP Cost: {}".format(skill.skill_data.mp_cost) style "label"
        text " •Target: {}".format(skill.skill_data.target) style "label"
        if damage > 0:
            text " •Dmg: {}".format(damage) style "label"
        if accu > 0:
            text " •Acu: {}%".format(accu) style "label"
        if crit > 0:
            text " •Crit: {}%".format(crit) style "label"
        if skill.skill_data.hits > 1:
            text " •Hits: {}".format(skill.skill_data.hits) style "label"
        if skill.skill_data.heal > 0:
            text " •HP: +{}".format(skill.skill_data.heal) style "label"
        if skill.skill_data.mp != 0:
            text " •MP: {0:+}".format(skill.skill_data.mp) style "label"
        if skill.skill_data.speed != 0:
            text " •Spd: {0:+}".format(skill.skill_data.speed) style "label"
        # if hasattr(skill, 'mpReduction') and (skill.mpReduction > 0):
        #     text " •TS MP: {}".format(skill.mpReduction) style "label"
        if skill.skill_data.base_cd > 0:
            text " •CD: {} rounds".format(skill.skill_data.base_cd) style "label"
        if len(skill.skill_data.active_effects) > 0:
            text " Effects:" style "sublabel"
            for effect in skill.skill_data.active_effects:
                if isinstance(effect, tuple) or isinstance(effect, list):
                    text "  ○ {}".format(effect[0]) style "sublabel"
                else:
                    text "  ○ {}".format(effect) style "sublabel"
        text "{}".format(skill.description) style "sublabel"


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
        def_dif = (char.base_defense - char.defense)*-1
        mag_def_dif = (char.base_mag_defense - char.mag_defense)*-1
        ref_dif = (char.base_reflexes - char.reflexes)*-1
        str_dif = (char.base_strength - char.strength)*-1
        spd_dif = (char.base_speed - char.speed)*-1
        acu_dif = (char.base_accuracy - char.accuracy)*-1
        fin_dif = (char.base_finesse - char.finesse)*-1
    vbox:
        text "{}".format(char.name) style "label"
        text "HP: {}/{}".format(char.hp, char.base_hp) style "sublabel"
        text "MP: {}/{}".format(char.mp, char.base_mp) style "sublabel"
        hbox:
            text "Def: {}".format(char.base_defense) style "sublabel"
            if def_dif != 0:
                text " {0:+}".format(def_dif) color ("#ff0000ff" if def_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Mag Def: {}".format(char.mag_defense) style "sublabel"
            if mag_def_dif != 0:
                text " {0:+}".format(mag_def_dif) color ("#ff0000ff" if mag_def_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Ref: {}".format(char.base_reflexes) style "sublabel"
            if ref_dif != 0:
                text " {0:+}".format(ref_dif) color ("#ff0000ff" if ref_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Str: {}".format(char.base_strength) style "sublabel"
            if str_dif != 0:
                text " {0:+}".format(str_dif) color ("#ff0000ff" if str_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Spd: {}".format(char.speed) style "sublabel"
            if spd_dif != 0:
                text " {0:+}".format(spd_dif) color ("#ff0000ff" if spd_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Acu: {}".format(char.accuracy) style "sublabel"
            if acu_dif != 0:
                text " {0:+}".format(acu_dif) color ("#ff0000ff" if acu_dif < 0 else "#11ff00ff") style "sublabel"
        hbox:
            text "Fin: {}".format(char.finesse) style "sublabel"
            if fin_dif != 0:
                text " {0:+}".format(fin_dif) color ("#ff0000ff" if fin_dif < 0 else "#11ff00ff") style "sublabel"
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
        if effect.mp != 0:
            text "• MP: {0:+}".format(effect.mp) color ("#ff0000ff" if effect.mp < 0 else "#11ff00ff") style "sublabel"
        if effect.defense != 0:
            text "• Def: {0:+}%".format(effect.defense) color ("#ff0000ff" if effect.defense < 0 else "#11ff00ff") style "sublabel"
        if effect.mag_defense != 0:
            text "• Mag Def: {0:+}%".format(effect.mag_defense) color ("#ff0000ff" if effect.mag_defense < 0 else "#11ff00ff") style "sublabel"
        if effect.reflexes != 0:
            text "• Ref: {0:+}%".format(effect.reflexes) color ("#ff0000ff" if effect.reflexes < 0 else "#11ff00ff") style "sublabel"
        if effect.strength != 0:
            text "• Str: {0:+}%".format(effect.strength) color ("#ff0000ff" if effect.strength < 0 else "#11ff00ff") style "sublabel"
        if effect.speed != 0:
            text "• Spd: {0:+}%".format(effect.speed) color ("#ff0000ff" if effect.speed < 0 else "#11ff00ff") style "sublabel"
        if effect.accuracy != 0:
            text "• Acu: {0:+}%".format(effect.accuracy) color ("#ff0000ff" if effect.accuracy < 0 else "#11ff00ff") style "sublabel"
        if effect.finesse != 0:
            text "• Fin: {0:+}%".format(effect.finesse) color ("#ff0000ff" if effect.finesse < 0 else "#11ff00ff") style "sublabel"
        if effect.description:
            text "• {}".format(effect.description) style "sublabel"