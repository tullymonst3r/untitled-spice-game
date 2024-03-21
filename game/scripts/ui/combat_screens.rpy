init python:
    import store.skillsLib as skillsLib
    import random
    recover = skillsLib.getSkill('recover')

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
                if len(combatLib.allies_alive) > 4:
                    scrollbars "vertical"
                for char_tag in combatLib.allies_alive:
                    frame:
                        xsize 350
                        vbox:
                            text "{}".format(combatLib.arena[char_tag].name) style "label"
                            bar:
                                value combatLib.arena[char_tag].hp
                                range combatLib.arena[char_tag].base_hp
                                left_bar "#ce1937ff"  right_bar "#ffffffaa"
                                xysize (325, 20)
                            bar:
                                value combatLib.arena[char_tag].mp
                                range combatLib.arena[char_tag].base_mp
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
                if len(combatLib.enemies_alive) > 4:
                    scrollbars "vertical"
                for char_tag in combatLib.enemies_alive:
                    frame:
                        xsize 350
                        vbox:
                            text "{}".format(combatLib.arena[char_tag].name) style "label"
                            bar:
                                value combatLib.arena[char_tag].hp
                                range combatLib.arena[char_tag].base_hp
                                left_bar "#ce1937ff"  right_bar "#ffffffaa"
                                xysize (325, 20)
                            bar:
                                value combatLib.arena[char_tag].mp
                                range combatLib.arena[char_tag].base_mp
                                left_bar "#1e8cdbff"  right_bar "#ffffffaa"
                                xysize (325, 15)
transform char_sprite_idle(x,y):
    pos (x, y) matrixcolor None
transform char_sprite_protect(x,y):
    pos (x, y)
    linear 0.3 pos (960, 540)
    pause 0.5
    linear 0.25 pos (x, y)
transform char_sprite_hurt(x,y):
    pos (x+random.randrange(10,20), y+random.randrange(10,20))
    linear 0.1 pos (x, y) matrixcolor TintMatrix('#ff0000') * SaturationMatrix(1.0)
    linear 0.1 pos (x+random.randrange(10,20), y+random.randrange(10,20))
    linear 0.1 pos (x, y)
    linear 0.1 pos (x+random.randrange(10,20), y+random.randrange(10,20))
    linear 0.1 pos (x, y) matrixcolor None
screen char_sprite(char):
    fixed:
        pos (char.x, char.y)
        xsize 200 ysize 200
        add "{}".format(char.sprite_name) anchor (0.5, 1.0)
        if char.sprite_state == 'protect':
            at char_sprite_protect(char.x, char.y)
        elif char.sprite_state == 'hurt':
            at char_sprite_hurt(char.x, char.y)
        else:
            at char_sprite_idle(char.x, char.y)


screen char_status(char):
    zorder -1
    if char.tag in combatLib.arena_tags:
        vbox:
            pos (char.x, char.y)
            anchor (0.0, 0.0)
            fixed:
                xanchor 0.5
                xsize 203 ysize 50
                if char.base_mp > 0:
                    bar:
                        xanchor -0.25 
                        value AnimatedValue(value=char.mp, range=char.base_mp, delay=0.5)
                        # value char.mp
                        # range char.base_mp
                        left_bar "full_mp.png" right_bar "empty_mp.png"
                        xysize (142, 50)
                bar:
                    value AnimatedValue(value=char.hp, range=char.base_hp, delay=0.5)
                    # value char.hp
                    # range char.base_hp
                    left_bar "full_hp.png" right_bar "empty_hp.png"
                    xysize (203, 50)
                    # bar:
                    #     value char.hp
                    #     range char.base_hp
                    #     left_bar "#ce1937ff" right_bar "#ffffffaa"
                    #     xysize (180, 20)
                    # if char.base_mp > 0:
                            # value char.mp
                            # range char.base_mp
                            # left_bar "#1e8cdbff" right_bar "#ffffffaa"
                            # xysize (180, 10)
            hbox:
                ysize 51 xanchor 0.5 spacing 5
                if len(char.teammate_preventive_effects) > 0:
                    for effect in char.teammate_preventive_effects:
                        if effect is not None:
                            use statusEffectIcon(effect)
                if len(char.effects) > 0:
                    for effect in char.effects:
                        if effect is not None:
                            use statusEffectIcon(effect)
        mousearea:
            pos (char.x, char.y)
            anchor (0.5, 0.0)
            xsize 200 ysize 50
            hovered Show("charTooltip", char=char)
            unhovered Hide("charTooltip")

screen statusEffectIcon(effect):
    fixed:
        xsize 51 ysize 51
        add "{}_icon".format(effect.icon)
        mousearea:
            xsize 51 ysize 51
            # hovered [Hide("effectTooltip"), Show("effectTooltip", effect=effect)]
            # unhovered Hide("effectTooltip")

screen cancel_select_btn():
    zorder -1
    frame:
        align(0.5, 1.0)
        button:
            xsize 150 ysize 75
            text "Cancel" style "sublabel" align (0.5, 0.5)
            action [Jump("actionSelection")]
screen select_target(in_list, target_type, select_all=False):
    default hovered_all = False
    zorder -1
    use cancel_select_btn
    for char in list(combatLib.arena.values()):
        if char.tag in in_list:
            fixed:
                pos (char.x, char.y)
                xsize 1 ysize 1
                imagebutton:
                    anchor (0.5, 1.0)
                    idle "sprite_target_{}".format('idle' if hovered_all == False else 'hover_{}'.format(target_type))
                    hover "sprite_target_hover_{}".format(target_type)
                    if select_all:
                        hovered SetScreenVariable("hovered_all", True)
                        unhovered SetScreenVariable("hovered_all", False)
                        action [Hide('select_target'), SetScreenVariable("hovered_all", False), Return(char)]
                    else:
                        action [Hide('select_target'), Return(char)]


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
                for (index, skill) in enumerate(char.skills):
                    if skill is not None:
                        if skill.cd > 0:
                            use regularBtn("CD: {}".format(skill.cd), None, True)
                        elif char.mp < (skill.skill_data.mp_cost):
                            use regularBtn("Not enough mp", None, True)
                        # elif skill.skill_data.magic_type == 'new':
                        # elif (hasattr(skill, 'magicType')) and (skill.skill_data.magic_type == 'new') and (char.tsTotalMana < 1):
                            # use regularBtn("Need Terrasphere", None, True)
                        else:
                            use attackBtn(skill, skill)
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
                            action [Hide("actions_box"), Return(recover)]
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
                        for (item_tuple) in playerLib.inventory.items():
                            python:
                                item = itemslib.getItem(item_tuple[0])
                            frame:
                                align (0.5, 0.5)
                                xsize 330 ysize 120
                                hbox:
                                    use attackBtn(item, item)
                                    text "x {}".format(item_tuple[1]) style "sublabel" align (0.5, 0.5)
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
# transform turn_animate:
#     anchor (0.5, 3.5)
#     ease 2.0 anchor (0.5, 3.0)
#     ease 2.0 anchor (0.5, 3.5)
#     repeat
transform turn_animate:
    alpha 1.0
    ease 2.0 alpha 0.0
    ease 2.0 alpha 1.0
    repeat
screen current_turn(x,y):
    zorder 100
    fixed:
        pos (x, y)
        xsize 1 ysize 1
        add "currentTurn.png" at turn_animate anchor (0.5, 2.5)

screen float_msg(x, y, text, textColor="#ffffff"):
    zorder 101
    fixed:
        pos (x, y)
        xsize 1 ysize 1
        text "{}".format(text) textalign 0.5 anchor (0.5, 0.5) size 40 bold True color textColor style "numberStyle" at txtAnimate
    timer 1.3 action Hide('float_msg')
screen float_num(x, y, val, textColor="#ffffff"):
    zorder 101
    fixed:
        pos (x, y)
        xsize 1 ysize 1
        text "{}".format(abs(val)) textalign 0.5 anchor (0.5, 0.5) size 60 bold True color textColor style "numberStyle" at numberAnimate
    timer 1.3 action Hide('float_num')
transform txtAnimate:
    align (0.5, 2.5) zoom 0.1
    linear 0.1 align (0.5, random.uniform(1.0, 3.0)) zoom 1.0
    pause 0.7
    linear 0.5 alpha 0.0
transform numberAnimate:
    align (0.5, 2.5) zoom 0.1
    linear 0.1 align (random.uniform(1.0, 2.0), random.uniform(1.0, 2.0)) zoom 1.0
    pause 0.7
    linear 0.5 alpha 0.0
style numberStyle:
    outlines [ (3.5, "#000", absolute(0), absolute(0)) ]


