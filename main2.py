import sys
import re
import math
import subprocess
import filecmp

def getWordCount(word, allWords):
    count = 0
    for w in allWords:
        if w == word: count += 1
    return count

def getAllWords(dataList):
    newList = []
    pos = 0
    for line in dataList:
        toAdd = line.split(' ')
        newList[pos:pos] = toAdd  
        pos += len(toAdd)
    print('NEWLIST1')
    print(newList)
    pos = 0
    finalList = [word for word in newList]
    for word in newList:
        cur = 0
        toAdd = ['']
        for char in word:
            if char == '\n':
                toAdd.append('\n')
            elif char != ' ':
                toAdd[cur] += char
            else:
                cur += 1
        print("ADD", toAdd)
        split = word.split('\n')
        splitCount = len(split)
        #print("Need to insert", split)
        if splitCount >= 2:
            toInsert = split
            for _ in range(splitCount-1):
                toInsert[1:1] = '\n'
            for i in toInsert:
                if i == '':
                    toInsert.remove('')
            print("Need to insert", toInsert)
            finalList[pos:pos] = toInsert
            finalList.remove(word)
            pos += splitCount
        pos += 1

    print('NEWLIST2')
    print(finalList)
    return finalList

def getTags(word, allWords):
    tag = ''
    pos = 0
    for w in allWords:
        if w == word:
            tag = tag + str(pos)+'_'
        pos += 1
    return word +'_' +tag

def removeWords(word, allWords):
    pos = 0
    newList = []
    for w in allWords:
        if w != word:
            newList.append(w)
    return newList

def writeWordsToFile(words, file):
    f = open(file, 'w')
    pos = 0
    for w in words:
        if w == '\n':
            f.write('\n')
        elif w == '':
            f.write('')
        else:
            toPut = ' '
            if pos < len(words)-1: # messy
                if words[pos+1] == '\n':
                    toPut = ''
            f.write(w+toPut)
        pos += 1
    f.close()

def compr3(file):
    # make copy of file
    data = open(file)
    data = data.read()
    print(data)
    allData = data.split(' ')
    allWords = getAllWords(allData) # ISSUE WITH THIS FUNCTION HERE!!!
    print(allData)
    print("All words prev")
    print(allWords)
    
    seenWords = {}
    # for each word in file, check every other word to see if
    # it exists in other places
    #pos = 0
    for word in allWords:
        #if word in seenWords: continue
        
        
        tag = getTags(word, allWords)
        count = getWordCount(word, allWords)
        #print('Count = ', word, count)
        #print('Tag =', tag)

        if len(word)*count >= len(tag):
            #print("better to use tag", tag)
            #seenWords[word] = 1
            pos = 0
            for w in allWords:
                if w == word:
                    allWords[pos] = tag
                    break
                pos += 1
            #allWords[pos] = tag
            allWords = removeWords(word, allWords)
        #else:
        #   seenWords[word] = 1
        # count dupe occurances, if tagged string < total space dupes take up, then replace
       # pos += 1
    print("All words final")
    print(allWords)
    newFile = file[0:len(file)-4] + '_compr.txt'
    writeWordsToFile(allWords, newFile)

charLookup = ['A','B','C','D','E','F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',]


divAmount = 10 + len(charLookup)
def abbreviate(num):
    curNum = num
    final = ''
    while curNum != 0:
        nextNum = curNum%divAmount
        
        if nextNum >= 10:
            nextNum = charLookup[nextNum-divAmount]
        final = str(nextNum)+ final 
        #print(nextNum)
        curNum = math.floor(curNum/divAmount)
        #print("Next", curNum)
    #print('final', final)
    return final
def getOrig(abbreviated):
    abbreviated = str(abbreviated)
    numSize = len(str(abbreviated))-1
    cur = 0
    for i in abbreviated:
        offset = i
        if i in charLookup:
            #print('in lookup')
            offset = int(charLookup.index(i)) + 10
        offset = int(offset)
        cur += offset * (divAmount**numSize)
        numSize -= 1
        #print('run', divAmount, offset, abbreviated)
    return cur


def removeWordsFromFile(file, word, tag):
    f = open(file, 'r')
    toAdjust = []
    print('Removing word', word)
  

    for line in f:
        words = line.split(' ')
        pos = 0
        newLine = line
         #update tag
        #line = re.escape(line)
        newLine = ''
        #if word in line:
            #print("In line", line)

        for w in words:
            if w == word:
                newLine += tag
            else:
                newLine += w   
            newLine += ' '
            #newLine = newLine.replace(word, tag)
            #newLine = re.sub(r"\b{}\b".format(word), str(tag), newLine)
        newLine = newLine[0:len(newLine)-1]
        toAdjust.append(newLine)
    f.close()
    f = open(file, 'w')
    for line in toAdjust:
        f.write(line)
    f.close()


def getFileWordCount(file, word):
    f = open(file, 'r')
    wCount = 0
    for line in f:
        line = line.rstrip('\n')
        words = line.split(' ')
        for w in words:
            if w == word:
                wCount += 1
    f.close()
    #print(wCount)
    return wCount

def getFileWordIndexes(file, word):
    f = open(file, 'r')
    pos = 0
    indexes = []
    for line in f:
        line = line.rstrip('\n')
        words = line.split(' ')
        for w in words:
            if w == word:
                indexes.append(pos)
            pos += 1
    #print('Indexes for', word, indexes)
    f.close()
    return indexes

def addComprChanges(file, changes):
    f = open(file, 'a')


    # find first occurence
    f.write('\n')
    for w in changes:
        f.write('_'+w[0])


def charElim(file):
    # find all solo chars to remove from abbreviate list
    print("TODO")

def abbreviateIsValid(file, tag):
    f = open(file, 'r')
    for w in f:
        w.replace('\n', '')
        words = w.split(' ')
        for x in words:
            if x == tag:
                return False
    f.close()
    return True 

def getNextAbbreviate(file, curAbbr):
    isValid = False
    while isValid == False:
        curAbbr += 1
        nextStr = abbreviate(curAbbr) 
        isValid = abbreviateIsValid(file, nextStr)
    print("CAN USE ABBREVIATE", abbreviate(curAbbr))
    return curAbbr

def filesEqual(file1, file2):
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    f1Data = []
    for l in f1:
        f1Data.append(l)
    f1.close()
    pos = 0
    for l in f2:
        if l != f1Data[pos]:
            print("NOT EQUAL", l, f1Data[pos])
            f2.close()
            return False
        pos += 1 
    f2.close()
    return True
def compr4(file):
    f = open(file, 'r')
    comprName = file[0:len(file)-4]+'_compressed.txt'
    f2 = open(comprName, 'w+')
    for l in f:
        f2.write(l)
    f2.close()
    f.close()
    
    comprChanges = []
    index = 0
    wordCount = getNextAbbreviate(file, 1)
    f2 = open(comprName, 'r')
    for l in f2:
        line = l.rstrip('\n')
        words = line.split(' ')
        for w in words:
           
            wCount = getFileWordCount(comprName, w)
            tag = w + '_'+str(abbreviate(wordCount))
            
            #print("Potential tag", tag)
            keepCount = len(w)*wCount
            replCount = (len(str(abbreviate(wordCount))))*wCount+len(w)+2
            if keepCount > replCount:
                print("THIS IS BETTER", w, keepCount, replCount, wCount)
                toAdd = [tag, w]
                if toAdd not in comprChanges:
                    comprChanges.append([tag, w])
                    
                    removeWordsFromFile(comprName, w, abbreviate(wordCount))
                    wordCount = getNextAbbreviate(file, wordCount)
               
            index += 1

    print('Final compr changes', comprChanges)
    addComprChanges(comprName, comprChanges)
    return comprName

def lastLine(file):
    f = open(file, 'r')
    lines = f.read().splitlines()
    last_line = lines[-1]
    f.close()
    return last_line


def decompr(file):
    print("TODO")    
    
    line = lastLine(file)
    line = line.split('_')
    del line[0]

    # create decompr file
    f = open(file, 'r')
    newFileName = 'decompr_'+file
    newFile = open(newFileName, 'w')
    toWrite = []

    for l in f:
        toWrite.append(l)
    
    toWrite = toWrite[0:len(toWrite)-1]
    
    toWrite[len(toWrite)-1] = toWrite[len(toWrite)-1][:-1] 
    
    print("Writing", toWrite)
    for l in toWrite:
        newFile.write(l)
    f.close()
    newFile.close()
    # remove last line

    # for each word remove and replace with tag reverse

    for i in range(0, len(line), 2):
        print("Subbing", line[i], line[i+1])
        removeWordsFromFile(newFileName,line[i+1], line[i])


    print("Lastline=", line)
    return newFileName
if len(sys.argv) != 2:
    print('Specify a file to compress')
else:
    file = sys.argv[1]
    #compr3(file)
    #removeWordsFromFile(file, "cavern")
    
    comprName = compr4(file)
    decomprName = decompr(comprName)
    print(filesEqual(file, decomprName))
    
    #removeWordsFromFile('cave_in_2.txt', "'Cause", 'REPLACE')
    #getFileWordIndexes(file, 'back')
    #getFileWordCount(file, 'back')
    #replaceFirstWord(file, 'a', 'asf')
    #orig_size = os.path.getsize(file)
    #compr_size = os.path.getsize(file[0:len(file)-4]+'_compressed.txt')
    #print(orig_size)
    #print(compr_size)
    #print("Compressed by", 100-(compr_size/orig_size)*100)