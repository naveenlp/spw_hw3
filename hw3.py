# most of the passwords seem to have some meaning
# we cannot use a dictionary according to the problem statement
# this means, if we were to generate random characters, it will be easily possible to identify the correct password
# so we prioritize modifying any digits as the first option, modifying unpronouncable characters as the second option
# modifying symbols as the third option, capitalizing letters as last option
# finally, we generate random patterns for passwords if required to make up numbers
# we split the input password into nibbles of digits, characters and symbols and apply the above logic on the nibbles and recombine to get various password combinations

# for modifying digits:
# case 1: digits are a pattern -> return patterns of similar length capped by n
# case 2: all other numbers are treated as random -> all possible random number sequences with the same length capped by n

# for modifying random unpronounceable characters:
# case 1: characters are in a pattern -> return patterns of a similar length capped by n
# case 2: characters are random -> generate random characters of similar length capped by n

# has symbol:
# return all other possible symbols capped by n

# pronounceable:
# return all randomly capitalized values capped by n

# https://docs.python.org/2/library/difflib.html#difflib.get_close_matches

import random
import string
import re
import itertools
import math
from operator import add

############################
#      CORE LOGIC
############################

def generateSweetWords(truePassword, n):
    digits, uprwords, symbols, prwords, allWords = breakdownPassword(truePassword)
    sortedWords = digits + uprwords + symbols + prwords
    
    sweetWordsHash = {}
    # this variable calculates additional number of random variables we need to get to around n sweetwords    
    additional_n = n
    for w in sortedWords:
        sweetNibbles = generateSweetNibble(w, additional_n, digits, uprwords, symbols, prwords)
        sweetWordsHash[w] = sweetNibbles
        additional_n = int(math.ceil(additional_n/len(sweetNibbles)))
                
    # to recombine, first we generate an array of arrays of the generated sweetword bits
    sweetWordsSorted = []
    for a in allWords:
        sweetWordsSorted.append(sweetWordsHash[a])
        
    # then we get a cartesian product of the splatted array
    prod = [''.join(p) for p in  list(itertools.product(*sweetWordsSorted))]
    # shuffle order of the product
    random.shuffle(prod)
    # remove true password from generated passwords before taking 
    prod = list(filter((truePassword).__ne__, prod))
    allCombinations = list(itertools.islice(prod, (n-1)))
    
    # make up any shortfall (can potentially be caused by repeated passwords in the product) 
    while(len(allCombinations)<(n-1)):
        new_pw = generateMakeupPassword(len(truePassword))
        if new_pw != truePassword:
            allCombinations.append(new_pw)
    
    # add true password, shuffle and return
    allCombinations.append(truePassword)
    random.shuffle(allCombinations)
    return allCombinations
    
def generateSweetNibble(word, n, digits, uprwords, symbols, prwords):
    if (word in digits) or (word in uprwords):
        if detectPattern(word):
            return generatePattern(word,n)
        else:
            return generateRandomWord(word,n)
    elif word in symbols:
        return generateSymbols(word,n)
    elif word in prwords:
        return generateRandomCapitalized(word,n)
    return []

def breakdownPassword(pw):
    l = re.split("(\d+)|([a-zA-Z]+)",pw)
    splitWords = [x for x in l if (x and (x is not None))]
    
    digits, uprwords, symbols, prwords = [], [], [], []
    for x in splitWords:
        if(x.isdigit()):
            digits.append(x)
        elif(x.isalpha()):
            if(isPronounceable(x)):
                prwords.append(x)
            else:
                uprwords.append(x)
        else:
            symbols.append(x)
    return digits, uprwords, symbols, prwords, splitWords



############################
#      SYMBOLS
############################
def generateSymbols(word, n):
    if n==1:
        return [word]
    # assume there's only 1 symbol. can improve algorithm by using multiple symbols
    symbolList = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '?', '<', '>', ',', '.', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '\'', '\\', ':', ';', '"', '/', '|', '`']
    symbolList.remove(word[0])
    outputList = symbolList[0:10]
    random.shuffle(outputList)
    outputList.insert(0, word)
    return list(itertools.islice(outputList, n))



###########################################
#    RANDOM CHARACTERS/DIGITS
###########################################
def generateMakeupPassword(length):
    return ''.join(random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits, length))
    
def generateRandomWord(word, n):
    if (n==1):
        return [word]
    charset = ''
    if bool(re.compile('[A-Z]').search(word)):
        charset = charset + string.ascii_uppercase
    if bool(re.compile('\d').search(word)):
        charset = charset + string.digits
    if (not charset) or bool(re.compile('[a-z]').search(word)):
        charset = charset + string.ascii_lowercase
    
    charArray = []
    while n > 1:
        newWord =  ''.join(random.choice(charset) for _ in range(len(word)))
         # repetitions are allowed as we generate random strings in the recombination step
        charArray.append(newWord)
        n -=1
    # this ensures only unique values are returned, as otherwise there are infinite patterns possible    
    charArray = list(set(charArray))
    if word in charArray:
        charArray.remove(word)
    charArray.insert(0, word)
    return charArray
    
    
###########################################
#    PATTERNS OF CHARACTERS/DIGITS
###########################################
def generatePattern(word, n):
    if n==1:
        return [word]
    # generates n randomized pattern words
    patternArray = []
    while n > 1:
        newWord = random.choice([generateSequence, generateRepeatingPattern])(word)
        # repetitions are allowed to avoid possible infinite loop
        patternArray.append(newWord)
        n -=1
    # this ensures only unique values are returned, as otherwise there are infinite patterns possible    
    patternArray = list(set(patternArray))
    if word in patternArray:
        patternArray.remove(word)
    patternArray.insert(0, word)
    return patternArray

# generate a sequence based on word
def generateSequence(word):
    if word[0] in list('01234567890'):
        chars = '01234567890'
    else:
        chars = 'abcdefghijklmnopqrstuvwxyz'
    
    if(len(word)>=len(chars)):
        return chars
    
    start_pt = random.randint(0,(len(chars)-len(word)))   
    seq = chars[start_pt:start_pt + len(word)]
    return seq[::random.choice([1,-1])]

# generate a repeating pattern based on word
def generateRepeatingPattern(word):
    letters = string.lowercase
    digits = string.digits
    length = len(word)
    repMax = math.floor(length/2)
    repMin = 1
    if repMax<=repMin:
        repFactor = 1
    else:
        repFactor = random.randrange(repMin, repMax, 1)
    substring = []
    for x in range(0, repFactor):
        if word[x] in digits:
            char = random.choice(digits)
        else:
            char = random.choice(letters)
        substring.append(char)
    substring = ''.join(substring)
    newWord = substring * length
    return newWord[:length]

def detectPattern(word):
    if (detectRepetitivePattern(word) | detectSequencePattern(word)):
        return True
    return False

def detectSequencePattern(word):
    asc = [ord(l) for l in list(word)]
    desc = list(reversed(asc))
    combined = map(add,asc,desc)
    return (len(set(combined)) <= 1)

def detectRepetitivePattern(word):
    # returns true if there is a pattern or repetition of characters 
    # returns false if there is no repetition of characters
    r = re.compile(r"(.+?)\1+").findall(word)
    if(len(r)==0):
        return False
    repetitionArr =  r[0]
    if len(repetitionArr) > 0:
        return True
    else:
        return False


####################################
#      PRONOUNCEABLE WORDS
####################################

def generateRandomCapitalized(word, n):
    if n==1:
        return [word]
    allCapitalizations = list(''.join(t) for t in itertools.product(*zip(word.lower(), word.upper())))
    random.shuffle(allCapitalizations)
    wordList = list(itertools.islice(allCapitalizations, (n-1)))
    wordList.insert(0,word)
    return wordList

VOWELS = "aeiou"
PHONES = ["bl","br","ch","cl","cr","dr","fl","fr","gl","gr","pl","pr","sc","sh","sk","sl","sm","sn","sp","st","sw","th","tr","tw","wh","wr","sch","scr","shr","sph","spl","spr","squ","str","thr"]

# Used only as a heuristic since we are not allowed to use dictionaries.
# Reference: http://stackoverflow.com/questions/18717536/in-python-how-can-i-distinguish-between-a-human-readible-word-and-random-string
def isPronounceable(word):
    if word:
        consecutiveVowels = 0
        consecutiveConsonents = 0
        for idx, letter in enumerate(word.lower()):
            vowel = True if letter in VOWELS else False

            if idx:
                prev = word[idx-1]               
                prevVowel = True if prev in VOWELS else False
                if not vowel and letter == 'y' and not prevVowel:
                    vowel = True

                if prevVowel != vowel:
                    consecutiveVowels = 0
                    consecutiveConsonents = 0

            if vowel:
                consecutiveVowels += 1
            else:
                consecutiveConsonents +=1

            if consecutiveVowels >= 3 or consecutiveConsonents > 3:
                return False

            if consecutiveConsonents == 3:
                subStr = word[idx-2:idx+1]
                if any(phone in subStr for phone in PHONES):
                    consecutiveConsonents -= 1
                    continue    
                return False                

    return True

# generateSweetWords('axsx138abcd$tower', 100)
# generateSweetWords('abcdefghijklmn1Hello$cqeY', 100)
# generateSweetWords('1password', 10)
