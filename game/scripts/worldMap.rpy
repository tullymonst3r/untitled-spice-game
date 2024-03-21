init python:
    import store.missionslib as missionslib
    import store.playerLib as playerLib
    import store.combatLib as combatLib
    import store.itemslib as itemslib
    import store.spellslib as spellslib
    import store.effectsLib as effectsLib
    currentMission = None
    exitMapMenu= False
    showEnterMapAnimation = True
    prevMission = currentMission

transform initMap(currentMission):
    zoom 0.7 xpos 0 ypos -400  alpha 0.0
    ease 1.0 alpha 1.0
    linear 1.0 zoom 1.5 xpos currentMission.x ypos currentMission.y
transform panMap(currentMission, prevMission):
    zoom 1.5 xpos prevMission.x ypos prevMission.y
    linear 0.7 xpos currentMission.x ypos currentMission.y
transform showMapMenuBottom():
    yalign 2.0
    easein 0.4 yalign 1.01
    on hide:
        easeout 0.4 yalign 2.0

screen worldMap():
    fixed:
        if showEnterMapAnimation:
            add "worldMap2.jpg" at initMap(currentMission)
        else:
            add "worldMap2.jpg" at panMap(currentMission, prevMission)

screen mapMenu(animations):
    zorder 99
    vbox:
        align (0.01, 0.5)
        fixed:
            xsize 1 ysize 1
            imagebutton:
                anchor (0.0, 0.0)
                idle "chevronLeft.png"
                hover "chevronLeft_hovered.png"
                action [Return((0, -1))]
    vbox:
        align (0.91, 0.5)
        fixed:
            xsize 1 ysize 1
            imagebutton:
                anchor (0.0, 0.0)
                idle "chevronRight.png"
                hover "chevronRight_hovered.png"
                action [Return((0, 1))]
    fixed:
        if animations:
            at showMapMenuBottom
        xalign 0.5 yalign 1.01
        xsize 1093 ysize 294
        add "map_menu_bottom.png" align (0.5, 0.5)
        grid 3 1:
            align (0.5, 0.7)
            xsize 970 ysize 100
            yspacing 10 xspacing 25
            use darkWoodBtn('Shop', (1,0))
            use metalBtn('Select mission', (2,0))
            use darkWoodBtn('Menu', (3,0))

screen mapHeader:
    if currentMission is not None:
        zorder 99
        frame:
            xsize 1750 ysize 100 align (0.5, 0.0)
            fixed:
                vbox:
                    align (0.5, 0.01)
                    text "{}".format(currentMission.name) style "header" xalign 0.5
                    text "{}".format(currentMission.description) style "description" xalign 0.5
style header:
    size 50
    color "#ffffff"                        
style description:
    size 25
    color "#ffffff"  


label world:
    window hide
    with Fade(1.0, 0, 0)
    $ exitMapMenu = False
    play music "audio/Kingdom_Under_Fire_Heroes_Soundtrack_Anxiousness.mp3"
    $ showMenuAnimations = True
    if missionslib.currentMission is None:
        # First time entering map
        $ missionslib.currentMission = 0
        $ currentMission = missionslib.missions[missionslib.currentMission]
        $ prevMission = currentMission
        $ showEnterMapAnimation = True
        show screen worldMap
        pause 2.0
        $ showEnterMapAnimation = False
    else:
        $ missionslib.currentMission = missionslib.currentMission
        $ currentMission = missionslib.missions[missionslib.currentMission]
        $ prevMission = currentMission
        $ showEnterMapAnimation = False
        show screen worldMap
    show screen mapHeader

    while exitMapMenu == False:
        call screen mapMenu(showMenuAnimations)
        $ selection = _return
        if selection[0] == 0:
            $ showMenuAnimations = False
            # Swap mission
            $ prevMission = currentMission
            $ missionslib.currentMission += selection[1]
            if missionslib.currentMission > 2:
                $ missionslib.currentMission = 0
            if missionslib.currentMission < 0:
                $ missionslib.currentMission = 2
            $ currentMission = missionslib.missions[missionslib.currentMission]
            # pause 0.7
        elif selection[0] == 1:
            # shop
            $ showMenuAnimations = True
        elif selection[0] == 2:
            $ showMenuAnimations = True
            # Select Mission
            $ exitMapMenu = True
            # call party_menu
            # $ cancel = _return
            # if cancel == False:
            #     # Accept and enter mission
            #     $ exitMapMenu = True
        elif selection[0] == 3:
            $ showMenuAnimations = True
            call player_menu

        $ renpy.hide_screen("mapMenu")
    hide screen mapHeader
    hide screen worldMap
    stop music fadeout 1.0
    with Fade(1.0, 0, 0)