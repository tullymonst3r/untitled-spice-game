define caraway = Character("Caraway", color="#a39a64")

label mission3:
    scene bg outside

    # . . .rest of scene
    # Announce the player that a combat will begin
    "\[ You have entered in combat \]"
    # Change to combat background
    scene bg water_field with Fade(0.5, 0, 0.5)

    # Setting both teams for combat
    $ allies = ['garlic', 'sage', 'rosemary', 'parsley']
    # $ allies = playerLib.party.copy()
    $ enemies = ['tentacle', 'tentacle', 'tentacle', 'octopus']
    $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
    call combat(combatants) from _call_combat_2

    show caraway_s at right
    with move
    if _return: # won last combat
        caraway "Well done, kids! Warm up is over."
        caraway "Now let the real battle begin."

        hide caraway_s
        with moveoutright

        "\[ You have entered in combat \]"
        $ allies = ['garlic', 'rosemary', 'sage', 'parsley']
        # $ allies = playerLib.party.copy()
        $ enemies = ['caraway']
        $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
        call combat(combatants) from _call_combat_3

        show caraway_s at right
        with move
        if _return: # won last combat
            caraway "Outstanding job out there!"
            caraway "You deserve a reward for such amazing display."

            "Give the player something I don't know."
        else:
            caraway "It was a valient effort."
    else:
        # continue with scene if player lost
        caraway "Better luck next time, kids."
    
    
    caraway "Now everyone, back to class."
    
    hide caraway_s
    with moveoutright

    hide bg water_field
    
    return


