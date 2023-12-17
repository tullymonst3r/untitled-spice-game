init -8 python in spellslib: 
    spells = {}

    class Spell(object):
        def __init__(self, name: str, magicType: str, cost: int, *args, **kwargs):
            self.name = name
            self.magicType = magicType
            self.cost = cost
            self.is_multiattack = kwargs.get('is_multiattack', False)
            self.cooldown = kwargs.get('cooldown', 0)
            self.icon = kwargs.get('icon', '')
            self.damage = kwargs.get('damage', 0)
        def __str__(self):
            return self.name
    
    # Example of spell data
    # spell = {
    #     name: "Name display. (str)",
    #     icon: "spell icon. (str)"
    #     magicType: "(old|new) Magic. `new` magic type requires magic weapon.",
    #     damage: "Attack damage. (int)",
    #     level: "Multiplier of damage and effects. Only `old` magic. (int)",
    #     cost: "Mana required to use this spell. (int)",
    #     cooldown: "Ammount of ronunds the spell is unavaileable after use. Only `old` magic. (int)",
    #     is_multiattack: "Whether the spell hits an entire team at a time. (boolean)",
    #     effects: "List of status effects applied on the target. (List of tuples. [...(effect_tag, level, duration(optional))])"
    # }

    spells['fireball'] = Spell('Fireball', 'old', 10, cooldown=2, damage=70)
    spells['hex'] = Spell('Hex', 'old', 25, is_multiattack=True, cooldown=3, damage=40)
