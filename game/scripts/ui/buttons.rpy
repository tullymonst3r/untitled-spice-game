screen darkWoodBtn(val, returnVal, disabled = False):
    use componentBtn(val, returnVal, disabled, '1')
screen lightWoodBtn(val, returnVal, disabled = False):
    use componentBtn(val, returnVal, disabled, '2')
screen metalBtn(val, returnVal, disabled = False):
    use componentBtn(val, returnVal, disabled, '3')
screen goldBtn(val, returnVal, disabled = False):
    use componentBtn(val, returnVal, disabled, '4')
screen componentBtn(val, returnVal, disabled = False, btnType = '1'):
    fixed:
        xsize 260 ysize 95
        add "btns/btn_dropshadow.png"
        imagebutton:
            idle "btns/btn_{}_{}.png".format(btnType, 'disabled' if disabled else 'idle')
            hover "btns/btn_{}_{}.png".format(btnType, 'disabled' if disabled else 'hover')
            action [Return(returnVal) if disabled == False else NullAction()]
        if val:
            text "{}".format(val) style "itemBtnText" align (0.5, 0.5)
screen regularBtn(val, returnVal, selected = False):
    fixed:
        xsize 259 ysize 101
        imagebutton:
            idle "item_btn{}.png".format('_selected' if selected else '')
            hover "item_btn{}.png".format('_selected' if selected else '_hovered')
            action [Return(returnVal) if selected == False else NullAction()]
        if val:
            text "{}".format(val) style "itemBtnText" align (0.5, 0.5)

screen attackBtn(equipment, returnVal, selected = False):
    fixed:
        xsize 259 ysize 101
        imagebutton:
            idle "item_btn{}.png".format('_selected' if selected else '')
            hover "item_btn{}.png".format('_selected' if selected else '_hovered')
            hovered Show("equipmentTooltip", equipment=equipment)
            unhovered Hide("equipmentTooltip")
            if selected == False:
                action [Hide("equipmentTooltip"), Return(returnVal)]
            else:
                action [Hide("equipmentTooltip"), NullAction()]
        text "{}".format(equipment.name) style "itemBtnText" align (0.5, 0.5)
style itemBtnText:
    size 20
    bold True
    color "#161616"
    outlines [ (1.5, "#ffffff69", absolute(0), absolute(0)) ]