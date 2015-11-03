# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:47:17 2015

@author: nghiatran
"""
from __future__ import division
import math
import pickle
from string import ascii_lowercase, digits, punctuation

## Define character set
character_set = ascii_lowercase + digits + punctuation

first_letters_file=open('first_letters.p', 'r')
bigrams_file=open('bigrams.p', 'r')

first_letters = pickle.load(first_letters_file)
bigrams = pickle.load(bigrams_file)

n = sum(first_letters.values())
first_letters_freqs = {}
for i in first_letters.keys():
    first_letters_freqs[i] = first_letters[i]/n

conditional_probs={}
for c1 in character_set:
    count =0;
    conditional_probs[c1] = {}
    for c2 in character_set: 
        count += bigrams[c1+c2]
    for c2 in character_set:
        conditional_probs[c1][c2] = bigrams[c1+c2] / count


def bigram_based_likelihood(pw):
    lowercased_pw = pw.lower()
    likelihood = first_letters_freqs[lowercased_pw[0]]
    for i in range(1,len(lowercased_pw)):
        likelihood *= conditional_probs[lowercased_pw[i-1]][lowercased_pw[i]]
    ##todo: need to multiply with the likelihood of the given length
    ## likelihood *= prob(a password's length is len(pw))
    return likelihood
    
    