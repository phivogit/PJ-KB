trainData = 'MarkovChain\\markov_chain.txt'
from MarkovChain.markov_chain import *
text = "I am"
tkns = text.split()
if(len(tkns) < 2):  #only first space encountered yet
    last_suggestion = next_word(tkns[0].lower())
    print(last_suggestion, end='  ', flush=True)
else: #send a tuple
    last_suggestion = next_word((tkns[-2].lower(), tkns[-1].lower()))
    print(last_suggestion, end='  ', flush=True)