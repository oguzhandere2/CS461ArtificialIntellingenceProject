import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
import numpy as np
from tkinter.ttk import Separator, Style
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import heapq
import re
import random
import gensim.downloader as api

today = datetime.today()
cutOffThreshold = 0.6
totalBoxesFilled = 0 
threshHold = 8
sleep=1

global val1
global val2
global val3
global val4
global val5

val1=10
val2=6
val3=4
val4=2

heuristicValues1 = [val1,val1,val1,val1,val1]
heuristicValues2 = [val2,val2,val2,val2,val2]
heuristicValues3 = [val3,val3,val3,val3,val3]
heuristicValues4 = [val4,val4,val4,val4,val4]

##Date of today
y = today.strftime("%d/%m/20%y")
print("Date of today: ", y)
time.sleep(sleep)
print("#=========================#")

print("We are connecting to daily NY Times Puzzle website: https://www.nytimes.com/crosswords/game/mini")
time.sleep(sleep)
print("#=========================#")

url = "https://www.nytimes.com/crosswords/game/mini"
response = requests.get(url)
soup = BeautifulSoup(response.text,"html.parser")
cluesArray = []

print("We are now determining todays clues by searching the class names specific to the across and down clues")
time.sleep(sleep)
print("#=========================#")

for b in soup.findAll('li',attrs={'class':'Clue-li--1JoPu'}):
    clue = b.find('span', attrs={'Clue-text--3lZl7'})
    cluesArray.append(b.get_text())
  
across = (cluesArray [0: int ( len(cluesArray ) / 2 )])
down = (cluesArray [int ( len(cluesArray ) / 2 ) :])

print("Across Clues with Numbers: " , across)
print("#=========================#")

print("Down Clues with Numbers:", down)
print("#=========================#")

whiteBoxTextsNumbers = {}
print("We are determining the coordinates of the black boxes and white boxes which include clue numbers")
time.sleep(sleep)
print("#=========================#")

for c in soup.findAll('g',attrs={'data-group':'cells'}):   
    box = c.findAll('rect', attrs={'class':'Cell-block--1oNaD Cell-nested--x0A1y'})
    whiteBox = c.findAll('rect', attrs={'class':'Cell-cell--1p4gH Cell-nested--x0A1y'})
    whiteBoxTexts = c.findAll ('text')
    for i in range(len(c)):
        if (len(c.contents[i])) == 3:
            whiteBoxTextsNumbers[i] = c.contents[i].contents[1].contents[1]
                                   
blackbox=[]
for i in box:
    blackbox.append(i.get("id"))

blackboxids=[]
for i in blackbox:
    blackboxids.append(i[8:])
        
print("Coordinates of the black boxes: ", blackboxids)
time.sleep(sleep)
print("#=========================#")

print ("Coordinates of white boxes with clue numbers: ", whiteBoxTextsNumbers)
time.sleep(sleep)
print("#=========================#")

def reveal():
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='C:/Users/ahmet/Desktop/CS461/Project/chromedriver.exe', options=options)
    driver.get(url)
    time.sleep(2.5)
    # click on initial message
    if len(driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")) != 0:
        python_button = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")[0]
        python_button.click()
        time.sleep(1.5)
    elif len(driver.find_elements_by_xpath("/html/body/div/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")) !=0:
        python_button = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")[0]
        python_button.click()
        time.sleep(1.5)
    else:
        python_button = driver.find_elements_by_xpath("/html/body/div/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button")[0]
        python_button.click()
        time.sleep(1.5)
    # click reveal button
    python_button = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[1]/ul/div[2]/li[2]/button")[0]
    python_button.click()
    time.sleep(0.5)
    # click puzzle button
    python_button = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]")[0]
    python_button.click()
    time.sleep(0.5)
    # click reveal button again
    python_button = driver.find_elements_by_xpath("/html/body/div/div/div[2]/div[2]/article/div[2]/button[2]")[0]
    python_button.click()
    time.sleep(0.5)
    revealedPage = driver.page_source
    soupReveal = BeautifulSoup(revealedPage,"html.parser")
    whiteBoxLetters={}
    for c in soupReveal.findAll('g',attrs={'data-group':'cells'}):   
        for i in range(len(c)):
            if (len(c.contents[i])) == 3:
                whiteBoxLetters[i] = c.contents[i].contents[1].contents[1]
            if (len(c.contents[i])) == 4:
                whiteBoxLetters[i] = c.contents[i].contents[2].contents[1]
    time.sleep(4)
    driver.close()
    return whiteBoxLetters     



def findAffectingBoxIndexOfClues(acrossCluesWithNumbers, downCluesWithNumbers, coordinatesOfWhiteBoxes, coordinatesOfBlackBoxes):
    result = {}
    reversed_coordinatesOfWhiteBoxes = {value : key for (key, value) in coordinatesOfWhiteBoxes.items()}
    for clues in acrossCluesWithNumbers:
        #clueNumber = int(clues[0])
        startingCoordinate = (reversed_coordinatesOfWhiteBoxes[clues[0]])
        maxWordCount = 5 - int(startingCoordinate % 5)
        currentWordCount = 0
        
        clueToAdd = clues[0] + "_A_" + clues[1:]
        result[clueToAdd] = []
        while currentWordCount < maxWordCount:
            result[clueToAdd].append(startingCoordinate)
            currentWordCount += 1
            startingCoordinate += 1
            if(str(startingCoordinate) in coordinatesOfBlackBoxes):
                break
    
    for clues in downCluesWithNumbers:
        #clueNumber = int(clues[0])
        startingCoordinate = int(reversed_coordinatesOfWhiteBoxes[clues[0]])
        maxWordCount = 5 - int(startingCoordinate / 5)
        currentWordCount = 0
        
        clueToAdd = clues[0] + "_D_" + clues[1:]
        result[clueToAdd] = []
        while currentWordCount < maxWordCount:
            result[clueToAdd].append(startingCoordinate)
            currentWordCount += 1
            startingCoordinate += 5
            if(str(startingCoordinate) in coordinatesOfBlackBoxes):
                break
    return result

def puzzleGrid(answers):
    puzzlegrid=[]
    t=0
    for i in answers:
        puzzlegrid.append(answers.get(i))
        t+=1
    puzzlegrid=np.array(puzzlegrid)
    puzzlegrid=puzzlegrid.reshape((5,5))
    return puzzlegrid

def similar(string1,string2):
    count=0
    for i in range(len(string1)):
        if string1[i]==string2[i]:
            count+=1
    count=count/len(string1)
    return count

def tryPredictions(affectingBoxesOfClues, coordinatesOfBlackBoxes, listOfCluesAndPredictions):
    global heuristicValues
    global threshHold
    cluesAndTheirAffectingBoxes = {}
    currentClueValues = {}
    global totalBoxesFilled 
    wordList = []
    
    for i in range(25):
        if str(i) in coordinatesOfBlackBoxes:
            currentClueValues[i] = "B"
        else:
            currentClueValues[i] = "-"
    
    #cluesAndTheirAffectingBoxes ex. --> ["5_A": [5, 6, 7, 8], ...]
    for key, value in affectingBoxesOfClues.items():
        clueID = key[:3] #number_A or #number_D. A and D stands for across and down
        cluesAndTheirAffectingBoxes[clueID] = value

    justCluesAndPredictions = {}    
    for key in listOfCluesAndPredictions.keys():
        justCluesAndPredictions[key] = []
    # mainListOfPredictions ex. --> [["1_A", "guess1", 233], ["2_A", "guess2", 230]]
    
    mainListOfPredictions = []
    for key, value in listOfCluesAndPredictions.items():
        for singleGuess in value:
            mainListOfPredictions.append([key, singleGuess[0], singleGuess[1]])
            wordList.append(singleGuess[0])
            justCluesAndPredictions[key].append(singleGuess[0])
    
    
    mainListOfPredictions.sort(key=lambda x: int(x[2]),reverse = True)
    
    for guess in mainListOfPredictions:
        word = guess[1]
        for ind in range(len(word)):
            if word[ind] == '-':
                print("Found:", word, "\n")
                mainListOfPredictions.remove(guess)
                break
    
    addedItemIndexes = []
    
    
    totalBoxesFilled = len(coordinatesOfBlackBoxes)
    #placement1
    previousCurrentClueValues = currentClueValues.copy()
    previousTotalBoxesFilled = totalBoxesFilled
    addedItemIndexes.append([0, previousCurrentClueValues, previousTotalBoxesFilled])
    turn = fitBoxAccordingly(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[0])
    lastIndex = 0
    """
    for index in range(1, len(mainListOfPredictions)):
        nodeID = mainListOfPredictions[index][0]
        if turn == nodeID[2]:
            if checkIfFits(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[index]):
                #placement2
                turn = fitBoxAccordingly(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[index])
                addedItemIndexes.append(index)
                lastIndex = index + 1
                break
    """         
    
    
    #main loop
    
    previousCurrentClueValues = currentClueValues.copy()
    previousTotalBoxesFilled = totalBoxesFilled
    while True:
        for index in range(lastIndex + 1, len(mainListOfPredictions)):
            #print("Turn for: ", mainListOfPredictions[index][0], mainListOfPredictions[index][1] )
            if totalBoxesFilled >= 25:
                break
            
            
            if checkIfFits(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[index]):
                previousCurrentClueValues = currentClueValues.copy()
                previousTotalBoxesFilled = totalBoxesFilled
                fitBoxAccordingly(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[index])
                addedItemIndexes.append([index, previousCurrentClueValues, previousTotalBoxesFilled])

                
        if totalBoxesFilled < 25:
            if len(addedItemIndexes) == 0:
                print("There is no puzzle solution with the specified threshHold of ", threshHold)
                break
            
            lastIndexNode = addedItemIndexes.pop()
            #print("Removing", mainListOfPredictions[lastIndex], "\n")
            #print(totalBoxesFilled, "\n", currentClueValues, "\n", previousTotalBoxesFilled, "\n",previousCurrentClueValues, "\n")
            
            lastIndex = lastIndexNode[0]
            currentClueValues = lastIndexNode[1]
            totalBoxesFilled = lastIndexNode[2]
            #removeWord(currentClueValues, cluesAndTheirAffectingBoxes, mainListOfPredictions[lastIndex])
        else:
            resultVal = checkSolutionValueNew(cluesAndTheirAffectingBoxes, currentClueValues, justCluesAndPredictions)
            if resultVal >= threshHold:
                print("Answer found!")
                break
            else:
                heuristicValue = checkAndModifyHeuristicValues(cluesAndTheirAffectingBoxes, currentClueValues, justCluesAndPredictions)
                print("Found a result but it's less than the threshold. Continuing...\n" , puzzleGrid(currentClueValues), "\n")
#                if len(addedItemIndexes) < (heuristicValue + 1):
#                    print("No item left")
#                    break
                if heuristicValue == 1:
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndex = lastIndexNode[0]
                    currentClueValues = lastIndexNode[1]
                    totalBoxesFilled = lastIndexNode[2]
                elif heuristicValue == 2:
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndex = lastIndexNode[0]
                    currentClueValues = lastIndexNode[1]
                    totalBoxesFilled = lastIndexNode[2]
                elif heuristicValue == 3:
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndex = lastIndexNode[0]
                    currentClueValues = lastIndexNode[1]
                    totalBoxesFilled = lastIndexNode[2]
                elif heuristicValue == 4:
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndex = lastIndexNode[0]
                    currentClueValues = lastIndexNode[1]
                    totalBoxesFilled = lastIndexNode[2]
                elif heuristicValue == 5:
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndexNode = addedItemIndexes.pop()
                    lastIndex = lastIndexNode[0]
                    currentClueValues = lastIndexNode[1]
                    totalBoxesFilled = lastIndexNode[2]   
    return currentClueValues          

def checkAndModifyHeuristicValues(cluesAndTheirAffectingBoxes, currentClueValues, justCluesAndPredictions):
    global heuristicValues1
    global heuristicValues2
    global heuristicValues3
    global heuristicValues4
    global cutOffThreshold
    t = 0
    for key,value in cluesAndTheirAffectingBoxes.items():
        
        if key[2] == "A":
            theWord = ""
            isFullWord = True
            for index in value:
                if  currentClueValues[index] == "-":
                    isFullWord = False
                    break
                theWord = theWord + currentClueValues[index]
            if isFullWord:
                foundAValue = False
                for words in justCluesAndPredictions[key]:
                    if(similar(words, theWord) >= cutOffThreshold):
                        foundAValue = True
                        heuristicValues1[t] = val1
                        heuristicValues2[t] = val2
                        heuristicValues3[t] = val3
                        heuristicValues4[t] = val4
                        break
                if not foundAValue:
                    heuristicValues1[t] -= 1
                    heuristicValues2[t] -= 1
                    heuristicValues3[t] -= 1
                    heuristicValues4[t] -= 1
        t += 1
    if sum(heuristicValues1) <= val1/2:
        for i in range(5):
            heuristicValues1[i] = val1 
        return 5 #Dont go any further
    elif sum(heuristicValues2) <= val2/2:
        for i in range(5):
            heuristicValues2[i] = val2 
        return 4 #Dont go any further
    elif sum(heuristicValues3) <= val3/2:
        for i in range(5):
            heuristicValues3[i] = val3 
        return 3 #Dont go any further
    elif sum(heuristicValues4) <= val4/2:
        for i in range(5):
            heuristicValues4[i] = val4 
        return 2 #Dont go any further
    else:
        return 1 #Keep going

def checkSolutionValue(wordList, cluesAndTheirAffectingBoxes, currentClueValues):
    resultingValue = 0 
    wordsInsidePuzzle = []
    for affectingBoxIndices in cluesAndTheirAffectingBoxes.values():
        theWord = ""
        for index in affectingBoxIndices:
            theWord = theWord + currentClueValues[index]
        wordsInsidePuzzle.append(theWord)
    
    for eachWord in wordsInsidePuzzle:
        if eachWord in wordList:
            resultingValue += 1
    
    return resultingValue

def checkSolutionValueNew(cluesAndTheirAffectingBoxes, currentClueValues, justCluesAndPredictions):
    resultingValue = 0 
    for key, value in cluesAndTheirAffectingBoxes.items():
        theWord = ""
        for index in value:
            theWord = theWord + currentClueValues[index]
        if theWord in justCluesAndPredictions[key]:
            resultingValue += 1
    
    return resultingValue
    
def changeTurn(turn):
    if turn == "A":
        return "D"
    else:
        return "A"
    
def checkIfFits(currentClueValues, cluesAndTheirAffectingBoxes, guessNode):
    clueID = guessNode[0]
    
    word = guessNode[1]
    boxValues = cluesAndTheirAffectingBoxes[clueID]
    for index in range(len(boxValues)):
        if currentClueValues[boxValues[index]] != "-" and currentClueValues[boxValues[index]] != word[index]:
            return False
            
    return True
    
def fitBoxAccordingly(currentClueValues, cluesAndTheirAffectingBoxes, guessNode):
    
    global totalBoxesFilled
    
    clueID = guessNode[0]
    word = guessNode[1]
    boxValues = cluesAndTheirAffectingBoxes[clueID]
    for index in range(len(boxValues)):
        if currentClueValues[boxValues[index]] == "-":
            totalBoxesFilled += 1
        currentClueValues[boxValues[index]] = word[index] #This is where we UPDATE 5x5 grid values. Use here for UI view change
    #maybe update UI here?
    if clueID[2] == "A":
        return "D"
    else:
        return "A"

def removeWord(currentClueValues, cluesAndTheirAffectingBoxes, guessNode):
    
    global totalBoxesFilled
    
    clueID = guessNode[0]
    boxValues = cluesAndTheirAffectingBoxes[clueID]
    
    
    startingIndex = boxValues[0]
    
    if(clueID[2] == "A"):        
        level = int(startingIndex / 5)
        
        if level == 0:
            for boxIndex in boxValues:
                for crossIndex in range(boxIndex, 25, 5):
                    if currentClueValues[crossIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        break
                            
        elif level == 4:
            for boxIndex in boxValues:
                for crossIndex in range(boxIndex, -1, -5):
                    if currentClueValues[crossIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        break
                            
        else:
            for boxIndex in boxValues:
                flag = True
                for crossIndex in range(boxIndex, -1, -5):
                    if currentClueValues[crossIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        flag = False
                        break
                if flag:    
                    for crossIndex in range(boxIndex, 25, 5):
                        if currentClueValues[crossIndex] == "-":
                            totalBoxesFilled -= 1
                            currentClueValues[boxIndex] = "-"
                            break
        return "A"
    else:
        level = int(startingIndex % 5)
        
        if level == 0:
            for boxIndex in boxValues:
                for downIndex in range(boxIndex, boxIndex + 5):
                    if currentClueValues[downIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        break
        elif level == 4:
            for boxIndex in boxValues:
                for downIndex in range(boxIndex, boxIndex - 5):
                    if currentClueValues[downIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        break
        else:
            for boxIndex in boxValues:
                flag = True
                for downIndex in range(boxIndex, boxIndex + (5 - (boxIndex % 5))):
                    if currentClueValues[downIndex] == "-":
                        totalBoxesFilled -= 1
                        currentClueValues[boxIndex] = "-"
                        flag = False
                        break
                if flag:
                    for crossIndex in range(boxIndex, boxIndex - ((boxIndex % 5) + 1)):
                        if currentClueValues[crossIndex] == "-":
                            totalBoxesFilled -= 1
                            currentClueValues[boxIndex] = "-"
                            break
        return "D"
    
    
print ("Now let us reveal the answers")
time.sleep(sleep)
print("#=========================#")

whiteBoxLetters = reveal()
print ("There are the coordinates of the boxes associated to the revealed letters ", whiteBoxLetters)
#time.sleep(sleep)
print("#=========================#")

## UI part
fen = tk.Tk()
fen.minsize(1500, 500)
fen.title("Puzzle Output")
fen.config(bg = "white")

#Creating the puzzle frame below 
puzzle = tk.Frame(fen, bg="white")
puzzle2 = tk.Frame(fen, bg="white")
puzzle.pack_propagate(False)
puzzle2.pack_propagate(False)

stop = stopwords.words('english') + list(string.punctuation)
letterCounts=[4,4,5,4,4,5,5,5,3,3]

def clues():
    a1 = "What a black three-leaf clover represents"
    a2 = "Highway division"
    a3 = "Wishy-washy R.S.V.P."
    a4 = "Snack that's the most-used brand name in New York Times crosswords"
    a5 = '"The Communist Manifesto" co-author'
    
    d1 = "___ Barton, nurse who founded the Red Cross"
    d2 = "Crust, mantle or core"
    d3 = "Remove from the packaging"
    d4 = 'Creature with five eyes and six legs'
    d5 = 'CBS sitcom starring Allison Janney and Anna Faris'
    sentence_clues=[a1,a2,a3,a4,a5,d1,d2,d3,d4,d5]
    return sentence_clues

def decontracted(phrase):
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub('[0-9]+', '', phrase)
    phrase = re.sub("_"," ", phrase)
    phrase = re.sub("-"," ", phrase)
    # remove numbers
    phrase = re.sub(r'\d+', '', phrase)
    # remove punctuations and convert characters to lower case
    phrase = "".join([char.lower() for char in phrase if char not in string.punctuation]) 
    # substitute multiple whitespace with single whitespace
    # Also, removes leading and trailing whitespaces
    phrase = re.sub('\s+', ' ', phrase).strip()
    return phrase

def lemma(solver, phrase):
    coinflip = random.randint(0,1)
    if coinflip == 1:
        try:
            similars = solver.most_similar(phrase, topn=10)
            randomsyn=word_tokenize(decontracted(random.choice(similars)[0]))
            return randomsyn[0]
        except:
            return "-"
    else:
        return "-"

def getCombinations(sentenceList):
    if len(sentenceList) == 1 :
        return [sentenceList]
    else:
        return [[sentenceList[i], sentenceList[i + 1]] for i in range(len(sentenceList) - 1)]

def guessSentence(solver, solverb, length, stop, sentence):
    pattern = r'[\d.,]+|[A-Z][.A-Z]+\b\.*|\w+|\S'
    tokenizer = RegexpTokenizer(pattern)
#    tokenizer = TweetTokenizer(strip_handles=True, reduce_len=True)
    wordNumber = len(tokenizer.tokenize(sentence.lower()))
    topn = 5000*wordNumber # No. of words to be returned by Gensim's most_similar()
    pos_words = [decontracted(word) for word in tokenizer.tokenize(sentence.lower()) if word not in stop and decontracted(word) != "" and len(word)!=1]
    probable_guesses=[]
    try:
        probable_guesses = [word for word in solver.most_similar(positive=pos_words, topn=topn) if len(word[0]) == length]
    except:
        try:
            probable_guesses = [word for word in solverb.most_similar(positive=pos_words, topn=topn) if len(word[0]) == length]
        except:
            pass
    probable_guesses = [word for word in probable_guesses if word[0].isalpha()==True]
    return probable_guesses, pos_words

def secondGuess(solver, solverb, prevGuesses, posWords):
    toSort=[]
    for guess in prevGuesses:
        checkMax=[]
        for wordClue in posWords:
            try:
                checkMax.append(solver.similarity(guess[0], wordClue))
            except:
                try:
                    checkMax.append(solverb.similarity(guess[0], wordClue))
                except:
                    checkMax.append(0)
        toSort.append(np.mean(heapq.nlargest(len(checkMax)//8+1, checkMax)))
    zipped = zip(toSort, prevGuesses)
    sortedzip = sorted(zipped)
    checksorted = [i for (i, s) in sortedzip][::-1]
    reshaped = [s for (i, s) in sortedzip][::-1]
    return reshaped, checksorted

def sortNew(newGuesses, sort, slist, k):
    sortedGuesses=[]
    index=0
    for tup in newGuesses:
        if index == croplist[k] and index == croplist[k]+50:
            sortedGuesses.append(tuple((tup[0],(sort[index]+slist[k]))))
            index+=1
        return sortedGuesses
    return sortedGuesses

slist = [0, 0, 0, 0, 0, 2, 5, 1, 4, 3]
croplist=[200, 0, 0, 300, 100, 250, 0, 0, 300, 0]
affectingBoxesOfClues = findAffectingBoxIndexOfClues(across, down, whiteBoxTextsNumbers, blackboxids)
inputDictionary = affectingBoxesOfClues.copy()

cluecoords=[]
for strings in [*inputDictionary]:
    cluecoords.append(strings[0:3])    
#MAIN ----------------------------------------------------------------------------------------------------

sentence_clues = []

justClueIDandLetterCount = {}
letterCounts = []
for key, value in inputDictionary.items():
    justClueIDandLetterCount[key[:3]] = len(value)
    
for acrossSentences in across:
    sentence_clues.append(acrossSentences[1:])
    letterCounts.append( justClueIDandLetterCount[(acrossSentences[0] + "_A")])
for acrossSentences in down:
    sentence_clues.append(acrossSentences[1:])
    letterCounts.append( justClueIDandLetterCount[(acrossSentences[0] + "_D")])
    
#print("letter counts:", letterCounts)
print("inputDictionary:", inputDictionary)

#solver1 = api.load("glove-wiki-gigaword-300") #glove-wiki-gigaword-300
#solver2 = api.load("conceptnet-numberbatch-17-06-300") #conceptnet-numberbatch-17-06-300

outputDictionary = {}
for index in range(10):
    sentence_clues = clues()
    guess, posw = guessSentence(solver1, solver2, letterCounts[index], stop, sentence_clues[index])
    newGuesses, checksorted = secondGuess(solver2, solver1, guess, posw)
    sortedGuesses = sortNew(newGuesses, checksorted, slist, index)
    outputDictionary[cluecoords[index]]=sortedGuesses

#print(sentence_clues)
listOfCluesAndPredictions = outputDictionary.copy()
resultingGrid = tryPredictions(affectingBoxesOfClues, blackboxids, listOfCluesAndPredictions)
print("AI answers:\n", puzzleGrid(resultingGrid))

#MAIN ----------------------------------------------------------------------------------------------------
for x in range (5):
    for y in range (5):
        boxIndex = 5*x + y
        box = tk.Label(puzzle, bg="black", padx = 0, pady = 0)
        for i in range(3):
            for j in range(3):
                #We fill each generated puzzle with according to its configuration at the particular step.
                minibox = None
                if i == 1 and j == 1 and (boxIndex in whiteBoxLetters):
                    minibox = tk.Label(box, text = whiteBoxLetters[boxIndex].upper()) #This place is used for letters
                elif i == 0 and j == 0 and (boxIndex in whiteBoxTextsNumbers):
                    minibox = tk.Label(box, text = whiteBoxTextsNumbers[boxIndex])
                else:
                    minibox = tk.Label(box, text = " ")
                    
                minibox.config(font=("Times New Roman", 16))
                
                minibox.grid(row = i, column = j, sticky = "w", pady = 0, padx = 0)
                
                if( str(boxIndex) in blackboxids): 
                    minibox.config(width=2, bg = "black")
                else:
                    minibox.config(width=2, bg = "white")
                
        box.grid(row = x, column = y, sticky = "w", pady = 1, padx = 1)
        box.config(width=2)
        
for x in range (5):
    for y in range (5):
        boxIndex = 5*x + y
        box = tk.Label(puzzle2, bg="black", padx = 0, pady = 0)
        for i in range(3):
            for j in range(3):
                #We fill each generated puzzle with according to its configuration at the particular step.
                minibox = None
                if i == 1 and j == 1 and (boxIndex in whiteBoxLetters):
                    minibox = tk.Label(box, text = resultingGrid[boxIndex].upper()) #This place is used for letters
                elif i == 0 and j == 0 and (boxIndex in whiteBoxTextsNumbers):
                    minibox = tk.Label(box, text = whiteBoxTextsNumbers[boxIndex])
                else:
                    minibox = tk.Label(box, text = " ")
                    
                minibox.config(font=("Times New Roman", 16))
                
                minibox.grid(row = i, column = j, sticky = "w", pady = 0, padx = 0)
                
                if( str(boxIndex) in blackboxids): 
                    minibox.config(width=2, bg = "black")
                else:
                    minibox.config(width=2, bg = "white")
                
        box.grid(row = x, column = y, sticky = "w", pady = 1, padx = 1)
        box.config(width=2)

        
#Configuring the place of the puzzle frame below            
puzzle.grid(column= 0, row = 0, pady=10 ,padx=10, sticky="n")
sep = Separator(fen, orient="vertical")
#sep.grid(column= 1, row=0, sticky="ns") #can be uncommented for an extra separator
sty = Style(fen)

puzzle2.grid(column= 5, row = 0, pady=10 ,padx=10, sticky="n")
sep = Separator(fen, orient="vertical")
#sep.grid(column= 1, row=0, sticky="ns") #can be uncommented for an extra separator
sty = Style(fen)

#Creating the date-groupname label below
# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dateAndGroupName = "Group name - date and time: ATOA - " + dt_string;
dateAndGroupNameLabel = tk.Label(fen, bg = "white", text = dateAndGroupName)
dateAndGroupNameLabel.config(font=("Times New Roman", 14))
dateAndGroupNameLabel.place(relx = -1,  rely = -1, anchor = 'e')

#Configuring the place of date-groupname frame below
dateAndGroupNameLabel.grid(column= 0, row = 1, pady=10 ,padx=10, sticky="n")

#Creating the across frame below 
acrossCluesFrame = tk.Frame(fen, bg="white")
acrossCluesFrame.pack_propagate(False)
mainLabel = tk.Label(acrossCluesFrame, bg="white", text = "ACROSS")
mainLabel.config(font=("Times New Roman", 24))
mainLabel.grid(row = 0, column = 0, sticky = "w")

hintIndex = 1
for hintString in across:
    modifiedHintString = hintString[0:1] + ". " + hintString[1:]
    newHintLabel = tk.Label(acrossCluesFrame, bg="white", text = modifiedHintString)
    newHintLabel.config(font=("Times New Roman", 12))
    newHintLabel.grid(row = hintIndex, column = 0, sticky = "w")
    hintIndex += 1
    
#Configuring the place of the across frame below      
acrossCluesFrame.grid(row = 0, column = 2, pady=10, padx=30, sticky = "w")
sep = Separator(fen, orient="vertical")
sep.grid(column= 3, row=0, sticky="ns")
sty = Style(fen)
sty.configure("TSeparator", background="black")

#Creating the down frame below 
downCluesFrame = tk.Frame(fen, bg="white")
downCluesFrame.pack_propagate(False)
mainLabel = tk.Label(downCluesFrame, bg="white", text = "DOWN")
mainLabel.config(font=("Times New Roman", 24))
mainLabel.grid(row = 0, column = 0, sticky = "w")

hintIndex = 1
for hintString in down:
    modifiedHintString = hintString[0:1] + ". " + hintString[1:]
    newHintLabel = tk.Label(downCluesFrame, bg="white", text = modifiedHintString)
    newHintLabel.config(font=("Times New Roman", 12))
    newHintLabel.grid(row = hintIndex, column = 0, sticky = "w")
    hintIndex += 1
    
#Configuring the place of the down frame below      
downCluesFrame.grid(row = 0, column = 4, pady=10, padx=30, sticky = "w")   

fen.mainloop()  