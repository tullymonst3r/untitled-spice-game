﻿
define config.rollback_enabled = False
define onion = Character("Onion Chives", color="#a39a64")
define garlic = Character("Garlic Chives", color="#256b36")


init python:
    import random
    combatGarlic = combatlib.CombatCharacter('Garlic', 'garlic_chives', 100, baseStrength=20, baseDefense=10, baseSpeed=10, baseFinesse=2, baseMana=30, spells=({'tag': 'fireball', 'cd': 0, 'lvl': 1}, {'tag': 'hex', 'cd': 0, 'lvl': 1}))
    combatJanny = combatlib.CombatCharacter('Town Jannitor', 'town_janitor', 200, baseStrength=10, baseDefense=5, baseSpeed=7, baseFinesse=1, hand="jannyWeapon")
    combatJanny2 = combatlib.CombatCharacter('Town Jannitor 2', 'town_janitor', 200, baseStrength=10, baseDefense=5, baseSpeed=7, baseFinesse=1, hand="jannyWeapon")
    combatlib.combatChars['garlic'] = combatGarlic
    combatlib.combatChars['janny'] = combatJanny
    combatlib.combatChars['janny2'] = combatJanny2

label start:
    scene bg chives_home
    # show onion_chives at left
    # with move

    # onion "My son."

    # onion "You are such a beta whimpy looser good for nothing."

    # onion "Even your brother, Soy Chives, is not as much of a soyboy as you are."

    # onion "Kill yourself."

    # hide onion_chives
    # with moveoutleft

    # garlic ". . ."

    # garlic "Thanks, dad."

    screen select_class:
        grid 2 2:
            xalign 0.5
            yalign 0.5
            spacing 20
            frame:
                xsize 250
                button:
                    text "Warrior"
                    style "custom_btn"
                    action [ToggleScreen("select_class"), Jump("choose_warrior")]
            frame:
                xsize 250
                button:
                    text "Ranger"
                    style "custom_btn"
                    action [ToggleScreen("select_class"), Jump("choose_ranger")]
            frame:
                xsize 250
                button:
                    text "Blacksmith"
                    style "custom_btn"
                    action [ToggleScreen("select_class"), Jump("choose_blacksmith")]
            frame:
                xsize 250
                button:
                    text "Wizard"
                    style "custom_btn"
                    action [ToggleScreen("select_class"), Jump("choose_wizard")]

    style custom_btn:
        color "#1a1a1a"
        idle_color "#1a1a1a"
        hover_color "#414141"
        xpadding 40
        ypadding 20
        xalign 0.5
        yalign 0.5

    screen item_card(item):
        vbox:
            xalign 0.5 ypos 50
            fixed:
                xsize 499 ysize 709
                add "item_card"
                add "{}".format(item.imageName) align (.5, .16)
                text "{}".format(item.name) align (.5, .67) style "h2"
                if hasattr(item, 'weaponData'):
                    text "• Damage: +{}".format(item.weaponData["damage"]) align (.2, .73) style "desc"
                    text "• Weight: {}".format(item.weaponData["weight"]) align (.18, .78) style "desc"
                    if item.weaponData.has_key('mana'):
                        text "• Mana: {}".format(item.weaponData["mana"]) align (.18, .83) style "desc"
                    if item.weaponData.has_key('precision'):
                        text "• Precision: {}".format(item.weaponData["precision"]) align (.18, .83) style "desc"
    style h2:
        color "#000000"
    style desc:
        size 20
        color "#000000"

    call screen select_class

    label choose_warrior:
        "You chose the Warrior class."

        "You gain +5 points of defense and +5 points of strength."
        python:
            combatGarlic.baseDefense += 5
            combatGarlic.baseStrength += 5
            renpy.notify("+5 defense and strength")
            foundItem = itemslib.items['gay_sword']
            combatGarlic.hand = 'gay_sword'
            combatGarlic = combatGarlic
        show screen item_card(foundItem)
        jump touch_grass

    label choose_ranger:
        "You chose the Ranger class."

        "You gain +3 points of finesse."
        python:
            combatGarlic.baseFinesse += 3
            renpy.notify("+3 finesse")
            foundItem = itemslib.items['mg42']
            combatGarlic.hand = 'mg42'
            combatGarlic = combatGarlic
        show screen item_card(foundItem)
        jump touch_grass
    
    label choose_blacksmith:
        "You chose the Blacksmith class."

        "You gain nothing."

        "Like real men."
        python:
            foundItem = itemslib.items['root_hammer']
            combatGarlic.hand = 'root_hammer'
            combatGarlic = combatGarlic
        show screen item_card(foundItem)
        jump touch_grass

    label choose_wizard:
        "You chose the Wizard class."

        "You gain +10 points of mana."
        python:
            combatGarlic.baseMana += 10
            renpy.notify("+10 mana")
            foundItem = itemslib.items['gay_stick']
            combatGarlic.hand = 'gay_stick'
            combatGarlic = combatGarlic
        show screen item_card(foundItem)
        jump touch_grass
    
    label touch_grass:

        # "You acquired a new weapon."

        $ renpy.pause()
        $ renpy.hide_screen("item_card")

        # "Now go outside, you fucking dweeb."

        # scene bg outside with Fade(0.5, 0, 0.5)

        # ""

        # garlic "Now what?"

        # "{color=#E9A875}Now you die!{/color}"

        # garlic "W-Who said that!?"

        # "Suddenly infront of Garlic, a wall of pure unpaid power raised, blocking his path."

        "\[ You have enterered in combat \]"

        scene bg combat_field with Fade(0.5, 0, 0.5)

        # Setting both teams for combat
        $ allies = ['garlic']
        $ enemies = ['janny', 'janny2']
        $ combatants = (allies,enemies) # set tuple
        call combat(combatants)

    return


