from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from sys import exit as end
from os import system
from tkinter import ttk
import keyboard
import time

#Functions
def printletter(letter):
    root.withdraw()
    time.sleep(0.1)
    keyboard.write(letter)
    root.deiconify()
    root.attributes('-topmost', True)
    
def holdKey(key):
    pass
    
    
# Create Keyboard
root = Tk()
root.title("Bucket Keyboard")
keyboardFrame = ttk.Frame(root, padding = "2")
keyboardFrame.grid(row=1,column=0)
MCFrame = ttk.Frame(keyboardFrame, padding = '2')
MCFrame.grid(row=0,column=0)
root.attributes('-topmost', True)
root.deiconify() 

KeyList = {
    '2': ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace'],
    '3': ['tab', 'Q', 'U', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\', 'enter'],
    '4': ['capslock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'delete'],
    '5': ["left shift", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'up'],
    '6': ["left ctrl", 'win', 'alt', 'spacebar', 'alt gr', 'right ctrl', 'left', 'down', 'right']
}

for krow, kletters in KeyList.items():
    currentRow = int(krow)
    currentColumn = 0
    for letter in kletters:
        if letter is CHAR:
            ttk.Button(keyboardFrame, text=letter.upper(), command=lambda l=letter: printletter(l)).grid(row=currentRow, column=currentColumn)
        else:
            ttk.Button(keyboardFrame, text=letter.upper(), command=lambda l=letter: printletter(l)).grid(row=currentRow, column=currentColumn)
        currentColumn+=1
ttk.Button(keyboardFrame, text=" ", command=lambda: printletter(' ')).grid(row=4, column=5)

#Variables
user_scr_width = int(winfo_screenwidth())
user_scr_height = int(winfo_screenheight())
size_value_map = [
            (int(0.63 * user_scr_width), int(0.37 * user_scr_height)),
            (int(0.70 * user_scr_width), int(0.42 * user_scr_height)),
            (int(0.78 * user_scr_width), int(0.46 * user_scr_height)),
            (int(0.86 * user_scr_width), int(0.51 * user_scr_height)),
            (int(0.94 * user_scr_width), int(0.56 * user_scr_height))
        ]


# Modify Keyboard

root.geometry(f"{size_value_map[size_current][0]}x{size_value_map[size_current][1]}")
root.resizable(False, False)
root.mainloop()


