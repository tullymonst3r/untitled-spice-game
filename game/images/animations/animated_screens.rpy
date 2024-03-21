init python:
    def hideAnimations():
        renpy.hide_screen('missedHit')
        renpy.hide_screen('rangeHit')
        renpy.hide_screen('magicHit')
        renpy.hide_screen('crit')
        renpy.hide_screen('impact')
        renpy.hide_screen('fire')
        renpy.hide_screen('hex')

image impact_animation = Movie(channel="vfx",
    play="images/animations/impact_animation.webm",
    mask="images/animations/impact_animation_mask.webm",
    framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen impact(position):
    zorder 100
    fixed:
        pos (position[0], position[1])
        xsize 1 ysize 1
        add "impact_animation" anchor (0.5, 0.99)
    timer 1.0 action [Hide('impact')]

image crit_animation = Movie(channel="vfx",
    play="images/animations/crit_animation.webm",
    mask="images/animations/crit_animation_mask.webm",
    framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen crit(position): #
    zorder 100
    fixed:
        pos (position[0], position[1])
        xsize 1 ysize 1
        add "crit_animation" anchor (0.5, 0.99)
    timer 1.0 action [Hide('crit')]

image magichit_animation = Movie(channel="vfx",
    play="images/animations/magic_hit_animation.webm",
    mask="images/animations/magic_hit_animation_mask.webm",
    framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen magicHit(position):
    zorder 100
    fixed:
        pos (position[0], position[1])
        xsize 1 ysize 1
        add "magichit_animation" anchor (0.5, 0.99)
    timer 1.32 action [Hide('magicHit')]

image missedhit_animation = Movie(channel="vfx",
    play="images/animations/missedhit_animation.webm",
    mask="images/animations/missedhit_animation_mask.webm",
    framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen missedHit(position):
    zorder 100
    fixed:
        pos (position[0], position[1])
        xsize 1 ysize 1
        add "missedhit_animation" anchor (0.5, 0.99) xysize(256, 308)
    timer 0.37 action [Hide('missedHit')]

image hex_animation = Movie(channel="vfx",
    play="images/animations/hexHit_animation.webm",
    mask="images/animations/hexHit_animation_mask.webm",
    framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen hex(position):
    zorder 100
    fixed:
        pos (position[0], position[1])
        xsize 1 ysize 1
        add "hex_animation" anchor (0.5, 0.99)
    timer 0.37 action [Hide('hex')]