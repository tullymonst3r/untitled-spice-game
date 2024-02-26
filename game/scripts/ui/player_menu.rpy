screen playerMenu():
    modal True
    zorder 99
    fixed:
        align (0.5, 0.5)
        xsize 350 ysize 853
        add "player_menu.png" align (0.5, 0.5)
        grid 1 4:
            align (0.5, 0.5)
            xsize 350 ysize 853
            yspacing 50
            use metalBtn('Party', 1)
            use metalBtn('Guardians', 2)
            use metalBtn('Inventory', 3)
            use darkWoodBtn('OK', 0)
label player_menu:
    $ exitPlayerMenu = False
    while exitPlayerMenu == False:
        call screen playerMenu
        $ selection = _return
        if selection == 1:
            call party_menu
        elif selection == 2:
            call guardians_menu
        elif selection == 3:
            $ exitPlayerMenu = True
        elif selection == 0:
            $ exitPlayerMenu = True
    return