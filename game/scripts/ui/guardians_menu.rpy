screen plusBtn(stat, enabled = True):
    if upgrades:
        if enabled:
            textbutton "+" text_style "textBtnEnabled" ysize 25 action Return(('upStat', stat))
        else:
            textbutton "+" text_style "textBtnDisabled" ysize 25
    else:
        null:
            ysize 25
screen minusBtn(stat, enabled = True):
    if upgrades:
        if enabled:
            textbutton "-" text_style "textBtnEnabled" ysize 25 action Return(('downStat', stat))
        else:
            textbutton "-" text_style "textBtnDisabled" ysize 25
    else:
        null:
            ysize 25
    

screen guardiansMenu():
    zorder 99
    fixed:
        frame:
            align (0.5, 0.5)
            padding (40, 40)
            xsize 1100 ysize 800
            hbox:
                align (0.5, 0.5)
                spacing 20
                frame:
                    # Guardian card
                    padding (20, 20)
                    xsize 700
                    yfill True
                    python:
                        guardian = combatLib.combatChars[playerLib.selectedGuardian]
                    vbox:
                        spacing 25
                        hbox:
                            spacing 25
                            # frame:
                            #     xsize 200 ysize 200
                            #     # add "{}".format(guardian.spriteName)
                            vbox:
                                hbox:
                                    spacing 50
                                    text "{} (LVL {})".format(guardian.name, guardian.level) style "label"
                                    text "XP: {}".format(guardian.xp) style "label"
                                for (upgradeable) in playerLib.upgradeableStats.items():
                                    hbox:
                                        spacing 15
                                        fixed:
                                            align (0.5, 0.5)
                                            xysize (100, 25)
                                            text "{}: ".format(upgradeable[1]['label']) style "sublabel" align (0.5, 0.5)
                                        use minusBtn(upgradeable[0], playerLib.unsavedUpgrades[upgradeable[0]] > 0)
                                        hbox:
                                            align (0.5, 0.5)
                                            fixed:
                                                xysize (400, 25)
                                                bar:
                                                    align (0.5, 0.5)
                                                    value getattr(guardian, upgradeable[0]) + playerLib.unsavedUpgrades[upgradeable[0]]
                                                    range upgradeable[1]['max']
                                                    right_bar "#484848" left_bar upgradeable[1]['color']
                                                    xysize (400, 25)
                                                text "{}/{}".format(getattr(guardian, upgradeable[0]) + playerLib.unsavedUpgrades[upgradeable[0]], upgradeable[1]['max']) style "sublabel" align (0.5, 0.5)
                                        use plusBtn(upgradeable[0], playerLib.upgradesAvailable > 0 and (getattr(guardian, upgradeable[0]) + playerLib.unsavedUpgrades[upgradeable[0]]) < upgradeable[1]['max'])
                                if (not upgrades):
                                    hbox:
                                        spacing 15
                                        fixed:
                                            align (0.5, 0.5)
                                            xysize (100, 25)
                                            text "TS MP: " style "sublabel" align (0.5, 0.5)
                                        null
                                        fixed:
                                            xysize (400, 25)
                                            bar:
                                                align (0.5, 0.5)
                                                value guardian.tsTotalMana range (guardian.tsTotalMana if guardian.tsTotalMana > 0 else 1)
                                                right_bar "#484848" left_bar '#0fa0c1'
                                                xysize (400, 25)
                                            text "{}".format(guardian.tsTotalMana) style "sublabel" align (0.5, 0.5)
                                    if guardian.upgrades > 0:
                                        frame:
                                            button:
                                                xsize 100 ysize 50
                                                text "Upgrade" style "sublabel" align (0.5, 0.5)
                                                action [Return(('upgradeStats', guardian.upgrades))]
                                else:
                                    text "Upgrades: {}".format(playerLib.upgradesAvailable) style "sublabel"
                                    hbox:
                                        spacing 15
                                        frame:
                                            button:
                                                xsize 100 ysize 50
                                                text "Save" style "sublabel" align (0.5, 0.5)
                                                action [Return(('saveUpgrades', None))]
                                        frame:
                                            button:
                                                xsize 100 ysize 50
                                                text "Cancel" style "sublabel" align (0.5, 0.5)
                                                action [Return(('cancelUpgrades', None))]
                        text "Equipment:" style "sublabel"
                        grid 2 2:
                            xalign 0.5
                            xfill True
                            yspacing 25 xspacing 25
                            for (index, equipment) in enumerate(guardian.equipment):
                                if equipment is not None:
                                    use attackBtn(equipment, ('selectSlot', index), playerLib.selectedSlot == index)
                                else:
                                    use regularBtn('', ('selectSlot', index), playerLib.selectedSlot == index)
                frame:
                    padding (20, 20)
                    ysize 770
                    xsize 300
                    if playerLib.selectedSlot is None:
                        viewport:
                            child_size (280, 750)
                            mousewheel True
                            draggable True
                            scrollbars "vertical"
                            vbox:
                                spacing 30
                                ysize 750
                                for (guardian) in playerLib.guardians.items():
                                    use regularBtn(combatLib.combatChars[guardian[0]].name, ('select', guardian[0]), guardian[0] == playerLib.selectedGuardian)
                    else:
                        if playerLib.selectedEquipmentType is None:
                            viewport:
                                child_size (280, 750)
                                mousewheel True
                                draggable True
                                vbox:
                                    spacing 30
                                    ysize 750
                                    use regularBtn('Cancel', ('cancelSlot', None))
                                    use regularBtn('Assign Attack', ('assign', 'attack'))
                                    use regularBtn('Assign Weapon', ('assign', 'weapon'))
                                    use regularBtn('Assign Spell', ('assign', 'spell'))
                                    use regularBtn('Unassign', ('unassign', None))
                        elif playerLib.selectedEquipmentType == 'weapon':
                            viewport:
                                child_size (280, 750)
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
                                vbox:
                                    spacing 30
                                    ysize 750
                                    use regularBtn('Cancel', ('cancelSlot', None))
                                    for (weapon) in playerLib.availableWeapons():
                                        use attackBtn(weapon, ('selectEquipment', weapon))
                        elif playerLib.selectedEquipmentType == 'spell':
                            viewport:
                                child_size (280, 750)
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
                                vbox:
                                    spacing 30
                                    ysize 750
                                    use regularBtn('Cancel', ('cancelSlot', None))
                                    for (unlockedSpell) in playerLib.availableSpells(guardian.unlockedSpells):
                                        use attackBtn(unlockedSpell, ('selectEquipment', unlockedSpell))
                        elif playerLib.selectedEquipmentType == 'attack':
                            viewport:
                                child_size (280, 750)
                                mousewheel True
                                draggable True
                                scrollbars "vertical"
                                vbox:
                                    spacing 30
                                    ysize 750
                                    use regularBtn('Cancel', ('cancelSlot', None))
                                    for (unlockedAttack) in playerLib.availableAttacks(guardian.unlockedAttacks):
                                        use attackBtn(unlockedAttack, ('selectEquipment', unlockedAttack))
        hbox:
            spacing 15
            align (0.5, 0.95)
            use regularBtn('OK', ('exit', None))

label guardians_menu:
    $ exitGuardianMenu = False
    $ upgrades = False
    while exitGuardianMenu == False:
        call screen guardiansMenu
        $ selection = _return
        if selection[0] == 'select':
            $ playerLib.selectGuardianToInspect(selection[1])
            $ upgrades = False
        elif selection[0] == 'upgradeStats':
            $ upgrades = True
            $ playerLib.resetUnsavedUpgrades(selection[1])
        elif selection[0] == 'saveUpgrades':
            $ upgrades = False
            $ playerLib.saveUpgrades()
        elif selection[0] == 'cancelUpgrades':
            $ upgrades = False
            $ playerLib.resetUnsavedUpgrades(0)
        elif selection[0] == 'upStat':
            $ playerLib.unsavedUpgrades[selection[1]] += playerLib.upgradeableStats[selection[1]]['jump']
            $ playerLib.upgradesAvailable -= 1
        elif selection[0] == 'downStat':
            $ playerLib.unsavedUpgrades[selection[1]] -= playerLib.upgradeableStats[selection[1]]['jump']
            $ playerLib.upgradesAvailable += 1
        elif selection[0] == 'selectSlot':
            $ playerLib.selectSlot(selection[1])
            $ upgrades = False
        elif selection[0] == 'cancelSlot':
            $ playerLib.selectSlot(None)
            $ upgrades = False
        elif selection[0] == 'assign':
            $ playerLib.selectAssignEquipment(selection[1])
            $ upgrades = False
        elif selection[0] == 'unassign':
            $ upgrades = False
            $ playerLib.unassignSlot()
            $ playerLib.selectSlot(None)
        elif selection[0] == 'selectEquipment':
            $ upgrades = False
            $ playerLib.assignSlot(selection[1])
            $ playerLib.selectSlot(None)
        elif selection[0] == 'exit':
            $ upgrades = False
            $ playerLib.selectSlot(None)
            $ exitGuardianMenu = True
    return