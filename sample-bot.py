# sample-bot.py

# sample bot to play wordle. see wordle.py for how to play.

import random

g_wordlist = None
def get_wordlist():
    global g_wordlist
    if None == g_wordlist:
        g_wordlist = []
        for i in open('wordlist.txt').readlines():
            i = i[:-1]
            g_wordlist.append(i)
    return g_wordlist

def ch2Ind(ch):
    return ord(ch) - 97
def ind2Ch(i):
    return chr(i + 97)

def getFeedbackBeta(guess, answer):
    s = guess + ':'
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            s += '3'
        elif ch in answer:
            s += '2'
        else:
            s += '1'
    return s

def getFeedback(guess, answer):
    # set up feedback var, result to be returned
    feedback = guess + ':'

    # initialize reps of answer and feedback
    feedbackRep = [0] * 5
    answerRep = list(answer)

    # check for perfect matches
    for i, ch in enumerate(guess):
        if ch == answer[i]:
            feedbackRep[i] = '3'
            answerRep[i] = 0

    # modify the rest of feedbackRep
    for i, ch in enumerate(guess):
        if feedbackRep[i] != '3':
            if answerRep.count(ch):
                feedbackRep[i] = '2'
                answerRep[answerRep.index(ch)] = 0
            else: 
                feedbackRep[i] = '1'

    return feedback + "".join(feedbackRep)


        


# this has lots of false positives, only pay attention to 3s
#
def could_match(target, guess, feedback):
    for i, ch in enumerate(feedback):
        if '3' == ch:
            if target[i] != guess[i]:
                return False
        else:
            if target[i] == guess[i]:
                return False
    return True

def findChars(c, s):
    start = 0
    out = []
    i = s.find(c, start)
    while(i != -1):
        out.append(i)
        i = s.find(c, start)
    return out

# Alternate method, instead of iterating through points in word, iterate through letters
# need to clean bad letters after iterating, 
def getInfo(state):    
    badLetters = [0] * 26
    goodLetters = dict()

    def add2Good(key, pos, val):
        if key not in goodLetters:
            goodLetters[key] = [0] * 6
        goodLetters[key][pos] = val

    for pair in state.split(','):
        guess, feedback = pair.split(':')
        for i, ch in enumerate(guess):     
            if(feedback[i] == '3'):
                add2Good(ch, i, 3)
                if guess.count(ch) > 1 and goodLetters[ch][5] == 0:
                    numOnes = 0
                    for i1 in range(5):
                        numOnes += guess[i1] == ch and feedback[i1] == '1'
                    if(numOnes > 0):
                        goodLetters[ch][5] = guess.count(ch) - numOnes
            elif(feedback[i] == '2'):
                add2Good(ch, i, 1)
                if guess.count(ch) > 1 and goodLetters[ch][5] == 0:
                    numOnes = 0
                    for i1 in range(5):
                        numOnes += guess[i1] == ch and feedback[i1] == '1'
                    if(numOnes > 0):
                        goodLetters[ch][5] = guess.count(ch) - numOnes
            elif(feedback[i] == '1'): 
                if ch in goodLetters.keys():
                    goodLetters[ch][i] = 1
                else:
                    badLetters[ch2Ind(ch)] = 1
        # clean badWords
        for ch in goodLetters.keys():
            badLetters[ch2Ind(ch)] = 0
    return badLetters, goodLetters

def updateInfo(newFeedback, info):
    badLettersTrue, goodLettersTrue = info
    badLetters = badLettersTrue.copy()
    goodLetters = goodLettersTrue.copy()

    def add2Good(key, pos, val):
        if key not in goodLetters:
            goodLetters[key] = [0] * 6
        goodLetters[key][pos] = val

    for pair in newFeedback.split(','):
        guess, feedback = pair.split(':')
        for i, ch in enumerate(guess):     
            if(feedback[i] == '3'):
                add2Good(ch, i, 3)
                if guess.count(ch) > 1 and goodLetters[ch][5] == 0:
                    numOnes = 0
                    for i1 in range(5):
                        numOnes += guess[i1] == ch and feedback[i1] == '1'
                    if(numOnes > 0):
                        goodLetters[ch][5] = guess.count(ch) - numOnes
            elif(feedback[i] == '2'):
                add2Good(ch, i, 1)
                if guess.count(ch) > 1 and goodLetters[ch][5] == 0:
                    numOnes = 0
                    for i1 in range(5):
                        numOnes += guess[i1] == ch and feedback[i1] == '1'
                    if(numOnes > 0):
                        goodLetters[ch][5] = guess.count(ch) - numOnes
            elif(feedback[i] == '1'): 
                if ch in goodLetters.keys():
                    goodLetters[ch][i] = 1
                else:
                    badLetters[ch2Ind(ch)] = 1
        # clean badWords
        for ch in goodLetters.keys():
            badLetters[ch2Ind(ch)] = 0
    return badLetters, goodLetters

# Alternate if feedback == 1 code, doesn't require clean badwords
# i1 = guess.find(ch)
# while(i1 != -1):
#     if feedback[i1] == '2' or feedback[i1] == '3':
#         add2Good(ch, i, 1)
#         break
#     i1 = guess.find(ch, i1 + 1)
# if ch not in goodLetters:
#     badLetters[ch2Ind(ch)] = 1s

def isPossible(guess, info):
    badLetters, goodLetters = info
    for ch in guess:
        if badLetters[ch2Ind(ch)] == 1:
            return False
    for key in goodLetters.keys():
        for i, val in enumerate(goodLetters[key][:-1]):
            if val == 1:
                if guess[i] == key:
                    return False
            elif val == 3:
                if guess[i] != key:
                    return False
        numKey = guess.count(key)
        if goodLetters[key][5] == 0:
            if key not in guess:
                return False
        elif guess.count(key) != goodLetters[key][5]:
            return False
    return True

def numPossible(wordlist, info):
    n = 0
    for word in wordlist:
        if isPossible(word, info):
            n += 1    
    return n

def getPossibles(wordList, info):
    possibles = []
    for word in wordList:
        if isPossible(word, info):
            possibles.append(word)
    return possibles 



def play(state):
    totalLoops = 1250
    answersCap = 50
    wordlist = get_wordlist()

    

    l = len(wordlist)

    

    info = getInfo(state)
    possibles = getPossibles(wordlist, info)
    
    if(len(possibles) <= answersCap):
        numAnswers = len(possibles)
    else:
        numAnswers = answersCap
    numGuesses = int(totalLoops / numAnswers)
    if(numGuesses >= len(wordlist)):
        numGuesses = len(wordlist)
    
    answers = []
    for w in possibles:
        answers.append(w)
    while(len(answers) > numAnswers):
        answers.pop(random.randrange(len(answers)))

    
    guesses = []

    for w in wordlist:
        guesses.append(w)
    while(len(guesses) > numGuesses):
        guesses.pop(random.randrange(len(guesses)))

    
    # guessArr = []
    bestGuess = 'error'
    bestSum = -1

    for i, guess in enumerate(guesses):
        # ansArr = []
        sum = 0
        for j, answer in enumerate(answers):
            newInfo = updateInfo(getFeedback(guess, answer), info)
            # ansArr.append(numPossible(wordlist, newInfo))
            sum += numPossible(wordlist, newInfo)
            # s = i * numAnswers + j
            # print(s)

        if sum < bestSum or bestSum == -1:
            bestGuess = guess
            bestSum = sum
        # guessArr.append(ansArr)

    print(bestGuess)
    return random.choice(possibles)
            




