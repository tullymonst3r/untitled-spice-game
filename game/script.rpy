
define config.rollback_enabled = False
# define garlic = Character("Garlic Chives", color="#256b36")
transform leftFlip:
    xalign 0.0 xzoom -1.0
transform rightFlip:
    xalign 1.0 xzoom -1.0
transform flip:
    xzoom -1.0


init python:
    import store.missionslib as missionslib

label start:
    # start game
    while missionslib.lastMissionEnded == False:
        # While game is not over
        # Go to world map
        call world from _call_world
        # Go to selected mission
        call expression "mission" + str(missionslib.currentMission + 1) from _call_expression
    # Last mission has been played. Show different unlockeable endings and credits(?)
    return


