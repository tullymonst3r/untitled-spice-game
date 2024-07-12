init python:
    def hideAnimations():
        renpy.hide_screen('missedHit')
        renpy.hide_screen('rangeHit')
        renpy.hide_screen('magicHit')
        renpy.hide_screen('crit')
        renpy.hide_screen('impact')
        renpy.hide_screen('fire')
        renpy.hide_screen('hex')

# image impact_animation = Movie(channel="vfx",
#     play="images/animations/impact_animation.webm",
#     mask="images/animations/impact_animation_mask.webm",
#     framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen impact(position):
    zorder 100
    python:
        x_var = random.randrange(-30, 30)
        y_var = random.randrange(-30, 30)
        var = random.randrange(1, 4)
        size = random.uniform(0.4, 1.0)
    fixed:
        pos (position[0]+x_var, position[1]+y_var)
        xsize 1 ysize 1
        add "impact_{}_animation".format(var) anchor (0.5, 0.99) zoom (size)
    timer 1.0 action [Hide('impact')]

# image crit_animation = Movie(channel="vfx",
#     play="images/animations/crit_animation.webm",
#     mask="images/animations/crit_animation_mask.webm",
#     framedrop=False, group="vfx", loop=False, keep_last_frame=False)
screen crit(position): #
    zorder 100
    python:
        x_var = random.randrange(-30, 30)
        y_var = random.randrange(-30, 30)
        var = random.randrange(1, 4)
        size = random.uniform(1.0, 1.7)
    fixed:
        pos (position[0]+x_var, position[1]+y_var)
        xsize 1 ysize 1
        add "crit_{}_animation".format(var) anchor (0.5, 0.99) zoom (size)
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

image impact_1_animation:
    Transform("images/animations/impact_1.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_1.png", crop=(1200,1200,300,300))
    pause 0.016
image impact_2_animation:
    Transform("images/animations/impact_2.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_2.png", crop=(1200,1200,300,300))
    pause 0.016
image impact_3_animation:
    Transform("images/animations/impact_3.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/impact_3.png", crop=(1200,1200,300,300))
    pause 0.016

image crit_1_animation:
    Transform("images/animations/crit_1.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_1.png", crop=(1200,1200,300,300))
    pause 0.016
image crit_2_animation:
    Transform("images/animations/crit_2.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_2.png", crop=(1200,1200,300,300))
    pause 0.016
image crit_3_animation:
    Transform("images/animations/crit_3.png", crop=(0,0,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(300,0,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(600,0,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(900,0,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(1200,0,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(0,300,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(300,300,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(600,300,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(900,300,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(1200,300,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(0,600,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(300,600,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(600,600,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(900,600,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(1200,600,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(0,900,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(300,900,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(600,900,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(900,900,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(1200,900,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(0,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(300,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(600,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(900,1200,300,300))
    pause 0.016
    Transform("images/animations/crit_3.png", crop=(1200,1200,300,300))
    pause 0.016