# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 19:40:10 2015

@author: nghiatran
"""
from string import ascii_letters, ascii_lowercase, digits
import math
import sys
reload(sys)  
sys.setdefaultencoding('utf8')



ngrams = {};
first_letter_counts ={};
character_set = ascii_lowercase + digits + punctuation
for c1 in character_set:
    first_letter_counts[c1] = 0
    for c2 in character_set:
        ngrams[c1+c2]=0.0
        
length = 5*pow(10,6)
f = open("rockyou-withcount.txt")
if length is not None:
    for i in range(length):
        line=f.next().strip()
        t = line.split()
        if len(t) <2:
            continue
        pw = t[1]
        try:
            pw.decode("ascii")
        except Exception:
            continue
        pw = pw.lower();
        
        if pw[0] in first_letter_counts:
            first_letter_counts[pw[0]] += 1

        for i in range(len(pw)-1):
            if pw[i:i+2] in ngrams: 
                ngrams[pw[i:i+2]] +=1
f.close()


first_letters_file=open('first_letters.p', 'wb')
bigrams_file=open('bigrams.p', 'wb')
pickle.dump(first_letter_counts,first_letters_file)
pickle.dump(ngrams,bigrams_file)
first_letters_file.close()
bigrams_file.close()
