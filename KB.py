from tkinter import *
from tkinter import ttk
train_data = 'Next-Word-Prediction\\markov_chain.txt'

root = Tk()
root.title("Bucket Keyboard")
keyboardFrame = ttk.Frame(root, padding = "2")
keyboardFrame.grid(row=0,column=0)

storedLetter = []
def printletter(letter):
    if str(letter) != ' ':
        storedLetter.append(letter)
    else:
        print(''.join(storedLetter))
        storedLetter.clear()
letterlist1 = ['Q', 'U', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
letterlist2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
letterlist3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
currentColumn = 0
for letter in letterlist1:
    ttk.Button(keyboardFrame, text=letter, command=lambda: printletter(letter)).grid(row=1, column=currentColumn)
    currentColumn +=1
currentColumn = 0
for letter in letterlist2:
    ttk.Button(keyboardFrame, text=letter, command=lambda: printletter(letter)).grid(row=2, column=currentColumn)
    currentColumn +=1
currentColumn = 0
for letter in letterlist3:
    ttk.Button(keyboardFrame, text=letter, command=lambda: printletter(letter)).grid(row=3, column=currentColumn)
    currentColumn +=1
ttk.Button(keyboardFrame, text=" ", command=lambda: printletter(' ')).grid(row=4, column=5)


root.mainloop()


