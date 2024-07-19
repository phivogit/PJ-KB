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
letterList = {
    'first': ['Q', 'U', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    'second': ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    'third': ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
}

for krow, kletters in letterList.items():
    if str(krow) == 'first':
        currentRow = 1
    elif str(krow) == 'second':
        currentRow = 2
    elif str(krow) == 'third':
        currentRow = 3
    currentColumn = 0
    for letter in kletters:
        ttk.Button(keyboardFrame, text=letter, command=lambda: printletter(letter)).grid(row=currentRow, column=currentColumn)
        currentColumn+=1
ttk.Button(keyboardFrame, text=" ", command=lambda: printletter(' ')).grid(row=4, column=5)


root.mainloop()


