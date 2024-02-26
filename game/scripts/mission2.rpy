# init python:
    # import store.combatlib as combatlib

label mission2:
    scene bg chives_home

    # . . .rest of scene
    # Announce the player that a combat will begin
    "\[ You have entered in combat \]"
    # Change to combat background
    scene bg combat_field with Fade(0.5, 0, 0.5)

    # Setting both teams for combat
    # $ allies = ['garlic', 'rosemary', 'sage']
    $ allies = playerLib.party.copy()
    $ enemies = ['fallenJanny', 'janny', 'janny']
    $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
    call combat(combatants) from _call_combat_1

    if combatlib.wonLastCombat:
        # continue with scene if player won
        garlic "I won!"
    else:
        # continue with scene if player lost
        garlic "I lost :("
    return


