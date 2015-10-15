__author__ = 'claireopila'

import string
import random
import math
import numpy as np

"""Make passwordswithout files"""

def makePassword1(password):
  ## this algorithm breaks up inputs into vowels and consonants by
  ## uppercase and lowercase, and numbers and punctuation
  ## inputs defined here
  vowels = ['a', 'e', 'i', 'o', 'u']
  cons = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', \
        'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
  vowelsUpper = ['A', 'E', 'I', 'O', 'U']
  consUpper = ['B', 'C', 'D','F', 'G', 'H', 'J', 'K', \
  'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
  digits = string.digits
  symbols = string.punctuation
  ## gets the length of the password inputh here
  lenPass = len(password)
  j = 0
  newPass = [ ]
  ## creates a new password of equivalent length
  while j < len(password):
  ## if the char in vowels,
  ##replace char with a newChar randomly selected from lowercase vowels
    if password[j] in vowels:
      newChar = random.choice(vowels)
  ## if the char in vowelsUpper,
  ##replace char with a newChar randomly selected from uppercase vowels
    elif password[j] in vowelsUpper:
      newChar = random.choice(vowelsUpper)
  ## if the char in cons
  ##replace char with a newChar randomly selected from lowercase consonants
    elif password[j] in cons:
      newChar = random.choice(cons)
  ## if the char in consUpper
  ##replace char with a newChar randomly selected from uppercase consonants
    elif password[j] in consUpper:
      newChar = random.choice(consUpper)
  ## if the char in digits
  ##replace char with a newChar randomly selected from digits
    elif password[j] in digits:
      newChar = random.choice(digits)
    else:
  ##otherwise it is a symbol, replace with a rnadomly selected symbol
      newChar = random.choice(symbols)
    newPass.append(newChar)
    j += 1
  newPass = ''.join(newPass)
  return newPass

def find_nearest(value):
  letterFreq = np.array([0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047, 0.0357,
    0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116, 0.0169, 0.0028,
          0.0164, 0.000])
  arrayIndices = np.where(np.logical_and(letterFreq >= (value - 0.02), letterFreq <= (value + 0.02)))
  # print "arrayIndices", arrayIndices
  # print "arrayindices", arrayIndices[0]
  letterChoice = random.choice(arrayIndices[0])
  return letterChoice

def makePassword2(password):
  ## this algorithm breaks up inputs into vowels and consonants by
  ## uppercase and lowercase, and numbers and punctuation
  ## inputs defined here
  alphaFreq = [0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047, 0.0357,
    0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116, 0.0169, 0.0028,
          0.0164, 0.000]
  lowerCase = string.lowercase
  upperCase = string.uppercase
  digits = string.digits
  symbols = string.punctuation
  ## gets the length of the password inputh here
  lenPass = len(password)
  newPass = [ ]
  ## creates a new password of equivalent length
  for char in password:
  ## if the char in vowels,
  ##replace char with a newChar randomly selected from lowercase vowels
    if char in lowerCase:
      numChar = ord(char)%97
      letterFreq = alphaFreq[numChar]
      ## finds an index position of letterfreq array to use randomly selected from range of values close to the frequency fo letter in question
      letterIndex= find_nearest(letterFreq)
      letterIndex += 97
      newChar = chr(letterIndex)

  ## if the char in vowelsUpper,
  ##replace char with a newChar randomly selected from uppercase vowels
    elif char in upperCase:
      numChar = ord(char)%65
      letterFreq = alphaFreq[numChar]
      ## finds an index position of letterfreq array to use randomly selected from range of values close to the frequency fo letter in question
      letterIndex= find_nearest(letterFreq)
      letterIndex += 65
      newChar = chr(letterIndex)
  ## if the char in digits
  ##replace char with a newChar randomly selected from digits
    elif char in digits:
      newChar = random.choice(digits)
    else:
  ##otherwise it is a symbol, replace with a rnadomly selected symbol
      newChar = random.choice(symbols)
    newPass.append(newChar)
  newPass = ''.join(newPass)
  return newPass

# print makePassword2("passWord123")
# print makePassword2("may8fifth89")

def makePassword3(password):
  ## makes a new password by keeping all letters the same
  ## swaps out numbers for new numbers by adding 1
  ## swaps out punctuation by randomly selecting punctuation
  letters = string.letters
  digits = string.digits
  punct = string.punctuation
  newPass = []
  for char in password:
  ## checks to see if the char is a digit, if so, adds 1 to it
    if char in digits:
        numChar = int(char)
        numCharNext = random.choice(digits)
        newChar = str(numCharNext)
    ## checks to see if the char is puncuation, if so, swaps out for a
    ## randomly selected punctuation
    elif char in punct:
      if char == "~":
        newChar = "!"
      else:
        newChar = random.choice(punct)
    else:
    ## if it is not a number or punctuation, keep the letter the same.
      newChar = char
    newPass.append(newChar)
  newPass = "".join(newPass)
  return newPass


def generateList(n, password):
  ## generates a list of passwords of size n, based on an input "password"
  pwList = [ ]
  digits = string.digits

  while n > 0:
    newPassword = makePassword3(password)
    pwList.append(newPassword)
    n -= 1
  pwList.insert(int(random.choice(digits)), password)
  for pw in pwList:
    print pw
  return pwList
#
generateList(10, "!Ciquser1")



"""Make Passwords with high prob file"""


def read_password_files(filename):
    """
    Return a list of passwords in all the password file(s), plus
    a proportional (according to parameter q) number of "noise" passwords.
    """
    pw_list = [ ]

    f = open(filename)
    text = f.read()
    f.close()
    lines= text.split()
    for line in lines:
      pw_list.extend( line.split() )
    # # add noise passwords
    # pw_list.extend( noise_list(int(q*len(pw_list))) )
    return pw_list


def make_password(L, tempPW):
    """
    make a random password like those in given password list
    """

    # start by choosing a random password from the list
    # # save its length as k; we'll generate a new password of length k
    # k = len(tempPW)
    # print "tempPW", tempPW
    # print "lentempPW", k
    # # create list of all passwords of length k; we'll only use those in model
    # L = [ pw for pw in pw_list if len(pw) == k ]
    # print "list of same length password", L
    k = len(tempPW)
    nL = len(L)
    print "nL", nL
    # start answer with the first char of that random password
    # row = index of random password being used
    row = random.randrange(nL)
    ans = L[row][:1]                  # copy first char of L[row]
    # print "ans", ans
    j = 1                             # j = len(ans) invariant
    while j < k:
      LL = [ i for i in range(nL) if L[i][j-1]==ans[-1] ]
      ## find all words with the same char of the last char added to answer
      ## randomly choose the index position of one of these words
      ## Then, add the char in this word next to the last char used in ans
      row = random.choice(LL)
      print "row", row
      ans = ans + L[row][j]
      j = j + 1
    return ans


pw_list = read_password_files("highProbPw.txt")
# print "make_passwords",  make_password(pw_list)

def generate_passwords( n, pw_list ):
    """ print n passwords and return list of them """
    tempPW = random.choice(pw_list)
    k = len(tempPW)
    L = [ pw for pw in pw_list if len(pw) == k ]

    ans = [ ]
    for t in range( n ):
        pw = make_password(L, tempPW)
        # print "pw", pw
        ans.append( pw )
    for pw in ans:
      print pw
    return ans

# generate_passwords(10, pw_list)




