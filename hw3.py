# most of the passwords seem to have some meaning
# we cannot use a dictionary according to the problem statement
# this means, if we were to generate random characters, it will be easily possible to identify the correct password
# so we prioritize modifying any digits as the first option, modifying unpronouncable characters as the second option
# modifying symbols as the third option, capitalizing letters as last option
# we then generate random patterns for passwords as the last option (only to make up numbers)
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

############################
#      CORE LOGIC
############################
DIGITS, UPRWORDS, SYMBOLS, PRWORDS = [],[],[],[]

def generateSweetWords(truePassword, n):
    # we make the assumption n is not too large (~1000). 
    # else, we might have to precisely count the number of generated values from each component in sortedWords  
    DIGITS, UPRWORDS, SYMBOLS, PRWORDS, allWords = breakdownPassword(truePassword)
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
    
    # TODO uncomment after completion and ensure true password does not get added from the above. also, for each generator, ensure values are unique
    # if(len(allCombinations)<(n-1)):
    #      allCombinations.append(generatePattern(truePassword, (n-1)-len(allCombinations)))
    
    # add true password, shuffle and return
    allCombinations.append(truePassword)
    random.shuffle(allCombinations)
    return allCombinations
    
def generateSweetWord(word, n):
    if (word in DIGITS) or (word in UPRWORDS):
        if detectPattern(word):
            return generatePattern(word,n)
        else:
            return generateRandom(word,n)
    elif word in SYMBOLS:
        return generateSweetSymbols(word,n)
    elif word in PRWORDS:
        return generateRandomCapitalized(word,n)
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



###########################################
#    RANDOM CHARACTERS/DIGITS
###########################################
def generateRandom(word, n):
    charset = ''
    if bool(re.compile('[A-Z]').search(word)):
        charset = charset + string.ascii_uppercase
    if bool(re.compile('\d').search(word)):
        charset = charset + string.digits
    if (not charset) or bool(re.compile('[a-z]').search(word)):
        charset = charset + string.ascii_lowercase
    
    patternArray = []
    while n > 0:
        newWord =  ''.join(random.choice(charset) for _ in range(len(word)))
         # repetitions are allowed as we generate random strings in the recombination step
        patternArray.append(newWord)
        n -=1
        
    return patternArray
    
    
###########################################
#    PATTERNS OF CHARACTERS/DIGITS
###########################################
def generatePattern(word, n):
    ## generates n randomized pattern words
    patternArray = []
    while n > 0:
        newWord = random.choice([generateSequence, generateRepeatingPattern])(word)
        # repetitions are allowed as we generate random strings in the recombination step
        patternArray.append(newWord)
        n -=1
    
    return patternArray

# generate a sequence based on word
def generateSequence(word):
    chars = random.choice('1234567890','abcdefghijklmnopqrstuvwxyz')
    
    if(len(word)>=len(chars)):
        return chars
    
    start_pt = random.randint(0,(len(chars)-len(word)))   
    seq = chars[start_pt:start_pt + len(word)]
    return seq[::random.choice([1,-1])]

# generate a repeating pattern based on word
def generateRepeatingPattern(word):
    letters = word.lowercase
    digits = word.digits
    length = len(word)
    repMax = math.floor(length/2)
    repMin = 1
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
    combined = map(operator.add,asc,desc)
    return (len(set(combined)) <= 1)

def detectRepetitivePattern(word):
    ## returns true if there is a pattern or repetition of characters 
    ## returns false if there is no repetition of characters
    r = re.compile(r"(.+?)\1+")
    repetitionArr =  r.findall(word)[0]
    print "repetition Arr", repetitionArr
    if len(repetitionArr) > 0:
        return True
    else:
        return False


####################################
#      PRONOUNCEABLE WORDS
####################################

def generateRandomCapitalized(word, n):
    allCapitalizations = list(''.join(t) for t in itertools.product(*zip(word.lower(), word.upper())))
    random.shuffle(allCapitalizations)
    return list(itertools.islice(allCapitalizations, n))

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
