init -8 python in charsLib:
    import store.playerLib as playerLib
    import store.effectsLib as effectsLib
    import store.skillsLib as skillsLib
    import math
    import copy
    import random
    import json

    chars = {}

    def getChar(tag, is_playable=None):
        char_object = None
        if tag in chars:
            char_object = copy.deepcopy(chars[tag])
        else:
            chars_json = open(renpy.config.gamedir + "/db/characters.json", "r")
            loaded_chars = json.load(chars_json)
            char = loaded_chars[tag]
            chars_json.close()
            char_object = copy.deepcopy(Char(tag=tag,**char))
            if ("equipped_skills" in char):
                for (index, skill) in enumerate(char['equipped_skills']):
                    if isinstance(skill, str):
                        # char_object.skills[index] = skillsLib.getSkill(skill)
                        char_object.skills.append(skillsLib.getSkill(skill))
                    else:
                        # char_object.skills[index] = skillsLib.Skill(tag="temp", **skill)
                        char_object.skills.append(skillsLib.Skill(tag="temp", **skill))
            if ('startup_effects' in char): effectsLib.applyEffects(char_object, char['startup_effects'])
            if ('startup_teammate_preventive_effects' in char): effectsLib.applyTeammatePreventiveEffects(char_object, char['startup_teammate_preventive_effects'])
        if is_playable is not None: char_object.is_playable = is_playable
        return char_object

    def addPlayableChar(tag):
        global chars
        chars_json = open(renpy.config.gamedir + "/db/characters.json", "r")
        loaded_chars = json.load(chars_json)
        char = loaded_chars[tag]
        chars_json.close()
        char_object = Char(tag=tag, **char, is_playable=True)
        chars[tag] = char_object
        if ("equipped_skills" in char):
            for (index, skill_tag) in enumerate(char['equipped_skills']):
                char_object.skills.append(skillsLib.getSkill(skill_tag))
                # char_object.skills[index] = skillsLib.getSkill(skill_tag)
        if ('startup_effects' in char): effectsLib.applyEffects(char_object, char['startup_effects'])
        chars[tag] = char_object

    class Char(object):
        x: int = 0
        y: int = 0
        zorder: int = 0
        sprite_state = 'idle'
        damage_done = 0
        heal_done = 0
        summoned_by = None # Tag of the character that summoned it.
        trans_from = None # Tag of the character that transformed into this char.
        def __init__(self, tag: str, name: str, *args, **kwargs):
            self.tag = tag
            self.og_tag = tag
            self.name = name
            self.sprite_name = kwargs.get('sprite_name', 'garlic_chives')
            self.base_hp = kwargs.get('base_hp', 100)
            self.hp = self.base_hp
            self.base_mp = kwargs.get('base_mp', 0)
            self.mp = self.base_mp
            self.base_turns = kwargs.get('base_turns', 1)
            self.turns = self.base_turns

            # Stats
            self.base_defense = kwargs.get('base_defense', 0) # % of damage mitigated (Minimum damage possible) TODO: Too OP at late game. Need rework
            self.defense = self.base_defense
            self.base_mag_defense = kwargs.get('base_mag_defense', 0) # % of damage mitigated (Minimum damage possible) TODO: Too OP at late game. Need rework
            self.mag_defense = self.base_mag_defense
            self.base_reflexes = kwargs.get('base_reflexes', 0) # Increases chances of dodging attacks. Increases chances of hitting melee attacks.
            self.reflexes = self.base_reflexes
            self.base_strength = kwargs.get('base_strength', 0) # Increases damage of all melee attacks
            self.strength = self.base_strength
            self.base_speed = kwargs.get('base_speed', 0) # Increases chances of dodging attacks. Increases chances of hitting melee attacks.
            self.speed = self.base_speed
            self.base_accuracy = kwargs.get('base_accuracy', 0) # Chances of hitting range and magic attacks
            self.accuracy = self.base_accuracy
            self.base_finesse = kwargs.get('base_finesse', 0) # Chances of crit damage in non magic attacks
            self.finesse = self.base_finesse
            
            self.is_playable = kwargs.get('is_playable', False)

            self.teammate_preventive_effects = kwargs.get('teammate_preventive_effects', [])
            self.preventive_effects = kwargs.get('preventive_effects', [])
            self.effects = kwargs.get('effects', [])
            
            self.skills = kwargs.get('skills', [])
            
            self.loot = kwargs.get('loot', {})
            # self.gold = kwargs.get('gold', 0)
        def __str__(self):
            return self.name
        def regenRound(self):
            # TODO: Show flat_num here?
            if self.base_mp > 0:
                self.mp += 10
                if self.mp > self.base_mp: self.mp = self.base_mp
        def reduceCooldowns(self, amount = 1):
            for skill in self.skills:
                if (skill is not None) and (skill.cd > 0): skill.cd -= amount
        def mpAlter(self, mp):
            if self.base_mp > 0:
                if mp > 0:
                    missing_mp = self.base_mp - self.mp
                    added_mp = mp if mp < missing_mp else missing_mp
                    self.mp += added_mp
                    renpy.show_screen("float_num", x=self.x, y=self.y, val=added_mp, textColor="#3bd5ff", _tag='man_'+str(self.x)+str(self.y), _transient=True)
                elif mp < 0:
                    abs_mp = abs(mp)
                    reduced_mp = abs_mp if abs_mp < self.mp else self.mp
                    self.mp -= reduced_mp
                    renpy.show_screen("float_num", x=self.x, y=self.y, val=reduced_mp, textColor="#803bff", _tag='men_'+str(self.x)+str(self.y), _transient=True)
        def heal(self, heal):
            remaining_heal = heal
            real_heal = 0
            missing_hp = self.base_hp - self.hp
            if missing_hp >= remaining_heal:
                self.hp += remaining_heal
                real_heal += remaining_heal
                renpy.show_screen("float_num", x=self.x, y=self.y, val=real_heal, textColor="#1dff25", _tag='heal_'+str(self.x)+str(self.y), _transient=True)
                return real_heal
            else:
                real_heal += missing_hp
                self.hp = self.base_hp
                renpy.show_screen("float_num", x=self.x, y=self.y, val=real_heal, textColor="#1dff25", _tag='heal_'+str(self.x)+str(self.y), _transient=True)
                return real_heal
        def hurt(self, damage, is_magic_attack = False, ignore_defense = False):
            remaining_damage = damage
            real_damage = 0
            blocked = False
            # TODO: Should negative defense increase the damage?
            if (not ignore_defense):
                if (not is_magic_attack) and (self.defense > 0):
                    # reduced_damage = random.randrange(0, int(self.base_hp * (self.defense / 100)))
                    reduced_damage = random.randrange(0, int(remaining_damage - (remaining_damage * (self.defense / 100))))
                    remaining_damage -= reduced_damage
                    if remaining_damage < 0:
                        remaining_damage = 0
                elif (is_magic_attack) and (self.mag_defense > 0):
                    # reduced_damage = random.randrange(0, int(self.base_hp * (self.mag_defense / 100)))
                    reduced_damage = random.randrange(0, int(remaining_damage - (remaining_damage * (self.mag_defense / 100))))
                    remaining_damage -= reduced_damage
                    if remaining_damage < 0:
                        remaining_damage = 0
            if remaining_damage > 0:
                if self.hp > 0:
                    if self.hp > remaining_damage:
                        self.hp -= remaining_damage
                        real_damage += remaining_damage
                        renpy.show_screen("float_num", x=self.x, y=self.y, val=real_damage, textColor="#ff1d1d", _tag='dam_'+str(self.x)+str(self.y), _transient=True)
                        return (real_damage, blocked)
                    else:
                        real_damage += self.hp
                        self.hp = 0 
                        renpy.show_screen("float_num", x=self.x, y=self.y, val=real_damage, textColor="#ff1d1d", _tag='dam_'+str(self.x)+str(self.y), _transient=True)
            else:
                renpy.show_screen("float_msg", x=self.x, y=self.y, text="BLOCKED", _tag='msg_'+str(self.x)+str(self.y), _transient=True)
                blocked = True
                if real_damage > 0:
                    renpy.show_screen("float_num", x=self.x, y=self.y, val=real_damage, textColor="#ff1d1d", _tag='dam_'+str(self.x)+str(self.y), _transient=True)
            return (real_damage, blocked)

    def resetStats(char: Char):
        char.turns = char.base_turns
        char.defense = char.base_defense
        char.mag_defense = char.base_mag_defense
        char.reflexes = char.base_reflexes
        char.speed = char.base_speed
        char.strength = char.base_strength
        char.accuracy = char.base_accuracy
        char.finesse = char.base_finesse
    

