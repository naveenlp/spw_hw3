# -*- coding, utf-8 -*-
"""
Created on Wed Oct 14 21,29,04 2015

@author, nghiatran
"""

import random

### This module contains utility functions that generate random words, characters
first_letter_probs=[('e', 0.18), ('t', 0.15), ('a', 0.15), ('o', 0.14), ('i', 0.10), ('n' , 0.10), ('s', 0.05), ('r', 0.05),('d', 0.04), ('u',0.02),('c',0.02)]
letter_cond_probs ={
'a' : [('n' , 0.4), ('t', 0.25), ('s', 0.20), ('l', 0.1), ('r', 0.05)],
'b' : [('e' , 0.3), ('o', 0.3), ('u', 0.2), ('l', 0.2)],
'c' : [('o' , 0.3), ('h', 0.3), ('a', 0.2), ('e', 0.2)],
'd' : [('e' , 0.3), ('i', 0.3), ('a', 0.2), ('t', 0.2)],
'e' : [('r' , 0.3), ('s', 0.3), ('n', 0.2), ('d', 0.2)],
'f' : [('o' , 0.3), ('t', 0.3), ('i', 0.2), ('e', 0.2)],  
'g' : [('e' , 0.3), ('a', 0.3), ('h', 0.2), ('o', 0.2)],
'h' : [('e' , 0.5), ('a', 0.2), ('o', 0.2), ('o', 0.1)],
'i' : [('n' , 0.3), ('t', 0.3), ('s', 0.2), ('c', 0.2)],
'j' : [('u' , 0.3), ('o', 0.3), ('a', 0.2), ('e', 0.2)],
'k' : [('e' , 0.3), ('i', 0.3), ('s', 0.2), ('a', 0.2)],
'l' : [('e' , 0.3), ('l', 0.3), ('i', 0.2), ('a', 0.2)],
'm' : [('a' , 0.3), ('o', 0.3), ('i', 0.2), ('p', 0.2)],
'n' : [('t' , 0.3), ('d', 0.3), ('g', 0.2), ('e', 0.2)],
'o' : [('n' , 0.3), ('r', 0.3), ('u', 0.2), ('f', 0.2)],
'p' : [('e' , 0.3), ('a', 0.3), ('a', 0.2), ('o', 0.2)],
'q' : [('u' , 0.9), ('a', 0.1)],
'r' : [('e' , 0.3), ('o', 0.3), ('a', 0.2), ('i', 0.2)],
's' : [('t' , 0.3), ('e', 0.3), ('a', 0.2), ('i', 0.2)],
't' : [('h' , 0.3), ('o', 0.3), ('i', 0.2), ('e', 0.2)],
'u' : [('r' , 0.3), ('s', 0.3), ('n', 0.2), ('t', 0.2)],
'v' : [('e' , 0.3), ('i', 0.3), ('a', 0.2), ('o', 0.2)],
'w' : [('a' , 0.3), ('i', 0.3), ('e', 0.2), ('h', 0.2)],
'x' : [('p' , 0.3), ('t', 0.3), ('i', 0.2), ('a', 0.2)],
'y' : [('o' , 0.3), ('s', 0.3), ('a', 0.2), ('t', 0.2)],
'z' : [('e' , 0.3), ('a', 0.3), ('i', 0.2), ('o', 0.2)]
}

#generate a random letter based on the specified frequencies
def simple_random_letter(freqs):
    cummulative_freqs = [0]
    for i in range(len(freqs)):
        cummulative_freqs.append(cummulative_freqs[i] + freqs[i][1])
    rand_numb = random.uniform(0,cummulative_freqs[-1])
    low = 0
    high = len(cummulative_freqs)-1
    while True:
        if low == high - 1:
            break
        mid = (low+high)/2
        if rand_numb <= cummulative_freqs[mid] :
            high =mid
        else: 
            low = mid
    return freqs[low][0]
                
            
def random_markov_letter(prev_char):
    return simple_random_letter(letter_cond_probs[prev_char])

## generate a random password using 1st order Markov model
def random_markov_password(length):
    first_letter= simple_random_letter(first_letter_probs)
    i=1
    p = ""+first_letter
    while i < length:
        p = p + random_markov_letter(p[i-1])
        i = i +1
    return p
    
print random_markov_letter('f')
print random_markov_password(6)

    

