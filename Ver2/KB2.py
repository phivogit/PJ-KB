from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from sys import exit as end
from os import system
import keyboard
import time
from MarkovChainP2 import *

class VKeyboard:
    def __init__(self, root=Tk()):
        self.dataFilePath = "userdata.txt"
        self.darkpurple = "#7151c4"
        self.purple = "#9369ff"
        self.darkblue = '#000d74'
        self.black = '#000000'
        self.blue = "#488bf0"
        self.darkyellow = "#bfb967"
        self.yellow = "#ebe481"
        self.darkred = "#591717"
        self.red = "#822626"
        self.bgColor = '#dfe29e'
        self.suggestionsColor1 = '#dfffbd' 
        self.suggestionsColor2 = '#f2bdff'
        self.sgColorN = "#90b859"
        self.sgColorM = "#7ab824"
        self.sgColorD = "#545454"
        self.root = root
        self.root.configure(bg=self.bgColor)
        self.unmap_bind = self.root.bind("<Unmap>", lambda e: [self.rel_win(), self.rel_alts(), self.rel_shifts(), self.rel_ctrls()])
        # makes sure shift/ctrl/alt/win keys aren't pressed down after keyboard closed
        self.root.protocol("WM_DELETE_WINDOW", lambda: [self.root.destroy(), end()])
        self.keylabelpadding = 6
        self.user_scr_width = int(self.root.winfo_screenwidth())
        self.user_scr_height = int(self.root.winfo_screenheight())

        self.trans_value = 1
        self.root.attributes('-alpha', self.trans_value)
        self.root.attributes('-topmost', True)

        self.size_value_map = [
            (int(0.63 * self.user_scr_width), int(0.37 * self.user_scr_height)),
            (int(0.70 * self.user_scr_width), int(0.42 * self.user_scr_height)),
            (int(0.78 * self.user_scr_width), int(0.46 * self.user_scr_height)),
            (int(0.86 * self.user_scr_width), int(0.51 * self.user_scr_height)),
            (int(0.94 * self.user_scr_width), int(0.56 * self.user_scr_height))
        ]
        self.size_value_names = ["Very Small", "Small", "Medium", "Large", "Very Large"]

        self.size_current = 3
        
        # open keyboard in medium size by default (not resizable)
        self.root.geometry(f"{self.size_value_map[self.size_current][0]}x{self.size_value_map[self.size_current][1]}")
        self.root.resizable(False, False)
        # keys in every row
        self.row2keys = ["esc", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
                         "f11", "f12", "print_screen", "scroll_lock", "numlock"]

        self.row3keys = ["`", "1", "2", "3", "4", "5", "6", "7",
                         "8", "9", "0", "-", "=", "backspace", "page_up"]

        self.row4keys = ["tab", "q", "w", "e", "r", "t", "y", 'u',
                         'i', 'o', 'p', '[', ']', 'enter', 'page_down']

        self.row5keys = ["capslock", 'a', 's', 'd', 'f', 'g', 'h', 'j',
                         'k', 'l', ';', "'", '\\', 'delete', 'home', 'end']

        self.row6keys = ["left shift", 'z', 'x', 'c', 'v', 'b', 'n', 'm',
                         ',', '.', '/', 'right shift', 'up', 'insert']

        self.row7keys = ["left ctrl", 'win', 'alt', 'spacebar', 'alt gr',
                         'right ctrl', 'left', 'down', 'right']

        # buttons for each row
        self.row2buttons = []
        self.row3buttons = []
        self.row4buttons = []
        self.row5buttons = []
        self.row6buttons = []
        self.row7buttons = []

        # Append function (to append the buttons into each row)
        appendrow2 = self.row2buttons.append
        appendrow3 = self.row3buttons.append
        appendrow4 = self.row4buttons.append
        appendrow5 = self.row5buttons.append
        appendrow6 = self.row6buttons.append
        appendrow7 = self.row7buttons.append

        # prevents frames having inconsistent relative dimensions
        self.root.columnconfigure(0, weight=1)
        for i in range(7):
            self.root.rowconfigure(i, weight=1)

        # Create fonts acc to resolution
        if self.user_scr_width < 1600:
            self.textfont = font.Font(family="Calibri", size=13, weight='normal')
            self.keyfont = font.Font(family="Calibri", size=10, weight='bold')
            self.bottomfont = font.Font(family='Calibri', size=9, weight='bold')
            self.neetfont = font.Font(family='Lucida Handwriting', size=7, weight='normal')
        else:
            self.textfont = font.Font(family="Calibri", size=15, weight='normal')
            self.keyfont = font.Font(family="Calibri", size=12, weight='bold')
            self.bottomfont = font.Font(family='Calibri', size=10, weight='bold')
            self.neetfont = font.Font(family='Lucida Handwriting', size=9, weight='normal')

        # spl_key_pressed is True if ALT, CTRL, SHIFT or WIN are held down using right click
        # if it is False, the 4 mentioned keys get released on clicking any other key
        self.spl_key_pressed = False
        
        #   ROW 0 - Display pending text
        keyframetext = Frame(self.root, borderwidth=5, bg=self.bgColor)
        keyframetext.rowconfigure(0, weight=1)
        keyframetext.columnconfigure(0, weight=6)
        keyframetext.columnconfigure(1, weight=2)
        self.sendButton = Button(keyframetext, text = 'SEND', command= self.send_text)
        self.sendButton.grid(row=0, column=1, sticky="nsew")
        self.textbox = Text(keyframetext, font=self.textfont, wrap="word", height=3)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        keyframetext.grid(row=0, column=0, columnspan=8, sticky="nsew")
        self.endingChar = ['.', '?', '!', ';']
        for char in self.endingChar:
            self.textbox.bind(char, self.updateUserPreference)
            
        #   ROW 1
        frameSuggestions = Frame(self.root, borderwidth = 1, bg = self.suggestionsColor1)
        frameSuggestions.rowconfigure(0, weight = 1)
        frameSuggestions.columnconfigure(0, weight = 1)
        frameSuggestions.rowconfigure(0, weight=1)
        for i in range(3):
            frameSuggestions.columnconfigure(i, weight=1)
        self.suggestionHeight = 3
        self.suggestion1 = Button(frameSuggestions, state="disabled", bg = self.sgColorD, text = ' ', height = self.suggestionHeight)
        self.suggestion2 = Button(frameSuggestions, state="disabled", bg = self.sgColorD, text = ' ', height = self.suggestionHeight)
        self.suggestion3 = Button(frameSuggestions, state="disabled", bg = self.sgColorD, text = ' ', height = self.suggestionHeight)
        
        self.suggestion1.grid(row = 0, column = 0, sticky = 'nsew')
        self.suggestion2.grid(row = 0, column = 1, sticky = 'nsew')
        self.suggestion3.grid(row = 0, column = 2, sticky = 'nsew')
        
        frameSuggestions.grid(row = 1, column = 0, columnspan = 12, sticky = 'nsew')
        
        #   ROW 2

        # create a frame for row2buttons
        keyframe1 = Frame(self.root, height=1)
        keyframe1.rowconfigure(0, weight=1)

        # create row2buttons
        for key in self.row2keys:
            ind = self.row2keys.index(key)
            keyframe1.columnconfigure(ind, weight=1)
            appendrow2(Button(
                keyframe1,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=1,
                relief=RAISED
            ))
            if key == "print_screen":
                self.row2buttons[ind].config(text="PrtScr", width=3, height=2)
            elif key == "scroll_lock":
                self.row2buttons[ind].config(text="ScrLck", width=3)
            elif key == "numlock":
                self.row2buttons[ind].config(text="NumLck", width=3)
            else:
                self.row2buttons[ind].config(text=key.title())

            self.row2buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        #   ROW 3   #

        # create a frame for row3buttons
        keyframe2 = Frame(self.root, height=1)
        keyframe2.rowconfigure(0, weight=1)

        # create row3buttons
        for key in self.row3keys:
            ind = self.row3keys.index(key)
            if ind == 13:
                keyframe2.columnconfigure(ind, weight=2)
            else:
                keyframe2.columnconfigure(ind, weight=1)
            appendrow3(Button(
                keyframe2,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=1,
                relief=RAISED
            ))
            if key == "page_up":
                self.row3buttons[ind].config(text="Pg Up", width=2)
            elif key == "backspace":
                self.row3buttons[ind].config(text=key.title(), width=4)

            self.row3buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        self.row3buttons[0].config(text="~\n`", height = 2)
        self.row3buttons[1].config(text="!\n1", pady = self.keylabelpadding)
        self.row3buttons[2].config(text="@\n2", pady = self.keylabelpadding)
        self.row3buttons[3].config(text="#\n3", pady = self.keylabelpadding)
        self.row3buttons[4].config(text="$\n4", pady = self.keylabelpadding)
        self.row3buttons[5].config(text="%\n5", pady = self.keylabelpadding)
        self.row3buttons[6].config(text="^\n6", pady = self.keylabelpadding)
        self.row3buttons[7].config(text="&\n7", pady = self.keylabelpadding)
        self.row3buttons[8].config(text="*\n8", pady = self.keylabelpadding)
        self.row3buttons[9].config(text="(\n9", pady = self.keylabelpadding)
        self.row3buttons[10].config(text=")\n0", pady = self.keylabelpadding)
        self.row3buttons[11].config(text="_\n-", pady = self.keylabelpadding)
        self.row3buttons[12].config(text="+\n=", pady = self.keylabelpadding)

        #   ROW 4   #

        # create a frame for row4buttons
        keyframe3 = Frame(self.root, width=1)
        keyframe3.rowconfigure(0, weight=1)

        # create row4buttons
        for key in self.row4keys:
            ind = self.row4keys.index(key)
            if ind == 13:
                keyframe3.columnconfigure(ind, weight=2)
            else:
                keyframe3.columnconfigure(ind, weight=1)
            appendrow4(Button(
                keyframe3,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=1,
                relief=RAISED
            ))
            if key == "page_down":
                self.row4buttons[ind].config(text="Pg Dn", width=2)
            elif key == "[":
                self.row4buttons[ind].config(text="{ ` [", width=1)
            elif key == "]":
                self.row4buttons[ind].config(text="} ` ]", width=1, height = 2)
            elif key == "tab":
                self.row4buttons[ind].config(text="Tab", width=3)
            elif key == "enter":
                self.row4buttons[ind].config(text="Enter", width=3)
            else:
                self.row4buttons[ind].config(text=key.title())

            self.row4buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        #   ROW 5   #

        # create a frame for row5buttons
        keyframe4 = Frame(self.root, height=1)
        keyframe4.rowconfigure(0, weight=1)

        # create row5buttons
        for key in self.row5keys:
            ind = self.row5keys.index(key)
            keyframe4.columnconfigure(ind, weight=1)
            appendrow5(Button(
                keyframe4,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=2,
                relief=RAISED
            ))
            if key == ";":
                self.row5buttons[ind].config(text=": ` ;", height = 2)
            elif key == "'":
                self.row5buttons[ind].config(text='" ` \'')
            elif key == "\\":
                self.row5buttons[ind].config(text="| ` \\")
            elif key == "capslock":
                self.row5buttons[ind].config(text="CapsLck", width=5)
            else:
                self.row5buttons[ind].config(text=key.title())

            self.row5buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        #   ROW 6   #

        # create a frame for row6buttons
        keyframe5 = Frame(self.root, height=1)
        keyframe5.rowconfigure(0, weight=1)

        # create row6buttons
        for key in self.row6keys:
            ind = self.row6keys.index(key)
            if ind == 0 or ind == 11:
                keyframe5.columnconfigure(ind, weight=3)
            else:
                keyframe5.columnconfigure(ind, weight=1)
            appendrow6(Button(
                keyframe5,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=1,
                relief=RAISED
            ))
            if key == ",":
                self.row6buttons[ind].config(text="< ` ,", height = 2)
            elif key == ".":
                self.row6buttons[ind].config(text="> ` .")
            elif key == "/":
                self.row6buttons[ind].config(text="? ` /")
            elif key == "up":
                self.row6buttons[ind].config(text="↑")
            elif key == "insert":
                self.row6buttons[ind].config(text="Insert", width=1)
            elif key == "left shift":
                self.row6buttons[ind].config(text="Shift", width=6)
            elif key == "right shift":
                self.row6buttons[ind].config(text="Shift", width=6)
            else:
                self.row6buttons[ind].config(text=key.title())

            self.row6buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        #   ROW 7   #

        # create a frame for row7buttons
        keyframe6 = Frame(self.root, height=1)
        keyframe6.rowconfigure(0, weight=1)

        # create row7buttons
        for key in self.row7keys:
            ind = self.row7keys.index(key)
            if ind == 3:
                keyframe6.columnconfigure(ind, weight=12)
            else:
                keyframe6.columnconfigure(ind, weight=1)
            appendrow7(Button(
                keyframe6,
                font=self.keyfont,
                border=5,
                bg=self.black,
                activebackground=self.darkblue,
                activeforeground="#bababa",
                fg="white",
                width=1,
                relief=RAISED
            ))

            if key == "left":
                self.row7buttons[ind].config(text="←")
            elif key == "down":
                self.row7buttons[ind].config(text="↓")
            elif key == "right":
                self.row7buttons[ind].config(text="→")
            elif key == "spacebar":
                self.row7buttons[ind].config(text="\n")
            elif key == "win":
                self.row7buttons[ind].config(text="Win")
            elif key == "left ctrl":
                self.row7buttons[ind].config(text="Ctrl")
            elif key == "right ctrl":
                self.row7buttons[ind].config(text="Ctrl")
            elif key == "alt":
                self.row7buttons[ind].config(text="Alt")
            elif key == "alt gr":
                self.row7buttons[ind].config(text="Alt")
            else:
                self.row7buttons[ind].config(text=key.title())

            self.row7buttons[ind].grid(row=0, column=ind, sticky="NSEW")

        # create final frame 7 for custom keys
        infoframe7 = Frame(self.root, height=1, bg=self.black)
        infoframe7.rowconfigure(0, weight=1)

        #empty space
        infoframe7.columnconfigure(0, weight=1)
        self.tips_space = Button(infoframe7, text="buttons :)", bg=self.black, relief=FLAT, disabledforeground="white", font=self.bottomfont, state=DISABLED, height=1)
        self.tips_space.grid(row=0, column=0, sticky="NSEW")

        # copy button
        infoframe7.columnconfigure(2, weight=1)
        self.copy_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.purple,
            text="COPY",
            activebackground=self.darkpurple,
            activeforeground="black",
            fg="black",
            relief=RAISED
        )
        self.copy_button.grid(row=0, column=2, padx=2, sticky="NSEW")

        # cut button
        infoframe7.columnconfigure(3, weight=1)
        self.cut_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.purple,
            text="CUT",
            activebackground=self.darkpurple,
            activeforeground="black",
            fg="black",
            relief=RAISED
        )
        self.cut_button.grid(row=0, column=3, padx=2, sticky="NSEW")

        # paste button
        infoframe7.columnconfigure(4, weight=1)
        self.paste_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.purple,
            text="PASTE",
            activebackground=self.darkpurple,
            activeforeground="black",
            fg="black",
            relief=RAISED
        )
        self.paste_button.grid(row=0, column=4, padx=2, sticky="NSEW")

        # select all button
        infoframe7.columnconfigure(5, weight=1)
        self.selall_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.purple,
            text="SELECT ALL",
            activebackground=self.darkpurple,
            activeforeground="black",
            fg="black",
            relief=RAISED
        )
        self.selall_button.grid(row=0, column=5, padx=2, sticky="NSEW")

        # task manager button
        infoframe7.columnconfigure(7, weight=1)
        self.taskmnger_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.blue,
            text="Task Manager",
            activebackground=self.darkblue,
            activeforeground="black",
            fg="black",
            relief=RAISED
        )
        self.taskmnger_button.grid(row=0, column=7, padx=2, sticky="NSEW")

        # pin keyboard button
        infoframe7.columnconfigure(8, weight=1)
        self.pinkb_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.darkblue,
            text="Unpin Keyboard 📌",
            activebackground=self.blue,
            activeforeground="black",
            fg="black",
            width=15,
            relief=SUNKEN,
            command=self.keyboard_top)
        self.pinkb_button.grid(row=0, column=8, padx=2, sticky="NSEW")

        infoframe7.columnconfigure(11, weight=1)
        self.settings_button = Button(
            infoframe7,
            font=self.bottomfont,
            border=5,
            bg=self.yellow,
            text="Keyboard Settings",
            activebackground=self.darkyellow,
            activeforeground="black",
            fg="black",
            relief=RAISED,
            command=self.kb_settings
        )
        self.settings_button.grid(row=0, column=11, padx=2, sticky="NSEW")

        keyframe1.grid(row=2, sticky="NSEW", padx=9, pady=5)
        keyframe2.grid(row=3, sticky="NSEW", padx=9)
        keyframe3.grid(row=4, sticky="NSEW", padx=9)
        keyframe4.grid(row=5, sticky="NSEW", padx=9)
        keyframe5.grid(row=6, sticky="NSEW", padx=9)
        keyframe6.grid(row=7, padx=9, sticky="NSEW")
        infoframe7.grid(row=8, padx=9, pady=5, sticky="NSEW")

    # an exception to get the symbols ? and _ from the keyboard module's virtual hotkeys
    # "SHIFT+-" or "SHIFT+/" don't work :/
    def send_text(self):
        self.root.withdraw()
        time.sleep(0.1)
        self.root.after(1, keyboard.write(self.textbox.get(1.0, "end-1c")))
        self.root.after(5, self.root.wm_deiconify())
        
    def quest_press(self, x):
        if self.row6buttons[0].cget('relief') == SUNKEN:
            if x == "-":
                self.vpresskey("shift+_")
            elif x == "/":
                self.vpresskey("shift+?")
        else:
            self.vpresskey(x)

        if self.spl_key_pressed:
            keyboard.press('shift')

    def rel_shifts(self):
        keyboard.release('shift')

        self.row6buttons[0].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )
        self.row6buttons[11].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )

    def prs_shifts(self):
        keyboard.press('shift')

        self.row6buttons[0].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")
        self.row6buttons[11].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")

    def rel_ctrls(self):
        keyboard.release('ctrl')

        self.row7buttons[0].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )
        self.row7buttons[5].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )

    def prs_ctrls(self):
        keyboard.press('ctrl')

        self.row7buttons[0].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")
        self.row7buttons[5].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")

    def rel_alts(self):
        keyboard.release('alt')

        self.row7buttons[2].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )
        self.row7buttons[4].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )

    def prs_alts(self):
        keyboard.press('alt')

        self.row7buttons[2].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")
        self.row7buttons[4].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")

    # release win key
    def rel_win(self):
        keyboard.release('win')

        self.row7buttons[1].config(
            relief=RAISED,
            bg=self.black,
            activebackground=self.darkblue,
            activeforeground="#bababa",
            fg="white"
        )

    # press win key
    def prs_win(self):
        keyboard.press('win')

        self.row7buttons[1].config(
            relief=SUNKEN,
            activebackground=self.black,
            bg=self.darkblue,
            fg="#bababa",
            activeforeground="white")
    ## ------------------------------------------------------------------------------------------------
    def updateUserPreference(self, event = None):
        '''Upload the last sentence to markov chain preference file'''
        self.prefFile = open(self.dataFilePath, "a")
        self.lastSentence = self.getLastSentence()
        print(f"Last sentence: {self.lastSentence}")
        if len(self.lastSentence) < 3:
            pass
        else:
            self.upl = self.removeDupPeriods(' '.join(self.lastSentence))
            print(f"Uploaded sentence: {self.upl}")
            self.prefFile.write("\n" + self.upl)
    def removeDupPeriods(self, text):
        '''Remove duplicated periods from provided text'''
        result = []
        dot_seen = False
        for char in text:
            if char == '.':
                if not dot_seen:
                    result.append(char)
                    dot_seen = True
            else:
                result.append(char)
                dot_seen = False
        return ''.join(result)

    def getLastSentence(self):
        '''Return the last sentence as a list. Use this when the last character is a period (.)'''
        self.text = self.textbox.get(1.0, "end-1c").rstrip() + '.'
        if self.text.count('.') == 1:
            self.splitText = self.text.split()
            self.retVal = []
            # Remove all extra spaces 
            for self.i in self.splitText:
                if self.i == '':
                    pass
                else:
                    self.retVal.append(self.i)
            return self.retVal
        else:
            # Retrieve the last sentence and turn it into a list
            self.croppedText = self.text[self.text[0:-1].rfind('.')+1:] + '.'
            self.splitText = self.croppedText.split()
            self.retVal = []
            # Remove all extra spaces
            for self.i in self.splitText:
                if self.i == '':
                    pass
                else:
                    self.retVal.append(self.i)
            return self.retVal
            
    def doNothing(self):
        '''do nothing'''
        pass
    
    def clearSG(self):
        '''Clear The suggestions from the buttons. Takes no parameter'''
        self.suggestion1.configure(text = '', bg=self.sgColorD, command = self.doNothing, state="disabled")
        self.suggestion2.configure(text = '', bg=self.sgColorD, command = self.doNothing, state="disabled")
        self.suggestion3.configure(text = '', bg=self.sgColorD, command = self.doNothing, state="disabled")
    
    def removePrevSentence(self, str):
        '''Remove the previous sentence (using the last 3 indexes of the tuple)
        Returns a string'''
        if str.find('.') == -1:
            return str
        else:
            return str[str.rfind('.')+1:].strip()
            

    def getSG(self, lastSG = ''):
        '''Return the suggestions list. Example: ['am', 'living', 'study']'''
        print(f"LastSG: {lastSG}")
        self.content = self.textbox.get(1.0, "end-1c").rstrip() + ' ' + lastSG 
        self.content = self.removePrevSentence(self.content)
        print(f"Evaluating content: {self.content}")
        self.suggestions = getNextWords(self.dataFilePath, self.content.lower().rstrip(), 3)
        print(f"self.suggestions = {self.suggestions}")
        return self.suggestions
    
    def updateSGButton(self, sglist):
        '''Update the suggestion buttons label'''
        if sglist == None or len(sglist) < 1 or sglist[0] == "END":
            self.clearSG()
        else:
            self.clearSG()
            match len(sglist):
                case 1:
                    self.suggestion2.configure(text = self.suggestions[0], state="normal", bg = self.sgColorM, command = lambda sgt = self.suggestions[0]: self.sendSG(sgt))
                case 2:
                    self.suggestion1.configure(text = self.suggestions[0], state="normal", bg = self.sgColorN, command = lambda sgt = self.suggestions[0]: self.sendSG(sgt))
                    self.suggestion2.configure(text = self.suggestions[1], state="normal", bg = self.sgColorM, command = lambda sgt = self.suggestions[1]: self.sendSG(sgt))
                case 3:
                    self.suggestion1.configure(text = self.suggestions[0], state="normal", bg = self.sgColorN, command = lambda sgt = self.suggestions[0]: self.sendSG(sgt))
                    self.suggestion2.configure(text = self.suggestions[1], state="normal", bg = self.sgColorM, command = lambda sgt = self.suggestions[1]: self.sendSG(sgt))
                    self.suggestion3.configure(text = self.suggestions[2], state="normal", bg = self.sgColorN, command = lambda sgt = self.suggestions[2]: self.sendSG(sgt))
                case _:
                    self.suggestion1.configure(text = self.suggestions[0], state="normal", bg = self.sgColorN, command = lambda sgt = self.suggestions[0]: self.sendSG(sgt))
                    self.suggestion2.configure(text = self.suggestions[1], state="normal", bg = self.sgColorM, command = lambda sgt = self.suggestions[1]: self.sendSG(sgt))
                    self.suggestion3.configure(text = self.suggestions[2], state="normal", bg = self.sgColorN, command = lambda sgt = self.suggestions[2]: self.sendSG(sgt))
    def sendSG(self, sgst):
        '''Send the suggestion into the text box'''
        self.textbox.focus_set()
        keyboard.write(f"{sgst} ")
        self.updateSGButton(self.getSG(sgst))
    ##-----------------------------------------------------------------------------------------------
    def vpresskey(self, x):
        '''function to press and release keys'''
        self.textbox.focus_set()
        keyboard.send(x)
        
        # Update Markov Suggestions
        if x == "spacebar":
            self.updateSGButton(self.getSG())
        else:
            self.clearSG()
                    
        if not self.spl_key_pressed:
            self.rel_shifts()
            self.rel_ctrls()
            self.rel_alts()
            self.rel_win()

        if self.pinkb_button.cget('relief') == RAISED:
            self.addkbtotop()
        self.unmap_bind = self.root.bind("<Unmap>", lambda e: [self.rel_win(), self.rel_alts(), self.rel_shifts(), self.rel_ctrls()])

    # function to hold SHIFT, CTRL, ALT or WIN keys
    def vupdownkey(self, event, y, a):
        if y == "shift":
            if self.row6buttons[0].cget('relief') == SUNKEN or self.row6buttons[11].cget('relief') == SUNKEN:
                self.rel_shifts()
            else:
                self.prs_shifts()

        elif y == "ctrl":
            if self.row7buttons[0].cget('relief') == SUNKEN or self.row7buttons[5].cget('relief') == SUNKEN:
                self.rel_ctrls()
            else:
                self.prs_ctrls()

        elif y == "alt":
            if self.row7buttons[2].cget('relief') == SUNKEN or self.row7buttons[4].cget('relief') == SUNKEN:
                self.rel_alts()
            else:
                self.prs_alts()

        elif y == "win":
            if self.row7buttons[1].cget('relief') == SUNKEN:
                self.rel_win()
            else:
                self.prs_win()

        if a == "L":
            self.spl_key_pressed = False
            # presses shift, alt, ctrl or win temporarily until remaining keys pressed
        elif a == "R":
            self.spl_key_pressed = True
            # holds down shift, alt, ctrl or win

    def inc_size(self):
        if 0 <= self.size_current < 4:
            self.size_current += 1
            new_width = self.size_value_map[self.size_current][0]
            new_height = self.size_value_map[self.size_current][1]

            self.root.geometry(f"{new_width}x{new_height}")
            self.root.update()
        else:
            pass

    def dec_size(self):
        if 0 < self.size_current <= 4:
            self.size_current -= 1
            new_width = self.size_value_map[self.size_current][0]
            new_height = self.size_value_map[self.size_current][1]

            self.root.geometry(f"{new_width}x{new_height}")
            self.root.update()
        else:
            pass

    def inc_trans(self):
        if 0.3 < self.trans_value <= 1.0:
            self.trans_value -= 0.1
            floatsubtractionsbelike = float(str(self.trans_value)[:3])
            self.trans_value = floatsubtractionsbelike
            self.root.attributes('-alpha', self.trans_value)
            self.root.update()
        else:
            pass

    def dec_trans(self):
        if 0.3 <= self.trans_value < 1.0:
            self.trans_value += 0.100069420
            floatadditionsbelike = float(str(self.trans_value)[:3])
            self.trans_value = floatadditionsbelike
            self.root.attributes('-alpha', self.trans_value)
            self.root.update()
        else:
            pass

    def removekbfromtop(self):
        self.root.attributes('-topmost', False)
        self.pinkb_button.config(bg=self.blue, activebackground=self.darkblue, relief=RAISED, text="Pin Keyboard 📌")
        self.root.update()

    # enable the option to keep keyboard on top
    def addkbtotop(self):
        self.root.attributes('-topmost', True)
        self.pinkb_button.config(relief=SUNKEN, bg=self.darkblue, activebackground=self.blue, text="Unpin Keyboard 📌")
        self.root.update()

    # Settings window
    def kb_settings(self):
        self.removekbfromtop()
        self.rel_shifts()
        self.rel_alts()
        self.rel_ctrls()
        self.rel_win()

        settings_window = Toplevel()
        settings_window.geometry(f'400x344+{int(self.user_scr_width / 2) - 200}+{int(self.user_scr_height / 2) - 200}')

        settings_window.title("KeyBoard Settings")
        settings_window.resizable(False, False)
        settings_window.config(bg=self.black)
        settings_window.overrideredirect(True)
        settings_window.grab_set()
        settings_window.focus_set()

        # Fonts for settings window
        stitlefont = font.Font(family="Calibri", size=20, weight="bold")
        sfont = font.Font(family="Calibri", size=16, weight="bold")

        mainframe = Frame(settings_window, height=344, width=400, bg=self.black, highlightthickness=2, highlightbackground=self.yellow)

        stitle = Label(mainframe, text="Keyboard Settings", font=stitlefont, bg=self.black, fg=self.yellow)
        stitle.place(anchor=N, x=200, y=20)

        transtitle = Label(mainframe, text="Opacity", font=sfont, bg=self.black, fg=self.blue, anchor=CENTER)
        transtitle.place(anchor=N, x=200, y=100)
        translabel = Label(mainframe, text=str(int(self.trans_value * 100)) + "%", font=sfont, bg=self.black, fg="white")
        translabel.place(anchor=N, x=200, y=140)
        transbuttless = Button(mainframe, text="-", font=stitlefont, bg=self.red, fg="white", command=lambda: [self.inc_trans(), translabel.config(text=(str(int(self.trans_value * 100)) + "%"))])
        transbuttless.place(x=100, y=145, height=20, width=30)
        transbuttmore = Button(mainframe, text="+", font=stitlefont, bg="green", fg="white", command=lambda: [self.dec_trans(), translabel.config(text=(str(int(self.trans_value * 100)) + "%"))])
        transbuttmore.place(x=270, y=145, height=20, width=30)

        sizetitle = Label(mainframe, text="Keyboard Size", font=sfont, bg=self.black, fg=self.blue, anchor=CENTER)
        sizetitle.place(anchor=N, x=200, y=190)
        sizelabel = Label(mainframe, text=self.size_value_names[self.size_current], font=sfont, bg=self.black, fg="white")
        sizelabel.place(anchor=N, x=200, y=230)
        sizebuttless = Button(mainframe, text="-", font=stitlefont, bg=self.red, fg="white", command=lambda: [self.dec_size(), sizelabel.config(text=self.size_value_names[self.size_current])])
        sizebuttless.place(x=100, y=237, height=20, width=30)
        sizebuttmore = Button(mainframe, text="+", font=stitlefont, bg="green", fg="white", command=lambda: [self.inc_size(), sizelabel.config(text=self.size_value_names[self.size_current])])
        sizebuttmore.place(x=270, y=237, height=20, width=30)

        donebutton = Button(mainframe, text="Done", anchor=S, font=stitlefont, bg=self.purple, activebackground=self.darkpurple, fg="black", command=lambda: [settings_window.destroy(), self.root.after(20, self.addkbtotop())])
        donebutton.place(x=155, y=290, height=35, width=90)

        mainframe.place(x=0, y=0)
        settings_window.mainloop()

    # function to check if keyboard on top or not and revert the option
    def keyboard_top(self):
        if self.pinkb_button.cget("relief") == RAISED:
            self.addkbtotop()
        elif self.pinkb_button.cget("relief") == SUNKEN:
            self.removekbfromtop()
        else:
            self.removekbfromtop()

    # start keyboard
    def start(self):
        self.root.mainloop()

    # add functionality to keyboard
    def engine(self):
        self.root.title("PJ-KB")
        self.root.protocol("WM_DELETE_WINDOW", lambda: [keyboard.release('shift'), keyboard.release('ctrl'), keyboard.release('alt'), keyboard.release('win'), self.root.destroy(), end()])
        for key in self.row2keys:
            ind = self.row2keys.index(key)
            self.row2buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row3keys:
            ind = self.row3keys.index(key)
            self.row3buttons[ind].config(command=lambda x=key: self.vpresskey(x))
        self.row3buttons[11].config(command=lambda x='-': self.quest_press(x))

        for key in self.row4keys:
            ind = self.row4keys.index(key)
            self.row4buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row5keys:
            ind = self.row5keys.index(key)
            self.row5buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row6keys:
            ind = self.row6keys.index(key)
            self.row6buttons[ind].config(command=lambda x=key: self.vpresskey(x))
            if key == "/":
                self.row6buttons[ind].config(command=lambda x='/': self.quest_press(x))
            elif key == "left shift":
                self.row6buttons[ind].config(command=lambda: self.vupdownkey(event="<Button-1>", y='shift', a="L"))
                self.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='shift', a="R": self.vupdownkey(event, y, a))
            elif key == "right shift":
                self.row6buttons[ind].config(command=lambda: self.vupdownkey(event="<Button-1>", y='shift', a="L"))
                self.row6buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='shift', a="R": self.vupdownkey(event, y, a))

        for key in self.row7keys:
            ind = self.row7keys.index(key)
            self.row7buttons[ind].config(command=lambda x=key: self.vpresskey(x))
            if key == "win":
                self.row7buttons[ind].config(command=lambda: self.vupdownkey("<Button-1>", 'win', "L"))
                self.row7buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='win', a="R": self.vupdownkey(event, y, a))
            elif key == ":)":
                self.row7buttons[ind].config(command=self.donothing)
            elif key == "left ctrl":
                self.row7buttons[ind].config(command=lambda: self.vupdownkey("<Button-1>", 'ctrl', "L"))
                self.row7buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='ctrl', a="R": self.vupdownkey(event, y, a))
            elif key == "right ctrl":
                self.row7buttons[ind].config(command=lambda: self.vupdownkey("<Button-1>", 'ctrl', "L"))
                self.row7buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='ctrl', a="R": self.vupdownkey(event, y, a))
            elif key == "alt":
                self.row7buttons[ind].config(command=lambda: self.vupdownkey("<Button-1>", 'alt', "L"))
                self.row7buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='alt', a="R": self.vupdownkey(event, y, a))
            elif key == "alt gr":
                self.row7buttons[ind].config(command=lambda: self.vupdownkey("<Button-1>", 'alt', "L"))
                self.row7buttons[ind].bind('<Button-3>', lambda event="<Button-3>", y='alt', a="R": self.vupdownkey(event, y, a))

        self.tips_space.config(text="Right click to hold\nSHIFT, CTRL, ALT or WIN keys", height=2)
        self.copy_button.config(command=lambda: self.vpresskey('ctrl+c'))
        self.cut_button.config(command=lambda: self.vpresskey('ctrl+x'))
        self.paste_button.config(command=lambda: self.vpresskey('ctrl+v'))
        self.selall_button.config(command=lambda: self.vpresskey('ctrl+a'))
        self.taskmnger_button.config(command=lambda: [self.removekbfromtop(), self.vpresskey('ctrl+shift+esc')])


if __name__ == '__main__':
    keyboard1 = VKeyboard()

    keyboard1.engine()

    keyboard1.start()
