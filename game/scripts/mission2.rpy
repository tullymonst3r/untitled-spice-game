define sage = Character("Sage", image = 'sage', color="#418CAA")
define rosemary = Character("Rosemary", image = 'rosemary', color="#992B41")
define garlic = Character("Garlic", image = 'garlic', color="#6C715C")
define parsley = Character("Parsley", image = 'parsley', color="#956D29")


label mission2:
    scene lyngarth_street day with None
    play music "audio/Sage and Rose Theme The Journey Continues.mp3"
    camera at vpunch
    "AAAAAAAAAAAAA!!!!"

    show sage shocked at left
    with moveinleft
    sage shocked "THAT THING STOLE MY UNDERWEAR!!!"
    show sage embarrased at left

    show rosemary confused at right
    rosemary confused "But I thought you don't wear panties. . ."
    hide rosemary

    show garlic annoyed at right, flip
    garlic annoyed "Uhg!"
    garlic annoyed "I hate trixies!"
    hide garlic

    show parsley ready at right
    parsley ready "Fuck em up, girls!"
    hide parsley with moveoutright
    hide sage with moveoutleft

    "\[ You have entered in combat \]"
    scene bg combat 1 with Fade(0.5, 0, 0.5)
    # scene bg combat train with Fade(0.5, 0, 0.5)

    $ allies = ['garlic', 'rosemary', 'sage', 'parsley']
    $ enemies = ['trixie', 'trixie', 'trixie', 'trixie']
    $ combatants = (allies,enemies)
    call combat(combatants) from _call_combat_1
    scene lyngarth_street day with Fade(0.5, 0, 0.5)
    if _return:
        show sage sappy with moveinleft
        sage sappy "Thanks, girls! <3"
    else:
        show sage cry
        sage cry "Uhhh!"
        sage cry "Can we go home? I need to get a new pair"
    hide sage with moveoutright
    return


