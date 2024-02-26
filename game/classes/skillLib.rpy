init -8 python in skillsLib:
    import copy
    import json
    _constant = True

    def getSkill(tag):
        skills_json = open(renpy.config.gamedir + "/classes/skills.json", "r")
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

            self.active_effects = kwargs.get('active_effects', []) # effects applied to target on use
            self.vfx = kwargs.get('vfx', None) # Animation played on the target on use
            self.sfx = kwargs.get('sfx', '22_Slash_04.mp3') # Sound effect played on use
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
    
