style label:
    size 25
    color "#ffffff"
style sublabel:
    size 20
    color "#ffffff"

screen combat_header:
    zorder -1
    frame:
        xsize 1920 ysize 250
        vbox:
            align (0, 0)
            text "Garlic's Party"
            vpgrid:
                cols 2
                spacing 5
                mousewheel True
                draggable True
                if len(combatlib.alliesAlive) > 4:
                    scrollbars "vertical"
                for alliesMember in combatlib.alliesAlive:
                    frame:
                        xsize 350
                        vbox:
                            text "{}".format(combatlib.arenaChars[alliesMember].name) style "label"
                            bar:
                                value combatlib.arenaChars[alliesMember].health
                                range combatlib.arenaChars[alliesMember].baseHealth
                                left_bar "#ce1937ff"  right_bar "#ffffffaa"
                                xysize (325, 20)
                            bar:
                                value combatlib.arenaChars[alliesMember].mana
                                range combatlib.arenaChars[alliesMember].baseMana
                                left_bar "#1e8cdbff"  right_bar "#ffffffaa"
                                xysize (325, 15)
        vbox:
            align (1.0, 0)
            text "Enemies"
            vpgrid:
                cols 2
                spacing 5
                mousewheel True
                draggable True
                if len(combatlib.enemiesAlive) > 4:
                    scrollbars "vertical"
                for enemyMember in combatlib.enemiesAlive:
                    frame:
                        xsize 350
                        vbox:
                            text "{}".format(combatlib.arenaChars[enemyMember].name) style "label"
                            bar:
                                value combatlib.arenaChars[enemyMember].health
                                range combatlib.arenaChars[enemyMember].baseHealth
                                left_bar "#ce1937ff"  right_bar "#ffffffaa"
                                xysize (325, 20)
                            bar:
                                value combatlib.arenaChars[enemyMember].mana
                                range combatlib.arenaChars[enemyMember].baseMana
                                left_bar "#1e8cdbff"  right_bar "#ffffffaa"
                                xysize (325, 15)

screen char_sprite(char):
    fixed:
        pos (char.x, char.y)
        xsize 200 ysize 200
        add "{}".format(char.spriteName) anchor (0.5, 1.0)

screen charStatus(char):
    zorder -1
    if char.tag in combatlib.arenaTags:
        vbox:
            pos (char.x, char.y)
            anchor (0.0, 0.0)
            fixed:
                xanchor 0.5
                xsize 203 ysize 50
                if char.baseMana > 0:
                    bar:
                        xanchor -0.25 
                        value AnimatedValue(value=char.mana, range=char.baseMana, delay=0.5)
                        # value char.mana
                        # range char.baseMana
                        left_bar "full_mp.png" right_bar "empty_mp.png"
                        xysize (142, 50)
                bar:
                    value AnimatedValue(value=char.health, range=char.baseHealth, delay=0.5)
                    # value char.health
                    # range char.baseHealth
                    left_bar "full_hp.png" right_bar "empty_hp.png"
                    xysize (203, 50)
                    # bar:
                    #     value char.health
                    #     range char.baseHealth
                    #     left_bar "#ce1937ff" right_bar "#ffffffaa"
                    #     xysize (180, 20)
                    # if char.baseMana > 0:
                            # value char.mana
                            # range char.baseMana
                            # left_bar "#1e8cdbff" right_bar "#ffffffaa"
                            # xysize (180, 10)
            if len(char.effects.keys()) > 0:
                hbox:
                    ysize 51 xanchor 0.5 spacing 5
                    for effectTag in char.effects.keys():
                        use statusEffectIcon(effectTag)
        mousearea:
            pos (char.x, char.y)
            anchor (0.5, 0.0)
            xsize 200 ysize 50
            hovered Show("charTooltip", char=char)
            unhovered Hide("charTooltip")

screen statusEffectIcon(effectTag):
    python:
        effect = effectsLib.effects[effectTag]
    fixed:
        xsize 51 ysize 51
        add "{}_icon".format(effectsLib.effects[effectTag].icon)
        mousearea:
            xsize 51 ysize 51
            hovered [Hide("effectTooltip"), Show("effectTooltip", effect=effect)]
            unhovered Hide("effectTooltip")

screen cancelSelectionButton:
    zorder -1
    frame:
        align(0.5, 1.0)
        button:
            xsize 150 ysize 75
            text "Cancel" style "sublabel" align (0.5, 0.5)
            action [Jump("actionSelection")]

screen selection_sprite_enemies:
    default hoveredAll = False
    zorder -1
    use cancelSelectionButton
    for enemyMember in combatlib.enemiesAlive:
        vbox:
            pos (combatlib.arenaChars[enemyMember].x, combatlib.arenaChars[enemyMember].y)
            fixed:
                xsize 1 ysize 1
                imagebutton:
                    anchor (0.5, 0.99)
                    idle "sprite_target_{}".format('idle' if hoveredAll == False else 'hover_enemy')
                    hover "sprite_target_hover_enemy"
                    hovered SetScreenVariable("hoveredAll", True)
                    unhovered SetScreenVariable("hoveredAll", False)
                    action [SetScreenVariable("hoveredAll", False), Hide("selection_sprite_enemies"), Return(True)]
screen selection_sprite_enemy:
    zorder -1
    use cancelSelectionButton
    for enemyMember in combatlib.enemiesAlive:
        vbox:
            pos (combatlib.arenaChars[enemyMember].x, combatlib.arenaChars[enemyMember].y)
            fixed:
                xsize 1 ysize 1
                imagebutton:
                    anchor (0.5, 0.99)
                    idle "sprite_target_idle"
                    hover "sprite_target_hover_enemy"
                    action [Hide("selection_sprite_enemy"), Return(enemyMember)]
screen selection_sprite_allies:
    default hoveredAll = False
    zorder -1
    use cancelSelectionButton
    for allyMember in combatlib.alliesAlive:
        vbox:
            pos (combatlib.arenaChars[allyMember].x, combatlib.arenaChars[allyMember].y)
            fixed:
                xsize 1 ysize 1
                imagebutton:
                    anchor (0.5, 0.99)
                    idle "sprite_target_{}".format('idle' if hoveredAll == False else 'hover_ally')
                    hover "sprite_target_hover_ally"
                    hovered SetScreenVariable("hoveredAll", True)
                    unhovered SetScreenVariable("hoveredAll", False)
                    action [SetScreenVariable("hoveredAll", False), Hide("selection_sprite_allies"), Return(True)]
screen selection_sprite_ally:
    zorder -1
    use cancelSelectionButton
    for allyMember in combatlib.alliesAlive:
        vbox:
            pos (combatlib.arenaChars[allyMember].x, combatlib.arenaChars[allyMember].y)
            fixed:
                xsize 1 ysize 1
                imagebutton:
                    anchor (0.5, 0.99)
                    idle "sprite_target_idle"
                    hover "sprite_target_hover_ally"
                    action [Hide("selection_sprite_ally"), Return(allyMember)]
screen selection_sprite_any:
    zorder -1
    use cancelSelectionButton
    for charTag in combatlib.arenaTags:
        if charTag is not None:
            vbox:
                pos (combatlib.arenaChars[charTag].x, combatlib.arenaChars[charTag].y)
                fixed:
                    xsize 1 ysize 1
                    imagebutton:
                        anchor (0.5, 0.99)
                        idle "sprite_target_idle"
                        hover "sprite_target_hover_any"
                        action [Hide("selection_sprite_any"), Return(charTag)]
screen selection_sprite_all:
    default hoveredAll = False
    zorder -1
    use cancelSelectionButton
    for charTag in combatlib.arenaTags:
        if charTag is not None:
            vbox:
                pos (combatlib.arenaChars[charTag].x, combatlib.arenaChars[charTag].y)
                fixed:
                    xsize 1 ysize 1
                    imagebutton:
                        anchor (0.5, 0.99)
                        idle "sprite_target_{}".format('idle' if hoveredAll == False else 'hover_any')
                        hover "sprite_target_hover_any"
                        hovered SetScreenVariable("hoveredAll", True)
                        unhovered SetScreenVariable("hoveredAll", False)
                        action [SetScreenVariable("hoveredAll", False), Hide("selection_sprite_all"), Return(True)]
screen selection_sprite_self(char):
    zorder -1
    use cancelSelectionButton
    vbox:
        pos (char.x, char.y)
        fixed:
            xsize 1 ysize 1
            imagebutton:
                anchor (0.5, 0.99)
                idle "sprite_target_idle"
                hover "sprite_target_hover_ally"
                action [Hide("selection_sprite_self"), Return(True)]
screen actions_box(char):
    zorder -1
    frame:
        xpadding 30
        ypadding 30
        xalign 0.5 yalign 1.01
        xsize 1000 ysize 250
        hbox:
            align (0.5, 0.5)
            spacing 60
            grid 2 2:
                xsize 970 ysize 100
                yspacing 10 xspacing 25
                for (index, equipment) in enumerate(char.equipment):
                    if equipment is not None:
                        if equipment.cd > 0:
                            use regularBtn("CD: {}".format(equipment.cd), None, True)
                        elif (hasattr(equipment, 'cost')) and (char.mana < (equipment.cost - char.tsTotalMana)):
                            use regularBtn("Not enough mana", None, True)
                        elif (hasattr(equipment, 'magicType')) and (equipment.magicType == 'new') and (char.tsTotalMana < 1):
                            use regularBtn("Need Terrasphere", None, True)
                        else:
                            use attackBtn(equipment, equipment)
                    else:
                        use regularBtn('', None, True)
            hbox:
                spacing 30
                vbox:
                    spacing 10
                    frame:
                        button:
                            xsize 150 ysize 75
                            text "Recover" style "sublabel" align (0.5, 0.5)
                            action [Hide("actions_box"), Return(combatlib.Attack(name="Recover", attackData=combatlib.AttackData(target="self", noDamage=True, heal=10, mana=10)))]
                    frame:
                        button:
                            xsize 150 ysize 75
                            text "Use item" style "sublabel" align (0.5, 0.5)
                            action [Hide("actions_box"), Jump("itemSelection")]
                frame:
                    align (1.0, 0.5)
                    button:
                        xsize 65 ysize 150
                        text "Escape" style "sublabel" align (0.5, 0.5)
                        action [Hide("actions_box"), Jump("confirmEscape")]
screen select_item():
    zorder 10
    fixed:
        frame:
            xpadding 30
            ypadding 30
            xsize 425 ysize 800
            align (0.5, 0.5)
            vbox:
                spacing 20
                align (0.5, 0.5)
                frame:
                    align (0.5, 0.5)
                    button:
                        xsize 150 ysize 75
                        text "Cancel" style "sublabel" align (0.5, 0.5)
                        action [Hide("select_item"), Jump("actionSelection")]
                viewport:
                    xalign 0.5
                    xsize 400
                    child_size (150, 700)
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    vbox:
                        spacing 25
                        xsize 150 ysize 700
                        for (itemTuple) in playerLib.itemsInventory.items():
                            python:
                                item = itemslib.items[itemTuple[0]]
                            frame:
                                align (0.5, 0.5)
                                xsize 330 ysize 120
                                hbox:
                                    use attackBtn(item, item)
                                    text "x {}".format(itemTuple[1]) style "sublabel" align (0.5, 0.5)
                                # button:
                                #     xsize 240 ysize 75
                                #     action [Hide("select_item"), Return((True, item))]
screen confirm_escape():
    zorder 10
    fixed:
        frame:
            xpadding 30
            ypadding 30
            xsize 500 ysize 400
            align (0.5, 0.5)
            vbox:
                spacing 20
                align (0.5, 0.5)
                text "Do you want to escape from battle?" align (0.5, 0.5)
                text "It will be marked as lost!" align (0.5, 0.5) style "sublabel"
                null height 10
                hbox:
                    align (0.5, 0.5)
                    spacing 150
                    textbutton "Yes" action Jump("combatLost")
                    textbutton "No" action Jump("actionSelection")
transform turn_animate:
    anchor (0.5, 3.5)
    ease 2.0 anchor (0.5, 3.0)
    ease 2.0 anchor (0.5, 3.5)
    repeat
screen current_turn(x,y):
    zorder -1
    vbox:
        pos (x, y)
        fixed:
            xsize 1 ysize 1
            add "currentTurn.png" at turn_animate

screen msg_effect(x, y, text, textColor="#ffffff"):
    zorder -1
    vbox:
        pos (x, y)
        fixed:
            xsize 1 ysize 1
            text "{}".format(text) anchor (0.5, 0.5) size 40 bold True color textColor style "numberStyle" at txtAnimate
screen number_effect(x, y, val, textColor="#ffffff"):
    zorder -1
    vbox:
        pos (x, y)
        fixed:
            xsize 1 ysize 1
            text "{}".format(abs(val)) anchor (0.5, 0.5) size 60 bold True color textColor style "numberStyle" at numberAnimate
transform txtAnimate:
    align (0.5, 2.5)
    linear 0.1 align (0.5, random.uniform(3.0, 5.0))
    pause 1.0
    align (100.0, 100.0)
transform numberAnimate:
    align (0.5, 2.5)
    linear 0.1 align (random.uniform(1.0, 2.0), random.uniform(3.0, 5.0))
    pause 1.0
    align (100.0, 100.0)
style numberStyle:
    outlines [ (3.5, "#000", absolute(0), absolute(0)) ]


