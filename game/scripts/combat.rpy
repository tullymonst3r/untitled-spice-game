init python:
    import random
    import store.itemslib as itemslib
    import store.combatlib as combatlib
    import store.spellslib as spellslib
    import store.effectsLib as effectsLib

    def checkTeamHealths():
        enemiesHp = 0
        for enemyMember in combatlib.enemies:
            if enemyMember is not None:
                enemiesHp += combatlib.arenaChars[enemyMember].health
                if enemyMember in combatlib.enemies:
                    if combatlib.arenaChars[enemyMember].health < 1:
                        tag = str(combatlib.arenaChars[enemyMember].x) + str(combatlib.arenaChars[enemyMember].y)
                        renpy.pause(0.7)
                        renpy.hide_screen(tag)
                        renpy.hide_screen("status_"+tag)
                        index = combatlib.enemies.index(enemyMember)
                        combatlib.enemies[index] = None
                        index = combatlib.arenaTags.index(enemyMember)
                        combatlib.arenaTags[index] = None
                        index = combatlib.enemiesAlive.index(enemyMember)
                        del combatlib.enemiesAlive[index]
                        renpy.play("audio/sfx/69_Enemy_death_01.mp3", channel='audio')
        alliesHp = 0
        for alliesMember in combatlib.allies:
            if alliesMember is not None:
                alliesHp += combatlib.arenaChars[alliesMember].health
                if alliesMember in combatlib.allies:
                    if combatlib.arenaChars[alliesMember].health < 1:
                        tag = str(combatlib.arenaChars[alliesMember].x) + str(combatlib.arenaChars[alliesMember].y)
                        renpy.pause(0.7)
                        renpy.hide_screen(tag)
                        renpy.hide_screen("status_"+tag)
                        index = combatlib.allies.index(alliesMember)
                        combatlib.allies[index] = None
                        index = combatlib.arenaTags.index(alliesMember)
                        combatlib.arenaTags[index] = None
                        index = combatlib.alliesAlive.index(alliesMember)
                        del combatlib.alliesAlive[index]
                        renpy.play("audio/sfx/69_Enemy_death_01.mp3", channel='audio')
        return (enemiesHp, alliesHp)
    
    def roundManaRecharge(attacker):
        if attacker.baseMana > 0:
            if attacker.mana < attacker.baseMana:
                attacker.mana += 10
            if attacker.mana > attacker.baseMana:
                attacker.mana = attacker.baseMana

label combat(combatants=([],[])):
    window hide  # Hide the window and quick menu while in combat
    $ quick_menu = False

    python:
        # startup battle
        combatlib.wonLastCombat = False
        combatlib.resetChars(combatants[0])
        combatlib.resetChars(combatants[1])
        combatlib.resetArena()

        # set player's allies sprites and total allies's health for lose condition
        alliesHp = 0
        for (i, alliesMember) in enumerate(combatants[0]):
            if alliesMember is not None:
                newTag = alliesMember + str(i)
                combatlib.addCharacterToArena(alliesMember, newTag)
                combatlib.allies.append(newTag)
                combatlib.arenaTags.append(newTag)
                combatlib.arenaChars[newTag].calcTerrasphereStats()
                # TODO: Automate the position of the sprites to allow more than 4
                if i == 0:
                    x = 700
                    y = 700
                    zorder = -4
                elif i == 1:
                    x = 450
                    y = 500
                    zorder = -5
                elif i == 2:
                    x = 450
                    y = 900
                    zorder = -3
                elif i == 3:
                    x = 200
                    y = 700
                    zorder = -4
                else:
                    x = 0
                    y = 0
                    zorder = -6
                combatlib.arenaChars[newTag].x = x
                combatlib.arenaChars[newTag].y = y
                combatlib.arenaChars[newTag].zorder = zorder
                renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=combatlib.arenaChars[newTag], _zorder=zorder)
                renpy.show_screen("charStatus", _tag="status_"+str(x)+str(y), char=combatlib.arenaChars[newTag])
                # cap at 4 members on each team
                if i == 4:
                    break
        combatlib.alliesAlive = combatlib.allies.copy()
        # set enemies' allies sprites and total enemies' health for win condition
        enemiesHp = 0
        for (i, enemyMember) in enumerate(combatants[1]):
            if enemyMember is not None:
                newTag = enemyMember + str(i)
                combatlib.addCharacterToArena(enemyMember, newTag)
                combatlib.enemies.append(newTag)
                combatlib.arenaTags.append(newTag)
                combatlib.arenaChars[newTag].calcTerrasphereStats()
                if i == 0:
                    x = 1300
                    y = 700
                    zorder = -4
                elif i == 1:
                    x = 1500
                    y = 500
                    zorder = -5
                elif i == 2:
                    x = 1500
                    y = 900
                    zorder = -3
                elif i == 3:
                    x = 1800
                    y = 700
                    zorder = -4
                else:
                    x = 0
                    y = 0
                    zorder = -6
                combatlib.arenaChars[newTag].x = x
                combatlib.arenaChars[newTag].y = y
                combatlib.arenaChars[newTag].zorder = zorder
                renpy.show_screen("char_sprite", _tag=str(x) + str(y), char=combatlib.arenaChars[newTag], _zorder=zorder)
                renpy.show_screen("charStatus", _tag="status_"+str(x)+str(y), char=combatlib.arenaChars[newTag])
                # cap at 4 members on each team
                if i == 4:
                    break
        combatlib.enemiesAlive = combatlib.enemies.copy()
        combatlib.arenaTags = combatlib.arenaTags
        combatlib.enemies = combatlib.enemies
        combatlib.allies = combatlib.allies
        defaultEnemies = combatlib.enemies.copy()

    play music "audio/Just Roll on Your Back.mp3"

    label combatLoop:
        $ i = 0
        jump charactersCycle
        label charactersCycle:
            $ renpy.hide_screen("actions_box")
            $ renpy.hide_screen("select_item")
            $ renpy.hide_screen("confirm_escape")
            $ attackerTag = combatlib.arenaTags[i]
            if attackerTag is None:
                # dead char
                $ i += 1
                if i < len(combatlib.arenaTags):
                    jump charactersCycle
                else:
                    jump combatLoop
            $ attacker = combatlib.arenaChars[attackerTag]
            $ effectsLib.triggerRoundEffects(attacker)
            if attacker.health > 0:
                jump characterTurn
            else:
                jump endCharacterTurn         
            label characterTurn:
                show screen current_turn(x=attacker.x, y=attacker.y)
                $ playerLib.selectedGuardian = attackerTag
                $ isAlly = attackerTag in combatlib.allies
                $ isPlayableAlly = (attacker.isPlayable) and (isAlly)
                $ combatlib.reduceCooldown(attackerTag)
                $ roundManaRecharge(attacker)
                $ turns = 0
                if attacker.turns > 0:
                    jump multipleTurnsCycle
                else:
                    jump endCharacterAction

                label multipleTurnsCycle:
                    if i < len(combatlib.arenaTags):
                        if attackerTag != combatlib.arenaTags[i]:
                            # Attacker used transformation ability
                            $ attackerTag = combatlib.arenaTags[i]
                            $ attacker = combatlib.arenaChars[attackerTag]
                    $ attackName = 'undefined'
                    $ targetText = ''
                    $ equipment = None
                    $ attackData = None
                    $ selectionEnded = False
                    jump actionSelection
                    

                    label actionSelection:
                        if isPlayableAlly:
                            call screen actions_box(attacker)
                            $ renpy.hide_screen("actions_box")
                            if _return:
                                # Attack selected
                                $ equipment = _return
                                jump targetSelection
                        else:
                            # TODO: Filter attacks when on cd or mana is not enough
                            python:
                                availableEquipments = []
                                for equipment in attacker.equipment:
                                    if equipment is not None:
                                        availableEquipments.append(equipment)
                            $ equipment = availableEquipments[random.randrange(0, len(availableEquipments))]
                            jump targetSelection
                    label itemSelection:
                        call screen select_item()
                        $ renpy.hide_screen("select_item")
                        if _return:
                            $ equipment = _return
                            jump targetSelection
                    label confirmEscape:
                        call screen confirm_escape()
                    label targetSelection:
                        if equipment is not None:
                            $ attackData = equipment.attackData
                            $ attackName = equipment.name
                        if attackData is not None:
                            $ targets = []
                            $ verb = attackData.verb
                            if attackData.target == 'enemy':
                                if isPlayableAlly:
                                    call screen selection_sprite_enemy
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    if isAlly:
                                        $ targets.append(renpy.random.choice(combatlib.enemiesAlive))
                                    else:
                                        $ targets.append(renpy.random.choice(combatlib.alliesAlive))
                            elif attackData.target == 'enemies':
                                if isPlayableAlly:
                                    call screen selection_sprite_enemies
                                    $ targets = combatlib.enemiesAlive.copy()
                                else:
                                    if isAlly:
                                        $ targets = combatlib.enemiesAlive.copy()
                                    else:
                                        $ targets = combatlib.alliesAlive.copy()
                            elif attackData.target == 'ally':
                                if isPlayableAlly:
                                    call screen selection_sprite_ally
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    if isAlly:
                                        $ targets.append(renpy.random.choice(combatlib.alliesAlive))
                                    else:
                                        $ targets.append(renpy.random.choice(combatlib.enemiesAlive))
                            elif attackData.target == 'allies':
                                if isPlayableAlly:
                                    call screen selection_sprite_allies
                                    $ targets = combatlib.alliesAlive.copy()
                                else:
                                    if isAlly:
                                        $ targets = combatlib.alliesAlive.copy()
                                    else:
                                        $ targets = combatlib.enemiesAlive.copy()
                            elif attackData.target == 'self':
                                if isPlayableAlly:
                                    call screen selection_sprite_self(attacker)
                                    $ targets.append(attackerTag)
                                else:
                                    $ targets.append(attackerTag)
                            elif attackData.target == 'all':
                                if isPlayableAlly:
                                    call screen selection_sprite_all
                                    $ targets = combatlib.arenaTags.copy()
                                else:
                                    $ targets = combatlib.arenaTags.copy()
                            elif attackData.target == 'any':
                                if isPlayableAlly:
                                    call screen selection_sprite_any
                                    if _return:
                                        $ targets.append(_return)
                                else:
                                    $ targets.append(renpy.random.choice(combatlib.arenaTags))
                            jump doAction
                    label doAction:
                        if (len(targets) == 1) and (attackData.target != 'self'):
                            $ targetText = ' on {}'.format(combatlib.arenaChars[targets[0]].name)
                        "[attacker.name] uses [attackName][targetText]."
                        $ combatlib.actionAttack(attacker, targets, equipment) # meaty function
                        jump endCharacterAction
                    label endCharacterAction:
                        $ turns += 1
                        $ lastMultiTurn = True
                        if turns >= attacker.turns:
                            # End of extra turns if applied
                            $ effectsLib.triggerRemoveActions(attacker)
                        else:
                            $ lastMultiTurn = False
                        pause(1.0)
                        $ teamsHealth = checkTeamHealths()
                        if teamsHealth[0] < 1:
                            jump combatWon
                        elif teamsHealth[1] < 1:
                            jump combatLost
                        if (not lastMultiTurn):
                            jump multipleTurnsCycle
                        else:
                            $ i += 1
                            if i < len(combatlib.arenaTags):
                                jump charactersCycle
                            else:
                                jump combatLoop                      
                label endCharacterTurn:
                    pause(1.0)
                    $ teamsHealth = checkTeamHealths()
                    if teamsHealth[0] < 1:
                        jump combatWon
                    elif teamsHealth[1] < 1:
                        jump combatLost
                    $ i += 1
                    if i < len(combatlib.arenaTags):
                        jump charactersCycle
                    else:
                        jump combatLoop   
    label combatLost:
        "You lost!"
        $ combatlib.wonLastCombat = False
        jump combatEnded
    label combatWon:
        "You won!"
        $ combatlib.wonLastCombat = True
        jump combatEnded
    label combatEnded:
        # TODO: Use renpy.get_screen to hide everything
        python:
            renpy.hide_screen('current_turn')
            renpy.hide_screen('charStatus')
            renpy.hide_screen('number_effect')
            renpy.hide_screen('charTooltip')
            renpy.hide_screen('equipmentTooltip')
            if combatlib.wonLastCombat:
                # Loot
                maxGold = 0
                for enemyTag in defaultEnemies:
                    char = combatlib.arenaChars[enemyTag]
                    maxGold += char.gold
                if maxGold > 0:
                    foundGold = random.randrange(0, maxGold + 1)
                    renpy.play("audio/sfx/bought_found_item_gold.mp3", channel='audio')
                    renpy.notify("You found " + str(foundGold) + " gold.")
                    renpy.pause(1.0)
                # XP
                leveledUpChars = []
                for allyTag in combatlib.alliesAlive:
                    char = combatlib.arenaChars[allyTag]
                    if char.isPlayable:
                        totalXp = char.damageDone + char.healDone
                        renpy.show_screen("number_effect", x=char.x, y=char.y, val=totalXp, textColor="#2df300", _tag='xp_'+str(char.x)+str(char.y), _transient=True)
                        renpy.play("audio/sfx/xp_plus.mp3", channel='audio')
                        hasLeveledUp = combatlib.combatChars[char.ogTag].gainXp(totalXp)
                        renpy.pause(1.0)
                        if hasLeveledUp:
                            leveledUpChars.append(allyTag)
                if len(leveledUpChars) > 0:
                    renpy.play("audio/sfx/level_up.mp3", channel='audio')
                    for leveledUpChar in leveledUpChars:
                        char = combatlib.arenaChars[leveledUpChar]
                        renpy.show_screen("msg_effect", x=char.x, y=char.y, text="LEVEL UP", _tag='msg_'+str(char.x)+str(char.y), _transient=True)
                    renpy.pause(1.0)
            if combatlib.hideSpritesAfterBattle:
                for charTag in combatlib.arenaTags:
                    if charTag is not None:
                        # TODO: Copy hp and mp to og chars for gauntlet cases
                        tag = str(combatlib.arenaChars[charTag].x) + str(combatlib.arenaChars[charTag].y)
                        renpy.hide_screen(tag)
                        renpy.hide_screen("status_"+tag)
            combatlib.arenaChars = {}
            combatlib.allies = []
            combatlib.alliesAlive = []
            combatlib.enemies = []
            combatlib.enemiesAlive = []
            combatlib.arenaTags = []
            playerLib.selectedGuardian = 'garlic'
        stop music
        $ quick_menu = True
    
    return
