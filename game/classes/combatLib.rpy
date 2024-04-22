init -7 python in combatLib: 
    import math
    import copy
    import random
    from typing import List
    import store.charsLib as charsLib
    import store.spellslib as spellslib
    import store.effectsLib as effectsLib
    import store.playerLib as playerLib
    import store.skillsLib as skillsLib

    # GLOBALS CONSTANTS
    crit_multiplier = 2 # percentage each finesse point is equals to
    reflex_multiplier = 1 # percentage each reflex point is equals to
    speed_multiplier = 1.5 # percentage each speed point is equals to
    accu_multiplier = 2 # percentage each accuracy point is equals to
    range_crit_multiplier = 0.5 # percentage each accuracy point is equals to

    ally_grid_pos_used = []
    # ally_grid = [
    #     [(240,270),(240,450),(240,630),(240,810)],
    #     [(400,270),(400,450),(400,630),(400,810)],
    #     [(560,270),(560,450),(560,630),(560,810)],
    #     [(720,270),(720,450),(720,630),(720,810)],
    # ]
    ally_grid = [
        [(240,360),(240,540),(240,720),(240,900)],
        [(400,360),(400,540),(400,720),(400,900)],
        [(560,360),(560,540),(560,720),(560,900)],
        [(720,360),(720,540),(720,720),(720,900)],
    ]
    enemy_grid_pos_used = []
    enemy_grid = [
        [(1040,180),(1040,360),(1040,540),(1040,720),(1040,900)],
        [(1200,180),(1200,360),(1200,540),(1200,720),(1200,900)],
        [(1360,180),(1360,360),(1360,540),(1360,720),(1360,900)],
        [(1520,180),(1520,360),(1520,540),(1520,720),(1520,900)],
        [(1680,180),(1680,360),(1680,540),(1680,720),(1680,900)],
        [(1840,180),(1840,360),(1840,540),(1840,720),(1840,900)]
    ]
    # enemy_grid = [
    #     [(1040,90),(1040,270),(1040,450),(1040,630),(1040,810)],
    #     [(1200,90),(1200,270),(1200,450),(1200,630),(1200,810)],
    #     [(1360,90),(1360,270),(1360,450),(1360,630),(1360,810)],
    #     [(1520,90),(1520,270),(1520,450),(1520,630),(1520,810)],
    #     [(1680,90),(1680,270),(1680,450),(1680,630),(1680,810)],
    #     [(1840,90),(1840,270),(1840,450),(1840,630),(1840,810)]
    # ]

    hide_sprites = True
    arena = {} # Dict of characters in combat (copies)
    arena_tags = [] # tags of chars in combat (order of turns)
    default_arena_tags = [] # tags of chars in combat (order of turns)
    allies = []
    allies_alive = []
    enemies = []
    enemies_alive = []

    def resetArena():
        global arena, arena_tags, allies, allies_alive, enemies, enemies_alive
        arena = {}
        arena_tags = []
        allies = []
        allies_alive = []
        enemies = []
        enemies_alive = []
    def addCharacterToArena(tag, new_tag, is_playable=False):
        global arena, arena_tags
        char = charsLib.getChar(tag, is_playable)
        char.tag = new_tag
        arena[new_tag] = char
        arena_tags.append(new_tag)
        arena = arena
        arena_tags = arena_tags
    def setArenaIdle():
        for char in list(arena.values()): char.sprite_state = 'idle'

    def characterAction(attacker: charsLib.Char, targets: List[charsLib.Char], skill):
        skill_data = getattr(skill, 'skill_data')

        attacker.sprite_state = 'attack'
        # renpy.pause(0.3)

        skillAction(attacker, targets, skill_data)
        
        if skill_data.mp_cost > 0: attacker.mp -= skill_data.mp_cost
        if skill.__class__.__name__ == 'Skill':
            if skill.skill_data.base_cd > 0: skill.cd = skill.skill_data.base_cd
        # if skill.__class__.__name__ == 'Item':
            # TODO: Reduce item stock
            # playerLib.items_inventory[equipment.tag] -= 1
    
    def skillAction(attacker: charsLib.Char, targets: List[charsLib.Char], skill_data: skillsLib.SkillData):
        total_damage = 0
        total_heal = 0
        max_damage = skill_data.damage
        crit_chance = 0
        guaranteed_hit = (skill_data.guaranteed_hit) or (skill_data.skill_type == 'special')
        if (max_damage > 0) or (skill_data.skill_type == 'melee'):
            if skill_data.skill_type == 'melee': max_damage += attacker.strength
            if max_damage < 0: max_damage = 1 # In case of negative strength
            if not skill_data.ignore_crits:
                crit_chance = int((skill_data.finesse + attacker.finesse) * crit_multiplier)
                if skill_data.skill_type == 'range':
                    crit_chance += int((skill_data.accuracy + attacker.accuracy) * range_crit_multiplier) # TODO: Balance this value
        if skill_data.vfx is not None:
            # TODO: Maybe differenciate multiattack vfx from single target vfx position?
            renpy.show_screen(skill_data.vfx, position=(targets[0].x, targets[0].y), _tag='vfx_'+str(targets[0].x)+str(targets[0].y),_transient=True)
        for i in range(skill_data.hits):
            for target in targets:
                hit_chances = 100
                if not guaranteed_hit:
                    if skill_data.low_chance: hit_chances = 0
                    hit_chances -= int(target.reflexes * reflex_multiplier)
                    if skill_data.skill_type == 'melee':
                        hit_chances += int((skill_data.speed + attacker.speed) * speed_multiplier)
                        hit_chances -= int((target.speed) * speed_multiplier)
                    if skill_data.skill_type == 'range': hit_chances += int((skill_data.accuracy + attacker.accuracy) * accu_multiplier)
                    if hit_chances > 100: hit_chances = 100
                hit_chances = random.randrange(hit_chances, 101)

                # if len(target.preventive_effects):
                #     for effect in target.preventive_effects:
                #         if random.randrange(100) < special_effect.chance:
                #             method = effectsLib.get(special_effect.action_fcn)
                #             hit_chances  = method(hit_chances)

                (damage_done, heal_done) = attack(target, skill_data, hit_chances, max_damage, crit_chance, i == skill_data.hits - 1)
                total_damage += damage_done
                total_heal += heal_done
            if i < (skill_data.hits - 1):
                renpy.pause(0.3)
                for target in targets: target.sprite_state = 'idle'
                renpy.pause(0.1)
        if skill_data.special_action is not None:
            method = getattr(skillsLib, skill_data.special_action)
            method(attacker, skill_data.special_val)
        attacker.damage_done += total_damage
        attacker.heal_done += total_heal
    
    def attack(target, skill_data: skillsLib.SkillData, hit_chances, max_damage, crit_chance, last_hit = True):
        is_crit = False
        blocked = False
        damage_done = 0
        heal_done = 0
        if random.randrange(100) < hit_chances:
            # Succesfull hit
            if max_damage > 0:
                target.sprite_state = 'hurt'
                is_magic_attack = skill_data.magic_type == 'new' or skill_data.magic_type == 'old'
                damage_result = damageTarget(target, max_damage, crit_chance, is_magic_attack, skill_data.ignore_defenses)
                blocked = damage_result[2]
                damage_done = damage_result[1]
                is_crit = damage_result[0]

            if skill_data.mp != 0: target.mpAlter(skill_data.mp)
            if skill_data.heal > 0: heal_done = target.heal(skill_data.heal)

            if last_hit:
                if len(skill_data.active_effects):
                    effectsLib.applyEffects(target, skill_data.active_effects)
                    effectsLib.triggerEffects(target, only_instant=True)
                if len(skill_data.preventive_effects):
                    effectsLib.applyTeammatePreventiveEffects(target, skill_data.preventive_effects)
            
            if blocked:
                renpy.play("audio/sfx/block.mp3", channel='audio')
            else:
                renpy.play("audio/sfx/{}.mp3".format(skill_data.sfx), channel='audio')
            
            if not is_crit:
                # renpy.show_screen('hitmark_vfx', x=target.x, y=target.y, _tag='an_'+str(target.x)+str(target.y), _transient=True)
                renpy.show_screen("impact", position=(target.x, target.y), _tag='an_'+str(target.x)+str(target.y),_transient=True)
            else:
                # Crit fx
                # renpy.show_screen('hitmark_vfx', x=target.x, y=target.y, crit=True, _tag='an_'+str(target.x)+str(target.y), _transient=True)
                renpy.show_screen("crit", position=(target.x, target.y), _tag='an_'+str(target.x)+str(target.y),_transient=True)
        else:
            renpy.show_screen("float_msg", x=target.x, y=target.y, text="MISS", _tag='msg_'+str(target.x)+str(target.y), _transient=True)
            renpy.play("audio/sfx/miss.mp3", channel='audio')
            renpy.show_screen("missedHit", position=(target.x, target.y), _tag='an_'+str(target.x)+str(target.y),_transient=True)
            # renpy.show_screen('miss_vfx', x=target.x, y=target.y, tag='an_'+str(target.x)+str(target.y), _transient=True)
        return (damage_done, heal_done)
    
    def damageTarget(target, max_damage, crit_chance = 0, is_magic_attack = False, ignore_defenses=False):
        is_crit = False
        real_damage = 0
        blocked = False
        if random.randrange(100) < crit_chance:
            # crit hit. doubles the damage
            max_damage = max_damage * 2
            is_crit = True
        hurt_result = target.hurt(max_damage, is_magic_attack, ignore_defenses) # TODO: Add ignore defenses option
        real_damage = hurt_result[0]
        blocked = hurt_result[1]
        return (is_crit, real_damage, blocked)

        