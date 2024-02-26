
define onion = Character("Onion Chives", color="#a39a64")

init python:
    import copy
    # import store.combatlib as combatlib

label mission1:
    scene bg chives_home
    show onion_chives at left
    with move

    onion "My son."

    onion "You are such a beta whimpy looser good for nothing."

    onion "Even your brother, Soy Chives, is not as much of a soyboy as you are."

    onion "Kill yourself."

    hide onion_chives
    with moveoutleft

    garlic ". . ."

    garlic "Thanks, dad."

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

        # "You gain +5 points of defense and +5 points of strength."
        python:
            # combatGarlic.baseDefense += 5
            # combatGarlic.baseStrength += 5
            # renpy.notify("+5 defense and strength")
            foundItem = itemslib.items['gay_sword']
            # combatGarlic.assignSlot(1, copy.deepcopy(foundItem))
            # combatlib.updateCharsDict()
        show screen item_card(foundItem)
        jump touch_grass

    label choose_ranger:
        "You chose the Ranger class."

        # "You gain +3 points of finesse."
        python:
            # combatGarlic.baseFinesse += 3
            # renpy.notify("+3 finesse")
            foundItem = itemslib.items['mg42']
            # combatGarlic.assignSlot(1, copy.deepcopy(foundItem))
            # combatlib.updateCharsDict()
        show screen item_card(foundItem)
        jump touch_grass
    
    label choose_blacksmith:
        "You chose the Blacksmith class."

        # "You gain nothing."

        # "Like real men."
        python:
            foundItem = itemslib.items['root_hammer']
            # combatGarlic.assignSlot(1, copy.deepcopy(foundItem))
            # combatlib.updateCharsDict()
        show screen item_card(foundItem)
        jump touch_grass

    label choose_wizard:
        "You chose the Wizard class."

        # "You gain +10 points of mana."
        python:
            # combatGarlic.baseMana += 10
            # renpy.notify("+10 mana")
            foundItem = itemslib.items['gay_stick']
            # combatGarlic.assignSlot(1, copy.deepcopy(foundItem))
            # combatlib.updateCharsDict()
        show screen item_card(foundItem)
        jump touch_grass
    
    label touch_grass:

        "You acquired a new weapon."

        $ renpy.hide_screen("item_card")

        "Now go outside, you fucking dweeb."

        scene bg outside with Fade(0.5, 0, 0.5)

        ""

        garlic "Now what?"

        "{color=#E9A875}Now you die!{/color}"

        garlic "W-Who said that!?"

        "Suddenly infront of Garlic, a wall of pure unpaid power raised, blocking his path."


        # . . .rest of scene
        # Announce the player that a combat will begin
        "\[ You have entered in combat \]"
        # Change to combat background
        scene bg combat_field with Fade(0.5, 0, 0.5)

        # Setting both teams for combat
        $ allies = ['garlic']
        $ enemies = ['janny', 'janny']
        $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
        call combat(combatants) from _call_combat

        if combatlib.wonLastCombat:
            # continue with scene if player won
            garlic "I won!"
        else:
            # continue with scene if player lost
            garlic "I lost :("

    return


