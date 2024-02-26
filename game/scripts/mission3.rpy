define caraway = Character("Caraway", color="#a39a64")

init python:
    import store.combatlib as combatlib
    tentacle = combatlib.CombatCharacter(
        'Tentacle',
        spriteName='octo_tenta',
        baseHealth=200,
        baseStrength=15,
        baseDefense=40,
        baseSpeed=3,
        baseFinesse=4,
        baseAccuracy=0,
        baseMagicDef=0,
        equipment=[
            combatlib.Attack(name="Lash", attackData=combatlib.AttackData(target="enemy")),
            combatlib.Attack(name="Swipe", attackData=combatlib.AttackData(target="enemies", damage=-5, finesse=-4)),
        ])
    octopus = combatlib.CombatCharacter(
        'Octopus',
        spriteName='octo_head',
        baseHealth=300,
        baseStrength=24,
        baseDefense=50,
        baseSpeed=3,
        baseFinesse=6,
        baseAccuracy=0,
        baseMagicDef=0,
        equipment=[
            combatlib.Attack(name="Bite", attackData=combatlib.AttackData(damage=5, finesse=4)),
            combatlib.Attack(name="Shriek", attackType="range", attackData=combatlib.AttackData(target="enemies", accuracy=25, damage=15)),
            combatlib.Attack(name="Tentacle Swirl", attackData=combatlib.AttackData(target="enemies", finesse=-6, damage=-15, hits=3)),
            combatlib.Attack(name="Ink Splash", attackType="range", attackData=combatlib.AttackData(target="enemies", accuracy=7, forceHitChance=True, active_effects=['slow1'])),
        ])
    combatCaraway = combatlib.CombatCharacter(
        'Caraway',
        spriteName='caraway_s_combat',
        baseHealth=500,
        baseStrength=0,
        baseDefense=20,
        baseSpeed=7,
        baseFinesse=12,
        baseAccuracy=30,
        baseMagicDef=40,
        baseTurns=3,
        equipmentLevels = {'megaHeal': 5},
        gold=50,
        equipment=[
            copy.deepcopy(itemslib.items['carawayTs']),
            copy.deepcopy(spellslib.spells['megaHeal']),
            copy.deepcopy(spellslib.spells['boost']),
            copy.deepcopy(spellslib.spells['transFallenJanny']),
            copy.deepcopy(spellslib.spells['transDiamonGiant']),
        ])
    combatlib.addCharacter('octopus', octopus)
    combatlib.addCharacter('tentacle', tentacle)
    combatlib.addCharacter('caraway', combatCaraway)

label mission3:
    scene bg outside

    # . . .rest of scene
    # Announce the player that a combat will begin
    "\[ You have entered in combat \]"
    # Change to combat background
    scene bg water_field with Fade(0.5, 0, 0.5)

    # Setting both teams for combat
    $ allies = ['garlic', 'rosemary', 'sage', 'thyme']
    # $ combatlib.gauntlet = True
    $ allies = playerLib.party.copy()
    $ enemies = ['tentacle', 'tentacle', 'tentacle', 'octopus']
    $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
    call combat(combatants) from _call_combat_2

    show caraway_s at right
    with move
    if combatlib.wonLastCombat:
        caraway "Well done, kids! Warm up is over."
        caraway "Now let the real battle begin."

        hide caraway_s
        with moveoutright

        "\[ You have entered in combat \]"
        $ allies = playerLib.party.copy()
        $ enemies = ['caraway']
        $ combatants = (allies,enemies) # set tuple (call statement only accepts one parameter)
        call combat(combatants) from _call_combat_3

        show caraway_s at right
        with move
        if combatlib.wonLastCombat:
            caraway "Outstanding job out there!"
            caraway "You deserve a reward for such amazing display."

            "Give the player something I don't know."
        else:
            caraway "It was a valient effort."
    else:
        # continue with scene if player lost
        caraway "Better luck next time, kids."
    
    # $ combatlib.gauntlet = False
    
    caraway "Now everyone, back to class."
    
    hide caraway_s
    with moveoutright

    hide bg water_field
    
    return


