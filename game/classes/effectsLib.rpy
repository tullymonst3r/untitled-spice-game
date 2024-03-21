init -7 python in effectsLib:
    import store.combatLib as combatLib
    import store.charsLib as charsLib
    import math
    import copy
    import json

    def getEffect(tag):
        effects_json = open(renpy.config.gamedir + "/db/effects.json", "r")
        loaded_effects = json.load(effects_json)
        effect = loaded_effects[tag]
        effects_json.close()
        return copy.deepcopy(Effect(tag=tag, **effect))
    def getSpecialEffect(tag):
        effects_json = open(renpy.config.gamedir + "/db/special_effects.json", "r")
        loaded_effects = json.load(effects_json)
        effect = loaded_effects[tag]
        effects_json.close()
        return copy.deepcopy(SpecialEffect(tag=tag, **effect))
    
    class SpecialEffect(object):
        def __init__(self, tag: str, duration: int, *args, **kwargs):
            self.tag = tag
            self.duration = duration # Time it takes to wear off. set to -1 for perpetual effect (int)
            self.icon = kwargs.get('icon', tag) # effect icon displayed on sprite. (str)
            self.name = kwargs.get('name', 'Effect')
            self.description = kwargs.get('description', '')
            self.chance = kwargs.get('chance', 0) # % of chance of this effect being called
            self.action_fcn = kwargs.get('action_fcn', None) # Name of function called when effect activates. (str)
            self.special_val = kwargs.get('special_val', None) # Special value used when effect activates

    class Effect(object):
        def __init__(self, name: str, tag: str, duration: int, *args, **kwargs):
            self.name = name # Name display. (str)
            self.tag = tag
            self.duration = duration # Time it takes to wear off. set to -1 for perpetual effect (int)
            self.icon = kwargs.get('icon', tag) # effect icon displayed on sprite. (str)
            self.description = kwargs.get('description', '')
            self.sfx = kwargs.get('sfx', None)

            self.instant_effect = kwargs.get('instant_effect', False) # Whether the effect will have instant effect. (boolean)
            self.effect_activation = kwargs.get('effect_activation', 'passive') # passive | active | reactive
            self.is_removable  = kwargs.get('is_removable', True) # Whether external events can remove this effect before its duration is over.
            self.effect_type = kwargs.get('effect_type', 'neutral') # neutral | positive | negative.
            self.effect_power = kwargs.get('effect_power', 1) # + 1.5 multiplier for each power point over 1. Stackable with other not perpetual effects

            self.hp = kwargs.get('hp', 0) # Healing applied each round. Set to negative for damage. (int)
            self.mp = kwargs.get('mp', 0) # Mp regenerated each round. Set to negative to reduce. (int)

            self.defense = kwargs.get('defense', 0)
            self.mag_defense = kwargs.get('mag_defense', 0)
            self.reflexes = kwargs.get('reflexes', 0)
            self.strength = kwargs.get('strength', 0)
            self.speed = kwargs.get('speed', 0)
            self.accuracy = kwargs.get('accuracy', 0)
            self.finesse = kwargs.get('finesse', 0)
            self.turns = kwargs.get('turns', 0)
            
            self.trigger_fcn = kwargs.get('trigger_fcn', None) # Name of function called when effect activates. (str)
            self.special_val = kwargs.get('special_val', None) # Special value used when effect activates
            self.remove_fcn = kwargs.get('remove_fcn', None) # Name of function called when effect is removed. (str)
        def __str__(self):
            return self.name
    
    def applyTeammatePreventiveEffects(char: charsLib.Char, added_effects):
        for item in added_effects:
            if isinstance(item, str):
                effect = getSpecialEffect(item)
            else:
                effect = getSpecialEffect(item[0])
                effect.duration = item[1]
            is_in_list = False
            if len(char.teammate_preventive_effects):
                for char_effect in char.teammate_preventive_effects:
                    if (char_effect.tag == effect.tag) and (char_effect.duration > -1):
                        is_in_list = True
                        char_effect.duration =  effect.duration
            if not is_in_list:
                char.teammate_preventive_effects.append(effect)
    def applyEffects(char: charsLib.Char, added_effects):
        for item in added_effects:
            if isinstance(item, str):
                effect = getEffect(item)
            # if isinstance(item, tuple) or isinstance(item, list): # (tag: str, power: int, duration?: int)
            else:
                effect = getEffect(item[0])
                effect.effect_power = item[1]
                if (item[2]): effect.duration = item[2]
            is_in_list = False
            if len(char.effects):
                for char_effect in char.effects:
                    if (char_effect.tag == effect.tag) and (char_effect.duration > -1):
                        is_in_list = True
                        char_effect.effect_power = effect.effect_power + char_effect.effect_power
                        char_effect.duration =  effect.duration
            if not is_in_list:
                char.effects.append(effect)
    
    def triggerEffects(char: charsLib.Char, *args, **kwargs):
        charsLib.resetStats(char)
        removed_effects = []
        for (index, effect) in enumerate(char.effects):
            if effect is not None:
                # if (effect.duration > 0) or (kwargs.get('only_instant', False)):
                multiplier = 1
                if effect.effect_power > 1: multiplier = 1.5 * (effect.effect_power - 1)
                if (effect.duration > 1):
                    if effect.defense != 0: char.defense += int(effect.defense * multiplier)
                    if effect.mag_defense != 0: char.mag_defense += int(effect.mag_defense * multiplier)
                    if effect.reflexes != 0: char.reflexes += int(effect.reflexes * multiplier)
                    if effect.speed != 0: char.speed += int(effect.speed * multiplier)
                    if effect.strength != 0: char.strength += int(effect.strength * multiplier)
                    if effect.accuracy != 0: char.accuracy += int(effect.accuracy * multiplier)
                    if effect.finesse != 0: char.finesse += int(effect.finesse * multiplier)
                if effect.turns != 0: char.turns += int(effect.turns * multiplier) # Might be too much
                if not kwargs.get('only_stats', False):
                    trigger = effect.instant_effect if kwargs.get('only_instant', False) else effect.effect_activation == kwargs.get('effect_activation', 'passive')
                    if trigger:
                        if effect.hp < 0: char.hurt(int(abs(effect.hp) * multiplier), is_magic_attack=False, ignore_defense=True)
                        if effect.hp > 0: char.heal(int(effect.hp * multiplier))
                        if effect.mp != 0: char.mpAlter(int(effect.mp * multiplier))
                        if effect.trigger_fcn is not None:
                            env = globals().copy()
                            env.update(locals())
                            method = env.get(effect.trigger_fcn)
                            method(char, effect)
                        if effect.sfx is not None: renpy.play("audio/sfx/{}.mp3".format(effect.sfx), channel='audio')
                if (kwargs.get('is_start_round', False)): effect.duration -= 1
                # if (effect.duration < 1) and (effect.remove_fcn is None): removed_effects.append(index)
                if (effect.duration < 1) and (effect.remove_fcn is None): char.effects[index] = None
        char.effects = [i for i in char.effects if i is not None]
        # if len(removed_effects):
        #     renpy.show_screen("float_msg", x=char.x, y=char.y, text="effects len: {}".format(len(char.effects)), _tag='msg_'+str(char.x)+str(char.y), _transient=True)
        #     renpy.pause()
        #     for i in removed_effects:
        #         renpy.show_screen("float_msg", x=char.x, y=char.y, text="i to delete: {}".format(i), _tag='msg_'+str(char.x)+str(char.y), _transient=True)
        #         renpy.pause()
        #         # if i in char.effects: char.effects.pop(i)
        #         char.effects.pop(i)

    def triggerRemoveEffects(char: charsLib.Char):
        removed_effects = []
        added_effects = []
        for (index, effect) in enumerate(char.effects):
            if effect.duration < 1:
                if effect.remove_fcn is not None:
                    env = globals().copy()
                    env.update(locals())
                    method = env.get(effect.remove_fcn)
                    result = method(char, effect)
                    added_effects = added_effects + result
                    # removed_effects.append(index)
                    char.effects[index] = None
        char.effects = [i for i in char.effects if i is not None]
        # if len(removed_effects):
        #     for i in removed_effects:
        #         char.effects.pop(i)
        if len(added_effects):
            applyEffects(char, added_effects)
            triggerEffects(char, only_stats=True)


    ################# SPECIAL FCN #################
    def overclockRemove(char: charsLib.Char, effect: Effect):
        renpy.pause(1.0)
        combatLib.setArenaIdle()
        char.turns = char.base_turns
        renpy.play("audio/sfx/debuff.mp3", channel='audio')
        renpy.show_screen("hex", position=(char.x, char.y), _tag='an_'+str(char.x)+str(char.y),_transient=True)
        return ['slow']
    def stunApply(char: charsLib.Char, effect: Effect):
        multiplier = 1
        if effect.effect_power > 1: multiplier = 1.5 * (effect.effect_power - 1)
        char.turns -= int(1 * multiplier)
        renpy.show_screen("float_msg", x=char.x, y=char.y, text="STUNNED", _tag='msg_'+str(char.x)+str(char.y), _transient=True)
        if char.turns > 0: renpy.pause(1.0)
    def stunRemove(char: charsLib.Char, effect: Effect):
        char.turns = char.base_turns
        return []
    def killSummon(char: charsLib.Char, effect: Effect):
        char.hp = 0
        return []
    def detransform(char: charsLib.Char, effect: Effect):
        renpy.pause(1.0)
        # Give the original char the proportional hp
        char_to_return = combatLib.arena[char.trans_from]
        hp_percent = (char.hp/char.base_hp) * 100
        char_to_return.hp = int((char_to_return.base_hp/100) * hp_percent)
        char_to_return.damage_done += char.damage_done
        char_to_return.heal_done += char.heal_done
        char_to_return.effects = char.effects.copy()
        for (index, effect) in enumerate(char_to_return.effects.copy()):
            if effect.tag == 'trans':
                del char_to_return.effects[index]
                break
        applyEffects(char_to_return, ['drunk'])
        triggerEffects(char_to_return, only_stats=True)
        renpy.show_screen("char_sprite", _tag=str(char_to_return.x) + str(char_to_return.y), char=char_to_return, _zorder=char_to_return.zorder)
        renpy.show_screen("char_status", _tag="status_"+str(char_to_return.x)+str(char_to_return.y), char=char_to_return)

        # Return original char to the list
        combatLib.arena_tags[combatLib.arena_tags.index(char.tag)] = char.trans_from
        if char.tag in combatLib.allies:
            combatLib.allies[combatLib.allies.index(char.tag)] = char.trans_from
            combatLib.allies_alive[combatLib.allies_alive.index(char.tag)] = char.trans_from
        if char.tag in combatLib.enemies:
            combatLib.enemies[combatLib.enemies.index(char.tag)] = char.trans_from
            combatLib.enemies_alive[combatLib.enemies_alive.index(char.tag)] = char.trans_from
        renpy.play("audio/sfx/debuff.mp3", channel='audio')
        renpy.show_screen("magicHit", position=(char_to_return.x, char_to_return.y), _tag='an_'+str(char_to_return.x)+str(char_to_return.y),_transient=True)
        return []

    ################# SPECIAL SPECIAL FCN #################
    def protectTeammate(char: charsLib.Char, targets):
        char.sprite_state = 'protect'
        return (
            "{} protects {}.".format(char, targets[0]),
            [char]
        )


            
