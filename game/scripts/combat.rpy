init python:
    import store.itemslib as itemslib
    import store.combatlib as combatlib
    import store.spellslib as spellslib

label combat(combatants=([],[])):
    window hide  # Hide the window and quick menu while in combat
    $ quick_menu = False

    python:
        # startup battle
        allies = combatants[0]
        enemies = combatants[1]
        combatlib.resetChars(allies)
        combatlib.resetChars(enemies)

        # set player's allies sprites and total allies's health for lose condition
        alliesHp = 0
        enemiesHp = 0
        zorder = 50
        i = 0
        x = 0
        y = 0
        for alliesMember in allies:
            alliesHp += combatlib.combatChars[alliesMember].health
            # TODO: Automate the position of the sprites to allow more than 4
            if i == 0:
                x = 0.35
                y = 0.7
            elif i == 1:
                x = 0.2
                y = 0.5
            elif i == 2:
                x = 0.2
                y = 0.9
            elif i == 3:
                x = 0.1
                y = 0.7
            else:
                x = 0.0
                y = 0.0
            combatlib.combatChars[alliesMember].x = x
            combatlib.combatChars[alliesMember].y = y
            renpy.show_screen("char_sprite", _tag="p" + str(i), char=combatlib.combatChars[alliesMember], x=x, y=y, _zorder=zorder)
            i += 1
            zorder -= 1
            # cap at 4 members on each team
            if i == 4:
                break
        # set enemies' allies sprites and total enemies' health for win condition
        enemiesHp = 0
        i = 0
        x = 0
        y = 0
        for enemyMember in enemies:
            enemiesHp += combatlib.combatChars[enemyMember].health
            if i == 0:
                x = 0.65
                y = 0.7
            elif i == 1:
                x = 0.75
                y = 0.5
            elif i == 2:
                x = 0.75
                y = 0.9
            elif i == 3:
                x = 0.85
                y = 0.7
            else:
                x = 0.0
                y = 0.0
            combatlib.combatChars[enemyMember].x = x
            combatlib.combatChars[enemyMember].y = y
            renpy.show_screen("char_sprite", _tag="e" + str(i), char=combatlib.combatChars[enemyMember], x=x, y=y, _zorder=zorder)
            i += 1
            zorder -= 1
            # cap at 4 members on each team
            if i == 4:
                break
        battleContinues = True
        victory = False

    screen combat_header:
        zorder 99
        frame:
            xsize 1920 ysize 250
            grid 2 1:
                fixed:
                    vbox:
                        align (0, 0)
                        text "Garlic's Party"
                        grid 2 2:
                            for alliesMember in allies:
                                frame:
                                    xsize 400 ysize 100
                                    text "{}".format(combatlib.combatChars[alliesMember].name) style "label"
                                    text "Health: {}".format(combatlib.combatChars[alliesMember].health) align (0, 0.5) style "sublabel"
                                    text "Mana: {}".format(combatlib.combatChars[alliesMember].mana) align (0, 0.9)  style "sublabel"
                    vbox:
                        align (0.999, 0)
                        text "Enemies"
                        grid 2 2:
                            for enemyMember in enemies:
                                frame:
                                    xsize 400 ysize 100
                                    text "{}".format(combatlib.combatChars[enemyMember].name) style "label"
                                    text "Health: {}".format(combatlib.combatChars[enemyMember].health) align (0, 0.5) style "sublabel"
    style label:
        size 25
        color "#ffffff"                        
    style sublabel:
        size 20
        color "#ffffff"                        
    
    show screen combat_header

    screen char_sprite(char, x, y):
        vbox:
            align (x, y)
            fixed:
                xsize 1 ysize 1
                add "{}".format(char.spriteName) anchor (0.5, 0.99)
                # frame:
                #     xsize 400 ysize 100 anchor (0.5, 0)
                #     text "{}".format(char.name) style "label"
                #     text "Health: {}".format(char.health) align (0, 0.5) style "sublabel"
                #     text "Mana: {}".format(char.mana) align (0, 0.9) style "sublabel"

    screen selection_sprite_enemies:
        zorder 99
        for enemyMember in enemies:
            vbox:
                align (combatlib.combatChars[enemyMember].x, combatlib.combatChars[enemyMember].y)
                fixed:
                    xsize 1 ysize 1
                    imagebutton:
                        anchor (0.5, 0.99)
                        idle "sprite_target_idle"
                        hover "sprite_target_hover_enemy"
                        action Return(enemyMember)

    screen actions_box(char):
        frame:
            xpadding 30
            ypadding 30
            xalign 0.5 yalign 0.99
            xsize 1000 ysize 200
            grid 2 2:
                align (0.5, 0.5)
                xsize 970 ysize 100
                yspacing 10 xspacing 25
                frame:
                    xsize 250 ysize 75
                    button:
                        text "Use fists" style "sublabel"
                        action [Hide("actions_box"), Return((1, 'Fists'))]
                        style "custom_btn"
                if char.hand is not None:
                    frame:
                        xsize 250 ysize 75
                        button:
                            text "Use {}".format(itemslib.items[char.hand].name) align (.18, .83) style "sublabel"
                            action [Hide("actions_box"), Return((2, itemslib.items[char.hand].name))]
                            style "custom_btn"
                if char.spells[0] is not None:
                    frame:
                        xsize 250 ysize 75
                        button:
                            if char.spells[0]['cd'] > 0:
                                text "CD: {}".format(char.spells[0]['cd']) align (.18, .83) style "sublabel"
                            elif char.mana < spellslib.spells[char.spells[0]['tag']].cost:
                                text "Not enough mana".format(char.spells[0]['cd']) align (.18, .83) style "sublabel"
                            elif spellslib.spells[char.spells[0]['tag']].magicType == 'new' and (char.hand is None or itemslib.items[char.hand].weaponData['type'] != 'magic'):
                                text "Need Terrasphere".format(char.spells[0]['cd']) align (.18, .83) style "sublabel"
                            elif char.hand is None or itemslib.items[char.hand].weaponData['type'] == 'magic':
                                text "Cast {} ({})".format(spellslib.spells[char.spells[0]['tag']].name, spellslib.spells[char.spells[0]['tag']].cost - itemslib.items[char.hand].weaponData['mana'] if spellslib.spells[char.spells[0]['tag']].cost - itemslib.items[char.hand].weaponData['mana'] > 0 else 0) style "sublabel"
                                action [Hide("actions_box"), Return((3, spellslib.spells[char.spells[0]['tag']].name, 0))]
                            else:
                                text "Cast {} ({})".format(spellslib.spells[char.spells[0]['tag']].name, spellslib.spells[char.spells[0]['tag']].cost) style "sublabel"
                                action [Hide("actions_box"), Return((3, spellslib.spells[char.spells[0]['tag']].name, 0))]
                            style "custom_btn"
                if char.spells[1] is not None:
                    frame:
                        xsize 250 ysize 75
                        button:
                            if char.spells[1]['cd'] > 0:
                                text "CD: {}".format(char.spells[1]['cd']) align (.18, .83) style "sublabel"
                            elif char.mana < spellslib.spells[char.spells[1]['tag']].cost:
                                text "Not enough mana".format(char.spells[1]['cd']) align (.18, .83) style "sublabel"
                            elif spellslib.spells[char.spells[1]['tag']].magicType == 'new' and (char.hand is None or itemslib.items[char.hand].weaponData['type'] != 'magic'):
                                text "Need Terrasphere".format(char.spells[1]['cd']) align (.18, .83) style "sublabel"
                            elif char.hand is None or itemslib.items[char.hand].weaponData['type'] == 'magic':
                                text "Cast {} ({})".format(spellslib.spells[char.spells[1]['tag']].name, spellslib.spells[char.spells[1]['tag']].cost - itemslib.items[char.hand].weaponData['mana'] if spellslib.spells[char.spells[1]['tag']].cost - itemslib.items[char.hand].weaponData['mana'] > 0 else 0) style "sublabel"
                                action [Hide("actions_box"), Return((3, spellslib.spells[char.spells[1]['tag']].name, 1))]
                            else:
                                text "Cast {} ({})".format(spellslib.spells[char.spells[1]['tag']].name, spellslib.spells[char.spells[1]['tag']].cost) style "sublabel"
                                action [Hide("actions_box"), Return((3, spellslib.spells[char.spells[1]['tag']].name, 1))]
                            style "custom_btn"

    while battleContinues:
        # Battle loop
        # Player's party turn
        $ p = 0
        while p < len(allies):
            $ attackerTag = allies[p]
            $ attacker = combatlib.combatChars[attackerTag]

            # Reduces cooldowns and recharges mana per round
            $ combatlib.reduceCooldown(attackerTag)
            if attacker.mana < attacker.baseMana:
                $ attacker.mana += 10
            if attacker.mana > attacker.baseMana:
                $ attacker.mana = attacker.baseMana

            # Show action buttons
            call screen actions_box(attacker)
            $ choice = _return
            $ renpy.hide_screen("actions_box")

            # Check if attack is multiple or single
            if (choice[0] == 3) and (spellslib.spells[attacker.spells[choice[2]]['tag']].is_multiattack):
                # Multi attack to enemies
                "[attacker.name] uses [choice[1]]."
                $ result = combatlib.castMultiSpell(attackerTag, enemies, choice[2])
                "It hit for [result[1]] total damage!"
                python:
                    for enemyMember in enemies:
                        if combatlib.combatChars[enemyMember].health < 1:
                            index = enemies.index(enemyMember)
                            tag = "e" + str(index)
                            renpy.hide_screen(tag)
                            del enemies[index]
                $ enemiesHp -= result[1]
            else:
                call screen selection_sprite_enemies
                $ selection = _return
                $ target = combatlib.combatChars[selection]
                "[attacker.name] uses [choice[1]] on [target.name]."
                if choice[0] == 2:
                    $ result = combatlib.weaponAttack(attackerTag, selection)
                elif choice[0] == 3:
                    $ result = combatlib.castSpell(attackerTag, selection, choice[2])
                else:
                    $ result = combatlib.attackFists(attackerTag, selection)
                if result[0] == 0:
                    "It missed for [result[1]] damage!"
                if result[0] == 1:
                    "It hit for [result[1]] damage!"
                if result[0] == 2:
                    "Critical hit for [result[1]] damage!"
                if target.health < 1:
                    # Enemy was killed
                    $ index = enemies.index(selection)
                    $ tag = "e" + str(index)
                    $ renpy.hide_screen(tag)
                    $ del enemies[index]
                $ enemiesHp -= result[1]
                $ renpy.hide_screen("selection_sprite")
            $ p += 1
        if enemiesHp < 1:
            # TODO: Player can win without killing everyone. enemiesHp is discounting total damage instead of actual damage dealt to enemies (ex. 100 attack on a 10hp enemy = 100 damage done whis is wrong)
            $ win = True
            "You won!"
            $ battleContinues = False
        else:
            # Enemie's party turn
            $ e = 0
            while e < len(enemies):
                $ attackerTag = enemies[e]
                $ attacker = combatlib.combatChars[attackerTag]
                $ enemyChoice = random.randrange(0, 2)
                $ targetTag = renpy.random.choice(allies)
                $ target = combatlib.combatChars[targetTag]
                if enemyChoice == 1:
                    if attacker.hand is not None:
                        $ weapon = itemslib.items[attacker.hand]
                        "[attacker.name] uses [weapon.name] on [target.name]."
                        $ result = combatlib.weaponAttack(attackerTag, targetTag)
                    else:
                        "[attacker.name] uses fists on [target.name]."
                        $ result = combatlib.attackFists(attackerTag, targetTag)
                else:
                    "[attacker.name] uses fists on [target.name]."
                    $ result = combatlib.attackFists(attackerTag, targetTag)
                if result[0] == 0:
                    "It missed for [result[1]] damage!"
                if result[0] == 1:
                    "It hit for [result[1]] damage!"
                if result[0] == 2:
                    "Critical hit for [result[1]] damage!"
                if target.health < 1:
                    # Enemy was killed
                    $ index = allies.index(targetTag)
                    $ tag = "p" + str(index)
                    $ renpy.hide_screen(tag)
                    $ del allies[index]
                $ alliesHp -= result[1]
                $ e += 1
            if alliesHp < 1:
                "You lose!"
                $ battleContinues = False
        
    # $ renpy.pause()

    $ quick_menu = True
    window show
