init python:
    def hideAnimations():
        renpy.hide_screen('missedHit')
        renpy.hide_screen('rangeHit')
        renpy.hide_screen('magicHit')
        renpy.hide_screen('crit')
        renpy.hide_screen('impact')
        renpy.hide_screen('fire')
        renpy.hide_screen('hex')

screen impact(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "impact_animation" anchor (0.5, 0.99)
screen crit(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "crit_animation" anchor (0.5, 0.99)
screen magicHit(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "magichit_animation" anchor (0.5, 0.99)
screen rangeHit(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "rangehit_animation" anchor (0.5, 0.99) xysize(276, 240)
screen missedHit(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "missedhit_animation" anchor (0.5, 0.99) xysize(256, 308)
screen fire(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "fire_animation" anchor (0.5, 0.99) xysize(256, 308)
screen hex(positions):
    zorder 100
    for position in positions:
        vbox:
            pos (position[0], position[1])
            fixed:
                xsize 1 ysize 1
                add "hex_animation" anchor (0.5, 0.99) xysize(256, 264)