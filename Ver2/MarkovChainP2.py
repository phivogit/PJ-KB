import re
from collections import defaultdict

def getCurrentSentence(text):
    '''Used to get the sentence the user is currently typing. Removes all previous sentences.'''
    splitText = text.split()
    if text == " " or text == "":
        return ""
    elif "." in splitText[-1]:
        return ""
    else:
        return text[text.rfind(".")+1:]

def getNextWords(dataFilePath, sentence, suggestionNum=3):
    # Get the current sentence and its word count
    currentSentence = getCurrentSentence(sentence)
    splitSentence = currentSentence.split()
    wordCount = len(splitSentence)

    # Dictionary to store counts of each possible next word
    transitionCounts = defaultdict(int)
    totalTransitions = 0  # Total number of transitions from the input sentence

    # Open and read the data file
    with open(dataFilePath, "r", encoding = "utf-8") as dataFile:
        for line in dataFile:
            # Extract words, including hyphenated ones
            splitLine = re.findall(r'\b[\w-]+\b', line)  # Modified regex pattern to include hyphenated words
            joinedLine = ' '.join(splitLine)

            # Case 1: Single word input
            if wordCount < 1:
                return []
            elif wordCount == 1:
                # Find all occurrences of the single word
                lastWord = splitSentence[0].lower()
                for i in range(len(splitLine) - 1):
                    if splitLine[i].lower() == lastWord:
                        nextWord = splitLine[i + 1]
                        transitionCounts[nextWord] += 1
                        totalTransitions += 1
                        
            # Case 2: Multi-word input
            else:
                # Find all occurrences of the input sentence
                joinedEvalSentence = ' '.join(splitSentence).lower()
                startIndex = 0
                while True:
                    # Search for the whole phrase in the line
                    startIndex = joinedLine.lower().find(joinedEvalSentence, startIndex)
                    if startIndex == -1:
                        break  # No more occurrences found
                    
                    # Count the number of words before the matched occurrence
                    wordsUpToIndex = joinedLine[:startIndex].split()
                    matchIndex = len(wordsUpToIndex)
                    
                    # Check if there's a next word after the matched occurrence
                    if matchIndex + wordCount < len(splitLine):
                        nextWord = splitLine[matchIndex + wordCount]
                        transitionCounts[nextWord] += 1
                        totalTransitions += 1

                    # Move startIndex forward to search for the next occurrence
                    startIndex += len(joinedEvalSentence)

    # Calculate the probabilities for each possible next word
    nextWordProbabilities = {word: count / totalTransitions for word, count in transitionCounts.items()}

    # Sort the next words by their probability in descending order and limit to `suggestionNum`
    sortedNextWords = sorted(nextWordProbabilities.items(), key=lambda x: x[1], reverse=True)[:suggestionNum]
    
    return [word for word, prob in sortedNextWords]

# Example usage
if __name__ == "__main__":
    print(getNextWords("userdata.txt", "I", 3))
    print(getNextWords("userdata.txt", "I am a ", 5))
    print(getNextWords("userdata.txt", "I am ", 5))
    print(getNextWords("userdata.txt", " ", 5))
    print(getNextWords("userdata.txt", "", 5))
    print(getNextWords("userdata.txt", "I am a dragon. I", 5))
    