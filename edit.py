for key in keyboard1.row5keys:
    ind = keyboard1.row5keys.index(key)
    keyboard1.row5buttons[ind].config(command=lambda x=key: keyboard1.vpresskey(x))
    if key == "/":
        keyboard1.row5buttons[ind].config(command=lambda x='/': keyboard1.quest_press(x))
    elif key == "left shift":
        keyboard1.row5buttons[ind].config(command=lambda: keyboard1.vupdownkey(event="<Button-1>", y='shift', a="L"))
        keyboard1.row5buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='shift', a="R": keyboard1.vupdownkey(event, y, a))
    elif key == "right shift":
        keyboard1.row5buttons[ind].config(command=lambda: keyboard1.vupdownkey(event="<Button-1>", y='shift', a="L"))
        keyboard1.row5buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='shift', a="R": keyboard1.vupdownkey(event, y, a))

for key in keyboard1.row6keys:
    ind = keyboard1.row6keys.index(key)
    keyboard1.row6buttons[ind].config(command=lambda x=key: keyboard1.vpresskey(x))
    if key == "win":
        keyboard1.row6buttons[ind].config(command=lambda: keyboard1.vupdownkey("<Button-1>", 'win', "L"))
        keyboard1.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='win', a="R": keyboard1.vupdownkey(event, y, a))
    elif key == ":)":
        keyboard1.row6buttons[ind].config(command=keyboard1.donothing)
    elif key == "left ctrl":
        keyboard1.row6buttons[ind].config(command=lambda: keyboard1.vupdownkey("<Button-1>", 'ctrl', "L"))
        keyboard1.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='ctrl', a="R": keyboard1.vupdownkey(event, y, a))
    elif key == "right ctrl":
        keyboard1.row6buttons[ind].config(command=lambda: keyboard1.vupdownkey("<Button-1>", 'ctrl', "L"))
        keyboard1.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='ctrl', a="R": keyboard1.vupdownkey(event, y, a))
    elif key == "alt":
        keyboard1.row6buttons[ind].config(command=lambda: keyboard1.vupdownkey("<Button-1>", 'alt', "L"))
        keyboard1.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='alt', a="R": keyboard1.vupdownkey(event, y, a))
    elif key == "alt gr":
        keyboard1.row6buttons[ind].config(command=lambda: keyboard1.vupdownkey("<Button-1>", 'alt', "L"))
        keyboard1.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='alt', a="R": keyboard1.vupdownkey(event, y, a))

keyboard1.tips_space.config(text="Right click to hold\nSHIFT, CTRL, ALT or WIN keys", height=2)
keyboard1.copy_button.config(command=lambda: keyboard1.vpresskey('ctrl+c'))
keyboard1.cut_button.config(command=lambda: keyboard1.vpresskey('ctrl+x'))
keyboard1.paste_button.config(command=lambda: keyboard1.vpresskey('ctrl+v'))
keyboard1.selall_button.config(command=lambda: keyboard1.vpresskey('ctrl+a'))
keyboard1.taskmnger_button.config(command=lambda: [keyboard1.removekbfromtop(), keyboard1.vpresskey('ctrl+shift+esc')])