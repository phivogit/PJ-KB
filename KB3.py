import pyautogui
from tkinter import *
import tkinter.font as font

class VirtualKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Keyboard")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.geometry("600x300")  # Initial window size

        # Create a frame for the keyboard
        self.keyboard_frame = Frame(self.root, bg="lightgrey")
        self.keyboard_frame.pack(expand=True, fill=BOTH)

        # Define the layout of the keyboard
        self.create_keys()

    def create_keys(self):
        # Define the layout of keys in rows
        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        # Add keys to the keyboard
        for i, row in enumerate(rows):
            for j, key in enumerate(row):
                button = Button(self.keyboard_frame, text=key, width=5, height=2,
                                command=lambda k=key: self.press_key(k))
                button.grid(row=i, column=j, padx=1, pady=1)

        # Add space bar
        space_button = Button(self.keyboard_frame, text="Space", width=20, height=2,
                              command=lambda: self.press_key(' '))
        space_button.grid(row=len(rows), column=0, columnspan=len(rows[0]), padx=1, pady=1)

    def press_key(self, key):
        try:
            pyautogui.press(key.lower())  # Simulate key press
        except Exception as e:
            print(f"Error: {e}")

# Create the root window
root = Tk()

# Create and run the virtual keyboard
keyboard = VirtualKeyboard(root)

# Start the Tkinter event loop
root.mainloop()
