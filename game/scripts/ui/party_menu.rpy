screen partyMenu():
    zorder 99
    fixed:
        frame:
            align (0.5, 0.5)
            padding (40, 40)
            xsize 700 ysize 800
            grid 2 1:
                xspacing 30
                frame:
                    xsize 300 ysize 550
                    align (0.5, 0.5)
                    padding (20, 20)
                    grid 1 4:
                        align (0.5, 0.5)
                        yspacing 30
                        for (index, slot) in enumerate(playerLib.party):
                            if slot is not None:
                                use regularBtn(combatlib.combatChars[slot].name, ('remove', index))
                            else:
                                use regularBtn('', ('remove', index))
                frame:
                    xsize 300
                    align (0.5, 0.5)
                    padding (20, 20)
                    viewport:
                        child_size (280, 750)
                        mousewheel True
                        draggable True
                        vbox:
                            ysize 750
                            for (guardian) in playerLib.guardians.items():
                                if (guardian[1] == False):
                                    use regularBtn(combatlib.combatChars[guardian[0]].name, ('add', guardian[0]), not playerLib.isPartySlotAvailable())
        hbox:
            spacing 15
            align (0.5, 0.95)
            use regularBtn('Cancel', ('cancel', None))
            use regularBtn('OK', ('exit', None))

label party_menu:
    $ exitPartyMenu = False
    $ cancel = False
    while exitPartyMenu == False:
        call screen partyMenu
        $ selection = _return
        if selection[0] == 'remove':
            $ playerLib.removePartyMember(selection[1])
        elif selection[0] == 'add':
            $ playerLib.addPartyMember(selection[1])
        elif selection[0] == 'exit':
            $ exitPartyMenu = True
        elif selection[0] == 'cancel':
            # Cancel and return select mission
            $ exitPartyMenu = True
            $ cancel = True
    return cancel