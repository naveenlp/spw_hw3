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

## Frequencies of password lengths. 
## These numbers can be obtained from passwords in the Rockyou database.
## A caveat is that Rockyou allowed for passwords with length less than 8.
## This does not reflect the current industry standard.
###########################
length_freqs = {6: 0.05, 7: 0.05, 8: 0.3, 9: 0.2, 10: 0.1, 11: 0.1, 12: 0.1, 13: 0.1}

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
    likelihood *= length_freqs[len(lowercased_pw)]
    return likelihood
    
    