init python:
    def checkTeamHealths():
        enemies_hp = 0
        for char_tag in combatLib.enemies:
            if char_tag is not None:
                char = combatLib.arena[char_tag]
                enemies_hp += char.hp
                if char.hp < 1:
                    xy_tag = str(char.x) + str(char.y)
                    renpy.pause(0.5)
                    renpy.hide_screen(xy_tag)
                    renpy.hide_screen("status_"+xy_tag)
                    index = combatLib.enemies.index(char_tag)
                    combatLib.enemies[index] = None
                    index = combatLib.arena_tags.index(char_tag)
                    combatLib.arena_tags[index] = None
                    index = combatLib.enemies_alive.index(char_tag)
                    del combatLib.enemies_alive[index]
                    renpy.play("audio/sfx/char_death.mp3", channel='audio')
                    renpy.show_screen("dead_char_sprite", _tag="dead_"+str(char.x) + str(char.y), char=char, _zorder=char.zorder)
        allies_hp = 0
        for char_tag in combatLib.allies:
            if char_tag is not None:
                char = combatLib.arena[char_tag]
                allies_hp += char.hp
                if char.hp < 1:
                    xy_tag = str(char.x) + str(char.y)
                    renpy.pause(0.5)
                    renpy.hide_screen(xy_tag)
                    renpy.hide_screen("status_"+xy_tag)
                    index = combatLib.allies.index(char_tag)
                    combatLib.allies[index] = None
                    index = combatLib.arena_tags.index(char_tag)
                    combatLib.arena_tags[index] = None
                    index = combatLib.allies_alive.index(char_tag)
                    del combatLib.allies_alive[index]
                    renpy.play("audio/sfx/char_death.mp3", channel='audio')
                    renpy.show_screen("dead_char_sprite", _tag="dead_"+str(char.x) + str(char.y), char=char, _zorder=char.zorder)
        return (enemies_hp, allies_hp)
    
    def selectTargets(in_list, random = False):
        targets = []
        for char in list(combatLib.arena.values()):
            if char.tag in in_list: targets.append(char)
        if random:
            return renpy.random.choice(targets)
        return targets

label combat(combatants=([],[])):
    window hide  # Hide the window and quick menu while in combat
    $ quick_menu = False
    stop music fadeout 2.0

    python:
        # startup battle
        won_combat = False
        combatLib.resetArena()

        # set player's allies sprites and total allies's hp for lose condition
        total_char_count = 0
        for (i, char_tag) in enumerate(combatants[0]):
            if char_tag is not None:
                newTag = char_tag + str(total_char_count)
                combatLib.addCharacterToArena(char_tag, newTag, is_playable=True)
                combatLib.allies.append(newTag)
                placing = True
                while placing:
                    if len(combatLib.ally_grid_pos_used) == 16: placing = False # No more space available
                    h = random.randrange(0, 4)
                    w = random.randrange(0, 4)
                    pos_txt = str(h)+str(w)
                    if pos_txt in combatLib.ally_grid_pos_used: continue # Position used
                    combatLib.ally_grid_pos_used.append(pos_txt)
                    x = combatLib.ally_grid[w][h][0]
                    y = combatLib.ally_grid[w][h][1]
                    zorder = h + -1
                    # renpy.show_screen("block", _tag='a'+str(x) + str(y), h=h, w=w, x=x, y=y)
                    placing = False # Char placed

                # TODO: Automate the position of the sprites to allow more than 4
                # if i == 0:
                #     x = 700
                #     y = 700
                #     zorder = -4
                # elif i == 1:
                #     x = 450
                #     y = 500
                #     zorder = -5
                # elif i == 2:
                #     x = 450
                #     y = 900
                #     zorder = -3
                # elif i == 3:
                #     x = 200
                #     y = 700
                #     zorder = -4
                # else:
                #     x = 0
                #     y = 0
                #     zorder = -6
                combatLib.arena[newTag].x = x
                combatLib.arena[newTag].y = y
                combatLib.arena[newTag].zorder = zorder
                renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=combatLib.arena[newTag], _zorder=zorder)
                renpy.show_screen("char_status", _tag="status_"+str(x)+str(y), char=combatLib.arena[newTag], _zorder=zorder)
                total_char_count += 1
                # cap at 4 members on each team
                # if i == 4:
                #     break
        combatLib.allies_alive = combatLib.allies.copy()
        # set enemies' allies sprites and total enemies' hp for win condition
        for (i, char_tag) in enumerate(combatants[1]):
            if char_tag is not None:
                newTag = char_tag + str(total_char_count)
                combatLib.addCharacterToArena(char_tag, newTag)
                combatLib.enemies.append(newTag)
                placing = True
                while placing:
                    if len(combatLib.enemy_grid_pos_used) == 30: placing = False # No more space available
                    h = random.randrange(1, 5)
                    w = random.randrange(0, 6)
                    pos_txt = str(h)+str(w)
                    if pos_txt in combatLib.enemy_grid_pos_used: continue # Position used
                    combatLib.enemy_grid_pos_used.append(pos_txt)
                    x = combatLib.enemy_grid[w][h][0]
                    y = combatLib.enemy_grid[w][h][1]
                    zorder = h + -1
                    # renpy.show_screen("block", _tag='a'+str(x) + str(y), h=h, w=w, x=x, y=y)
                    placing = False # Char placed
                # if i == 0:
                #     x = 1300
                #     y = 700
                #     zorder = -4
                # elif i == 1:
                #     x = 1550
                #     y = 500
                #     zorder = -5
                # elif i == 2:
                #     x = 1550
                #     y = 900
                #     zorder = -3
                # elif i == 3:
                #     x = 1800
                #     y = 700
                #     zorder = -4
                # else:
                #     x = 0
                #     y = 0
                #     zorder = -6
                combatLib.arena[newTag].x = x
                combatLib.arena[newTag].y = y
                combatLib.arena[newTag].zorder = zorder
                renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=combatLib.arena[newTag], _zorder=zorder)
                renpy.show_screen("char_status", _tag="status_"+str(x)+str(y), char=combatLib.arena[newTag], _zorder=zorder)
                total_char_count += 1
                # cap at 4 members on each team
                # if i == 4:
                #     break
        combatLib.enemies_alive = combatLib.enemies.copy()
        combatLib.arena_tags = combatLib.arena_tags
        combatLib.default_arena_tags = combatLib.arena_tags.copy()
        combatLib.enemies = combatLib.enemies
        combatLib.allies = combatLib.allies
        defaultEnemies = combatLib.enemies.copy()

    play music "audio/Just Roll on Your Back.mp3"

    label combatLoop:
        $ i = 0
        stop sound
        jump charactersCycle
        label charactersCycle:
            $ renpy.hide_screen("actions_box")
            $ renpy.hide_screen("select_item")
            $ renpy.hide_screen("confirm_escape")
            $ attacker_tag = combatLib.arena_tags[i]
            if attacker_tag is None:
                # dead char
                $ i += 1
                if i < len(combatLib.arena_tags):
                    jump charactersCycle
                else:
                    jump combatLoop
            $ attacker = combatLib.arena[attacker_tag]
            $ effectsLib.triggerEffects(attacker, effect_activation='passive', is_start_round=True)
            if attacker.hp > 0:
                jump characterTurn
            else:
                jump endCharacterTurn         
            label characterTurn:
                show screen current_turn(x=attacker.x, y=attacker.y)
                $ playerLib.selected_guardian = attacker_tag
                $ is_ally = attacker_tag in combatLib.allies
                $ is_playable_ally = (attacker.is_playable) and (is_ally)
                $ attacker.reduceCooldowns()
                $ attacker.regenRound()
                $ turns = 0
                if attacker.turns > 0:
                    jump multipleTurnsCycle
                else:
                    jump endCharacterAction

                label multipleTurnsCycle:
                    if i < len(combatLib.arena_tags):
                        if attacker_tag != combatLib.arena_tags[i]:
                            # Attacker used transformation ability
                            $ attacker_tag = combatLib.arena_tags[i]
                            $ attacker = combatLib.arena[attacker_tag]
                    $ attack_name = 'undefined'
                    $ target_text = ''
                    $ skill = None
                    $ skill_data = None
                    jump actionSelection
                    

                    label actionSelection:
                        if is_playable_ally:
                            call screen actions_box(attacker)
                            $ renpy.hide_screen("actions_box")
                            if _return:
                                # Attack selected
                                $ skill = _return
                                jump targetSelection
                            else:
                                jump actionSelection
                        else:
                            # TODO: Filter attacks when on cd or mana is not enough
                            python:
                                available_skills = []
                                for skill in attacker.skills:
                                    if skill is not None:
                                        available_skills.append(skill)
                            if len(available_skills) == 0:
                                $ skill = skillsLib.getSkill('recover')
                            else:
                                $ skill = available_skills[random.randrange(0, len(available_skills))]
                            jump targetSelection
                    label itemSelection:
                        call screen select_item()
                        $ renpy.hide_screen("select_item")
                        if _return:
                            $ skill = _return
                            jump targetSelection
                        else:
                            jump itemSelection
                    label confirmEscape:
                        call screen confirm_escape()
                    label targetSelection:
                        if skill is not None:
                            $ skill_data = skill.skill_data
                            $ attack_name = skill.name
                        if skill_data is not None:
                            $ targets = []
                            if skill_data.target == 'enemy':
                                if is_playable_ally:
                                    call screen select_target(combatLib.enemies_alive, 'enemy')
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    if is_ally:
                                        $ targets.append(selectTargets(combatLib.enemies_alive, True))
                                    else:
                                        $ targets.append(selectTargets(combatLib.allies_alive, True))
                            elif skill_data.target == 'enemies':
                                if is_playable_ally:
                                    call screen select_target(combatLib.enemies_alive, 'enemy', True)
                                    $ targets = selectTargets(combatLib.enemies_alive)
                                else:
                                    if is_ally:
                                        $ targets = selectTargets(combatLib.enemies_alive)
                                    else:
                                        $ targets = selectTargets(combatLib.allies_alive)
                            elif skill_data.target == 'ally':
                                if is_playable_ally:
                                    call screen select_target(combatLib.allies_alive, 'ally')
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    if is_ally:
                                        $ targets.append(selectTargets(combatLib.allies_alive, True))
                                    else:
                                        $ targets.append(selectTargets(combatLib.enemies_alive, True))
                            elif skill_data.target == 'allies':
                                if is_playable_ally:
                                    call screen select_target(combatLib.allies_alive, 'ally', True)
                                    $ targets = selectTargets(combatLib.allies_alive)
                                else:
                                    if is_ally:
                                        $ targets = selectTargets(combatLib.allies_alive)
                                    else:
                                        $ targets = selectTargets(combatLib.enemies_alive)
                            elif skill_data.target == 'self':
                                if is_playable_ally:
                                    call screen select_target([attacker_tag], 'ally')
                                    $ targets.append(attacker)
                                else:
                                    $ targets.append(attacker)
                            elif skill_data.target == 'all':
                                if is_playable_ally:
                                    call screen select_target(combatLib.arena_tags, 'any', True)
                                    $ targets = selectTargets(combatLib.arena_tags)
                                else:
                                    $ targets = selectTargets(combatLib.arena_tags)
                            elif skill_data.target == 'any':
                                if is_playable_ally:
                                    call screen select_target(combatLib.arena_tags, 'any')
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    $ targets.append(selectTargets(combatLib.arena_tags, True))
                            jump doAction
                    label doAction:
                        if (len(targets) == 1) and (skill_data.target != 'self'):
                            $ target_text = ' on {}'.format(targets[0].name)
                        "[attacker.name] uses [attack_name][target_text]."

                        # protection and oher teammate effects
                        $ preventive_event = False
                        $ preventive_event_txt = ''
                        if skill_data.target == 'enemy':
                            python:
                                if is_ally:
                                    for enemy_tag in combatLib.enemies_alive:
                                        if enemy_tag != targets[0].tag:
                                            for preventive_effect in combatLib.arena[enemy_tag].teammate_preventive_effects:
                                                if random.randrange(100) < preventive_effect.chance:
                                                    preventive_event = True
                                                    method = getattr(effectsLib, preventive_effect.action_fcn)
                                                    (preventive_event_txt, targets) = method(combatLib.arena[enemy_tag], targets)
                                                    break
                                else:
                                    for ally_tag in combatLib.allies_alive:
                                        if ally_tag != targets[0].tag:
                                            for preventive_effect in combatLib.arena[ally_tag].teammate_preventive_effects:
                                                if random.randrange(100) < preventive_effect.chance:
                                                    preventive_event = True
                                                    method = getattr(effectsLib, preventive_effect.action_fcn)
                                                    (preventive_event_txt, targets) = method(combatLib.arena[ally_tag], targets)
                                                    break
                        if preventive_event:
                            "[preventive_event_txt]"
                            $ combatLib.setArenaIdle()
                        $ combatLib.characterAction(attacker, targets, skill) # meaty function
                        jump endCharacterAction
                    label endCharacterAction:
                        if (skill_data is not None) and (not skill_data.quick_action):
                            $ turns += 1
                        $ last_multi_turn = True
                        if turns >= attacker.turns:
                            $ last_multi_turn = True
                            # End of extra turns if applied
                            $ effectsLib.triggerRemoveEffects(attacker)
                        else:
                            $ last_multi_turn = False
                        pause(1.0)
                        $ combatLib.setArenaIdle()
                        $ teams_health = checkTeamHealths()
                        if teams_health[0] < 1:
                            jump combatWon
                        elif teams_health[1] < 1:
                            jump combatLost
                        if (not last_multi_turn):
                            jump multipleTurnsCycle
                        else:
                            $ i += 1
                            if i < len(combatLib.arena_tags):
                                jump charactersCycle
                            else:
                                jump combatLoop
                label endCharacterTurn:
                    pause(1.0)
                    $ teams_health = checkTeamHealths()
                    if teams_health[0] < 1:
                        jump combatWon
                    elif teams_health[1] < 1:
                        jump combatLost
                    $ i += 1
                    if i < len(combatLib.arena_tags):
                        jump charactersCycle
                    else:
                        jump combatLoop   
    label combatLost:
        "You lost!"
        $ won_combat = False
        jump combatEnded
    label combatWon:
        "You won!"
        $ won_combat = True
        jump combatEnded
    label combatEnded:
        stop music fadeout 2.0
        # TODO: Use renpy.get_screen to hide everything
        python:
            renpy.hide_screen('current_turn')
            # renpy.hide_screen('char_status')
            renpy.hide_screen('float_num')
            renpy.hide_screen('charTooltip')
            renpy.hide_screen('skillTooltip')
            combatLib.ally_grid_pos_used = []
            combatLib.enemy_grid_pos_used = []
            # renpy.hide_screen('dead_char_sprite')
            if won_combat:
                total_xp = 0
                for allyTag in combatLib.allies_alive:
                    char = combatLib.arena[allyTag]
                    if char.is_playable:
                        char_xp = char.damage_done + char.heal_done
                        total_xp += char_xp
                        renpy.show_screen("float_num", x=char.x, y=char.y, val=char_xp, textColor="#2df300", _tag='xp_'+str(char.x)+str(char.y), _transient=True)
                        renpy.play("audio/sfx/xp_plus.mp3", channel='audio')
                        renpy.pause(1.0)
                has_leveled_up = playerLib.gainXp(total_xp)
                if has_leveled_up:
                    renpy.play("audio/sfx/level_up.mp3", channel='audio')
                    garlic_combat = combatLib.arena[combatLib.default_arena_tags[0]]
                    renpy.show_screen("float_msg", x=garlic_combat.x, y=garlic_combat.y, text="LEVEL UP", _tag='msg_'+str(garlic_combat.x)+str(garlic_combat.y), _transient=True)
                    renpy.pause(1.0)
            if combatLib.hide_sprites:
                for char_tag in combatLib.default_arena_tags:
                    if char_tag is not None:
                        tag = str(combatLib.arena[char_tag].x) + str(combatLib.arena[char_tag].y)
                        renpy.hide_screen(tag)
                        renpy.hide_screen("status_"+tag)
                        renpy.hide_screen("dead_"+tag)
            combatLib.resetArena()
            playerLib.selected_guardian = 'garlic'
    
        $ quick_menu = True
    
    return won_combat
