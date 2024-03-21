init -8 python in skillsLib:
    import store.charsLib as charsLib
    import store.effectsLib as effectsLib
    import store.combatLib as combatLib
    import copy
    import json
    import random
    _constant = True

    def getSkill(tag):
        skills_json = open(renpy.config.gamedir + "/db/skills.json", "r")
        loaded_skills = json.load(skills_json)
        skill = loaded_skills[tag]
        skills_json.close()
        return copy.deepcopy(Skill(tag=tag, **skill))

    class SkillData(object):
        def __init__(self, *args, **kwargs):
            self.target = kwargs.get('target', 'enemy') # enemy | enemies | ally | allies | self | all | any
            self.skill_type = kwargs.get('skill_type', 'melee') # melee | range | special
            self.magic_type = kwargs.get('magic_type', None) # None | new | old 

            self.hits = kwargs.get('hits', 1) # number of hits per skill
            self.base_cd = kwargs.get('base_cd', 0) # Cooldown applied after use
            self.mp_cost = kwargs.get('mp_cost', 0) # MP required to use skill

            self.damage = kwargs.get('damage', 0) # Damage modifier. Ignores negatives
            self.heal = kwargs.get('heal', 0) # Heal modifier. Negatives are ignored.
            self.mp = kwargs.get('mp', 0) # MP modifier.

            self.speed = kwargs.get('speed', 0)
            self.accuracy = kwargs.get('accuracy', 0)
            self.finesse = kwargs.get('finesse', 0)

            self.guaranteed_hit = kwargs.get('guaranteed_hit', False)
            self.ignore_crits = kwargs.get('ignore_crits', False)
            self.ignore_defenses = kwargs.get('ignore_defenses', False)
            self.low_chance = kwargs.get('low_chance', False) # Whether the initial chance of hit is 0 or 100
            self.quick_action = kwargs.get('quick_action', False) # Whether the initial chance of hit is 0 or 100

            self.preventive_effects = kwargs.get('preventive_effects', []) # effects applied to target on use
            self.active_effects = kwargs.get('active_effects', []) # effects applied to target on use
            self.vfx = kwargs.get('vfx', None) # Animation played on the target on use
            self.sfx = kwargs.get('sfx', 'slash') # Sound effect played on use
            self.special_action = kwargs.get('special_action', None) # Name of function called when effect activates. (str)
            self.special_val = kwargs.get('special_val', None) # Value passed to the special action function. (str)
        def __str__(self):
            return self.target + "|" + self.skill_type
    class Skill(object):
        def __init__(self, tag, name, *args, **kwargs):
            self.tag = tag
            self.name = name # Displayed Name
            self.description = kwargs.get('description', '')
            self.icon_name = kwargs.get('icon_name', 'fight_0')
            self.cd = kwargs.get('cd', 0) # Cooldown
            self.sp_price = kwargs.get('sp_price', 0) # Skill points required to unlock skill
            if ('skill_data' in kwargs):
                self.skill_data = SkillData(**kwargs.get('skill_data'))
            else:
                self.skill_data = SkillData()
    
    def triggerStatEffects(attacker: charsLib.Char, *args):
        effectsLib.triggerEffects(target, only_instant=True)
    
    def summonEntity(attacker: charsLib.Char, summon_tag):
        summoned_char = charsLib.getChar(summon_tag)
        # Add summon to arena
        summoned_char.tag = summon_tag + str(len(combatLib.arena_tags))
        effectsLib.applyEffects(summoned_char, ['summon'])

        # Insert summon into combat after summoner's turn
        combatLib.arena_tags.insert((combatLib.arena_tags.index(attacker.tag)) + 1, summoned_char.tag)
        x = attacker.x
        y = attacker.y
        zorder = attacker.zorder - 1
        if attacker.tag in combatLib.allies:
            combatLib.allies.insert((combatLib.allies.index(attacker.tag)) + 1, summoned_char.tag)
            combatLib.allies_alive.insert((combatLib.allies_alive.index(attacker.tag)) + 1, summoned_char.tag)
            x += 150
            y -= 150
        elif attacker.tag in combatLib.enemies:
            combatLib.enemies.insert((combatLib.enemies.index(attacker.tag)) + 1, summoned_char.tag)
            combatLib.enemies_alive.insert((combatLib.enemies_alive.index(attacker.tag)) + 1, summoned_char.tag)
            x -= 150
            y -= 150
        summoned_char.x = x
        summoned_char.y = y
        summoned_char.zorder = zorder
        renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=summoned_char, _zorder=zorder)
        renpy.show_screen("char_status", _tag="status_"+str(x)+str(y), char=summoned_char)
        combatLib.arena[summoned_char.tag] = summoned_char
    
    def transformTo(attacker: charsLib.Char, transform_tag):
        trans_char=charsLib.getChar(transform_tag)

        trans_char.tag=transform_tag + str(len(combatLib.arena_tags))
        trans_char.trans_from=attacker.tag
        trans_char.name="{} ({})".format(attacker.name, trans_char.name)
        trans_char.base_turns=attacker.base_turns
        trans_char.turns=attacker.turns
        trans_char.is_playable=attacker.is_playable
        trans_char.x=attacker.x
        trans_char.y=attacker.y
        trans_char.zorder=attacker.zorder
        trans_char.effects = attacker.effects.copy()
        effectsLib.applyEffects(trans_char, ['trans'])
        attacker_hp_percent = (attacker.hp/attacker.base_hp) * 100
        trans_char.hp = int((trans_char.base_hp/100) * attacker_hp_percent)
        effectsLib.triggerEffects(trans_char, only_instant=True)

        combatLib.arena[trans_char.tag] = trans_char
        renpy.show_screen("char_sprite", _tag=str(trans_char.x) + str(trans_char.y), char=trans_char, _zorder=trans_char.zorder)
        renpy.show_screen("char_status", _tag="status_"+str(trans_char.x)+str(trans_char.y), char=trans_char)

        # Insert transform char into the attacker's turn
        combatLib.arena_tags[combatLib.arena_tags.index(attacker.tag)] = trans_char.tag
        if attacker.tag in combatLib.allies:
            combatLib.allies[combatLib.allies.index(attacker.tag)] = trans_char.tag
            combatLib.allies_alive[combatLib.allies_alive.index(attacker.tag)] = trans_char.tag
        if attacker.tag in combatLib.enemies:
            combatLib.enemies[combatLib.enemies.index(attacker.tag)] = trans_char.tag
            combatLib.enemies_alive[combatLib.enemies_alive.index(attacker.tag)] = trans_char.tag

    
