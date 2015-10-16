# most of the passwords seem to have some meaning
# we cannot use a dictionary according to the problem statement
# this means, if we were to generate random characters, it will be easily possible to identify the correct password
# so we prioritize modifying any digits as the first option, modifying unpronouncable characters as the second option
# capitalizing letters as second option, replacing symbols as the third option, generate fake passwords as the last option (only to make up numbers)
# we split the input password into groups of digits, characters and symbols and apply the above on the groups thus formed

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
import string
import math
   


############################
#      CORE LOGIC
############################
DIGITS, UPRWORDS, SYMBOLS, PRWORDS = [],[],[],[]

def generateSweetWords(truePassword, n):
    # we make the assumption n is not too large (~1000). 
    # else, we might have to precisely count the number of generated values from each component in sortedWords  
    DIGITS, UPRWORDS, SYMBOLS, PRWORDS, allWords = breakdownPassword(pw)
    sortedWords = DIGITS + UPRWORDS + SYMBOLS + PRWORDS
    
    sweetWordsHash = {}
    for w in sortedWords:
        sweetWordsHash[w] = generateSweetWord(w, n)
            
    # to recombine, first we generate an array of arrays of the generated sweetword bits
    sweetWordsSorted = []
    for a in allWords:
        sweetWordsSorted.append(sweetWordsHash[a])
        
    # then we get a cartesian product of the splatted array    
    allCombinations = [''.join(p) for p in list(itertools.islice(itertools.product(*sweetWordsSorted), (n-1)))]
    
    # uncomment after completion    
    # if(len(allCombinations)<(n-1)):
    #      allCombinations.append(generatePattern('112233', (n-1)-len(allCombinations)))
    
    # add true password, shuffle and return
    allCombinations.append(truePassword)
    return random.shuffle(allCombinations)
    
def generateSweetWord(word, n):
    if word in DIGITS:
        return generateSweetDigits(word,n)
    elif word in UPRWORDS:
        return generateSweetUprWords(word,n)
    elif word in SYMBOLS:
        return generateSweetSymbols(word,n)
    elif word in PRWORDS:
        return generateSweetPrwords(word,n)
    return []

def breakdownPassword(pw):
    l = re.split("(\d+)|([a-zA-Z]+)",pw)
    splitWords = [x for x in l if (x and (x is not None))]
    
    digits, uprWords, symbols, prWords = [], [], [], []
    for x in splitWords:
        if(x.isdigit()):
            digits.append(x)
        elif(x.isalpha()):
            if(isPronounceable(x)):
                prWords.append(x)
            else:
                uprWords.append(x)
        else:
            symbols.append(x)
    return digits, uprWords, symbols, prWords, splitWords




############################
#      SYMBOLS
############################
def generateSweetSymbols(word, n):
    # assume there's only 1 symbol. can improve algorithm by using multiple symbols
    list = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '\'', '\\', ':', ';', '"', '<', '>', ',', '.', '?', '/', '|']
    list.remove(word)
    return itertools.islice(random.shuffle(list), n)

###########################
#    PATTERNS
###########################
def detectPattern(string):
    ## returns true if there is a pattern or repetition of characters 
    ## returns false if there is no repetition of characters
    r = re.compile(r"(.+?)\1+")
    repetitionArr =  r.findall(string)[0]
    print "repetition Arr", repetitionArr
    if len(repetitionArr) > 0:
        return True
    else:
        return False

def generatePattern(word, n):
    #  TODO ensure this can handle both patterns
    ## generates a randomized pattern of n words
    ## this detects the length of the word, and then creates a repeat factor between 1 and the floor of lenght/2
    ## it then randomly generates a letter or digit (depending on whether the original word had a letter or digit)
    ## and appends this to a substring
    ## it then multiplies this substring by the length of the word to ensure adequate coverage, and a repeating pattern
    ## then, it splices this repeating pattern by the length of the word to get a patterned word of same length
    letters = string.lowercase
    digits = string.digits
    lengthString = len(word)
    patternArray = []
    i = 0
    repMax = math.floor(lengthString/2)
    repMin = 1
    while n > 0:
        repFactor = random.randrange(repMin, repMax, 1)
        substring = []
        for x in range(0, repFactor):
            if word[x] in digits:
                char = random.choice(digits)
            else:
                char = random.choice(letters)
            substring.append(char)
        substring = ''.join(substring)
        newWord = substring * lengthString
        newWord = newWord[:lengthString]
        patternArray.append(newWord)
        n -=1
    return patternArray

# ###########################
# #      NUMBERS
# ###########################
# def replacementNumbers(digits):
#     if(hasPattern(digits)):
#         return generatePattern(digits)
#     else if(isDate(digits)):
#         return generateDate(len(digits))
#     else:
#         return generateRandomDigits(len(digits))

# we could additionally check for a date pattern to improve the algorithm

# def generateRandomDigits(length):
#     return ''.join(random.choice(string.lowercase) for i in range(length))




# ###########################
# #      WORDS
# ###########################

# def replacementWord(word):
#     repl = ''
#     if(isPronounceable(word)):
#         repl = generatePronounceableWord(len(word))
#     else if(hasPattern(word)):
#         repl = generateDate(len(digits))
#     else:
#         repl = generateRandomDigits(len(digits))
#     return capitalizeRandomChar(word, repl)

def countCapitalChar(word):
    capsCount = len(re.findall(r'[A-Z]',word))
    onlyFirst = ((word[0].isupper()) & (capsCount==1))
    return capsCount, onlyFirst

def capitalizeRandomChar(original, word):
    count, onlyFirstLetter = countCapitalChar(original)
    
    if(count==0):
        return word
        
    if(onlyFirstLetter):
        return word.capitalize()
    
    letters = list(word)
    wordSize = len(letters)
    ncap = min(random.randint(0,count), wordSize)
    for i in random.sample(range(0, len(letters)), ncap):
        letters[i] = letters[i].upper()
    return ''.join(letters)

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
