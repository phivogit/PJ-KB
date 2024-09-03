text = "This is the last day on Earth. What are you doing."
if text.count('.') == 1:
    splitText = text.split()
    retVal = []
    # Remove all extra spaces 
    for i in splitText:
        if i == '':
            pass
        else:
            retVal.append(i)
    print(retVal)
else:
    # Retrieve the last sentence and turn it into a list
    croppedText = text[text[0:-1].rfind('.')+1:] + '.'
    splitText = croppedText.split()
    retVal = []
    # Remove all extra spaces
    for i in splitText:
        if i == '':
            pass
        else:
            retVal.append(i)
    print(retVal)