import nltk
from PyDictionary import PyDictionary
from difflib import SequenceMatcher
import Levenshtein
from udpy import UrbanClient
from threading import Thread
i = 1
#buraya dikkat
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def getNWordsList(n):
    n = n + 1
    
    f = open("words_alpha.txt", "r")
    
    resultingList = []
    for word in f:
        if len(word) == n:
            resultingList.append( [ (word[:len(word) - 1]).lower(), 0])
    
    return resultingList

def getAllWords(words3, words4, words5):
    
    
    f = open("words_alpha.txt", "r")
    
    resultingList = []
    for word in f:
        if len(word) == 4:
            words3.append( [ (word[:len(word) - 1]).lower(), 0])
        elif len(word) == 5:
            words4.append( [ (word[:len(word) - 1]).lower(), 0])
        elif len(word) == 6:
            words5.append( [ (word[:len(word) - 1]).lower(), 0])
            
    return resultingList

def getWordPoints(word, tokens):
    
    meaning = dict.meaning(word)
    for sentence in meaning["Noun"]:
        print("")
        
        
    for sentence in meaning["Verb"]:
        print("")
        
def getSentenceWords(sentence):
    return nltk.word_tokenize(sentence)
        
def getCombinations(sentenceList):
    
    if len(sentenceList) == 1 :
        return [sentenceList]
    else:
        return [[sentenceList[i], sentenceList[i + 1]] for i in range(len(sentenceList) - 1)]
    
def compareMeanings(dictionaryMeaning, clue):
    comparisonSum = 0.0
    dictionaryCombinations = getCombinations(dictionaryMeaning)
    clueCombinations = getCombinations(clue)
    
    
    for i in range(len(dictionaryCombinations)):
        leftString = (' '.join(map(str, dictionaryCombinations[i]))).lower()
        for j in range(len(clueCombinations)):
            rightString = (' '.join(map(str, clueCombinations[j]))).lower()
            comparisonSum += Levenshtein.distance(leftString,rightString)
    
    return comparisonSum
    #   comparisonSum / (len(dictionaryCombinations) * len(clueCombinations))

def calculateWordPoints(words, clue):
    print(len(words),"kadar gidecek.\n")
    i = 1
    for word in words:
        print(word[0])
        meanings = wordDatabase[word[0]]
        if i % 10 == 0:
            print(i,"\n")
        i += 1
        if meanings is not None:
            for sentence in meanings:
                word[1] += compareMeanings(getSentenceWords(sentence), clue)
            
     


def addItems(threadname, words, dict):
    global wordDatabase
    global i
    for word in words:
        meanings = dict.meaning(word[0], True)
        print(i, "\n")
        i += 1
        sentences = []
        if meanings is not None:
            for allsentences in meanings.values():
                for sentence in allsentences:
                    sentences.append(sentence)
        wordDatabase[word[0]] = sentences  
        

    
def preProcess():
    
    dict = PyDictionary()
    words3 = []
    words4 = []
    words5 = []
    getAllWords(words3, words4, words5)
    
    lengthForWords3 = len(words3)
    perLengthForWords3 = int(lengthForWords3 / 10)
    
    lengthForWords4 = len(words4)
    perLengthForWords4 = int(lengthForWords4 / 10)
    
    lengthForWords5 = len(words5)
    perLengthForWords5 = int(lengthForWords5 / 10)
    
    listOfThreads = []
    for i in range(10):
        wordSubForWords3 = words3[i * perLengthForWords3 : (i * perLengthForWords3) + perLengthForWords3]
        wordSubForWords4 = words4[i * perLengthForWords4 : (i * perLengthForWords4) + perLengthForWords4]
        wordSubForWords5 = words5[i * perLengthForWords5 : (i * perLengthForWords5) + perLengthForWords5]
        
        threadName = "thread-" + str(i)
        t3 = Thread(target=addItems, args=(threadName + "_3",wordSubForWords3,dict,))
        t4 = Thread(target=addItems, args=(threadName + "_4",wordSubForWords4,dict,))
        t5 = Thread(target=addItems, args=(threadName + "_5",wordSubForWords5,dict,))
        
        listOfThreads.append(t3)
        listOfThreads.append(t4)
        listOfThreads.append(t5)
    
    if lengthForWords3 % 10 != 0:
        lastWordSubForWords3 = words3[10 * perLengthForWords3 : ]
        lastThread3 = Thread(target=addItems, args=("lastThread_3",lastWordSubForWords3,dict,))
        listOfThreads.append(lastThread3)
    
    if lengthForWords4 % 10 != 0:
        lastWordSubForWords4 = words4[10 * perLengthForWords4 : ]
        lastThread4 = Thread(target=addItems, args=("lastThread_4",lastWordSubForWords4,dict,))
        listOfThreads.append(lastThread4)
    
    if lengthForWords5 % 10 != 0:
        lastWordSubForWords5 = words5[10 * perLengthForWords5 : ]
        lastThread5 = Thread(target=addItems, args=("lastThread_5",lastWordSubForWords5,dict,))
        listOfThreads.append(lastThread5)
    
    
    
    for threadd in listOfThreads:
        threadd.start()
    
    for threadd in listOfThreads:
        threadd.join()
        
        
    #return wordDatabase
    
"""
dict = PyDictionary()

word = "a"
meanings = dict.meaning(word, True)
print(meanings["Adjective"])

print(similar(meanings["Noun"][1] ,clueA1))



words3 = getNWordsList(3)
#dictionary definitionlar keliemelre parçalanıp clue ile compare meaninge verilcek. 
print("buraya geldi")
calculateWordPoints(words3, clueA1)
"""



if __name__ == '__main__':
    #clueA1 = "Biblical boat"
    #clueA4 = "What's the spymaster provides in Codenames"
    #clueA6 = "\"L\" on an elevator"
    #clueD2 = "Emphasize, as an embarassing error"  
    #preProcess()
    words3 = {}
    words4 = {}
    words5 = {}
    client = UrbanClient()
    try:
        defs = client.get_definition("not")
    except:
        print(len(defs))
        
    print(len(defs))
    for d in defs:
        print(d.definition)
    
    
    for word, meanings in wordDatabase.items():
        
        try:
            defs = client.get_definition(word)
        except:
            print("exception occured.")
            
        if len(defs) != 0 or len(wordDatabase[word]) != 0:
            for d in defs:
                    wordDatabase[word].append(d.definition)
            if len(word) == 3:
                words3[word] = wordDatabase[word]
            elif len(word) == 4:
                words4[word] = wordDatabase[word]
            elif len(word) == 5:
                words5[word] = wordDatabase[word]
    
    
            
    
    #for key, value in wordDatabase.items()
    #selam()
    #print(wordDatabase)
    #words3 = []
    #words4 = []
    #words5 = []
    #getAllWords(words3, words4, words5)
    #calculateWordPoints(words3, clueA1)
    print("biter")
    